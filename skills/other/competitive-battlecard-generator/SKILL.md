---
name: competitive-battlecard-generator
description: "Use when analyzing competitors, creating sales battlecards, building competitive positioning, preparing for competitive deals, or updating competitive intelligence. Triggers: 'battlecard for [competitor]', 'competitive analysis of [competitor]', 'how do we beat [competitor]', 'compare us to [competitor]', 'competitive intel', 'win against [competitor]'."
version: 1.0.0
---

# Competitive Battlecard Generator

Generate comprehensive, actionable competitive battlecards using WebSearch. Each battlecard gives sales teams the intelligence they need to win competitive deals — competitor strengths, weaknesses, objection handling, and trap questions, all grounded in real research. Can batch-process up to 5 competitors in a single run.

---

## Activation

When the user triggers this skill, follow the steps below **in order**. Do NOT skip the input step. Do NOT produce a battlecard without gathering context first.

---

## Step 1 — Collect Input

Ask the user for these inputs **all at once** in a numbered list:

```
I need some context before building your battlecard(s). Answer these questions:

1. What is your company name and what do you do? (one sentence)
2. Which competitor(s) do you want a battlecard for? (1-5 names)
3. (Optional) What are your key differentiators? (3-5 bullets)
4. (Optional) Any known weaknesses of the competitor(s)?
5. (Optional) Are you usually compared to them? In what context?
```

**Rules for this step:**
- Wait for the user to respond before proceeding. Do NOT generate placeholder answers.
- Only question 1 and 2 are required. If either is missing, ask again.
- If the user provides more than 5 competitors, tell them you will batch the first 5 and they can run the skill again for the rest.
- If the user provides optional inputs, use them to sharpen the analysis. If they skip optionals, proceed without them — you will research independently.

---

## Step 2 — Competitor Overview

For each competitor, run 2-3 WebSearch queries to establish a factual baseline.

**Search patterns:**
- `"{competitor} what does it do"` or `"{competitor} company overview"`
- `"{competitor} funding crunchbase"` or `"{competitor} series funding investors"`
- `"{competitor} customers case studies"` or `"{competitor} pricing"`

**Gather these data points:**

| Field | Description |
|---|---|
| **What they do** | Their positioning statement — how they describe themselves (from their homepage or about page) |
| **Founded** | Year founded |
| **HQ** | Headquarters location |
| **Company size** | Employee count range |
| **Funding** | Total raised, last round, key investors (for private companies) |
| **Key customers** | Named logos from case studies, website, or press releases (3-8 names) |
| **Target market** | Who they sell to — company size, industry, buyer persona |
| **Pricing model** | Pricing tiers, per-seat, usage-based, etc. If not publicly available, write "Pricing not publicly available — ask during discovery" |
| **Recent news** | 1-3 headlines from the last 90 days with source URLs |

**Rules:**
- If any data point is not findable after searching, write "Not found." Never fabricate company data.
- Always include the source URL for each data point in the Sources section.

---

## Step 3 — Their Pitch

For each competitor, run 1-2 WebSearch queries to document their messaging.

**Search patterns:**
- `"{competitor}"` (homepage messaging)
- `"{competitor} why choose us"` or `"{competitor} vs alternatives"`

**Gather:**

| Field | Description |
|---|---|
| **Main value proposition** | Their primary claim — the one sentence from their homepage or hero section |
| **Top 3-5 claims** | The specific promises they make (speed, accuracy, cost savings, ease of use, etc.) |
| **How they differentiate** | What they say makes them different from competitors |
| **Key messaging themes** | Recurring themes across their marketing (innovation, simplicity, enterprise-grade, etc.) |
| **Awards or recognition** | Analyst reports (Gartner, Forrester), G2 badges, industry awards they highlight |

---

## Step 4 — Strengths Analysis

Honestly assess what the competitor does well. A battlecard that ignores competitor advantages is useless — sales reps will lose credibility if they dismiss a competitor that the prospect already likes.

For each competitor, run 1-2 WebSearch queries.

