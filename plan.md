# 🎙️ DubStudio — Full Detailed Plan (Realistic Studio-Quality AI Dubbing SaaS)

A web SaaS that dubs any video into another language at **studio quality**:
- **Same voice, new language** — clone each speaker so a child stays a child, a man stays a man.
- **Keep the background** — music (BGM) + sound effects (SFX) preserved; only the dialogue is replaced.
- **Perfect timing** — translated speech aligned to the original timestamps.
- Built on your **own pipeline** using ElevenLabs raw APIs (cheaper + full control than their packaged Dubbing).

Stack: **own auth · PostgreSQL · S3 · Stripe · ElevenLabs (Scribe + Voice Clone + Multilingual v2/v3)**.

---

# 1. WHY OWN PIPELINE (not ElevenLabs' packaged "Dubbing")

| | ElevenLabs Dubbing product | **Your own pipeline (raw APIs)** |
|---|---|---|
| Pricing | ~$0.24–0.60 / min | **~$0.10 / min** (character-based) |
| BGM / SFX control | limited | ✅ full — you separate & keep them |
| Voice identity | decent | ✅ clone each speaker (child=child) |
| Customization | low | ✅ total (timing, voices, mixing) |
| Margin | 60–85% | **90%+** |

> You assemble the pieces yourself → cheaper, better, fully yours.

---

# 2. THE DUBBING PIPELINE (the core engine — studio quality)

```
1. INGEST        video → extract audio (ffmpeg)
2. SEPARATE      audio → [vocals] + [background music + SFX]   (Demucs)   ← keeps BGM/SFX
3. TRANSCRIBE    vocals → text + word timestamps + speaker labels   (ElevenLabs Scribe)
4. TRANSLATE     text → target language (keep meaning + length)   (DeepL / GPT)
5. VOICE CLONE   per speaker → instant voice clone from their original audio   (ElevenLabs IVC)
                 → child voice stays child, each speaker keeps their tone
6. TTS           translated lines → speech in the cloned voice   (Multilingual v2/v3)
7. ALIGN         fit each generated line to the original timestamp (stretch/pad to match)
8. MIX           new dialogue + ORIGINAL background (BGM/SFX)  → final audio   (ffmpeg/pydub)
9. REMUX         final audio onto the video
10. LIP-SYNC     (optional add-on) mouth matches new language   (LatentSync / paid)
```

**Result:** the video sounds like the SAME people speaking the NEW language, with all the original
music and effects intact. That's real studio dubbing.

---

# 3. ELEVENLABS MODELS USED + COST (character-based)

| Model | Use | Price |
|---|---|---|
| **Scribe v1/v2** | Speech→Text (transcribe + timestamps + speakers) | **$0.22 / hour** |
| **Scribe v2 Realtime** | (optional) live transcription | $0.39 / hour |
| **Multilingual v2 / v3** | high-quality TTS in cloned voice, 32 langs | **$0.10 / 1K chars** |
| **Flash / Turbo** | faster/cheaper TTS (lower cost tier) | **$0.05 / 1K chars** |
| Instant Voice Clone (IVC) | clone speaker from sample | included with plan |

### Cost per minute of dubbing (the real number)
- 1 min of speech ≈ **~900 characters** (~150 words)
- Transcribe (Scribe): $0.22/hr ÷ 60 = **~$0.004/min**
- TTS (Multilingual v2): 900 × $0.10/1000 = **~$0.09/min**  (Flash: ~$0.045/min)
- Demucs separation: runs on your GPU/CPU ≈ **~$0** (your compute)
- **Total ≈ $0.10 / min** (or ~$0.05/min with Flash)

### Margin
| | Cost | Sell | Margin |
|---|---|---|---|
| Per minute | ~$0.05–0.10 | $1.00–2.50 | **90%+** |

---

# 4. PRICING (what you charge)

Subscription minutes + overage. Each target language = separate minutes.

