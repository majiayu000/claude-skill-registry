---
name: marketing
description: Marketing workflows — SEO audits, campaign planning, content strategy, email sequences, competitive analysis, brand review, performance reporting. Use when auditing SEO, planning campaigns, creating content strategy, building email sequences, or analyzing marketing performance.
routing:
  triggers:
    - "marketing"
    - "SEO"
    - "campaign"
    - "content strategy"
    - "email sequence"
    - "brand review"
    - "competitive analysis"
    - "marketing performance"
  category: business
  force_route: false
  pairs_with:
    - csuite
user-invocable: true
---

# Marketing

Umbrella skill for marketing workflows: SEO audits, campaign planning, content strategy, email sequences, competitive analysis, brand review, and performance reporting. Each mode loads its own reference files on demand -- this skill detects the mode, loads the right references, and executes the appropriate framework.

**Scope**: Marketing strategy, content, and analysis. Use csuite for executive-level growth decisions, voice-writer for voice-calibrated content, publish for blog pipeline mechanics, and research-pipeline for formal multi-source research.

---

## Mode Detection

Classify the user's request into exactly one mode before proceeding. If the request spans multiple modes, choose the primary one and note the secondary.

| Mode | Signal Phrases | Reference |
|------|---------------|-----------|
| **SEO_AUDIT** | SEO audit, keyword research, content gaps, technical SEO, on-page analysis, competitor SEO | `references/seo-audit.md` |
| **CAMPAIGN** | Campaign plan, product launch, lead gen, awareness campaign, channel strategy, budget allocation | `references/campaign-planning.md` |
| **CONTENT** | Content strategy, editorial calendar, content framework, funnel mapping, blog structure, content types | `references/content-strategy.md` |
| **EMAIL** | Email sequence, drip campaign, nurture flow, onboarding emails, re-engagement, email automation | `references/email-sequences.md` |
| **COMPETITIVE** | Competitive analysis, competitor research, battlecard, positioning comparison, market landscape | `references/seo-audit.md` (competitor section) + `references/campaign-planning.md` (positioning) |
| **BRAND** | Brand review, voice check, style guide, messaging consistency, tone audit | `references/content-strategy.md` (voice section) |
| **PERFORMANCE** | Marketing report, performance analysis, campaign results, metrics summary, ROI analysis | `references/campaign-planning.md` (metrics section) |

Load the reference(s) required by the detected mode. **Always load `references/llm-marketing-failure-modes.md` regardless of mode** — it contains detection heuristics and concrete examples for every marketing failure pattern below.

---

## LLM Failure Modes

See `references/llm-marketing-failure-modes.md` for the complete failure mode catalog (generic copy, keyword stuffing, fabricated metrics, hallucinated competitor data, tone mismatch, vanity metrics, template regurgitation, unsubstantiated claims, channel-agnostic recommendations, recency bias). Universal failure modes in `skills/shared-patterns/llm-domain-failure-modes-base.md`.

---

## Mode: SEO_AUDIT

**Framework**: RESEARCH -> AUDIT -> PRIORITIZE

**Phase 1: RESEARCH** -- Gather keyword and competitive data.

Inputs required:
- URL or domain (or topic for keyword-only research)
- Audit type: Full site audit | Keyword research | Content gap analysis | Technical SEO check | Competitor SEO comparison (default: full site)
- Target keywords (optional)
- Competitors (optional -- identify 2-3 via web search if not provided)

Load `references/seo-audit.md` for the full methodology.

Execute keyword research:
- Classify by intent: informational, navigational, commercial, transactional
- Assess: primary keywords, secondary keywords, long-tail opportunities, question-based keywords
- Estimate difficulty and opportunity relative to the site's current authority

**Gate**: Keywords classified by intent. Competitors identified.

**Phase 2: AUDIT** -- Evaluate the site against SEO fundamentals.