**Search patterns:**
- `"{competitor} reviews G2"` or `"why I chose {competitor}"`
- `"{competitor} case study results"`

**Document:**

| Field | Description |
|---|---|
| **What they do well** | Objective strengths — features, UX, integrations, market position |
| **Where they have an advantage over you** | Be honest. If they are better at something, say so. This helps reps prepare instead of getting blindsided. |
| **What their customers love** | Pull from reviews, testimonials, and case studies |
| **Why companies choose them** | The top 2-3 reasons buyers pick them over alternatives |

---

## Step 5 — Weaknesses Analysis

Use WebSearch aggressively to find real complaints, criticisms, and gaps. This is the highest-value section of the battlecard.

Run 3-4 WebSearch queries per competitor:

**Search patterns:**
- `"{competitor} reviews complaints"` or `"{competitor} negative reviews G2 Capterra"`
- `"{competitor} reddit problems"` or `"{competitor} reddit complaints"`
- `"{competitor} issues limitations"` or `"switching from {competitor}"`
- `"{competitor} vs"` (often surfaces comparison articles that highlight weaknesses)

**Organize weaknesses into categories:**

| Category | What to look for |
|---|---|
| **Feature gaps** | Missing capabilities that buyers frequently ask about |
| **Pricing complaints** | Too expensive, hidden fees, forced annual contracts, price increases |
| **Support/service issues** | Slow support, poor onboarding, unresponsive account management |
| **Implementation difficulties** | Long setup times, complex configuration, migration pain |
| **Product quality** | Bugs, downtime, performance issues, outdated UI |
| **Customer churn signals** | People posting about leaving, "alternatives to {competitor}" searches |
| **Scalability concerns** | Breaks at volume, enterprise readiness gaps |

**Rules:**
- Every weakness claim must have a source (URL, review platform, Reddit thread). Never invent criticisms.
- Distinguish between isolated complaints and patterns. A single bad review is an anecdote; five reviews mentioning the same issue is a pattern.

---

## Step 6 — Win/Loss Patterns

Based on all research gathered so far, synthesize win/loss patterns. If the user provided optional inputs in Step 1 (known weaknesses, comparison context), factor those in.

Run 1-2 additional WebSearch queries if needed:

**Search patterns:**
- `"{competitor} vs {your company}"` or `"why I switched from {competitor}"`
- `"{competitor} alternative for {use case}"`

**Document four categories:**

| Category | Description |
|---|---|
| **When you WIN against them** | Conditions, buyer profiles, and use cases where you have the advantage. Be specific: company size, industry, technical requirements, decision-maker priorities. |
| **When you LOSE to them** | Conditions where they are stronger. Sales reps need to know when they are walking into a tough fight. |
| **Deal killers** | Specific things that make the competitor unbeatable for certain buyers (e.g., "If the buyer needs X integration, they will choose {competitor} every time — we do not support it yet") |
| **Landmine questions** | 3-5 questions that expose the competitor's weaknesses without being negative. These are questions the sales rep can suggest the prospect ask the competitor during their evaluation. |

---

## Step 7 — Objection Handling

For each competitor, create 5-8 objection handling entries. These should cover the most common things a prospect says when they are leaning toward the competitor.

**Format for each entry:**

| They Say | The Truth | We Say |
|----------|-----------|--------|
| {What the prospect or competitor claims} | {The reality behind the claim — factual, sourced where possible} | {Your counter-positioning — conversational tone, not corporate speak} |

**Rules:**
- "They Say" should be phrased as the prospect would say it, not as a formal objection label. Example: "But {competitor} has better integrations" — not "Integration breadth objection."
- "The Truth" must be factual and fair. Acknowledge if the claim has merit, then provide the nuance.
- "We Say" must be conversational. Write it the way a sales rep would actually say it on a call. No jargon, no buzzwords, no corporate positioning statements.
- If you do not have enough information to fill 5 entries, fill what you can and note which objections need input from the user's sales team.

---

## Step 8 — Trap Questions

