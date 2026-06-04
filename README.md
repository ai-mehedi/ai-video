# 🎬 AI Film Studio (open-source, your own)

Make realistic short films with a **reusable character**, from **one dashboard**, using free tools.
Built to test free video quality first — and **swap to a paid video model later** (one config switch)
only if needed. Full design: see [`MASTER_PLAN.md`](MASTER_PLAN.md).

## 📂 Structure
```
00_script/      story.md, script-ready shot_list.csv   ← the storyboard (brain)
01_character/   train_lora.yaml + dataset/             ← your reusable character (LoRA)
pipeline/       config.py + make_*.py + dashboard.py   ← the engine + control panel
02_keyframes/ 03_clips_raw/ 04_lipsync/ 05_audio/ 06_upscaled/ 07_final/
```

## 🚀 Quick start (on the pod)
```bash
cd /workspace && git clone <this-repo> ai-project && cd ai-project
bash setup.sh
huggingface-cli login          # free, accept FLUX.1-dev license once
```
Then either run stages, or open the dashboard:
```bash
python pipeline/dashboard.py            # 🎛️ one-screen studio (web link)
# or one command per stage:
python pipeline/make_images.py          # 1) keyframes
python pipeline/make_videos.py          # 2) animate (JUDGE VIDEO QUALITY HERE)
python pipeline/make_voice.py           # 3) dialogue in your voice
python pipeline/make_lipsync.py         # 4) lip sync (talking shots)
python pipeline/make_music.py           # 5) music
python pipeline/make_sfx.py             # 6) sound effects (foley)
python pipeline/assemble.py             # 7) quick rough cut -> 07_final/rough_cut.mp4
# then finish in DaVinci -> see 07_final/EDIT_GUIDE.md
```

## 🧠 How it works (organized, not scattered)
- `shot_list.csv` = the brain. One row per shot.
- `config.py` = all settings in one place (character, style, models).
- Each script reads the CSV → makes every shot → saves named + sorted (`shot_01`, `shot_02`...).
- Same character every shot (fixed seed / your LoRA) = consistency.

## 🔁 Reusable assets (build once, reuse forever)
- 🧬 Character LoRA (`01_character/`) — your face/character
- 🎙️ Voice (F5-TTS reference)
- ⚙️ Pipeline + dashboard

## ⬆️ Upgrading video later (only if free quality is poor)
In `config.py` change `VIDEO_ENGINE = "wan"` → `"kling"`/`"veo"`, add an API key, done.
Everything else stays the same.

## ♻️ If the pod is wiped
`git clone` this repo on a new pod → `bash setup.sh` → re-download models → continue.
(Big files — models, LoRA, clips — are NOT in git; re-download / back up to HuggingFace or Drive.)

## ⚠️ Honest note
Free **Wan** video is good but not Veo/Sora-level. Test it first (that's the plan). The biggest
realism wins: Character LoRA + low guidance + film grain in DaVinci.
