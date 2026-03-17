---
name: batch-review
description: Review multiple content pieces for compliance, brand, and SEO in batch
user-invocable: true
---

You are helping the marketing team review multiple content pieces at once.

Follow these steps:

### Step 1: Get the Content Batch

Ask the user for the content to review. Accept:
- Multiple pasted content pieces (separated by clear markers)
- Directory path containing content files
- List of URLs to audit
- Spreadsheet or CSV with content entries

Also ask which review types to run:
- **Compliance** — DSHEA and FTC check (default: on)
- **Brand** — brand voice scoring (default: on)
- **SEO** — SEO optimization audit (default: on)
- **Pre-publish** — full publication readiness check (default: off)

### Step 2: Process Each Piece

For each content piece, delegate to the appropriate agents:
- brand-validator for compliance and brand scoring
- seo-optimizer for SEO analysis
- pre-publish-agent for publication readiness (if selected)

Track progress: "Reviewing piece 3 of 12..."

### Step 3: Present Batch Summary

Display a summary table:

| # | Title/ID | Compliance | Brand Score | SEO Score | Status |
|---|----------|-----------|-------------|-----------|--------|
| 1 | "Blog: Pre-Workout Guide" | PASS | 85/100 | 72/100 | Ready |
| 2 | "Email: Spring Sale" | FAIL | 91/100 | N/A | Needs Fix |
| ... | ... | ... | ... | ... | ... |

**Batch Statistics:**
- Total pieces reviewed: N
- Ready for publication: N
- Needs fixes: N
- Critical issues: N

### Step 4: Detail Drill-Down

For pieces that need fixes, offer to show detailed reports. Present critical issues first, then warnings.

### Step 5: Batch Remediation

Offer to:
- Auto-fix simple compliance issues across all pieces
- Generate a task list of manual fixes needed
- Re-run the review after fixes are applied
- Export the review results as a report

### Error Handling

- If a content piece is unreadable or corrupted, skip it and note in the summary
- If the batch is very large (>20 pieces), process in chunks and show intermediate progress
- If review agents are unavailable, run available checks and note which were skipped
