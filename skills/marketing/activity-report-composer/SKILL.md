---
name: activity-report-composer
description: "Turn the audit log of work done on a WordPress site into a polished written report. Wraps the v7.1 respira_generate_activity_report MCP tool with six framings: agency client report, case study, internal recap, testimonial draft, build-in-public, personal recap."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: reporting
---

# Activity Report Composer

**Version:** 1.0.0
**Updated:** 2026-05-24
**Category:** reporting
**Status:** stable
**Requires:** Respira for WordPress plugin 7.1+ + MCP server

---

## Description

Turn the audit log of work done on a WordPress site into a polished, written report. This skill wraps the new v7.1 `respira_generate_activity_report` MCP tool, which returns structured data (totals, top tools used, hours saved, cost saved at agency rate, highlights). The skill then walks the agent through writing that data into one of six framings.

The six framings:

1. **Agency client report** — formal, results-focused, addressed to the client
2. **Case study** — third-person narrative for marketing, anonymize-toggle available
3. **Internal recap** — for team standups, terse, what shipped + what's next
4. **Testimonial draft** — first-person, optimized as a customer quote
5. **Build in public** — public-facing, social-media-shaped, what got done this week
6. **Personal recap** — for the operator's own records, no marketing varnish

---

## When to Use

- End of month — generate a client report for billing
- Quarterly review — build-in-public summary for socials
- Pitching a case study to a prospect
- Capturing testimonial language while the work is fresh
- Internal weekly review for an agency team

---

## Trigger Phrases

- "generate a client report"
- "make a monthly report"
- "activity report"
- "compose an activity report"
- "build an agency client report"
- "draft a case study from this site"
- "build-in-public summary"
- "internal recap"
- "what did i ship this month"
- "client billing report"

---

## Execution Workflow

### Step 1 — Confirm site + window

Call `respira_get_active_site`. Ask the user which window to summarize: default is the last 30 days. Common windows: 7 days (weekly), 30 days (monthly), 90 days (quarterly).

### Step 2 — Confirm framing

Ask the user which of the six framings to use. If they don't say, recommend based on the trigger phrase ("client report" → agency client report; "build in public" → build in public framing). Default if unspecified: agency client report.

### Step 3 — Pull the structured data

Call `respira_generate_activity_report` with the window and framing. The tool returns:

```json
{
  "client": "string",
  "window": "30 days",
  "framing": "agency_client_report",
  "hoursSaved": "5.1",
  "costSaved": {"amount": "408", "currency": "EUR"},
  "totals": {"edits": 42, "pages": 14, "snapshots": 27, "rollbacks": 2},
  "topTools": [
    {"name": "respira_update_module", "scope": "write", "n": 14},
    {"name": "respira_extract_builder_content", "scope": "read", "n": 23}
  ],
  "notes": ["Migrated 14 blog posts to /journal/...", "..."]
}
```

### Step 4 — Compose the report in the chosen framing

Write the report using the framing's voice:

**Agency client report** — addressed to the client by name, leads with the headline number (hours saved, cost saved), then the work summary, then next steps. Professional, no informalities.

**Case study** — third-person narrative. "Acme Inc. reduced their content production time by 40% in 30 days using Respira-augmented AI workflows." Anonymize toggle: if enabled, replace the client name with "a B2B SaaS company" or similar. Anonymize all identifying details in the highlights.

**Internal recap** — bullets, no narrative. "42 edits, 14 pages touched, 0 rollbacks. Top time-saver: bulk Divi module updates. Next: ship the pricing page redesign."

**Testimonial draft** — first-person, in the operator's voice, framed as a quote. "In the last 30 days I saved 5 hours of agency time on [client] thanks to Respira's snapshot-first edits. We shipped 14 pages with zero rollbacks."

**Build in public** — punchy, social-shaped. "This week on Respira: 42 edits across 14 client pages, 5 hours saved, 0 rollbacks. The agent took a swing, snapshotted before every change, and not once did I have to undo it. Here's what landed →"

**Personal recap** — terse log entry for the operator's own notes. Date, totals, what got done, what was hard, what's next. No marketing voice.

### Step 5 — Offer three output formats

After the report is composed, ask the user which output they want:

- **Markdown** — for pasting into a doc, Notion, Linear, email
- **Email-ready HTML** — for sending directly through the agency's mail client
- **Social-shaped** — short version for LinkedIn or X (build-in-public + testimonial framings only)

### Step 6 — Save (optional)

Offer to save the report as a custom post type entry on the site (so it shows up in the Activity reports archive). Use `respira_create_custom_post` with `post_type=respira_activity_report` if that CPT exists.

---

## Output template — Agency client report (example)

```markdown
# Activity Report: {client_name} — {window}

**{hoursSaved}h of work saved · €{costSaved} at our standard rate**

## Summary

In the last {window}, {totals.edits} edits landed across {totals.pages} pages on {client_name}'s site. {totals.snapshots} snapshots were captured before any change, and {totals.rollbacks} were rolled back during review.

## What we did

{notes formatted as bullet list}

## Top operations

{topTools formatted as a small table — name, read/write, count}

## Next steps

{agent fills in — could be empty if no obvious next steps, or could reference open work}

---

Prepared by Respira for {client_name} · {date}
```

---

## Anonymization rules (case-study framing only)

If the user selects case-study framing with anonymize ON:

- Replace client name everywhere with industry descriptor ("a B2B SaaS company", "a Lisbon-based design agency", "a multi-location restaurant group")
- Replace specific URLs with `[client website]`
- Replace named pages with generic descriptors ("the pricing page", "the careers section", "a long-form sales landing page")
- Replace named team members with role descriptors ("their head of marketing", "the founder")
- Keep all numbers exact — they are the proof
- Note "Customer data anonymized at customer's request" at the bottom

---

## Hard rules

- Never invent numbers. Every figure in the report comes from the `respira_generate_activity_report` response or from the totals counted in the audit log. If the data is empty, say so — do not pad.
- Never name customers in the build-in-public or social outputs unless the user explicitly OKs it for *this specific report*. Default to "a client" or "an agency I work with."
- The hours-saved + cost-saved numbers in the structured data already factor in the operator's stated rate. Do not multiply or convert them.
- Reports are an output, not a record. They live in the user's Markdown / email / dashboard, not in the audit log itself.

---

## Telemetry

Records: site URL hash, framing chosen, window length, totals from the response, output format selected, success/failure. No report text, no client name, no notes are sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`
