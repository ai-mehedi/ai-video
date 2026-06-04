# 🎬 AI FILM STUDIO — MASTER PLAN

> A complete, organized system to make realistic short films (3–5 min) with a **reusable
> custom character**, controlled from **one dashboard**, using **100% open-source** tools on a
> 48–80GB GPU (RunPod). This document is the full plan. The project is built from it.

---

## 1. VISION (what we are building)

Not a pile of scattered tools — **one organized studio**:

> Prompt a story → get a storyboard → generate each shot (image → video) → add dialogue,
> music, SFX → realistic film. Your main character is a **reusable "model"** that looks the
> **same in every shot and every film**. Everything controlled from **one dashboard**.

Three pillars:
1. 🧬 **Reusable Character** — trained once, used forever (a LoRA)
2. 🎛️ **Studio Dashboard** — one web screen to control the whole production
3. ⚙️ **Automated Pipeline** — storyboard drives shot-by-shot generation

---

## 2. THE PROBLEMS WE ARE SOLVING (from real experience)

| Problem | Root cause | The fix built into this plan |
|---|---|---|
| Plastic / waxy face | Raw model, high guidance, no skin detail | Realism LoRA + low guidance (3.0) + Face Detailer + film grain |
| Face not matching | No identity lock | 🧬 **Character LoRA** (reusable) |
| Consistency breaks | Animating from text each time | **Keyframe-first**: perfect the still, then animate |
| Location keeps changing | No fixed reference | Same location text + fixed seed + reference image |
| Sweat / water fake | Asking video model to invent it | Put wet look in the **still first**, then animate short clips |
| Scattered / disorganized | Manual node wiring per stage | **Dashboard + CSV-driven pipeline** |

---

## 3. SYSTEM ARCHITECTURE

```
                ┌───────────────────────────────────────────────┐
                │            🎛️  STUDIO DASHBOARD                 │
                │   (one web screen — control everything)        │
                └───────────────┬───────────────────────────────┘
                                │ reads / drives
                ┌───────────────▼───────────────────────────────┐
                │      🧠  STORYBOARD  (shot_list.csv)           │
                │   one row per shot: action, location,          │
                │   dialogue, music, sfx, camera                 │
                └───────────────┬───────────────────────────────┘
        ┌───────────┬───────────┼───────────┬───────────┐
        ▼           ▼           ▼           ▼           ▼
    IMAGES       VIDEO        VOICE       MUSIC        SFX
   (FLUX +      (Wan 2.2)    (F5-TTS)   (MusicGen)  (MMAudio)
    🧬 LoRA)        │            │           │           │
        ▼           ▼           ▼           ▼           ▼
   02_keyframes 03_clips    05_audio/voice  /music     /sfx
        └───────────┴──────────┬┴───────────┴───────────┘
                               ▼
                     EDIT + COLOR GRADE (DaVinci Resolve)
                               ▼
                         🎬 FINAL FILM
```

---

## 4. TECH STACK (final choices — all free / open source)

| Job | Tool | Why this one |
|---|---|---|
| Image (keyframes) | **FLUX.1-dev** | Best free photoreal image model |
| Character identity | **Character LoRA** (ai-toolkit) | Reusable, locks the face |
| Realism (anti-plastic) | **XLabs realism LoRA** + Face Detailer | Kills the waxy look |
| Video (animate) | **Wan 2.2 I2V** | Best free image→video, good water/motion |
| Voice (your own) | **F5-TTS** | Clone voice from 30-sec sample |
| Lip sync | **LatentSync** | Best free lip sync |
| SFX (auto foley) | **MMAudio** | Sound synced to the video |
| Music | **MusicGen** | Free score from a text prompt |
| Upscale / smooth | **Real-ESRGAN + RIFE** | Sharpen + smooth motion |
| Edit + grade | **DaVinci Resolve (free)** | Pro editing + color + grain |
| Dashboard | **Gradio** | Simple web UI on the pod |
| Pipeline | **Python (diffusers) + CSV** | Organized, one command per stage |

---

## 5. REUSABLE ASSETS (build once, use for every film)

| Asset | Built how | Reuse |
|---|---|---|
| 🧬 **Character LoRA** | train on 20–40 photos | every shot, every film |
| 🎙️ **Voice model** | F5-TTS reference sample | all dialogue, every film |
| ⚙️ **Pipeline scripts** | make_images / videos / voice / music | every film |
| 🎛️ **Dashboard** | dashboard.py | every film |
| 🎨 **Style preset** | character + realism text in config | consistent look |

> A new film = just a new `shot_list.csv` + your story. The reusable assets stay.

---

## 6. THE COMPLETE WORKFLOW (every stage, in order)

