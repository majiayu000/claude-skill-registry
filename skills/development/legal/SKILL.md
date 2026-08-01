---
name: legal
description: 'Skill Name: blockchain-lawyer:review'
---

# BLOCKCHAIN LAWYER SKILL SPECIFICATION

**Skill Name**: `blockchain-lawyer:review`
**Type**: Legal Review & Guidance Agent
**Status**: Template for Implementation
**Created**: December 27, 2025

---

## 1. SKILL OVERVIEW

This Claude Code skill provides blockchain legal expertise for Aurigraph DLT project, including:
- Legal document review and analysis
- Blockchain law compliance verification
- Risk assessment and mitigation
- Regulatory compliance guidance
- Smart contract liability analysis
- Terms and conditions customization

### Available Operations

```
/blockchain-lawyer review         # Review legal documents
/blockchain-lawyer analyze        # Analyze legal risks
/blockchain-lawyer customize      # Customize documents for jurisdiction
/blockchain-lawyer compliance     # Check GDPR/CCPA/export compliance
/blockchain-lawyer risks          # Identify legal risks in code
```

---

## 2. SKILL FRONTMATTER

```yaml
---
name: blockchain-lawyer
description: >
  Blockchain legal expert providing legal document review, compliance verification,
  and risk assessment for blockchain platforms. Includes regulatory guidance for
  GDPR, CCPA, export controls, sanctions, smart contracts, and crypto-specific issues.

author: Aurigraph DLT Legal Team
version: 1.0.0
category: Legal & Compliance

tools:
  - Glob         # Search legal documents
  - Grep         # Search legal provisions
  - Read         # Read full documents
  - WebSearch    # Research legal precedents
  - WebFetch     # Fetch regulatory guidance

tags:
  - legal
  - blockchain
  - compliance
  - regulatory
  - risk-assessment
  - crypto
  - gdpr
  - ccpa

triggers:
  - "blockchain lawyer"
  - "legal review"
  - "compliance check"
  - "legal risk"
  - "regulatory guidance"
---
```

---

## 3. SKILL COMMANDS

### Command 1: Review Documents

```yaml
name: review
description: Review legal documents for blockchain compliance

parameters:
  document:
    type: string
    description: "Document name (privacy-policy, terms, eula, etc.)"
  jurisdiction:
    type: string
    description: "Target jurisdiction (us, eu, uk, ca, etc.)"
  focus_areas:
    type: array
    description: "Specific areas to focus on (e.g., ['liability', 'gdpr', 'smart-contracts'])"

examples:
  - "/blockchain-lawyer review --document privacy-policy-platform --jurisdiction eu --focus-areas gdpr,data-retention"
  - "/blockchain-lawyer review --document terms-platform --jurisdiction us --focus-areas liability,transaction-finality"
```

### Command 2: Analyze Risks

```yaml
name: analyze
description: Analyze legal risks in documents or code

parameters:
  input:
    type: string
    description: "Document or code to analyze"
  risk_level:
    type: enum
    values: [critical, high, medium, low]
    description: "Minimum risk level to report"

examples:
  - "/blockchain-lawyer analyze --input eula-platform.md --risk-level critical"
  - "/blockchain-lawyer analyze --input SmartContractService.java --risk-level high"
```

### Command 3: Customize Documents

```yaml
name: customize
description: Customize legal documents for specific jurisdiction

parameters:
  document:
    type: string
    description: "Document to customize"
  jurisdiction:
    type: string
    description: "Target jurisdiction"
  company_info:
    type: object
    description: "Company information for customization"
    properties:
      company_name:
        type: string
      address:
        type: string
      contact_email:
        type: string
      phone:
        type: string
      domain:
        type: string

examples:
  - "/blockchain-lawyer customize --document privacy-policy --jurisdiction california --company_name 'Aurigraph DLT' --address '123 Main St, SF, CA' --contact_email legal@aurigraph.io"
```

### Command 4: Compliance Check

