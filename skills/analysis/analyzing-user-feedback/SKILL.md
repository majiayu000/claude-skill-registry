---
name: "analyzing-user-feedback"
description: "Analyze user/customer feedback and produce a User Feedback Analysis Pack (source inventory, normalized feedback table, taxonomy/codebook, themes + evidence, recommendations, and feedback loop). Use for voice of customer, feature request analysis, support ticket synthesis, churn reason synthesis, and survey open-ends."
---

# Analyzing User Feedback

## Scope

**Covers**
- Aggregating and normalizing feedback from multiple channels (support, sales, research, reviews, surveys, usage signals)
- Turning raw feedback into **themes with evidence** and **actionable recommendations**
- Identifying **friction / reasons users won’t use the product** (not just validation)
- Producing a repeatable **feedback loop** (cadence, owners, and handoffs)

**When to use**
- “Synthesize our user feedback into themes and actions.”
- “Analyze support tickets / feature requests for the top issues.”
- “Create a voice-of-customer report for <area> in the last <time window>.”
- “Summarize churn reasons / cancellation feedback.”
- “Cluster survey open-ends into insights and recommendations.”

**When NOT to use**
- You need to collect new feedback first (use `conducting-user-interviews` / `designing-surveys`)
- You need backlog prioritization as the primary output (use `prioritizing-roadmap`)
- You need a PRD/spec for a chosen solution (use `writing-prds` / `writing-specs-designs`)
- You only need to respond to individual tickets (support workflow, not synthesis)

## Inputs

**Minimum required**
- Product area / workflow to analyze (or “all product”)
- Time window + volume expectations (e.g., “last 90 days”, “~2k tickets”)
- Feedback sources available (tickets, interviews, sales notes, reviews, surveys, community, logs)
- The decision this analysis should inform (roadmap theme, launch readiness, onboarding fixes, messaging, quality)
- Any segmentation that matters (ICP, persona, plan tier, lifecycle stage)
- Constraints: privacy/PII rules, internal-only vs shareable, deadline/time box

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If data access is limited, proceed using a **small representative sample** and label confidence/limitations.
- Do not request secrets. If feedback contains PII, ask for **redacted excerpts** or aggregated fields only.

## Outputs (deliverables)

Produce a **User Feedback Analysis Pack** in Markdown (in-chat; or as files if requested):

1) **Context snapshot** (scope, decision, time window, segments, constraints)
2) **Source inventory + sampling plan** (what’s included/excluded; why)
3) **Taxonomy + codebook** (tags, definitions, and coding rules)
4) **Normalized feedback table** (tagged items; links/IDs if available; no PII)
5) **Themes & evidence report** (top themes, representative quotes, frequency/severity, confidence)
6) **Recommendations** (actions, owners/time horizon if known, expected impact, open research questions)
7) **Feedback loop plan** (cadence, stakeholders, how engineering participates, how insights are stored)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Intake + decision framing
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm the decision, scope, time window, audience, and constraints. Define what “good” looks like.
- **Outputs:** Context snapshot.
- **Checks:** A stakeholder can answer: “What decision will this analysis change?”

### 2) Inventory sources + define the sampling plan
- **Inputs:** List of sources + access constraints.
- **Actions:** Create a source inventory, decide inclusions/exclusions, and pick a sample strategy (random, stratified, top-volume buckets).
- **Outputs:** Source inventory + sampling plan.
- **Checks:** Sampling plan covers the highest-volume and highest-risk segments (or explicitly explains why not).

### 3) First-pass read-through (open coding)
- **Inputs:** Sampled feedback items.
- **Actions:** Read/annotate items manually to surface what’s “wrong” and why users struggle or churn. Write raw notes before building categories.
- **Outputs:** Initial codes/notes + candidate themes list.
- **Checks:** Notes capture **rejection reasons** and **friction**, not just feature ideas.

### 4) Build the taxonomy + codebook
- **Inputs:** Initial codes; product context.
- **Actions:** Define a tagging schema (topic, lifecycle stage, severity, user segment, root cause, sentiment). Write clear tag definitions and rules.
- **Outputs:** Taxonomy + codebook.
- **Checks:** Two people could tag the same item similarly using the codebook.

### 5) Normalize and tag the feedback table
- **Inputs:** Raw items; taxonomy/codebook.
- **Actions:** Create a normalized table, tag each item, and capture evidence fields (source, date, segment, verbatim excerpt, link/ID).
- **Outputs:** Normalized feedback table (tagged).
- **Checks:** No PII; every row has at least 1 primary theme tag + a severity/impact signal.

### 6) Synthesize themes + quantify carefully
- **Inputs:** Tagged table.
- **Actions:** Summarize top themes, quantify frequency by segment/source, identify severity and “why it happens”, and call out unknowns/bias.
- **Outputs:** Themes & evidence report with confidence levels.
- **Checks:** Each theme includes representative evidence (quotes/examples) and is not purely speculative.

### 7) Translate into actions + learning plan
- **Inputs:** Themes report; constraints.
- **Actions:** Convert themes into actions (bugs, UX fixes, comms, product bets) and open questions (what to research next). Tie each action to evidence and expected impact.
- **Outputs:** Recommendations + learning plan.
- **Checks:** Recommendations are concrete enough to execute next sprint/quarter (clear owner/time horizon if known).

### 8) Share out + establish the feedback loop + quality gate
- **Inputs:** Draft pack.
- **Actions:** Propose the share-out format (doc + review). Define cadence, owners, and storage (where insights live). Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps.
- **Outputs:** Final User Feedback Analysis Pack.
- **Checks:** Pack is shareable as-is; limitations are explicit; follow-up actions are scheduled.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (support tickets):** “Analyze the last 60 days of onboarding-related tickets. Output a User Feedback Analysis Pack and top 10 recommended fixes.”  
Expected: source inventory + sampling, taxonomy, tagged table, themes with quotes, and ranked actions.

**Example 2 (survey + reviews):** “Synthesize survey open-ends and app store reviews for our new pricing change. What are the biggest friction points and why?”  
Expected: themes split by source/segment, severity signals, and recommendations (incl. messaging/UX changes).

**Boundary example:** “Read all our feedback and tell us what to build next.”  
Response: ask for scope/time window/decision + a sample dataset; otherwise produce a sampling plan + a minimal first-pass synthesis with explicit limitations.

