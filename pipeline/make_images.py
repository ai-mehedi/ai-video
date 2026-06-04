#!/usr/bin/env python3
# ============================================================================
#  STAGE 1 — MAKE IMAGES (keyframes)
#  Reads the shot list (CSV) and makes ONE image per shot, automatically.
#  Output: 02_keyframes/shot_01.png, shot_02.png, ...
#
#  RUN:   python pipeline/make_images.py
#         python pipeline/make_images.py 03      # only remake shot 03
#
#  SETUP (one time on the pod):
#     pip install -U diffusers transformers accelerate torch sentencepiece protobuf pandas
#     huggingface-cli login        # paste a free HF token, accept FLUX.1-dev license once
# ============================================================================
import os, sys, csv
import torch
from diffusers import FluxPipeline

# import settings from config.py (one folder up control)
sys.path.insert(0, os.path.dirname(__file__))
import config as C

# --- make sure output folder exists ---
os.makedirs(C.KEYFRAME_DIR, exist_ok=True)

# --- optional: only build one shot if you pass its id, e.g. "03" ---
only_shot = sys.argv[1] if len(sys.argv) > 1 else None

# --- read the shot list (the master file) ---
with open(C.SHOT_LIST, newline="", encoding="utf-8") as f:
    shots = list(csv.DictReader(f))
print(f"Loaded {len(shots)} shots from {C.SHOT_LIST}")

# --- load FLUX once (slow), then reuse for every shot ---
print("Loading FLUX model... (first time downloads ~24GB)")
pipe = FluxPipeline.from_pretrained(C.FLUX_MODEL, torch_dtype=torch.bfloat16)
pipe = pipe.to("cuda")

# --- load realism LoRA (kills plastic skin) if the file exists ---
if C.REALISM_LORA and os.path.exists(C.REALISM_LORA):
    try:
        pipe.load_lora_weights(C.REALISM_LORA)
        print(f"Realism LoRA loaded (scale {C.LORA_SCALE})")
    except Exception as e:
        print(f"[warn] could not load LoRA: {e} — continuing without it")
else:
    print("[info] no realism LoRA found — using prompt realism only")

# ============================================================================
#  Build a prompt for ONE shot by combining: character + action + scene + style
# ============================================================================
def build_prompt(shot):
    parts = [
        C.CHARACTER,                                  # same face every time
        shot.get("character_action", ""),             # what he's doing
        shot.get("location", ""),                     # where
        shot.get("time_lighting", ""),                # lighting/time
        f'{shot.get("shot_scale","")} shot',          # wide / close-up
        shot.get("emotion", ""),                      # mood
        C.STYLE,                                       # realism style
    ]
    return ", ".join(p for p in parts if p and p.strip())

# ============================================================================
#  Make every shot
# ============================================================================
for shot in shots:
    sid = shot["shot_id"]
    if only_shot and sid != only_shot:
        continue

    prompt = build_prompt(shot)
    out_path = os.path.join(C.KEYFRAME_DIR, f"shot_{sid}.png")
    print(f"\n=== Shot {sid} ===\n{prompt}")

    # fixed seed = same character look across shots (consistency)
    generator = torch.Generator("cuda").manual_seed(C.SEED + int(sid))

    image = pipe(
        prompt=prompt,
        width=C.WIDTH,
        height=C.HEIGHT,
        num_inference_steps=C.STEPS,
        guidance_scale=C.GUIDANCE,
        generator=generator,
        joint_attention_kwargs={"scale": C.LORA_SCALE} if C.REALISM_LORA else None,
    ).images[0]

    image.save(out_path)
    print(f"saved -> {out_path}")

print("\n✅ Done. All keyframes are in", C.KEYFRAME_DIR)
print("Look at them. To remake one shot:  python pipeline/make_images.py 03")
