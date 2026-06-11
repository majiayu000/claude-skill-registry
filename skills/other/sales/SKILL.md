---
name: sales
description: Sales workflows — call prep, pipeline analysis, outreach, competitive intelligence, forecasting. Use when prepping for calls, reviewing pipeline health, drafting personalized outreach, analyzing competitors, or building forecasts.
routing:
  triggers:
    - "sales"
    - "call prep"
    - "pipeline review"
    - "forecast"
    - "draft outreach"
    - "prospect research"
    - "competitive intelligence"
  category: business
  force_route: false
  pairs_with:
    - csuite
user-invocable: true
---

# Sales

Umbrella skill for sales execution: call preparation, pipeline health analysis, outreach drafting, competitive intelligence, and forecasting. Each mode loads its own references on demand. Detects the mode from the request, loads the right context, and executes the appropriate workflow.

**Scope**: Revenue-facing workflows where the user is preparing for, executing, or following up on sales activities. Use csuite for strategic business decisions. Use research-pipeline for deep multi-source research. Use voice-writer for content generation.

---

## Mode Detection

Classify the request into exactly one mode. If the request spans multiple, choose the primary and note the secondary.

| Mode | Signal Phrases | Primary Activity |
|------|---------------|-----------------|
| **CALL-PREP** | "prep me for", "meeting with", "call with", "get ready for", "before my call" | Research + agenda + questions for an upcoming meeting |
| **PIPELINE** | "pipeline review", "deal health", "stale deals", "pipeline hygiene", "which deals" | Analyze pipeline health, prioritize deals, flag risks |
| **OUTREACH** | "draft outreach", "cold email", "reach out to", "write email to", "LinkedIn message" | Research prospect then draft personalized message |
| **COMPETITIVE** | "competitive intel", "battlecard", "how do we compare", "vs competitor", "competitor research" | Analyze competitors, build positioning, talk tracks |
| **FORECAST** | "forecast", "gap to quota", "commit vs upside", "pipeline coverage", "will I hit my number" | Weighted forecast with scenarios and gap analysis |
| **CALL-SUMMARY** | "call notes", "summarize call", "follow up email", "action items from call", "what happened on the call" | Extract action items, draft follow-up, log summary |
| **RESEARCH** | "research company", "look up", "intel on", "who is", "tell me about" | Company/person research for sales context |

---

## Reference Loading Table

Load only the references required by the detected mode. Always load `references/llm-sales-failure-modes.md` for any mode.

| Mode | Load These References |
|------|----------------------|
| CALL-PREP | `references/call-prep.md`, `references/llm-sales-failure-modes.md` |
| PIPELINE | `references/pipeline-analysis.md`, `references/llm-sales-failure-modes.md` |
| OUTREACH | `references/outreach-patterns.md`, `references/llm-sales-failure-modes.md` |
| COMPETITIVE | `references/competitive-intelligence.md`, `references/llm-sales-failure-modes.md` |
| FORECAST | `references/pipeline-analysis.md`, `references/llm-sales-failure-modes.md` |
| CALL-SUMMARY | `references/call-prep.md`, `references/llm-sales-failure-modes.md` |
| RESEARCH | `references/call-prep.md`, `references/competitive-intelligence.md`, `references/llm-sales-failure-modes.md` |

---

## Workflow: CALL-PREP

**Framework**: GATHER -> RESEARCH -> SYNTHESIZE -> DELIVER

**Phase 1: GATHER** -- Collect meeting context from the user.

Ask for: company name, meeting type (discovery/demo/negotiation/check-in/QBR), attendees (names + titles), user's goal for the call, any context they want to share (paste notes, emails, prior interactions).

Accept whatever they provide. Missing fields become research targets, not blockers.

**Gate**: Company name known. Meeting type classified.

**Phase 2: RESEARCH** -- Web research to fill gaps.

Search for: company news (last 30 days), funding/leadership changes, attendee LinkedIn profiles, company product/service description, industry context. Extract: what the company does, recent trigger events, attendee backgrounds, hiring signals.

Source every company fact from search results. State 'not found' for missing data. Do not invent revenue figures, employee counts, or funding rounds that were not found in search results. See `references/llm-sales-failure-modes.md`.

**Gate**: Company profile assembled from verified sources. Gaps explicitly noted.

**Phase 3: SYNTHESIZE** -- Build the prep brief.

