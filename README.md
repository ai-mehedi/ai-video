# 🎬 AI Video Restoration (RunPod)

Turn old / low-quality video into a clean, sharp, cinematic, 60fps, 1080p result.
Free open-source models, runs on a RunPod 48 GB GPU, driven from a Gradio web app.

## Pipeline

```
input ─► 1 Preprocess ─► 2 AI Restore ─► 3 Assemble ─► 4 Interpolate ─► 5 Grade+Encode ─► output
         FFmpeg            CodeFormer +     FFmpeg        RIFE → 60fps      FFmpeg
         deint+denoise     Real-ESRGAN                    (minterpolate     cinematic look
         extract frames    SR + faces                      fallback)        + 1080p + audio
```

| Tool | Job | License |
|------|-----|---------|
| FFmpeg | decode, deinterlace, denoise, grade, encode | free |
| Real-ESRGAN | general super-resolution / upscale | free (BSD) |
| CodeFormer | face restoration + drives Real-ESRGAN bg upscale | free (NTU S-Lab) |
| RIFE (Practical-RIFE) | frame interpolation to 60fps | free (MIT) |

## Setup on RunPod

1. Start a pod with a **PyTorch** template and a **48 GB GPU** (A6000 / L40 / A40).
   Give it plenty of disk (a 10-min video extracts to many GB of PNG frames — 100 GB+ volume recommended).
2. Upload this folder (or `git clone` it) to the pod, e.g. into `~/video-restore`.
3. Run setup once:
   ```bash
   cd ~/video-restore
   bash setup.sh
   ```
4. **RIFE weights** (optional but recommended for best 60fps): download the model
   from the Practical-RIFE README into `~/Practical-RIFE/train_log/`.
   If missing, the pipeline automatically falls back to FFmpeg `minterpolate`
   (works fine, slightly lower quality).

## Run the app

```bash
cd ~/video-restore
python app.py
```

- Open port **7860** from the RunPod **Connect** panel, or use the public
  `*.gradio.live` link it prints.
- Upload a video, choose options, click **Restore ▶**, watch the live log.

## Run from the command line (no UI)

```bash
python restore.py --input old.mp4 --output new.mp4 \
    --target-height 1080 --fps 60 --upscale 2 \
    --face-fidelity 0.7 --denoise 0.4 --grade-strength 0.6
```

Add `--deinterlace` for old camcorder/VHS footage. Use `--upscale 4` for very
low-resolution sources. `--keep-work` keeps the scratch frames for inspection.

## Notes / expectations

- A 10-min clip = 15,000–18,000 frames. End-to-end to 1080p/60fps is roughly
  **30 min – a few hours** on one 48 GB GPU depending on settings.
- This is **v1** — exact model script arguments and output folder names can
  differ between repo versions. If a stage errors, the live log shows the exact
  command; that's what we tune. The pipeline is built to fail loudly at the
  stage that breaks, not silently.
- Output is **SDR with a vivid cinematic "HDR look"** — plays on every
  screen/phone. (True HDR10 is a future option.)
