#!/usr/bin/env bash
# ============================================================================
#  ONE-COMMAND SETUP  —  AI Short Film Studio
#  Installs ComfyUI + Manager + ALL custom nodes + creates project folders.
#  You run this ONCE on a fresh RunPod. After this, everything is point-and-click.
#
#  HOW TO RUN (copy these 2 lines into the RunPod web terminal):
#     cd /workspace
#     bash <(curl -s https://raw.githubusercontent.com/YOUR-USERNAME/ai-film-studio/main/setup.sh)
#
#  ...OR if you cloned the repo already:
#     bash /workspace/ai-project/setup.sh
# ============================================================================
set -e   # stop on first error

# --- where everything lives (RunPod persistent disk) ---
ROOT="/workspace"
COMFY="$ROOT/ComfyUI"
NODES="$COMFY/custom_nodes"

echo "================================================================"
echo "  AI FILM STUDIO — auto setup starting"
echo "  This installs ComfyUI + all nodes. Takes ~5-10 min."
echo "================================================================"

cd "$ROOT"

# ---------------------------------------------------------------- ComfyUI
if [ ! -d "$COMFY" ]; then
  echo ">> Installing ComfyUI..."
  git clone https://github.com/comfyanonymous/ComfyUI.git
  pip install -r "$COMFY/requirements.txt"
else
  echo ">> ComfyUI already here, skipping."
fi

mkdir -p "$NODES"
cd "$NODES"

# ---------------------------------------------------------------- helper
clone_node () {   # clone_node <git-url>
  name=$(basename "$1" .git)
  if [ ! -d "$name" ]; then
    echo ">> Installing node: $name"
    git clone "$1"
    # install its requirements if it has any
    [ -f "$name/requirements.txt" ] && pip install -r "$name/requirements.txt" || true
  else
    echo ">> $name already installed, skipping."
  fi
}

# ---------------------------------------------------------------- custom nodes
clone_node https://github.com/ltdrdata/ComfyUI-Manager.git              # the GUI installer (point & click)
clone_node https://github.com/ltdrdata/ComfyUI-Impact-Pack.git          # Face Detailer (anti-plastic)
clone_node https://github.com/ltdrdata/ComfyUI-Impact-Subpack.git       # face detection models
clone_node https://github.com/kijai/ComfyUI-WanVideoWrapper.git         # Wan 2.2 image->video
clone_node https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git  # load/save video
clone_node https://github.com/kijai/ComfyUI-KJNodes.git                 # helper nodes used by Wan
clone_node https://github.com/ShmuelRonen/ComfyUI-LatentSyncWrapper.git # lip sync
clone_node https://github.com/kijai/ComfyUI-MMAudio.git                 # auto sound effects

# ---------------------------------------------------------------- project folders
echo ">> Creating project folder structure..."
PROJ="$ROOT/ai-project"
mkdir -p "$PROJ"/{00_script,01_character/dataset,01_character/output,02_keyframes,03_clips_raw,04_lipsync,05_audio/voice,05_audio/sfx,05_audio/music,06_upscaled,07_final}

# ---------------------------------------------------------------- model folders (empty, fill via Manager)
mkdir -p "$COMFY"/models/{checkpoints,unet,diffusion_models,vae,clip,clip_vision,loras,text_encoders}

echo ""
echo "================================================================"
echo "  ✅ DONE. Nodes + folders installed."
echo ""
echo "  NEXT (all in the browser, no terminal):"
echo "  1. Start ComfyUI:   cd $COMFY && python main.py --listen"
echo "     (On RunPod, use the template's 'Connect' button / port 8188)"
echo "  2. In ComfyUI, click the 'Manager' button (bottom)."
echo "  3. 'Model Manager' -> search & DOWNLOAD with one click:"
echo "        - FLUX.1-dev (fp8)        -> images"
echo "        - Wan 2.2 I2V 14B (fp8)   -> video"
echo "        - umt5 / clip / vae       -> (Manager picks the right folder)"
echo "  4. Copy your trained LoRA into: $COMFY/models/loras/"
echo "  5. Open the workflow guides in ai-project/ and build the graph."
echo "================================================================"
