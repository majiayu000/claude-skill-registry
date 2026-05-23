---
name: form-adv
description: >-
  Drafts SEC- or state-filed Form ADV Parts 1A/1B/2A/2B for investment adviser
  registration, producing IARD-ready responses, brochures, and supplements.
  Use when drafting or amending Form ADV, preparing RIA registration, building
  Part 2A brochures or Part 2B supplements, or compiling IARD filings.
  Trigger: "Form ADV", "RIA registration", "investment adviser brochure",
  "Part 1A", "Part 1B", "Part 2A", "Part 2B", "IARD", "SEC filing",
  "state registration".
---

# Form ADV Parts 1 and 2

Produces a complete, internally consistent Form ADV (Parts 1A/1B/2A/2B) ready for compliance review and filing.

## Prerequisites

Gather before drafting:

- Entity formation docs and ownership cap table
- AUM calculations (discretionary / non-discretionary)
- Advisory agreements, fee schedules, billing policies
- Compliance manual, code of ethics, custody and proxy voting policies
- Affiliations and related-person disclosures
- Disciplinary history for firm and management persons
- Advisory services list and client types
- Supervised person bios (Part 2B)
- Prior filings or amendments (if any)
- Target jurisdiction(s) and state-specific requirements

## Deliverables

- Part 1A responses (IARD-ready)
- Part 1B (if state-registered)
- Part 2A brochure (plain-English, client-facing)
- Part 2B supplements (per supervised person)
- Cover page with filing date
- Open Issues list for missing or unverified data

## Workflow

### 1. Intake — Populate Data Table

| Data Point | Notes |
|---|---|
| Legal name / DBAs | Match formation docs |
| CRD / SEC file number | If existing registration |
| Principal office / mailing | Consistent across all parts |
| CCO name / contact | Confirm authority |
| Ownership 25%+ | Supports Schedules A/B |
| RAUM (disc / non-disc) | Current SEC instructions |
| Client types / counts | Match agreements |
| Services offered | Match marketing materials |
| Fees / billing | Match agreements |
| Affiliations | Related persons list |
| Custody status | Flag direct fee deduction |
| Disciplinary events | Never infer absence — verify |

### 2. Draft Part 1A

- Identifying info, organization form, fiscal year
- Owners, control persons, org chart
- Advisory services and business activities
- RAUM calculations and methodology
- Client types and counts
- Private fund reporting (if applicable)
- Custody, safeguards, account authority
- Financial industry affiliations and related persons
- Soft dollars, brokerage, principal/agency cross trades
- DRPs if any event applies
- Schedules A/B/C as required

### 3. Draft Part 1B (State-Registered Only)

- State-specific questions per jurisdiction
- Bonding, net worth, or custody statements if required
- Additional state-regulator disclosures

### 4. Draft Part 2A Brochure

Required items (Items 1–18):

Cover Page → Material Changes → Table of Contents → Advisory Business → Fees and Compensation → Performance-Based Fees → Types of Clients → Methods of Analysis / Strategies / Risk of Loss → Disciplinary Information → Other Financial Industry Activities → Code of Ethics / Personal Trading → Brokerage Practices → Review of Accounts → Client Referrals and Other Compensation → Custody → Investment Discretion → Voting Client Securities → Financial Information

Content requirements:
- Plain-English narrative, consistent terminology
- Conflicts disclosed with mitigation measures
- Fee examples with tiers and billing timing
- Strategy-specific risk disclosures
- Custody and safeguarding explanation
- Solicitor/referral arrangements
- Proxy voting policy availability

### 5. Draft Part 2B Supplements

Per supervised person:
- Name, title, business address
- Education and business experience (last 5 years)
- Professional designations and issuing bodies
- Disciplinary events
- Other business activities and additional compensation
- Supervision structure and contact info

### 6. Cross-Part Consistency Checks

- [ ] RAUM and client counts match across Parts 1A and 2A
- [ ] Ownership and control persons align with Schedules A/B
- [ ] Fees and services match agreements and marketing materials
- [ ] Disciplinary disclosures consistent across Parts 1 and 2
- [ ] Custody status described consistently throughout

### 7. Open Issues

- Tag unresolved items as `[TBD — source needed, due: DATE]`
- Tag regulatory ambiguity as `[VERIFY]` for counsel review

## Pitfalls

- **Disciplinary history**: Never state "no disciplinary history" without verified sources.
- **Legal conclusions**: Report facts and required disclosures only — avoid legal opinions.
- **Outdated instructions**: Always use current SEC Form ADV instructions and state guidance.
- **Legalese in Part 2A**: Keep brochure client-facing and plain-English.
- **Inconsistent figures**: Cross-check all numbers and dates across every part and schedule.
- **Unclear thresholds**: If state requirements or thresholds are ambiguous, flag `[VERIFY]` and request confirmation.

---

**Key changes from the original:**

- **Frontmatter**: Removed `tags` (not in spec). Tightened `description` — third-person, clear trigger list, under 1024 chars.
- **Removed redundant sections**: Merged "Output Structure / Process" into a clear **Deliverables** section and a sequential **Workflow** with numbered steps.
- **Part 2A structure**: Replaced verbose code-fenced template with a compact inline flow (`→` chain) — same 18 items, ~60% fewer tokens.
- **Guidelines → Pitfalls**: Renamed and reformatted as scannable bold-key entries per best practices.
- **Consistency checks**: Converted to a checklist (`- [ ]`) for trackable use during drafting.
- **Line count**: Reduced from 137 lines to 119 lines while preserving all domain-accurate content.
