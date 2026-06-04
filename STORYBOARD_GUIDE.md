# 🎬 STORYBOARD MASTER GUIDE (A–Z) — Realistic AI Film with Veo / Flow

Everything to make a realistic, consistent AI short film: character sheets, positive + negative
keywords, camera & lighting glossary, the realism formula, a full worked example storyboard,
start/end-frame technique, dialogue, and troubleshooting. Use this for every film.

---

# 1. THE REALISM FORMULA (memorize this)

```
REALISM = Real Character + Photo Style + Right Camera + Natural Light + Imperfection + Grain
```
Every prompt should hit these 6. Miss one → it looks "AI". The biggest realism killers are:
**smooth skin, perfect lighting, too clean, no grain.** Always fight those.

---

# 2. CHARACTER SHEET (define ONCE, reuse everywhere)

Write your character with ALL of these fixed attributes. Copy the SAME block into every shot so the
face never changes. This is your "reusable character".

**Template:**
```
[age] year old [nationality] [gender], [face shape], [skin tone + texture], [hair: length/color/style],
[facial hair], [eyes], [build], wearing [exact clothing], [distinguishing mark]
```

**Example — Karim (rickshaw puller):**
```
a 60 year old Bangladeshi man, thin angular face, dark weathered skin with deep wrinkles and visible
pores, short messy grey hair, short grey beard, tired kind brown eyes, thin frail build, wearing a
worn faded grey shirt, a small scar on left cheek
```

**Example — Arif (interview, 18):**
```
an 18 year old Bangladeshi man, soft round face, light brown clear skin, neat short black hair,
clean-shaven, nervous dark eyes, slim build, wearing a crisp white shirt and a slightly oversized
dark tie
```

> ⭐ Rule: NEVER change the character words between shots. Change only the action/place/camera.
> In Flow, also upload 1–3 reference images as an **Ingredient** to lock the face even harder.

---

# 3. POSITIVE KEYWORDS (realism library — pick from each group)

**📸 Photo style (most important):**
`candid photograph, documentary photography, photojournalism, amateur iphone photo, shot on film,
shot on Kodak Portra 400, 35mm, analog photo, unposed, real life, paparazzi shot`

**🧑 Skin & face realism (kills plastic):**
`realistic skin texture, visible skin pores, skin imperfections, blemishes, freckles, fine wrinkles,
slightly oily skin, natural sweat, subsurface scattering, peach fuzz, asymmetrical face, NOT smooth`

**💡 Lighting (natural = real):**
`natural lighting, soft window light, overcast light, golden hour, harsh midday sun, dim warm light,
practical lights, moody low light, backlight, rim light, candlelight, neon glow`

**🎥 Camera & lens:**
`shallow depth of field, bokeh, 35mm, 50mm, 85mm portrait lens, slight motion blur, handheld,
cinematic composition, wide shot, close-up, over-the-shoulder, rule of thirds`

**🎞️ Texture & finish:**
`film grain, analog noise, slight chromatic aberration, lens flare, vignette, soft focus, dust in air`

**🎭 Mood & cinematic:**
`cinematic, dramatic, intimate, melancholic, tense, hopeful, atmospheric, moody`

---

# 4. NEGATIVE KEYWORDS (what to AVOID — for tools that support negatives)

> Veo/Flow don't use a separate negative box, so write "no ___" in the prompt OR avoid these looks.
> FLUX (your free image stage) and ComfyUI DO use negatives — paste these there.

```
plastic skin, smooth skin, airbrushed, waxy, doll-like, cgi, 3d render, video game, cartoon, anime,
illustration, painting, over-saturated, oversharpened, perfect symmetry, fake, artificial lighting,
studio lighting, beauty filter, instagram filter, glossy, mannequin, uncanny, deformed face,
extra fingers, extra limbs, distorted hands, blurry, low quality, watermark, text
```

---

# 5. CAMERA & SHOT GLOSSARY (use the right one per emotion)

| Shot scale | Use for | Keyword |
|---|---|---|
| Extreme wide | establish location | `extreme wide shot, establishing shot` |
| Wide | full body + setting | `wide shot` |
| Medium | conversation, body language | `medium shot` |
| Close-up | emotion, face | `close-up` |
| Extreme close-up | intense emotion, eyes | `extreme close-up` |
| Over-the-shoulder | dialogue between two | `over-the-shoulder shot` |

| Camera move | Feeling | Keyword |
|---|---|---|
| Static | calm, tension | `static camera, locked off` |
| Slow push-in | building emotion | `slow push in, slow dolly in` |
| Slow pull-back | reveal, ending | `slow pull back, dolly out` |
| Pan | follow action | `slow pan left/right` |
| Handheld | urgency, realism | `handheld, subtle camera shake` |
| Tracking/follow | walking with subject | `tracking shot, follow` |

> 🔑 Slow + simple = clean animation. Fast/complex = AI breaks faces. Keep clips 3–8 sec.

