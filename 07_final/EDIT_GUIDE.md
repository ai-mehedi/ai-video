# 🎬 FINAL EDIT — DaVinci Resolve (free). This is where it becomes "Netflix".

Raw AI clips never look finished. The **color grade + grain + sound mix** is the last 30% of realism.

## 0. Quick preview first (optional)
Before DaVinci, get a fast rough cut:
```
python pipeline/assemble.py     ->  07_final/rough_cut.mp4
```
Watch it to judge pacing + video quality. Then do the real edit below.

## 1. Import
- Open DaVinci Resolve (free). New project.
- Drag in: `06_upscaled/` (or `03_clips_raw/`) clips, `05_audio/voice/`, `/music/`, `/sfx/`.

## 2. Assemble (Edit page)
- Lay clips on the timeline in shot order (shot_01 → shot_07), following `shot_list.csv`.
- Trim each to the feel you want. Order = your story.

## 3. Sound (Fairlight page)
- Put voice, music, SFX on separate tracks.
- **Ducking:** music auto-dips under dialogue (Dynamics → Ducking).
- EQ voice for clarity. Add reverb to match the space (alley = slap echo, rain = soft).
- Levels: dialogue loudest → SFX support → music under. Master to ~ **-14 LUFS**.

## 4. Color grade (Color page) — the realism magic
1. Balance each shot's exposure/white so all clips MATCH (kills the "different AI look").
2. Apply a **film LUT** (free Kodak/Fuji-style) for a unified cinematic mood.
3. Add subtle **film grain** + light **vignette** → destroys the clean "AI" feel.
4. Optional: gentle **bloom/halation** on neon/highlights for glow.

## 5. Export (Deliver page)
- H.264/H.265, 1080p (or 4K), **24fps** for cinematic feel.
- Save to `07_final/`.

---

## Checklist
- [ ] Clips in order, trimmed
- [ ] Voice synced, music ducked, SFX layered, mastered -14 LUFS
- [ ] All shots color-matched
- [ ] Film LUT + grain + vignette applied
- [ ] Exported 1080p/24fps to 07_final/

> The single biggest "is it real?" upgrade after generation = **color grade + grain here.**