On-page: title tags, meta descriptions, H1/H2 structure, keyword usage, internal linking, image alt text, URL structure. Technical: page speed, mobile-friendliness, structured data, crawlability, broken links, HTTPS, Core Web Vitals, indexation. Content gaps: competitor topic coverage, content freshness, thin content, missing content types, funnel gaps, topic cluster opportunities.

**Guard against keyword stuffing** (see failure modes). Keyword density > 2% is a finding, not a recommendation.

**Gate**: All audit sections completed with evidence.

**Phase 3: PRIORITIZE** -- Produce actionable output.

Output:
1. Executive summary (3-5 sentences: biggest strength, top 3 priorities, overall assessment)
2. Keyword opportunity table (15-25 keywords, sorted by opportunity score)
3. On-page issues table (page, issue, severity, fix)
4. Content gap recommendations (topic, why it matters, format, priority, effort)
5. Technical SEO checklist (check, pass/fail/warning, details)
6. Competitor comparison matrix (dimensions x competitors x winner)
7. Prioritized action plan: Quick Wins (this week, <2 hours each) and Strategic Investments (this quarter)

**Gate**: Every recommendation has expected impact, effort estimate, and dependencies.

---

## Mode: CAMPAIGN

**Framework**: BRIEF -> PLAN -> CALENDAR

**Phase 1: BRIEF** -- Define objectives and audience.

Inputs required:
- Campaign goal (drive signups, increase awareness, launch product, generate leads, re-engage churned users)
- Target audience (demographics, roles, industries, pain points, buying stage)
- Timeline with fixed dates
- Budget range (optional)

Load `references/campaign-planning.md` for channel selection, budget allocation, and metrics frameworks.

Define: campaign name, one-sentence summary, SMART primary objective, secondary objectives. Build audience profile: "[Role] at [company type] struggling with [pain point] looking for [outcome]. Discovers solutions through [channels], cares about [priorities]."

**Guard against generic messaging** (see failure modes). Core message must reference the specific audience pain point, not a generic benefit.

**Gate**: SMART objective stated. Audience profile complete with pain points and channels.

**Phase 2: PLAN** -- Design channel strategy and content.

Channel strategy: for each recommended channel, state why it fits the audience and objective, content format, effort level, budget allocation (if budget provided). Cover owned (blog, email, social), earned (PR, influencer, community), and paid (SEM, social ads, display).

Key messages: core message (one sentence), 3-4 supporting messages tied to pain points, proof points, and message variations by channel.

Content pieces needed: asset name, type, description, priority, timeline.

Success metrics: primary KPI with target, 3-5 secondary KPIs, tracking method, reporting cadence.

**Guard against vanity metrics** (see failure modes). Every KPI must connect to a business outcome.

**Gate**: Channel strategy justified. Metrics tied to business outcomes. Content assets listed with priorities.

**Phase 3: CALENDAR** -- Build the execution timeline.

Week-by-week content calendar:

| Week | Content Piece | Channel | Owner/Notes | Dependencies | Status |
|------|--------------|---------|-------------|--------------|--------|

Calendar rules: start with milestones, work backward, map content to funnel stages, batch by theme, balance channels, leave 20% flexibility.

Include: risks and mitigations (2-3), budget allocation breakdown (if budget provided), next steps with immediate action items.

**Gate**: Calendar complete. Dependencies mapped. Budget allocated (if applicable).

---

## Mode: CONTENT

**Framework**: AUDIT -> FRAMEWORK -> MAP

**Phase 1: AUDIT** -- Assess current content state.

Inputs required:
- Content type (blog, social, email, landing page, press release, case study, or strategy-level)
- Topic or theme
- Target audience
- Key messages (2-4)

Load `references/content-strategy.md` for templates, writing patterns, and SEO fundamentals.

If strategy-level: audit existing content volume, channels, performance, publishing cadence, and audience engagement. Identify the binding constraint: Discovery, Content quality, Conversion, Retention, or Capacity.

**Gate**: Current state understood. Binding constraint identified (if strategy-level).

**Phase 2: FRAMEWORK** -- Select and apply the right content framework.

