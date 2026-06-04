#!/usr/bin/env python3
# ============================================================================
#  STAGE 1 — MAKE IMAGES (keyframes).  Reads the storyboard, makes 1 per shot.
#  RUN:  python pipeline/make_images.py        (all shots)
#        python pipeline/make_images.py 03     (only shot 03)
# ============================================================================
import os, sys, csv
import torch
from diffusers import FluxPipeline

sys.path.insert(0, os.path.dirname(__file__))
import config as C

os.makedirs(C.KEYFRAME_DIR, exist_ok=True)
only = sys.argv[1] if len(sys.argv) > 1 else None

with open(C.SHOT_LIST, newline="", encoding="utf-8") as f:
    shots = list(csv.DictReader(f))
print(f"Loaded {len(shots)} shots from {C.SHOT_LIST}")

print("Loading FLUX... (first run downloads ~24GB)")
pipe = FluxPipeline.from_pretrained(C.FLUX_MODEL, torch_dtype=torch.bfloat16).to("cuda")

# realism LoRA (anti-plastic) + optional character LoRA (your reusable model)
adapters, scales = [], []
if C.REALISM_LORA and os.path.exists(C.REALISM_LORA):
    pipe.load_lora_weights(C.REALISM_LORA, adapter_name="realism"); adapters.append("realism"); scales.append(C.REALISM_LORA_SCALE)
if C.CHARACTER_LORA and os.path.exists(C.CHARACTER_LORA):
    pipe.load_lora_weights(C.CHARACTER_LORA, adapter_name="character"); adapters.append("character"); scales.append(C.CHARACTER_LORA_SCALE)
if adapters:
    pipe.set_adapters(adapters, adapter_weights=scales)
    print("LoRAs active:", list(zip(adapters, scales)))

def build_prompt(s):
    parts = [C.CHARACTER, s.get("character_action",""), s.get("location",""),
             s.get("time_lighting",""), f'{s.get("shot_scale","")} shot',
             s.get("emotion",""), C.STYLE]
    return ", ".join(p for p in parts if p and p.strip())

for s in shots:
    sid = s["shot_id"]
    if only and sid != only:
        continue
    prompt = build_prompt(s)
    out = os.path.join(C.KEYFRAME_DIR, f"shot_{sid}.png")
    print(f"\n=== Shot {sid} ===\n{prompt}")
    g = torch.Generator("cuda").manual_seed(C.SEED + int(sid))   # fixed seed = consistent character
    img = pipe(prompt=prompt, width=C.WIDTH, height=C.HEIGHT,
               num_inference_steps=C.STEPS, guidance_scale=C.GUIDANCE, generator=g).images[0]
    img.save(out)
    print("saved ->", out)

print("\n✅ Done. Keyframes in", C.KEYFRAME_DIR)