| Plan | Price/mo | Included | Overage | Lip-sync add-on |
|---|---|---|---|---|
| Free trial | $0 | 3 min (watermark) | — | — |
| **Starter** | **$19** | 30 min | $1.20/min | +$1/min |
| **Pro** | **$49** | 120 min | $0.90/min | +$1/min |
| **Business** | **$149** | 500 min | $0.60/min | +$1/min |
| Pay-as-you-go | — | — | $2.00/min | +$1/min |

Add-ons (extra revenue): lip-sync, voice cloning library, rush processing, API access, white-label.

---

# 5. ARCHITECTURE

```
┌──────────────┐   HTTPS   ┌─────────────────────┐
│  Frontend    │◀────────▶│   Backend API        │
│  Next.js     │           │   FastAPI (Python)   │
│  upload, UI, │           │   own JWT auth       │
│  dashboard,  │           │   jobs + billing     │
│  player      │           └──────┬──────────────┘
└──────────────┘                  │
        ┌──────────────┬──────────┼───────────────┬───────────────┐
        ▼              ▼          ▼               ▼               ▼
   PostgreSQL      S3 storage   Worker (GPU)   ElevenLabs API   Stripe
   users, jobs,    videos +     Demucs +       Scribe + Clone   subscriptions
   usage, subs     audio        align + mix    + Multilingual   + webhooks
```

- **Backend** = FastAPI (Python) — perfect for the audio pipeline + ML libs.
- **Worker** = a GPU box (RunPod/your server) that runs Demucs + alignment + mixing; calls ElevenLabs for STT/TTS. Jobs queued (Redis/Celery).
- **Frontend** = Next.js (Vercel).

---

# 6. OWN AUTH SYSTEM (no third-party)

- **Signup/login:** email + password.
- **Passwords:** hashed with **bcrypt** (never store plain).
- **Sessions:** **JWT** access token (short-lived) + refresh token (httpOnly cookie).
- **Email verify** + password reset (token links, sent via Resend/SES).
- **Roles:** user / admin.
- **Rate limiting** on auth endpoints.

Endpoints:
```
POST /auth/signup        POST /auth/login        POST /auth/refresh
POST /auth/logout        POST /auth/verify-email POST /auth/forgot-password
POST /auth/reset-password GET  /auth/me
```

---

# 7. DATABASE (PostgreSQL) — schema

```sql
users(            id, email, password_hash, name, email_verified, role, created_at )
subscriptions(    id, user_id, stripe_customer_id, stripe_sub_id, plan, status,
                  minutes_included, minutes_used, renews_at )
projects(         id, user_id, title, source_lang, created_at )
jobs(             id, project_id, user_id, status,           -- queued|processing|done|failed
                  source_video_url, target_lang, num_speakers,
                  result_video_url, duration_min, lipsync, cost_cents, created_at )
voices(           id, user_id, job_id, speaker_label, eleven_voice_id )   -- cloned voices
usage_events(     id, user_id, job_id, minutes, chars, api_cost_cents, created_at )
```

`minutes_used` vs `minutes_included` = the billing gate. Block/charge overage when exceeded.

---

# 8. BACKEND API (main endpoints)

```
POST /projects                      create project
POST /jobs           { project_id, target_lang, num_speakers, lipsync }  -> start dubbing
GET  /jobs/:id                      status + result url (poll)
GET  /jobs                          list my jobs
POST /uploads/sign                  get S3 presigned URL (client uploads video directly)
POST /billing/checkout              Stripe checkout session
POST /billing/webhook               Stripe events (sub created/updated/cancelled)
GET  /me/usage                      minutes used / included
```

### Job processing (worker)
```
on new job:
  1. check user has minutes (else 402)
  2. download video from S3 → ffmpeg extract audio
  3. Demucs → vocals.wav + background.wav
  4. Scribe (vocals) → segments[{start,end,speaker,text}]
  5. translate each segment text → target lang
  6. for each speaker: IVC clone from their vocal slices → voice_id
  7. for each segment: Multilingual TTS(text, voice_id) → clip, time-fit to [start,end]
  8. concat clips on a silent timeline at timestamps → new_vocals.wav
  9. mix new_vocals + background.wav → final_audio.wav
  10. ffmpeg remux final_audio onto video → result.mp4
  11. (if lipsync) LatentSync(result.mp4, final_audio) 
  12. upload result to S3, set job done, record usage + cost
```

