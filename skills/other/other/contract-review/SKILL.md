---
name: contract-review
description: Analyze and red-flag contracts systematically, identifying risks, unfavorable terms, and negotiation opportunities
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Contract Review

> Systematically analyze contracts to identify risks, unfavorable clauses, and negotiation opportunities before signing.

## When to Use This Skill

- Reviewing vendor/SaaS contracts
- Analyzing partnership agreements
- Evaluating client service agreements
- Reviewing employment contracts
- Due diligence on M&A documents

## Methodology Foundation

Based on **legal contract analysis frameworks** combined with:
- Risk assessment matrices
- Common clause libraries
- Industry-standard benchmarks
- Negotiation leverage analysis

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Identifies risky clauses | Risk tolerance level |
| Flags unusual terms | What to negotiate |
| Compares to standards | Final accept/reject |
| Suggests alternatives | Business trade-offs |
| Summarizes obligations | Legal counsel needs |

## Instructions

### Step 1: Contract Overview

**Initial Assessment:**
| Element | What to Capture |
|---------|-----------------|
| Parties | Who's bound |
| Type | Service, license, partnership |
| Term | Duration, renewal |
| Value | Total commitment |
| Jurisdiction | Governing law |

### Step 2: Risk Categories

**Clause Risk Matrix:**
| Category | Low Risk | Medium Risk | High Risk |
|----------|----------|-------------|-----------|
| **Liability** | Mutual caps | Uncapped | Unlimited indemnity |
| **Term** | Monthly | Annual | Multi-year auto-renew |
| **Data** | Standard DPA | Custom terms | Broad usage rights |
| **IP** | License only | Work for hire | Assignment |
| **Termination** | 30-day notice | For cause only | Penalties |

### Step 3: Clause-by-Clause Analysis

**Key Clauses to Review:**

**Payment Terms:**
- Net terms (30/60/90)
- Late payment penalties
- Price escalation clauses
- Audit rights

**Liability & Indemnification:**
- Cap on liability (multiple of fees)
- Carve-outs (willful misconduct, IP)
- Indemnification scope
- Insurance requirements

**Termination:**
- For convenience vs. for cause
- Notice periods
- Transition assistance
- Data return/destruction

**IP & Data:**
- Ownership of deliverables
- License scope
- Data usage rights
- Confidentiality obligations

### Step 4: Benchmarking

**Industry Standards:**
| Clause | Typical | Favorable | Unfavorable |
|--------|---------|-----------|-------------|
| Liability cap | 12 mo fees | 24 mo fees | Uncapped |
| Payment | Net 30 | Net 45 | Net 15 |
| Termination | 30 days | 60 days | 90+ days |
| Auto-renewal | 30-day opt-out | 60-day opt-out | 90-day opt-out |

### Step 5: Generate Recommendations

**Output Structure:**
1. Executive summary (2-3 sentences)
2. Risk rating (Low/Medium/High/Critical)
3. Red flags (must address)
4. Yellow flags (should negotiate)
5. Green flags (acceptable)
6. Recommended redlines
7. Questions for counsel

## Examples

### Example 1: SaaS Vendor Contract Review

**Input:**
```
Review this SaaS contract summary:
- 3-year term with 90-day auto-renewal notice
- Unlimited liability for data breaches
- Vendor can change pricing with 30-day notice
- Data can be used for "service improvement"
- Termination only for material breach
```

