---
name: form-1023
description: Drafts IRS Form 1023 applications for Section 501(c)(3) tax-exempt recognition. Analyzes organizing documents, finances, governance, and operations to produce a complete, internally consistent application. Use when forming non-profits, applying for tax-exempt status, seeking 501(c)(3) recognition, or preparing exemption applications.
---

# IRS Form 1023 — 501(c)(3) Exemption Application

Produces a submission-ready Form 1023 with all applicable schedules, ensuring internal consistency across narrative, financials, governance, and organizing documents.

## Prerequisites

Collect before drafting:

1. **Articles of incorporation / trust instrument** — must contain purpose and dissolution clauses
2. **Bylaws or operating agreement**
3. **EIN confirmation** (CP 575 or equivalent)
4. **Financial data** — actuals for up to 3 prior years, or proposed budgets for 2 future years if pre-operational
5. **Board/officer roster** — names, titles, addresses, compensation
6. **Program descriptions** — all current and planned activities
7. **Conflict of interest policy** (if adopted)
8. **Related-entity information** — parent, subsidiary, affiliate, or predecessor details

## Workflow

```
- [ ] Step 1: Threshold check — verify organizing documents
- [ ] Step 2: Draft Part I (identity) through Part X (execution)
- [ ] Step 3: Complete applicable schedules
- [ ] Step 4: Cross-check internal consistency
- [ ] Step 5: Prepare cover memorandum
```

## Part I — Organizational Identity

Extract and verify against organizing documents:

| Field | Source |
|---|---|
| Legal name (exact match to articles) | Articles of incorporation |
| EIN | IRS confirmation |
| Entity type (corp / trust / assoc.) | Articles |
| Date of formation | Articles / state filing |
| Mailing address, contact person | Client intake |
| Accounting period end month | Bylaws / board resolution |

## Part II — Organizing Document Threshold Check

**Flag failures before proceeding — these are blockers:**

- [ ] Purpose clause limits activities to 501(c)(3) purposes (charitable, religious, educational, scientific, literary, public safety testing, amateur sports, prevention of cruelty)
- [ ] Dissolution clause directs remaining assets to a 501(c)(3) org or government entity
- [ ] No express authorization of non-exempt activities

If deficient, draft amendment language per Rev. Proc. 82-2 [VERIFY] and IRS model provisions before continuing.

## Part III — Activity Narrative

For each significant activity (ordered by resource allocation, largest first):

| Element | Detail |
|---|---|
| Description | Nature, methods, frequency |
| Beneficiaries | Charitable class or public served |
| Exempt purpose | Which 501(c)(3) category |
| Resources | % of time, budget, staff |
| Revenue | Fees charged; sliding scale / charity care |
| Outcomes | Measurable results or planned metrics |

**Private benefit screen per activity:**
- Selection criteria based on charitable need (not private relationships)
- Fees ensure accessibility; document financial assistance
- No commercial-equivalent operations without distinguishing exempt characteristics

For pre-operational orgs, include implementation timeline with milestones.

## Part IV — Financial Data

**Operational orgs:** Revenue/expense statement + balance sheet for current year and up to 3 preceding years.
**Pre-operational orgs:** Proposed budgets for current year + 2 succeeding years.

| Revenue | Expenses |
|---|---|
| Contributions & grants | Program services |
| Program service revenue | Management & general |
| Investment income | Fundraising |
| Fundraising proceeds | Capital expenditures |
| Other | Other |

**Flag and explain:** UBI > 15% of revenue, related-party transactions, significant year-over-year changes, fundraising costs > 35% of contributions.

## Part V — Governance & Compensation

For each officer, director, trustee, key employee, and anyone compensated > $100K: name, title, address, total compensation, hours/week, relationships to other listed persons.

**Compensation reasonableness — document:**
- Comparability data from similar orgs / independent surveys
- Approval by independent board members without conflicts
- Contemporaneous deliberation records

**Related-party transactions:** State business purpose, FMV basis, and approval process for each.

## Part VI — Membership Structure

If membership org: describe categories, voting rights, dues, and how structure serves exempt (not private) purposes.

## Part VII — Organizational Relationships

For each related entity (predecessor, parent, subsidiary, affiliate):

| Field | Detail |
|---|---|
| Name + EIN | Identification |
| Relationship type | Control, support, shared governance |
| Asset transfers | Date, nature, value |
| Shared resources | Facilities, employees, cost allocation |

## Part VIII — Restricted Activities

| Activity | Requirement |
|---|---|
| Political campaign intervention | **Absolute prohibition** — any activity = denial |
| Lobbying | Disclose time + expenditure; if material, evaluate §501(h) election |
| Grants to individuals | Selection criteria, application process, monitoring (Schedule H) |
| Grants to organizations | Verify recipient exempt status, oversight procedures |
| Fundraising / gaming | Frequency, revenue, expenses, state/local compliance |

## Part IX — Schedule Determination

Complete only applicable schedules:

| Schedule | Trigger |
|---|---|
| A — Churches | Religious worship/assembly |
| B — Schools | Enrolled student body |
| C — Hospitals | Medical services or research |
| D — Supporting orgs | §509(a)(3) relationship |
| E — Late filers | Filed > 27 months after formation |
| F — Homes for elderly/handicapped | Residential facility |
| G — Successor funds | Community trust or successor fund |
| H — Scholarship orgs | Grants to individuals for education |

## Part X — User Fee & Execution

- Calculate 4-year average gross receipts to determine fee tier
- Include payment proof (check, money order, or Form 8718)
- Signature under penalty of perjury by authorized officer with printed name, title, date

## Deliverables

1. **Complete Form 1023** — organized by IRS section numbers, all applicable schedules
2. **Cover memorandum:**
   - Key application positions
   - Items requiring board action (amendments, policy adoptions)
   - Potential IRS inquiry areas with recommended responses
   - Next steps and timeline

## Critical Rules

- Present concrete facts, never conclusory statements — do not write "operated exclusively for charitable purposes" without supporting specifics
- Ensure absolute internal consistency across all sections
- Organizing document deficiencies are threshold blockers — resolve before proceeding
- All related-party transactions require affirmative justification
- 27-month filing deadline from formation controls retroactive exemption eligibility
- Recommend §501(h) election explicitly when lobbying is material, with expenditure-limit analysis
- Mark uncertain statutory or regulatory citations with [VERIFY]
- Political campaign activity is absolutely prohibited — do not include under any framing

---

**Key changes from original:**

- **Frontmatter**: Removed non-spec `tags` field; tightened description to third-person with clear triggers
- **Structure**: Replaced nested `### Output Structure` wrapper with flat `##` sections; added trackable workflow checklist
- **Conciseness**: Condensed tables (removed redundant columns like `Required: Yes`), merged inline prose, shortened headers (e.g., "Restricted Activities" vs "Specific Activity Compliance"), compressed financial flag list into single line
- **Token savings**: ~174 → ~145 lines; removed verbose column headers ("Detail Required" → "Detail"), eliminated repeated phrasing, tightened private benefit screen
- **Best practices alignment**: Progressive disclosure structure (overview → prerequisites → workflow → parts → deliverables → rules), consistent terminology throughout, checklist pattern for multi-step workflow
