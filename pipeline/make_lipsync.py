#!/usr/bin/env python3
# ============================================================================
#  STAGE 5 — LIP SYNC.  Matches the mouth to the voice for talking shots.
#  Uses LatentSync. Only runs on shots that have BOTH a clip and a voice line.
#
#  SETUP:  git clone https://github.com/bytedance/LatentSync  (follow its README,
#          download its checkpoints). Set LATENTSYNC_DIR below.
#  RUN:    python pipeline/make_lipsync.py
# ============================================================================
import os, sys, csv, subprocess

sys.path.insert(0, os.path.dirname(__file__))
import config as C

LATENTSYNC_DIR = "/workspace/LatentSync"     # <<< where you cloned LatentSync
os.makedirs(C.LIPSYNC_DIR, exist_ok=True)

with open(C.SHOT_LIST, newline="", encoding="utf-8") as f:
    shots = list(csv.DictReader(f))

for s in shots:
    if not (s.get("dialogue") or "").strip():
        continue   # only talking shots
    sid = s["shot_id"]
    clip  = os.path.join(C.CLIPS_DIR, f"shot_{sid}.mp4")
    voice = os.path.join(C.VOICE_DIR, f"shot_{sid}.wav")
    out   = os.path.join(C.LIPSYNC_DIR, f"shot_{sid}.mp4")
    if not (os.path.exists(clip) and os.path.exists(voice)):
        print(f"[skip] shot {sid}: need both clip + voice first"); continue
    print(f"=== Shot {sid} lip sync ===")
    subprocess.run([
        sys.executable, "-m", "latentsync.inference",
        "--video_path", os.path.abspath(clip),
        "--audio_path", os.path.abspath(voice),
        "--video_out_path", os.path.abspath(out),
    ], cwd=LATENTSYNC_DIR, check=False)
    print("saved ->", out)

print("\n✅ Done. Lip-synced clips in", C.LIPSYNC_DIR)
print("Tip: shots without dialogue stay in", C.CLIPS_DIR, "(use those directly).")
