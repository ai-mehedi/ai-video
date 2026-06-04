# 🎬 AI Short Film Studio — Full Production Plan (100% Open Source, 48GB GPU)

> Goal: Netflix-style short film (3–5 min) with **your own face** as the main character.
> Constraint: **No paid AI.** Everything here is free / open source and runs on a single 48GB GPU
> (A6000 / A40 / L40 / 6000 Ada all work).
>
> Core idea: **Don't do text→video.** Build the film like a real set — storyboard → perfect still
> image per shot → animate the still → add voice/lipsync/SFX/music → color grade. Consistency is
> won at the *image* stage, not fought at the *video* stage.

---

## 0. The Golden Rules (read first — these fix your problems)

1. **One Character LoRA of yourself** = fixes "face not matching." Train once, use everywhere.
2. **Keyframe first, animate second** = fixes consistency + location breaking. Make the photo
   perfect, *then* turn it into video.
3. **Short clips only (3–6 sec each)**. A 4-min film = ~50–80 clips stitched in an editor.
   Never try to generate long shots — that is where everything breaks.
4. **Plastic face is killed in 3 places:** realistic base model → Face Detailer → post-grade + grain.
5. **Realism lives in post.** Raw AI never looks like Netflix. Color grade + grain + sound design
   is 40% of the final look.

---

## 1. Software Stack (install these)

| Job | Tool (open source) | Why |
|---|---|---|
| Orchestration | **ComfyUI** + ComfyUI-Manager | Runs image, video, lipsync, audio nodes — one hub |
| Keyframe images | **FLUX.1-dev** (fp8) | Best free photoreal image model |
| Image realism | **Impact Pack (Face Detailer)** | Kills plastic face, fixes eyes/skin |
| Character LoRA | **ai-toolkit** (ostris) *or* **kohya_ss** | Train your face into FLUX |
| Video (animate) | **Wan 2.2 I2V** (14B, fp8) | Best free image-to-video; good motion/water |
| Lip sync | **LatentSync** (ByteDance) | Best free lip sync; fallback **Wav2Lip-HD** |
| Talking face (option) | **Hallo2 / Sonic** | Audio-driven portrait if no body movement needed |
| Your voice (TTS clone) | **F5-TTS** *(or XTTS-v2)* | Clone your voice from a 30-sec sample |
| Voice conversion | **RVC** | Record yourself, convert to a cleaner/character voice |
| SFX (auto from video) | **MMAudio** | Generates foley synced to your clip (footsteps, water) |
| SFX / ambience (text) | **Stable Audio Open** | "rain", "city night", "shower water" |
| Background music | **MusicGen** (Meta, medium/large) | Free score from a text prompt |
| Upscale video | **Real-ESRGAN** / **SUPIR** | Sharpen final frames |
| Smooth motion | **RIFE** (frame interpolation) | 16fps → 32/60fps, removes choppiness |
| Edit + color grade | **DaVinci Resolve (free)** | Pro NLE + grading, 100% free |

> Everything except DaVinci runs inside ComfyUI. Install ComfyUI-Manager first, then install the
> custom nodes for Wan, LatentSync, MMAudio, Impact Pack from the Manager.

---

## 2. Folder Structure (set this up day 1)

```
ai-project/
├── 00_script/          # script.txt, shot_list.csv
├── 01_character/       # your training photos + trained LoRA (.safetensors)
├── 02_keyframes/       # the perfect still image for every shot (shot_01.png ...)
├── 03_clips_raw/       # animated video clips from Wan (shot_01.mp4 ...)
├── 04_lipsync/         # clips after lip sync
├── 05_audio/
│   ├── voice/          # your cloned voice lines
│   ├── sfx/            # generated sound effects
│   └── music/          # background score
├── 06_upscaled/        # final upscaled + interpolated clips
└── 07_final/           # DaVinci project + exported film
```

---

## 3. PHASE 1 — Script & Storyboard (paper, no GPU)

1. Write the script. Keep it **tight** — 3–5 min is ~400–700 words of dialogue + action.
2. Break it into **shots**, not scenes. Each shot = one camera angle = one clip.
3. Make a **shot list** (`00_script/shot_list.csv`):

| shot | scene | shot_scale | camera_move | location | action | dialogue | duration |
|---|---|---|---|---|---|---|---|
| 01 | intro | wide | slow push-in | rooftop night | hero stands | — | 5s |
| 02 | intro | close-up | static | rooftop night | hero looks down | "It ends tonight." | 4s |

