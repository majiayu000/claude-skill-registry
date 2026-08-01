---
name: kai-ad-campaign
description: Plan, evaluate, and produce paid ad campaigns across platforms (Meta, Google, LinkedIn, TikTok, Microsoft, Pinterest, Snapchat, Amazon, X). Evaluate existing ads, map funnel stages (TOF/MOF/BOF), produce ad variants per platform with policy compliance, output ready-to-upload copy. Use when "ad campaign", "create ads", "run ads for", "paid campaign", "media plan", "launch ads", "Meta campaign", "Google Ads campaign", "multi-platform ads", "evaluate my ads", "how are my ads doing", "audit my ads", "ad performance", "analyze ads", or any request to evaluate existing or create new advertising.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

# /kai-ad-campaign — Ads That Clear Policy And Earn Their Spend

## Objective

Either a verdict on the ads already running, or a ready-to-upload campaign across the platforms that fit the product — funnel stages mapped, variants written to each platform's character specs, every ad checked against that platform's policy reference before it was written, and an execution plan that never activates spend in the same action that creates it.

Two modes, and the mode changes what is permitted:

| Mode | Triggered by | Permission |
|---|---|---|
| Evaluation | "evaluate", "analyze", "audit", "how are my ads doing", "ad performance", "review my ads" | **Read-only.** No creating, pausing, activating, bid changes, budget changes, asset uploads, keyword additions, or targeting mutations while evaluating. |
| Creation | "create", "launch", "build", "new campaign", "run ads" | Produce copy and structure; live writes stay approval-gated. |
| Both | Evaluation findings become the input to creation | Read-only until the evaluation is delivered. |

Evaluation mode does not require `MARKETING.md`. Creation mode does.

## Done when

Work type `paid-ad-campaign` — floor **E5/C4/O4** (`harness/eco-floors.yaml`), `spend_authority: true`.

- **E5** — the platform returned ad object ids **and** a read-back of the live entity confirms targeting, budget, schedule, and creative match the approved bundle field-for-field. A successful API call is not E5. **Hard stop: live-account mutation without recorded human approval is never SHIPPED, whatever else the evidence shows.**
- **C4** — the platform policy reference was loaded and the ad checked against it *before* submission; plus `four_us_score` ≥ 10/16, `banned_word_check` clean, and `mutation_risk_lint` clean. C4 is the field standard, not a lint pass.
- **O4** — CAC, ROAS, CPL, or qualified lead rate read from the ads connector no earlier than the conversion window plus learning phase, against a threshold declared before launch. Platform-reported ROAS is not O5; O5 needs a holdout, geo-split, or incrementality design.

Evaluation-only runs are graded as `audit-report` instead — E3/C4/O1, with every number resolving to a pulled source and each P0 recommendation naming the metric it targets.

## Constraints

### Always

- **Read `MARKETING.md` from the project root before creation work.** If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Five things must be known before writing creation-mode ads:** which platforms, budget range, the goal (leads, conversions, traffic, awareness, installs), the landing page traffic goes to, and what creative assets already exist.
- **Load the platform's policy reference and skill contract before writing a single line of that platform's copy.** The table under Context is the lookup. `harness/references/advertising-compliance.md` (FTC, GDPR, CAN-SPAM) applies to every platform on top of the platform's own rules.
- **Credentials come out of `.env.local` by `grep`, never `source`.** Extracting a variable is not the same as executing the file.
- **Approval gate before production.** Present the campaign map — platform selection, funnel stages, variants per stage, and any regulated-industry compliance concern — and get confirmation before producing ads.
- **No numbers without a pull.** Spend, CTR, CPC, CPL, and retention figures come from the platform API or the analytics source, cited with the date range. Model memory is not a data source.

### Per ad, before it ships

1. Four U's ≥ **10/16**.
2. Zero banned words, zero AI slop.
3. Platform character limits respected — headlines, descriptions, primary text.
4. A specific number or stat anchors the claim.
5. No policy violation against the loaded reference.
6. No superlatives without proof.
7. One clear CTA.

### Creative diversity

Across the three variants per funnel stage, rotate the hook type — variant A pain/agitate, variant B social proof or stat-led, variant C pattern interrupt or story — **and** rotate the concrete creative format. Three ads sharing a production format with different opening lines are not three creatives.

