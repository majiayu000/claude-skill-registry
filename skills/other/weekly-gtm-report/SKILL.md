---
name: weekly-gtm-report
description: "Use when generating weekly GTM performance reports, summarizing pipeline activity, reviewing outreach metrics, or creating executive updates. Triggers: 'weekly report', 'GTM report', 'pipeline review', 'weekly update', 'outreach summary', 'Friday report'."
version: 1.0.0
---

# Weekly GTM Report

Generate a structured weekly GTM performance report by reading data from the local `docs/` directory and optional CRM exports. Produces an executive-ready summary with metrics, highlights, week-over-week trends, and recommended actions.

## Tools Used

- **Read** — load pipeline data, signal reports, account briefs, sequence configs, battlecards, meeting prep notes, CRM CSV exports, and previous reports
- **Write** — save the weekly report and update the reports index
- **Glob** — discover available data files across `docs/` subdirectories
- **Bash** — date calculations (week number, date ranges)

## Methodology

Follow these steps in order. Do not skip steps. Do not fabricate metrics. If data is missing for a section, include the section with a "No data available" note and a suggestion for how to populate it.

### Step 1: Data Collection

Ask the user:

> What week is this report for? (default: current week)

Use Bash to compute the ISO week number and Monday-to-Friday date range for the target week.

Then scan the `docs/` directory for available data sources. Run these searches:

```
Glob: docs/pipeline/scored-leads.md
Glob: docs/signals/*.md
Glob: docs/accounts/*.md
Glob: docs/sequences/*.md
Glob: docs/battlecards/*.md
Glob: docs/meeting-prep/*.md
Glob: docs/reports/week-*.md
```

Also ask the user:

> Do you have a CRM export CSV for this week? If so, provide the file path.

Read every file that exists. For each data source found, summarize what was loaded (file count and date range of contents). For each data source NOT found, note it as unavailable. Present the summary to the user before proceeding:

> **Data loaded:**
> - Pipeline: scored-leads.md (12 leads, last updated 2026-03-07)
> - Signals: 4 signal reports found
> - Sequences: not found
> - Battlecards: 3 battlecards found
> - Meeting prep: not found
> - Previous reports: 2 found (latest: week-2026-W10)
>
> I'll build the report from what's available. Missing sections will note what data is needed.

### Step 2: Pipeline Summary

**Requires:** `docs/pipeline/scored-leads.md`

If the pipeline file exists, extract and present:

1. **Total leads by tier** — count of HOT, WARM, COLD, and PARK leads
2. **Movement since last report** — compare against the previous week's report (if one exists in `docs/reports/`). Identify leads that were upgraded, downgraded, newly added, or closed/removed
3. **Pipeline velocity** — if date-added or last-scored timestamps exist, calculate average days a lead has spent in its current tier
4. **Top 5 hottest leads** — the five highest-scoring leads with their composite scores, strongest signal, and recommended next action

Format as a table:

| Tier | Count | Change vs Last Week |
|------|-------|---------------------|
| HOT  | {n}   | {+/- or "new"}      |
| WARM | {n}   | {+/- or "new"}      |
| COLD | {n}   | {+/- or "new"}      |
| PARK | {n}   | {+/- or "new"}      |

**If not found:** Note "No pipeline data available. Run the Qualification Scorer skill to generate `docs/pipeline/scored-leads.md`."

### Step 3: Outreach Activity

**Requires:** `docs/sequences/*.md` or CRM export CSV

If sequence files or CRM data exist, extract:

1. **Active sequences** — list each sequence by name, status (active/paused/completed), and contacts enrolled
2. **Messages sent by channel** — email, LinkedIn, phone. Aggregate totals for the week
3. **Response rates** — replies received divided by messages sent, broken down by channel if data permits
4. **Highlights** — best performing sequence (highest response rate) and best individual response (most promising reply or conversion)

Format as a table:

| Channel  | Sent | Replies | Response Rate |
|----------|------|---------|---------------|
| Email    | {n}  | {n}     | {n}%          |
| LinkedIn | {n}  | {n}     | {n}%          |
| Phone    | {n}  | {n}     | {n}%          |

