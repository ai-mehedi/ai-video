# 🎬 "শেষ রিকশা" — The Last Rickshaw (TEST FILM, ~75 sec)

**Purpose:** First pipeline TEST — uses ANY generated face (not your own), to learn the full flow
(keyframe → video → voice → lipsync → music → edit) before making the real film.

**Genre:** Emotional drama
**Setting:** Old Dhaka, monsoon rain (neon + rain — cinematic and hides AI flaws)
**Main character:** KARIM — old rickshaw puller, 60s, thin, weathered kind face, grey beard, soaked
**Theme:** A poor father's quiet sacrifice for his daughter's future.
**Locations (2):** Old Dhaka rainy alley/street · School gate

> AI design notes: weathered old face = AI does this BETTER than smooth young faces (less plastic).
> Rain hides imperfections. Only 2 locations. Emotion via close-ups. Only 2 short dialogue lines.
> For the test you can SKIP training a LoRA — just generate a consistent old-man face with a fixed
> seed + same description in every keyframe (see status note below).

---

## SCENE 1 — EXT. OLD DHAKA ALLEY — DAWN (RAIN)
*A narrow, wet, neon-lit Old Dhaka lane at dawn. KARIM pulls his empty rickshaw through the rain,
tired but moving. Rain drips from his grey hair and beard.*

*(no dialogue — visuals + rain + sad flute music)*

---

## SCENE 2 — EXT. SHOP AWNING — CONTINUOUS
*KARIM stops under a shop awning. From his chest pocket he takes a folded, wet photo of his young
daughter in a school uniform. He looks at it tenderly.*

**KARIM** *(soft, tired)*
> "আর একটু, মা… আর একটু।"
> *(Aar ektu, ma… aar ektu.)* — "A little more, my child… just a little more."

*He opens a small rusty tin box full of crumpled notes and coins, and adds today's few coins.*

---

## SCENE 3 — EXT. BUSY DHAKA STREET — DAY (RAIN)
*KARIM pulls harder now through a busy rainy street — rickshaw bells, headlights, splashing water.
He is determined.*

*(no dialogue — sound of rain, bells, traffic; music builds)*

---

## SCENE 4 — EXT. SCHOOL GATE — DAY (RAIN)
*KARIM arrives at a school gate. At the admission desk he counts the wet money with trembling hands.
He has just enough. Relief.*

*Then, standing in the rain outside the school, he looks up at the building and smiles — tired,
proud, happy. Rain on his face hides his tears.*

**KARIM** *(whisper, to himself)*
> "হয়ে গেছে।"
> *(Hoye gechhe.)* — "It's done."

**TITLE CARD:** *"বাবা — For every father who gave everything."*

**FADE TO BLACK.**

---

## VOICE (F5-TTS) — both lines are KARIM
Record your reference sample slow, low, aged and tired. 2 short Bangla lines only.

## MUSIC (MusicGen prompts)
- Scene 1–2: "sad solo bamboo flute, slow, lonely, rain, emotional"
- Scene 3: "building emotional strings with soft tabla, determined, hopeful"
- Scene 4: "warm hopeful flute and strings, bittersweet, proud, resolution"

## SFX (MMAudio + Stable Audio Open)
heavy monsoon rain · rickshaw bell · wet street traffic · splashing water · distant city
