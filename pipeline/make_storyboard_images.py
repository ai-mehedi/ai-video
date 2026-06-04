#!/usr/bin/env python3
# ============================================================================
#  STORYBOARD IMAGE GENERATOR (fal.ai) — makes START + END frame for every shot.
#  Cheap (~$0.025/image FLUX Dev). Output: 02_keyframes/shot_01_start.png, _end.png ...
#  Then you upload these to Google Flow (first frame / last frame) and make the video.
#
#  SETUP (runs anywhere — even your laptop, no GPU needed):
#     pip install fal-client requests
#     export FAL_KEY="your-fal-key"        # free key from https://fal.ai (Dashboard → Keys)
#
#  RUN:
#     python pipeline/make_storyboard_images.py            # all shots, both frames
#     python pipeline/make_storyboard_images.py 03         # only shot 03
#     python pipeline/make_storyboard_images.py 03 start   # only shot 03 start frame
# ============================================================================
import os, sys, csv, urllib.request
import fal_client

sys.path.insert(0, os.path.dirname(__file__))
import config as C

if not os.environ.get("FAL_KEY"):
    print("[!] No FAL_KEY set.  Run:  export FAL_KEY=\"your-key\"  (free at https://fal.ai)")
    sys.exit(1)

os.makedirs(C.STORYBOARD_DIR, exist_ok=True)
only_shot  = sys.argv[1] if len(sys.argv) > 1 else None
only_frame = sys.argv[2] if len(sys.argv) > 2 else None   # "start" or "end"

with open(C.STORYBOARD_CSV, newline="", encoding="utf-8") as f:
    shots = list(csv.DictReader(f))
print(f"Loaded {len(shots)} shots from {C.STORYBOARD_CSV}")

def build_prompt(frame_desc):
    # CHARACTER (same every frame = consistent face) + the frame description + realism style
    return ", ".join(p for p in [C.CHARACTER, frame_desc, C.STYLE] if p and p.strip())

def generate(prompt, out_path, seed):
    print(f"  -> {out_path}")
    result = fal_client.subscribe(
        C.FAL_MODEL,
        arguments={
            "prompt": prompt,
            "image_size": C.FAL_IMAGE_SIZE,
            "num_inference_steps": C.FAL_STEPS,
            "guidance_scale": C.FAL_GUIDANCE,
            "seed": seed,
            "num_images": 1,
        },
    )
    url = result["images"][0]["url"]
    urllib.request.urlretrieve(url, out_path)

for s in shots:
    sid = s["shot_id"]
    if only_shot and sid != only_shot:
        continue
    frames = {"start": s.get("start_frame", ""), "end": s.get("end_frame", "")}
    for fname, desc in frames.items():
        if only_frame and fname != only_frame:
            continue
        if not desc.strip():
            continue
        out = os.path.join(C.STORYBOARD_DIR, f"shot_{sid}_{fname}.png")
        print(f"\n=== Shot {sid} [{fname}] ===")
        # fixed seed per shot+frame = same character look, reproducible
        seed = (int(sid) * 100) + (1 if fname == "start" else 2)
        generate(build_prompt(desc), out, seed)

print("\n✅ Done. Frames in", C.STORYBOARD_DIR)
print("Next: upload each shot's start/end frames to Google Flow → generate the video shot.")
print("Re-roll one frame:  python pipeline/make_storyboard_images.py 03 start")
