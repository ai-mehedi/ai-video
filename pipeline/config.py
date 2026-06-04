# ============================================================================
#  ⚙️  CONFIG — ALL settings in ONE place. Edit here, nothing else.
#  Every script + the dashboard reads this file.
# ============================================================================

# ---------------------------------------------------------------- WHICH FILM
SHOT_LIST = "00_script/shot_list.csv"      # the storyboard = the brain of the film

# ---------------------------------------------------------------- CHARACTER
# Added to EVERY shot so the character looks the same (consistency).
# TESTING: a generated character (no LoRA needed).
# REAL FILM: train your LoRA, then put your trigger word here (e.g. "myhero").
CHARACTER = (
    "an 18 year old Bangladeshi man, soft round face, light brown clear skin, "
    "neat short black hair, clean-shaven, nervous dark eyes, slim build, "
    "wearing a crisp white shirt and a dark tie"
)
# (rickshaw film character, swap in when making that one:)
# CHARACTER = "a 60 year old Bangladeshi rickshaw puller, thin face, weathered dark skin, short grey beard, kind tired eyes, deep wrinkles"

# Your trained Character LoRA (the reusable "model"). Empty = off (testing mode).
CHARACTER_LORA = ""        # later: "/workspace/ai-project/01_character/output/myhero.safetensors"
CHARACTER_LORA_SCALE = 0.95

# ---------------------------------------------------------------- STYLE (realism)
STYLE = (
    "candid documentary photograph, shot on Kodak Portra 400 film, 35mm, photojournalism, "
    "natural imperfect lighting, grainy, realistic skin texture with visible pores, "
    "amateur photo, not smooth skin, cinematic"
)

# ---------------------------------------------------------------- IMAGE MODEL (FLUX)
FLUX_MODEL   = "black-forest-labs/FLUX.1-dev"
REALISM_LORA = "/workspace/runpod-slim/ComfyUI/models/loras/realism_lora.safetensors"  # XLabs (anti-plastic)
REALISM_LORA_SCALE = 0.9

WIDTH    = 1216
HEIGHT   = 832
STEPS    = 28
GUIDANCE = 3.0     # LOW = realistic skin. High = plastic.
SEED     = 12345   # FIXED = same character every shot

# ---------------------------------------------------------------- VIDEO MODEL (swappable!)
# This is the KEY switch. Start free with "wan". If quality is poor, change to a
# paid engine later (kling / veo) — the rest of the pipeline stays the same.
VIDEO_ENGINE = "wan"        # "wan" (free, local)  |  "kling" / "veo" (paid API, later)
WAN_MODEL    = "Wan-AI/Wan2.2-I2V-A14B-Diffusers"
VIDEO_FRAMES = 81           # 81 @16fps ≈ 5 sec. Keep clips short (3-6s).
VIDEO_FPS    = 16
VIDEO_STEPS  = 30
# (for paid later) PAID_API_KEY = "..."   # filled in only if you upgrade the video stage

# ---------------------------------------------------------------- VOICE (F5-TTS)
VOICE_REF_AUDIO = "05_audio/voice/ref.wav"   # your 20-30 sec sample
VOICE_REF_TEXT  = "the exact words spoken in my reference sample"

# ---------------------------------------------------------------- MUSIC (MusicGen)
MUSIC_MODEL = "facebook/musicgen-large"

# ---------------------------------------------------------------- STORYBOARD IMAGES (fal.ai)
# Cheap start/end frame images for Google Flow. ~$0.025/image with FLUX Dev.
# Get a free key at fal.ai → set it:  export FAL_KEY="your-key"
STORYBOARD_CSV  = "00_script/storyboard_frames.csv"
STORYBOARD_DIR  = "02_keyframes"            # frames saved here: shot_01_start.png / shot_01_end.png
FAL_MODEL       = "fal-ai/flux/dev"         # realistic + cheap. (schnell = "fal-ai/flux/schnell" cheaper)
FAL_IMAGE_SIZE  = "landscape_16_9"          # widescreen frames
FAL_STEPS       = 28
FAL_GUIDANCE    = 3.5

# ---------------------------------------------------------------- FOLDERS (auto)
KEYFRAME_DIR = "02_keyframes"
CLIPS_DIR    = "03_clips_raw"
LIPSYNC_DIR  = "04_lipsync"
VOICE_DIR    = "05_audio/voice"
MUSIC_DIR    = "05_audio/music"
SFX_DIR      = "05_audio/sfx"
