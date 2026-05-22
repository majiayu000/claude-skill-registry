---
name: using-security-architect
description: Routes to security architecture skills - threat modeling, controls, compliance, authorization
---

# Using Security Architect

## Overview

This meta-skill routes you to the right security architecture skills based on your situation. Load this skill when you need security expertise but aren't sure which specific security skill to use.

**Core Principle**: Different security tasks require different skills. Match your situation to the appropriate skill, load only what you need.

## When to Use

Load this skill when:
- Starting any security-related task
- User mentions: "security", "threat", "authentication", "authorization", "compliance", "classified", "review this design"
- You recognize security implications but unsure which skill applies
- You need to document security decisions

**Don't use for**: Simple features with no security implications (e.g., UI styling, basic CRUD with existing auth)

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-security-architect/SKILL.md`

Reference sheets like `threat-modeling.md` are at:
  `skills/using-security-architect/threat-modeling.md`

NOT at:
  `skills/threat-modeling.md` ← WRONG PATH

When you see a link like `[threat-modeling.md](threat-modeling.md)`, read the file from the same directory as this SKILL.md.

---

## Routing by Situation

### New System Design

**Symptoms**: "Design a new...", "We're building...", "Greenfield project"

**Route to**:
1. **First**: [threat-modeling.md](threat-modeling.md) - Identify threats before implementation
2. **Then**: [secure-by-design-patterns.md](secure-by-design-patterns.md) - Design with security built-in
3. **Then**: [security-controls-design.md](security-controls-design.md) - Select appropriate controls

**Example**: "Design authentication system" → Load all three in order

---

### Existing System Review

**Symptoms**: "Review this design", "Security audit", "Does this look secure?"

**Route to**: [security-architecture-review.md](security-architecture-review.md)

**When to add**:
- Add [threat-modeling.md](threat-modeling.md) if design lacks threat analysis
- Add [secure-by-design-patterns.md](secure-by-design-patterns.md) if architecture has gaps

**Example**: "Review this plugin system" → Load [security-architecture-review.md](security-architecture-review.md)

---

### Specific Security Domains

#### Authentication/Authorization Design
**Route to**:
- [threat-modeling.md](threat-modeling.md) (identify auth threats)
- [secure-by-design-patterns.md](secure-by-design-patterns.md) (defense-in-depth, fail-secure)
- Consider: [security-authorization-and-accreditation.md](security-authorization-and-accreditation.md) (if government/ATO needed)

#### Configuration & Secrets
**Route to**:
- [threat-modeling.md](threat-modeling.md) (config tampering threats)
- [security-controls-design.md](security-controls-design.md) (separation of config vs code)

#### API Security
**Route to**:
- [threat-modeling.md](threat-modeling.md) (STRIDE on API endpoints)
- [security-architecture-review.md](security-architecture-review.md) (review access controls)

---

### Specialized Contexts (Extensions)

#### Classified/High-Security Systems

**Symptoms**: "TOP SECRET", "classified data", "security clearances", "multi-level security", "Bell-LaPadula"

**Route to**:
1. [classified-systems-security.md](classified-systems-security.md) (REQUIRED for classified contexts)
2. Plus core skills: [threat-modeling.md](threat-modeling.md), [secure-by-design-patterns.md](secure-by-design-patterns.md)

**Example**: "Design system handling SECRET and UNCLASSIFIED" → Load [classified-systems-security.md](classified-systems-security.md) first

---

#### Compliance/Regulatory

**Symptoms**: "HIPAA", "PCI-DSS", "SOC2", "GDPR", "compliance audit", "regulatory requirements"

**Route to**: [compliance-awareness-and-mapping.md](compliance-awareness-and-mapping.md)

**When to add**:
- Add [security-authorization-and-accreditation.md](security-authorization-and-accreditation.md) if ATO/AIS needed
- Add core skills for implementing compliant controls

**Example**: "Build HIPAA-compliant system" → Load [compliance-awareness-and-mapping.md](compliance-awareness-and-mapping.md) + [threat-modeling.md](threat-modeling.md)

---

#### Government Authorization

**Symptoms**: "ATO", "AIS", "authority to operate", "SSP", "SAR", "POA&M", "FedRAMP", "FISMA"

**Route to**: [security-authorization-and-accreditation.md](security-authorization-and-accreditation.md)

**Cross-reference**: Load `muna/technical-writer/operational-acceptance-documentation` for SSP/SAR writing

---

### Documentation Tasks

**Symptoms**: "Document security decisions", "Write security docs", "Explain threat model"

**Route to**: [documenting-threats-and-controls.md](documenting-threats-and-controls.md)

**Cross-faction reference**: Load `muna/technical-writer/documentation-structure` for ADR format, clarity guidelines

**Example**: "Document why we chose MLS" → Load [documenting-threats-and-controls.md](documenting-threats-and-controls.md) + documentation-structure

---

## Core vs Extension Skills

### Core Skills (Universal - Use for Any Project)

Load these for **any** project with security needs:

- [threat-modeling.md](threat-modeling.md) - Identify threats (STRIDE, attack trees)
- [security-controls-design.md](security-controls-design.md) - Design controls (defense-in-depth, fail-secure)
- [security-architecture-review.md](security-architecture-review.md) - Review designs for security gaps
- [secure-by-design-patterns.md](secure-by-design-patterns.md) - Apply secure design patterns
- [documenting-threats-and-controls.md](documenting-threats-and-controls.md) - Document security decisions

### Extension Skills (Specialized - Use for Specific Contexts)

Load these **only** when context requires:

- [classified-systems-security.md](classified-systems-security.md) - Handling classified/sensitive data with clearances
- [compliance-awareness-and-mapping.md](compliance-awareness-and-mapping.md) - Regulatory compliance (HIPAA, PCI-DSS, GDPR, etc.)
- [security-authorization-and-accreditation.md](security-authorization-and-accreditation.md) - Government ATO/AIS processes

**Decision**: If you're unsure whether context is "specialized", start with core skills. Specialized contexts will be explicit in requirements.

---

## Decision Tree

```
Is this security-related?
├─ No → Don't load security skills
└─ Yes → Continue

