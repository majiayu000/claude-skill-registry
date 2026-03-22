---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: contract-review
description: "Analyze contracts for risks, check completeness, and provide actionable recommendations. Supports employment contracts, NDAs, service agreements, and more."
version: "1.0.0"
author: claude-office-skills
license: MIT

# Categorization
category: legal
tags:
  - contract
  - review
  - risk-analysis
  - legal
  - compliance
department: Legal

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
# Skills = Solution Guide (WHAT + HOW)
# MCP = Tool Provider (WITH WHAT)
mcp:
  server: office-mcp
  tools:
    - extract_text_from_pdf
    - extract_text_from_docx
    - analyze_document_structure
  optional_tools:
    - create_docx
    - docx_to_pdf

# Knowledge Base Integration
# Knowledge = Domain expertise as structured data
knowledge:
  base:
    - mcp-servers/office-mcp/knowledge/base/risk_patterns.json
    - mcp-servers/office-mcp/knowledge/base/completeness.json
  jurisdictions:
    - mcp-servers/office-mcp/knowledge/base/jurisdictions/us.json
    - mcp-servers/office-mcp/knowledge/base/jurisdictions/china.json
    - mcp-servers/office-mcp/knowledge/base/jurisdictions/eu.json
  custom:
    # Users can add their own knowledge files here
    # Example: ./knowledge/my_company_rules.json

# Skill Capabilities (for discovery/matching)
capabilities:
  - contract_analysis
  - risk_identification
  - legal_compliance_check
  - negotiation_recommendations

# Input/Output Specification
input:
  required:
    - type: file
      formats: [pdf, docx, txt]
      description: The contract document to review
    - type: text
      name: party_role
      description: Which party you are (employee, contractor, buyer, etc.)
  optional:
    - type: text
      name: jurisdiction
      description: Legal jurisdiction (US, EU, China, UK)
    - type: text
      name: concerns
      description: Specific areas of concern

output:
  primary:
    type: report
    format: markdown
    sections:
      - risk_summary
      - detailed_findings
      - completeness_check
      - negotiation_priorities

# Language Support
languages:
  - en
  - zh

# Related Skills
related_skills:
  - nda-generator
  - offer-letter
  - contract-template
---

# Contract Review Skill

## Overview

I help you review contracts by identifying potential risks, checking for missing elements, and providing specific recommendations. I have knowledge of common risk patterns and jurisdiction-specific rules.

**What I can do:**
- Identify 15+ common contract risks
- Check if your contract is complete
- Explain complex legal language in plain terms
- Suggest specific changes to protect your interests
- Support US, EU, China, and UK jurisdictions