**If not found:** Note "No outreach data available. Run the Outreach Sequence Builder skill to create sequences at `docs/sequences/`, or provide a CRM export CSV."

### Step 4: Signals Detected

**Requires:** `docs/signals/*.md`

If signal files exist, extract:

1. **New signals this week** — filter signal reports to those with detection dates within the target week. Present as a table:

| Company | Signal Type | Date | Score | Source |
|---------|-------------|------|-------|--------|
| {name}  | {type}      | {date}| {n}/20 | [{source}]({url}) |

2. **Signal trends** — compare against previous weeks if older signal files exist. Are funding signals increasing? Hiring signals? Competitor churn? Note any shifts
3. **Recommended actions** — for the top 3 highest-scoring new signals, provide a specific next step (e.g., "Acme Corp raised Series B last Tuesday. Reach out to their new VP Sales this week with a congrats + value angle.")

**If not found:** Note "No signal data available. Run the Signal Scanner skill to populate `docs/signals/`."

### Step 5: Meetings and Research

**Requires:** `docs/meeting-prep/*.md` and/or `docs/accounts/*.md`

If meeting prep or account files exist, extract:

1. **Meetings held this week** — list each meeting with company name, attendees (if noted), and date
2. **New accounts researched** — list account briefs created or updated this week (based on file modification dates)
3. **Key takeaways** — pull any outcomes, decisions, or insights noted in meeting prep files
4. **Follow-up actions outstanding** — extract any action items, next steps, or commitments mentioned in meeting notes that have not been marked complete

Format as a table:

| Date | Company | Type | Key Takeaway | Follow-Up |
|------|---------|------|--------------|-----------|
| {date} | {name} | {meeting/research} | {one line} | {action item} |

**If not found:** Note "No meeting or account research data available. Use the Meeting Prep Brief skill to generate `docs/meeting-prep/` files, or the Account Research Brief skill for `docs/accounts/`."

### Step 6: Competitive Updates

**Requires:** `docs/battlecards/*.md`

If battlecard files exist, check their modification dates against the target week:

1. **Updated this week** — list battlecards that were modified during the report week, with a one-line summary of what changed
2. **Competitor moves** — extract any new competitor intelligence noted in updated battlecards (pricing changes, product launches, customer wins/losses, funding)
3. **Freshness check** — list all battlecards with their last-modified date. Flag any that have not been updated in over 30 days as "overdue for refresh"

Format as a table:

| Competitor | Last Updated | Status | Notable Change |
|------------|--------------|--------|----------------|
| {name}     | {date}       | {fresh/stale/updated this week} | {one line or "none"} |

**If not found:** Note "No battlecard data available. Run the Competitive Battlecard Generator skill to create `docs/battlecards/`."

### Step 7: Key Metrics Dashboard

Aggregate all available data into a single metrics summary. Only include metrics where data exists. Do not fabricate numbers.

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Leads in pipeline | {n} | {n or "—"} | {+/- or "—"} |
| HOT leads | {n} | {n or "—"} | {+/- or "—"} |
| New leads added | {n} | {n or "—"} | {+/- or "—"} |
| Signals detected | {n} | {n or "—"} | {+/- or "—"} |
| Signals acted on | {n} | {n or "—"} | {+/- or "—"} |
| Messages sent | {n} | {n or "—"} | {+/- or "—"} |
| Replies received | {n} | {n or "—"} | {+/- or "—"} |
| Overall response rate | {n}% | {n or "—"}% | {+/- or "—"} |
| Meetings held | {n} | {n or "—"} | {+/- or "—"} |
| Meetings booked (next week) | {n} | {n or "—"} | {+/- or "—"} |
| Accounts researched | {n} | {n or "—"} | {+/- or "—"} |
| Pipeline value | ${n} | ${n or "—"} | {+/- or "—"} |

For the "Last Week" and "Change" columns, read the most recent previous report from `docs/reports/` to pull comparison values. If no previous report exists, use "—" for all comparison fields and note "First report — no baseline available."

### Step 8: Recommendations