What's the situation?
├─ New system design → threat-modeling + secure-by-design-patterns + security-controls-design
├─ Reviewing existing → architecture-security-review
├─ Documenting security → documenting-threats-and-controls + muna/technical-writer/documentation-structure
└─ Domain-specific → See "Specific Security Domains" above

Is this a specialized context?
├─ Classified data → ADD: classified-systems-security
├─ Compliance required → ADD: compliance-awareness-and-mapping
├─ Government ATO → ADD: security-authorization-and-accreditation
└─ No → Core skills sufficient
```

---

## Cross-Faction References

Security work often requires skills from other factions:

**Muna (Documentation)**:
- `muna/technical-writer/documentation-structure` - When documenting security (ADRs, SSPs)
- `muna/technical-writer/clarity-and-style` - When explaining security to non-experts

**Load both factions when**: Documenting security decisions, writing security policies, explaining threats to stakeholders

---

## Common Routing Patterns

### Pattern 1: New Authentication System
```
User: "Design authentication with passwords and OAuth"
You: Loading threat-modeling + secure-by-design-patterns + security-controls-design
```

### Pattern 2: Design Review
```
User: "Review this plugin security design"
You: Loading architecture-security-review
```

### Pattern 3: Classified System
```
User: "Build system handling TOP SECRET data"
You: Loading classified-systems-security + threat-modeling + secure-by-design-patterns
```

### Pattern 4: Compliance Project
```
User: "Build HIPAA-compliant patient portal"
You: Loading compliance-awareness-and-mapping + threat-modeling + security-controls-design
```

### Pattern 5: Security Documentation
```
User: "Document our MLS security decisions"
You: Loading documenting-threats-and-controls + muna/technical-writer/documentation-structure
```

---

## When NOT to Load Security Skills

**Don't load security skills for**:
- UI styling (colors, fonts, layouts)
- Basic CRUD with existing, tested auth
- Non-security refactoring (renaming variables, extracting functions)
- Documentation that isn't security-related

**Example**: "Add dark mode toggle to settings" → No security skills needed (unless settings include security-sensitive preferences)

---

## Quick Reference Table

| Task Type | Load These Skills | Notes |
|-----------|------------------|-------|
| **New system design** | threat-modeling, secure-by-design-patterns, security-controls-design | Load in order |
| **Design review** | architecture-security-review | Add threat-modeling if no threat analysis exists |
| **Authentication** | threat-modeling, secure-by-design-patterns | Consider authorization-and-accreditation if ATO needed |
| **API security** | threat-modeling, architecture-security-review | Apply STRIDE to endpoints |
| **Classified data** | classified-systems-security + core skills | Extension required |
| **Compliance** | compliance-awareness-and-mapping + core skills | Extension for regulatory contexts |
| **Government ATO** | security-authorization-and-accreditation + core skills | Extension for ATO/AIS |
| **Document security** | documenting-threats-and-controls, muna/documentation-structure | Cross-faction |

---

## Common Mistakes

### ❌ Loading All Skills at Once
**Wrong**: Load all 8 security-architect skills for every security task
**Right**: Load only the skills your situation needs (use decision tree)

### ❌ Skipping Threat Modeling
**Wrong**: Jump straight to implementation for new security features
**Right**: Always threat model first for new systems/features

### ❌ Using Core Skills for Specialized Contexts
**Wrong**: Use generic threat modeling for classified systems
**Right**: Load classified-systems-security for MLS contexts

### ❌ Not Cross-Referencing Muna
**Wrong**: Write security docs without documentation structure skills
**Right**: Load both ordis/documenting-threats + muna/documentation-structure

---

## Examples

### Example 1: Payment Processing System

```
User: "Design a payment processing microservice"