Every variant declares both a `hook_type` (`pattern_interrupt | social_proof | pain_agitate | direct_offer | story`) and a concrete `creative_format`. Example pairings: `problem_agitation` + `founder`, `social_proof` + `testimonial_mashup`, `pattern_interrupt` + `ugly_ad`.

Formats are selected by `select_creative_formats(...)` in `kai/paid_media/creative_formats.py`, keyed on platform, funnel stage, available assets, and regulated-industry risk. Each selected format carries its check results — platform fit, funnel fit, asset feasibility, compliance status, missing assets, compliance flags. When the selector returns `NEEDS_ASSET` or `REVIEW`, the format stays in the plan only if the missing asset or the review step is stated explicitly.

### API execution (Meta)

- Load `harness/references/ad-write-guardrails.md` before any write path. Default to read-only reports, dry-run previews, upload validation, and recommendations. Live write access is approval-gated and never auto-approved.
- **Verify video ids against the live library before creating a video ad.** A single digit difference is a different or nonexistent video. Never trust an id from logs or docs.
- Verify the Instagram account id; pull from Page settings when it is not in `.env.local`. Use `instagram_user_id`, **not** `instagram_actor_id`.
- Create everything `PAUSED` first. **Activation is a separate high-risk action — never activate in the same action that creates entities or uploads assets.**
- The write guardrail packet carries: account allowlist, target campaign/ad set ids, dry-run payload, before/after diff, evidence source, platform policy result, rollback reference, and the human approval note.
- Bid and budget writes are blocked unless capped: current value, proposed value, percent change, daily cap, per-change cap, and rollback path all stated. Never auto-approve a bid or budget change.
- Strip organic-only captions, hashtags, and comment-keyword CTAs from paid copy.
- Entity order: campaign (paused) → ad set(s) with targeting and budget → ads with inline creative (`object_story_spec`) → review in Ads Manager → activate as its own approved action.

### Launch decision gate

Load `knowledge/playbooks/meta-creative-testing-decision-framework.md` when any of these hold: 10 or more ads/creatives will be created; ad set daily budget sits below recent or target CPA; existing winners are already producing leads, purchases, or qualified calls; or the user is asking whether to push all, push a subset, pause all, or find the best launch structure. Write the decision memo *before* execution. Defaults for large batches: create all requested ads `PAUSED` when staging helps, activate only the recommended subset when budget is tight, keep proven winner ad sets separate from exploratory batches, and protect existing winners unless the user explicitly wants a refresh test. Separate "create paused for review" from "activate for spend" in every recommendation.

### New-brand or first-paid-test launches

Load `knowledge/playbooks/paid-media-launch-playbook.md` and apply its defaults before writing ads: minimum test budget of **target CPA × 50**; build the measurement checklist before campaign copy; Meta starts with one campaign per product plus simple retargeting; Google starts with branded search, non-branded search per product or problem, and shopping only once feed quality is ready; avoid Performance Max until the account has baseline data. Produce `workspace/ads/_launch-brief.md` and `workspace/ads/_measurement-checklist.md`.

## Context