```yaml
name: compliance
description: Check document compliance with specific regulations

parameters:
  document:
    type: string
    description: "Document to check"
  regulations:
    type: array
    values: [gdpr, ccpa, export-control, sanctions, aml-kyc, eea-privacy]
    description: "Regulations to verify compliance with"

examples:
  - "/blockchain-lawyer compliance --document privacy-policy --regulations gdpr,ccpa"
  - "/blockchain-lawyer compliance --document terms --regulations export-control,sanctions"
```

### Command 5: Risk Assessment

```yaml
name: risks
description: Identify legal risks in code or smart contracts

parameters:
  code_file:
    type: string
    description: "Code file to analyze"
  risk_areas:
    type: array
    values: [liability, smart-contract, wallet-security, aml-kyc, export-control, data-privacy]
    description: "Risk areas to focus on"

examples:
  - "/blockchain-lawyer risks --code_file DemoService.java --risk_areas liability,smart-contract"
  - "/blockchain-lawyer risks --code_file CrmDemoResource.java --risk_areas aml-kyc,data-privacy"
```

---

## 4. IMPLEMENTATION GUIDE

### Step 1: Create Skill File

Create file: `/Users/subbujois/subbuworkingdir/Aurigraph-DLT/.claude/skills/blockchain-lawyer.md`

```markdown
---
name: blockchain-lawyer
description: Blockchain legal expert for document review, compliance verification, and risk assessment
version: 1.0.0
---

# Blockchain Lawyer Skill

[Implementation content here]
```

### Step 2: Register Commands

Register each command handler:
- `review` - Document review processor
- `analyze` - Risk analysis engine
- `customize` - Document customization
- `compliance` - Compliance verification
- `risks` - Code risk assessment

### Step 3: Configure Tools

Enable access to:
- `Glob` - Find legal documents
- `Grep` - Search legal text
- `Read` - Read full documents
- `WebSearch` - Research legal precedents
- `WebFetch` - Fetch regulatory guidance

---

## 5. CORE COMPETENCIES

### Legal Document Review

The skill can:
- ✓ Review Privacy Policies for GDPR/CCPA compliance
- ✓ Review Terms & Conditions for enforceability
- ✓ Review EULAs for liability protection
- ✓ Identify missing or inadequate provisions
- ✓ Flag legal risks and exposure
- ✓ Suggest fixes and improvements

**Key Areas**:
- GDPR Articles 15-22 (user rights)
- CCPA §1798.100-120 (user rights)
- Transaction finality and immutability
- Smart contract liability
- Wallet security responsibility
- Export control compliance
- Sanctions list screening

### Compliance Verification

The skill verifies:
- ✓ **GDPR**: All user rights documented
- ✓ **CCPA**: California-specific rights included
- ✓ **Export Controls**: EAR/ITAR compliance
- ✓ **Sanctions**: OFAC and country restrictions
- ✓ **AML/KYC**: Anti-money laundering procedures
- ✓ **Data Privacy**: International transfers
- ✓ **Blockchain-specific**: Transaction finality, smart contracts

### Risk Assessment

The skill identifies:
- ✓ **Liability Risks**: Unprotected legal exposure
- ✓ **Compliance Risks**: Regulatory violations
- ✓ **Operational Risks**: Undefended procedures
- ✓ **Smart Contract Risks**: Code liability issues
- ✓ **Data Privacy Risks**: Inadequate protections
- ✓ **Export Control Risks**: Sanctions violations

---

## 6. BLOCKCHAIN-SPECIFIC EXPERTISE

### Blockchain Law Knowledge

**Transaction Finality**:
- Explains immutability of blockchain transactions
- Verifies finality language in T&C
- Identifies risks from user expectations
- Recommends protective language

**Smart Contract Liability**:
- Assesses developer responsibility for contract code
- Identifies liability exposure from vulnerabilities
- Recommends risk disclaimers
- Analyzes indemnification requirements

**Wallet Security**:
- Verifies user responsibility for private keys
- Assesses backup and recovery language
- Identifies risks from key loss
- Recommends security best practices

