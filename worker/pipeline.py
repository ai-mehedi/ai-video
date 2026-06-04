"""
DubStudio — dubbing pipeline (the core engine).

Flow:  extract audio → Demucs (split vocals/background) → Scribe (transcribe + speakers)
       → translate → clone each speaker's voice → TTS in target language → align → mix → remux.

Keeps original music/SFX (background track) and each speaker's voice identity (voice clone).
All ElevenLabs calls are REST (no SDK needed). GPU is used only by Demucs (+ optional lip-sync).
"""
import os, subprocess, tempfile, json, time, wave, contextlib
import requests
from pydub import AudioSegment

ELEVEN_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVEN_BASE = "https://api.elevenlabs.io/v1"
TTS_MODEL   = os.environ.get("TTS_MODEL", "eleven_multilingual_v2")   # or eleven_turbo_v2_5 (cheaper)
STT_MODEL   = os.environ.get("STT_MODEL", "scribe_v1")


# ----------------------------------------------------------------------------- helpers
def _run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def _headers():
    return {"xi-api-key": ELEVEN_KEY}

def audio_duration_sec(path):
    a = AudioSegment.from_file(path)
    return len(a) / 1000.0


# ----------------------------------------------------------------------------- 1. extract
def extract_audio(video_path, out_wav):
    """Pull a clean 44.1k mono wav out of the video."""
    _run(["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "44100", out_wav])
    return out_wav


# ----------------------------------------------------------------------------- 2. separate (GPU)
def separate(audio_wav, work_dir):
    """
    Demucs: split into vocals.wav + background.wav (music + SFX).
    We keep 'background' untouched and only replace the vocals.
    """
    out = os.path.join(work_dir, "demucs")
    # htdemucs gives stems: vocals, drums, bass, other. --two-stems=vocals = vocals + no_vocals.
    _run(["python", "-m", "demucs", "--two-stems", "vocals", "-o", out, audio_wav])
    name = os.path.splitext(os.path.basename(audio_wav))[0]
    stem_dir = os.path.join(out, "htdemucs", name)
    vocals     = os.path.join(stem_dir, "vocals.wav")
    background = os.path.join(stem_dir, "no_vocals.wav")
    return vocals, background


# ----------------------------------------------------------------------------- 3. transcribe
def transcribe(vocals_wav):
    """
    ElevenLabs Scribe → words with timestamps + speaker ids. Returns grouped segments:
    [{start, end, speaker, text}]
    """
    with open(vocals_wav, "rb") as f:
        r = requests.post(
            f"{ELEVEN_BASE}/speech-to-text",
            headers=_headers(),
            data={"model_id": STT_MODEL, "diarize": "true", "timestamps_granularity": "word"},
            files={"file": f},
            timeout=600,
        )
    r.raise_for_status()
    data = r.json()
    return _group_words(data.get("words", []))

def _group_words(words):
    """Group word-level results into speaker segments (new segment on speaker change or long gap)."""
    segments, cur = [], None
    GAP = 0.8  # seconds of silence starts a new segment
    for w in words:
        if w.get("type") and w["type"] != "word":
            continue
        spk = w.get("speaker_id", "speaker_0")
        if cur is None or spk != cur["speaker"] or (w["start"] - cur["end"]) > GAP:
            if cur:
                segments.append(cur)
            cur = {"start": w["start"], "end": w["end"], "speaker": spk, "text": w["text"]}
        else:
            cur["end"] = w["end"]
            cur["text"] += (" " if not w["text"].startswith(("'", ".", ",", "?", "!")) else "") + w["text"]
    if cur:
        segments.append(cur)
    return segments


# ----------------------------------------------------------------------------- 4. translate
def translate_segments(segments, target_lang):
    """Translate each segment's text. Uses deep-translator (free Google). Swap for DeepL/GPT later."""
    from deep_translator import GoogleTranslator
    tr = GoogleTranslator(source="auto", target=target_lang)
    for s in segments:
        try:
            s["text_translated"] = tr.translate(s["text"]) or s["text"]
        except Exception:
            s["text_translated"] = s["text"]
    return segments


# ----------------------------------------------------------------------------- 5. clone voices
def clone_voices(vocals_wav, segments, work_dir):
    """
    For each speaker, cut a few of their slices from the vocals and create an Instant Voice Clone.
    Returns {speaker_id: eleven_voice_id}. So child stays child, each speaker keeps their tone.
    """
    voc = AudioSegment.from_file(vocals_wav)
    speakers = {}
    for s in segments:
        speakers.setdefault(s["speaker"], []).append(s)

    voice_ids = {}
    for spk, segs in speakers.items():
        # build a ~20-30s sample from this speaker's longest slices
        segs = sorted(segs, key=lambda x: (x["end"] - x["start"]), reverse=True)[:6]
        sample = AudioSegment.silent(duration=0)
        for s in segs:
            sample += voc[int(s["start"] * 1000):int(s["end"] * 1000)]
        sample_path = os.path.join(work_dir, f"sample_{spk}.mp3")
        sample.export(sample_path, format="mp3")

        with open(sample_path, "rb") as f:
            r = requests.post(
                f"{ELEVEN_BASE}/voices/add",
                headers=_headers(),
                data={"name": f"dub_{spk}_{int(time.time())}",
                      "description": "auto voice clone for dubbing"},
                files=[("files", (os.path.basename(sample_path), f, "audio/mpeg"))],
                timeout=300,
            )
        r.raise_for_status()
        voice_ids[spk] = r.json()["voice_id"]
    return voice_ids


def delete_voices(voice_ids):
    """Clean up cloned voices after the job (avoid filling the ElevenLabs voice library)."""
    for vid in voice_ids.values():
        try:
            requests.delete(f"{ELEVEN_BASE}/voices/{vid}", headers=_headers(), timeout=60)
        except Exception:
            pass


# ----------------------------------------------------------------------------- 6. synthesize (TTS)
def synthesize(segments, voice_ids, work_dir):
    """TTS each translated segment in that speaker's cloned voice. Returns [(clip_path, start, end)]."""
    clips = []
    for i, s in enumerate(segments):
        vid = voice_ids.get(s["speaker"])
        if not vid or not s.get("text_translated"):
            continue
        r = requests.post(
            f"{ELEVEN_BASE}/text-to-speech/{vid}",
            headers={**_headers(), "Content-Type": "application/json"},
            json={"text": s["text_translated"], "model_id": TTS_MODEL,
                  "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}},
            timeout=300,
        )
        r.raise_for_status()
        clip_path = os.path.join(work_dir, f"tts_{i:03d}.mp3")
        with open(clip_path, "wb") as f:
            f.write(r.content)
        clips.append((clip_path, s["start"], s["end"]))
    return clips


# ----------------------------------------------------------------------------- 7. align + 8. mix
def fit_clip(clip_path, target_sec):
    """Gently speed up/slow down a TTS clip to fit the original slot (keeps lip timing close)."""
    clip = AudioSegment.from_file(clip_path)
    if target_sec <= 0:
        return clip
    ratio = (len(clip) / 1000.0) / target_sec
    ratio = max(0.8, min(1.25, ratio))   # don't distort too much
    if abs(ratio - 1.0) < 0.05:
        return clip
    out = clip_path.replace(".mp3", "_fit.wav")
    _run(["ffmpeg", "-y", "-i", clip_path, "-filter:a", f"atempo={ratio:.3f}", out])
    return AudioSegment.from_file(out)

def build_and_mix(clips, background_wav, total_sec, out_wav):
    """Place each dubbed clip at its timestamp, then mix with the original background (music+SFX)."""
    base = AudioSegment.silent(duration=int(total_sec * 1000))
    for clip_path, start, end in clips:
        seg = fit_clip(clip_path, end - start)
        base = base.overlay(seg, position=int(start * 1000))
    background = AudioSegment.from_file(background_wav)
    final = background.overlay(base)          # keep music/SFX, add new dialogue on top
    final.export(out_wav, format="wav")
    return out_wav


# ----------------------------------------------------------------------------- 9. remux
def remux(video_path, final_audio_wav, out_video):
    """Replace the video's audio with the dubbed audio."""
    _run(["ffmpeg", "-y", "-i", video_path, "-i", final_audio_wav,
          "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
          "-shortest", out_video])
    return out_video


# ----------------------------------------------------------------------------- orchestrate
def run_pipeline(video_path, target_lang, num_speakers=None, lipsync=False, work_dir=None):
    """Full dub. Returns path to the dubbed video."""
    work_dir = work_dir or tempfile.mkdtemp(prefix="dub_")
    print(">> extract audio");      audio = extract_audio(video_path, os.path.join(work_dir, "audio.wav"))
    print(">> separate (Demucs)");  vocals, background = separate(audio, work_dir)
    print(">> transcribe (Scribe)");segments = transcribe(vocals)
    print(f"   {len(segments)} segments")
    print(">> translate");          segments = translate_segments(segments, target_lang)
    print(">> clone voices");       voices = clone_voices(vocals, segments, work_dir)
    try:
        print(">> synthesize (TTS)");clips = synthesize(segments, voices, work_dir)
        total = audio_duration_sec(audio)
        print(">> align + mix");     final_audio = build_and_mix(clips, background, total,
                                                                 os.path.join(work_dir, "final.wav"))
        out_video = os.path.join(work_dir, "result.mp4")
        print(">> remux");           remux(video_path, final_audio, out_video)
        if lipsync:
            print(">> lip-sync (optional) — wire LatentSync here")
            # out_video = lipsync_step(out_video, final_audio)
        return out_video
    finally:
        delete_voices(voices)        # always clean up cloned voices
