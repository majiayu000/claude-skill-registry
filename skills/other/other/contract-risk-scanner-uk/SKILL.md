---
name: contract-risk-scanner-uk
description: Review UK property and pensions contracts, extract key terms, identify legal risks, compare against standard terms, generate compliance checklist. Use when reviewing contracts, agreements, legal documents, conveyancing, pensions agreements. Keywords: contract, risk, terms, compliance, conveyancing, pensions, legal, agreement, clause, liability.
allowed-tools: Read, Bash(grep:*), Glob, mcp__neo4j-apex__*, mcp__neo4j-cms-handbook__*, mcp__archon__rag_search_knowledge_base
model: claude-opus-4-5-20251101
context: fork
agent: general-purpose
---

# UK Contract Risk Scanner

## Purpose

Analyze UK property conveyancing and pensions contracts to extract key terms, identify legal risks, compare against standard terms, and generate compliance checklists. Specialized for UK legal requirements.

## Contract Types Supported

### Property/Conveyancing
- Sale and purchase agreements
- Lease agreements
- Property management contracts
- Searches and surveys contracts
- Mortgage offers

### Pensions
- Trust deeds
- Investment management agreements
- Administration service contracts
- Actuarial services agreements
- Custodian agreements
- Member agreements (AVCs, transfers)

### General Commercial
- Service agreements
- Consultancy contracts
- Software licenses
- Data processing agreements (GDPR)

## Risk Analysis Workflow

### Phase 1: Document Intake and Classification

**Step 1: Load contract**
```
# Read contract document
Read(file_path="[contract-path]")

# Or search for contracts in directory
Glob(pattern="**/*{contract,agreement,deed}*.{pdf,docx,txt}")
```

**Step 2: Classify contract type**

Identify:
- Contract type (property/pensions/commercial)
- Parties involved
- Jurisdiction (England & Wales, Scotland, Northern Ireland)
- Governing law
- Contract date and term

**Step 3: Extract metadata**

```markdown
## Contract Metadata

**Contract Type**: [Type]
**Parties**:
- Party A: [Name, Company Number]
- Party B: [Name, Company Number]

**Key Dates**:
- Execution Date: [Date]
- Commencement Date: [Date]
- Expiry Date: [Date] or "No fixed term"

**Jurisdiction**: [England & Wales/Scotland/NI]
**Governing Law**: [English Law/Scots Law]

**Value**: £[Amount] or description
**Term**: [Duration]
```

### Phase 2: Extract Key Terms

**Essential contract terms**:

```markdown
## Key Terms Extracted

### Parties and Representatives
- **Contracting Parties**: [Names]
- **Authorized Representatives**: [Names, roles]
- **Notice Addresses**: [Addresses for legal notices]

### Financial Terms
- **Contract Value**: £[Amount]
- **Payment Terms**: [Net 30 days / staged payments / on completion]
- **Price Variation**: [Fixed / index-linked / review mechanism]
- **VAT Treatment**: [Standard/exempt/reverse charge]
- **Late Payment**: [Interest rate, penalties]

### Performance Obligations
- **Deliverables**: [What each party must provide]
- **Performance Standards**: [KPIs, SLAs]
- **Timescales**: [Deadlines, milestones]
- **Acceptance Criteria**: [How performance is verified]

### Term and Termination
- **Initial Term**: [Duration]
- **Renewal**: [Automatic/optional, notice period]
- **Termination Rights**:
  - Convenience: [Notice period, break clauses]
  - For cause: [Material breach, insolvency]
  - Force majeure: [Scope, suspension vs termination]

### Liability and Indemnity
- **Liability Cap**: £[Amount] or [Multiple of fees]
- **Excluded Losses**: [Consequential loss, loss of profit, etc.]
- **Indemnities**: [Who indemnifies whom, for what]
- **Insurance**: [Types required, minimum amounts]

### Intellectual Property
- **Ownership**: [Who owns what]
- **Licenses**: [Rights granted, limitations]
- **Background IP**: [Pre-existing rights]
- **Moral Rights**: [Waived/retained]

### Data Protection (GDPR)
- **Controller/Processor**: [Role definitions]
- **Data Processing Terms**: [Schedule reference]
- **Data Subject Rights**: [How handled]
- **Security Requirements**: [Standards, breach notification]

### Confidentiality
- **Definition**: [What is confidential]
- **Exceptions**: [Standard carve-outs]
- **Term**: [Duration after contract end]

### Dispute Resolution
- **Governing Law**: [English/Scots law]
- **Jurisdiction**: [Courts of England & Wales/Scotland]
- **Alternative DR**: [Mediation, arbitration, expert determination]
```

### Phase 3: Risk Identification

**Risk categories with severity scoring**:

#### High Risk 🔴

**1. Unlimited Liability**
```
❌ RISK: No liability cap or exclusions
CLAUSE: [Quote relevant clause]
IMPACT: Unlimited financial exposure
MITIGATION: Negotiate cap at [X times annual fees / £Y amount]
```

**2. Onerous Indemnities**
```
❌ RISK: Broad indemnity with no carve-outs
CLAUSE: "[Quote]"
IMPACT: Liability for third-party acts outside your control
MITIGATION: Add negligence qualifier, cap indemnity, require insurance
```

**3. Automatic Renewal Without Exit**
```
❌ RISK: Auto-renewal with long notice period
CLAUSE: "[Quote]"
IMPACT: Locked in for [X years] even if service poor
MITIGATION: Reduce notice period to [30/60/90] days
```

**4. Intellectual Property Assignment**
```
❌ RISK: All IP created vests in other party
CLAUSE: "[Quote]"
IMPACT: Loss of valuable IP, limits reuse
MITIGATION: Retain ownership, grant license only
```

**5. Data Controller Risk (GDPR)**
```
❌ RISK: Acting as data controller without DPO/systems
CLAUSE: "[Quote]"
IMPACT: ICO fines up to £17.5M or 4% turnover
MITIGATION: Clarify processor role, require client instructions
```

#### Medium Risk 🟡

**6. Payment Terms**
```
⚠️ RISK: Extended payment terms without security
CLAUSE: "[Quote]"
IMPACT: Cash flow issues
MITIGATION: Request advance payment, retention of title, personal guarantee
```

**7. Change Control**
```
⚠️ RISK: No mechanism for scope changes
CLAUSE: "[Quote - or note absence]"
IMPACT: Scope creep without additional payment
MITIGATION: Add formal change control process
```

**8. Termination for Convenience**
```
⚠️ RISK: Other party can terminate anytime, you cannot
CLAUSE: "[Quote]"
IMPACT: Loss of expected revenue
MITIGATION: Mutual termination rights or notice/payment in lieu
```

**9. Insurance Requirements**
```
⚠️ RISK: Excessive insurance minimums
CLAUSE: "[Quote]"
IMPACT: Uninsurable or prohibitively expensive
MITIGATION: Negotiate realistic levels based on risk
```

**10. Non-Compete/Non-Solicit**
```
⚠️ RISK: Broad restrictions post-termination
CLAUSE: "[Quote]"
IMPACT: Business restrictions, staff retention issues
MITIGATION: Narrow scope, reasonable duration (6-12 months max)
```

#### Low Risk 🟢

**11. Standard Confidentiality**
```
✓ ACCEPTABLE: Standard NDA provisions with exceptions
CLAUSE: "[Quote]"
IMPACT: Minimal, standard protection
```

**12. Reasonable Liability Cap**
```
✓ ACCEPTABLE: Cap at [X times fees / £Y amount]
CLAUSE: "[Quote]"
IMPACT: Limited, manageable exposure
```

### Phase 4: UK-Specific Legal Checks

#### Property/Conveyancing Contracts

**Title Issues**:
```
# Check for:
- [ ] Title guarantee (full/limited/none)
- [ ] Incumbrances disclosed
- [ ] Planning permissions in place
- [ ] Building regulations compliance
- [ ] Rights of way clearly defined
- [ ] Boundary disputes noted
- [ ] Restrictive covenants identified
```

**Searches and Surveys**:
```
- [ ] Local authority search
- [ ] Environmental search
- [ ] Water & drainage search
- [ ] Chancel check (if pre-2013 property)
- [ ] Coal mining search (if applicable)
```

**Completion**:
```
- [ ] Completion date specified
- [ ] Time of essence clause (if critical)
- [ ] Deposit amount and holder
- [ ] Interest on deposit
- [ ] Retention for remedial works (if any)
```

**UK Property Law Compliance**:
```
- [ ] Complies with Law of Property Act 1925
- [ ] Meets Land Registration Act 2002 requirements
- [ ] GDPR-compliant (conveyancing data)
- [ ] Money Laundering Regulations 2017 compliance
- [ ] Estate Agents Act 1979 (if agent involved)
```

#### Pensions Contracts

**Trust Deed Essentials**:
```
- [ ] Trustee powers clearly defined
- [ ] Amendment provisions specified
- [ ] Beneficiary classes identified
- [ ] Investment powers adequate
- [ ] Conflicts of interest policy
- [ ] Indemnity provisions for trustees
```

**Regulatory Compliance**:
```
# Check against regulations database
mcp__neo4j-apex__read_neo4j_cypher(
  query="
    MATCH (o:Obligation)-[:APPLIES_TO]->(e:Entity)
    WHERE e.type = 'pension scheme'
    AND o.topic CONTAINS $topic
    RETURN o.title, o.requirement, o.deadline
  ",
  params={"topic": "[contract topic]"}
)
```

