---
name: qualification-scorer
description: "Use when scoring leads, qualifying prospects, prioritizing pipeline, deciding which accounts to pursue, or building a lead scoring model. Triggers: 'score this lead', 'qualify this prospect', 'is this a good lead', 'lead scoring', 'prioritize my pipeline', 'qualification framework'."
version: 1.0.0
---

# Qualification Scorer

Score and qualify leads using a multi-axis framework. Takes a lead or list of leads, evaluates them on four axes (Fit, Timing, Access, Intent), classifies them into tiers, and produces actionable next steps for each.

## Tools Used

- **Read** — load `docs/icp.md`, `docs/signals/*.md`, `docs/accounts/*.md`, CSV files
- **Write** — output scored results to `docs/pipeline/scored-leads.md`
- **Glob** — discover existing docs that can enrich scoring

## Steps

### Step 1: Context Loading

Check for existing files that inform scoring. Run these searches:

```
Glob: docs/icp.md
Glob: docs/signals/*.md
Glob: docs/accounts/*.md
```

- If `docs/icp.md` exists, read it and extract ICP criteria (company size, industry, stage, budget range). Use these criteria to auto-score the Fit axis.
- If `docs/signals/*.md` files exist, read them and extract known trigger events, intent data, and timing indicators. Use these to inform Timing and Intent scoring.
- If `docs/accounts/*.md` files exist, read them and cross-reference any leads against known account briefs for enrichment.
- If NONE of these files exist, ask the user:

> I don't see an ICP definition at `docs/icp.md`. Before I can score leads accurately, I need to understand your ideal customer. Tell me:
> 1. What company size do you target? (employee count or revenue range)
> 2. What industries or verticals?
> 3. What company stage? (seed, Series A, growth, enterprise)
> 4. What budget range per month are you selling into?

Store the user's answers as the working ICP definition for this scoring session.

### Step 2: Lead Input

Ask the user how they want to provide leads:

