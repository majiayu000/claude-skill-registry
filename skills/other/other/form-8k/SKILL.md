---
name: form-8k
description: >-
  Drafts SEC Form 8-K current reports with item-accurate narratives, exhibit
  indexing, and EDGAR-ready formatting. Use when a public company must disclose
  a reportable event (material agreement, acquisition, personnel change, Reg FD
  disclosure) or file a current report within four business days. Trigger on
  "Form 8-K", "current report", "8-K filing", "EDGAR", "Item 1.01", "Item 2.01",
  "Item 5.02", "Reg FD".
---

# Form 8-K Current Report

Drafts an EDGAR-ready Form 8-K from verified source documents. Requires triggering event facts (dates, parties, terms), registrant identifiers from the latest 10-K/10-Q, item selection with rationale, and source documents (agreements, resolutions, press releases, employment/separation docs).

## Quick Start

1. Collect registrant identifiers: exact legal name, Commission File No., CIK, IRS EIN, state of incorporation, fiscal year end, address, phone, trading symbols.
2. Identify triggered items using the Item Selection Matrix below.
3. Gather source documents for each triggered item.
4. Draft cover page, item narratives, exhibit index, and signature block.
5. Run quality checks before finalizing.

## Cover Page Fields

All sourced from latest 10-K/10-Q cover unless noted:

- Registrant exact legal name, Commission File No., CIK, IRS EIN
- State of incorporation (charter or 10-K/10-Q)
- Fiscal year end, principal executive offices address and phone
- Trading symbol(s) and exchange(s) [VERIFY]
- Reporting item checkboxes and Rule 425/14a-12/14d-2/13e-4 communication checkboxes [VERIFY]
- If 8-K/A, indicate amendment

## Item Selection Matrix

| Item | Trigger | Required Narrative | Typical Exhibits |
|---|---|---|---|
| 1.01 | Material definitive agreement entered | Date, parties, purpose, key terms, duration, termination, conditions | Agreement (10.x) |
| 1.02 | Material definitive agreement terminated | Date, parties, reason, fees/obligations | Termination notice (10.x) |
| 2.01 | Acquisition/disposition completed | Date, assets/business, consideration, structure, significance | Purchase agreement (10.x), pro forma (99.x) |
| 2.02 | Results of operations/financial condition | Reference press release/presentation; note furnished status | Press release (99.x) |
| 2.03 | Direct financial or off-balance-sheet obligation created | Date, amount, terms, maturity, covenants, default events | Credit agreement (10.x) |
| 2.05 | Exit/disposal costs | Plan nature, expected charges, timing | Board materials (99.x) |
| 2.06 | Material impairment | Nature, amount, timing | Press release (99.x) |
| 3.02 | Unregistered equity sales | Date, securities, exemption, consideration | Subscription/SPA (10.x) |
| 5.02 | Director/officer appointment, departure, or compensation | Name, title, effective date, background, compensation | Offer/separation letter (10.x) |
| 5.03 | Charter/bylaws amendment or fiscal year change | Amendment description, effective date | Charter/bylaws (3.1/3.2) |
| 7.01 | Regulation FD disclosure | Description of furnished information | Presentation (99.x) |
| 8.01 | Other events | Factual description, materiality context | Press release (99.x) |
| 9.01 | Financial statements and exhibits | Identify financials, list all exhibits | FS/pro forma (99.x), agreements (10.x) |

## Narrative Drafting

Use objective, non-promotional language. Cite only verifiable facts. State event date and any different effective date. Use exact legal names and titles. Quantify all material dollar amounts. Align narratives with press releases and exhibits.

**Item 1.01 — Material Definitive Agreement:**

```text
On [Date], [Registrant] entered into [Agreement Title] with [Counterparty].
The agreement relates to [Purpose/Transaction].
Material terms: [Consideration], [Duration], [Termination Rights], [Key Conditions], [Material Covenants].
Effective [Effective Date]; terminable upon [Conditions].
```

**Item 5.02 — Personnel Change:**

```text
Effective [Date], [Name] was [appointed/resigned/terminated] as [Title].
Background: [Prior roles, relevant experience].
Compensation: [Base salary], [Bonus], [Equity], [Severance], [Other material terms].
No family relationships or related-party transactions with directors/officers, except [if any].
```

## Item 2.01 / 9.01 Financials

- Apply Reg S-X Rule 3-05 and Article 11 significance tests [VERIFY].
- Determine if audited target financials and pro forma financials are required.
- If unavailable, state they will be filed by amendment within 71 calendar days of the 8-K due date (Item 9.01 safe harbor) [VERIFY].

## Exhibit Index (Item 9.01(d))

| Exhibit No. | Description | Status |
|---|---|---|
| 2.1 | Purchase agreement for [Transaction] | Filed |
| 3.1 | Amended and Restated Certificate of Incorporation | Filed |
| 10.1 | Material definitive agreement | Filed |
| 99.1 | Press release dated [Date] | Furnished |
| 99.2 | Investor presentation dated [Date] | Furnished |

Filed = binding obligation or governance document. Furnished = Items 2.02 and 7.01 press releases and presentations (not subject to Section 18 liability).

## Signature Block

```text
Pursuant to the requirements of the Securities Exchange Act of 1934, the registrant has duly caused this report to be signed on its behalf by the undersigned hereunto duly authorized.

Date: [Filing Date]

[Registrant Name]

By: __________________________
Name: [Officer Name]
Title: [Officer Title]
```

## Quality Checks

- [ ] All dates, names, and amounts match source documents
- [ ] Item numbers match described events
- [ ] Exhibits referenced are attached and correctly numbered
- [ ] Items 2.02 and 7.01 materials are furnished (not filed)
- [ ] Narratives consistent with press releases and exhibits
- [ ] Signature authority documented or customary
- [ ] Filing deadline confirmed from triggering event date

## Pitfalls

- **No projections or opinions** unless required by the item or in furnished materials.
- **Forward-looking statements**: If an exhibit contains them, include cautionary language in that exhibit.
- **8-K/A**: Use for material corrections or delayed financials under Item 9.01.
- **Confidential treatment**: Flag Rule 24b-2 and prepare a separate application [VERIFY].
- **EDGAR formatting**: Maintain compatible formatting; avoid typographical inconsistencies.

---