**Quantum Cryptography**:
- Understands NIST Level 5 compliance
- Assesses CRYSTALS-Dilithium/Kyber implementation
- Verifies security claims accuracy
- Identifies risks from quantum threats

### Regulatory Compliance

**GDPR Compliance**:
- Articles 15-22 user rights
- Data processing agreements (DPA)
- Standard Contractual Clauses (SCCs)
- Data Protection Impact Assessment (DPIA)

**CCPA Compliance**:
- §1798.100 right to know
- §1798.105 right to delete
- §1798.120 right to opt-out
- §1798.150 right to appeal

**Export Controls**:
- EAR (Export Administration Regulations)
- Sanctions screening (OFAC)
- Restricted jurisdictions
- Compliance verification

**AML/KYC**:
- Know-your-customer procedures
- Anti-money laundering controls
- Sanctions list screening
- Beneficial ownership verification

---

## 7. USE CASES

### Use Case 1: Pre-Publication Legal Review

**Scenario**: Documents ready for publication, need legal review

**Skill Execution**:
```
/blockchain-lawyer review
  --document privacy-policy-platform
  --jurisdiction eu
  --focus-areas gdpr,data-retention
```

**Output**:
- ✓ GDPR compliance status
- ✓ Data retention period review
- ✓ User rights documentation check
- ✓ Risk identification
- ✓ Recommended fixes

### Use Case 2: Jurisdiction-Specific Customization

**Scenario**: Need to customize documents for California

**Skill Execution**:
```
/blockchain-lawyer customize
  --document privacy-policy
  --jurisdiction california
  --company_name "Aurigraph DLT"
  --contact_email legal@aurigraph.io
```

**Output**:
- ✓ CCPA-specific provisions added
- ✓ California privacy rights documented
- ✓ State-specific contact procedures
- ✓ Attorney review recommendations

### Use Case 3: Export Control Compliance

**Scenario**: Verify platform complies with export controls

**Skill Execution**:
```
/blockchain-lawyer compliance
  --document terms-platform
  --regulations export-control,sanctions
```

**Output**:
- ✓ Export control language review
- ✓ Sanctions list procedure check
- ✓ Restricted country compliance
- ✓ OFAC screening verification

### Use Case 4: Code Risk Assessment

**Scenario**: Identify legal risks in Java backend code

**Skill Execution**:
```
/blockchain-lawyer risks
  --code_file DemoService.java
  --risk_areas liability,smart-contract,data-privacy
```

**Output**:
- ✓ Liability exposure assessment
- ✓ Smart contract risk analysis
- ✓ Data privacy compliance check
- ✓ Recommended mitigations

---

## 8. KNOWLEDGE BASE

The skill leverages:

**Internal Documents** (in `/docs/legal/`):
- PRIVACY_POLICY_PLATFORM.md
- PRIVACY_POLICY_WEBSITE.md
- TERMS_AND_CONDITIONS_PLATFORM.md
- TERMS_AND_CONDITIONS_WEBSITE.md
- EULA_PLATFORM.md
- EULA_WEBSITE.md
- README.md (implementation guide)
- ACCELERATED_LEGAL_REVIEW_PLAN.md

**External References**:
- GDPR (EU Regulation 2016/679)
- CCPA (California Consumer Privacy Act)
- EAR (Export Administration Regulations)
- ITAR (International Traffic in Arms Regulations)
- Blockchain law best practices
- Crypto regulatory guidance
- Smart contract standards

---

## 9. RESPONSE FORMAT

### Review Response Template

