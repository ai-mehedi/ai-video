# 🛠️ DubStudio — Technical Plan

How to build the dubbing SaaS. Start as a thin wrapper around the ElevenLabs Dubbing API (fast,
cheap to launch), then optionally move to your own pipeline for higher margin.

---

## 1. How it works (user flow)

```
User uploads video → picks source + target language(s) → pays / uses plan minutes
   → backend sends job to ElevenLabs Dubbing API
   → poll for completion → store result → user previews + downloads dubbed video
```

Optional steps: speaker count, voice choice, lip-sync add-on, edit lines (Dubbing Studio style).

---

## 2. Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌────────────────────┐
│  Frontend   │────▶│   Backend / API   │────▶│  ElevenLabs Dubbing │
│ (Next.js)   │     │  (FastAPI/Node)   │     │  API  (the engine)  │
│ upload, UI, │◀────│  jobs, auth,      │◀────│                    │
│ dashboard   │     │  billing, storage │     └────────────────────┘
└─────────────┘     └───────┬──────────┘
                            │
              ┌─────────────┼──────────────┐
              ▼             ▼              ▼
        Auth (Clerk/   Storage (S3/R2:  Payments (Stripe;
        Supabase)      videos)          local: bKash/SSLCommerz)
                            │
                        Database (Postgres: users, jobs, usage minutes)
```

---

## 3. Tech Stack (recommended)

| Layer | Pick | Why |
|---|---|---|
| Frontend | **Next.js + Tailwind** | fast, modern, easy deploy on Vercel |
| Backend | **FastAPI (Python)** or Next API routes | jobs, ElevenLabs calls, webhooks |
| Auth | **Supabase Auth** or Clerk | quick login + user management |
| Database | **Supabase Postgres** | users, jobs, usage tracking |
| File storage | **Cloudflare R2** or AWS S3 | store uploaded + dubbed videos (R2 = cheap, no egress fee) |
| Dubbing engine | **ElevenLabs Dubbing API** | the actual AI dubbing |
| Payments | **Stripe** (global) + **bKash/SSLCommerz** (Bangladesh) | subscriptions + local |
| Hosting | **Vercel** (frontend) + **Railway/Render** (backend) | cheap, simple |
| Queue (later) | Redis / Celery | handle many jobs |

> No GPU needed for the wrapper model — ElevenLabs does the heavy lifting. Cheap to host.

---

## 4. Core backend logic (the key part)

```
POST /api/dub
  1. Auth user, check they have enough plan minutes (or charge pay-as-you-go)
  2. Upload video to storage (R2/S3)
  3. Call ElevenLabs: create dubbing job (source_lang, target_lang, num_speakers)
  4. Save job_id + status in DB, deduct estimated minutes
  5. Poll / webhook until done → save dubbed file URL
  6. Notify user → they preview + download
```

Track **usage minutes per user** in the DB (this is your billing core). Each target language counts
separately. Block or charge overage when minutes run out.

---

## 5. MVP — build the smallest sellable version first

**MVP = upload → dub ONE language → pay → download.** Nothing else. Ship in ~3 weeks.

| # | Build | Done when |
|---|---|---|
| 1 | Landing page + signup/login | users can create an account |
| 2 | Upload video → storage | file lands in R2/S3 |
| 3 | Dub job → ElevenLabs API → poll → store result | one video gets dubbed end-to-end |
| 4 | Dashboard: see jobs, download result | user downloads dubbed video |
| 5 | Stripe: 1 paid plan + free trial (3 min watermarked) | money can be collected |
| 6 | Usage tracking (minutes per user) | overage/limits enforced |

> Skip for MVP: lip-sync, multi-language batch, voice cloning, API access, teams. Add after first
> paying users.

---

## 6. Build Phases (after MVP)

| Phase | Add | Value |
|---|---|---|
| **A (MVP)** | upload → dub 1 lang → pay → download | sellable |
| **B** | multi-language, voice selection, edit lines | more useful, upsell |
| **C** | **lip-sync add-on** (ElevenLabs or LatentSync) | premium revenue |
| **D** | referral, teams, bulk/agency, white-label | growth + B2B |
| **E** | **own pipeline** (Whisper + open TTS + LatentSync) | margin 90%+ |

---

## 7. Own-pipeline option (later — for margin)

Replace ElevenLabs to cut cost per minute from ~$0.40 to ~$0.02–0.05:

```
Whisper (transcribe) → translate (DeepL/NLLB) → XTTS/F5-TTS (clone & speak target lang)
   → Demucs (keep original music/SFX) → LatentSync (lip-sync) → mux back to video
```
Runs on a GPU (RunPod). More work + you maintain quality, but **margin jumps to 90%+** at scale.

> Strategy: **launch on ElevenLabs (fast, reliable), migrate heavy users to own pipeline later.**

---

## 8. Costs to run (tech)

| Item | Early cost |
|---|---|
| Vercel + Railway/Render | ~$0–40/mo |
| Supabase (DB + auth) | free tier → ~$25/mo |
| Cloudflare R2 storage | ~$5–20/mo |
| ElevenLabs API | usage-based (covered by your pricing) |
| **Total fixed** | **~$50–100/mo to start** |

---

## 9. Security & Legal (don't skip)

- **Terms of Service:** user confirms they own/have rights to dub the content (copyright shield).
- Store user files privately; auto-delete after X days (storage cost + privacy).
- Stripe handles card data (don't store cards).
- Privacy policy + GDPR basics.

---

## 10. First build order (do this)

1. Buy domain + set up Next.js on Vercel + Supabase (auth + DB)
2. Build upload → R2 storage
3. Wire ElevenLabs Dubbing API (one language) end-to-end
4. Add Stripe (1 plan + free trial)
5. Usage-minute tracking
6. Polish UI → launch beta to 10 creators

> Ship the MVP, get 10 real users, then add features they ask for. Don't build everything first.

---

### TL;DR
Next.js + Supabase + R2 + **ElevenLabs Dubbing API** + Stripe = a sellable dubbing SaaS in ~3 weeks,
~$50–100/mo to run, 60–85% margin. Launch as a wrapper, move to your own pipeline later for 90%+.