---

# 9. KEEPING BGM / SFX + VOICE IDENTITY (the quality secret)

- **BGM/SFX preserved:** Demucs splits audio into *vocals* and *everything else*. You only replace
  vocals; the *everything else* (music, effects, ambience) is kept and mixed back. ✅
- **Voice identity preserved:** ElevenLabs **Instant Voice Clone** per speaker → the cloned voice
  carries age/gender/tone, so a **child sounds like a child**, an old man like an old man, in the
  new language. ✅
- **Multi-speaker:** Scribe gives speaker labels → clone + dub each speaker separately.
- **Timing:** place each dubbed line at its original timestamp; gently stretch/compress to fit so
  it stays in sync with the picture.

---

# 10. TECH STACK (summary)

| Layer | Pick |
|---|---|
| Frontend | Next.js + Tailwind (Vercel) |
| Backend API | FastAPI (Python) |
| Auth | own (bcrypt + JWT) |
| Database | PostgreSQL (Supabase/Neon/RDS) |
| Storage | AWS S3 (or Cloudflare R2) |
| Queue/worker | Redis + Celery, worker on RunPod GPU |
| Audio | ffmpeg, Demucs, pydub |
| Dubbing AI | ElevenLabs (Scribe, IVC, Multilingual v2/v3) |
| Translate | DeepL or GPT |
| Lip-sync (add-on) | LatentSync (own) or paid |
| Payments | Stripe (+ bKash/SSLCommerz for Bangladesh) |

---

# 11. MVP — smallest sellable version (~3–4 weeks)

Ship this first, nothing more:
1. Own auth (signup/login/JWT)
2. Upload video (S3 presigned) — **hard 5-min cap, validate duration before queuing**
3. Worker: extract → Demucs → Scribe → translate → IVC clone → TTS → align → mix → remux (1 language)
4. Dashboard: job status + download result
5. Stripe: free trial (3 min, watermark) + 1 paid plan
6. Usage-minute tracking

**Skip for MVP:** lip-sync, multi-language batch, voice library, API, teams. Add after first users.

---

# 12. BUILD PHASES (after MVP)

| Phase | Add | Why |
|---|---|---|
| A (MVP) | upload → dub 1 lang → pay → download | sellable |
| B | multi-language, voice picker, edit lines | upsell |
| C | **lip-sync add-on** | premium revenue |
| D | referral, teams, agency/white-label, API | growth + B2B |
| E | own self-hosted TTS/STT for top languages | cut even ElevenLabs cost |

---

# 13. SECURITY & LEGAL

- Passwords bcrypt; JWT short-lived + refresh in httpOnly cookie.
- **ToS:** user confirms they have rights to dub the content (copyright shield).
- Auto-delete user media after N days (privacy + storage cost).
- Stripe handles cards (PCI). HTTPS everywhere. Rate-limit auth + jobs.
- Private S3 buckets; signed URLs for downloads.

---

# 14. COSTS TO RUN

| Item | Early cost |
|---|---|
| Vercel + backend host | ~$0–40/mo |
| PostgreSQL (Neon/Supabase) | free → ~$25/mo |
| S3/R2 storage | ~$5–20/mo |
| GPU worker (RunPod, on-demand) | pay per job (~cents/min) |
| ElevenLabs API | ~$0.05–0.10/min dubbed (in your pricing) |
| **Fixed total** | **~$50–100/mo to launch** |

---

# 15. SCALING, CONCURRENCY & VIDEO LENGTH LIMITS

The #1 risk for a video SaaS: heavy jobs + many users at once. Solved with **length caps + a job
queue + autoscaling workers**. Never let the web server do the heavy work.

