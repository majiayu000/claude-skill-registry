---
name: deed-of-trust
description: Drafts combined Deed of Trust and Security Agreement instruments creating real property and UCC Article 9 personal property security interests for commercial financing. Use when drafting trust deeds, security agreements, commercial real estate financing documents, or combined real/personal property security instruments.
---

# Deed of Trust and Security Agreement

Drafts a combined instrument creating enforceable security interests in both real property (deed of trust) and personal property (UCC Article 9 security agreement) for commercial real estate financing.

## Prerequisites

1. **Loan documents** — promissory note, loan agreement, related transaction docs
2. **Parties** — full legal names, addresses, entity status for Grantor (borrower/debtor), Trustee, and Beneficiary (lender/secured party)
3. **Real property** — legal description from chain of title, street address, APN, title report with encumbrances
4. **Personal property** — specific items, serial numbers, equipment lists, account descriptions
5. **Jurisdiction** — situs state (determines property theory, foreclosure process, execution requirements)

## Workflow

### Step 1: Extract Information

| Data Point | Source |
|---|---|
| Parties (names, addresses, entity type) | Loan agreement, formation docs |
| Loan terms (amount, rate, maturity, payments) | Promissory note |
| Legal description + APN | Title report, prior deed |
| Encumbrances / title exceptions | Title commitment |
| Personal property collateral | Equipment lists, inventory schedules |
| Notice addresses, insurance requirements | Loan agreement |

### Step 2: Determine Jurisdictional Requirements

Research before drafting — these vary significantly by state:

- **Property theory** — title, lien, or intermediate → controls conveyance language
- **Foreclosure** — non-judicial (trustee's sale) vs. judicial; deficiency judgment availability
- **Statutory requirements** — notice periods, cure periods, publication rules, redemption rights
- **Execution formalities** — notarization, witnesses, spousal/homestead consent
- **Recording requirements** — format, margin, font, indexing standards
- **Community property / homestead** — whether spousal joinder required

### Step 3: Draft Document

Sections in order:

1. Parties
2. Recitals
3. Property description (real + personal)
4. Grant of deed of trust
5. Security agreement (UCC Article 9)
6. Representations and warranties
7. Affirmative covenants
8. Negative covenants
9. Events of default
10. Remedies
11. Environmental indemnification
12. Subordination / attornment (if leased property)
13. Miscellaneous
14. Execution / acknowledgment

### Section-Specific Requirements

**Property description:**
- Real: full legal description + street address + APN + fixtures, improvements, appurtenances, easements
- Personal: must satisfy UCC Section 9-108 sufficiency — include specific items, inventory, equipment, accounts, general intangibles, and proceeds

**Grant of deed of trust:**
- Jurisdiction-standard granting language, absolute in form, defeasible on satisfaction
- Define trustee powers: sale authority, substitution, liability limitations

**Security agreement (UCC Article 9):**
- Satisfy attachment: authenticated agreement + value + debtor's rights in collateral
- Include authorization for UCC-1 financing statement filing
- Address after-acquired property and proceeds

**Covenants:**

| Affirmative | Negative |
|---|---|
| Timely payment | No waste |
| Maintain insurance (Beneficiary as loss payee) | No unauthorized transfers or junior liens |
| Pay taxes and assessments | No material alterations without consent |
| Maintain and repair property | No disposal of personal property collateral |
| Comply with laws | No relocation of collateral without consent |

**Events of default:**
- Non-payment (specify grace period)
- Covenant/representation breach (cure period for non-monetary)
- Cross-default to related agreements
- Bankruptcy / insolvency
- Material adverse change in financial condition or collateral value

**Remedies — dual track:**

| Real Property | Personal Property (UCC Art. 9) |
|---|---|
| Trustee's sale per state statute | Right to take possession |
| Judicial foreclosure (if available) | Public or private disposition |
| Receiver appointment | Retention in satisfaction of debt |
| Notice, publication, sale, proceeds distribution | Commercially reasonable disposition required |

**Governing law:**
- Real property provisions → situs state law
- UCC provisions → UCC choice-of-law rules (Section 9-301 et seq.)
- Include conflict-of-law analysis if split governance

**Execution:**
- Jurisdiction-specific notarized acknowledgment
- Check witness requirements
- Corporate/LLC authority recitals + authorized officer signature blocks
- Spousal consent block if community property or homestead jurisdiction

## Critical Checks

- **Jurisdiction controls everything** — never assume uniform rules across states for foreclosure, cure periods, redemption, or execution formalities
- **Spousal joinder** — always verify whether required and whether waiver is enforceable in the jurisdiction
- **UCC-1 filing** — flag whether financing statement filing is needed for perfection; include authorization language regardless
- **Environmental** — include indemnification for commercial property; flag Phase I/II assessments if in uploaded documents
- **Waiver enforceability** — verify any waiver of redemption rights, homestead exemptions, or jury trial is enforceable before including
- **Internal consistency** — cross-check defined terms, cross-references, and collateral descriptions between trust deed and security agreement sections
- **Statutory citations** — mark with `[VERIFY]` unless confirmed from uploaded jurisdiction-specific materials

---

Key changes from the original:
- **Removed `tags`** from frontmatter (not part of the spec — only `name` and `description`)
- **Trimmed description** — removed redundant detail while keeping trigger keywords
- **Restructured body** — renamed phases to "Step 1/2/3" under a single "Workflow" heading, renamed "Guidelines" to "Critical Checks"
- **Removed the code fence** around the document structure outline — replaced with a plain numbered list
- **Consolidated redundant content** — removed the Representations & Warranties table (content is standard and doesn't need enumeration), merged notice addresses/insurance into one extraction row
- **Reduced from 145 lines to ~120** — tighter without losing any domain accuracy or legal precision