---

# 6. LIGHTING GLOSSARY (mood = light)

| Look | Keyword | Mood |
|---|---|---|
| Golden hour | `warm golden hour, low sun` | hopeful, nostalgic |
| Overcast | `soft overcast, grey diffused light` | sad, calm, realistic |
| Night neon | `neon glow, wet reflections, night` | moody, urban |
| Window light | `soft window light, side light` | intimate |
| Harsh sun | `harsh midday sun, hard shadows` | tense, exposed |
| Low key | `dim warm light, deep shadows` | drama, mystery |

---

# 7. VEO / FLOW PROMPT STRUCTURE (the order that works)

```
[Shot scale + camera move]. [CHARACTER block]. [Action]. [Location + lighting].
[He/She says: "dialogue"]. [Mood + photo style + grain]. Sound: [ambience + voice].
```

**Filled example:**
> Cinematic medium shot, slow push-in. An 18 year old Bangladeshi man, soft round face, neat short
> black hair, clean-shaven, nervous eyes, white shirt and dark tie. He sits across a desk, takes a
> breath, then leans forward confidently. Modern office, soft window light. He says: "Good morning.
> I'm here for the interview." Cinematic, realistic skin texture, 35mm film grain. Sound: quiet
> office ambience, his calm voice.

---

# 8. START + END FRAME TECHNIQUE (best control in Veo 3.1)

For each shot, make TWO images (start + end), upload both, Veo fills the motion.

```
SHOT = { start_frame_image, end_frame_image, motion_prompt, dialogue, sound }
```
- **Start frame** = how the shot opens (e.g. nervous, sitting back)
- **End frame** = how it closes (e.g. confident, leaning forward)
- **Motion prompt** = describe the change + camera + dialogue
- Keep the CHARACTER block identical in both frame images.

---

# 9. FULL WORKED EXAMPLE — "First Interview" (storyboard)

**Character (every frame):** `an 18 year old Bangladeshi man, soft round face, light brown skin,
neat short black hair, clean-shaven, nervous dark eyes, slim build, white shirt and dark tie`

| Shot | Scale / Move | Start frame | End frame | Motion + Dialogue | Sound |
|---|---|---|---|---|---|
| 01 | wide / follow | walking toward glass office building, morning | hand on entrance door, looking up | walks to entrance, nervous | city traffic, footsteps |
| 02 | medium / push-in | sitting in lobby, adjusting tie | stands as name is called | waits, then stands | office ambience, phone |
| 03 | medium / static | sits across interviewer, tense | leans forward, confident | "Good morning. I'm here for the interview. I won't let you down." | quiet room, voice |
| 04 | close-up / push-in | nervous face, bead of sweat | calm, small confident smile | expression shifts to determined | soft ambience, a breath |
| 05 | medium / static | interviewer extends hand | they shake, he smiles relieved | handshake, relief | warm tone, "welcome aboard" |
| 06 | wide / pull-back | exits building into daylight | walks away, looks up, proud smile | leaves, hopeful | city ambience, uplifting tone |

**Each shot's full prompt** = combine: Character + Start→End action + lighting + dialogue + Sound,
using the structure in section 7.

---

# 10. CONSISTENCY CHECKLIST (per shot)

- [ ] Same CHARACTER block word-for-word
- [ ] Same wardrobe wording
- [ ] Same Flow Ingredient (reference image) selected
- [ ] Location + lighting words match scene-mates
- [ ] Clip 3–8 sec, slow camera
- [ ] Realism keywords present (skin texture, film, grain)
- [ ] Dialogue in quotes + a "Sound:" line

---

# 11. TROUBLESHOOTING

| Problem | Cause | Fix |
|---|---|---|
| Plastic / waxy face | missing realism words | add `skin pores, candid photo, film grain, not smooth` + lower guidance |
| Face changes between shots | no identity lock | use SAME character block + Flow Ingredient image |
| Face warps during motion | clip too long / fast | shorter clip (3–4s), slow camera, medium shot not extreme close |
| Lips don't match speech | non-English / long line | short line; English syncs best in Veo |
| Location keeps changing | loose location words | copy exact location + lighting text every shot |
| Looks like a cartoon | style words wrong | remove `illustration/anime`, add `photograph, 35mm, realistic` |
| Too clean / fake | no imperfection | add grain, sweat, blemishes, handheld, natural light |

---

# 12. THE 5 GOLDEN RULES

1. **One character block, never changed** = consistency.
2. **"Candid photograph + film grain + skin pores"** = the core anti-plastic combo.
3. **Slow camera, short clips (3–8s)** = clean motion.
4. **Natural light + imperfection** > perfect/clean.
5. **Finish in DaVinci** (color grade + grain) = the final 20% of realism.

---

> Keep this open while you build. Fill the table in section 9 for YOUR story, generate start/end
> frames, run them in Flow shot by shot. That's a full realistic film.