Produce: account snapshot table, attendee profiles with talking points, context/history summary, suggested agenda tailored to meeting type, discovery questions targeting understanding gaps, potential objections with responses.

Meeting type shapes the output:
- **Discovery**: questions > talking. Focus on qualification signals.
- **Demo**: tailored examples for their use case. Focus on technical requirements.
- **Negotiation**: objection handling, value justification. Focus on path to agreement.
- **Check-in/QBR**: value delivered, expansion opportunities. Focus on renewal signals.

**Gate**: All sections populated. No placeholder text. No fabricated details.

**Phase 4: DELIVER** -- Present the formatted brief.

Output a structured markdown brief: Account Snapshot (table), Attendee Profiles, Context & History, Suggested Agenda (numbered), Discovery Questions (5-7), Potential Objections (table: objection | response), Internal Notes.

---

## Workflow: PIPELINE

**Framework**: INGEST -> SCORE -> PRIORITIZE -> DELIVER

**Phase 1: INGEST** -- Get pipeline data.

Accept: CSV upload (preferred), pasted deal descriptions, or verbal pipeline summary. Required fields per deal: name, amount, stage, close date. Helpful: last activity date, owner, primary contact, created date.

If the user describes deals verbally, structure into a deal table before analysis.

**Gate**: Deals structured in tabular format. At minimum: name, amount, stage, close date.

**Phase 2: SCORE** -- Health assessment on four dimensions.

| Dimension | Weight | Red Flag |
|-----------|--------|----------|
| Stage Progression | 25 | Same stage 30+ days |
| Activity Recency | 25 | No activity 14+ days |
| Close Date Accuracy | 25 | Close date in the past |
| Contact Coverage | 25 | Single-threaded (one contact) |

Score each deal on each dimension. Compute pipeline health score (0-100). Identify risk flags: stale deals, stuck deals, past close dates, single-threaded deals, missing data.

Do not fabricate activity dates or deal history the user did not provide. If a field is missing, flag it as a hygiene issue rather than assuming a value.

**Gate**: Health score computed. Risk flags enumerated. Hygiene issues listed.

**Phase 3: PRIORITIZE** -- Rank deals and generate action plan.

Default weighting: Close Date (30%), Deal Size (25%), Stage (20%), Activity (15%), Risk (10%). User can override: "focus on big deals" or "I need quick wins."

Classify deals into: Close This Week, Close This Month, Nurture, Consider Removing.

Generate top 3 priority actions with: deal name, reason it is priority, specific next step, dollar impact.

**Gate**: Deals ranked. Top 3 actions identified. Dead-weight deals flagged.

**Phase 4: DELIVER** -- Output the pipeline review.

Sections: Pipeline Health Score (table), Priority Actions This Week (top 3), Deal Prioritization Matrix (by time horizon), Risk Flags (stale/stuck/past-date/single-threaded tables), Hygiene Issues (table), Pipeline Shape (by stage, by month, by size), Recommendations, Deals to Consider Removing.

---

## Workflow: OUTREACH

**Framework**: RESEARCH -> HOOK -> DRAFT -> DELIVER

**Phase 1: RESEARCH** -- Always research before drafting. Never send generic outreach.

Parse the request: extract person name, company, title/role, email/LinkedIn if provided.

Search for: person background (LinkedIn, bio), company overview, recent news/trigger events, shared connections or interests, company hiring signals.

Must find before drafting: who they are (title, background), what the company does, a personalization hook (trigger event, their content, mutual connection, company initiative).

**Gate**: Target identified. Company understood. At least one genuine personalization hook found.

**Phase 2: HOOK** -- Select the personalization angle.

Priority order:
1. Trigger event (funding, hiring, product launch, news) -- most timely
2. Mutual connection -- social proof
3. Their content (post, article, talk) -- shows research
4. Company initiative -- relevant to their priorities
5. Role-based pain point -- least personal, last resort

Ground every opening in specific research. Reference a finding only true of this prospect. See `references/outreach-patterns.md` for anti-template patterns.

**Gate**: Hook selected with source. Opening line drafted from real research.

**Phase 3: DRAFT** -- Write the message.

Email structure (AIDA): Personalized opening (hook), Interest (their problem in 1-2 sentences), Desire (brief proof point from a similar company), Action (clear, low-friction CTA).

