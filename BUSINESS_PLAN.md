# 💼 DubStudio — Business Plan

AI dubbing SaaS. Customers upload a video, choose a language, get a professionally dubbed video
with natural AI voices. You sell it by subscription + per-minute. You run sales; this plan covers
the model, pricing, margins, and go-to-market.

---

## 1. The Problem & The Product

**Problem:** Creators & businesses want to reach new-language audiences, but human dubbing is
**expensive ($75–150/min), slow (days), and hard to organize.**

**Product (DubStudio):** Upload a video → pick target language(s) → get a dubbed video in minutes,
natural AI voices, optional lip-sync. **10–50× cheaper, minutes not days.**

**One-liner:** *"Dub any video into any language in minutes — for the price of a coffee."*

---

## 2. Target Customers (who you sell to)

| Segment | Why they pay | Where to find them |
|---|---|---|
| 🎬 YouTubers / creators | reach global audience, more views/revenue | YouTube, creator FB groups, Discord |
| 🎓 Course / e-learning creators | sell courses in more languages | Udemy/Teachable creators, LinkedIn |
| 📣 Marketers / agencies | localize ads & promos for clients | agencies, Upwork, LinkedIn |
| 🏢 Small businesses | product videos in local languages | local business groups |
| 🌏 Regional media (South Asia) | English ⇄ Bangla/Hindi/Urdu content | your home market — your edge |

**Your edge:** you know the **South Asia market**. Start there (Bangla/Hindi/Urdu dubbing) where big
players underfocus, then expand. Less competition, warm network for sales.

---

## 3. Business Model

**Reseller / wrapper model** (fastest, lowest risk):
- Backend uses **ElevenLabs Dubbing API** (you don't build the AI).
- You add: clean UI, accounts, payments, project management, support.
- You **mark up the per-minute cost** + charge subscriptions.

Later (for margin): swap to your **own pipeline** (Whisper + open TTS + LatentSync) → cost drops to
near-zero per minute → margin jumps. (See `TECH_PLAN.md`.)

---

## 4. Pricing (what you charge)

**Hybrid: subscription tiers + per-minute overage.** Each target language = separate minutes.

| Plan | Price/mo | Included dubbing | Overage | For |
|---|---|---|---|---|
| **Free trial** | $0 | 3 min (watermarked) | — | try it |
| **Starter** | **$19** | 30 min | $1.50/min | small creators |
| **Pro** | **$49** | 100 min | $1.20/min | active creators |
| **Business** | **$149** | 400 min | $0.90/min | agencies/teams |
| Pay-as-you-go | — | — | **$2.50/min** | one-off jobs |

> Add-ons (extra revenue): **lip-sync** (+$1/min), **extra voices / voice cloning**, **priority
> processing**, **rush delivery**, **API access** for businesses.

---

## 5. Margins (how you make money)

| | Cost (you pay ElevenLabs) | You charge | Margin |
|---|---|---|---|
| Per minute | ~$0.24–0.60 | $0.90–2.50 | **60–85%** |

**Example — Pro plan ($49 for 100 min):**
- Your cost: 100 min × ~$0.40 = **$40** … tight at full use, but most users don't use all minutes
- Realistic: avg user dubs ~40 min → cost ~$16 → **$33 profit/user/month**
- **Unused-minutes economics** (like a gym) = healthy margin.

**With your OWN pipeline later:** cost/min drops to ~$0.02–0.05 → margin **90%+**.

### Simple revenue math
| Paying users | Avg $/user/mo | Monthly revenue | Est. profit (70%) |
|---|---|---|---|
| 50 | $40 | $2,000 | ~$1,400 |
| 200 | $40 | $8,000 | ~$5,600 |
| 1,000 | $40 | $40,000 | ~$28,000 |

---

## 6. Go-To-Market (your sales plan)

**Phase 1 — Niche launch (South Asia / a creator niche)**
- Pick ONE niche (e.g. "dub English courses into Bangla/Hindi").
- DM 50 creators/agencies, offer free dub of 1 video → convert to paid.
- Post before/after dubbing demos on YouTube/TikTok/LinkedIn (proof sells).

**Phase 2 — Content + referrals**
- Publish "how to dub your video" content (SEO) → inbound signups.
- Referral: give 30 free minutes for each referred paying user.

**Phase 3 — Agencies & API**
- Sell **bulk/white-label** to agencies (higher value, recurring).
- Offer **API access** to businesses (sticky, high-margin).

**Sales channels:** direct DMs/outreach, creator communities, YouTube demos, LinkedIn (B2B),
local business networks, Fiverr/Upwork (find people already buying dubbing).

---

## 7. Competition & Positioning

| Competitor | Their gap → your angle |
|---|---|
| ElevenLabs (direct) | technical/general → you = **niche, done-for-you, regional languages** |
| HeyGen / Rask | pricey, English-first → you = **cheaper, South-Asia focus, simpler** |
| Fiverr human dubbers | slow & costly → you = **minutes, fraction of price** |

**Position:** *"The easiest, cheapest dubbing for [your niche] — especially South Asian languages."*

---

## 8. Costs to Run (your expenses)

| Item | Cost |
|---|---|
| ElevenLabs API (scales with usage) | variable (passed into pricing) |
| Hosting (Vercel + DB + storage) | ~$20–80/mo early |
| Payments (Stripe) | ~3% per transaction |
| Domain + email | ~$20/mo |
| **Startup total** | **under ~$150/mo to launch** |

Low overhead → profitable early with even 10–20 paying users.

---

## 9. Risks & Mitigation

| Risk | Mitigation |
|---|---|
| ElevenLabs price/policy change | abstract the provider; plan own pipeline (TECH_PLAN) |
| Copyright (users dub others' content) | Terms of Service: users confirm they have rights |
| Big player adds your feature | win on **niche + service + regional languages** |
| Margins thin at heavy use | minute caps + own-pipeline migration |

---

## 10. 90-Day Plan

- **Weeks 1–3:** build MVP (upload → dub 1 language → pay → download)
- **Weeks 4–6:** beta with 10 creators (free), collect testimonials + fix
- **Weeks 7–9:** launch Starter/Pro plans, start outreach sales
- **Weeks 10–12:** add lip-sync add-on + referral; push to 50 paying users

**First goal: 50 paying users (~$2k MRR).** Then scale outreach + add own-pipeline for margin.

---

> You handle sales. The product just needs to make dubbing **easy, cheap, and reliable** for ONE
> niche first. Win that niche, then expand languages and segments.
