#!/usr/bin/env bash
# ============================================================================
#  🚀 ONE-LINE START — fixes everything + installs + launches the GUI dashboard.
#  You run this ONCE. After it opens the dashboard, you never need the terminal again.
#
#  RUN ON THE POD:
#     cd /workspace/ai-video && bash start.sh
# ============================================================================
set +e   # keep going even if a step warns

echo "================================================================"
echo "  🎬 AI Film Studio — starting up. Sit back, this is automatic."
echo "================================================================"

# 1) keep models on the persistent volume (so they survive pod restarts)
export HF_HOME=/workspace/hf_cache
grep -q 'HF_HOME=/workspace/hf_cache' ~/.bashrc || echo 'export HF_HOME=/workspace/hf_cache' >> ~/.bashrc

# 2) fix torch + torchvision (matching pair for CUDA 12.4 — fixes the nms error)
echo ">> [1/3] Installing matching torch (a few minutes)..."
pip install -q --force-reinstall torch==2.5.1 torchvision==0.20.1 \
  --index-url https://download.pytorch.org/whl/cu124

# 3) install everything else
echo ">> [2/3] Installing the studio libraries..."
pip install -q -U "diffusers>=0.32" transformers accelerate sentencepiece protobuf \
  gradio pandas imageio imageio-ffmpeg

# 4) quick check
python - <<'PY'
import torch
print(">> torch", torch.__version__, "| GPU ready:", torch.cuda.is_available())
PY

echo ">> [3/3] Launching the dashboard..."
echo "================================================================"
echo "  When you see a link like  https://xxxxx.gradio.live"
echo "  -> OPEN IT IN YOUR BROWSER. That is your studio. All buttons."
echo "================================================================"

# 5) launch the GUI (this keeps running — leave the terminal open)
python pipeline/dashboard.py
