#!/usr/bin/env python3
"""
Gradio web UI for the AI video restoration pipeline.

Run on the RunPod pod:
    python app.py

Then open the pod's HTTP port (7860) via the RunPod "Connect" panel.
It launches with share=True so you also get a public gradio.live link.
"""

import os
import subprocess
import sys
import time

import gradio as gr

HERE = os.path.dirname(os.path.abspath(__file__))
RESTORE = os.path.join(HERE, "restore.py")
OUT_DIR = os.path.join(HERE, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)


def restore_video(video_path, server_path, target_height, fps_mode, upscale,
                  face_fidelity, denoise, deinterlace, grade_strength):
    """Generator: streams the pipeline log, then yields the finished video."""
    # Prefer a file already on the pod — avoids slow/flaky browser upload of big files.
    src = (server_path or "").strip() or video_path
    if not src:
        yield "Upload a video, or paste the path to a video already on the pod.", None
        return
    if not os.path.isfile(src):
        yield f"File not found on the pod: {src}", None
        return
    video_path = src

    stamp = str(int(time.time()))
    out_path = os.path.join(OUT_DIR, f"restored_{stamp}.mp4")

    cmd = [
        sys.executable, RESTORE,
        "--input", video_path,
        "--output", out_path,
        "--target-height", str(int(target_height)),
        "--fps", "60" if fps_mode == "Smooth 60fps" else "0",
        "--upscale", str(int(upscale)),
        "--face-fidelity", str(face_fidelity),
        "--denoise", str(denoise),
        "--grade-strength", str(grade_strength),
    ]
    if deinterlace:
        cmd.append("--deinterlace")

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, bufsize=1)

    buffer = []
    for line in proc.stdout:
        buffer.append(line.rstrip())
        # keep the log readable: show the tail
        yield "\n".join(buffer[-40:]), None
    proc.wait()

    if proc.returncode == 0 and os.path.isfile(out_path):
        buffer.append(f"\n✅ Finished: {out_path}")
        yield "\n".join(buffer[-40:]), out_path
    else:
        buffer.append(f"\n❌ Failed (exit {proc.returncode}). See log above.")
        yield "\n".join(buffer[-40:]), None


with gr.Blocks(title="AI Video Restoration") as demo:
    gr.Markdown(
        "# 🎬 AI Video Restoration\n"
        "Upscale, restore, smooth and cinematically grade old/low-quality video. "
        "Long videos take a while — watch the live log below."
    )
    with gr.Row():
        with gr.Column():
            inp = gr.Video(label="Source video (small files only — upload here)")
            server_path = gr.Textbox(
                label="…or path to a video already on the pod (best for big files)",
                placeholder="/workspace/myvideo.mp4",
            )
            target_height = gr.Dropdown([720, 1080, 1440, 2160], value=1080, label="Output height")
            fps_mode = gr.Radio(["Smooth 60fps", "Keep source fps"], value="Smooth 60fps",
                                label="Motion")
            with gr.Accordion("Advanced", open=False):
                upscale = gr.Radio([2, 4], value=2, label="AI upscale factor (4 = very low-res sources)")
                face_fidelity = gr.Slider(0.0, 1.0, value=0.7, step=0.05,
                                          label="Face fidelity (0 = max restore, 1 = faithful)")
                denoise = gr.Slider(0.0, 1.0, value=0.4, step=0.1, label="Denoise strength")
                deinterlace = gr.Checkbox(False, label="Deinterlace (old camcorder footage)")
                grade_strength = gr.Slider(0.0, 1.2, value=0.6, step=0.1,
                                           label="Cinematic grade strength")
            go = gr.Button("Restore ▶", variant="primary")
        with gr.Column():
            out_video = gr.Video(label="Result")
            logbox = gr.Textbox(label="Live log", lines=20, max_lines=20)

    go.click(
        restore_video,
        inputs=[inp, server_path, target_height, fps_mode, upscale, face_fidelity,
                denoise, deinterlace, grade_strength],
        outputs=[logbox, out_video],
    )

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=True)