| Need | Load |
|---|---|
| Meta policy · API execution · contract | `harness/references/meta-ads-rules.md` · `harness/references/meta-ads-api-reference.md` · `harness/skill-contracts/meta-ads.yaml` |
| Google policy · contract | `harness/references/google-ads-policy-reference.md` · `harness/skill-contracts/google-ads.yaml` |
| LinkedIn policy | `harness/references/linkedin-ads-rules.md` |
| TikTok policy | `harness/references/tiktok-ads-policy-reference.md` |
| Microsoft policy | `harness/references/microsoft-ads-rules.md` |
| Pinterest policy | `harness/references/pinterest-ads-rules.md` |
| Snapchat policy | `harness/references/snapchat-ads-policy-reference.md` |
| Amazon policy | `harness/references/amazon-ads-policy-reference.md` |
| X/Twitter policy | `harness/references/x-ads-policy-reference.md` |
| Law that applies to every platform | `harness/references/advertising-compliance.md` |
| Any workflow that uploads, creates, activates, pauses, or changes bids/budgets | `harness/references/ad-write-guardrails.md` |
| First paid test or new brand | `knowledge/playbooks/paid-media-launch-playbook.md` |
| Batch creative testing, budget-vs-CPA calls | `knowledge/playbooks/meta-creative-testing-decision-framework.md` |
| Format selection by platform, stage, assets, risk | `kai/paid_media/creative_formats.py` (`select_creative_formats`) |
| On-site behavior behind ad traffic | `harness/references/posthog-marketing-queries.md` (UTM pageviews #2, ad visitor journeys #5, campaign attribution #8) |

**Platform constraints worth carrying inline** — the policy reference still loads before writing:

| Platform | Key constraints |
|---|---|
| Meta | Headline 27 chars, primary text 125 chars visible. Special Ad Categories, no before/after imagery, personal-attributes ban |
| Google | 15 headlines at 30 chars, 4 descriptions at 90 chars. No superlatives without proof |
| LinkedIn | Professional context required, B2B claim substantiation |
| TikTok | No political ads, weight-management restrictions, AI-content disclosure required |
| Microsoft | Mirrors Google's RSA format; country-level gambling bans, clinical trials ban |
| Pinterest | All weight-loss ads banned, strict body-image rules |
| Snapchat | Young-audience protections, EU political ad ban |
| Amazon | 18-month claim evidence rule, no competitor disparagement |
| X/Twitter | Verification tier affects ad access; political ad certification by country |

**Funnel structure** — adapt to the product; not every product needs every stage. Three variants per stage per platform is the default:

| Stage | Objective | Audience | Typical platforms |
|---|---|---|---|
| TOF (awareness) | Reach | Cold — lookalikes, interest-based | Meta, TikTok, Google Display |
| MOF (consideration) | Traffic, engagement | Warm — site visitors, engagers | Meta, Google Search, LinkedIn |
| BOF (conversion) | Leads, sales | Hot — cart abandoners, demo requesters | Meta retargeting, Google Search (brand), email |

**Evaluation scoring benchmarks** — adjust to the vertical (B2B SaaS, local service, ecommerce):

| Metric | Poor | OK | Good | Great |
|---|---|---|---|---|
| CTR | < 0.5% | 0.5–1% | 1–2% | > 2% |
| CPC | > $5 | $3–5 | $1.50–3 | < $1.50 |
| CPL | > $50 | $30–50 | $15–30 | < $15 |
| Video 25% retained | < 30% | 30–50% | 50–70% | > 70% |
| Video 75% retained | < 5% | 5–10% | 10–20% | > 20% |
| Landing page bounce | > 80% | 60–80% | 40–60% | < 40% |

Every evaluated ad gets one of four verdicts: **keep**, **optimize** (with the specific fix — copy, creative, or targeting), **pause**, or **create new** (a gap: missing funnel stage, untested hook, unserved segment). The evaluation report carries account-level totals (active campaigns, active ads, 30-day spend, average CTR/CPC/CPL), campaign-level and ad-level performance, and those verdicts.

**Output** goes to `workspace/ads/`:

- `_evaluation-report.md` — evaluation mode only.
- `_campaign-map.md` — funnel structure, platform mix, variant counts. Presented for approval before production.
- One folder per platform holding the variant files: `meta/tof-variant-a.md`, `google/search-rsa-branded.md`, `linkedin/…`.
- `_quality-report.md` — per-ad Four U's score, character-limit result, policy result, and status; the policy flags needing legal review or carrying borderline claims; and which variants to test first based on hook diversity.
- `_platform-setup.md` — campaign structure per platform, audience targeting, budget allocation across platforms and stages, bid strategy, and UTM conventions.
- `_launch-brief.md`, `_measurement-checklist.md`, and `_meta-creative-testing-decision.md` when their trigger conditions fire.

## Escalate when

- Any live write is requested — creating, activating, pausing, uploading, or changing a bid or budget. These go to human approval every time.
- Budget cannot fairly test the requested batch; propose a staged subset rather than splitting spend across everything.
- The product sits in a regulated category (health, finance, housing, employment, credit) where the loaded policy reference flags the intended claim or targeting.
- Platform data cannot be pulled and the user wants performance conclusions anyway.
- Existing winners would be disturbed by the proposed test and the user has not asked for a refresh.
- A claim in the copy has no substantiation and the platform requires proof.
