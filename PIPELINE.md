# 🎬 ORGANIZED PIPELINE — story → script → storyboard → shots (with audio)

No scattered windows. ONE master file controls everything. Each stage = ONE command.

---

## The idea (organized, not scattered)

```
       ┌──────────────────────────────────────────────┐
       │   00_script/shot_list.csv   ← THE BRAIN 🧠     │
       │   (every shot: action, location, dialogue,    │
       │    music, sfx — one row per shot)             │
       └───────────────────┬──────────────────────────┘
                           │  every script reads this file
        ┌──────────┬───────┴────┬───────────┬──────────┐
        ▼          ▼            ▼           ▼          ▼
   make_images  make_videos  make_voice  make_music  make_sfx
        │          │            │           │          │
        ▼          ▼            ▼           ▼          ▼
   02_keyframes 03_clips_raw 05_audio/voice  /music    /sfx
   shot_01.png  shot_01.mp4  shot_01.wav   scene_1.wav ...
```

You edit settings in **ONE file** (`pipeline/config.py`) and run **ONE command per stage**.
Everything is named `shot_01`, `shot_02`… and lands in the right folder automatically.

---

## The full workflow (in order)

| Step | What you do | Command |
|---|---|---|
| 1 | Write the **story** | edit `00_script/story.md` |
| 2 | Write the **script** | edit `00_script/script.md` |
| 3 | Fill the **storyboard** (shot list) | edit `00_script/shot_list.csv` |
| 4 | Set character + style | edit `pipeline/config.py` |
| 5 | **Make all images** | `python pipeline/make_images.py` |
| 6 | **Make all videos** | `python pipeline/make_videos.py` |
| 7 | **Make all voice** | `python pipeline/make_voice.py` |
| 8 | **Make music** | `python pipeline/make_music.py` |
| 9 | Edit + grade | DaVinci Resolve |

---

## How a shot becomes a prompt (automatic)

For each row in the CSV, the script builds a prompt by combining columns:

```
CHARACTER + character_action + location + time_lighting + shot_scale + emotion + STYLE
```

Example — row `shot_01`:
> *"a 60 year old Bangladeshi rickshaw puller… , pulls his empty rickshaw through the rain,
> narrow old dhaka alley, dawn / rain / neon glow, wide shot, weary, candid documentary
> photograph, shot on Kodak Portra…"*

So you only write SHORT words in the CSV → the script makes the full prompt. Organized.

---

## ONE-TIME setup on the pod
```bash
# 1. get the project onto the pod
cd /workspace && git clone <your-github-repo> ai-project && cd ai-project

# 2. install python libraries
pip install -U diffusers transformers accelerate torch sentencepiece protobuf pandas imageio imageio-ffmpeg

# 3. login to HuggingFace (free) to download FLUX (accept its license once on the model page)
huggingface-cli login
```

Then just: `python pipeline/make_images.py`  🎬

---

## Why this is better for you than ComfyUI
- ✅ **One control file** (the CSV) instead of scattered node windows
- ✅ **One command per stage**, makes ALL shots automatically
- ✅ Change the prompt style for the WHOLE film by editing **one line** in config.py
- ✅ Re-make a single shot: `python pipeline/make_images.py 03`
- ✅ Everything auto-named + auto-organized into folders

## The trade-off (honest)
- ❌ If a script errors, it's a code error (I'll help you read it)
- ❌ First run downloads big models (FLUX ~24GB, Wan later)
- ❌ Needs a HuggingFace token (free, one time) for FLUX

---

## Status of scripts
- ✅ `config.py` — all settings
- ✅ `make_images.py` — STAGE 1 (images) — READY
- ⬜ `make_videos.py` — STAGE 2 (Wan video) — next
- ⬜ `make_voice.py` — STAGE 3 (F5-TTS) — next
- ⬜ `make_music.py` — STAGE 4 (MusicGen) — next

> We build + test ONE stage at a time. Get images working first, then add video, then audio.
