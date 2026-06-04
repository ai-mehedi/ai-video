# 🎙️ DubStudio Worker — the dubbing engine

Turns a video into another language: keeps the **background music/SFX**, clones **each speaker's
voice** (child stays child), and syncs the new dialogue. Runs as a **RunPod Serverless** GPU worker.

## Files
- `pipeline.py` — the dubbing pipeline (extract → Demucs → Scribe → translate → clone → TTS → mix → remux)
- `handler.py` — RunPod serverless entry + local test mode
- `requirements.txt`, `Dockerfile` — to build the worker image

## The pipeline (what happens to each video)
```
1. extract audio (ffmpeg)
2. Demucs → vocals.wav + background.wav        ← keeps music + SFX
3. Scribe (ElevenLabs) → segments + speakers + timestamps
4. translate each segment (Google/DeepL/GPT)
5. clone each speaker's voice (ElevenLabs IVC)  ← keeps each voice/tone
6. TTS each line in the cloned voice (Multilingual v2)
7. align clips to original timing (atempo fit)
8. mix new dialogue + original background
9. remux audio onto the video
10. (optional) lip-sync
```

## Environment variables
```
ELEVENLABS_API_KEY=...        # required
TTS_MODEL=eleven_multilingual_v2   # or eleven_turbo_v2_5 (cheaper)
STT_MODEL=scribe_v1
```

## Test locally (needs a GPU or it runs Demucs on CPU = slow)
```bash
pip install -r requirements.txt        # + system ffmpeg
export ELEVENLABS_API_KEY="your-key"
python handler.py sample.mp4 bn        # dub sample.mp4 into Bangla (bn)
# language codes: bn=Bangla, hi=Hindi, ur=Urdu, en=English, es=Spanish, ar=Arabic...
```
Output: a `result.mp4` path is printed.

## Deploy on RunPod Serverless
```bash
docker build -t youruser/dubstudio-worker .
docker push youruser/dubstudio-worker
```
Then on RunPod → Serverless → New Endpoint → use this image → set `ELEVENLABS_API_KEY` env →
set max workers (= your concurrency cap) → scale-to-zero on.

Your API server sends a job:
```json
{ "input": { "video_url": "https://...", "target_lang": "bn", "num_speakers": 2,
             "lipsync": false, "result_put_url": "<S3 presigned PUT>" } }
```
Worker returns: `{ "result_url": "..." }`.

## Notes / next steps
- **Translation** uses free Google for MVP — swap to DeepL or GPT for better quality.
- **Lip-sync** is a stub — wire LatentSync when you add the paid add-on.
- **Voice clones are auto-deleted** after each job (keeps your ElevenLabs library clean).
- Enforce the **5-min length cap** in the API before sending jobs here.
- Quality knobs: `voice_settings` (stability/similarity) in `pipeline.synthesize`, and the
  `atempo` fit range in `pipeline.fit_clip`.
