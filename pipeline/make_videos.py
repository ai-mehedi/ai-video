#!/usr/bin/env python3
# ============================================================================
#  STAGE 2 — MAKE VIDEOS.  Animates each keyframe into a short clip.
#  This is the stage where you JUDGE VIDEO QUALITY (free Wan vs paid later).
#
#  RUN:  python pipeline/make_videos.py        (all shots)
#        python pipeline/make_videos.py 03      (only shot 03)
#
#  The VIDEO_ENGINE switch in config.py picks the engine:
#    "wan"  -> free, local (default)
#    "kling"/"veo" -> paid API (add later only if Wan quality is poor)
# ============================================================================
import os, sys, csv
import torch

sys.path.insert(0, os.path.dirname(__file__))
import config as C

os.makedirs(C.CLIPS_DIR, exist_ok=True)
only = sys.argv[1] if len(sys.argv) > 1 else None

with open(C.SHOT_LIST, newline="", encoding="utf-8") as f:
    shots = list(csv.DictReader(f))

def motion_prompt(s):
    # describe ONLY the movement (the keyframe already has the look)
    move = s.get("camera_move", "")
    act  = s.get("character_action", "")
    return f"{move}, {act}, natural motion, cinematic, slow"

# ---------------------------------------------------------------- WAN (free, local)
def run_wan(shots):
    from diffusers import WanImageToVideoPipeline
    from diffusers.utils import load_image, export_to_video
    print("Loading Wan 2.2 I2V... (first run downloads the model)")
    pipe = WanImageToVideoPipeline.from_pretrained(C.WAN_MODEL, torch_dtype=torch.bfloat16).to("cuda")
    for s in shots:
        sid = s["shot_id"]
        if only and sid != only: continue
        img_path = os.path.join(C.KEYFRAME_DIR, f"shot_{sid}.png")
        if not os.path.exists(img_path):
            print(f"[skip] no keyframe for shot {sid} — run make_images.py first"); continue
        out = os.path.join(C.CLIPS_DIR, f"shot_{sid}.mp4")
        print(f"\n=== Shot {sid} (Wan) ===\n{motion_prompt(s)}")
        image = load_image(img_path)
        result = pipe(image=image, prompt=motion_prompt(s),
                      negative_prompt="static, distorted, morphing, extra limbs, flicker, jitter",
                      num_frames=C.VIDEO_FRAMES, num_inference_steps=C.VIDEO_STEPS).frames[0]
        export_to_video(result, out, fps=C.VIDEO_FPS)
        print("saved ->", out)

# ---------------------------------------------------------------- PAID (later)
def run_paid(shots):
    print(f"VIDEO_ENGINE='{C.VIDEO_ENGINE}' selected — paid API.")
    print("To enable: add your API key + call code here (Kling/Veo/Runway).")
    print("Left as a stub on purpose — start free with 'wan' first.")

if __name__ == "__main__":
    if C.VIDEO_ENGINE == "wan":
        run_wan(shots)
    else:
        run_paid(shots)
    print("\n✅ Done. Clips in", C.CLIPS_DIR)
