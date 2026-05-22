---
name: crm-hygiene-scanner
description: "Use when auditing CRM data quality, finding duplicate records, identifying stale leads, cleaning pipeline data, or improving data hygiene. Triggers: 'clean my CRM', 'audit CRM data', 'find duplicates', 'CRM hygiene', 'data quality check', 'stale leads', 'pipeline cleanup'."
version: 1.0.0
---

# CRM Hygiene Scanner

Scan a CSV export of CRM data (contacts, companies, or deals), detect duplicates, flag stale records, measure data completeness, calculate an overall quality score, and produce a prioritized cleanup plan. This is a read-only audit — the original file is never modified.

## Tools Used

- **Read** — load the CSV file and any existing hygiene reports
- **Write** — save the hygiene report to `docs/crm-hygiene-report.md`
- **Bash** — run Python one-liners for CSV parsing, fuzzy matching, and statistical analysis
- **Glob** — check for existing reports before overwriting

## Methodology

Follow these steps in order. Do not skip steps. Do not fabricate data.

### Step 1: Input

Ask the user for four pieces of information before proceeding:

> To run the CRM hygiene scan, I need:
>
> 1. **CRM export file path** — path to the CSV file on disk
> 2. **Data type** — is this contacts, companies, or deals/opportunities?
> 3. **CRM system** — which CRM did this come from? (HubSpot, Salesforce, Pipedrive, or other)
> 4. **Critical fields** — which fields matter most for your business? (e.g., email, phone, company name, deal stage, last activity date, owner)

Wait for all four answers. Do not assume defaults.

Once the user responds, validate the CSV path exists using Read. If the file is not found, tell the user and ask for the correct path.

### Step 2: Data Profiling

Read the CSV and build a profile of the dataset. Use Bash with Python one-liners for parsing.

Produce these metrics:

| Metric | How to Calculate |
|---|---|
| **Total records** | Row count (excluding header) |
| **Column inventory** | List every column name |
| **Data types** | Infer type per column: text, email, phone, date, number, boolean, URL |
| **Fill rate per column** | `(non-empty cells / total rows) * 100` — report as percentage |
| **Date range** | Oldest and newest value across all date columns |
| **Unique vs. total values** | For each key field (email, company name, phone), count unique values vs. total rows |
| **Row completeness** | Average number of filled columns per row, as a percentage of total columns |

Present the profile to the user as a table before continuing. This gives them a chance to flag any column mapping issues early.

For CSVs with more than 10,000 rows: read the first 10,000 rows for profiling and extrapolate. Clearly note that results are based on a sample and state the sample size.

### Step 3: Duplicate Detection

Scan for three types of duplicates. Present each group with a confidence level.

#### 3a. Exact Duplicates (Confidence: HIGH)

- Same email address (case-insensitive, whitespace-trimmed)
- Same company name AND same contact name (case-insensitive)

#### 3b. Fuzzy Duplicates (Confidence: MEDIUM)

- Similar company names after normalization. Normalize by:
  - Lowercasing
  - Stripping legal suffixes: Inc, Inc., Incorporated, LLC, Ltd, Ltd., GmbH, AG, Corp, Corp., Co, Co.
  - Stripping punctuation and extra whitespace
  - Comparing the normalized strings — flag if they match or if the edit distance is 2 or fewer characters
- Similar contact names accounting for:
  - First name vs. nickname (e.g., "Robert" vs. "Bob", "William" vs. "Will")
  - Reversed first/last name order
  - Middle name included vs. omitted

#### 3c. Cross-Field Duplicates (Confidence: MEDIUM)

- Different email but same phone number AND same name
- Different email but same company AND same job title (likely the same person who changed email)

#### Duplicate Output Format

Group duplicates together. For each group, present:

```
Duplicate Group #{n} — Confidence: {HIGH/MEDIUM}
| Row | Name | Email | Company | Phone | Last Activity | Completeness |
|-----|------|-------|---------|-------|---------------|--------------|
| ... | ...  | ...   | ...     | ...   | ...           | {n}/{total} fields filled |

Recommendation: Keep Row {X} (most complete + most recent activity). Merge data from Row {Y} into Row {X} before deleting.
```

For each group, recommend which record to keep based on:
1. Most fields filled (highest completeness)
2. Most recent last activity date
3. If tied, keep the one with a valid email address

