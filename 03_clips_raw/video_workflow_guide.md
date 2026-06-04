# 🎞️ Image → Video Workflow — ComfyUI (Wan 2.2 I2V)

Animate each approved keyframe into a short clip. Input = `02_keyframes/shot_XX.png`,
output = `03_clips_raw/shot_XX.mp4`. **Short clips only (3–6 sec).** Long = drift + morph + break.

---

## Models to download (free)

| File | Goes in |
|---|---|
| `wan2.2_i2v_14B_fp8.safetensors` (or GGUF Q5/Q6 for less VRAM) | `models/diffusion_models/` |
| `umt5_xxl_fp8.safetensors` (text encoder) | `models/clip/` (or `text_encoders/`) |
| `wan_2.1_vae.safetensors` | `models/vae/` |
| (optional) Wan I2V CLIP vision if your node needs it | `models/clip_vision/` |

Custom nodes (via ComfyUI-Manager): **ComfyUI-WanVideoWrapper** (Kijai) — the standard Wan nodes.
Also install **ComfyUI-VideoHelperSuite** (for video load/save/combine).

---

## The node graph (reuse for every shot)

```
[Load Image]  ->  02_keyframes/shot_XX.png
        │
        ▼
[WanVideo Model Loader]  wan2.2_i2v_14B_fp8     (precision: fp8)
        │
        ▼
[WanVideo Image-to-Video Encode]  <- your start image
        │
        ▼
[WanVideo Text Encode]   POSITIVE = MOTION prompt only (see below)
        │                NEGATIVE = "static, distorted, morphing, extra limbs, jitter"
        ▼
[WanVideo Sampler]
        steps: 25-30      cfg: 6        shift: 5
        frames: 81        fps: 16       (81 frames @16fps ≈ 5.0 sec)
        width: 1280  height: 720        (720p; upscale later)
        seed: fixed per scene
        │
        ▼
[WanVideo Decode]
        │
        ▼
[Video Combine]  ->  03_clips_raw/shot_XX.mp4   (format mp4, h264, fps 16)
```

> If you only have the lighter setup or hit OOM: use the **GGUF Q5** model, drop to **640x360**
> internal then upscale, or lower frames to 49 (≈3 sec). 48GB fp8 720p is normally fine.

---

## Motion prompt = describe ONLY the movement

The keyframe already defines who/where/look. Here you ONLY say what MOVES. Keep it short & slow.

**Good examples:**
- `slow camera push in, hero breathing slowly, hair moving gently in the wind`
- `rain falling, water dripping down face, subtle head turn toward camera`
- `slow pan left, coat moving slightly, steady calm motion`
- `sparks flying, quick forward motion, dramatic`

**Negative (always):**
```
static, frozen, morphing, melting, distorted face, extra fingers, extra limbs,
warping background, flickering, jitter, duplicate
```

---

## Settings cheat sheet

| Want | Set |
|---|---|
| Calm/cinematic | frames 81, slow motion words, cfg 6 |
| Strong action | cfg 6–7, motion words like "fast, running", keep clip ≤4s |
| Less drift / more stable | fewer frames (49–65), simpler motion prompt |
| Smoother result | leave 16fps here, fix with RIFE later (Phase 9) |

---

## Camera movement (match your shot_list.csv)
Put the camera move from the CSV into the motion prompt:
- `slow push-in` → "slow camera push in"
- `slow pan left` → "slow camera pan left"
- `handheld follow` → "handheld camera follow, subtle shake"
- `static` → "locked camera, no camera movement" (let only the subject move)
- `pull-out` → "slow camera pull back"

Slow + simple = clean animation. Fast + complex = the model breaks faces/water.

---

## Sweat / water / shower
Wan 2.2 handles fluids better than most models, BUT only animates water that's ALREADY in the
keyframe. So:
1. Make sure sweat/rain/steam is visible in `shot_XX.png` first.
2. Motion prompt: `water dripping, droplets sliding down skin, steam rising, slow motion`.
3. Keep the clip short (≤5s) and camera slow so droplets read naturally.

---

## Fixing common breakage
| Problem | Fix |
|---|---|
| Face morphs/changes mid-clip | shorten clip (49 frames), simpler motion, lower cfg to 5 |
| Background warps | "locked camera", reduce motion words, fewer frames |
| Too static / dead | add gentle motion words, raise cfg to 7 |
| Choppy | keep as-is, RIFE smooths it in Phase 9 |
| Limbs glitch on big movement | split into 2 shorter clips, or change to a tighter shot scale |

---

## Workflow order
1. Animate scene by scene, keeping the SAME seed family per scene.
2. Watch each clip fully. Re-roll only bad ones (cheap — keyframe identity already locked).
3. Save approved clips to `03_clips_raw/shot_XX.mp4`.
4. Talking shots → go to lip sync (Phase 6). Non-talking → straight to upscale (Phase 9).

### Per-shot checklist
- [ ] Start image = approved keyframe
- [ ] Motion prompt describes movement only
- [ ] Negative prompt set
- [ ] Clip ≤ 6 sec (81 frames @16fps)
- [ ] Same seed family as scene-mates
- [ ] Face stays consistent the whole clip
- [ ] Saved to 03_clips_raw/