Your routing:
1. Recognize: New system + financial domain → security critical
2. Load: threat-modeling (identify payment-specific threats)
3. Load: secure-by-design-patterns (encryption, secrets management)
4. Load: security-controls-design (PCI-DSS controls)
5. Consider: compliance-awareness-and-mapping (PCI-DSS is compliance requirement)
```

### Example 2: Simple Feature (No Security Needed)

```
User: "Add a favorites button to the UI"

Your routing:
1. Recognize: UI feature, uses existing auth, no new security surface
2. Decision: No security skills needed
3. Proceed with standard implementation
```

### Example 3: Classified System Architecture

```
User: "Review architecture for system handling SECRET and UNCLASSIFIED data"

Your routing:
1. Recognize: Classified context (SECRET mentioned) + review task
2. Load: classified-systems-security (MLS patterns required)
3. Load: architecture-security-review (review process)
4. Load: threat-modeling (if threats not already modeled)
```

---

## Phase 1 Note

**Currently Available** (Phase 1):
- ✅ `using-security-architect` (this skill)
- ✅ `threat-modeling` (in progress)

**Coming Soon** (Phases 2-3):
- `security-controls-design`
- `architecture-security-review`
- `secure-by-design-patterns`
- `classified-systems-security`
- `compliance-awareness-and-mapping`
- `security-authorization-and-accreditation`
- `documenting-threats-and-controls`

**For Phase 1**: Focus on threat-modeling as primary skill. Reference other skills by name even though they're not implemented yet - this tests the routing logic.

---

## Summary

**This skill maps your situation → specific security skills to load.**

1. Identify your situation (new system, review, specialized context)
2. Use decision tree to find applicable skills
3. Load core skills for universal needs
4. Add extension skills for specialized contexts
5. Cross-reference Muna for documentation needs
6. Don't load security skills when not needed

**Meta-rule**: When in doubt, start with [threat-modeling.md](threat-modeling.md). Threats drive everything else.

---

## Security Architect Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

### Core Skills (Universal)

1. [threat-modeling.md](threat-modeling.md) - STRIDE analysis, attack trees, threat identification, security-critical systems analysis
2. [secure-by-design-patterns.md](secure-by-design-patterns.md) - Defense-in-depth, fail-secure design, least privilege, separation of concerns
3. [security-controls-design.md](security-controls-design.md) - Control selection, defense layering, encryption, secrets management
4. [security-architecture-review.md](security-architecture-review.md) - Design review process, security gap analysis, architecture evaluation
5. [documenting-threats-and-controls.md](documenting-threats-and-controls.md) - Security documentation, threat model writing, control documentation

### Extension Skills (Specialized Contexts)

6. [classified-systems-security.md](classified-systems-security.md) - Multi-level security (MLS), Bell-LaPadula, classified data handling, security clearances
7. [compliance-awareness-and-mapping.md](compliance-awareness-and-mapping.md) - HIPAA, PCI-DSS, SOC2, GDPR, regulatory mapping, compliance frameworks
8. [security-authorization-and-accreditation.md](security-authorization-and-accreditation.md) - ATO/AIS processes, SSP/SAR, POA&M, FedRAMP, FISMA, government authorization