### Step 4: Stale Record Detection

Flag records based on inactivity. Adapt the criteria to the data type the user specified in Step 1.

#### For Contacts

| Classification | Criteria |
|---|---|
| **Stale** (90-180 days) | No activity in 90-180 days, or no email sent/received in 60-90 days |
| **Dormant** (180-365 days) | No activity in 180-365 days |
| **Dead** (365+ days) | No activity in over 365 days |

Also flag:
- Contacts with no associated company (orphaned contacts)
- Contacts with no email address AND no phone number (unreachable)

#### For Companies

| Classification | Criteria |
|---|---|
| **Stale** (90-180 days) | No associated contact activity in 90-180 days |
| **Dormant** (180-365 days) | No associated contact activity in 180-365 days |
| **Dead** (365+ days) | No associated contact activity in over 365 days |

Also flag:
- Companies with zero associated contacts (empty accounts)

#### For Deals/Opportunities

| Classification | Criteria |
|---|---|
| **Stale** (30-60 days) | Deal stuck in the same stage for 30-60 days |
| **Dormant** (60-180 days) | Deal stuck in the same stage for 60-180 days |
| **Dead** (180+ days) | Deal stuck in the same stage for 180+ days, or no activity for 180+ days |

Also flag:
- Deals with no associated contact
- Deals with no owner assigned
- Deals with a close date in the past but still marked as open

If the CSV does not contain a last activity date or equivalent column, tell the user which column you looked for, report that staleness detection is limited, and skip to Step 5.

Present staleness results as a summary table:

```
| Classification | Count | % of Total | Action |
|---|---|---|---|
| Active (< 90 days) | ... | ...% | No action needed |
| Stale (90-180 days) | ... | ...% | Re-engage or update |
| Dormant (180-365 days) | ... | ...% | Archive or run win-back |
| Dead (365+ days) | ... | ...% | Archive immediately |
```

### Step 5: Missing Data Analysis

For each field the user identified as critical in Step 1, report:

| Field | Records Missing | % Missing | Impact |
|---|---|---|---|
| {field name} | {count} | {percentage} | {impact assessment} |

#### Impact Assessment

Classify the impact of each missing field:

- **Critical** — This field is required for outreach or pipeline management. Missing it blocks action. Examples: email on a contact, deal stage on an opportunity, company name on an account.
- **High** — This field significantly improves targeting or personalization. Missing it reduces effectiveness. Examples: job title, industry, company size.
- **Medium** — This field is useful but not blocking. Examples: phone number, LinkedIn URL, address.
- **Low** — Nice to have. Examples: Twitter handle, secondary email.

#### Enrichment Recommendations

For each critical or high-impact missing field, suggest enrichment tools:

| Missing Field | Recommended Tools |
|---|---|
| Email | Apollo.io, Hunter.io, Clearbit, Snov.io |
| Phone | Apollo.io, Lusha, ZoomInfo |
| Company size / industry | Clearbit, Apollo.io, LinkedIn Sales Navigator |
| Job title | LinkedIn Sales Navigator, Apollo.io |
| LinkedIn URL | Apollo.io, Phantombuster |
| Company website | Clearbit, manual Google search |
| Revenue / funding | Crunchbase, PitchBook, Clearbit |

#### High-Impact Missing Records

List the top 10 records where missing data has the highest business impact. Prioritize by:
1. Records in active deals or hot pipeline stages
2. Records with recent activity but missing contact info
3. Records matching ICP but missing fields needed for outreach

### Step 6: Data Quality Score

Calculate an overall hygiene score on a 0-100 scale using four weighted components.

#### Component 1: Fill Rate of Critical Fields (40% weight)

Average the fill rates of the fields the user identified as critical in Step 1.

```
fill_score = average_fill_rate_of_critical_fields (0-100)
```

#### Component 2: Duplicate Rate (25% weight)

```
duplicate_rate = (records_in_duplicate_groups / total_records) * 100
duplicate_score = max(0, 100 - (duplicate_rate * 5))
```

A 1% duplicate rate costs 5 points. A 20%+ duplicate rate scores 0.

#### Component 3: Stale Record Rate (20% weight)

