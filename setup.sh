#!/usr/bin/env bash
# ============================================================================
#  ONE-COMMAND SETUP — installs everything for the Python pipeline + dashboard.
#  RUN ON THE POD:   bash setup.sh
# ============================================================================
set -e
echo ">> Installing Python libraries (this takes a few minutes)..."
pip install -U \
  torch \
  "diffusers>=0.32" transformers accelerate sentencepiece protobuf \
  gradio pandas imageio imageio-ffmpeg \
  || echo "[warn] some pip installs failed — check messages above"

echo ""
echo ">> Optional (audio stages):"
echo "     pip install f5-tts          # voice cloning"
echo "     pip install audiocraft      # music (MusicGen)"
echo ""
echo ">> Now log in to HuggingFace (free) to download FLUX:"
echo "     huggingface-cli login"
echo "     (accept the FLUX.1-dev license once on its HF model page)"
echo ""
echo "================================================================"
echo "  ✅ Setup ready. Then run ONE of these:"
echo "     python pipeline/make_images.py     # make keyframes"
echo "     python pipeline/make_videos.py     # animate them"
echo "     python pipeline/dashboard.py       # the studio dashboard (web)"
echo "================================================================"