## 15.1 Video length limits (hard caps — protect the app)
A 1-hour video = 60× the cost/time of a 1-min clip → can crash a worker (memory), block the queue,
and run up huge API bills. So cap length per plan:

| Plan | Max video length | Notes |
|---|---|---|
| Free trial | **2 min** | enough to test |
| Starter | **5 min** | shorts, ads, clips |
| Pro | **15 min** | lessons, longer content |
| Business | **30–60 min** | via chunking (15.5) |

> **MVP = hard 5-min cap.** Reject longer uploads with: *"Max 5 minutes — please split your video."*
> Validate duration on upload (ffprobe) BEFORE queuing.

## 15.2 Why heavy jobs don't crash the server
The web/API server **only accepts the upload and queues a job** (~0.1s) → it can serve thousands of
concurrent users. All heavy work (Demucs, Scribe, TTS, mix) happens in **background workers**, not
on the API server. Users get an async **"we'll notify you when ready"** (like HeyGen/Descript).

```
Users ──▶ API server (light, queues job) ──▶ Redis QUEUE ──▶ Worker pool (GPU, autoscale 1→N)
                                                                   │ Demucs→Scribe→clone→TTS→mix
                                                                   ▼
                                                      Result → S3 → notify user 🎬
```

## 15.3 Autoscaling workers (RunPod Serverless or cloud autoscale)
- **Queue empty** → 0 workers → **$0 cost** (scale to zero)
- **Queue grows** → spin up more GPU workers (e.g. 1 per ~5 waiting jobs, up to a max)
- **Queue clears** → scale back down
- You **pay only while processing** → spiky demand handled cheaply

## 15.4 Per-user concurrency + priority (so no one hogs)
| Plan | Jobs at once | Queue priority |
|---|---|---|
| Free | 1 | lowest |
| Starter | 2 | normal |
| Pro | 3 | high |
| Business | 10 | highest |

Paid jobs jump the line (priority queue). One user can't flood the system.

## 15.5 Long videos LATER — chunking (no giant jobs ever)
To support 30–60 min on higher tiers without killing the app, **split, don't lengthen**:
```
1-hour video → split into 12 × 5-min chunks → 12 workers process IN PARALLEL → stitch back
```
Each chunk is a small, safe job. With enough workers, a 1-hour video finishes about as fast as a
5-min one. Add this as a Business feature after MVP.

## 15.6 Other protections
- **Validate duration on upload** (ffprobe) — reject over-limit before queuing.
- **DB connection pooling** (PgBouncer) so the database doesn't choke.
- **Rate limiting** on API + auth endpoints.
- **Idempotent jobs + retries**; **dead-letter queue** for failures (don't silently lose jobs).
- **Auto-delete** media after N days (storage + privacy).
- **ElevenLabs rate limits:** queue API calls; request higher limits as you grow.

---

# 16. 90-DAY ROADMAP

- **Wk 1–4:** build MVP (auth → upload → dub pipeline → pay → download)
- **Wk 5–6:** beta 10 creators (free) → testimonials + fixes
- **Wk 7–9:** launch Starter/Pro; you start sales outreach (South Asia niche)
- **Wk 10–12:** add lip-sync + referral → push to **50 paying users (~$2k MRR)**

---

### TL;DR
Own pipeline = **Demucs (keep BGM/SFX) + Scribe (transcribe) + Instant Voice Clone (keep each
voice) + Multilingual TTS (new language) + align + mix + remux.** Cost **~$0.10/min**, sell
**$1–2.50/min**, **90%+ margin**. Stack: own auth + Postgres + S3 + Stripe + ElevenLabs. Ship a
1-language MVP in ~3–4 weeks, then add lip-sync and scale.

**Scale safely:** hard **5-min cap** at MVP, **queue + autoscaling GPU workers** (scale to zero when
idle), per-user concurrency limits, and **chunking** for long videos later. The web server only
queues jobs — heavy work runs in background workers, so many users never crash it.
