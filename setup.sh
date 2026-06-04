#!/usr/bin/env bash
# ============================================================================
#  ONE-COMMAND SETUP — installs everything for the Python pipeline + dashboard.
#  RUN ON THE POD:   bash setup.sh
# ============================================================================
set -e
echo ">> Installing matching torch + torchvision for CUDA 12.4 (matches most RunPod drivers)..."
pip install --force-reinstall torch==2.5.1 torchvision==0.20.1 \
  --index-url https://download.pytorch.org/whl/cu124 \
  || echo "[warn] torch install failed — if your pod driver differs, pick the matching cuXXX index at pytorch.org"

echo ">> Installing the rest of the libraries..."
pip install -U \
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
