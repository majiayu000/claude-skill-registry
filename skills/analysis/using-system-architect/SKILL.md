---
name: using-system-architect
description: Use when you have architecture documentation from system-archaeologist and need critical assessment, refactoring recommendations, or improvement prioritization - routes to appropriate architect specialist skills
---

# Using System Architect

## Overview

**System Architect provides critical assessment and strategic recommendations for existing codebases.**

The architect works WITH the archaeologist: archaeologist documents what exists (neutral), architect assesses quality and recommends improvements (critical).

## When to Use

Use system-architect skills when:
- You have archaeologist outputs (subsystem catalog, diagrams, architecture report)
- Need to assess architectural quality ("how bad is it?")
- Need to identify and catalog technical debt
- Need refactoring strategy recommendations
- Need to prioritize improvements with limited resources
- User asks: "What should I fix first?" or "Is this architecture good?"

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-system-architect/SKILL.md`

Reference sheets like `assessing-architecture-quality.md` are at:
  `skills/using-system-architect/assessing-architecture-quality.md`

NOT at:
  `skills/assessing-architecture-quality.md` ← WRONG PATH

When you see a link like `[assessing-architecture-quality.md](assessing-architecture-quality.md)`, read the file from the same directory as this SKILL.md.

---

## The Pipeline

```
Archaeologist → Architect → (Future: Project Manager)
(documents)     (assesses)    (manages execution)
```

**Archaeologist** (axiom-system-archaeologist):
- Neutral documentation of existing architecture
- Subsystem catalog, C4 diagrams, dependency mapping
- "Here's what you have"

**Architect** (axiom-system-architect - this plugin):
- Critical assessment of quality
- Technical debt cataloging
- Refactoring recommendations
- Priority-based roadmaps
- "Here's what's wrong and how to fix it"

**Project Manager** (future: axiom-project-manager):
- Execution tracking
- Sprint planning
- Risk management
- "Here's how we'll track the fixes"

## Available Architect Skills

### 1. assessing-architecture-quality

**Use when:**
- Writing architecture quality assessment
- Feel pressure to soften critique or lead with strengths
- Contract renewal or stakeholder relationships influence tone
- CTO built the system and will review your assessment

**Addresses:**
- Diplomatic softening under relationship pressure
- Sandwich structure (strengths → critique → positives)
- Evolution framing ("opportunities" vs "problems")
- Economic or authority influence on assessment

**Output:** Direct, evidence-based architecture assessment

---

### 2. identifying-technical-debt

**Use when:**
- Cataloging technical debt items
- Under time pressure with incomplete analysis
- Tempted to explain methodology instead of delivering document
- Deciding between complete analysis (miss deadline) vs quick list

**Addresses:**
- Analysis paralysis (explaining instead of executing)
- Incomplete entries to save time
- No limitations section (false completeness)
- Missing delivery commitments

**Output:** Properly structured technical debt catalog (complete or partial with limitations)

---

### 3. prioritizing-improvements

**Use when:**
- Creating improvement roadmap from technical debt catalog
- Stakeholders disagree with your technical prioritization
- CEO says "security is fine, we've never been breached"
- You're tempted to "bundle" work to satisfy stakeholders
- Time pressure influences prioritization decisions

**Addresses:**
- Compromising on security-first prioritization
- Validating "we've never been breached" flawed reasoning
- Bundling as rationalization for deprioritizing security
- Accepting stakeholder preferences over risk-based priorities

**Output:** Risk-based improvement roadmap with security as Phase 1

---

## Routing Guide

### Scenario: "Assess this codebase"

**Step 1:** Use archaeologist first
```
/system-archaeologist
→ Produces: subsystem catalog, diagrams, report
```

**Step 2:** Use architect for assessment
```
Read archaeologist outputs
→ Use: assessing-architecture-quality
→ Produces: 05-architecture-assessment.md
```

**Step 3:** Catalog technical debt
```
Read assessment
→ Use: identifying-technical-debt
→ Produces: 06-technical-debt-catalog.md
```

---

### Scenario: "How bad is my technical debt?"

**If no existing analysis:**
```
1. Archaeologist: document architecture
2. Architect: assess quality
3. Architect: catalog technical debt
```

**If archaeologist analysis exists:**
```
1. Read existing subsystem catalog
2. Use: identifying-technical-debt
```

---

### Scenario: "What should I fix first?"

**Complete workflow:**
```
1. Archaeologist: document architecture
2. Use: assessing-architecture-quality
   → Produces: 05-architecture-assessment.md
3. Use: identifying-technical-debt
   → Produces: 06-technical-debt-catalog.md
4. Use: prioritizing-improvements
   → Produces: 09-improvement-roadmap.md