```
# Document Review: [Document Name]

## Jurisdiction: [Target Jurisdiction]

## Compliance Status
- GDPR: ✅ Compliant / ⚠️ Needs fixes / ❌ Non-compliant
- CCPA: ✅ Compliant / ⚠️ Needs fixes / ❌ Non-compliant
- Export Control: ✅ Compliant / ⚠️ Needs fixes / ❌ Non-compliant

## Critical Issues (Blocks Publication)
1. Issue 1: [Description]
   - Risk: [Legal exposure]
   - Fix: [Recommendation]

## Important Issues (Should Fix)
1. Issue 1: [Description]
   - Impact: [Legal risk]
   - Fix: [Recommendation]

## Minor Issues (Can Fix Later)
1. Issue 1: [Description]
   - Recommendation: [Enhancement]

## Risk Assessment
- Overall Risk Level: [Critical/High/Medium/Low]
- Recommended Actions: [List of next steps]
- Timeline: [Suggested review timeline]

## Sign-Off Recommendation
Ready for publication: [Yes/No/With modifications]
Recommended next step: [Attorney review/Publication/Further customization]
```

---

## 10. INTEGRATION WITH PROJECT

### Integration Points

1. **Legal Document Management**
   - Reviews all documents in `/docs/legal/`
   - Verifies compliance before publication
   - Tracks document versions

2. **Development Process**
   - Analyzes code for legal risks
   - Identifies liability exposure
   - Recommends protective measures

3. **Compliance Tracking**
   - Monitors regulatory compliance
   - Tracks required certifications
   - Documents legal review history

4. **User Communication**
   - Helps draft legal notifications
   - Reviews user-facing terms
   - Ensures accurate disclosures

### Team Access

**Who can use**:
- ✓ Legal team members
- ✓ Compliance officers
- ✓ Development team (for risk assessment)
- ✓ Product team (for disclosure accuracy)

**Access control**:
- Legal documents: Available to authorized users
- Risk analysis: Available to all team members
- Compliance review: Available to legal/compliance only

---

## 11. ACCURACY & RELIABILITY

### Confidence Levels

The skill provides:
- **High Confidence** (95%+): Document compliance checks, risk identification, provision verification
- **Medium Confidence** (70-90%): Legal interpretation, recommendation prioritization
- **Lower Confidence** (<70%): Enforceability prediction (needs attorney verification)

### Important Disclaimers

**The skill:**
- ✓ Provides analysis and recommendations
- ✓ Identifies risks and missing provisions
- ✓ Verifies compliance with standards
- ✗ Does NOT provide legal advice
- ✗ Cannot replace attorney review
- ✗ Cannot guarantee enforceability

**Required**: Attorney review before publication

---

## 12. FUTURE ENHANCEMENTS

### Phase 2 (v1.1)
- Automated attorney coordination
- Integration with legal research databases
- Template generation for common scenarios
- Regulatory update notifications

### Phase 3 (v2.0)
- AI-powered contract generation
- Jurisdiction-specific automatic customization
- Real-time compliance monitoring
- Automated legal risk scoring

---

## 13. HOW TO ENABLE THIS SKILL

### Option A: Manual Creation

1. Create file: `/.claude/skills/blockchain-lawyer.md`
2. Add frontmatter with skill configuration
3. Register commands with handlers
4. Enable tool access

### Option B: Use Skill Development Tool

```
/skill-development create
  --name blockchain-lawyer
  --description "Blockchain legal expert"
  --version 1.0.0
```

### Option C: Via Plugin Creation

```
/plugin-dev:skill-development
  Create blockchain-lawyer skill with legal review capabilities
```

---

## 14. QUICK START

### Get Legal Review of Document

```
/blockchain-lawyer review
  --document [document-name]
  --jurisdiction [target-jurisdiction]
```

### Check Compliance

```
/blockchain-lawyer compliance
  --document [document-name]
  --regulations gdpr,ccpa,export-control
```

### Analyze Code Risks

```
/blockchain-lawyer risks
  --code_file [file-name]
  --risk_areas liability,smart-contract
```

---

**This skill specification is ready for implementation.**

To enable this skill in Claude Code:
1. Copy this specification
2. Use skill development tools to create
3. Add to project's skill registry
4. Grant appropriate access permissions
5. Start using with `/blockchain-lawyer` commands

---

**Created**: December 27, 2025
**Version**: 1.0.0
**Status**: Ready for Implementation
