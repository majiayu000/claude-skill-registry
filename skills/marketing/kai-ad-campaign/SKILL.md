---
name: kai-ad-campaign
description: Plan, evaluate, and produce paid ad campaigns across platforms (Meta, Google, LinkedIn, TikTok, Microsoft, Pinterest, Snapchat, Amazon, X). Evaluate existing ads, map funnel stages (TOF/MOF/BOF), produce ad variants per platform with policy compliance, output ready-to-upload copy. Use when "ad campaign", "create ads", "run ads for", "paid campaign", "media plan", "launch ads", "Meta campaign", "Google Ads campaign", "multi-platform ads", "evaluate my ads", "how are my ads doing", "audit my ads", "ad performance", "analyze ads", or any request to evaluate existing or create new advertising.
---

Plan, evaluate, and batch-produce ad campaigns across platforms and funnel stages. Every ad passes platform policy compliance + quality gates.

## Mode Detection

Before loading product context, determine the mode:

- **Evaluation mode** — user says "evaluate", "analyze", "audit", "how are my ads doing", "ad performance", "review my ads"
- **Creation mode** — user says "create", "launch", "build", "new campaign", "run ads"
- **Evaluate + Create** — user wants both (evaluation first, then create/fix based on findings)

Evaluation mode does NOT require `MARKETING.md`. Creation mode does.

---

## Phase E: Ad Evaluation (Evaluation Mode Only)

Skip this phase entirely if the user only wants to create new ads.

Evaluation mode is read-only. Do not create, pause, activate, change bids, change budgets, upload assets, add keywords, or mutate targeting while evaluating performance.

### E.1 Pull Active Campaigns

Load the Meta API reference: `harness/references/meta-ads-api-reference.md`

1. Extract credentials from `.env.local` using grep (never `source`):
   ```bash
   META_TOKEN=$(grep '^META_ACCESS_TOKEN=' .env.local | cut -d= -f2-)
   AD_ACCOUNT_ID=$(grep '^META_AD_ACCOUNT_ID=' .env.local | cut -d= -f2-)
   ```

2. List all active campaigns with insights:
   ```bash
   curl "https://graph.facebook.com/v21.0/act_${AD_ACCOUNT_ID}/campaigns?fields=id,name,objective,status,daily_budget,insights.date_preset(last_30d){impressions,clicks,spend,ctr,cpc,actions,cost_per_action_type}&filtering=[{\"field\":\"effective_status\",\"operator\":\"IN\",\"value\":[\"ACTIVE\"]}]&limit=50&access_token=${META_TOKEN}"
   ```

3. For each campaign, pull ad-level insights:
   ```bash
   curl "https://graph.facebook.com/v21.0/act_${AD_ACCOUNT_ID}/ads?fields=id,name,status,effective_status,campaign_id,creative{id,object_story_spec},insights.date_preset(last_30d){impressions,clicks,spend,ctr,cpc,actions,cost_per_action_type,video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p100_watched_actions}&filtering=[{\"field\":\"effective_status\",\"operator\":\"IN\",\"value\":[\"ACTIVE\"]}]&limit=100&access_token=${META_TOKEN}"
   ```

### E.2 Cross-Reference with PostHog

Load: `harness/references/posthog-marketing-queries.md`