**Camera tips for clean AI motion:**
- Slow & simple animates clean. Fast/complex motion breaks.
- Vary shot scale: wide (establish) → medium → close-up (emotion).
- Keep location names + lighting identical across shots in the same scene.

---

## 4. PHASE 2 — Train YOUR Character LoRA (the #1 fix)

This makes every shot have **your real face**, consistently.

**Photos you need (15–40 images):**
- Different angles: front, 3/4 left, 3/4 right, profile, slight up/down.
- Different expressions: neutral, smile, serious.
- Good even lighting, sharp, no heavy filters, no sunglasses.
- Plain/varied backgrounds. Crop to face+shoulders for most.

**Train with ai-toolkit (FLUX LoRA):**
- Resolution: 1024 (or 768 to save VRAM — 48GB handles 1024 fine).
- Steps: ~2000–3000. Learning rate: 1e-4 (default ai-toolkit FLUX config).
- Trigger word: e.g. `myhero` — you'll put this in every prompt.
- Output → `01_character/myhero_flux.safetensors`.

> Optional: also train a **body/outfit LoRA** if your character wears a specific costume, so the
> outfit stays consistent too.

---

## 5. PHASE 3 — Keyframe Images (where you WIN consistency)

For **every shot**, make one perfect still in ComfyUI with FLUX + your LoRA.

**Workflow (ComfyUI):**
```
FLUX.1-dev  +  myhero LoRA (weight ~0.8–1.0)
   → prompt: "myhero, [shot scale], [location], [lighting], [action], cinematic, film still"
   → Face Detailer pass (Impact Pack)   ← removes plastic skin, fixes eyes
   → save to 02_keyframes/shot_XX.png
```

**Kill plastic face:**
- FLUX CFG/guidance low (~3.5). High guidance = waxy.
- Always run **Face Detailer** (denoise ~0.4–0.5).
- Add to prompt: `visible skin pores, natural skin texture, subsurface scattering, soft cinematic lighting`.
- Negative (if using SDXL backup): `plastic skin, smooth skin, cgi, 3d render, airbrushed`.

**Lock location consistency:**
- Write the **same location description** word-for-word for every shot in that scene.
- Reuse the **same seed** for the establishing look, then vary only camera angle in the prompt.
- For exact background reuse, generate the location plate once and use it as an
  img2img / reference (ControlNet depth) for other angles.

**Sweat / wet / shower (your hard case):**
- Solve it in the *still* first: prompt `sweating, wet skin, water droplets, glistening skin, steam`.
- Get the wet look perfect in the photo → Phase 4 just animates it. Don't ask the video model to
  invent sweat from a dry image.

---

## 6. PHASE 4 — Animate Each Keyframe (Image → Video)

Use **Wan 2.2 I2V (14B fp8)** in ComfyUI. Feed `shot_XX.png` → get `shot_XX.mp4`.

**Settings:**
- Length: **3–6 sec** per clip (e.g. 16fps × 81 frames ≈ 5s). Longer = drift/break.
- Motion prompt: describe ONLY the motion — "slow push in, hero breathing, hair moves in wind,
  water dripping." Keep it minimal.
- Resolution: 720p out of Wan, upscale later. (48GB can do 720p I2V comfortably with fp8.)
- If a clip drifts/morphs: shorten it, lower motion strength, or split into two shorter clips.

**Water/sweat motion:** Wan 2.2 handles fluids better than most. Keep the shot short and the
camera slow so the water reads naturally.

> Workflow: do ALL shots as stills first (Phase 3), approve them, *then* batch-animate. Re-roll
> only bad clips — cheap because the identity/location is already locked in the still.

---

## 7. PHASE 5 — Voice (your own, free)

**Option A — Clone your voice (F5-TTS):**
- Record a clean 30–60 sec sample of yourself reading.
- F5-TTS clones it → type any dialogue → get it in your voice.
- Per-line files → `05_audio/voice/shot_XX.wav`.

**Option B — Record yourself + RVC:**
- Act the lines yourself, then RVC cleans/converts to a consistent voice character.

> For multiple characters: clone different reference voices (friends/family samples) or use XTTS-v2
> multi-speaker. All free.

---

## 8. PHASE 6 — Lip Sync

Use **LatentSync** in ComfyUI: input = animated clip + voice line → output = lips matching speech.

```
04_lipsync/shot_XX.mp4 = LatentSync( 03_clips_raw/shot_XX.mp4 , 05_audio/voice/shot_XX.wav )
```

- Works best on clear, front-ish faces → frame your talking shots as medium/close-up.
- For pure talking-head shots with little body motion, **Hallo2 / Sonic** (audio→portrait) can give
  even better mouth detail straight from the keyframe.
