---
name: genres
description: '> Style/formatting: Follow ~/.claude/skills/word-doc-generator/SKILL.md'
---

# KNOW YOUR CUSTOMER (KYC) - Genre Template

> **Style/formatting:** Follow `~/.claude/skills/word-doc-generator/SKILL.md`

## Purpose

Streamlined due diligence for customer onboarding and ongoing monitoring. Focuses on identity verification, beneficial ownership, PEP/sanctions screening, and adverse media. Designed for compliance with AML/CFT regulations.

---

## WHEN TO USE

- New customer onboarding
- Periodic KYC refresh/review
- Enhanced due diligence triggers
- Account opening procedures
- Counterparty verification

---


## SOURCE INTELLIGENCE

> **See full details:** `sections/universal/RESEARCH_INTELLIGENCE.skill.md`

### KYC - Verification Limitations

| Area | Known Gaps | Friction |
|------|-----------|----------|
| **Identity Docs** | Cannot verify authenticity via OSINT; forgeries exist | N/A |
| **Address** | Electoral rolls incomplete; privacy protections increasing | `(pub)` to `(restr)` |
| **Source of Funds** | Requires documentation from subject; cannot verify via public sources | `(opaque)` |
| **Business Purpose** | Stated purpose cannot be verified without investigation | N/A |
| **Ongoing Monitoring** | Requires continuous screening; point-in-time reports insufficient | `(paid)` |

### KYC requires direct documentation from subject; OSINT provides corroboration only.

### Cross-reference `jurisdictions/[COUNTRY].skill.md` for jurisdiction-specific limitations.

---

## REPORT STRUCTURE

### Required Sections (In Order)

1. **Executive Summary** → `sections/universal/EXECUTIVE_SUMMARY.skill.md`
2. **Identity Verification** → `sections/company/COMPANY_OVERVIEW.skill.md`
3. **Ownership & Ultimate Beneficial Owner** → `sections/company/OWNERSHIP_SHAREHOLDERS.skill.md`
4. **PEP Status** → `sections/universal/PEP_STATUS.skill.md`
5. **Sanctions & Watchlists** → `sections/universal/SANCTIONS_WATCHLISTS.skill.md`
6. **Adverse Media** → `sections/universal/ADVERSE_MEDIA.skill.md`
7. **Research Limitations** → `sections/universal/RESEARCH_LIMITATIONS.skill.md`

---

## IDENTITY VERIFICATION TEMPLATE

```markdown
## Identity Verification

### Entity Identification

| Field | Value |
|-------|-------|
| **Legal Name** | [FULL_LEGAL_NAME] |
| **Registration Number** | [NUMBER] |
| **Jurisdiction** | [COUNTRY] |
| **Date of Incorporation** | [DATE] |
| **Registered Address** | [ADDRESS] |
| **Trading Names** | [IF ANY] |

### Verification Sources

| Source | Status | Date Verified |
|--------|--------|---------------|
| Company Registry | [Verified/Unable to verify] | [DATE] |
| Regulatory Register | [Verified/N/A] | [DATE] |
| Website | [Verified/N/A] | [DATE] |

### Discrepancies Noted

[IF ANY:]
- [DISCREPANCY 1]
- [DISCREPANCY 2]

[IF NONE:]
No discrepancies identified between declared information and registry records.
```

---

## UBO IDENTIFICATION TEMPLATE

```markdown
## Ultimate Beneficial Ownership

### UBO Summary

| Name | Ownership % | Nationality | PEP Status | Verification |
|------|-------------|-------------|------------|--------------|
| **[NAME]** | [X]% | [COUNTRY] | [Yes/No] | [Registry/Declaration] |

### Ownership Chain

[DESCRIBE OWNERSHIP STRUCTURE - can be simple or include diagram reference]

**Direct Shareholders:**
1. [SHAREHOLDER 1] - [X]%
2. [SHAREHOLDER 2] - [X]%

**Ultimate Beneficial Owners (>25%):**
1. [UBO 1] - Controls [X]% via [CHAIN]

### Verification Status

- [ ] UBO declaration obtained
- [ ] Registry verification complete
- [ ] ID documents verified (if EDD)
- [ ] Source of wealth verified (if EDD)
```

---

## RISK RATING TEMPLATE

```markdown
## KYC Risk Assessment

### Risk Factors

| Factor | Rating | Notes |
|--------|--------|-------|
| **Country Risk** | [High/Medium/Low] | [JURISDICTION] |
| **Industry Risk** | [High/Medium/Low] | [SECTOR] |
| **Product Risk** | [High/Medium/Low] | [PRODUCTS/SERVICES] |
| **Channel Risk** | [High/Medium/Low] | [Non-face-to-face/etc.] |
| **PEP Exposure** | [Yes/No] | [DETAILS] |
| **Sanctions Exposure** | [Yes/No] | [DETAILS] |
| **Adverse Media** | [Yes/No] | [DETAILS] |

### Overall Risk Rating

**[HIGH / MEDIUM / LOW]**

[RATIONALE FOR RATING]

### Recommended Actions

- [ACTION 1]
- [ACTION 2]
```

---

## STANDARD PHRASES

**Clean customer:**
> KYC screening identified no adverse findings. The customer presents a [low/medium] risk profile based on the factors assessed.

**PEP identified:**
> [NAME] is identified as a Politically Exposed Person ([CATEGORY]). Enhanced due diligence is recommended.

**Adverse findings:**
> KYC screening identified matters requiring attention, including [BRIEF_LIST]. Enhanced due diligence is recommended before onboarding.

**UBO not verified:**
> Ultimate beneficial ownership could not be fully verified from public sources. Additional documentation should be requested from the customer.

---

## EDD TRIGGERS

Enhanced Due Diligence should be applied when:

- PEP or PEP-connected
- High-risk jurisdiction (FATF grey/black list)
- Complex ownership structure
- High-risk industry (crypto, gambling, weapons, etc.)
- Adverse media identified
- Sanctions near-match
- Unusual transaction patterns

---

## DISCLAIMERS

**See `library/DISCLAIMERS.skill.md`**:
- KYC screening disclaimer
- Point-in-time limitation
- Public source reliance

---

## TYPICAL DURATION

- Standard KYC: 1-2 business days
- Enhanced KYC: 3-5 business days