> How would you like to provide the leads to score?
>
> **A.** Paste a list (company name, contact name, title — one per line)
> **B.** Single lead deep-dive (I'll ask you detailed questions about one prospect)
> **C.** Give me a CSV file path to read

Handle each input mode:

- **Option A (list):** Parse the pasted text. Extract company name, contact name, and title for each row. Tolerate messy formatting (comma-separated, tab-separated, or line-by-line).
- **Option B (single lead):** Ask follow-up questions about the lead: company name, contact name and title, company size, industry, any recent events you know of, how you found them, any engagement so far.
- **Option C (CSV):** Read the file at the given path. Map columns to company, contact, and title. If column names are ambiguous, show the header row and ask the user to confirm the mapping.

### Step 3: Scoring Framework

For each lead, evaluate four axes. Score each axis 1 through 5.

#### Fit (1-5) — Does this company match the ICP?

| Score | Criteria |
|-------|----------|
| 5 | Perfect match: right size, industry, stage, and budget |
| 4 | Strong match: 3 of 4 ICP criteria match |
| 3 | Partial match: 2 of 4 ICP criteria match |
| 2 | Weak match: 1 criterion matches |
| 1 | No match: wrong segment entirely |

If `docs/icp.md` was loaded, auto-score Fit by comparing the lead's known attributes against the ICP criteria. If information is missing, default to 3 and flag it for user review.

#### Timing (1-5) — Is now the right moment?

| Score | Criteria |
|-------|----------|
| 5 | Active buying event: demo requested, RFP published, contract with competitor ending |
| 4 | Strong trigger: just raised funding, new CXO hired, hiring spree in relevant roles |
| 3 | Moderate trigger: product launch, market shift, expansion announcement |
| 2 | Weak trigger: general growth, no urgency indicators |
| 1 | No trigger: stable company, no change signals detected |

If `docs/signals/*.md` files were loaded, cross-reference leads against known signals to auto-score. Otherwise, default to 2 and flag for user input.

#### Access (1-5) — Can you reach the decision maker?

| Score | Criteria |
|-------|----------|
| 5 | Warm introduction available: mutual connection, past relationship, shared investor |
| 4 | Second-degree connection: shared community, alumni network, conference overlap |
| 3 | Cold but reachable: email address known, LinkedIn profile open, active on social media |
| 2 | Cold and gated: no email found, LinkedIn restricted, requires research |
| 1 | Unreachable: no contact info, heavy gatekeeper, not present on social platforms |

IMPORTANT: Do NOT auto-score Access. Default to 2 for all leads and explicitly ask the user to review. The user almost always knows more about their access than any data source can reveal.

#### Intent (1-5) — How much buying intent is visible?

| Score | Criteria |
|-------|----------|
| 5 | Explicit intent: requested a demo, responded to outreach, asked for pricing |
| 4 | High intent: reviewing competitors, published a pain point, attended your webinar |
| 3 | Moderate intent: hiring for a related role, engaging with your content |
| 2 | Low intent: company matches ICP but no engagement yet |
| 1 | No intent: no visible interest or engagement signals |

If signal files were loaded, use them to inform Intent scoring. Otherwise, default to 2 and flag for user review.

### Step 4: Composite Scoring

Calculate the composite score and assign a tier for each lead.

**Score** = Fit + Timing + Access + Intent (maximum 20)

**Tier Classification:**

| Score Range | Tier | Recommended Action |
|-------------|------|-------------------|
| 17-20 | HOT | Reach out within 24 hours. Top priority. Personalize heavily. |
| 13-16 | WARM | Add to active outreach sequence. Nurture with value-first touchpoints. |
| 9-12 | COLD | Monitor for trigger events. Build relationship passively. Revisit monthly. |
| Below 9 | PARK | Add to quarterly review list. Not ready now. Check back in 90 days. |

For each lead, generate a one-line recommended action that accounts for their specific score distribution. Examples:
- Fit=5, Access=1 -> "Find a warm intro path before reaching out — this is a perfect-fit account stuck behind a cold wall."
- Fit=3, Timing=5 -> "Timing is urgent but fit is uncertain. Validate ICP match before investing outreach effort."
- Fit=5, Timing=5, Access=5, Intent=1 -> "Everything lines up except intent. Test with a highly relevant value-drop to see if they bite."

### Step 5: Interactive Review

Present the scores to the user in a table. Then ask:

> Here are the scores for your leads. Do these look right?
>
> **Pay special attention to Access and Intent** — you often know things about these that I can't see from the data. Tell me if any scores should be adjusted.
>
> Reply with adjustments like: "Acme Corp Access should be 4 — I have a mutual connection through our investor" or "All looks good."

If the user provides adjustments:
1. Update the scores for the specified leads.
2. Recalculate composite scores and tier classifications.
3. Regenerate recommended actions if the tier changed.
4. Show the updated table.

Repeat until the user confirms the scores are accurate.

### Step 6: Output

Write the final scored results to `docs/pipeline/scored-leads.md`. Create the directory if it does not exist.

Use this format:

```markdown
# Scored Leads

> Generated: {YYYY-MM-DD} | Leads scored: {count}

## Summary

| Tier | Count |
|------|-------|
| HOT  | {n}   |
| WARM | {n}   |
| COLD | {n}   |
| PARK | {n}   |

## All Leads

| Company | Contact | Title | Fit | Timing | Access | Intent | Score | Tier | Recommended Action |
|---------|---------|-------|-----|--------|--------|--------|-------|------|--------------------|
| {data}  | {data}  | {data}| {n} | {n}    | {n}    | {n}    | {n}   | {tier}| {action}          |

(Sorted by score, highest first.)

## HOT Lead Engagement Plans

### {Company Name} — Score: {n}/20

- **Why HOT:** {brief explanation of what makes this lead top-tier}
- **Channel:** {recommended outreach channel — email, LinkedIn, warm intro, phone}
- **Angle:** {what to lead with — the specific pain point, trigger event, or connection to reference}
- **Timing:** {when to reach out and why — e.g., "This week. Their contract with X expires in 30 days."}
- **First touch:** {draft of the opening line or subject line}

(Repeat for each HOT lead.)
```

The table MUST be formatted as a clean Markdown table that can be copy-pasted directly into a spreadsheet (Google Sheets, Excel) or CRM import. One row per lead, pipe-delimited, no extra formatting.

### Step 7: Pipeline Dashboard

After writing the file, present a quick-reference dashboard to the user in the conversation:

1. **Tier Distribution** — how many leads in each tier, with percentages.

2. **Weakest Axis** — identify which scoring axis has the lowest average across all leads. Provide a specific recommendation. Examples:
   - "Your pipeline has a Timing gap — most leads scored 1-2 on Timing. Consider adding trigger event monitoring (job changes, funding rounds, new hires) to catch leads at the right moment."
   - "Access is your bottleneck — 70% of leads scored 2 or below. Focus on building warm intro paths through communities, events, or mutual connections before outreach."
   - "Intent is weak across the board. Most leads are ICP-fit but haven't engaged yet. Run a content campaign or webinar to generate intent signals before sequencing."

3. **Top 3 This Week** — name the three leads to focus on this week, with a one-sentence reason for each.

## Key Rules

1. Scoring MUST be interactive. Always present scores and let the user adjust before finalizing. Never write the output file until the user confirms scores.
2. Do NOT auto-score Access or Intent without asking the user for input. Default them conservatively (2) and explicitly request user review. Users always know more about their relationships and engagement history than data can show.
3. If `docs/icp.md` exists, use it to auto-score Fit. Do not ask the user to re-describe their ICP when a definition already exists.
4. If `docs/signals/*.md` files exist, use them to auto-score Timing and Intent. Cross-reference lead names and company names against signal data.
5. CRM-ready output. The Markdown table must be directly pasteable into a spreadsheet. No merged cells, no multi-line entries within a row, no special formatting beyond pipe-delimited columns.
6. Create `docs/pipeline/` directory if it does not already exist. Never overwrite without confirmation — if `scored-leads.md` already exists, ask the user: "A previous scored leads file exists. Overwrite it or append to it?"
7. For single-lead deep-dives (Option B), still follow the full framework but go deeper on each axis with follow-up questions.
8. When scoring a list of more than 10 leads, present scores in batches of 10 for review to keep the interaction manageable.
