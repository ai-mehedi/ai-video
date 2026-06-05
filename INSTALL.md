# 📦 Full Installation (RunPod)

End-to-end setup for the AI video pipeline: **restoration** (upscale + faces + 60fps +
cinematic grade) and the **cartoon** route (ChatGPT keyframes → LoRA → Diffutoon).

---

## 1. Start a RunPod pod

- Template: **PyTorch** (CUDA preinstalled)
- GPU: **48 GB** (A6000 / L40 / A40)
- Disk / volume: **100 GB+** (a 10-min video extracts to many GB of frames)
- Expose **HTTP port 7860** (for the Gradio app)

## 2. Get the code onto the pod

```bash
cd /workspace
git clone https://github.com/ai-mehedi/ai-video.git
cd ai-video
```
(or `git pull` if you already cloned it)

## 3. Set up your API key (the `.env` file)

The `.env` lives in the **project root** (`/workspace/ai-video/.env`). It is
**gitignored** — it is never committed or shared.

```bash
cp .env.example .env
nano .env          # paste your OPENAI_API_KEY, save with Ctrl+O, exit Ctrl+X
```

`.env` contents:
```
OPENAI_API_KEY=sk-...your real key...
OPENAI_IMAGE_MODEL=gpt-image-1
```

The Python scripts auto-load this with `python-dotenv` — you do **not** need to
`export` anything manually.

## 4. Run the installer (one command)

```bash
bash setup.sh
```

This installs:
- **FFmpeg** + system tools
- Python deps (`gradio`, `openai`, `python-dotenv`, `scenedetect`, …)
- **Real-ESRGAN** (fast super-resolution)
- **CodeFormer** (face restoration) + weights
- **Practical-RIFE** (60fps interpolation)
- **DiffSynth-Studio** (Diffutoon cartoon stylization)
- and patches the known `basicsr`/`torchvision` import bug automatically.

Takes ~10–20 min on first run (downloads models).

## 5. RIFE weights (for best 60fps — optional)

Download the model from the Practical-RIFE README (Google Drive) into
`~/Practical-RIFE/train_log/`. If missing, the pipeline auto-falls back to
FFmpeg `minterpolate` (works, slightly lower quality).

## 6. Cartoon models (for the cartoon route — when you build it)

Diffutoon needs an SD1.5 cartoon checkpoint + AnimateDiff + ControlNets.
DiffSynth downloads most on first run; pick a cartoon checkpoint (e.g. ToonYou /
RevAnimated from Civitai) and point the Diffutoon config at it. (We wire this in
when we build the cartoon stage.)

---

## 7. Run it

### Web app (Gradio)
```bash
python app.py
```
Open **port 7860** from the RunPod "Connect" panel, or the public `*.gradio.live`
link it prints. For big files, paste the **path on the pod** (e.g.
`/workspace/myvideo.mp4`) instead of uploading through the browser.

### Command line (restoration)
```bash
python restore.py --input /workspace/old.mp4 --output /workspace/new.mp4 \
    --target-height 1080 --fps 60 --upscale 2 \
    --face-fidelity 0.7 --denoise 0.4 --grade-strength 0.6
```

Useful flags:
- `--no-faces`      skip face restoration (faster)
- `--fp32`          disable fp16 (slower, more VRAM)
- `--upscale 4`     for very low-res sources
- `--deinterlace`   old camcorder/VHS footage
- `--keep-work`     keep scratch frames for inspection

---

## Transfer big videos to the pod (don't upload via browser)

- **RunPod file manager** → upload into `/workspace/`
- **runpodctl**: local `runpodctl send video.mp4` → pod `runpodctl receive <code>`
- **wget/curl** if the video is at a URL