For individual content pieces, apply the appropriate template from `references/content-strategy.md`:
- Blog: headline options (2-3), hook, 3-5 sections with subheadings, conclusion with CTA, SEO recommendations
- Social: platform-specific format, hook in first line, hashtags, engagement prompt
- Email: subject line options (2-3), preview text, scannable body, one primary CTA
- Landing page: headline/subheadline, value props, social proof placement, CTA hierarchy
- Press release: headline, dateline, lead paragraph (who/what/when/where/why), boilerplate
- Case study: title with result, challenge/solution/results structure, customer quote placeholder

SEO for web content: primary keyword in headline + first paragraph + one subheading + meta description. 2-3 internal links. 1-2 external authority links. Keyword density < 2%.

**Guard against generic copy** (see failure modes). Every headline must be specific to the audience and topic. "Unlock the power of [X]" is rejected.

**Guard against template regurgitation** (see failure modes). Content must reflect user's specific audience, product, and constraints.

**Gate**: Content drafted. SEO recommendations attached (for web content). No generic phrasing.

**Phase 3: MAP** -- For strategy-level requests, build the content plan.

Editorial calendar: content types, topics, channels, cadence, funnel stage mapping. Distribution strategy: primary channels, repurposing plan, promotion tactics. Funnel mapping: awareness content, consideration content, decision content -- identify gaps.

**Gate**: Content plan covers all funnel stages. Cadence matches capacity. Distribution strategy defined.

---

## Mode: EMAIL

**Framework**: ARCHITECT -> DRAFT -> OPTIMIZE

**Phase 1: ARCHITECT** -- Design the sequence structure.

Inputs required:
- Sequence type: Onboarding | Lead nurture | Re-engagement | Product launch | Event follow-up | Upgrade/upsell | Win-back | Educational drip
- Goal (what the sequence achieves)
- Audience (who receives it, what stage, segmentation)
- Brand voice (if configured, apply automatically; otherwise ask)

Load `references/email-sequences.md` for sequence templates, branching logic, and benchmarks.

Define: narrative arc (story across all emails), journey mapping (each email to a buyer/user stage), escalation logic (how intensity builds), success definition (what action triggers exit).

Recommended email count and cadence by type:
- Onboarding: 5-7 emails over 14-21 days
- Lead nurture: 4-6 emails over 3-4 weeks
- Re-engagement: 3-4 emails over 10-14 days
- Win-back: 3-5 emails over 30 days
- Product launch: 4-6 emails over 2-3 weeks

**Gate**: Sequence type selected. Email count and cadence defined. Narrative arc documented.

**Phase 2: DRAFT** -- Write each email.

For each email produce:
- Subject line: 2-3 options, varied approaches, under 50 characters
- Preview text: 40-90 characters, complements (not repeats) subject
- Purpose: one sentence
- Body copy: full draft, hook/body/CTA structure, short paragraphs, personalization tokens
- Primary CTA: button text and destination
- Timing: days after trigger or previous email
- Segment/condition notes: who receives, who skips

**Guard against generic copy** (see failure modes). Subject lines must not be interchangeable between companies.

**Guard against tone-deaf messaging** (see failure modes). A win-back email is not a product launch email. Tone must match the emotional context.

**Gate**: All emails drafted. Subject lines specific. Tone matches sequence stage.

**Phase 3: OPTIMIZE** -- Add branching, testing, and benchmarks.

Sequence logic:
- Branching conditions (opened but not clicked -> softer re-ask; clicked CTA -> skip ahead)
- Exit conditions (conversion defined and enforced)
- Re-entry rules, suppression rules

Flow diagram (text-based):
```
[Trigger] --> Email 1 (Day 0)
                |
          Opened? --Yes--> Email 2 (Day 3)
                |              |
                No        Clicked? --Yes--> [EXIT: Converted]
                |              |
                v              No
          Email 1b (Day 2)     v
                +--------> Email 3 (Day 7)
```

A/B test suggestions: 2-3 tests with what to test, split method, success metric.

