# 🎬 FLOW STORYBOARD (Start + End Frame) — "First Interview" (~40 sec test film)

Using Veo 3.1 **First & Last Frame** control. For EACH shot:
1. Generate the **START frame** image + the **END frame** image (FLUX free, or Imagen/Flow).
2. In Flow → upload START as first frame, END as last frame.
3. Add the **motion prompt** + dialogue + sound → Generate.
4. Veo fills the motion between the two frames = controlled, consistent result.

**Character (keep identical in every frame):**
> an 18-year-old young man, clean-shaven, neat short black hair, slightly nervous,
> wearing a crisp white shirt and a dark tie, slim build

**Consistency tip:** make ONE good character image first, use it as a Flow **Ingredient**, and base
all frames on it so the same face appears in every shot.

---

## SHOT 01 — Arriving (wide)
- **START frame:** the young man walks toward a tall modern glass corporate building, morning, holding a folder, nervous.
- **END frame:** he reaches the glass entrance doors, hand reaching for the handle, looking up at the building.
- **Motion prompt:** `Cinematic wide shot, slow follow. He walks toward the glass office building and reaches the entrance. Morning light, busy city. Sound: city traffic, footsteps.`

## SHOT 02 — Waiting (medium)
- **START frame:** he sits in a modern glass office lobby, nervous, adjusting his tie, blurred workers behind.
- **END frame:** he looks up alert as his name is called, beginning to stand.
- **Motion prompt:** `Medium shot, slow push-in. He waits nervously, adjusts his tie, then looks up and stands as his name is called. Soft window light. Sound: quiet office ambience, distant phone.`

## SHOT 03 — The interview (medium, DIALOGUE)
- **START frame:** he sits across a desk from a professional interviewer, slightly tense, hands folded.
- **END frame:** he leans forward, more confident, making eye contact.
- **Motion prompt:** `Medium shot, static. He sits across the interviewer, takes a breath, then leans forward confidently. He says: "Good morning. I'm here for the interview. I won't let you down." Sound: quiet room, his calm voice.`

## SHOT 04 — Close-up (emotion)
- **START frame:** close-up of his face, nervous, a bead of sweat, eyes uncertain.
- **END frame:** close-up, his expression shifts to calm determination, a small confident smile.
- **Motion prompt:** `Cinematic close-up, slow push-in. His nervous face slowly turns calm and determined. Realistic skin texture, natural light. Sound: soft ambience, a single breath.`

## SHOT 05 — Handshake
- **START frame:** the interviewer extends a hand across the desk, smiling.
- **END frame:** the two shake hands, the young man smiling with relief.
- **Motion prompt:** `Medium shot, static. The interviewer extends a hand; the young man shakes it, relieved and happy. Warm light. Sound: light office tone, a warm "welcome aboard".`

## SHOT 06 — Leaving (wide, ending)
- **START frame:** he walks out of the glass building doors into daylight, holding the folder.
- **END frame:** he walks away down the street, looks up at the sky, a proud relieved smile.
- **Motion prompt:** `Cinematic wide, slow pull-back. He exits the building, walks into the daylight, looks up and smiles. Hopeful mood, golden light, film grain. Sound: city ambience, uplifting tone.`

---

# 🖼️ FRAME IMAGE PROMPTS (to generate the start/end stills)

Generate these in FLUX (free) or Flow/Imagen. Keep the character line in EVERY one.

| Shot | Frame | Image prompt (add character line first) |
|---|---|---|
| 01 | start | `...walking toward a tall modern glass office building, morning, holding a folder, nervous, wide cinematic, 35mm` |
| 01 | end | `...standing at the glass entrance doors, hand on the handle, looking up, wide cinematic` |
| 02 | start | `...sitting in a modern glass office lobby, adjusting his tie, nervous, blurred workers behind, medium shot` |
| 02 | end | `...in the lobby standing up alert as his name is called, medium shot` |
| 03 | start | `...sitting across a desk from an interviewer, tense, hands folded, office, medium shot` |
| 03 | end | `...leaning forward confidently across the desk, eye contact, medium shot` |
| 04 | start | `...extreme close-up, nervous face, a bead of sweat, uncertain eyes, realistic skin` |
| 04 | end | `...extreme close-up, calm determined face, small confident smile, realistic skin` |
| 05 | start | `...interviewer extending a hand across the desk, smiling, medium shot` |
| 05 | end | `...shaking hands with the interviewer, relieved happy smile, medium shot` |
| 06 | start | `...walking out of glass building doors into daylight, holding a folder, wide cinematic` |
| 06 | end | `...walking away down the street, looking up at the sky, proud smile, golden light, wide` |

---

## Workflow recap
1. Make the 12 frame images (2 per shot) → keep the same face.
2. In Flow: per shot → first frame = START, last frame = END → paste motion prompt → Generate.
3. Veo creates the in-between motion + audio.
4. Download 6 clips → DaVinci → trim, grade, grain → export.

> First/Last frame = the most CONTROL you can get in Flow. Great call.