### Stage 0 — Story & Storyboard (no GPU)
1. Write/generate the **story** → `00_script/story.md`
2. Write the **script** → `00_script/script.md`
3. Fill the **storyboard** → `00_script/shot_list.csv` (one row per shot)

### Stage 1 — Build the Reusable Character (one time)
4. Collect 20–40 photos → train **Character LoRA** → save as reusable model

### Stage 2 — Keyframes (images)
5. Dashboard / `make_images.py` reads the CSV → makes one perfect still per shot
6. Realism locked here (LoRA + low guidance + Face Detailer). Re-roll until good.

### Stage 3 — Animate (video)
7. `make_videos.py` (Wan 2.2) turns each still into a 3–6 sec clip

### Stage 4 — Voice & Lip Sync
8. `make_voice.py` (F5-TTS) makes dialogue in your voice
9. LatentSync matches mouth to voice

### Stage 5 — Sound & Music
10. MMAudio = foley, MusicGen = score (from CSV columns)

### Stage 6 — Finish
11. Upscale (Real-ESRGAN) + smooth (RIFE)
12. Edit + color grade + grain + mix in DaVinci → export

---

## 7. THE STUDIO DASHBOARD (one screen)

Built with Gradio, opens in a browser. Tabs:

| Tab | Controls |
|---|---|
| 📋 **Storyboard** | view/edit the shot list |
| ⚙️ **Character & Style** | character text, realism style, guidance slider, seed |
| 🖼️ **Keyframes** | generate one / all shots, preview gallery, re-roll |
| 🎞️ **Video** | animate keyframes, preview clips |
| 🎙️ **Voice & Music** | dialogue + music per shot/scene |
| 📦 **Export** | collect everything for DaVinci |

One place. Buttons, not node-wiring. Like an editor.

---

## 8. FOLDER STRUCTURE

```
ai-project/
├── MASTER_PLAN.md            ← this file
├── README.md                 ← quick start + restart guide
├── setup.sh                  ← one-command install on the pod
├── 00_script/
│   ├── story.md  script.md  shot_list.csv     ← the storyboard (brain)
├── 01_character/
│   ├── dataset/              ← training photos
│   ├── train_lora.yaml       ← LoRA training config
│   └── output/               ← trained LoRA (reusable model)
├── pipeline/
│   ├── config.py             ← ALL settings in one place
│   ├── dashboard.py          ← the studio dashboard
│   ├── make_images.py
│   ├── make_videos.py
│   ├── make_voice.py
│   └── make_music.py
├── 02_keyframes/   03_clips_raw/   04_lipsync/
├── 05_audio/{voice,music,sfx}/
├── 06_upscaled/    07_final/
```

---

## 9. BUILD PHASES (the order we create the project)

| Phase | Build | Result |
|---|---|---|
| **A** | Folder structure + config + README + setup.sh | clean skeleton |
| **B** | Story + script + shot_list.csv (test film) | the storyboard |
| **C** | LoRA training config | reusable character ready to train |
| **D** | `make_images.py` + dashboard (image tab) | generate keyframes |
| **E** | `make_videos.py` | animate clips |
| **F** | `make_voice.py` + `make_music.py` | audio |
| **G** | Export + DaVinci guide | final film |

> We build + test **one phase at a time.** Don't move on until the current phase works.

---

## 10. HARDWARE & SETUP

- **GPU:** RunPod A100 80GB (or 48GB works). Add a **/workspace network volume** (keeps files).
- **One-time setup:** `setup.sh` installs everything; `huggingface-cli login` for FLUX.
- **Cost saving:** start pod → work → **stop pod** when idle (pay only while running).

---

## 11. REALISTIC EXPECTATIONS (honest)

- ✅ Reusable consistent character — **yes** (LoRA does this)
- ✅ Organized one-dashboard control — **yes** (Gradio)
- ✅ Shot-by-shot automated production — **yes** (CSV pipeline)
- ⚠️ "One prompt → perfect film, zero edits" — **not 100% yet.** You review + re-roll shots.
  The system gets you ~90% automated; the last 10% (taste, grade, re-rolls) is you.
- 📌 Start with a **60–90 sec test film** before the full 3–5 min.

---

## 12. DECISIONS TO CONFIRM (before building the project)

1. **Character:** your own face (needs your photos) — or a generated character for testing first?
2. **First film:** the Bangladesh test ("The Last Rickshaw") — or your own story?
3. **Engine:** Python pipeline + dashboard (organized, recommended) — confirmed?

> Once confirmed, we build **Phase A** (skeleton) and move down the list, testing each step.

---

### TL;DR
Reusable **Character LoRA** + **Gradio dashboard** + **CSV-driven Python pipeline** =
organized studio. Story → storyboard → images → video → voice → music → grade. All free.
Build phase by phase, test each, start with a short test film.
