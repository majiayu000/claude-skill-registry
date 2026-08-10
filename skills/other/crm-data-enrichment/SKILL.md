---
name: crm-data-enrichment
description: Enrich CRM records with firmographic and contact data, filling gaps in company and person profiles to improve segmentation, routing, and outreach quality. Use when the user requests crm data enrichment or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# CRM Data Enrichment

Enrich company and contact records in your CRM with up-to-date firmographic, technographic, and demographic data. This skill identifies gaps in existing records, sources enrichment data from available signals, merges and deduplicates entries, validates accuracy, and updates fields — giving sales teams cleaner data for segmentation, lead routing, and personalized outreach.

## Workflow

1. **Identify Gaps in CRM Data** — Audit the target CRM records to surface missing or outdated fields. Common gaps include annual revenue, employee count, industry classification, technology stack, direct phone numbers, verified email addresses, and current job titles. Prioritize fields that directly impact lead scoring and routing logic.

2. **Source Enrichment Data** — Pull data from company websites, LinkedIn profiles, SEC filings, job postings, DNS/TXT records (for tech stack detection), press releases, and third-party data providers. Cross-reference at least two independent sources per data point to reduce single-source risk.

3. **Match and Merge Records** — Align enrichment data to CRM records using deterministic matching on domain, email, or unique identifiers, supplemented by fuzzy matching on company name and location. Deduplicate records where enrichment reveals two CRM entries represent the same entity, preserving the most complete record as the primary.

4. **Validate Accuracy** — Apply confidence scoring to each enriched field. Flag data points sourced from a single unverified origin as low-confidence. Cross-check revenue and headcount against recent earnings reports or LinkedIn company pages. Validate email deliverability and phone connectivity where possible.

5. **Update CRM Fields** — Write validated enrichment data back to the CRM, respecting field-level permissions and avoiding overwrites of manually verified data. Log all changes with timestamps and source attribution for audit trails. Trigger downstream automations (lead scoring recalculation, territory reassignment) based on newly populated fields.

## Usage

Provide the CRM records (or describe the fields and current data) you want enriched, along with which fields to prioritize. Specify the CRM system if relevant (Salesforce, HubSpot, etc.) and any enrichment constraints.

**Example prompt:**
> Enrich this company record for NovaTech Solutions. Currently we only have the company name and domain (novatech.io). Fill in revenue, employee count, industry, headquarters, founding year, tech stack, and key contacts. Format as a before/after comparison.

## Examples

### Example 1: Company Record Enrichment

**Input:** Sparse CRM record for NovaTech Solutions.

**Before:**

| Field | Value |
|---|---|
| Company Name | NovaTech Solutions |
| Domain | novatech.io |
| Industry | — |
| Annual Revenue | — |
| Employee Count | — |
| Headquarters | — |
| Founded | — |
| Tech Stack | — |
| LinkedIn URL | — |

**After Enrichment:**

| Field | Value | Source | Confidence |
|---|---|---|---|
| Company Name | NovaTech Solutions, Inc. | SEC filing | High |
| Domain | novatech.io | Existing | — |
| Industry | Enterprise Software (SaaS) | LinkedIn + Crunchbase | High |
| Annual Revenue | $42M ARR | Crunchbase Series C filing | Medium |
| Employee Count | 280 | LinkedIn company page | High |
| Headquarters | Austin, TX | Company website footer | High |
| Founded | 2017 | Crunchbase | High |
| Tech Stack | AWS, React, PostgreSQL, Snowflake, Segment | DNS records + job postings | Medium |
| LinkedIn URL | linkedin.com/company/novatech-solutions | LinkedIn search | High |

**Fields added:** 7 of 7 gaps filled. Revenue flagged as medium confidence (sourced from fundraising disclosure, not audited financials).

---

### Example 2: Contact Record Enrichment

**Input:** Contact record with only name and email.

**Before:**

| Field | Value |
|---|---|
| First Name | Sarah |
| Last Name | Nguyen |
| Email | s.nguyen@novatech.io |
| Title | — |
| Phone | — |
| LinkedIn | — |
| Location | — |
| Reports To | — |

**After Enrichment:**

| Field | Value | Source | Confidence |
|---|---|---|---|
| First Name | Sarah | Existing | — |
| Last Name | Nguyen | Existing | — |
| Email | s.nguyen@novatech.io | Existing (verified deliverable) | High |
| Title | VP of Engineering | LinkedIn profile | High |
| Phone | +1 (512) 555-0173 | Company directory page | Medium |
| LinkedIn | linkedin.com/in/sarah-nguyen-eng | LinkedIn search | High |
| Location | Austin, TX | LinkedIn profile | High |
| Reports To | James Park, CTO | LinkedIn org chart + press release | Medium |

**Fields added:** 5 of 5 gaps filled. Phone flagged as medium confidence (directory pages can lag behind extensions changes).

## Best Practices

- Always enrich the company record before enriching associated contacts — firmographic context improves contact validation.
- Set confidence thresholds for auto-update vs. manual review; fields below 70% confidence should be queued for human verification.
- Preserve manually entered data by default; only overwrite when enrichment data has demonstrably higher confidence and recency.
- Run enrichment on a recurring schedule (monthly for active pipeline accounts, quarterly for nurture) rather than one-off batches.
- Log every field change with source and timestamp so sales reps can assess trustworthiness.
- Respect data privacy regulations (GDPR, CCPA) — do not enrich with personal data where consent requirements are unmet.

## Edge Cases

- **Domain mismatch or redirect** — When a company domain redirects to a parent org, verify whether the CRM record refers to the subsidiary or parent before merging firmographic data.
- **Stale LinkedIn data** — Job titles on LinkedIn can lag real-world changes by months. Cross-reference with recent press releases, company announcements, or email signature blocks for current titles.
- **Duplicate records post-enrichment** — Enrichment may reveal that two CRM accounts (e.g., "NovaTech" and "NovaTech Solutions Inc.") are the same entity. Flag for merge review rather than auto-merging to prevent accidental data loss.
- **Private companies with no public financials** — Revenue and funding data may be unavailable or speculative. Mark these fields as estimates with explicit confidence bands (e.g., "$30M–$50M estimated ARR").
- **Contacts with common names** — When matching contacts by name alone, require a secondary identifier (domain, company, location) to avoid false positive matches. Never enrich a contact record based solely on name similarity.