Write 3-5 questions that a prospect can ask the competitor during their evaluation. These questions are designed to expose the competitor's weaknesses — but they must sound natural, not hostile.

**For each trap question, provide:**

1. **The question** — phrased the way a prospect would naturally ask it
2. **Why it matters** — what this question reveals about the competitor
3. **What a good answer looks like** — if the competitor answers well, they may genuinely be strong here
4. **What a bad answer looks like** — how the competitor will likely dodge, deflect, or struggle

**Rules:**
- Trap questions must never sound loaded or aggressive. They should sound like normal due-diligence questions a smart buyer would ask any vendor.
- Each question should target a different weakness (do not cluster all questions around the same issue).
- Ground each question in a real weakness found in Step 5.

---

## Step 9 — Positioning Statement

For each competitor, write a concise positioning statement that a sales rep can use when the competitor comes up in conversation.

**Three components:**

| Component | What to write |
|---|---|
| **When they come up** | One sentence to acknowledge the competitor without dismissing them. Shows respect and confidence. |
| **How to differentiate** | 2-3 sentences explaining the user's angle — why the user's product is a better choice for certain buyers. Must be specific, not generic "we're better." |
| **When to compete vs. walk away** | One sentence defining when this is a winnable deal vs. when the sales rep should focus elsewhere. |

---

## Step 10 — Output

### Per-Competitor Battlecard: `docs/battlecards/{competitor-name-slug}.md`

The slug is the competitor name lowercased with spaces replaced by hyphens and special characters removed (e.g., "Scale AI" becomes `scale-ai`, "HubSpot" becomes `hubspot`).

Create the `docs/battlecards/` directory if it does not exist.

Use this structure:

```markdown
# {Competitor Name} — Competitive Battlecard

**Generated:** {YYYY-MM-DD}
**Your Company:** {user's company name}
**Refresh Cadence:** Quarterly — battlecards go stale fast. Re-run this skill every 90 days.

---

## Company Details

| Field | Detail |
|---|---|
| **What they do** | {positioning statement} |
| **Founded** | {year} |
| **HQ** | {location} |
| **Employees** | {count or range} |
| **Funding** | {total raised, last round, key investors} |
| **Key Customers** | {logos} |
| **Target Market** | {who they sell to} |
| **Pricing** | {model and tiers, or "Not publicly available"} |

### Recent News
- {headline} — [{source}]({url}) ({date})
- ...

---

## Their Pitch

**Value Proposition:** {main claim}

**Top Claims:**
1. {claim}
2. {claim}
3. {claim}

**Differentiation Angle:** {how they describe what makes them different}

**Messaging Themes:** {recurring themes}

**Awards/Recognition:** {analyst mentions, badges, awards}

---

## Why {Your Company} Wins

### A | {Advantage Category 1}
{Description with proof points. Why the user's product is better in this dimension. Include specific evidence — features, customer quotes, benchmarks.}

### B | {Advantage Category 2}
{Description with proof points.}

### C | {Advantage Category 3}
{Description with proof points.}

---

## Their Strengths (Know What You're Up Against)

{Honest assessment. What they do well, where they have an advantage, what customers love. Sales reps who dismiss competitor strengths lose credibility.}

---

## Their Weaknesses

{Organized by category: feature gaps, pricing complaints, support issues, implementation difficulties, product quality, churn signals. Every claim cited with a source.}

---

## When We Win vs. Lose

| Scenario | Outcome | Why |
|----------|---------|-----|
| {Buyer profile / use case / conditions} | **WIN** | {Why you win in this scenario} |
| {Buyer profile / use case / conditions} | **WIN** | {Why you win in this scenario} |
| {Buyer profile / use case / conditions} | **LOSE** | {Why you lose in this scenario} |
| {Buyer profile / use case / conditions} | **LOSE** | {Why you lose in this scenario} |

**Deal Killers:** {Things that make the competitor unbeatable for certain buyers}

---

## Objection Handling

| They Say | The Truth | We Say |
|----------|-----------|--------|
| "{prospect/competitor claim}" | {reality behind the claim} | "{conversational counter-positioning}" |
| ... | ... | ... |

---

## Trap Questions

1. **"{Natural-sounding question}"**
   - *Why it matters:* {what this question reveals}
   - *Good answer:* {what it looks like if they handle it well}
   - *Bad answer:* {how they will likely dodge or struggle}

2. **"{Natural-sounding question}"**
   - *Why it matters:* ...
   - *Good answer:* ...
   - *Bad answer:* ...

3. ...

---

## Quick Positioning

> **When they come up:** {one sentence to acknowledge them}
>
> **How to differentiate:** {2-3 sentences — your angle}
>
> **Compete or walk away:** {one sentence — when to fight, when to focus elsewhere}

---

## Sources

- [{description}]({url})
- [{description}]({url})
- ...

---

*Last Updated: {YYYY-MM-DD} | Refresh quarterly or when major competitor news breaks.*
```

