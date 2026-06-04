# DubStudio GPU worker — for RunPod Serverless
# CUDA base so Demucs runs on GPU.
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

# ffmpeg for audio/video, git for demucs models
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the Demucs model into the image so workers start fast (no cold download).
RUN python -c "import demucs.pretrained as p; p.get_model('htdemucs')" || true

COPY pipeline.py handler.py ./

# RunPod Serverless entry
CMD ["python", "-u", "handler.py"]