Rules: under 150 words. No markdown formatting (no bold, no headers). Short paragraphs (2-3 sentences). One value prop. One CTA. Plain text that looks natural in any email client.

Also produce: 2-3 subject line alternatives (under 50 chars, no spam words), LinkedIn connection request (under 300 chars, no pitch), follow-up sequence (Day 3, Day 7, Day 14 breakup).

**Gate**: Email under 150 words. No markdown formatting. Opening references specific research. CTA is one clear ask.

**Phase 4: DELIVER** -- Output the outreach package.

Sections: Research Summary (target, hook, goal), Email Draft (subject, body), Subject Alternatives, LinkedIn Message, Why This Approach (table: element | based on), Follow-up Sequence.

---

## Workflow: COMPETITIVE

**Framework**: SCOPE -> RESEARCH -> ANALYZE -> DELIVER

**Phase 1: SCOPE** -- Define the competitive landscape.

Gather: user's company and product, competitors to analyze (1-5), any specific deals where they are competing, known strengths/weaknesses.

If first interaction, ask for seller context. On subsequent invocations, confirm stored context.

**Gate**: Seller context established. Competitor list defined.

**Phase 2: RESEARCH** -- Systematic research per competitor.

For each competitor, search for: product features, pricing model, recent announcements (90 days), product updates/changelog, G2/Capterra reviews, customer base, careers/hiring signals.

Also search: "[Your company] vs [Competitor]" for existing comparisons.

Never fabricate pricing, features, or customer claims. If pricing is not publicly available, state "pricing not publicly listed" rather than guessing. See `references/llm-sales-failure-modes.md`.

**Gate**: Each competitor researched from public sources. No fabricated claims.

**Phase 3: ANALYZE** -- Build competitive positioning.

For each competitor, produce: where they win (with your counter), where you win (with proof points), pricing intelligence, talk tracks (early mention / displacement / late addition), objection handling, landmine questions (questions that expose their weaknesses without badmouthing).

Build a comparison matrix: Feature | You | Competitor 1 | Competitor 2 | ...

Acknowledge where competitors are strong. Credibility comes from honesty about relative strengths.

**Gate**: Comparison matrix complete. Talk tracks per competitor. Landmine questions identified.

**Phase 4: DELIVER** -- Output the competitive analysis.

Sections: Comparison Matrix (feature grid), Per-Competitor Battlecards (profile, differentiators, talk tracks, objections, landmines), Refresh Recommendations.

---

## Workflow: FORECAST

**Framework**: INGEST -> WEIGHT -> SCENARIO -> DELIVER

**Phase 1: INGEST** -- Gather pipeline and targets.

Required: pipeline deals (CSV, pasted, or described), quota number, period end date, already-closed amount.

Required per deal: name, amount, stage, close date. Helpful: last activity date, owner, account name.

**Gate**: Pipeline data structured. Quota and timeline known.

**Phase 2: WEIGHT** -- Apply stage probabilities and risk adjustments.

Default stage probabilities (user can override):

| Stage | Probability |
|-------|------------|
| Closed Won | 100% |
| Negotiation / Contract | 80% |
| Proposal / Quote | 60% |
| Evaluation / Demo | 40% |
| Discovery / Qualification | 20% |
| Prospecting / Lead | 10% |

Risk adjustments: no activity 14+ days (-10%), close date in past (-20%), single-threaded (-10%), stage 30+ days stuck (-15%). These compound.

Classify each deal: Commit (high confidence, would stake forecast on it) or Upside (could close but has risk).

Do not inflate forecast numbers. Better to under-promise than to include deals the user knows are unlikely. See `references/llm-sales-failure-modes.md`.

**Gate**: Weighted forecast calculated. Commit vs upside classified. Risk adjustments applied.

**Phase 3: SCENARIO** -- Build three scenarios and gap analysis.

| Scenario | Method |
|----------|--------|
| Best Case | All deals close as expected |
| Likely Case | Stage-weighted probabilities with risk adjustments |
| Worst Case | Only commit deals close |

Gap analysis: quota minus (closed + likely forecast) = gap. For each gap dollar: identify acceleration candidates, revival candidates, new pipeline needed.

Coverage ratio: open pipeline / remaining quota. Below 2x is risky. 3x is healthy.

**Gate**: Three scenarios calculated. Gap quantified. Coverage ratio stated.

**Phase 4: DELIVER** -- Output the forecast.

