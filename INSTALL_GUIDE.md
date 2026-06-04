# 🛠️ EASY INSTALL GUIDE — almost no command line

You do NOT need to be a programmer. The plan:
**deploy a ready ComfyUI pod → run ONE setup line → everything else is buttons in the browser.**

---

## STEP 1 — Deploy a ready-made ComfyUI pod (zero install)

On RunPod, **don't build from scratch.** Pick a template that already has ComfyUI:
1. RunPod → **Deploy** → choose your **A100 80GB**.
2. In **Templates**, search for **"ComfyUI"** (e.g. "ComfyUI" by community, or "AI-Dock ComfyUI").
   These come with ComfyUI + Manager already installed and a web button to open it.
3. ⚠️ Add a **Network Volume** (e.g. 100–200GB) mounted at `/workspace` so your files and models
   SURVIVE when the pod stops. Without this, everything is deleted on stop.
4. Deploy → wait → click **Connect → ComfyUI / port 8188**. ComfyUI opens in your browser. ✅

> If your template already has ComfyUI, you can SKIP installing ComfyUI in Step 2 — just run
> setup.sh which adds the extra nodes and skips what's already there.

---

## STEP 2 — Run the ONE setup line (adds all the special nodes + folders)

Open the pod's **Web Terminal** (a button in RunPod) and paste this ONE line:

```bash
bash <(curl -s https://raw.githubusercontent.com/YOUR-USERNAME/ai-film-studio/main/setup.sh)
```

*(Replace `YOUR-USERNAME` after you push this repo to GitHub. Until then: clone your repo first,
then run `bash /workspace/ai-project/setup.sh`.)*

It auto-installs: Face Detailer, Wan video, LatentSync lip sync, MMAudio, VideoHelper, and makes
all your `00_script … 07_final` folders. Takes ~5–10 min. **That's the only terminal step.**

---

## STEP 3 — Get the models (point & click, NO terminal)

Inside ComfyUI:
1. Click the **"Manager"** button (bottom of screen).
2. Click **"Model Manager"**.
3. Search and click **Install** (one click each) for:
   | Search for | Use |
   |---|---|
   | `FLUX.1-dev` (fp8) | keyframe images |
   | `Wan 2.2 I2V 14B` (fp8) | image → video |
   | `t5xxl` / `clip_l` | text encoders (image) |
   | `umt5` | text encoder (video) |
   | `vae` (flux ae + wan vae) | decoders |
4. The Manager puts each file in the correct folder automatically. ✅

> Some models (like FLUX.1-dev) are "gated" — if asked, make a free HuggingFace account, accept the
> model's license once on its HF page, and paste a free HF token. One-time.

**Custom nodes the easy way:** if you ever skip setup.sh, you can also install every node by clicking
**Manager → Install Custom Nodes → search → Install**. Same result, all buttons.

---

## STEP 4 — Put your LoRA in place

After you train your face LoRA (see `01_character/lora_training_config.yaml`), copy the file to:
```
/workspace/ComfyUI/models/loras/myhero_flux.safetensors
```
Drag-and-drop works in the RunPod file browser — no command needed.

---

## STEP 5 — Build the workflows (drag & drop)

ComfyUI workflows are just boxes you connect with your mouse. Follow:
- `02_keyframes/keyframe_workflow_guide.md` → image graph
- `03_clips_raw/video_workflow_guide.md` → video graph

> 💡 Even easier: search **"Wan 2.2 I2V workflow"** and **"FLUX workflow"** online — people share
> ready `.json` workflow files. In ComfyUI just **drag the .json onto the canvas** and it builds
> itself. Then you only swap in your LoRA + prompts.

---

## Daily routine (after setup is done — all browser)
1. RunPod → **Start** your pod (your `/workspace` is still there).
2. Open ComfyUI in browser.
3. Make keyframes → animate → repeat.
4. **Stop** the pod when done (so you stop paying).

---

## If something breaks
- A node failed to load? → Manager → **"Update All"** → restart ComfyUI.
- Out of memory (OOM)? → use the **fp8 / GGUF** model version, or lower resolution.
- Model in wrong folder? → Manager → Model Manager re-installs to the right place.

---

### TL;DR
1. Deploy a **ComfyUI RunPod template** + a **/workspace network volume**.
2. Paste **one** `setup.sh` line in the terminal.
3. Click-install models in **Manager**.
4. Drop in your LoRA.
5. Everything else = drag-and-drop boxes + your prompts. No coding.
