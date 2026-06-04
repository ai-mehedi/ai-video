#!/usr/bin/env python3
# ============================================================================
#  🎛️  STUDIO DASHBOARD — control the whole film from ONE web screen.
#  RUN:  python pipeline/dashboard.py    → open the public https://...gradio.live link
# ============================================================================
import os, sys, csv, subprocess
import gradio as gr

sys.path.insert(0, os.path.dirname(__file__))
import config as C
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT)
for d in (C.KEYFRAME_DIR, C.CLIPS_DIR, C.VOICE_DIR, C.MUSIC_DIR):
    os.makedirs(d, exist_ok=True)

_pipe = None
def get_pipe(character_lora_scale, realism_scale):
    global _pipe
    if _pipe is None:
        import torch
        from diffusers import FluxPipeline
        print("Loading FLUX (first run downloads ~24GB)...")
        _pipe = FluxPipeline.from_pretrained(C.FLUX_MODEL, torch_dtype=torch.bfloat16).to("cuda")
        names, scales = [], []
        if C.REALISM_LORA and os.path.exists(C.REALISM_LORA):
            _pipe.load_lora_weights(C.REALISM_LORA, adapter_name="realism"); names.append("realism"); scales.append(realism_scale)
        if C.CHARACTER_LORA and os.path.exists(C.CHARACTER_LORA):
            _pipe.load_lora_weights(C.CHARACTER_LORA, adapter_name="character"); names.append("character"); scales.append(character_lora_scale)
        if names: _pipe.set_adapters(names, adapter_weights=scales)
    return _pipe

def load_shots():
    with open(C.SHOT_LIST, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def shots_table():
    rows = load_shots()
    cols = ["shot_id","scene","shot_scale","location","character_action","dialogue","status"]
    return [[r.get(c,"") for c in cols] for r in rows], cols

def build_prompt(r, character, style):
    parts = [character, r.get("character_action",""), r.get("location",""),
             r.get("time_lighting",""), f'{r.get("shot_scale","")} shot', r.get("emotion",""), style]
    return ", ".join(p for p in parts if p and p.strip())

def gen_one(shot_id, character, style, guidance, seed):
    import torch
    rows = {r["shot_id"]: r for r in load_shots()}
    if shot_id not in rows: return None, f"Shot {shot_id} not found."
    prompt = build_prompt(rows[shot_id], character, style)
    pipe = get_pipe(C.CHARACTER_LORA_SCALE, C.REALISM_LORA_SCALE)
    g = torch.Generator("cuda").manual_seed(int(seed)+int(shot_id))
    img = pipe(prompt=prompt, width=C.WIDTH, height=C.HEIGHT,
               num_inference_steps=C.STEPS, guidance_scale=float(guidance), generator=g).images[0]
    out = os.path.join(C.KEYFRAME_DIR, f"shot_{shot_id}.png"); img.save(out)
    return img, f"✅ {out}\n\n{prompt}"

def gen_all(character, style, guidance, seed, progress=gr.Progress()):
    g=[]
    for r in progress.tqdm(load_shots(), desc="Shots"):
        img,_ = gen_one(r["shot_id"], character, style, guidance, seed)
        if img is not None: g.append((img, f"shot_{r['shot_id']}"))
    return g, f"✅ {len(g)} keyframes in {C.KEYFRAME_DIR}/"

def imgs_gallery():
    d=C.KEYFRAME_DIR
    return [(os.path.join(d,f),f) for f in sorted(os.listdir(d))] if os.path.isdir(d) else []

def vids_list():
    d=C.CLIPS_DIR
    return [os.path.join(d,f) for f in sorted(os.listdir(d)) if f.endswith(".mp4")] if os.path.isdir(d) else []

def make_videos_cli(shot):
    cmd = [sys.executable, "pipeline/make_videos.py"] + ([shot] if shot.strip() else [])
    subprocess.Popen(cmd)
    return f"▶ Started video generation ({'shot '+shot if shot.strip() else 'all shots'}). Refresh in a few minutes."

with gr.Blocks(title="AI Film Studio", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🎬 AI Film Studio — Dashboard")

    with gr.Tab("📋 Storyboard"):
        data, cols = shots_table()
        gr.Dataframe(value=data, headers=cols, interactive=False, wrap=True)
        gr.Markdown(f"Source: `{C.SHOT_LIST}` — edit it to change the film.")

    with gr.Tab("⚙️ Character & Style"):
        character = gr.Textbox(value=C.CHARACTER, label="Character (same every shot)", lines=3)
        style     = gr.Textbox(value=C.STYLE, label="Realism style", lines=3)
        guidance  = gr.Slider(1.5,5.0,value=C.GUIDANCE,step=0.1,label="Guidance (low=real, high=plastic)")
        seed      = gr.Number(value=C.SEED, label="Seed (fixed = consistent character)")

    with gr.Tab("🖼️ Keyframes"):
        with gr.Row():
            with gr.Column():
                shot_id = gr.Textbox(value="01", label="Shot ID")
                b1 = gr.Button("🎬 Generate THIS shot", variant="primary")
                b2 = gr.Button("🎬🎬 Generate ALL")
                st = gr.Textbox(label="Status", lines=5)
            with gr.Column():
                out_img = gr.Image(label="Result", height=380)
        b3 = gr.Button("🔄 Refresh gallery")
        gal = gr.Gallery(value=imgs_gallery(), label="Keyframes", columns=4, height=360)
        b1.click(gen_one,[shot_id,character,style,guidance,seed],[out_img,st])
        b2.click(gen_all,[character,style,guidance,seed],[gal,st])
        b3.click(lambda: imgs_gallery(), None, gal)

    with gr.Tab("🎞️ Video"):
        gr.Markdown("Animate keyframes → clips (engine = **%s** from config). Judge quality here." % C.VIDEO_ENGINE)
        vshot = gr.Textbox(value="", label="Shot ID (empty = all)")
        vbtn = gr.Button("▶ Make video(s)", variant="primary")
        vst  = gr.Textbox(label="Status", lines=2)
        vref = gr.Button("🔄 Refresh clips")
        vid  = gr.Video(label="Preview a clip")
        vlist= gr.Dropdown(choices=vids_list(), label="Clips", interactive=True)
        vbtn.click(make_videos_cli,[vshot],[vst])
        vref.click(lambda: gr.update(choices=vids_list()), None, vlist)
        vlist.change(lambda p: p, vlist, vid)

    with gr.Tab("🎙️ Voice & Music"):
        gr.Markdown("Run from terminal for now:\n```\npython pipeline/make_voice.py\npython pipeline/make_music.py\n```")

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=True)