**Pensions-Specific Risks**:
```
- [ ] TPR reporting obligations clear
- [ ] Scheme Actuary terms reasonable
- [ ] Administration SLA adequate
- [ ] Custodian responsibilities defined
- [ ] Investment manager liability capped
- [ ] Conflicts of interest provisions
```

**UK Pensions Law Compliance**:
```
- [ ] Pensions Act 1995 compliance
- [ ] Pensions Act 2004 compliance
- [ ] TPR Codes of Practice alignment
- [ ] LGPS Regulations 2013 (if LGPS)
- [ ] FCA requirements (if investments)
```

#### GDPR/Data Protection

**Data Processing Terms**:
```
- [ ] Article 28 requirements met
- [ ] Processor obligations specified
- [ ] Sub-processor provisions included
- [ ] Data breach notification (72 hours)
- [ ] Data subject rights procedures
- [ ] Security measures defined
- [ ] Return/deletion on termination
- [ ] Audit rights included
```

**UK GDPR Specifics**:
```
- [ ] ICO registration confirmed
- [ ] Lawful basis identified
- [ ] UK adequacy assessment (if international transfers)
- [ ] Data Protection Act 2018 compliance
- [ ] PECR compliance (if electronic marketing)
```

### Phase 5: Benchmarking Against Standards

**Compare against standard terms**:

```
# Search for standard terms in knowledge base
mcp__archon__rag_search_knowledge_base(
  query="standard [contract type] terms UK",
  match_count=5
)
```

**Industry standard comparison**:

| Term | This Contract | Industry Standard | Assessment |
|------|---------------|-------------------|------------|
| Liability cap | £50,000 | 1-3x annual fees | Below standard |
| Payment terms | Net 60 days | Net 30 days | Unfavorable |
| Notice period | 6 months | 3 months | Onerous |
| IP ownership | Client owns all | License only | Unfavorable |

### Phase 6: Compliance Checklist Generation

```markdown
## Contract Compliance Checklist

### Pre-Signature Requirements

#### Legal Review
- [ ] Contract reviewed by qualified solicitor
- [ ] Jurisdiction confirmed (E&W/Scotland/NI)
- [ ] Parties have legal capacity to contract
- [ ] Authority to sign verified (board resolution if needed)

#### Financial
- [ ] Contract value within authority limits
- [ ] Budget available
- [ ] Payment terms acceptable
- [ ] VAT treatment confirmed

#### Insurance
- [ ] Professional indemnity insurance adequate
- [ ] Public liability insurance in place
- [ ] Cyber insurance (if processing data)
- [ ] Certificates of insurance obtained

#### Data Protection
- [ ] DPO consulted (if applicable)
- [ ] DPIA completed (if high risk processing)
- [ ] Data processing agreement signed
- [ ] Privacy notice updated

#### Risk Assessment
- [ ] Risk register updated
- [ ] Key risks identified and mitigated
- [ ] Escalation for high-risk terms
- [ ] Insurance review completed

### Post-Signature Requirements

#### Contract Management
- [ ] Contract registered in contract management system
- [ ] Key dates diarized (renewal, termination notice)
- [ ] Performance monitoring established
- [ ] Invoice/payment tracking set up

#### Compliance
- [ ] Insurance certificates filed
- [ ] GDPR records updated
- [ ] Third-party due diligence completed
- [ ] Modern Slavery Act statement (if applicable)

#### Ongoing
- [ ] Annual contract review scheduled
- [ ] KPI/SLA monitoring active
- [ ] Relationship manager assigned
- [ ] Variation control process in place
```

### Phase 7: Generate Risk Report

**Report template**:

```markdown
# Contract Risk Analysis Report

**Contract**: [Title]
**Parties**: [Party A] and [Party B]
**Analyst**: Claude Opus 4.5
**Date**: [Analysis date]

## Executive Summary

[2-3 paragraph summary of contract purpose, key terms, and overall risk assessment]

**Overall Risk Rating**: [High / Medium / Low]
**Recommendation**: [Proceed / Negotiate changes / Reject]

## Contract Overview

[Detailed summary from Phase 1]

## Key Terms Summary

[Extract from Phase 2, highlighting most important 5-10 terms]

## Risk Analysis

### Critical Risks (High Priority 🔴)

[Details from Phase 3 - High risks]

**Recommendation**: These risks should be addressed before signing.

### Notable Risks (Medium Priority 🟡)

[Details from Phase 3 - Medium risks]

**Recommendation**: Address if possible, or accept with mitigation.

### Acceptable Terms (Low Risk 🟢)

[Confirmation of standard/acceptable terms]

## UK Legal Compliance

### [Contract Type] Specific Requirements

[Details from Phase 4]

### GDPR/Data Protection

[GDPR compliance check results]

### Other Regulatory Requirements

[Any other applicable regulations]

## Benchmarking

[Comparison table from Phase 5]

## Recommendations

### Must-Have Changes (Do Not Sign Without)
1. [Change 1 - with rationale]
2. [Change 2 - with rationale]

### Should-Have Changes (Negotiate If Possible)
1. [Change 1 - with rationale]
2. [Change 2 - with rationale]

### Nice-to-Have Changes (Opportunistic)
1. [Change 1 - with rationale]

## Compliance Checklist

[Checklist from Phase 6]

## Negotiation Strategy

### Priorities
1. **Critical**: [Issue] - [Why it's important] - [Fallback position]
2. **Important**: [Issue] - [Why it's important] - [Fallback position]

### Likely Counter-Arguments
- [Argument 1] - [Your response]
- [Argument 2] - [Your response]

### Trade-Offs
- Willing to accept [X] if they agree to [Y]
- Can concede on [A] to secure [B]

## Next Steps

1. [Immediate action]
2. [Follow-up action]
3. [Long-term action]

## Appendices

### A. Risk Register

| ID | Risk | Severity | Likelihood | Impact | Mitigation | Owner |
|----|------|----------|------------|--------|------------|-------|
| R1 | [Risk] | High | High | £[X] | [Action] | [Person] |

### B. Clause-by-Clause Analysis

[Detailed clause analysis if required]

### C. Regulatory References

- [Regulation 1]
- [Regulation 2]

---

**Disclaimer**: This analysis is for guidance only and does not constitute legal advice. Contracts should be reviewed by a qualified solicitor before signing.

**Generated by**: Claude Opus 4.5 via UK Contract Risk Scanner
**Date**: [Timestamp]
```

## Red Flags Quick Reference

**STOP - Do Not Sign If**:
- ❌ Unlimited liability with no cap
- ❌ Unilateral termination (they can exit, you can't)
- ❌ Assignment of all IP you create
- ❌ Personal guarantees without discussion
- ❌ Non-compete preventing you from working
- ❌ Jurisdiction in foreign country without reason
- ❌ Payment only on completion (for long projects)
- ❌ Waiver of consequential loss exclusion
- ❌ Data controller role without DPO/systems
- ❌ Indemnity for their negligence

**CAUTION - Negotiate These**:
- ⚠️ Payment terms >30 days
- ⚠️ Automatic renewal >1 year
- ⚠️ Liability cap <1x annual fees
- ⚠️ Broad confidentiality (no standard exceptions)
- ⚠️ Exclusive supply obligations
- ⚠️ Excessive insurance requirements
- ⚠️ No change control process
- ⚠️ Vague performance standards
- ⚠️ Long termination notice (>3 months)
- ⚠️ Restrictive non-solicit clauses

## Common UK Contract Law Issues

**Misrepresentation Act 1967**:
- Pre-contractual statements may be actionable
- Check warranty/representation language carefully

**Unfair Contract Terms Act 1977**:
- Cannot exclude liability for death/personal injury
- Reasonableness test for B2B exclusions
- Entire agreement clauses must be reasonable

**Late Payment of Commercial Debts Act 1998**:
- Statutory right to interest (8% + base rate)
- Automatic unless contract specifies different rate

**Supply of Goods and Services Act 1982**:
- Implied terms about quality and fitness for purpose
- Services must be provided with reasonable care

## Integration with Other Skills

- **lgps-scheme-amendment-analyzer**: For pension scheme contracts
- **conventional-commits-uk**: If tracking contract reviews in git
- **github-workflow**: Version control for contract templates
- **cost-optimizer**: Use Opus for high-value contracts only

## Quick Commands

```bash
# Search for risk keywords in contract
grep -iE "limit|liability|indemnit|warrant|terminat|arbitrat" contract.txt

# Extract financial terms
grep -iE "£|GBP|payment|fee|cost|price" contract.txt

# Find dates
grep -Eo "[0-9]{1,2}[/ -][0-9]{1,2}[/ -][0-9]{2,4}" contract.txt

# Extract parties
grep -i "party\|parties\|between" contract.txt | head -10
```

## Summary

This skill provides comprehensive UK contract risk analysis by:
- Extracting key terms systematically
- Identifying legal risks with severity ratings
- Checking UK-specific compliance (GDPR, property law, pensions law)
- Benchmarking against industry standards
- Generating negotiation strategies
- Providing compliance checklists

**Always use Opus model** for contract analysis due to legal complexity and high stakes.

Helps ensure contracts protect your interests while complying with UK legal requirements.