Pull landing page data to cross-reference ad traffic with on-site behavior:
- Pageviews with UTM breakdown (query #2)
- Ad visitor journeys (query #5)
- Campaign attribution / conversions (query #8)

### E.3 Score Each Ad

| Metric | Poor | OK | Good | Great |
|--------|------|----|------|-------|
| CTR | < 0.5% | 0.5–1% | 1–2% | > 2% |
| CPC | > $5 | $3–5 | $1.50–3 | < $1.50 |
| CPL | > $50 | $30–50 | $15–30 | < $15 |
| Video 25% retained | < 30% | 30–50% | 50–70% | > 70% |
| Video 75% retained | < 5% | 5–10% | 10–20% | > 20% |
| Landing page bounce | > 80% | 60–80% | 40–60% | < 40% |

Adjust benchmarks to the vertical (B2B SaaS, local service, ecommerce, etc.).

### E.4 Generate Evaluation Report

Output to `workspace/ads/_evaluation-report.md`:

```markdown
# Ad Evaluation Report — [Date]

## Summary
- Active campaigns: [N]
- Active ads: [N]
- Total 30-day spend: $[X]
- Avg CTR: [X]% | Avg CPC: $[X] | Avg CPL: $[X]

## Campaign Performance

| Campaign | Objective | Spend | Impressions | Clicks | CTR | CPC | Leads | CPL |
|----------|-----------|-------|-------------|--------|-----|-----|-------|-----|

## Ad-Level Performance

| Ad | Campaign | CTR | CPC | Spend | Leads | CPL | Verdict |
|----|----------|-----|-----|-------|-------|-----|---------|

## Recommendations

### Keep (performing well)
[List ads to keep running]

### Optimize (underperforming but fixable)
[List ads with specific fix recommendations — copy, creative, targeting]

### Pause (not working)
[List ads to turn off]

### Create New
[Gaps identified — missing funnel stages, untested hooks, audience segments]
```

### E.5 Transition to Creation

If evaluation reveals gaps or the user wants new ads, transition to Phase 0 → Phase 1 below with the evaluation findings as context.

---

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Campaign Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Platforms** — which platforms? (Meta, Google, LinkedIn, TikTok, etc.)
2. **Budget range** — affects platform mix and bid strategy recommendations
3. **Goal** — leads, conversions, traffic, awareness, app installs?
4. **Landing page** — where do ads send traffic?
5. **Existing assets** — any images/video already available?

### New Launch Add-On

If the campaign is for a new brand, new product, first paid test, or "launch ads" request, load:

- `knowledge/playbooks/paid-media-launch-playbook.md`

Apply these launch defaults before writing ads:

- Use `Target CPA x 50` as the minimum test budget.
- Build the measurement checklist before campaign copy.
- Start Meta with one campaign per product plus simple retargeting.
- Start Google with branded search, non-branded search per product/problem, and shopping only when feed quality is ready.
- Avoid Performance Max until the account has baseline data.
- Produce `workspace/ads/_launch-brief.md` and `workspace/ads/_measurement-checklist.md`.

### Meta Creative Testing Add-On

If the platform is Meta and the request includes 10+ creatives, API creation, video batches, existing winners, low budgets, or a "best solution" question, load:

- `knowledge/playbooks/meta-creative-testing-decision-framework.md`

Before recommending activation or creating live ads:

- Separate "create paused for review" from "activate for spend."
- Compare daily budget against target CPA and recent CPA.
- Protect existing winning ad sets unless the user explicitly wants a refresh test.
- Recommend a staged active subset when budget cannot fairly test the full batch.
- Produce `workspace/ads/_meta-creative-testing-decision.md` when writing workspace artifacts.

## Phase 2: Campaign Architecture

Generate `workspace/ads/_campaign-map.md` with:

### Funnel Structure

| Stage | Objective | Audience | Platforms | Ad Count |
|-------|-----------|----------|-----------|----------|
| **TOF (Awareness)** | Reach/awareness | Cold — lookalikes, interest-based | Meta, TikTok, Google Display | 3 variants each |
| **MOF (Consideration)** | Traffic/engagement | Warm — site visitors, engagers | Meta, Google Search, LinkedIn | 3 variants each |
| **BOF (Conversion)** | Leads/sales | Hot — cart abandoners, demo requesters | Meta retarget, Google Search (brand), Email | 3 variants each |

Adapt to the actual product and platforms. Not every product needs every stage.

### Per-Platform Ad Specs

Before writing any ad, load the platform's policy reference and skill contract. For Meta, also load the API reference for execution:

| Platform | Policy Reference | API/Execution Reference | Contract | Key Constraints |
|----------|-----------------|------------------------|----------|-----------------|
| Meta | `harness/references/meta-ads-rules.md` | `harness/references/meta-ads-api-reference.md` | `harness/skill-contracts/meta-ads.yaml` | Headline 27 chars, primary text 125 chars visible |
| Google | `harness/references/google-ads-policy-reference.md` | — | `harness/skill-contracts/google-ads.yaml` | 15 headlines (30 chars), 4 descriptions (90 chars) |
| LinkedIn | `harness/references/linkedin-ads-rules.md` | — | — | Professional context, B2B claim substantiation |
| TikTok | `harness/references/tiktok-ads-policy-reference.md` | — | — | No political ads, AI disclosure required |
| Microsoft | `harness/references/microsoft-ads-rules.md` | — | — | Similar to Google RSA format |
| Pinterest | `harness/references/pinterest-ads-rules.md` | — | — | All weight loss banned, strict body image |
| Snapchat | `harness/references/snapchat-ads-policy-reference.md` | — | — | Young audience protections |
| Amazon | `harness/references/amazon-ads-policy-reference.md` | — | — | 18-month claim evidence rule |
| X/Twitter | `harness/references/x-ads-policy-reference.md` | — | — | Verification tier affects access |

All paths relative to `E:\Dev2\kai-cmo-harness-work\`.

Also load: `harness/references/advertising-compliance.md` for FTC/GDPR/CAN-SPAM requirements that apply to ALL platforms.

Also load: `harness/references/ad-write-guardrails.md` for any workflow that may upload assets, create ads, create campaigns/ad sets/ad groups, activate/pause entities, or change bids/budgets.

### Approval Gate

Present the campaign map to the user before producing ads. Confirm:
- Platform selection
- Funnel stages
- Number of variants per stage
- Any compliance concerns (regulated industry?)

## Phase 3: Batch Production

Produce ads by platform and funnel stage. For each ad:

### Output Format

```markdown
# [Platform] — [Funnel Stage] — Variant [A/B/C]

**Platform:** Meta / Google / LinkedIn / etc.
**Funnel stage:** TOF / MOF / BOF
**Objective:** [campaign objective]
**Audience:** [target description]

## Ad Copy

### Headlines
[Per platform specs — e.g., 15 headlines for Google RSA, 1 for Meta]

### Primary Text / Description
[Per platform specs]

### CTA
[Button text or action]

### Display URL / Path
[If applicable]

## Hook Type
[pattern_interrupt | social_proof | pain_agitate | direct_offer | story]

## Quality Gate Results
- Four U's: [X]/16 (min 10)
- Banned words: PASS/FAIL
- Platform char limits: PASS/FAIL
- Has number/stat: PASS/FAIL
- Policy compliance: PASS/FAIL
```

### Quality Gates (per ad)

1. **Four U's >= 10/16**
2. **Zero banned words** and **zero AI slop**
3. **Platform character limits** respected (headlines, descriptions, primary text)
4. **Has specific number or stat** anchoring the claim
5. **Platform policy compliance** — no violations from the loaded policy reference
6. **No superlatives without proof** (Google requirement, good practice everywhere)
7. **Single clear CTA** per ad

### Hook Variety

Across the 3 variants per stage, use different hook types:
- Variant A: Pain/agitate
- Variant B: Social proof or stat-led
- Variant C: Pattern interrupt or story

### Batch Output

```
workspace/ads/
├── _campaign-map.md
├── meta/
│   ├── tof-variant-a.md
│   ├── tof-variant-b.md
│   ├── tof-variant-c.md
│   ├── mof-variant-a.md
│   └── bof-variant-a.md
├── google/
│   ├── search-rsa-branded.md
│   ├── search-rsa-nonbranded.md
│   └── pmax-assets.md
├── linkedin/
│   └── ...
└── _quality-report.md
```

## Phase 4: Quality Report

Generate `workspace/ads/_quality-report.md`:

```markdown
# Ad Campaign Quality Report

## Summary
- Total ads: [N]
- Platforms: [list]
- Passed all gates: [N]
- Policy flags: [N]

## Per-Ad Results
| Ad | Platform | Stage | Four U's | Char Limits | Policy | Status |
|----|----------|-------|----------|-------------|--------|--------|

## Policy Flags
[Any ads that need legal review or have borderline claims]

## A/B Test Recommendations
[Which variants to test first based on hook type diversity]
```

## Phase 5: API Execution (Optional — Meta)

If the user wants to create ads via API (not just produce copy), load `harness/references/meta-ads-api-reference.md` and follow this sequence:

Load `harness/references/ad-write-guardrails.md` before API execution. Default to read-only reports, dry-run previews, upload validation, and recommendations. Live write access is approval-gated and never auto-approved.

### Launch Decision Gate

Before creating or activating Meta ads by API, load `knowledge/playbooks/meta-creative-testing-decision-framework.md` when any of these are true:

- 10 or more ads/creatives will be created.
- The ad set daily budget is below the recent or target CPA.
- Existing winners are already producing leads, purchases, or qualified calls.
- The user asks whether to push all, push a subset, pause all, or find the best launch structure.

For those cases, write or present a decision memo before execution. Default behavior for large batches is:

- Create all requested ads as `PAUSED` when staging is useful.
- Activate only the recommended subset when budget is tight.
- Keep proven winner ad sets separate from exploratory batches.
- Strip organic-only captions, hashtags, and comment-keyword CTAs from paid copy.

### Pre-Flight Checks

1. **Verify credentials:** Extract all required env vars via `grep` from `.env.local`
2. **Verify video IDs:** Before creating any video ad, query the video library first:
   ```bash
   curl "https://graph.facebook.com/v21.0/act_${AD_ACCOUNT_ID}/advideos?fields=id,title,created_time&limit=20&access_token=${META_TOKEN}"
   ```
   Never trust video IDs from logs or docs without verification — a single digit difference means a different (or nonexistent) video.
3. **Verify Instagram account ID:** Pull from Page settings if not in `.env.local`
4. **Set all ads to PAUSED initially** — review before activating
5. **Build the write guardrail packet:** include account allowlist, target campaign/ad set IDs, dry-run payload, before/after diff, evidence source, platform policy result, rollback reference, and human approval note.
6. **Block bid/budget writes unless capped:** include current value, proposed value, percent change, daily cap, per-change cap, and rollback path. Never auto-approve bid or budget changes.

### Execution Order

```
1. Create campaign (PAUSED)
2. Create ad set(s) with targeting + budget
3. For each ad:
   a. If video ad → verify video_id exists in library
   b. Create ad with inline creative (object_story_spec)
   c. Use instagram_user_id (NOT instagram_actor_id)
4. Review all created ads in Ads Manager
5. Activate
```

Activation is a separate high-risk action. Do not activate in the same action that creates or uploads assets.

### Cross-Reference with PostHog

After ads are live, use `harness/references/posthog-marketing-queries.md` to track:
- Landing page traffic from UTM parameters (query #2)
- Visitor journeys from ad click to conversion (query #5)
- Campaign attribution and conversion rates (query #8)

---

## Phase 6: Platform Setup Notes

Generate `workspace/ads/_platform-setup.md` with:
- Campaign structure per platform (campaigns, ad sets, ad groups)
- Audience targeting recommendations
- Budget allocation across platforms and stages
- Bid strategy recommendations
- Tracking/UTM parameter conventions
