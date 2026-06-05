#!/usr/bin/env python3
"""
AI video restoration pipeline.

Stages:
  1. Preprocess  (FFmpeg: optional deinterlace + denoise, extract frames + audio)
  2. Restore     (CodeFormer + Real-ESRGAN: super-resolution + face restoration)
  3. Assemble    (FFmpeg: restored frames -> intermediate video at source fps)
  4. Interpolate (RIFE -> 60fps; falls back to FFmpeg minterpolate if RIFE missing)
  5. Grade+Encode(FFmpeg: cinematic "HDR look" + scale to target height + mux audio)

Designed to run on a RunPod pod with a 48 GB GPU. Prints progress markers
(STAGE x/5 ...) so the Gradio app can stream them to the browser.

Run standalone:
  python restore.py --input in.mp4 --output out.mp4 --target-height 1080 --fps 60
"""

import argparse
import glob
import os
import shlex
import shutil
import subprocess
import sys
import time

# Repo locations created by setup.sh (override with env vars if you cloned elsewhere)
CODEFORMER_DIR = os.environ.get("CODEFORMER_DIR", os.path.expanduser("~/CodeFormer"))
RIFE_DIR = os.environ.get("RIFE_DIR", os.path.expanduser("~/Practical-RIFE"))


def log(msg):
    """Print immediately so the Gradio app can stream it live."""
    print(msg, flush=True)


def run(cmd, cwd=None):
    """Run a shell command, streaming its output. Raise on non-zero exit."""
    if isinstance(cmd, (list, tuple)):
        printable = " ".join(shlex.quote(str(c)) for c in cmd)
    else:
        printable = cmd
    log(f"  $ {printable}")
    proc = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str))
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): {printable}")


def probe_fps(path):
    """Return source frame rate as a float (defaults to 30 if it can't be read)."""
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", path,
        ]).decode().strip()
        num, den = out.split("/") if "/" in out else (out, "1")
        return float(num) / float(den)
    except Exception:
        log("  ! could not probe fps, assuming 30")
        return 30.0


def has_audio(path):
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=codec_type", "-of", "csv=p=0", path,
        ]).decode().strip()
        return out == "audio"
    except Exception:
        return False


# ----------------------------------------------------------------------------
# Stage 1: preprocess + extract frames
# ----------------------------------------------------------------------------
def stage_preprocess(args, work):
    log("STAGE 1/5  Preprocess (clean + extract frames)")
    frames_in = os.path.join(work, "frames_in")
    os.makedirs(frames_in, exist_ok=True)

    filters = []
    if args.deinterlace:
        filters.append("bwdif=mode=send_frame")     # deinterlace, keep fps
    if args.denoise > 0:
        # luma/chroma spatial + temporal denoise; scales with --denoise 0..1
        s = args.denoise
        filters.append(f"hqdn3d={4*s:.1f}:{3*s:.1f}:{6*s:.1f}:{4.5*s:.1f}")
    vf = ",".join(filters) if filters else "null"

    run([
        "ffmpeg", "-y", "-i", args.input,
        "-vf", vf, "-qscale:v", "2",
        os.path.join(frames_in, "%08d.png"),
    ])

    audio_path = None
    if has_audio(args.input):
        audio_path = os.path.join(work, "audio.aac")
        run(["ffmpeg", "-y", "-i", args.input, "-vn", "-c:a", "aac", "-b:a", "192k", audio_path])
    else:
        log("  (no audio track found)")

    n = len(glob.glob(os.path.join(frames_in, "*.png")))
    log(f"  extracted {n} frames")
    if n == 0:
        raise RuntimeError("No frames extracted — bad input file?")
    return frames_in, audio_path


# ----------------------------------------------------------------------------
# Stage 2: AI restore (CodeFormer w/ Real-ESRGAN background upsampler)
# ----------------------------------------------------------------------------
def stage_restore(args, work, frames_in):
    log("STAGE 2/5  AI restore (super-resolution + face restoration)")
    cf_out = os.path.join(work, "cf_out")
    os.makedirs(cf_out, exist_ok=True)

    cmd = [
        sys.executable, os.path.join(CODEFORMER_DIR, "inference_codeformer.py"),
        "-i", frames_in,
        "-o", cf_out,
        "-w", str(args.face_fidelity),     # 0 = max restoration, 1 = max fidelity to source
        "--upscale", str(args.upscale),
        "--bg_upsampler", "realesrgan",    # upscales the whole frame, not just faces
        "--face_upsample",
    ]
    run(cmd, cwd=CODEFORMER_DIR)

    # CodeFormer writes full restored frames to <out>/final_results/
    restored = os.path.join(cf_out, "final_results")
    if not glob.glob(os.path.join(restored, "*.png")):
        # fall back: search anywhere under cf_out for the frame set
        cands = glob.glob(os.path.join(cf_out, "**", "*.png"), recursive=True)
        if not cands:
            raise RuntimeError(f"CodeFormer produced no frames in {cf_out}")
        restored = os.path.dirname(cands[0])
    log(f"  restored frames in {restored}")
    return restored


# ----------------------------------------------------------------------------
# Stage 3: assemble restored frames into an intermediate video
# ----------------------------------------------------------------------------
def stage_assemble(args, work, restored_dir, src_fps):
    log("STAGE 3/5  Assemble restored frames")
    sr_video = os.path.join(work, "sr.mp4")
    run([
        "ffmpeg", "-y", "-framerate", f"{src_fps}",
        "-pattern_type", "glob", "-i", os.path.join(restored_dir, "*.png"),
        "-c:v", "libx264", "-crf", "12", "-preset", "medium",
        "-pix_fmt", "yuv420p", sr_video,
    ])
    return sr_video