Performance benchmarks:

| Metric | Onboarding | Lead Nurture | Re-engagement | Win-back |
|--------|-----------|--------------|---------------|----------|
| Open rate | 50-70% | 20-30% | 15-25% | 15-20% |
| CTR | 10-20% | 3-7% | 2-5% | 2-4% |
| Conversion | 15-30% | 2-5% | 3-8% | 1-3% |
| Unsubscribe | <0.5% | <0.5% | 1-2% | 1-3% |

**Gate**: Branching logic defined. Exit conditions explicit. Benchmarks set.

---

## Mode: COMPETITIVE

**Framework**: RESEARCH -> COMPARE -> RECOMMEND

**Phase 1: RESEARCH** -- Gather competitor intelligence.

Inputs required:
- Competitor name(s)
- Your company/product context (recommended)
- Focus areas (messaging, product, content, pricing, market presence -- default: all)

Research using web search:
- Primary sources: website (homepage, product, pricing, about, careers), blog, social, press releases
- Secondary sources: review sites (G2, Capterra), analyst reports, news coverage, community forums

For each competitor: one-sentence positioning, target audience, size/stage indicators, recent developments.

**Guard against hallucinated competitor data** (see failure modes). Every claim must come from a search result or user-provided data. Include dates.

**Gate**: All competitors researched from verifiable sources. Data dated.

**Phase 2: COMPARE** -- Build structured comparisons.

Messaging analysis: tagline, core value prop, messaging themes (3-5), tone characterization, how they describe the problem. Product positioning: category, emphasized features, claimed differentiators, pricing approach. Content strategy: blog frequency, content types, social presence, thought leadership themes.

Messaging comparison matrix:

| Dimension | Your Company | Competitor A | Competitor B |
|-----------|-------------|--------------|--------------|
| Primary tagline | | | |
| Target buyer | | | |
| Key differentiator | | | |
| Tone/voice | | | |
| Core value prop | | | |

Content gap analysis: topics they cover that you don't, formats they use that you don't, audiences they reach that you don't.

**Gate**: Comparison matrix complete. Gaps identified with evidence.

**Phase 3: RECOMMEND** -- Actionable positioning and next steps.

Positioning gaps to exploit. Messaging angles unclaimed by competitors. Audience segments underserved. 3-5 actionable recommendations split into quick wins and strategic moves.

Optional battlecard output: quick overview, their pitch, honest strengths, weaknesses, your differentiators, objection handling table, landmines to set/defuse.

**Gate**: Recommendations grounded in comparison data. No fabricated intelligence.

---

## Mode: BRAND

**Framework**: LOAD -> REVIEW -> REVISE

**Phase 1: LOAD** -- Establish review criteria.

Inputs required:
- Content to review (pasted, file path, or URL)
- Brand guidelines source (configured, user-provided, or generic review)

Load `references/content-strategy.md` for voice attribute frameworks and style guide patterns.

**Gate**: Content loaded. Review criteria established.

**Phase 2: REVIEW** -- Evaluate against brand standards.

With brand guidelines: voice/tone alignment, terminology compliance, messaging pillar consistency, style guide compliance. Without guidelines: clarity, consistency, professionalism. Always check: unsubstantiated claims, missing disclaimers, comparative claims, regulatory language, testimonial issues.

Output as findings table:

| Issue | Location | Severity | Suggestion |
|-------|----------|----------|------------|

Severity: High (contradicts brand, compliance risk), Medium (inconsistent but not damaging), Low (minor style issue).

**Guard against unsubstantiated claims** (see failure modes). Flag every superlative without evidence.

**Gate**: All issues identified and severity-rated.

**Phase 3: REVISE** -- Provide actionable fixes.

Before/after for top 3-5 highest-severity issues. Legal/compliance flags listed separately. Overall assessment: alignment quality, biggest strengths, most important improvements.

**Gate**: Revisions provided. Compliance flags separated.

---

## Mode: PERFORMANCE

**Framework**: GATHER -> ANALYZE -> RECOMMEND