```
stale_rate = (stale + dormant + dead records) / total_records * 100
stale_score = max(0, 100 - (stale_rate * 2))
```

A 10% stale rate costs 20 points. A 50%+ stale rate scores 0.

#### Component 4: Data Freshness (15% weight)

Based on the average number of days since last update across all records.

| Average Days Since Update | Score |
|---|---|
| 0-30 | 100 |
| 31-60 | 80 |
| 61-90 | 60 |
| 91-180 | 40 |
| 181-365 | 20 |
| 365+ | 0 |

If no date column is available, default this component to 50 and note the limitation.

#### Final Score

```
final_score = (fill_score * 0.40) + (duplicate_score * 0.25) + (stale_score * 0.20) + (freshness_score * 0.15)
```

#### Grade

| Score | Grade | Meaning |
|---|---|---|
| 90-100 | **A** | Excellent — minor cleanup only |
| 75-89 | **B** | Good — some hygiene issues to address |
| 60-74 | **C** | Fair — significant cleanup needed |
| 40-59 | **D** | Poor — major data quality problems |
| 0-39 | **F** | Critical — CRM data is unreliable for decision-making |

Present the score breakdown to the user before writing the report.

### Step 7: Cleanup Recommendations

Generate a prioritized action list based on all findings from Steps 3-6.

#### P0: Merge Exact Duplicates (do first)

List every exact duplicate group with the recommended merge action. Include row numbers and the "keep" record.

Estimate: "{X} duplicate groups to merge. Estimated time: ~{Y} minutes at 30 seconds per merge."

#### P1: Review Fuzzy Duplicates (do second)

List every fuzzy duplicate group. These require human review — the scanner flags them, but a person must decide.

Estimate: "{X} fuzzy duplicate groups to review. Estimated time: ~{Y} minutes at 1 minute per group."

#### P2: Re-Engage or Archive Stale Records (do third)

- **Stale records (90-180 days):** Run a re-engagement campaign. Suggest a simple "Are you still interested?" email template.
- **Dormant records (180-365 days):** Move to a separate list or tag them. Run a last-chance campaign before archiving.
- **Dead records (365+ days):** Archive immediately. Remove from active lists and sequences.

Estimate: "{X} records to triage. Estimated time: ~{Y} minutes for bulk tagging + {Z} minutes for re-engagement setup."

#### P3: Enrich Missing Fields (do fourth)

For each critical missing field, recommend the enrichment approach:
- If fewer than 50 records: manual enrichment via LinkedIn or company websites
- If 50-500 records: use an enrichment tool (Apollo, Clearbit, etc.)
- If 500+ records: use a bulk enrichment API with a validation step

Estimate: "{X} records to enrich across {Y} fields. Tool cost estimate: ~${Z} using Apollo/Clearbit at standard rates."

#### P4: Prevent Future Issues (ongoing)

Recommend process changes:
- Required fields at record creation (list which fields should be mandatory)
- Naming conventions (e.g., "Always use full company legal name without suffixes")
- Automated dedup rules (e.g., "Block creation if email already exists")
- Regular hygiene cadence: "Run this scanner monthly. Set a calendar reminder."
- Data entry standards doc: suggest creating one based on the issues found

### Step 8: Output

Check if `docs/crm-hygiene-report.md` already exists using Glob. If it does, ask the user: "A previous hygiene report exists. Overwrite it or save as a new file with today's date?"

Write the report to `docs/crm-hygiene-report.md` (or the date-stamped alternative) using this structure:

```markdown
# CRM Hygiene Report

> **Scan date:** {YYYY-MM-DD}
> **Data type:** {contacts / companies / deals}
> **CRM system:** {HubSpot / Salesforce / Pipedrive / other}
> **Records scanned:** {total count}
> **Data Quality Score:** {score}/100 — Grade: {A/B/C/D/F}
>
> This report may contain personal data. Handle according to your organization's data privacy policies.

## Executive Summary

{3-5 sentences summarizing the key findings. Lead with the score and grade. Highlight the biggest problem. State the estimated total cleanup time.}

## Data Profile

| Column | Data Type | Fill Rate | Unique Values | Notes |
|---|---|---|---|---|
| {name} | {type} | {n}% | {count} | {any flags} |

**Date range:** {oldest} to {newest}
**Average row completeness:** {n}%

## Duplicates

**Total duplicate groups found:** {count}
**Total records affected:** {count} ({percentage}% of all records)

### Exact Duplicates ({count} groups)

{Duplicate group tables from Step 3, with merge recommendations}

### Fuzzy Duplicates ({count} groups)

{Duplicate group tables from Step 3, with review recommendations}

### Cross-Field Duplicates ({count} groups)

{Duplicate group tables from Step 3, with review recommendations}

## Stale Records

| Classification | Count | % of Total |
|---|---|---|
| Active (< 90 days) | {n} | {n}% |
| Stale (90-180 days) | {n} | {n}% |
| Dormant (180-365 days) | {n} | {n}% |
| Dead (365+ days) | {n} | {n}% |

{Additional flags: orphaned contacts, empty accounts, stuck deals — as relevant to the data type}

## Missing Data

| Field | Records Missing | % Missing | Impact | Enrichment Tool |
|---|---|---|---|---|
| {name} | {count} | {n}% | {Critical/High/Medium/Low} | {tool recommendation} |

### High-Impact Records to Fix First

{Top 10 records where missing data blocks the most value, with specific fields to fill}

## Data Quality Score Breakdown

| Component | Weight | Raw Score | Weighted Score |
|---|---|---|---|
| Fill rate (critical fields) | 40% | {n}/100 | {n} |
| Duplicate rate | 25% | {n}/100 | {n} |
| Stale record rate | 20% | {n}/100 | {n} |
| Data freshness | 15% | {n}/100 | {n} |
| **Total** | **100%** | | **{n}/100** |

**Grade: {A/B/C/D/F}**

## Cleanup Action Plan

### P0: Merge Exact Duplicates
{List of groups with merge instructions}
**Estimated time:** {n} minutes

### P1: Review Fuzzy Duplicates
{List of groups requiring human review}
**Estimated time:** {n} minutes

### P2: Re-Engage or Archive Stale Records
- **Stale ({n} records):** {action}
- **Dormant ({n} records):** {action}
- **Dead ({n} records):** {action}
**Estimated time:** {n} minutes

### P3: Enrich Missing Fields
{Enrichment plan per field with tool and cost estimates}
**Estimated time:** {n} minutes + {tool cost estimate}

### P4: Prevention
{Process recommendations based on the specific issues found}

## Total Estimated Cleanup Time

| Priority | Task | Time |
|---|---|---|
| P0 | Merge exact duplicates | ~{n} min |
| P1 | Review fuzzy duplicates | ~{n} min |
| P2 | Triage stale records | ~{n} min |
| P3 | Enrich missing fields | ~{n} min |
| **Total** | | **~{n} min** |
```

After writing the file, confirm to the user:

> Hygiene report saved to `docs/crm-hygiene-report.md`.
>
> **Score: {n}/100 (Grade {X})**
>
> Top 3 actions to take now:
> 1. {most impactful cleanup action}
> 2. {second most impactful}
> 3. {third most impactful}

## Key Rules

1. **NEVER modify the original CSV.** This is a read-only audit. Do not write to, rename, move, or alter the source file under any circumstances.
2. **Be specific, not generic.** The report must name exact records, exact duplicate groups, and exact missing fields. "You have duplicates" is not acceptable — "Rows 14 and 87 are duplicates (john.smith@acme.com)" is.
3. **Handle large files gracefully.** If the CSV has more than 10,000 rows, sample the first 10,000 rows for analysis. Clearly state that results are extrapolated from a sample and report the sample size.
4. **PII warning.** Always include the privacy notice in the report header: "This report may contain personal data. Handle according to your organization's data privacy policies."
5. **No vendor lock-in.** Enrichment recommendations must include multiple tool options. Never recommend only one vendor.
6. **Adapt to available columns.** Not every CSV will have all expected columns. If a column needed for analysis is missing (e.g., no "last activity date" for staleness detection), note the limitation and skip that sub-analysis rather than failing.
7. **Wait for user input.** Do not proceed past Step 1 until the user has answered all four questions. Do not assume which fields are critical.
8. **Existing report check.** Always check for a previous report before writing. Ask the user whether to overwrite or create a date-stamped version.
9. **Keep it generic.** This skill works with any CRM export in CSV format. Do not reference specific internal tools, databases, or vendor accounts.