**What I cannot do:**
- Provide legal advice (I'm an AI, not a lawyer)
- Guarantee legal compliance
- Replace professional legal review for high-stakes contracts

---

## How to Use Me

### Step 1: Share Your Contract
Upload your contract file (PDF, DOCX, or paste text) and tell me:
- What type of contract is this? (employment, NDA, service, lease, etc.)
- Which party are you? (employee, contractor, buyer, seller, etc.)
- What jurisdiction/country?
- Any specific concerns?

### Step 2: I Will Analyze
I'll review the contract and provide:
1. **Risk Summary** - High/Medium/Low risks found
2. **Clause Analysis** - Specific problematic clauses
3. **Completeness Check** - Missing standard elements
4. **Recommendations** - What to negotiate or change

### Step 3: Ask Follow-ups
Feel free to ask:
- "Explain Section 5 in simple terms"
- "What's the worst case if I sign this?"
- "How do I negotiate the non-compete clause?"
- "Is this normal for [industry]?"

---

## Risk Patterns I Look For

### High Risk (Red Flags)

#### 1. Unlimited Liability
**What it means:** You could be responsible for unlimited damages.
**Look for:** "unlimited liability", "full indemnification", no liability cap
**Recommendation:** Add liability cap (e.g., 12 months of fees, or contract value)

#### 2. Broad IP Assignment
**What it means:** You give away all intellectual property, including work you did before.
**Look for:** "all intellectual property", "work product", "inventions", "work for hire"
**Recommendation:** Exclude pre-existing IP; define scope clearly; check state protections (CA Labor Code 2870)

#### 3. Unilateral Termination
**What it means:** The other party can end the contract anytime, but you can't.
**Look for:** "at will", "unilateral termination", "without cause", "sole discretion"
**Recommendation:** Require mutual termination rights or reasonable notice period

#### 4. One-Sided Indemnification
**What it means:** Only you bear responsibility for problems, not them.
**Look for:** "indemnify and hold harmless", "defend at own expense", "all claims"
**Recommendation:** Negotiate mutual indemnification

#### 5. Broad Rights Waiver
**What it means:** You give up legal rights you're entitled to.
**Look for:** "waive", "waiver of rights", "release all claims", "forever discharge"
**Recommendation:** Remove or limit scope; some waivers may be unenforceable

#### 6. Missing Data Protection
**What it means:** No provisions for how personal data is handled (GDPR/CCPA risk).
**Look for:** Absence of "personal data", "GDPR", "privacy", "data protection"
**Recommendation:** Add data protection clause compliant with applicable laws

### Medium Risk (Yellow Flags)

#### 7. Auto-Renewal Trap
**What it means:** Contract renews automatically with difficult opt-out.
**Look for:** "automatically renew", "unless written notice", "evergreen"
**Recommendation:** Add clear opt-out with 30-day notice minimum

#### 8. Excessive Penalty
**What it means:** Penalty for breach exceeds reasonable damages.
**Look for:** "penalty", "liquidated damages", "forfeit"
**Recommendation:** Ensure penalty is proportionate to actual damages

#### 9. Broad Non-Compete
**What it means:** Restrictions on future work that are too broad.
**Look for:** "non-compete", "non-competition", "competitive business"
**Recommendation:** Limit to 1-2 years, specific geography, narrow scope
**Note:** California: generally unenforceable; FTC proposing ban (pending)

#### 10. Perpetual Confidentiality
**What it means:** Confidentiality obligations that never expire.
**Look for:** "perpetual", "indefinite", "forever", "in perpetuity"
**Recommendation:** Set reasonable time limit (3-5 years typical)

#### 11. Unfavorable Jurisdiction
**What it means:** Disputes resolved in a place far from you or favoring them.
**Look for:** "jurisdiction", "arbitration venue", "exclusive venue"
**Recommendation:** Negotiate neutral venue or your local jurisdiction

#### 12. Unfavorable Payment Terms
**What it means:** Long payment cycles or subjective acceptance criteria.
**Look for:** "net 90", "upon satisfaction", "when commercially reasonable"
**Recommendation:** Negotiate shorter cycles (net 30), objective acceptance criteria

#### 13. Uncontrolled Scope Changes
**What it means:** No process for managing changes to work scope.
**Look for:** "change order", "as directed", "scope change", "additional work"
**Recommendation:** Add change management process with pricing mechanism

#### 14. Missing Force Majeure
**What it means:** No provision for unforeseeable events (pandemic, disaster).
**Look for:** Absence of "force majeure", "act of god"
**Recommendation:** Add standard force majeure clause

### Low Risk (Worth Noting)

#### 15. Missing Audit Rights
**What it means:** No right to verify compliance or check records.
**Look for:** Absence of "inspection", "audit rights", "records access"
**Recommendation:** Add reasonable audit rights for significant contracts

---

## Completeness Checklist

A well-drafted contract should include:

### Essential Elements
- [ ] **Parties**: Full legal names and addresses of all parties
- [ ] **Effective Date**: When the contract begins
- [ ] **Term/Duration**: How long the contract lasts
- [ ] **Scope**: What's being provided/delivered
- [ ] **Compensation**: Payment amount, schedule, and method
- [ ] **Termination**: How and when the contract can be ended

### Important Clauses
- [ ] **Confidentiality**: How sensitive information is protected
- [ ] **Intellectual Property**: Who owns created work
- [ ] **Liability Limits**: Caps on responsibility
- [ ] **Indemnification**: Who covers what damages
- [ ] **Governing Law**: Which jurisdiction's laws apply
- [ ] **Dispute Resolution**: How disagreements are handled

### Execution
- [ ] **Signature Blocks**: Space for all parties to sign
- [ ] **Date Lines**: When signatures were added
- [ ] **Witness/Notary**: If required by type or jurisdiction

---

## Jurisdiction-Specific Knowledge

### United States

#### Employment Contracts
- **At-Will Default**: Most states allow termination without cause (except Montana)
- **Exempt vs Non-Exempt**: Critical classification for overtime eligibility
  - Non-exempt: Entitled to overtime (1.5x after 40 hrs/week)
  - Exempt: Must meet salary threshold ($684/week) AND duties test
- **Minimum Wage**: Federal $7.25/hr, but many states higher (CA: $16/hr)
- **Non-Competes**: Void in California; FTC proposing nationwide ban

#### State Variations
| State | Key Differences |
|-------|-----------------|
| **California** | Daily overtime after 8hrs; non-competes void; strong employee protections |
| **Texas** | Strong at-will; non-competes enforceable if reasonable |
| **New York** | NYC extra protections; salary history ban; paid family leave |

### European Union

- **GDPR Compliance**: Data processing agreements required
- **Working Time Directive**: Max 48 hrs/week average
- **Notice Periods**: Often legally mandated (1-3 months common)
- **Non-Competes**: Must be compensated in many countries
- **Language**: May need to be in local language to be enforceable

### China

- **Labor Contract Law**: Mandatory written contract within 30 days
- **Probation Period**: Limited by contract length (max 6 months)
- **Non-Compete**: Must pay compensation (30-50% of salary) during restriction
- **Severance**: Required for many termination scenarios
- **Social Insurance**: Contributions mandatory (pension, medical, etc.)

### United Kingdom

- **Statutory Rights**: Cannot contract out of employment rights
- **Notice Periods**: Minimum 1 week per year of service (up to 12)
- **Restrictive Covenants**: Must be reasonable to be enforceable
- **TUPE**: Employee rights protected in business transfers

---

## Output Format

When I review your contract, I'll provide:

```
## Contract Analysis Report

**Document**: [Contract Name]
**Type**: [Employment/Service/NDA/etc.]
**Jurisdiction**: [Country/State]
**Your Role**: [Which party you are]

---

### Risk Summary

| Severity | Count | Key Issues |
|----------|-------|------------|
| 🔴 High  | X     | [Brief list] |
| 🟡 Medium| X     | [Brief list] |
| 🟢 Low   | X     | [Brief list] |

**Overall Assessment**: [SAFE / REVIEW NEEDED / HIGH RISK]

---

### Detailed Findings

#### 🔴 High Risk Issues

**1. [Issue Name]** (Section X.X)
> "[Exact quote from contract]"

- **Problem**: [What's wrong]
- **Impact**: [How it affects you]
- **Recommendation**: [Specific change to request]

[...continue for each issue...]

---

### Completeness Check

✅ Present:
- [List of included elements]

⚠️ Missing or Unclear:
- [List of missing elements with recommendations]

---

### Negotiation Priorities

1. **Must Change**: [Most critical issues]
2. **Should Change**: [Important but negotiable]
3. **Nice to Have**: [Lower priority improvements]

---

### Disclaimer

This analysis is for informational purposes only and does not constitute 
legal advice. For important contracts, consult a qualified attorney.
```

---

## Example Interactions

### Example 1: Employment Contract Review

**User**: Review this employment contract. I'm the employee, this is for a US company in California.

**Me**: [After analysis]

## Contract Analysis Report

**Document**: Employment Agreement
**Type**: Employment Contract  
**Jurisdiction**: United States (California)
**Your Role**: Employee

### Risk Summary

| Severity | Count | Key Issues |
|----------|-------|------------|
| 🔴 High  | 2     | IP assignment too broad, No liability cap |
| 🟡 Medium| 3     | Non-compete (unenforceable in CA), Auto-renewal, Arbitration |
| 🟢 Low   | 1     | No audit rights |

**Overall Assessment**: ⚠️ REVIEW NEEDED

### Detailed Findings

#### 🔴 High Risk Issues

**1. Broad IP Assignment** (Section 5.1)
> "Employee assigns to Company all right, title and interest in any and all inventions, discoveries, and work product..."

- **Problem**: This assigns ALL inventions, including personal projects
- **Impact**: Even code you write on weekends for personal projects could belong to the company
- **Recommendation**: Add California Labor Code 2870 language: "This does not apply to inventions developed entirely on Employee's own time without using Company resources, unless related to Company's business."

**2. Non-Compete Clause** (Section 9)
> "Employee agrees not to work for any competitor for 24 months after termination..."

- **Problem**: Attempts to restrict future employment
- **Impact**: In California, this is **unenforceable** under Business & Professions Code 16600
- **Recommendation**: Request removal. If they refuse, don't worry - it's void in CA anyway.

---

### Example 2: Quick Question

**User**: Is a 3-year non-compete normal?

**Me**: No, 3 years is longer than typical. Here's the context:

| Duration | Assessment |
|----------|------------|
| 6 months | Short, usually reasonable |
| 1 year | Common, often enforceable |
| 2 years | Upper limit of reasonableness |
| 3 years | **Excessive** - likely unenforceable in many jurisdictions |

**Important**: In California, non-competes are void regardless of duration. Many other states require they be "reasonable" - 3 years usually fails this test.

**Recommendation**: Negotiate down to 1 year maximum, or request removal entirely.

---

## Tips for Better Results

1. **Tell me your role**: Are you the employee, contractor, buyer, or seller?
2. **Specify jurisdiction**: US? Which state? EU? China?
3. **Share context**: Is this a job you really want? Big client? High stakes?
4. **Ask follow-ups**: I can explain any clause in more detail
5. **Use me iteratively**: Review → Negotiate → Review revised version

---

## Limitations

- I provide general guidance, not legal advice
- My knowledge may not reflect the latest legal changes
- Some risks are industry-specific and may need expert review
- For high-stakes contracts (M&A, major deals), always use a lawyer
- I can't verify if the other party will actually follow the contract

---

## Languages

This skill works with contracts in multiple languages including English and Chinese. 
Feel free to share contracts in either language - I can analyze and respond accordingly.

---

*Built by the Claude Office Skills community. Contributions welcome!*
