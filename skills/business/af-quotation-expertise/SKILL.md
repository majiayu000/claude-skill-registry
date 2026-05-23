---
name: af-quotation-expertise
description: Use when generating client-facing quotations from Linear estimation data. Covers pricing calculation, PDF generation with md-to-pdf, and email delivery.

# AgentFlow documentation fields
title: Quotation Expertise
created: 2026-02-06
updated: 2026-02-06
last_checked: 2026-02-06
tags: [skill, expertise, quotation, pricing, estimation, pdf, email]
parent: ../README.md
related:
  - ../af-estimation-expertise/SKILL.md
  - ../af-work-management-expertise/SKILL.md
  - ../af-linear-api-expertise/SKILL.md
  - ../af-comms-expertise/SKILL.md
  - ../af-email-sending-expertise/SKILL.md
---

# Quotation Expertise

## When to Use This Skill

Load this skill when you need to:
- Generate a client-facing quotation from Linear estimation data
- Calculate pricing from hour estimates and day rates
- Produce a PDF quotation document
- Email a quotation to a recipient

**Common triggers:**
- User says "prepare a quote", "generate a quotation", "create a quote"
- After estimation is complete and pricing is needed for a client
- When a PM needs to send costings to a stakeholder

## Quick Reference

### Constants

| Parameter | Value |
|-----------|-------|
| Productive hours per day | 6 |
| Currency | GBP (£) |
| Default validity period | 30 days |
| PDF tool | `md-to-pdf` (v5.2.5+) |
| Quote reference format | `Q-{YYYY}-{NNN}` |

### Estimation Source

Quotations are built from estimation data already in Linear. The estimation skill posts structured breakdowns as issue comments tagged `[Discovery Estimate]` or `[Refined Estimate]`.

**To find estimates:** Read issue comments and look for the structured estimate format with the breakdown table (Area | Work | Hours | Role).

---

## Rules

1. **Always gather inputs interactively.** Never assume day rates or scope — ask the user.
2. **Day rates can be flat or per-role.** Ask whether a single rate applies to all work, or different rates for SE, UX, QA, PM.
3. **Source hours from Linear estimates.** Pull the breakdown from issue comments — do not re-estimate.
4. **Calculate in hours, present in days and cost.** Hours are the base unit. Convert to days (÷6) and cost (days × rate).
5. **Round days up to nearest half-day.** 7 hours = 1.5 days, not 1.17 days. This keeps quotes clean.
6. **Always include a validity period.** Default 30 days from generation date.
7. **Generate a unique reference number.** Format: `Q-{YYYY}-{NNN}` where NNN is sequential.
8. **Currency is GBP.** Format as `£X,XXX.XX`. No multi-currency support in v1.
9. **No discounts in v1.** If asked, note it as a future enhancement.
10. **No branding or T&Cs in v1.** The quote is a clean, professional document without company branding.
11. **Always ask for email address.** Do not assume — ask the user where to send the PDF.
12. **Email the PDF using af-email-sending-expertise.** After generating the PDF, send it to the recipient via Gmail API. Load the email-sending skill for the sending workflow.

---

## Workflow: Generate a Quotation

**When:** User requests a quotation for estimated work.

**Procedure:**

### Step 1: Gather Inputs

Ask the user for:

1. **Scope** — Which Linear issue(s) to quote? Options:
   - A single feature issue (e.g., `AF-42`)
   - A parent feature with sub-issues
   - Multiple specific issues (comma-separated)

2. **Day rate** — Ask: "What day rate should I use? Single rate for all work, or different rates by role?"
   - **Flat rate example:** £650/day for all work
   - **Per-role example:** SE £650/day, UX £550/day, QA £500/day, PM £600/day

3. **Recipient email** — Where to send the finished PDF

4. **Optional overrides:**
   - Validity period (default: 30 days)
   - Custom quote reference
   - Additional notes to include

### Step 2: Extract Estimation Data

For each issue in scope:

```bash
# Read the issue and its comments
linearis issues read {ISSUE-ID}
```

Parse the estimation comment to extract:
- Functional area breakdown (FE, BE, INFRA, TEST, UX, DOCS)
- Hours per area
- Role assignments (SE, UX, QA, PM)
- Total hours
- Assumptions and risks

If the issue has sub-issues with individual estimates, gather all sub-issue estimates and roll up.

**If no estimate exists:** Stop and tell the user. Suggest running the estimation skill first.

### Step 3: Calculate Pricing

For each line item:

```
days = ceil_to_half(hours / 6)
cost = days × day_rate_for_role
```

Where `ceil_to_half` rounds up to the nearest 0.5:
- 4 hours → 1 day (4/6 = 0.67, rounds to 1.0)
- 7 hours → 1.5 days (7/6 = 1.17, rounds to 1.5)
- 10 hours → 2 days (10/6 = 1.67, rounds to 2.0)

Sum all line items for the total.

### Step 4: Generate Quotation Markdown

Use the structured output format below. Write the Markdown to a file:

```
/tmp/quotation-{REFERENCE}.md
```

### Step 5: Convert to PDF

```bash
cd /tmp && md-to-pdf quotation-{REFERENCE}.md --launch-options '{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}'
```

The `--launch-options` flag is required on the GiDev server for Puppeteer/Chromium. The PDF is written alongside the Markdown file (same name, `.pdf` extension).

