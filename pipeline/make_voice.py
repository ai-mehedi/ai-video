#!/usr/bin/env python3
# ============================================================================
#  STAGE 3 — MAKE VOICE.  Reads the 'dialogue' column, makes 1 wav per line.
#  Uses F5-TTS to clone YOUR voice from a 20-30 sec reference sample.
#
#  SETUP:  pip install f5-tts
#          put your sample at 05_audio/voice/ref.wav  + set VOICE_REF_TEXT in config
#  RUN:    python pipeline/make_voice.py
# ============================================================================
import os, sys, csv, subprocess

sys.path.insert(0, os.path.dirname(__file__))
import config as C

os.makedirs(C.VOICE_DIR, exist_ok=True)

with open(C.SHOT_LIST, newline="", encoding="utf-8") as f:
    shots = list(csv.DictReader(f))

if not os.path.exists(C.VOICE_REF_AUDIO):
    print(f"[!] Missing reference voice: {C.VOICE_REF_AUDIO}")
    print("    Record a 20-30 sec clip of yourself, save it there, set VOICE_REF_TEXT in config.py")
    sys.exit(1)

for s in shots:
    line = (s.get("dialogue") or "").strip()
    if not line:
        continue   # only shots that have dialogue
    sid = s["shot_id"]
    out = os.path.join(C.VOICE_DIR, f"shot_{sid}.wav")
    print(f"=== Shot {sid} voice ===\n  \"{line}\"")
    # F5-TTS command-line clone
    subprocess.run([
        "f5-tts_infer-cli",
        "--model", "F5-TTS",
        "--ref_audio", C.VOICE_REF_AUDIO,
        "--ref_text",  C.VOICE_REF_TEXT,
        "--gen_text",  line,
        "--output",    out,
    ], check=False)
    print("saved ->", out)

print("\n✅ Done. Voice lines in", C.VOICE_DIR)
