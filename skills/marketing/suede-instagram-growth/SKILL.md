---
name: suede-instagram-growth
description: "Suede-owned Instagram growth operating system for account-specific audits, Reels, carousels, Stories, conversion mapping, calendars, and daily candidate-production loops. Use when the user names Instagram, IG, Reels, Stories, asks to analyze recent posts, grow a handle, run a daily workflow, create or repurpose Instagram content, or distinguish views from follows, leads, and sales. NOT FOR: multi-platform organic strategy (use suede-social), full video rendering or editing (use suede-video), paid Meta campaigns (use suede-ads or suede-ad-creative), analytics instrumentation (use suede-analytics), or any publish, comment, follow, like, or DM action without exact approval."
metadata:
  version: 1.0.0
---

# Suede Instagram Growth

Turn one Instagram account into an evidence-backed content and conversion
system. Every recommendation must resolve to the account's current content,
audience, offer, voice, production capacity, or a clearly labeled experiment.
Do not produce generic "post consistently" advice and do not pretend public
view counts reveal private saves, shares, retention, leads, or sales.

## Red Flags — Correct These First

- **"Lock this context forever."** Keep an account brief for the current
  workspace or run, attach source dates, and refresh mutable facts. Never claim
  permanent memory.
- **"Browse the last 30 posts automatically."** Use an authenticated Instagram
  surface, user export, authorized API, or user-supplied links. Instagram's
  terms prohibit automated collection without permission; never substitute
  unauthorized scraping.
- **"This went viral, so it converts."** Views are attention. Conversion needs
  follows, profile actions, DMs, leads, attributed checkout, or sales evidence.
- **"Use 15 hashtags and the best posting time."** Hashtag count, timing,
  format, and cadence are account-level tests. Verify current platform limits
  and the account's Insights before prescribing them.
- **"Run the daily workflow" means publish.** It means refresh evidence and
  prepare approval-ready candidates. Publishing is a separate authorized step.

## Operating Contract

### 1. Read existing context before asking

Read `.agents/product-marketing.md`, `.claude/product-marketing.md`, or the
legacy `product-marketing-context.md` when present. Also read any account brief,
content ledger, offer sheet, brand guide, approved voice samples, and recent
performance export supplied by the user.

Build or refresh this **Account Evidence Pack**:

```text
Handle and visible identity:
Account type: personal | creator | business | unknown
Objective: awareness | qualified followers | leads | sales | community
Primary audience:
Offer, price, and conversion path:
Voice samples and source dates:
Faceless preference and available media:
Current cadence and production capacity:
Timezone and follower-active windows:
Recent-post evidence source and coverage:
Attribution source: none | Insights | links/UTMs | CRM | checkout | mixed
Claims or topics requiring review:
Last refreshed:
Unknowns that affect confidence:
```

Start from accessible evidence. Ask one compact batch of questions only when a
missing answer would materially change the work. Never ask for information
already present in current files, the authenticated account, or supplied data.

### 2. Label every fact by evidence class

Use these labels in audits and recommendations:

- **Observed-public:** visible post, caption, date, format, views, likes, or
  comments.
- **Observed-owned:** authenticated Insights, export, DM log, link analytics,
  CRM, or checkout evidence the user is authorized to access.
- **Computed:** a formula calculated from observed values; show the formula and
  denominator.
- **Inferred:** a hypothesis to test. Never word it as an account fact.
- **Unknown:** the needed measure is unavailable. State what would resolve it.

### 3. Use the halt contract for real blockers

Use this exact format when authorized evidence, asset rights, identity, or
external-action approval blocks the requested result:

```text
HALT — <one-line blocker>
Why it blocks: <specific missing authority or evidence>
Resolve with:
1. <option>
2. <option>
3. <option, when useful>
Waiting for: <the exact item or approval>
```

Continue with safe drafts or worksheets only when they remain useful and do not
imply the blocker was resolved.

## First Action: Audit the Account

When the user supplies a handle or says to analyze the account:

1. **Verify identity and access.** Confirm the visible handle and whether the
   evidence is public-only or authenticated. Do not connect a third-party tool,
   request a password, or install an integration as a shortcut.
2. **Collect the recent cohort.** Default to the most recent 30 feed posts and
   Reels; use all available posts if fewer than 30 exist. Exclude pinned age,
   boosted distribution, collaborations, or giveaways only by tagging them,
   never silently.
3. **Collect comparable fields.** Use the schema in
   [references/account-audit.md](references/account-audit.md). Record `n` for
   every metric cohort; never compare a private metric against a public-only
   post as if both are complete.
4. **Code the content.** Assign one topic, pillar, hook family, format,
   structure, CTA, audience problem, offer proximity, and production burden to
   each post.
5. **Normalize within the account.** Compare like formats and similar
   distribution conditions. Use medians and quartiles when the cohort supports
   them; show raw counts when it does not.