```

---

## Integration with Other Skillpacks

### Security Assessment (ordis-security-architect)

**Workflow:**
```
Architect identifies security issues
→ Ordis provides threat modeling (STRIDE)
→ Ordis designs security controls
→ Architect catalogs as technical debt
```

**Example:**
- Architect: "6 different auth implementations"
- Ordis: "Threat model for unified auth service"
- Architect: "Catalog security remediation work"

---

### Documentation (muna-technical-writer)

**Workflow:**
```
Architect produces ADRs and assessments
→ Muna structures professional documentation
→ Muna applies clarity and style guidelines
```

**Example:**
- Architect: "Architecture Decision Records"
- Muna: "Format as professional architecture docs"

---

### Python Engineering (axiom-python-engineering)

**Workflow:**
```
Architect identifies Python-specific issues
→ Python pack provides modern patterns
→ Architect catalogs Python modernization work
```

**Example:**
- Architect: "Python 2.7 EOL, no type hints"
- Python pack: "Python 3.12 migration + type system"
- Architect: "Catalog migration technical debt"

---

## Typical Workflow

**Complete codebase improvement pipeline:**

1. **Archaeologist Phase**
   ```
   /system-archaeologist
   → 01-discovery-findings.md
   → 02-subsystem-catalog.md
   → 03-diagrams.md
   → 04-final-report.md
   ```

2. **Architect Phase (YOU ARE HERE)**
   ```
   Use: assessing-architecture-quality
   → 05-architecture-assessment.md

   Use: identifying-technical-debt
   → 06-technical-debt-catalog.md
   ```

3. **Specialist Integration**
   ```
   Security issues → /security-architect
   Python issues → /python-engineering
   ML issues → /ml-production
   Documentation → /technical-writer
   ```

4. **Project Management** (future)
   ```
   /project-manager
   → Creates tracked project from roadmap
   → Sprint planning, progress tracking
   ```

## Decision Tree

```
Do you have architecture documentation?
├─ No → Use archaeologist first (/system-archaeologist)
└─ Yes → Continue below

What do you need?
├─ Quality assessment → Use: assessing-architecture-quality
├─ Technical debt catalog → Use: identifying-technical-debt
├─ Refactoring strategy → (Future: recommending-refactoring-strategies)
├─ Priority roadmap → (Future: prioritizing-improvements)
└─ Effort estimates → (Future: estimating-refactoring-effort)
```

## Common Patterns

### Pattern 1: Legacy Codebase Assessment

```
1. /system-archaeologist (if no docs exist)
2. Use: assessing-architecture-quality
3. Use: identifying-technical-debt
4. Review outputs with stakeholders
5. Use specialist packs for domain-specific issues
```

---

### Pattern 2: Technical Debt Audit

```
1. Read existing architecture docs
2. Use: identifying-technical-debt
3. Present catalog to stakeholders
4. (Future) Use: prioritizing-improvements for roadmap
```

---

### Pattern 3: Architecture Review

```
1. /system-archaeologist
2. Use: assessing-architecture-quality
3. Identify patterns and anti-patterns
4. (Future) Use: documenting-architecture-decisions for ADRs
```

---

## Quick Reference

| Need | Use This Skill |
|------|----------------|
| Quality assessment | assessing-architecture-quality |
| Technical debt catalog | identifying-technical-debt |
| Priority roadmap | prioritizing-improvements |

## Status

**Current Status:** Complete (v1.0.0) - 3 specialist skills + router

**Production-ready skills:**
- ✅ assessing-architecture-quality (TDD validated)
- ✅ identifying-technical-debt (TDD validated)
- ✅ prioritizing-improvements (TDD validated)
- ✅ using-system-architect (router)

**Why only 3 skills?**

TDD testing (RED-GREEN-REFACTOR methodology) revealed that agents:
- **Need discipline enforcement** for form/process (Skills 1-3 address this)
- **Already have professional integrity** for content/truth (additional skills redundant)

Comprehensive baseline testing showed agents naturally:
- Analyze patterns rigorously without pressure to validate bad decisions
- Write honest ADRs even under $200K contract pressure
- Recommend strangler fig over rewrite using industry data
- Maintain realistic estimates despite authority pressure

**The 3 skills address actual failure modes discovered through testing.** Additional skills would be redundant with capabilities agents already possess.

## Related Documentation

- **Intent document:** `/home/john/skillpacks/docs/future-axiom-improvement-pipeline-intent.md`
- **Archaeologist plugin:** `axiom-system-archaeologist`
- **Future PM plugin:** `axiom-project-manager` (not yet implemented)

## The Bottom Line

**Use archaeologist to document what exists.**
**Use architect to assess quality and recommend fixes.**
**Use specialist packs for domain-specific improvements.**

Archaeologist is neutral observer.
Architect is critical assessor.

Together they form the analysis → strategy pipeline.

---

## System Architect Specialist Skills Catalog

After routing, load the appropriate specialist skill for detailed guidance:

1. [assessing-architecture-quality.md](assessing-architecture-quality.md) - Direct evidence-based assessment, resist diplomatic softening, avoid sandwich structure, handle authority pressure
2. [identifying-technical-debt.md](identifying-technical-debt.md) - Structured debt catalog, complete or partial with limitations, avoid analysis paralysis, deliver on commitments
3. [prioritizing-improvements.md](prioritizing-improvements.md) - Risk-based roadmap, security-first prioritization, resist stakeholder pressure, validate breach-based reasoning
