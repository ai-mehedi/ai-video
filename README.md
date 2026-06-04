# 🎬 AI Short Film Studio (Open Source, 48GB GPU)

Make a Netflix-style short film (3–5 min) with **my own face** as the main character —
using **100% free / open-source** tools. This repo is the **backup of all my plans & configs**
so I can rebuild the whole pipeline if RunPod is wiped.

## 📂 What's in this repo (the important text — always backed up)
| File | What it is |
|---|---|
| `plan.md` | Master production plan (all 10 phases, tools, timeline) |
| `00_script/shot_list.csv` | Shot-by-shot plan (camera, location, dialogue, SFX, music) |
| `01_character/lora_training_config.yaml` | Train my face into FLUX (ai-toolkit) |
| `02_keyframes/keyframe_workflow_guide.md` | ComfyUI image workflow (FLUX + LoRA + Face Detailer) |
| `03_clips_raw/video_workflow_guide.md` | Image→video (Wan 2.2 I2V) settings |
| `05_audio/audio_guide.md` | Voice clone + lip sync + SFX + music |

## 🚫 What is NOT in this repo (too big — stored elsewhere)
- **AI models** (`.safetensors`, etc.) → re-download free from HuggingFace
- **My trained LoRA** (`myhero_flux.safetensors`) → back up to **HuggingFace Hub** (free, private) or Google Drive
- **My training photos** → keep private/offline
- **Generated clips / audio / keyframes** → regenerable; back up finals to Drive

## ♻️ If RunPod gets deleted — how to restart
1. New pod (48GB GPU) → `git clone <this repo>`
2. Re-install: ComfyUI + Manager, then nodes (Impact Pack, WanVideoWrapper, VideoHelperSuite, LatentSync, MMAudio)
3. Re-download models from HuggingFace (see each guide's "Models to download" table)
4. Download my LoRA + photos back from HuggingFace/Drive
5. Follow `plan.md` from the phase I left off (check `status` column in `shot_list.csv`)

## 🗺️ Pipeline order
`script → train face LoRA → keyframes → animate → voice → lipsync → SFX → music → upscale → color grade`

## 💡 Tip for big files
Back up the trained LoRA to a **free private HuggingFace repo**:
```
pip install huggingface_hub
huggingface-cli login
huggingface-cli upload <user>/myhero-lora myhero_flux.safetensors
```
That keeps GitHub for plans (text) and HuggingFace for weights (big files).
