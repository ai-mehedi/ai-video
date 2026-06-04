# ============================================================================
#  ⚙️  CONFIG — ALL settings in ONE place. Edit here, nothing else.
#  Every script (make_images, make_videos, make_voice...) reads this file.
# ============================================================================

# ---------------------------------------------------------------- WHICH FILM
# Point to the shot list you want to build (the "brain" of the whole film).
SHOT_LIST = "00_script/test_shot_list.csv"     # test film. For real film: "00_script/shot_list.csv"

# ---------------------------------------------------------------- CHARACTER
# This text is added to EVERY shot so the character looks the same.
# Keep it identical across all shots = consistent face.
CHARACTER = (
    "a 60 year old Bangladeshi rickshaw puller, thin face, weathered dark skin, "
    "short grey beard, kind tired eyes, deep wrinkles"
)

# ---------------------------------------------------------------- STYLE (realism)
# Realism words added to every shot. This fights the "plastic AI" look.
STYLE = (
    "candid documentary photograph, shot on Kodak Portra 400 film, 35mm, photojournalism, "
    "natural imperfect lighting, grainy, realistic skin texture with visible pores, "
    "amateur photo, slightly soft focus, not smooth skin, cinematic"
)

# ---------------------------------------------------------------- IMAGE MODEL (FLUX)
FLUX_MODEL   = "black-forest-labs/FLUX.1-dev"   # downloaded via HuggingFace (needs free token, one time)
REALISM_LORA = "/workspace/runpod-slim/ComfyUI/models/loras/realism_lora.safetensors"  # XLabs realism
LORA_SCALE   = 0.9                              # 0 = off, 0.9 = strong realism

# ---------------------------------------------------------------- IMAGE SETTINGS
WIDTH    = 1216      # cinematic widescreen
HEIGHT   = 832
STEPS    = 28        # higher = better quality, slower
GUIDANCE = 3.0       # LOW (2.5-3.5) = realistic skin. High = plastic.
SEED     = 12345     # FIXED number = same character every shot (consistency!)

# ---------------------------------------------------------------- FOLDERS (auto)
KEYFRAME_DIR = "02_keyframes"
CLIPS_DIR    = "03_clips_raw"
VOICE_DIR    = "05_audio/voice"
MUSIC_DIR    = "05_audio/music"
SFX_DIR      = "05_audio/sfx"

# ---------------------------------------------------------------- VIDEO MODEL (Wan)
WAN_MODEL    = "Wan-AI/Wan2.2-I2V-A14B-Diffusers"   # image-to-video
VIDEO_FRAMES = 81     # 81 frames @16fps ≈ 5 seconds
VIDEO_FPS    = 16
VIDEO_STEPS  = 30

# ---------------------------------------------------------------- VOICE (F5-TTS)
VOICE_REF_AUDIO = "05_audio/voice/ref.wav"    # your 20-30 sec voice sample
VOICE_REF_TEXT  = "this is the exact text spoken in my reference sample"