6. **Map business value.** Classify each post as `converts`, `assists`,
   `attention-only`, or `unknown` using the rules below.
7. **Return the playbook.** Name repeatable patterns, dead weight, evidence
   gaps, and the next 3–5 controlled tests. Each recommendation must cite the
   post IDs or cohort behind it.

### Conversion classification

- **Converts:** has an attributable primary action: qualified follow, DM start,
  lead, checkout, or sale. Record the attribution source.
- **Assists:** produces measurable saves, shares, profile visits, site taps, or
  qualified comments without a reliably attributed primary action.
- **Attention-only:** sits in the cohort's top reach/view quartile while its
  primary-action rate is at or below the comparable-format median.
- **Unknown:** downstream measures are absent or attribution is not reliable.

Never promote `unknown` to `attention-only` or `converts` by intuition.

## Choose the Requested Mode

| User language | Execute |
|---|---|
| "analyze my account" | 30-post audit and conversion map |
| "make a calendar" | ranked 30- or 60-day test calendar |
| "create a Reel" | hook set, timed script, shot plan, caption, CTA, test card |
| "make a carousel" | selected narrative, exact slide copy, visual direction, caption |
| "repurpose this" | source atomization and a platform-native Instagram bundle |
| "analyze competitors" | lawful comparable-account pattern and whitespace audit |
| "run daily workflow" | evidence refresh and approval-ready candidate package |

If the request contains several modes, run them in dependency order: audit or
context refresh, strategy, asset creation, QA, approval package.

## Strategy and Planning

### Content pillars

Derive 3–5 starting pillars from the intersection of:

1. audience problem or desire;
2. account expertise or credible access;
3. observed response pattern;
4. offer or strategic objective;
5. repeatable production source.

For each pillar, return:

```text
Pillar:
Audience job:
Proof the account can own it:
Observed supporting posts:
Primary format hypothesis:
Business bridge:
Stop condition:
```

Do not force equal shares. Rank pillar allocation from recent evidence and the
next learning goal.

### Calendar

Build calendars as experiments, not filler. Every row must contain:

```text
Date/timezone | format | pillar | audience problem | hook | payoff | CTA
Evidence source | one variable being tested | primary metric | asset owner
Production status | approval status | readback field
```

Use the lowest cadence that can preserve evidence, voice, rights, and review
quality. If the user requests daily content, daily candidate generation is
allowed; do not claim daily publishing is optimal without account evidence.

### Competitor and trend research

Use public or authorized evidence only. Select 3–8 comparable accounts by
audience, offer, maturity, geography, and format; record why each qualifies.
Collect additional posts only while another bounded batch changes the leading
patterns. Public competitor research cannot see saves, shares, retention,
follows-per-post, DMs, or sales unless the account discloses them.

For trends, label each item `rising`, `active`, `saturated`, or `unverified`
only when the current source supports that label. Record source, observed date,
rights status, audience fit, and shelf life. A trend is optional; account fit
and source rights outrank novelty.

## Ideation and Selection

Generate 30–50 ideas only when requested or when the calendar horizon requires
that volume. Build them from the account's actual patterns:

- mistakes and avoidable losses;
- myths with proof-backed corrections;
- specific frameworks and checklists;
- unpopular opinions the account can defend;
- before/after demonstrations;
- audience objections and buying triggers;
- founder or operator evidence;
- product proof and customer outcomes;
- timely trends with a lawful, original treatment.

Score each idea from 0–20:

| Criterion | 0–4 rule |
|---|---|
| Audience recognition | 4 = target viewer identifies their problem in one read |
| Specific payoff | 4 = one concrete promised outcome, with no inflated claim |
| Evidence strength | 4 = owned proof or demonstrable source supports the idea |
| Voice fit | 4 = matches at least two supplied voice markers |
| Business bridge | 4 = natural next step connects to the stated objective |

Rank by total score, but show every component. Do not label an idea "viral."
Call it a test candidate and state why.

## Content Creation Contracts

Read [references/content-production.md](references/content-production.md) for
the full format templates.

### Reels

Return:

1. 20 hook candidates when the user asks for a hook factory; otherwise 5.
2. A selected hook with the selection score and evidence.
3. A second-by-second script: visual, voiceover, on-screen text, edit beat, and
   the retention job of each beat.
4. A faceless shot plan by default when requested: screen recording, product
   proof, licensed B-roll, kinetic type, hands/process, diagrams, or owned media.
5. A caption, one primary CTA, alt-text/accessibility notes, and a keyword plus
   hashtag test—not a fixed hashtag quota.
6. A rights and claim checklist.
7. One-variable test card and post-publication readback fields.

Choose duration from the idea and the account's comparable retention. If no
evidence exists, label 15–45 seconds as a starting test range, not an optimum.

### Carousels

Pick the narrative before writing: `problem-proof`, `mistake-fix`,
`framework`, `before-after`, `myth-evidence`, or `demo-walkthrough`. Set slide
count from the number of necessary beats; 8–10 is a starting range only when the
idea genuinely has that many beats.