Based on all available data, generate four analysis sections. Be specific. Reference actual companies, signals, and numbers from the data. Do not provide generic advice.

#### What's Working

Identify 2-3 things that are performing well this week. Examples:
- "Email response rate hit 12% this week, up from 8% — the new subject line formula from Sequence 3 is outperforming."
- "Signal Scanner is surfacing high-quality leads: 3 of 5 new signals scored HOT."

#### What Needs Attention

Identify 2-3 areas that require focus. Examples:
- "4 WARM leads have been sitting at WARM for 3+ weeks with no tier movement. Risk of going stale."
- "Battlecards for Competitor X haven't been updated in 45 days. They launched a new pricing tier last week."

#### 3 Actions for Next Week

Provide exactly three specific, concrete actions. Each must reference a real data point from the report. Format:

1. **{Action}** — {Why, referencing specific data}
2. **{Action}** — {Why, referencing specific data}
3. **{Action}** — {Why, referencing specific data}

#### Resource Allocation

Based on the data, suggest where to spend time next week. Divide a hypothetical 40-hour week across GTM activities:

| Activity | Hours | Rationale |
|----------|-------|-----------|
| {activity} | {n}h | {why} |
| {activity} | {n}h | {why} |
| {activity} | {n}h | {why} |
| {activity} | {n}h | {why} |

### Step 9: Output

Write the report to `docs/reports/week-{YYYY-WNN}.md` where `{YYYY-WNN}` is the ISO year and week number (e.g., `week-2026-W11.md`). Create the `docs/reports/` directory if it does not exist.

Use this structure:

```markdown
# Weekly GTM Report — Week {WNN} ({Mon date} to {Fri date})

> Generated: {YYYY-MM-DD} | Report: week-{YYYY-WNN} | Generated by: Weekly GTM Report v1.0.0

## Executive Summary

- {3-5 bullet points highlighting the most important things from this week}

---

## Pipeline

{Content from Step 2}

## Outreach Activity

{Content from Step 3}

## Signals

{Content from Step 4}

## Meetings & Research

{Content from Step 5}

## Competitive Updates

{Content from Step 6}

---

## Key Metrics

{Table from Step 7}

---

## Recommendations

### What's Working
{Content from Step 8}

### What Needs Attention
{Content from Step 8}

### Actions for Next Week
{Content from Step 8}

### Resource Allocation
{Content from Step 8}

---

*Next report: week-{YYYY-WNN+1}*
```

After writing the report, update `docs/reports/README.md`. If the file does not exist, create it. If it exists, prepend the new entry to the top of the report list.

```markdown
# Weekly GTM Reports

| Week | Date Range | Report | Highlights |
|------|------------|--------|------------|
| W{NN} | {Mon} - {Fri} | [week-{YYYY-WNN}](week-{YYYY-WNN}.md) | {one-line summary} |
| ... | ... | ... | ... |
```

## Key Rules

1. **Never fabricate metrics.** Every number in the report must come from a file in `docs/` or from user-provided data. If data does not exist for a section, write "No data available" and suggest which skill to run to generate it.
2. **The report must work with minimal data.** Even if only `docs/pipeline/scored-leads.md` exists, produce a useful report. Even if only `docs/signals/` has data, produce a useful report. Populate what you can, mark the rest as unavailable.
3. **Always include all sections.** Do not drop sections that have no data. Include them with a "No data available" note so the user sees the full picture of what they could be tracking.
4. **Executive-readable.** No jargon, no acronyms without definition on first use, no tool-specific language. A VP of Sales who has never seen this system should understand the report.
5. **Week-over-week comparisons are mandatory when previous reports exist.** Read the most recent report from `docs/reports/` and compute deltas for every metric. If this is the first report, note "First report — no baseline available" and skip comparisons.
6. **Check for existing reports before writing.** Use Glob to check `docs/reports/` for a report matching the target week. If one already exists, ask the user: "A report for this week already exists. Overwrite it or create a supplemental update?"
7. **Ask the user to confirm the week before proceeding.** Never assume the target week without confirmation.
8. **Keep it generic.** This skill works for any GTM team. Do not reference specific internal tools, databases, or vendor accounts.