# ----------------------------------------------------------------------------
# Stage 4: frame interpolation to 60 fps
# ----------------------------------------------------------------------------
def stage_interpolate(args, work, sr_video, src_fps):
    if args.fps <= 0:
        log("STAGE 4/5  Interpolation skipped (keeping source fps)")
        return sr_video, src_fps

    log(f"STAGE 4/5  Interpolate to {args.fps} fps")
    rife_script = os.path.join(RIFE_DIR, "inference_video.py")
    rife_model = os.path.join(RIFE_DIR, "train_log")

    use_rife = os.path.isfile(rife_script) and os.path.isdir(rife_model) and \
        glob.glob(os.path.join(rife_model, "*.pkl"))

    if use_rife:
        before = set(glob.glob(os.path.join(work, "*.mp4")))
        run([sys.executable, rife_script, "--video", sr_video, "--fps", str(args.fps)],
            cwd=work)
        after = set(glob.glob(os.path.join(work, "*.mp4")))
        produced = sorted(after - before)
        if produced:
            return produced[-1], args.fps
        log("  ! RIFE ran but no new file found, falling back to minterpolate")

    # Fallback: FFmpeg motion interpolation (no extra model needed)
    log("  using FFmpeg minterpolate (RIFE unavailable)")
    out = os.path.join(work, "sr60.mp4")
    run([
        "ffmpeg", "-y", "-i", sr_video,
        "-vf", f"minterpolate=fps={args.fps}:mi_mode=mci:mc_mode=aobmc:vsbmc=1",
        "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", out,
    ])
    return out, args.fps


# ----------------------------------------------------------------------------
# Stage 5: cinematic grade + scale + final encode + mux audio
# ----------------------------------------------------------------------------
def build_grade_vf(strength, target_height):
    """Build the cinematic 'HDR look' FFmpeg filter chain (SDR, plays everywhere)."""
    s = max(0.0, min(1.5, strength))
    contrast = round(1 + 0.18 * s, 4)
    saturation = round(1 + 0.22 * s, 4)
    brightness = round(0.012 * s, 4)
    gamma = round(1 - 0.04 * s, 4)
    # teal in shadows, warmth in highlights = the classic cinematic split-tone
    rs, bs = round(-0.06 * s, 4), round(0.06 * s, 4)
    rh, bh = round(0.05 * s, 4), round(-0.04 * s, 4)
    sharp = round(0.6 * s, 4)
    return (
        f"scale=-2:{target_height}:flags=lanczos,"
        f"eq=contrast={contrast}:saturation={saturation}:brightness={brightness}:gamma={gamma},"
        f"curves=preset=medium_contrast,"
        f"colorbalance=rs={rs}:bs={bs}:rh={rh}:bh={bh},"
        f"unsharp=5:5:{sharp}:5:5:0,"
        f"format=yuv420p"
    )


def stage_grade_encode(args, work, video, audio_path):
    log("STAGE 5/5  Cinematic grade + final encode")
    vf = build_grade_vf(args.grade_strength, args.target_height)

    cmd = ["ffmpeg", "-y", "-i", video]
    if audio_path:
        cmd += ["-i", audio_path]
    cmd += ["-vf", vf, "-c:v", "libx264", "-crf", str(args.crf),
            "-preset", "slow", "-pix_fmt", "yuv420p"]
    if audio_path:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-map", "0:v:0", "-map", "1:a:0", "-shortest"]
    cmd += ["-movflags", "+faststart", args.output]
    run(cmd)
    log(f"DONE  ->  {args.output}")


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="AI video restoration pipeline")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--workdir", default=None, help="scratch dir (default: alongside output)")
    ap.add_argument("--target-height", type=int, default=1080)
    ap.add_argument("--fps", type=int, default=60, help="target fps (0 = keep source)")
    ap.add_argument("--upscale", type=int, default=2, help="AI upscale factor (use 4 for very low-res sources)")
    ap.add_argument("--face-fidelity", type=float, default=0.7,
                    help="CodeFormer -w: 0=max restore, 1=stay faithful to source")
    ap.add_argument("--denoise", type=float, default=0.4, help="0=off .. 1=strong")
    ap.add_argument("--deinterlace", action="store_true", help="for old interlaced footage")
    ap.add_argument("--grade-strength", type=float, default=0.6, help="0=off .. ~1=strong cinematic")
    ap.add_argument("--crf", type=int, default=16, help="final quality, lower=better (16 ~ visually lossless)")
    ap.add_argument("--keep-work", action="store_true", help="don't delete the scratch dir")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        sys.exit(f"Input not found: {args.input}")

    work = args.workdir or (os.path.splitext(args.output)[0] + "_work")
    os.makedirs(work, exist_ok=True)
    log(f"Workdir: {work}")

    t0 = time.time()
    src_fps = probe_fps(args.input)
    log(f"Source fps: {src_fps:.3f}")

    frames_in, audio = stage_preprocess(args, work)
    restored = stage_restore(args, work, frames_in)
    sr_video = stage_assemble(args, work, restored, src_fps)
    interp_video, _ = stage_interpolate(args, work, sr_video, src_fps)
    stage_grade_encode(args, work, interp_video, audio)

    if not args.keep_work:
        shutil.rmtree(work, ignore_errors=True)

    mins = (time.time() - t0) / 60
    log(f"Total time: {mins:.1f} min")


if __name__ == "__main__":
    main()