Return exact text and visual direction for each slide. Slide 1 must identify
the audience tension or payoff. Every middle slide does one job. The last slide
summarizes the earned payoff and gives one next action.

### Captions and voiceover

- First line must stand alone before truncation.
- Use the account's sentence length, vocabulary, humor, punctuation, and taboo
  list from real voice samples.
- Use `pause`, `emphasis`, `beat`, and pronunciation markers for AI voiceover;
  never add synthetic emotion that contradicts the brand.
- Use only relevant hashtags whose current availability and meaning were
  checked. Do not manufacture "big/medium/niche" volume tiers without data.
- Run final copy through `suede-deslop` when it is available.

## Daily Workflow

Read [references/daily-loop.md](references/daily-loop.md), then execute:

1. Refresh account evidence, active offer, content queue, and yesterday's
   readback.
2. Review authorized trend and audience-signal sources.
3. Score candidate ideas and select 1–3 that cover distinct audience jobs.
4. Produce complete Reel, carousel, Story, or static packages.
5. Check claims, identity, asset rights, disclosures, accessibility, and CTA.
6. Return the exact approval packet; do not publish yet.
7. If exact content and visible identity are approved, publish only through a
   current authorized surface.
8. Read back the live permalink, rendered media, text, tags, CTA destination,
   and account identity. Log the post ID and measurement checkpoint.

Completion is proven by the package checklist for draft-only work, or by live
permalink readback for authorized publishing. A prepared composer is not a
published post.

## Measurement and Iteration

Read [references/measurement.md](references/measurement.md).

Use the campaign objective to select one primary metric and 2–4 diagnostics.
When denominators exist, calculate rates explicitly:

```text
save rate = saves / accounts reached
share rate = shares / accounts reached
comment rate = comments / accounts reached
follow rate = follows attributed to post / accounts reached
profile-action rate = profile actions / accounts reached
lead rate = attributed leads / accounts reached
sales rate = attributed sales / accounts reached
```

Do not combine these into a universal engagement score. Compare the current
post to its format-specific trailing median and the named experiment cohort.
Change one meaningful variable per test whenever practical.

## Suede-Owned Account Mode

When the target account belongs to Suede Labs AI, Jason Colapietro, or a named
Suede product:

- Anchor public positioning in creator ownership infrastructure,
  programmable IP, rights, provenance, registry-backed media, royalty routing,
  licensing readiness, and agent commerce. Do not reduce Suede to a generic AI
  music app.
- Build proof-led lanes from live product demonstrations, creator education,
  founder/operator evidence, rights workflows, provenance records, and agent
  commerce—not unsupported futurism.
- Never claim registration proves legal title, prevents copying, clears all
  rights, guarantees royalties, or completes a transaction unless current
  evidence proves that exact state.
- Use only `docs/assets/suede-ai-logo-transparent.png` as the Suede S mark
  (SHA-256 `83a7ee0317e4debe2e7b076c20ba067feb76a587f9e829dc6310ae4be4b44dfa`).
  Never redraw, trace, approximate, typeset, recolor, distort, or generate a
  replacement. If the file is missing or the checksum differs, omit the mark
  and use the halt contract.
- Confirm rights for every song, clip, voice, likeness, screenshot, testimonial,
  partner logo, and third-party post before including it.

## Boundaries

- Do not publish, schedule, comment, follow, like, repost, message, or modify an
  Instagram account without explicit approval of the exact content and visible
  identity.
- Do not scrape Instagram, bypass access controls, evade rate limits, or use a
  consumer password in an automation.
- Do not invent private Insights, audience sentiment, competitor conversion,
  trends, testimonials, results, scarcity, partnerships, rights, or product
  claims.
- Do not generate harassment, deceptive engagement bait, fake controversy,
  fake social proof, engagement pods, purchased followers, or undisclosed
  synthetic endorsements.
- Do not use copyrighted music, footage, likenesses, logos, or reposted creator
  content without a verified lawful basis and required attribution or
  disclosure.
- Do not treat drafts, scheduled items, composer previews, or API container IDs
  as published posts. Require live readback.

## Routing

- Use `suede-social` for cross-platform organic strategy and repurposing beyond
  Instagram.
- Use `suede-video` for rendering, editing, shot production, and multi-cut video
  pipelines after the Instagram content contract is approved.
- Use `suede-image` for production of image assets and `suede-design` for the
  visual system.
- Use `suede-copy` for broader conversion copy and `suede-deslop` for the final
  anti-slop pass.
- Use `suede-analytics` for UTMs, event instrumentation, attribution repair,
  and verified reporting pipelines.
- Use `suede-ads` and `suede-ad-creative` for paid Meta campaigns.
- From `suede-social`: route Instagram-specific account audits, Reels,
  carousels, Stories, and daily Instagram loops here.
