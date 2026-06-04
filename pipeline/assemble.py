#!/usr/bin/env python3
# ============================================================================
#  STAGE 7 — ASSEMBLE (quick rough cut).  Stitches all shots in order into one
#  video with ffmpeg, so you can preview the whole film FAST (before DaVinci).
#  Uses lip-synced clip if it exists, else the raw clip. Lays voice over each shot.
#
#  SETUP:  ffmpeg (already on most pods; else: apt-get install -y ffmpeg)
#  RUN:    python pipeline/assemble.py   ->  07_final/rough_cut.mp4
# ============================================================================
import os, sys, csv, subprocess, tempfile

sys.path.insert(0, os.path.dirname(__file__))
import config as C

OUT_DIR = "07_final"; os.makedirs(OUT_DIR, exist_ok=True)
out = os.path.join(OUT_DIR, "rough_cut.mp4")

with open(C.SHOT_LIST, newline="", encoding="utf-8") as f:
    shots = list(csv.DictReader(f))

def clip_for(sid):
    lip = os.path.join(C.LIPSYNC_DIR, f"shot_{sid}.mp4")
    raw = os.path.join(C.CLIPS_DIR, f"shot_{sid}.mp4")
    return lip if os.path.exists(lip) else (raw if os.path.exists(raw) else None)

tmp = tempfile.mkdtemp()
processed = []
for s in shots:
    sid = s["shot_id"]
    clip = clip_for(sid)
    if not clip:
        print(f"[skip] no clip for shot {sid}"); continue
    voice = os.path.join(C.VOICE_DIR, f"shot_{sid}.wav")
    seg = os.path.join(tmp, f"seg_{sid}.mp4")
    if os.path.exists(voice):
        # mux voice onto the clip
        subprocess.run(["ffmpeg","-y","-i",clip,"-i",voice,
                        "-c:v","libx264","-c:a","aac","-shortest",seg], check=False)
    else:
        subprocess.run(["ffmpeg","-y","-i",clip,"-c:v","libx264","-an",seg], check=False)
    if os.path.exists(seg):
        processed.append(seg)

if not processed:
    print("No clips found. Run make_images.py + make_videos.py first."); sys.exit(1)

# concat list
listfile = os.path.join(tmp, "list.txt")
with open(listfile, "w") as f:
    for p in processed:
        f.write(f"file '{p}'\n")

subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",listfile,
                "-c:v","libx264","-c:a","aac",out], check=False)
print(f"\n✅ Rough cut -> {out}  ({len(processed)} shots)")
print("This is a FAST preview. For the real film, use DaVinci (see 07_final/EDIT_GUIDE.md).")
