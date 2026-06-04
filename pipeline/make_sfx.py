#!/usr/bin/env python3
# ============================================================================
#  STAGE 6 — SFX (auto foley).  Makes sound synced to each clip using MMAudio.
#  Reads each clip in 03_clips_raw/ and writes a matching sound file.
#
#  SETUP:  pip install mmaudio   (or clone the MMAudio repo + its checkpoints)
#  RUN:    python pipeline/make_sfx.py
#
#  NOTE: MMAudio's exact CLI/API varies by version. This script tries the common
#  CLI; if your install differs, generate SFX from the dashboard/notes instead.
# ============================================================================
import os, sys, csv, subprocess

sys.path.insert(0, os.path.dirname(__file__))
import config as C

os.makedirs(C.SFX_DIR, exist_ok=True)

with open(C.SHOT_LIST, newline="", encoding="utf-8") as f:
    shots = list(csv.DictReader(f))

for s in shots:
    sid = s["shot_id"]
    clip = os.path.join(C.CLIPS_DIR, f"shot_{sid}.mp4")
    out  = os.path.join(C.SFX_DIR, f"shot_{sid}.wav")
    if not os.path.exists(clip):
        print(f"[skip] no clip for shot {sid}"); continue
    prompt = s.get("sfx", "") or "ambient sound"
    print(f"=== Shot {sid} SFX: {prompt} ===")
    # common MMAudio CLI (adjust to your install if needed):
    subprocess.run([
        sys.executable, "-m", "mmaudio.cli",
        "--video", os.path.abspath(clip),
        "--prompt", prompt,
        "--output", os.path.abspath(out),
    ], check=False)
    print("saved ->", out)

print("\n✅ Done (or check messages). SFX in", C.SFX_DIR)
