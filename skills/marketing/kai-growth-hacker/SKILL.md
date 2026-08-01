---
name: kai-growth-hacker
description: 'Build an exhaustive first-growth-hire distribution operating system across B2B and B2C channels: LinkedIn, events, AI outbound, AEO, blogs, long-form writing, YouTube, webinars, X, influencers, AI UGC, organic TikTok, paid social, sponsorships, partnerships, lifecycle, referral, and community. Use when "growth hacker", "first growth hire", "distribution hire", "cover every channel", "channel hacking", "0 to ARR growth system", "growth operator", "growth hacker OS", or any request to fan out channel operators and plug the result into Kai workflows.'
---

# Kai Growth Hacker - First-Hire Distribution OS

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

Build a complete growth-hacker operating package. The package maps every plausible channel, scores stage fit, fans out specialist operators, creates test briefs, defines approval gates, and routes execution into the right Kai skills.

This skill does not send, publish, scrape, enrich, spend, upload, call, text, or mutate live systems. It creates the local plan, ledgers, briefs, and approval queues needed before live work.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the project root.

If it exists, read it before asking questions. If it does not exist, run `/kai-start` or infer a temporary brief from trusted project files and mark unknowns as `[TODO]`.

Load these files before production:

- `knowledge/playbooks/growth-hacker-first-hire-os.md`
- `knowledge/playbooks/growth-loops-applied.md`
- `knowledge/playbooks/demand-generation.md`
- `knowledge/playbooks/social-media-strategy.md`
- `knowledge/playbooks/influencer-marketing.md`
- `knowledge/playbooks/event-webinar-marketing.md`
- `knowledge/playbooks/paid-media-launch-playbook.md`
- `knowledge/playbooks/content-repurposing.md`
- `knowledge/playbooks/analytics-attribution.md`
- `knowledge/frameworks/aeo-ai-search/aeo-ai-search-playbook-2026.md` when AEO is in scope
- `harness/references/social-automation-rules.md` when organic social execution is in scope
- `harness/references/advertising-compliance.md` when paid, sponsorship, affiliate, or creator work is in scope
- platform-specific policy references before writing ads or platform-bound posts

## Phase 1: Discovery

Read from `MARKETING.md`. Ask only for missing facts:

1. **Business type**: B2B, B2C, marketplace, local service, ecommerce, creator, or mixed.
2. **Stage**: pre-launch, first revenue, early growth, growth, or scale.
3. **Primary conversion**: waitlist, trial, demo, call, purchase, subscription, event registration, or partner lead.
4. **Current channels**: what is active, what has failed, what has proof.
5. **Assets available**: product demo, founder voice, customer proof, reviews, UGC, podcast/video, blog, email list, CRM, ad account.
6. **Budget and time**: monthly spend, founder/operator hours, production capacity.
7. **Regulated or sensitive categories**: healthcare, finance, legal, minors, employment, housing, credit, political, personal attributes, or consumer data.
8. **Approval rules**: who can approve live posts, sends, spend, creator contracts, lead enrichment, CRM updates, and public claims.

## Phase 2: Channel Map

Create `workspace/growth-hacker/_channel-map.md`.

Cover at minimum:

### B2B

- LinkedIn organic
- LinkedIn articles/newsletters
- Events and webinars
- AI outbound and SDR
- ABM
- AEO and AI search
- Blogs and SEO
- Long-form operator writing
- YouTube
- X/founder media
- B2B influencers and creators
- Partnerships and co-marketing
- Newsletter/lifecycle
- Podcast
- Community and Reddit
- PR and digital publications
- Paid media and retargeting

### B2C

- AI UGC and creative volume
- Organic TikTok
- Paid social
- B2C influencers and creator commerce
- Events, pop-ups, and field marketing
- Sponsorships
- Email, SMS, and retention loops
- Referral, affiliate, and community loops
- Instagram/Reels, YouTube Shorts, Pinterest, Snapchat, and relevant social surfaces
- Ecommerce SEO, product pages, creator-led landing pages, and offer testing when commerce is in scope

For every channel, write:

```markdown
## [Channel]

**Fit:** [high / medium / low / blocked]
**Why now:** [stage and audience reason]
**Inputs needed:** [...]
**Execution loop:** [...]
**Kai skills:** [...]
**Gates:** [...]
**Metrics:** [...]
**Kill rule:** [...]
**Next test:** [...]
```

## Phase 3: Prioritize

Create `workspace/growth-hacker/_prioritization-scorecard.md`.

Score every channel 1-5:

| Dimension | Question |
|---|---|
| Audience density | Does the ICP gather here often enough to matter? |
| Message fit | Can the channel carry the proof, offer, and story? |
| Speed to signal | Can we learn within the sprint window? |
| Cost to test | Can we test without large sunk cost or fragile setup? |
| Compounding value | Does output become an owned asset, list, source, or loop? |
| Compliance risk | Can we run this without policy, consent, or data risk? |
| Operator advantage | Do we have unusual taste, data, access, or speed here? |

Pick:

- **Primary channel**: the best near-term growth bet.
- **Secondary channel**: supports the primary or has independent signal.
- **Exploratory channel**: cheap, high-upside learning.
- **Blocked channels**: delayed because source access, compliance, offer, or tracking is not ready.

## Phase 4: Fan-Out Plan