**Phase 1: GATHER** -- Collect performance data.

Inputs required:
- Report type: Campaign | Channel | Content | Overall marketing | Custom
- Time period
- Data source: user-provided metrics (paste, CSV, key numbers)
- Comparison period (optional)
- Stakeholder audience (optional -- executive summary vs. detailed)

Load `references/campaign-planning.md` for metric definitions and benchmarks.

If user has not provided data: prompt with "Please paste or share your performance data. I can work with spreadsheets, CSV data, or just the key numbers."

**Guard against fabricated metrics** (see failure modes). All performance data comes from the user or connected tools.

**Gate**: Data received from user. Report type and time period confirmed.

**Phase 2: ANALYZE** -- Interpret the data.

Key metrics dashboard:

| Metric | This Period | Prior Period | Change | Target | Status |
|--------|------------|--------------|--------|--------|--------|

Status: On track | At risk | Off track.

Trend analysis: directional trends (4+ periods), inflection points, seasonality, anomalies, leading indicators. What worked: top 3-5 wins with data and replication hypothesis. What needs improvement: bottom 3-5 with diagnosis and recommended fixes.

Attribution context: clarify what model is in use. Note limitations. Last-touch understates awareness channels; first-touch understates conversion channels.

**Gate**: Trends identified with evidence. Wins and misses attributed to causes.

**Phase 3: RECOMMEND** -- Prioritize next actions.

For each recommendation: what to do, why (linked to data), expected impact, effort, priority.

Impact/effort matrix:

| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Do first | Plan next sprint |
| **Low Impact** | Do if time | Deprioritize |

Next period focus: top 3 priorities, tests to run, metric targets.

Report formatting: tables for data, bold key numbers, executive summary suitable for forwarding. Detailed appendix for granular data.

**Gate**: Recommendations linked to data. Priorities ranked. Next-period targets set.

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No audience context | User says "write a blog post about X" without who/why | Ask for audience, pain point, and desired outcome before generating |
| Generic output | Draft uses cliche marketing phrases | Reject and rewrite with specifics. Check against failure modes table. |
| Unverifiable competitor claims | No search results support the claim | State explicitly what could not be verified. Never fill gaps with plausible fiction. |
| Metrics without context | Numbers presented without comparison or trend | Always include prior period, target, or benchmark for context |
| Keyword stuffing in recommendations | SEO advice over-optimizes for density | Cap at 1-2%. Natural language first. |
| Tone mismatch | Same voice for incident response and product launch | Check situation context. Adjust tone while keeping brand voice consistent. |
| Scope creep across modes | Request spans 3+ modes | Pick the primary mode. Complete it. Offer secondary mode as follow-up. |
| Data fabrication request | User asks "what would good metrics look like" | Provide benchmark ranges with sources. Never present benchmarks as the user's actual data. |

---

## References

| Reference | When to Load | Content |
|-----------|-------------|---------|
| `references/seo-audit.md` | SEO_AUDIT mode: keyword research, on-page analysis, technical SEO, content gaps, competitor benchmarking | Full audit methodology with intent classification, technical checklist, competitor comparison framework |
| `references/campaign-planning.md` | CAMPAIGN and PERFORMANCE modes: audience segmentation, channel strategy, budget allocation, success metrics, timeline planning | Channel selection matrices, budget frameworks, metrics by campaign type, reporting templates |
| `references/content-strategy.md` | CONTENT and BRAND modes: content frameworks, writing patterns, editorial calendar, voice documentation, style enforcement | Content type templates, SEO fundamentals, headline formulas, CTA patterns, brand voice frameworks |
| `references/email-sequences.md` | EMAIL mode: sequence architecture, subject line patterns, engagement metrics, A/B testing | Sequence type templates, branching logic, flow diagrams, benchmark tables |
| `references/llm-marketing-failure-modes.md` | All modes (load selectively): where LLMs fail at marketing tasks | Detailed failure taxonomy with examples, detection heuristics, and mitigation strategies |
