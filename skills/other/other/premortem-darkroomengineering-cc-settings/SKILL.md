---
name: premortem
description: |
  Analyze what could go wrong with a plan. Use when:
  - User asks "what could go wrong", "risks", "potential issues"
  - Before implementing a significant change
  - User wants to validate an approach
  - Planning a risky operation
context: fork
agent: oracle
---

# Premortem Analysis

Analyze potential failure modes before they happen.

## Purpose

Imagine the project has failed. What went wrong?

This technique surfaces risks that optimism bias might hide.

## Analysis Framework

### 1. Technical Risks
- What could break?
- What dependencies might fail?
- What edge cases are unhandled?
- What performance issues might emerge?

### 2. Integration Risks
- How might this affect other parts of the system?
- What backwards compatibility issues exist?
- What migration challenges are there?

### 3. Operational Risks
- What could go wrong in production?
- What monitoring is missing?
- What recovery procedures are needed?

### 4. User Experience Risks
- How might users misuse this?
- What accessibility issues exist?
- What confusion might arise?

## Output Format

```
## Premortem: [Feature/Change]

### High Risk
- [Critical failure mode]
  → Mitigation: [How to prevent]

### Medium Risk
- [Significant issue]
  → Mitigation: [How to address]

### Low Risk
- [Minor concern]
  → Mitigation: [Simple fix]

### Recommendations
1. [Priority action]
2. [Secondary action]
3. [Nice to have]
```

## When to Run

- Before large refactoring
- Before deploying new features
- Before architectural changes
- When something feels risky

## Remember

- Be genuinely pessimistic
- Consider non-obvious failure modes
- Propose concrete mitigations
- Store risks as learnings for future reference
