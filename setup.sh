#!/usr/bin/env bash
# One-shot setup for a RunPod pod (PyTorch template, CUDA, 48 GB GPU).
# Run once after the pod starts:
#     bash setup.sh
set -e

echo "== system packages =="
apt-get update -y
apt-get install -y ffmpeg git wget aria2

echo "== python packages =="
pip install --upgrade pip
# torch/torchvision usually preinstalled on RunPod PyTorch templates.
pip install gradio gdown opencv-python realesrgan basicsr facexlib gfpgan

cd ~

echo "== CodeFormer (super-resolution + face restoration) =="
if [ ! -d ~/CodeFormer ]; then
  git clone https://github.com/sczhou/CodeFormer.git
fi
cd ~/CodeFormer
pip install -r requirements.txt
python basicsr/setup.py develop
# weights
python scripts/download_pretrained_models.py facelib
python scripts/download_pretrained_models.py CodeFormer
cd ~

echo "== Practical-RIFE (60fps interpolation) =="
if [ ! -d ~/Practical-RIFE ]; then
  git clone https://github.com/hzwer/Practical-RIFE.git
fi
cd ~/Practical-RIFE
pip install -r requirements.txt || true
# NOTE: RIFE model weights must be downloaded into ~/Practical-RIFE/train_log/
# Get the latest model link from the repo README (Google Drive) and:
#   gdown <FILE_ID> -O model.zip && unzip model.zip -d train_log
# If train_log/*.pkl is missing, the pipeline auto-falls back to FFmpeg minterpolate.
cd ~

echo "== patch basicsr / torchvision compatibility =="
# Newer torchvision moved functional_tensor; basicsr/CodeFormer still import the old path.
for d in $(python -c "import basicsr,os;print(os.path.dirname(basicsr.__file__))") ~/CodeFormer/basicsr; do
  if [ -d "$d" ]; then
    grep -rl 'torchvision.transforms.functional_tensor' "$d" 2>/dev/null \
      | xargs -r sed -i 's/torchvision.transforms.functional_tensor/torchvision.transforms.functional/g'
  fi
done

echo "== done. Launch the app with:  python app.py =="
