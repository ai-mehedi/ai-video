# 🖼️ Keyframe Image Workflow — ComfyUI (FLUX + your LoRA + Face Detailer)

This is the MOST important stage. You make ONE perfect still per shot here.
Fix face, location, sweat, lighting NOW — the video stage only animates what you give it.

---

## Models to download (free)

Put files in these ComfyUI folders:

| File | Goes in | Source |
|---|---|---|
| `flux1-dev-fp8.safetensors` | `models/checkpoints/` | Black Forest Labs (HuggingFace) |
| (or split) `flux1-dev.safetensors` + `ae.safetensors` | `models/unet/`, `models/vae/` | HF |
| `clip_l.safetensors` + `t5xxl_fp8_e4m3fn.safetensors` | `models/clip/` | HF (comfyanonymous repo) |
| `myhero_flux.safetensors` (YOUR LoRA) | `models/loras/` | from training |

Custom nodes (install via **ComfyUI-Manager**):
- **ComfyUI-Impact-Pack** (Face Detailer)
- **rgthree-comfy** (quality-of-life, optional)

---

## The node graph (build this once, reuse for every shot)

```
[Load Checkpoint: flux1-dev-fp8]
        │
        ▼
[Load LoRA: myhero_flux]  ── strength: 0.85  (0.7 if face looks stiff/plastic)
        │
        ▼
[CLIP Text Encode  — POSITIVE]   <- your shot prompt (see template below)
        │
        ▼
[Empty Latent Image]  width 1024  height 1024   (or 1216x832 for widescreen)
        │
        ▼
[KSampler]   steps 20   cfg 1.0   sampler euler   scheduler simple   denoise 1.0
        │     (FLUX uses guidance, not cfg — keep cfg=1, set FluxGuidance ~3.5)
        ▼
[FluxGuidance]  guidance: 3.5     ← LOW = realistic skin. High = plastic/waxy.
        │
        ▼
[VAE Decode]
        │
        ▼
[FaceDetailer]  (Impact Pack)     ← THIS kills plastic face
        │   bbox: face_yolov8m       denoise 0.45   feather 5   guide_size 512
        ▼
[Save Image]  ->  02_keyframes/shot_XX.png
```

### FaceDetailer settings (the anti-plastic step)
- `denoise`: **0.4–0.5** (higher = changes face more; too high breaks likeness)
- `bbox_threshold`: 0.5
- `feather`: 5
- Keep your LoRA active so the detailer re-renders the face AS YOU, with real skin.

---

## Prompt template (fill per shot from shot_list.csv)

**Positive:**
```
myhero, [shot_scale] shot, [character_action], [location], [time_lighting],
[emotion] expression,
cinematic film still, shot on 35mm, shallow depth of field,
natural skin texture, visible skin pores, subsurface scattering, soft cinematic lighting,
detailed eyes, film grain
```

**Example — shot 05 (sweating in rain):**
```
myhero, close-up shot, breathing hard with sweat and rain on face, dark back alley at night,
rain, exhausted intense expression,
cinematic film still, shot on 35mm, shallow depth of field,
wet skin, water droplets, glistening skin, natural skin texture, visible skin pores,
detailed eyes, dramatic rim light, film grain
```

> FLUX largely ignores negative prompts. If you use an SDXL realistic model as backup instead,
> add negative: `plastic skin, smooth skin, airbrushed, cgi, 3d render, doll, waxy`.

---

## Locking CONSISTENCY (do this every time)

1. **Location:** copy the location + lighting words EXACTLY the same for all shots in a scene.
2. **Wardrobe:** keep the wardrobe phrase identical (e.g. always "black coat").
3. **Seed:** generate the scene's first/establishing shot, note its seed. Reuse a fixed seed family
   for that scene so the look stays stable; change only the action/angle words.
4. **Exact same background across angles?** Generate the location once, then use
   **ControlNet (depth)** or img2img with that plate as reference for the other angles.

---

## Sweat / wet / shower — solve it HERE
- Add: `sweating, wet skin, water droplets, glistening skin, steam` (shower: `steam, fogged glass`).
- Get it perfect in the still. The video model (Wan 2.2) then just animates the existing water —
  it will NOT reliably invent sweat from a dry image.

---

## Workflow order (important)
1. Generate ALL keyframes first (one PNG per shot in `02_keyframes/`).
2. Review every face up close. Re-roll any bad ones (cheap — identity already locked by LoRA).
3. ONLY when all stills are approved → move to Phase 4 (animate with Wan 2.2 I2V).

This is why your consistency won't break: you approve the look as static images before any motion.

---

## Quick checklist per shot
- [ ] Trigger word `myhero` in prompt
- [ ] LoRA strength 0.85
- [ ] FluxGuidance 3.5 (not high)
- [ ] Same location/wardrobe wording as scene-mates
- [ ] Face Detailer ran (skin has pores, not plastic)
- [ ] Saved as `02_keyframes/shot_XX.png`
