# 🔊 Audio Guide — Voice (your own) + Lip Sync + SFX + Music (all free)

Order: 1) make voice lines → 2) lip sync to clips → 3) auto SFX → 4) music → mix in DaVinci.

```
05_audio/
├── voice/     shot_XX.wav   (your cloned voice, one file per dialogue line)
├── sfx/       shot_XX.wav   (foley/ambience per shot)
└── music/     scene_XX.wav  (background score per scene/act)
```

---

## 1. VOICE — clone your own voice (F5-TTS)

**Install:** `git clone https://github.com/SWivid/F5-TTS && cd F5-TTS && pip install -e .`

**Steps:**
1. Record a **clean 15–30 sec** sample of yourself reading naturally (quiet room, no music).
   Save as `ref.wav` + write what you said in `ref.txt`.
2. Generate each line from your `shot_list.csv` dialogue:
   ```
   f5-tts_infer-cli \
     --model F5-TTS \
     --ref_audio "ref.wav" \
     --ref_text  "the exact words in ref.wav" \
     --gen_text  "It ends tonight." \
     --output    "05_audio/voice/shot_02.wav"
   ```
3. One `.wav` per dialogue shot.

**Tips:**
- Match emotion: record the ref sample in the tone you want (calm ref → calm output).
- For multiple characters: use a different `ref.wav` per character (friends/family samples).
- **Alternative — XTTS-v2** (Coqui TTS): also free, multilingual, good if you want non-English.
- **Alternative — record yourself acting + RVC**: convert your raw recording to a cleaner/consistent
  voice with a trained RVC model. Best control over performance.

---

## 2. LIP SYNC — match mouth to voice (LatentSync)

**Install:** `git clone https://github.com/bytedance/LatentSync` (follow its README, download checkpoints).

**Run per talking shot:**
```
python -m latentsync.inference \
  --video_path  03_clips_raw/shot_02.mp4 \
  --audio_path  05_audio/voice/shot_02.wav \
  --video_out_path 04_lipsync/shot_02.mp4
```

**Tips:**
- Works best on clear, front-ish faces → frame dialogue as medium/close-up shots.
- If the clip is wider than the talking moment, crop to the face, sync, then place back in DaVinci.
- **Alternatives:**
  - **Hallo2 / Sonic** — drive a portrait directly from audio (great for pure talking-head shots,
    can skip Wan for those).
  - **Wav2Lip-HD** — older fallback, reliable on tricky shots.
- ComfyUI has LatentSync + Wav2Lip nodes too if you prefer staying in ComfyUI.

> Non-dialogue shots: skip this — go straight to upscale (Phase 9).

---

## 3. SFX — sound effects & foley

### A) Auto foley from the video — MMAudio (easiest, synced)
Feed the clip, it generates sound matched to the motion (footsteps, cloth, water, ambience).
```
# via MMAudio repo or ComfyUI MMAudio node:
input:  03_clips_raw/shot_04.mp4  (rain/running)
output: 05_audio/sfx/shot_04.wav
```
Great first pass — already time-aligned to the picture.

### B) Specific sounds from text — Stable Audio Open
For exact effects/ambience, prompt them:
```
"rain on pavement, night"          -> 05_audio/sfx/rain_loop.wav
"footsteps running on wet ground"  -> 05_audio/sfx/run_steps.wav
"shower water running, bathroom"   -> 05_audio/sfx/shower.wav
"distant city traffic ambience"    -> 05_audio/sfx/city_amb.wav
"metal impact, sparks"             -> 05_audio/sfx/impact.wav
```
**Layering:** one continuous ambience under the whole scene + specific hits on each action.
Pull the SFX column from your `shot_list.csv` as your shopping list.

---

## 4. MUSIC — background score (MusicGen)

**Install:** Meta AudioCraft → `pip install audiocraft` (use `musicgen-medium` or `musicgen-large`).

**Generate per scene/mood (from the music column in shot_list.csv):**
```python
from audiocraft.models import MusicGen
m = MusicGen.get_pretrained('facebook/musicgen-large')
m.set_generation_params(duration=30)
prompts = [
  "tense cinematic score, slow dark strings, building tension, 90 bpm",   # intro
  "driving percussion, urgent chase music, dark synth, fast",             # chase
  "low ominous drone, minimal, dread",                                    # confront
  "epic orchestral hit, climax, powerful",                                # climax
  "soft emotional piano, hopeful, gentle strings, sunrise",               # ending
]
# render each -> 05_audio/music/scene_XX.wav
```
**Tips:**
- Generate a few variations per mood, keep the best.
- Make pieces a bit longer than the scene so you can trim cleanly.
- **Alternative — YuE** if you ever want music WITH vocals/song. MusicGen = instrumental score.

---

## 5. FINAL MIX (in DaVinci Resolve — Fairlight page, free)

1. Lay clips on the timeline, drop voice/SFX/music on separate audio tracks.
2. **Ducking:** make music auto-dip when dialogue plays (Fairlight → Dynamics → Ducking,
   or keyframe music volume down under voice lines).
3. **EQ voice** for clarity; add **reverb** to match the space (shower = more echo, alley = slap echo).
4. Rough levels: **dialogue loudest**, SFX support, music under everything.
5. Master the whole film to about **-14 LUFS** (good for web/YouTube).

---

## Audio order checklist
- [ ] Record ref.wav, clone voice with F5-TTS → all dialogue lines in 05_audio/voice/
- [ ] LatentSync each talking clip → 04_lipsync/
- [ ] MMAudio pass on action clips + Stable Audio for specific SFX → 05_audio/sfx/
- [ ] MusicGen per scene mood → 05_audio/music/
- [ ] Mix + duck + EQ + master in DaVinci → export
