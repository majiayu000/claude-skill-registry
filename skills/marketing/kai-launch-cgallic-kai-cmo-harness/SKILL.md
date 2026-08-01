---
name: kai-launch
description: Plan and produce a complete product launch marketing package — landing page copy, email sequences, ad campaigns, press release, social posts, and launch timeline. Orchestrates all other kai skills into a coordinated launch. Use when "product launch", "launch campaign", "go-to-market", "GTM plan", "launch marketing", "we're launching", "prepare launch materials", or any request to coordinate marketing for a new product, feature, or major update.
---

# /kai-launch — One Launch, One Message, Every Channel

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

A dated launch a team can execute: a phased timeline, an asset set scoped to the channels the business actually has, and every asset carrying the same value proposition, the same proof points, and the same CTA destination. Plus a post-launch monitoring plan that says what to watch, when, and what to do when a number goes the wrong way.

The failure mode this skill exists to prevent is a launch where the ad, the email, and the page each describe a slightly different product.

## Done when

Work type `campaign` — floor **E5/C3/O4** (`harness/eco-floors.yaml`, contract `harness/skill-contracts/campaign.yaml`). Composite: the launch is CLOSED only when every child asset is CLOSED and the campaign-level threshold is met. One unshipped asset keeps the launch open.

- **E5** — each asset reaches its own execution target and someone other than its producer reads it back at the live target: page returns 200, ESP reports the send, the platform returns ad object ids reconciled to the approved bundle, the press release shows a live pickup URL.
- **C3** — every asset passes the gates its own work type declares (`four_us_score`, `banned_word_check`, `seo_lint` for search content, `mutation_risk_lint` for paid), and a named non-producer reads the launch pack end to end. Messaging consistency is part of that read: same value prop, same stats, same CTA across all assets.
- **O4** — pipeline generated, CAC, or campaign ROI clears a threshold declared before launch day, read at the 45-day window. Attribution is required; platform-reported numbers alone do not carry it.

Each child asset carries its own floor. A paid ad in this launch is still `paid-ad-campaign` (E5/C4/O4) and needs its own policy check and approval.

## Constraints

- **The timeline and asset checklist are approved before anything is produced.** Present both, confirm scope, then write. Remove assets for channels the business does not have rather than producing them speculatively.
- **Landing page copy comes first, and it defines the messaging everyone else inherits.** Extract the core value proposition, the key stats and proof points, the CTA destination, and the persona hooks into `workspace/launch/_messaging-guide.md`, then write every other asset against it. The press release crystallizes the announcement narrative; blogs expand it; emails, ads, social, and the LinkedIn article carry it.
- **Per-asset production is bound by the harness pipeline, not by this skill's convenience:** load the governing framework from `knowledge/`, load the skill contract from `harness/skill-contracts/`, load the platform policy reference from `harness/references/` *before* writing any ad copy, write against framework plus persona, run the gates. Max 2 retries per asset, each naming the specific failing dimension. After 2 failures, escalate to a human and log the diagnosis in `memory/lessons.md`.
- **Ad copy never gets written before its platform policy reference is loaded.** The per-platform table is in `.claude/rules/architecture-and-memory.md`.
- Quantitative claims in launch assets — customer counts, performance numbers, funding, market size — follow the Kai Data Provenance Rule (`harness/references/audit-data-provenance.md`). Missing data is a data gap, never a rounded guess.
- Nothing publishes, sends, or spends without human approval. Producing ad copy is not authorization to activate a campaign; drafting a sequence is not authorization to send it.
- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — README, manifests, landing pages, route files, analytics and email config — and confirm the draft. Do not open with discovery questions the repo can answer.

**Know these before producing anything** (from `MARKETING.md` first; ask only for what it cannot answer): what is launching (new product, feature, major update, rebrand) · the go-live date · which channels exist and at what size (list size, ad budget, social following, press contacts) · the launch offer or hook (launch pricing, early access, beta invite) · whether a landing page exists or must be built.

## Context

| Need | Load |
|---|---|
| Multi-channel campaign sequencing | `knowledge/playbooks/campaign-orchestration.md` |
| Format contract and per-asset gate thresholds | `harness/skill-contracts/campaign.yaml` + the per-asset contract in `harness/skill-contracts/` |
| Platform ad policy before writing ads | `.claude/rules/architecture-and-memory.md` (per-platform table) → `harness/references/` |
| Provenance for any number in a launch asset | `harness/references/audit-data-provenance.md` |
| Persona hooks and language | `knowledge/personas/_persona-index.md` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |
| Landing page copy | `/kai-landing-page` |
| Email set | `/kai-email-system` |
| Ad set | `/kai-ad-campaign` |

**Launch phases** — the timing map that anchors every asset's due date:

| Phase | Timing | Activities |
|-------|--------|------------|
| Pre-launch | T-14 to T-7 | Teaser emails, waitlist, social hints, internal prep |
| Warm-up | T-7 to T-1 | Blog posts, detailed previews, influencer/press outreach |
| Launch Day | T-0 | Announcement email, ads live, press release, social blitz |
| Post-launch | T+1 to T+14 | Nurture sequence, retargeting ads, case study collection, performance review |
| Sustain | T+14 to T+30 | Content marketing, SEO articles, ongoing ad optimization |

**Default asset set** — adapt to the channels the business actually has:

| Asset | Channel | Phase |
|-------|---------|-------|
| Landing page copy | Web | Pre-launch |
| Teaser email (1-2) | Email | Pre-launch |
| Announcement email | Email | Launch day |
| Follow-up sequence (3-5) | Email | Post-launch |
| Meta ads — TOF (3 variants) | Meta | Launch day |
| Meta ads — retarget (3 variants) | Meta | Post-launch |
| Google ads — brand RSA | Google | Launch day |
| Google ads — non-brand RSA | Google | Launch day |
| Blog post — announcement | Blog | Warm-up |
| Blog post — long-form | Blog | Post-launch |
| LinkedIn article | LinkedIn | Launch day |
| Press release | PR | Launch day |
| Social posts (5-10) | Social | All phases |

**Output tree** — `workspace/launch/`:

```
workspace/launch/
├── _timeline.md
├── _messaging-guide.md          # Core VP, stats, CTA, extracted from landing page
├── _monitoring.md               # Day 1/3/7/14 checks, metrics per channel, adjust triggers
├── _quality-report.md           # Per-asset gate results + launch readiness checklist
├── landing-page/copy.md
├── emails/                      # teaser-1, teaser-2, announcement, follow-up-1, follow-up-2
├── ads/meta/  ads/google/
├── blog/                        # announcement, long-form
├── pr/press-release.md
├── social/                      # launch-day-posts, sustain-posts
└── linkedin/article.md
```

**Monitoring plan** covers the day 1 / 3 / 7 / 14 check-in schedule, the metrics to watch per channel (email open and click rates, ad CTR and CPA, landing page conversion), the thresholds that trigger a change (kill underperforming ads, shift budget to winners), and the follow-on content early results justify (FAQ post, case study, feature tutorial).

## Escalate when

- The launch date does not leave room for the pre-launch phase, and compressing it means shipping assets past their gates.
- A channel in the asset list has no account, no audience, or no budget behind it.
- Ad spend, press distribution fees, or any launch-day cost is unauthorized.
- Launch claims (customer counts, performance, funding) cannot be sourced.
- The product is in a regulated category where the announcement narrative carries compliance risk.
- The launch offer's terms (pricing, guarantee, early-access cap) are unconfirmed by the business.