Sections: Summary Table (quota, closed, pipeline, weighted, gap, coverage), Forecast Scenarios (table), Pipeline by Stage (table with probability and weighted value), Commit vs Upside (deal-level tables with reasons), Risk Flags (table), Gap Analysis (options to close), Recommendations.

---

## Workflow: CALL-SUMMARY

**Framework**: EXTRACT -> STRUCTURE -> DRAFT -> DELIVER

**Phase 1: EXTRACT** -- Parse call notes or transcript.

Accept: pasted notes (bullet points, rough notes, stream of consciousness), full transcript, or verbal description of what happened.

Extract: attendees (names, titles), call type (discovery/demo/negotiation/check-in), key discussion points, customer priorities stated, objections/concerns raised, competitor mentions, action items (with owners), agreed next steps, deal impact signals.

**Gate**: Key discussion points identified. Action items extracted with owners.

**Phase 2: STRUCTURE** -- Organize into internal summary.

Produce: Call Summary header (company, date, attendees, type), Key Discussion Points, Customer Priorities, Objections/Concerns (with status: addressed/open), Competitive Intel, Action Items (table: owner | action | due date), Next Steps, Deal Impact assessment.

**Gate**: Summary structured. All action items have owners and dates.

**Phase 3: DRAFT** -- Write customer follow-up email.

Rules: plain text only (no markdown, no bold, no headers). Concise. Reference key discussion points. List commitments made. State clear next step with timeline. Professional but not stiff.

Only include commitments the user explicitly stated were made. Do not infer or invent commitments from the summary. If uncertain, ask.

**Gate**: Email is plain text. Under 200 words. Next step stated with date.

**Phase 4: DELIVER** -- Output both artifacts.

Sections: Internal Summary (full structured summary for your team), Customer Follow-Up Email (ready to send), CRM Update Suggestions (stage change, next step field, activity log).

---

## Workflow: RESEARCH

**Framework**: PARSE -> SEARCH -> SYNTHESIZE -> DELIVER

**Phase 1: PARSE** -- Identify the research target.

Classify: company research, person research, competitor research, or pre-meeting research. Extract: company name/domain, person name and title, research purpose.

**Gate**: Target identified. Research type classified.

**Phase 2: SEARCH** -- Systematic web research.

Company searches: homepage, news (last 90 days), funding, careers, product, customers. Person searches: LinkedIn profile, background, recent activity. Domain-based: extract company from domain, then run company searches.

**Gate**: Sources gathered. No fabricated details.

**Phase 3: SYNTHESIZE** -- Build the research profile.

Produce: Quick Take (2-3 sentences: who they are, why they might need you, best angle), Company Profile (table), Recent News (with relevance), Hiring Signals, Key People (with talking points), Qualification Signals (positive/concerns/unknown), Recommended Approach (entry point, opening hook, discovery questions).

Never state employee count, revenue, or funding as fact unless found in search results. Mark uncertain data points explicitly.

**Gate**: Profile complete. All facts sourced. Gaps noted.

**Phase 4: DELIVER** -- Output the research brief.

Sections: Quick Take, Company Profile (table), Recent News, Hiring Signals, Key People (with talking points), Qualification Signals, Recommended Approach, Sources.

---

## LLM Failure Modes

See `references/llm-sales-failure-modes.md` for the complete failure mode catalog (fabricated company details, invented history, generic outreach, hallucinated financials, optimistic forecasting, template personalization, fake competitor claims, over-promising, ignoring disqualification signals). Universal failure modes in `skills/shared-patterns/llm-domain-failure-modes-base.md`.

---

## Output Format Specifications

### All Modes

- Structured markdown with clear headers
- Tables for structured data (company profiles, deal lists, scoring)
- Bullet lists for action items and recommendations
- No motivational framing ("Great news!" / "Exciting opportunity!")
- No atmosphere text. Every sentence carries information.

### Customer-Facing Output (Outreach, Follow-Up Emails)

- Plain text only. No markdown formatting.
- Under 200 words for follow-ups, under 150 for cold outreach.
- Short paragraphs (2-3 sentences max).
- One clear CTA per message.

### Internal Output (Summaries, Analysis, Forecasts)

- Use tables for multi-dimensional data.
- Include "Sources" or "Based On" attribution for factual claims.
- Flag uncertainty explicitly: "Not confirmed" / "Estimate" / "Based on [source]".
