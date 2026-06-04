# 🖱️ ComfyUI — Detailed Step-by-Step (First Image → First Video)

Total beginner guide. Follow in order. Don't skip. Each step says exactly what to click.

---

# PART 1 — Understand your screen

When ComfyUI opens you see:
- A **big empty canvas** (grey area) — your workspace where boxes (nodes) live.
- **Top bar** — has a menu (☰ or "Workflow", "Edit", etc.) and the **ComfyUI logo**.
- **Left side icons** (a vertical bar) — Workflows 📁, Nodes, **Models** 🧊, Queue.
- **Top-right** — a **"Manager"** button (this is ComfyUI-Manager — your install tool).
- **Bottom-center / bottom-right** — a **"Queue Prompt"** or **"Run" ▶** button. This RUNS the job.

> If you ever get lost: press **Ctrl + A** then **Delete** to clear the canvas, and reload a template.

---

# PART 2 — Download the FLUX model FIRST (you need this before anything)

ComfyUI is empty — it has no AI model yet. Install FLUX:

1. Click the **"Manager"** button (top-right).
2. A window opens. Click **"Model Manager"**.
3. In the search box, type: **flux**
4. Find one named like **"FLUX.1-dev fp8"** (or "flux1-dev-fp8").
5. Click **"Install"** next to it. ⏳ It downloads (big file — wait a few minutes).
6. Also search and install these (FLUX needs them):
   - **t5xxl_fp8** (text encoder)
   - **clip_l** (text encoder)
   - **ae** or **flux vae** (the VAE / decoder)
7. When all say "Installed" → close the Manager window.

> 💡 If Model Manager doesn't have FLUX, use the EASIER way in Part 3 step 4 ("Install Missing
> Models") — it auto-finds them for you.

---

# PART 3 — Load a ready FLUX workflow (do NOT build by hand)

1. Top bar → click **"Workflow"** menu → click **"Browse Templates"**
   *(or click the 📁 template icon on the left bar).*
2. A gallery of ready workflows opens.
3. Find the **"Flux"** group → click **"Flux Dev"** (the full quality one).
4. The workflow loads — you'll see connected boxes appear on the canvas. ✅
5. **If you see RED boxes** = missing models. Fix it the easy way:
   - Click **Manager → "Install Missing Models"**
   - Click **Install** on everything in the list → wait → reload the page.
   - Red boxes turn normal = ready.

---

# PART 4 — Make your FIRST image (Karim)

1. On the canvas, find the box called **"CLIP Text Encode (Positive Prompt)"**.
   - It's the text box for what you WANT to see. Sometimes labelled green or "Positive".
2. Click inside it, delete the old text, and paste this:

```
a 60 year old Bangladeshi rickshaw puller, thin face, weathered dark skin,
short grey beard, kind tired eyes, deep wrinkles, wearing an old wet grey shirt,
pulling an empty rickshaw through a narrow Old Dhaka alley at dawn, monsoon rain,
neon shop signs reflecting on wet ground, cinematic wide shot, shot on 35mm,
moody atmosphere, natural skin texture, rain on skin, film grain
```

3. (FLUX has no negative prompt — ignore any "Negative" box, leave it empty.)
4. Check image size: find **"Empty Latent Image"** box → set **width 1216, height 832**
   (wide cinematic). For first test you can leave default 1024x1024.
5. Click the big **"Queue Prompt"** / **"Run ▶"** button (bottom).
6. Watch the boxes light up green one by one (it's working ⏳ ~30–60 sec).
7. An **image of Karim appears** in the "Save Image" / "Preview" box. 🎉🎬

> THIS IS YOUR FIRST WIN. If you see Karim in the rain → your studio works!

---

# PART 5 — Save / find your image

- The image auto-saves to ComfyUI's **output folder**: `/workspace/ComfyUI/output/`
- To see/download it: open **FileBrowser (port 8080)** or **JupyterLab (8888)** →
  go to `ComfyUI/output/` → your PNG is there.
- Rename it to **shot_01.png** and (later) move to your `ai-project/02_keyframes/` folder.

**Don't like the face?** Click **Queue Prompt** again — it makes a new one (different each time).
Keep clicking until Karim looks right. Change words in the prompt to adjust.

---

# PART 6 — Keep the face the SAME (important for your 7 shots)

For all 7 shots, Karim must look like the SAME man. Two rules:
1. **Keep this exact description in every shot's prompt** (don't change his face words):
   `a 60 year old Bangladeshi rickshaw puller, thin face, weathered dark skin, short grey beard,
   kind tired eyes, deep wrinkles`
2. **Lock the seed:** find the **"KSampler"** box → there's a **"seed"** number and a
   **"control_after_generate"** setting. Set it to **"fixed"** (not "randomize") once you get a
   good face. Same seed + same face words = same man across shots.
   - Then only change the ACTION and BACKGROUND words for each shot (from `test_shot_list.csv`).

---

# PART 7 — Make it realistic (kill plastic face) — optional but good

1. FLUX guidance: find the **"FluxGuidance"** box → set value to **3.5** (low = real skin).
2. Add a **Face Detailer** later (needs Impact Pack installed) for perfect skin/eyes.
   For the first test, skip it — just get an image first.

---

# ✅ Your goal RIGHT NOW
Just get **ONE image of Karim** on the screen. That's it.
- Install FLUX (Part 2)
- Load Flux Dev template (Part 3)
- Paste prompt + Queue (Part 4)

Once you see Karim → tell me, and we move to making the VIDEO from it.

---

# 🆘 If something breaks
| Problem | Fix |
|---|---|
| Red boxes | Manager → Install Missing Models → reload page |
| "Manager" button missing | Tell me — node may need installing |
| Out of memory error | Use fp8 model, or lower image size to 1024x1024 |
| Image is blurry/bad | Click Queue again (new seed), or check steps = 20 |
| Nothing happens on Queue | Check bottom for a red error message → paste it to me |
