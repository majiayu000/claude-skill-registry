---
name: form-d
description: Drafts SEC Form D Notice of Exempt Offering for EDGAR filing under Regulation D. Captures issuer details, related persons, offering structure, exemption basis (Rule 504, 506(b), 506(c)), sales compensation, and use of proceeds. Use when filing Form D, preparing an exempt offering notice, or handling Regulation D compliance for unregistered securities.
tags:
  - corporate
  - drafting
  - regulatory
---

# Form D Notice of Exempt Offering

Drafts a complete SEC Form D for EDGAR filing within 15 days of first sale in a Regulation D exempt offering.

## Prerequisites

1. **Issuer organizational documents** — articles/certificate of incorporation or formation, operating agreement
2. **CIK number** — if previously assigned by SEC
3. **Offering materials** — PPM, subscription agreements, term sheets
4. **Related persons list** — all executive officers, directors, and promoters with business addresses
5. **Compensation arrangements** — broker-dealer agreements, finder's fees, CRD numbers
6. **Prior Form D filings** — if this is an amendment

## Output Structure

### Item 1: Filing Information

| Field | Notes |
|-------|-------|
| CIK Number | From prior EDGAR filings; blank if first filing |
| Filing Type | New Notice or Amendment (specify number) |
| Date of First Sale | Exact date or "Yet to occur" |

### Item 2: Issuer Information

| Field | Notes |
|-------|-------|
| Legal Name | Exactly as in organizational documents |
| Principal Business Address | Street address required (no P.O. boxes) |
| Jurisdiction of Inc./Org. | State or foreign jurisdiction |
| Entity Type | Corporation, LP, LLC, GP, trust, other |
| Year of Inc./Org. | Four-digit year |
| SIC Code | Primary Standard Industrial Classification code |
| Phone / Website | Issuer contact |

Flag recent name changes, redomiciliation, or structural changes with effective dates.

### Item 3: Related Persons

For each executive officer, director, and promoter:

| Field | Required |
|-------|----------|
| Full Legal Name | Yes |
| Business Street Address | Yes |
| Relationship(s) | Executive Officer / Director / Promoter (all that apply) |

**Promoter**: person who takes initiative in founding/organizing the business or receives compensation/securities in connection with the offering per the regulatory definition.

### Item 4: Securities Offered

| Field | Detail |
|-------|--------|
| Type(s) | Equity, debt, option/warrant, pooled investment fund interests, tenant-in-common, mineral property securities, other |
| Total Offering Amount | Aggregate maximum |
| Total Amount Sold | As of filing date |
| Price Per Unit | Or "variable pricing" |
| Minimum Investment | Per investor, if applicable |

If multiple classes/series, describe each separately with distinct rights and preferences.

### Item 5: Exemption(s) Claimed

| Exemption | Key Conditions |
|-----------|---------------|
| Rule 504 | Aggregate offering ≤ $10M in 12 months [VERIFY current threshold] |
| Rule 506(b) | No general solicitation; unlimited accredited + up to 35 sophisticated non-accredited |
| Rule 506(c) | General solicitation permitted; must verify all purchasers are accredited |
| Section 4(a)(2) | If claimed alongside Reg D, state separate basis |

Confirm alignment between actual offering conduct and claimed exemption.

### Item 6: Offering Structure & Sales Compensation

| Field | Detail |
|-------|--------|
| Duration | First sale date → expected termination |
| Offering Basis | Best efforts or firm commitment |
| Minimum Offering Amount | If applicable; describe escrow arrangements |
| Use of Proceeds | Working capital, asset acquisition, debt repayment, etc. |

For each broker-dealer, finder, or intermediary:

| Field | Required |
|-------|----------|
| Name | Yes |
| CRD Number | If registered |
| Associated Broker-Dealer | If applicable |
| Compensation Type | Cash commission, finder's fee, securities, other |
| Compensation Amount/Terms | Dollar amount or formula |
| State(s) of Solicitation | Where solicitation will occur |

### Item 7: Issuer Financial Condition

- [ ] Development-stage company
- [ ] Limited operating history
- [ ] Recent material losses
- [ ] Audited financials provided to investors (may be required by exemption type and investor sophistication)

### Item 8: Signature

| Field | Required |
|-------|----------|
| Signatory Name | Printed full name |
| Title | Authorized person (executive officer, director, or general partner) |
| Date | Date of execution |

Include certification that signatory has reviewed the filing and information is true and correct in all material respects. Electronic signatures acceptable per EDGAR authentication requirements.

## Guidelines

- **15-day deadline** — file no later than 15 days after first sale of securities
- **Amendments** — required for material changes, new solicitation states, or annually for ongoing offerings
- **Cross-reference** — verify all entries against organizational documents, offering materials, and actual conduct
- **Public record** — Form D is publicly available on EDGAR; avoid inadvertent disclosure of confidential terms
- **State blue sky** — federal Form D does not satisfy state notice filing requirements; flag need for separate state filings
- **No legal opinions** — flag uncertainties about exemption qualification for attorney review
- Mark unverified statutory thresholds or citations with `[VERIFY]`