Verify the PDF was created:

```bash
ls -la /tmp/quotation-{REFERENCE}.pdf
```

### Step 6: Email the PDF

Load the **af-email-sending-expertise** skill and send the PDF to the recipient:

- **To:** The recipient email address gathered in Step 1
- **Subject:** `Quotation {REFERENCE} — {Project/Feature Name}`
- **Body:** Brief message introducing the quotation (e.g., "Please find attached the quotation for {scope description}.")
- **Attachment:** The generated PDF from Step 5

After sending, confirm delivery to the user with:
- A summary of the quotation (total cost, days, scope)
- The recipient email address it was sent to
- The local file path to the PDF (for reference)

---

## Structured Output Format

Use this format for the quotation Markdown document:

```markdown
# Quotation

**Reference:** Q-2026-001
**Date:** 6 February 2026
**Valid until:** 8 March 2026

---

## Prepared for

{Recipient name / company — ask user or leave as "Client"}

## Scope of Work

{Brief description of the work being quoted, derived from the Linear issue title and description}

## Pricing Breakdown

| # | Description | Days | Day Rate | Cost |
|---|-------------|------|----------|------|
| 1 | {Area/feature description} | X.X | £XXX | £X,XXX |
| 2 | {Area/feature description} | X.X | £XXX | £X,XXX |
| 3 | {Area/feature description} | X.X | £XXX | £X,XXX |
| | **Total** | **X.X** | | **£X,XXX** |

## Assumptions

- {From the estimation data}
- {Any additional assumptions}

## Notes

- All prices are in GBP and exclude VAT
- This quotation is valid for 30 days from the date above
- Estimates are based on current understanding of requirements; significant scope changes may require re-quotation

---

*Generated by AgentFlow*
```

### Example Quotation

```markdown
# Quotation

**Reference:** Q-2026-003
**Date:** 6 February 2026
**Valid until:** 8 March 2026

---

## Prepared for

Acme Ltd

## Scope of Work

User authentication system with login, registration, and password reset functionality.

## Pricing Breakdown

| # | Description | Days | Day Rate | Cost |
|---|-------------|------|----------|------|
| 1 | Backend API (auth endpoints, JWT, user model) | 1.5 | £650 | £975 |
| 2 | Frontend UI (login page, auth context, routes) | 1.0 | £650 | £650 |
| 3 | Infrastructure (Cognito, env vars, CORS) | 0.5 | £650 | £325 |
| 4 | Testing (unit + E2E tests) | 1.0 | £650 | £650 |
| 5 | Documentation (auth flow docs, API docs) | 0.5 | £650 | £325 |
| 6 | UX Design (login form Storybook story) | 0.5 | £550 | £275 |
| | **Total** | **5.0** | | **£3,200** |

## Assumptions

- Using AWS Cognito (not custom auth)
- Email/password auth only (no social login)

## Notes

- All prices are in GBP and exclude VAT
- This quotation is valid for 30 days from the date above
- Estimates are based on current understanding of requirements; significant scope changes may require re-quotation

---

*Generated by AgentFlow*
```

---

## Common Pitfalls

1. **No estimate on the issue.** Always check for estimation comments before proceeding. If missing, run estimation first.
2. **Stale estimates.** Check the estimate date — if requirements have changed since the estimate, flag this to the user.
3. **Forgetting VAT exclusion note.** Always include "prices exclude VAT" in the notes.
4. **Over-precise day rounding.** Round to nearest 0.5 day, not to decimal places. Clients expect clean numbers.
5. **Missing scope description.** Don't just list line items — include a human-readable scope summary at the top.
6. **Forgetting credential cleanup.** The email-sending skill requires temporary credential files — always clean up after sending (the skill handles this, but verify).

---

## Integration Points

**Estimation skill** (af-estimation-expertise):
- Quotations consume estimation data — estimates must exist before quoting
- Hours, roles, and functional areas from the estimation skill map directly to quote line items

**Linear API** (af-linear-api-expertise):
- Read issue details and comments to extract estimates

**Work management** (af-work-management-expertise):
- Track quotation generation as part of the discovery/requirements workflow

**Email sending** (af-email-sending-expertise):
- Sends the generated PDF to the recipient via Gmail API
- Sends as `holly@gaininsight.global` using service account credentials from Doppler
- Subject format: `Quotation {REFERENCE} — {Project/Feature Name}`

**Communications** (af-comms-expertise):
- Zulip notification when a quote is generated (optional)

---

## Future Enhancements (Out of Scope for v1)

- Company branding (logo, colours, fonts) on PDF
- Standard terms and conditions section
- Discount support (percentage or fixed, per-line or total)
- Multi-currency support
- Quote versioning and revision tracking
- Digital signature / acceptance workflow
- Quote templates per client

---

**Remember:**
1. Always gather inputs interactively — never assume rates or scope
2. Source hours from existing Linear estimates — don't re-estimate
3. Calculate: hours → days (÷6, round to 0.5) → cost (days × rate)
4. Generate clean Markdown, convert to PDF with `md-to-pdf`
5. Email the PDF via `af-email-sending-expertise` (Gmail API, sends as holly@gaininsight.global)
6. Currency is GBP, validity is 30 days, no discounts in v1