Create `workspace/growth-hacker/_agent-fanout-plan.md`.

Use these operators:

| Operator | Responsibility | Output |
|---|---|---|
| Growth Lead | Owns channel thesis and scorecard | `_90-day-sprint.md` |
| Evidence Scout | Finds proof and source gaps | `_evidence-ledger.md`, `_data-gaps.md` |
| B2B Channel Operator | Writes B2B test cards | `_b2b-channel-tests.md` |
| B2C Channel Operator | Writes B2C test cards | `_b2c-channel-tests.md` |
| Content Engine | Turns winning ideas into content assets | `_asset-backlog.md` |
| Creator/Partner Manager | Builds creator, partner, and sponsor queue | `_creator-partner-shortlist.md` |
| Outbound/SDR Operator | Builds source, suppression, and approval plan | `_outbound-approval-plan.md` |
| Paid Media Operator | Builds creative ledger and paid test notes | `_creative-ledger.md` |
| Analytics Operator | Defines dashboard and read windows | `_metrics-dashboard.md` |
| Compliance Reviewer | Blocks unsafe assets/actions | `_quality-report.md` |

If actual subagents are available, split read-only research by channel family and keep final integration in the main thread. If actual subagents are not available, still write the same operator queue so future runs can delegate.

## Phase 5: Build Test Cards

Create:

- `workspace/growth-hacker/_b2b-channel-tests.md`
- `workspace/growth-hacker/_b2c-channel-tests.md`

Each test card must include:

- Hypothesis
- Channel
- Audience
- Offer or CTA
- Asset required
- Distribution action
- Source tracking
- Compliance gate
- Owner
- Timeline
- Kill rule
- Graduation rule
- Next Kai skill to run

Do not invent benchmarks. Use first-party history, user-provided goals, or mark the target as a data gap.

## Phase 6: Create The 90-Day Sprint

Create `workspace/growth-hacker/_90-day-sprint.md`.

Use this cadence:

| Window | Work |
|---|---|
| Days 1-10 | Inventory, evidence, channel map, scorecard, tracking gaps |
| Days 11-30 | Build test assets, approval queues, landing/follow-up path, first test batch |
| Days 31-60 | Read results, kill weak tests, improve strongest path, repurpose winners |
| Days 61-90 | Graduate one repeatable channel, write runbook, set budget and owner cadence |

## Phase 7: Output Package

Write the complete package to:

```text
workspace/growth-hacker/
```

Required files:

```text
_brief.md
_channel-map.md
_prioritization-scorecard.md
_90-day-sprint.md
_agent-fanout-plan.md
_b2b-channel-tests.md
_b2c-channel-tests.md
_asset-backlog.md
_creative-ledger.md
_outbound-approval-plan.md
_creator-partner-shortlist.md
_metrics-dashboard.md
_decision-log.md
_data-sources.md
_data-gaps.md
_quality-report.md
```

## Specialist Routing

After the package is built, route execution to the specialist skill:

| Need | Skill |
|---|---|
| Stage diagnosis | `/kai-growth-plan` |
| LinkedIn, X, TikTok, YouTube, Instagram posts | `/kai-social` |
| Blog, long-form, SEO, or article draft | `/kai-write`, `/kai-content-calendar`, `/kai-topical-map` |
| AEO and AI-search visibility | `/kai-surround-sound`, `/kai-seo-audit` |
| Outbound or account workflow | `/kai-sdr-operator`, `/kai-cold-outreach` |
| Creator, influencer, UGC | `/kai-influencer` |
| Paid social and retargeting | `/kai-ad-campaign`, `/kai-retarget`, `/kai-daily-ad-review` |
| Webinar or event | `/kai-webinar`, `/kai-launch` |
| Partnership, sponsorship, affiliate | `/kai-partnership`, `/kai-influencer` |
| Email, SMS, lifecycle, retention | `/kai-email-system`, `/kai-newsletter`, `/kai-retention` |
| Measurement | `/kai-analytics`, `/kai-data-dashboard` |
| Gate review | `/kai-gate` |

## Quality Gates

Before handoff:

1. Run `python scripts/quality_gates/banned_word_check.py --file <file>` against customer-facing markdown files.
2. Run `python scripts/quality_gates/four_us_score.py --file <file>` on strategic briefs, test cards, outbound briefs, page briefs, and content assets. Use 12/16 for strategic/content/page work and 10/16 for ads/email/outreach.
3. Run `python scripts/quality_gates/seo_lint.py --file <file>` on SEO/AEO pages.
4. Run `python scripts/quality_gates/agent_readiness_lint.py https://<domain>` before AEO/surround-sound execution.
5. Apply `harness/references/advertising-compliance.md` and platform policy references before ads, sponsorships, affiliates, or creator campaigns.
6. Confirm `_data-gaps.md` lists missing analytics, source access, proof, budgets, or legal approvals.
7. Confirm `_quality-report.md` lists every blocked live action.

## Live-Action Rule

Do not send email, send DMs, publish posts, upload ads, change spend, sign creator contracts, scrape/enrich lead lists, call or text prospects, mutate CRM records, or edit live sites without explicit approval and a saved dry-run artifact.

## Final Response

Return:

- Package path.
- Primary, secondary, and exploratory channel picks.
- Blocked channels and why.
- Specialist `/kai` skills to run next.
- Gates run and gates still required.
