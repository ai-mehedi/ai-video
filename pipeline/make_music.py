#!/usr/bin/env python3
# ============================================================================
#  STAGE 4 — MAKE MUSIC.  Reads the 'music' column, makes one track per mood.
#  Uses MusicGen (free, Meta). One file per unique music mood in the storyboard.
#
#  SETUP:  pip install audiocraft
#  RUN:    python pipeline/make_music.py
# ============================================================================
import os, sys, csv

sys.path.insert(0, os.path.dirname(__file__))
import config as C

os.makedirs(C.MUSIC_DIR, exist_ok=True)

with open(C.SHOT_LIST, newline="", encoding="utf-8") as f:
    shots = list(csv.DictReader(f))

# collect unique music moods from the storyboard
moods = []
for s in shots:
    m = (s.get("music") or "").strip()
    if m and m not in moods:
        moods.append(m)
print("Music moods found:", moods)

import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained(C.MUSIC_MODEL)
model.set_generation_params(duration=20)   # 20 sec per piece (trim/loop in DaVinci)

for i, mood in enumerate(moods, 1):
    prompt = f"cinematic film score, {mood}, emotional, instrumental"
    print(f"=== Music {i}: {prompt} ===")
    wav = model.generate([prompt])
    out = os.path.join(C.MUSIC_DIR, f"music_{i:02d}")
    audio_write(out, wav[0].cpu(), model.sample_rate, strategy="loudness")
    print("saved ->", out + ".wav")

print("\n✅ Done. Music in", C.MUSIC_DIR)