### Summary File: `docs/battlecards/README.md`

If this file already exists, update it. If not, create it.

```markdown
# Competitive Battlecards

Last updated: {YYYY-MM-DD}

## Competitor Summary

| Competitor | One-Line Summary | Biggest Weakness | When We Win | When We Lose | Battlecard |
|---|---|---|---|---|---|
| {Name} | {What they do in one sentence} | {Top weakness} | {Top win scenario} | {Top loss scenario} | [{name}.md](./{slug}.md) |
| ... | ... | ... | ... | ... | ... |

---

*Refresh quarterly. Run the Competitive Battlecard Generator skill to update or add new competitors.*
```

When updating README.md, merge new competitor entries with any existing rows. If a competitor was previously listed, replace its row with the new data.

---

## Tools

| Tool | Purpose |
|---|---|
| **WebSearch** | Primary tool. Run 10-15 searches per competitor to cover all sections. Batch independent searches into the same message to run in parallel. |
| **Read** | Check if `docs/battlecards/README.md` or existing battlecards already exist. |
| **Write** | Output the battlecard file and update the README. |
| **Glob** | Check `docs/battlecards/` for existing battlecard files to avoid overwriting without warning. |

---

## Rules (Non-Negotiable)

1. **Be honest about competitor strengths.** A battlecard that pretends the competitor has no advantages is worse than useless — it destroys sales rep credibility. Acknowledge what they do well, then show why you still win.
2. **Always cite sources.** Every weakness claim, review quote, and factual assertion must trace back to a URL in the Sources section. No source, no claim.
3. **Trap questions must sound natural.** They should read like normal due-diligence questions a smart buyer would ask any vendor. Never hostile, never loaded.
4. **Objection handling must be conversational.** Write "We Say" entries the way a sales rep would actually talk on a call. No corporate jargon, no buzzword-laden positioning statements.
5. **Never fabricate data.** If WebSearch returns nothing for a data point, write "Not found." Do not invent funding amounts, employee counts, customer names, or review quotes.
6. **Handle pricing honestly.** If pricing is not publicly available, write "Pricing not publicly available — ask during discovery." Do not guess pricing.
7. **Include a refresh date.** Every battlecard must include a "Last Updated" date and a note that battlecards should be refreshed quarterly. Competitive intelligence goes stale fast.
8. **Check for existing battlecards.** Before writing, use Glob to check `docs/battlecards/` for an existing file for this competitor. If one exists, tell the user and ask: "A battlecard for {competitor} already exists (last updated {date}). Do you want to (A) overwrite it with fresh research, or (B) skip this competitor?"
9. **No internal references.** This skill is part of a public playbook. Never reference internal tools, client names, Notion databases, or proprietary infrastructure.
10. **Works universally.** This skill works for any B2B company analyzing any competitor. Do not assume a specific industry, company size, or GTM motion.
11. **Create directories as needed.** If `docs/battlecards/` does not exist, create it before writing files.
12. **Cap at 5 competitors per run.** If the user asks for more than 5, process the first 5 and tell them to run the skill again for the rest. Each competitor requires 10-15 searches — more than 5 in a single run degrades quality.