- Fallback: **Wav2Lip-HD** if LatentSync struggles on a shot.

---

## 9. PHASE 7 — Sound Effects & Foley

**Auto foley — MMAudio:** feed the video clip, it generates synced sound (footsteps, water,
cloth, ambience). Fast win for realism. → `05_audio/sfx/shot_XX.wav`.

**Text SFX / ambience — Stable Audio Open:** prompt specific sounds:
`"shower water running"`, `"night city ambience"`, `"thunder rumble"`, `"sword unsheath"`.

> Layer ambience under the whole scene + specific hits per action. This is what sells the world.

---

## 10. PHASE 8 — Background Music

**MusicGen (Meta), medium or large model:**
- Prompt the mood: `"tense cinematic score, slow strings, dark, building tension, 90 bpm"`.
- Generate per scene/act (intro theme, tension, climax, outro).
- → `05_audio/music/scene_XX.wav`.

> Tip: generate a few variations, pick best, keep volume LOW under dialogue (DaVinci ducking).

---

## 11. PHASE 9 — Upscale & Smooth

Before editing, clean every clip:
1. **RIFE** frame interpolation: 16fps → 32/60fps (removes AI choppiness).
2. **Real-ESRGAN** (or **SUPIR** for hero shots): upscale 720p → 1080p/4K, sharpen.
- → `06_upscaled/shot_XX.mp4`.

---

## 12. PHASE 10 — Edit + Color Grade (DaVinci Resolve, free)

This is where it becomes "Netflix."

1. **Assemble** all clips on the timeline per the shot list.
2. **Sync** voice, lipsync clips, SFX, music. Use **track ducking** so music dips under dialogue.
3. **Color grade** for the cinematic look:
   - Balance exposure/white point per shot so all clips match (consistency!).
   - Apply a **film LUT** (Kodak/Fuji-style free LUTs) for a unified mood.
   - Add slight **film grain** + subtle **vignette** → kills the "clean AI" plastic feel.
   - Optional light **bloom/halation** for cinematic glow.
4. **Sound design polish:** EQ voice, reverb to match space (shower = echo), master to ~ -14 LUFS.
5. **Export:** H.264/H.265, 1080p or 4K, 24fps for cinematic feel.

---

## 13. Problem → Fix Cheat Sheet (your original issues)

| Problem | Fix |
|---|---|
| Plastic/waxy face | FLUX low guidance + Face Detailer + skin-texture prompt + grain in DaVinci |
| Face not matching | Your **Character LoRA** in every keyframe |
| Sweat/shower fake | Get wet look in the **still** first, then short-clip animate; Wan 2.2 for fluids |
| Consistency breaks | **Keyframe-first** method; same LoRA + seed + locked descriptions |
| Location changes | Same location text word-for-word; reuse location plate via ControlNet depth |
| Choppy / morphing video | Clips ≤6 sec, slow camera, RIFE smoothing |
| Whole film feels disjointed | One LoRA + one color grade/LUT across all shots |

---

## 14. Realistic Timeline (solo, learning as you go)

| Week | Work |
|---|---|
| 1 | Install stack, train your Character LoRA, test keyframes |
| 2 | Finalize script + shot list, generate ALL keyframes, perfect the faces |
| 3 | Animate all clips (Wan), re-roll bad ones |
| 4 | Voice clone + lip sync all dialogue |
| 5 | SFX + music + upscale/RIFE |
| 6 | Edit + color grade + sound mix + export |

> Honest note: photoreal + perfect consistency + 5 min is at the **edge** of current open-source
> tech. Expect lots of re-rolls. Start with a **60–90 sec test film** first to learn the full
> pipeline end-to-end before committing to the full 3–5 min.

---

## 15. VRAM Notes (48GB)

- FLUX.1-dev fp8: ~16–24GB — fine.
- Wan 2.2 14B I2V fp8: ~24–40GB at 720p — fine; drop resolution if OOM.
- LatentSync / MMAudio / MusicGen: light, run after video.
- Train LoRA and run inference at different times (don't do both at once).
- Use **fp8 / GGUF** quantized model versions to stay safe on VRAM.

---

### TL;DR
Train **one LoRA of yourself** → make a **perfect still for every shot** (fix face + location +
sweat here) → **animate short clips** with Wan 2.2 → **clone your voice** (F5-TTS) → **lip sync**
(LatentSync) → **auto SFX** (MMAudio) + **music** (MusicGen) → **upscale/smooth** (RIFE/ESRGAN) →
**edit + color grade + grain** in DaVinci. All free. Build a 90-sec test first.