**Output:**
```
## Contract Review: SaaS Vendor Agreement

### Risk Rating: HIGH

---

### Executive Summary

This contract heavily favors the vendor with limited termination rights, uncapped liability exposure for you, and one-sided price increase provisions. Recommend significant negotiation before signing.

---

### Red Flags (Must Address)

| Clause | Issue | Risk | Recommendation |
|--------|-------|------|----------------|
| **Auto-Renewal** | 90-day notice for 3-year contract | Lock-in risk | Reduce to 30-60 days |
| **Pricing** | Vendor can change with 30-day notice | Budget risk | Cap increases at 5%/year or CPI |
| **Termination** | Material breach only | Lock-in risk | Add termination for convenience with notice |
| **Liability** | Unlimited for data breaches | Financial risk | Cap at 24 months of fees |

---

### Yellow Flags (Should Negotiate)

| Clause | Issue | Recommendation |
|--------|-------|----------------|
| **Data Usage** | "Service improvement" is vague | Define scope, exclude training AI |
| **Term Length** | 3 years is long | Request 1-year with renewal option |
| **SLA** | None mentioned | Require 99.9% uptime with credits |

---

### Green Flags (Acceptable)

- Standard confidentiality provisions
- Reasonable IP license terms
- Clear support response times

---

### Recommended Redlines

**Priority 1 (Deal Breakers):**
```
Section 8.2: Change "90 days" to "30 days"
Section 12.1: Add "and termination for convenience
              with 60 days written notice"
Section 14.3: Add "not to exceed 24 months of fees
              paid under this Agreement"
```

**Priority 2 (Strongly Preferred):**
```
Section 5.1: Add "Price increases shall not exceed
              5% annually"
Section 9.4: Change "service improvement" to
              "providing and improving the Service
              for Customer"
```

---

### Questions for Legal Counsel

1. Is unlimited data breach liability acceptable given our cyber insurance coverage?
2. What's our exposure if we need to exit before term completion?
3. Are there regulatory implications for the data usage clause?

---

### Negotiation Leverage

**Your Position:** First-year customer, significant deal size

**Their Likely Flex:**
- Auto-renewal notice period
- Liability caps
- Pricing caps

**Their Likely Firm:**
- Base term length
- Core data usage rights
```

### Example 2: Quick Risk Assessment

**Input:**
```
Quick review - key concerns only:
- Unlimited indemnification for IP claims
- 2x annual fees liability cap
- Net 45 payment terms
- 60-day termination notice
- Standard DPA included
```

**Output:**
```
## Quick Risk Assessment

### Overall: MEDIUM RISK

| Clause | Rating | Note |
|--------|--------|------|
| Indemnification | HIGH | Unlimited IP indemnity is risky |
| Liability Cap | GREEN | 2x is standard |
| Payment | GREEN | Net 45 is favorable |
| Termination | GREEN | 60 days is reasonable |
| Data Protection | GREEN | Standard DPA |

### Priority Action

**Address Indemnification:**
- Request mutual cap on IP indemnity
- Propose "lesser of [amount] or 12 months fees"
- Alternative: carve out for willful infringement only

**Everything Else:** Acceptable, proceed if IP indemnity resolved.
```

## Skill Boundaries

### What This Skill Does Well
- Identifying common risk patterns
- Comparing to industry benchmarks
- Structuring negotiation priorities
- Flagging unusual clauses

### What This Skill Cannot Do
- Provide legal advice
- Know jurisdiction-specific requirements
- Assess strategic business importance
- Replace qualified legal counsel

### When to Escalate to Human
- Contracts over $100K annual value
- Non-standard or heavily negotiated terms
- Any regulated industry requirements
- Indemnification or liability questions

## Iteration Guide

**Follow-up Prompts:**
- "What's the worst-case scenario for the liability clause?"
- "Draft redline language for [specific clause]"
- "How does this compare to [competitor] contracts?"
- "What should we ask for in return if we accept [term]?"

## References

- ACC (Association of Corporate Counsel) Contract Guidelines
- IACCM Contract Terms Benchmarking
- Tech Contract Negotiation Best Practices
- Standard SaaS Agreement Templates

## Related Skills

- `rfp-response` - Creating proposals
- `nda-generator` - Confidentiality agreements
- `terms-analyzer` - Terms of service review

## Skill Metadata

- **Domain**: Legal
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 30-60 min per contract
- **Prerequisites**: Contract access, business context
