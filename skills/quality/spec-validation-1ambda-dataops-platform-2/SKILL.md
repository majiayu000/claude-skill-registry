---
name: spec-validation
description: Self-evaluation and quality validation for specifications and documents. Identifies gaps, contradictions, and missing details using structured checklists. Use after drafting specs, PRDs, or feature documents.
---

# Spec Validation

Systematic quality validation for specifications using structured checklists and self-evaluation patterns.

## When to Use

- After drafting *_FEATURE.md specifications
- Reviewing PRDs for completeness
- Validating requirements before handoff
- Self-checking document quality

## Core Principle

> **The best form of feedback is clearly defined rules, then explaining which rules failed and why.**

---

## Validation Framework

### 1. Completeness Check

| Section | Required Elements | Validation Question |
|---------|-------------------|---------------------|
| Problem | Specific pain point | Is the problem measurable, not vague? |
| Users | Primary + secondary | Are personas defined with proficiency? |
| Scope | In-scope + non-goals | Are explicit exclusions documented? |
| Success | Quantified metrics | Can we measure success after 30 days? |
| Risks | Scenarios + mitigations | Is worst-case documented with exit strategy? |

### 2. Clarity Check

| Criterion | Test | Fix |
|-----------|------|-----|
| No TBD/TODO | Search for "TBD", "TODO", "??", "TBC" | Resolve or escalate |
| Acronyms defined | All acronyms in glossary | Add definitions |
| Edge cases covered | Each use case has edge cases | Document behavior |
| Error messages actionable | User can self-resolve at 3 AM | Add context/guidance |

### 3. Consistency Check

| Check | Method | Resolution |
|-------|--------|------------|
| Policy contradictions | Compare rules pairwise | Document precedence |
| Trade-off conflicts | Map priority vs constraint | Make explicit choice |
| Priority ambiguity | Count must-have items | Limit to 3-5 MVP items |

### 4. Feasibility Check

| Aspect | Validation | Owner |
|--------|------------|-------|
| Technical constraints | Engineering review | Tech Lead |
| Dependencies | Identify external blockers | PM |
| Timeline | Scope vs deadline match | PM + Eng |
| Risks | Mitigation plans exist | PM |

---

## Self-Evaluation Pattern

Use `mcp__sequential-thinking__sequentialthinking` for systematic review:

```python
# Structured self-evaluation
mcp__sequential-thinking__sequentialthinking(
    thought="Reviewing spec for completeness: checking problem statement",
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)
```

### Sequential Review Steps

1. **Problem Clarity**: Is the root problem specific and measurable?
2. **User Definition**: Are primary users and stakeholders identified?
3. **Scope Boundaries**: Are in-scope and non-goals explicit?
4. **Success Criteria**: Can we objectively measure success?
5. **Risk Coverage**: Are failure scenarios and rollback documented?

---

## Validation Report Template

```markdown
## Spec Validation Report: {FEATURE_NAME}

### Summary
- **Overall Status**: PASS / NEEDS REVISION
- **Critical Issues**: {count}
- **Warnings**: {count}

### Completeness (X/5 sections)
| Section | Status | Issue |
|---------|--------|-------|
| Problem | PASS/FAIL | {detail if fail} |
| Users | PASS/FAIL | {detail if fail} |
| Scope | PASS/FAIL | {detail if fail} |
| Success | PASS/FAIL | {detail if fail} |
| Risks | PASS/FAIL | {detail if fail} |

### Clarity Issues
- [ ] {Issue 1}
- [ ] {Issue 2}

### Consistency Issues
- [ ] {Contradiction 1}

### Open Questions (Require Stakeholder Input)
1. {Question needing clarification}

### Recommendations
1. {Specific fix recommendation}
```

---

## Common Validation Failures

| Failure | Detection | Resolution |
|---------|-----------|------------|
| Vague success metric | "Improve", "faster", "better" | Quantify with numbers |
| Missing non-goals | No explicit exclusions | Ask "What are we NOT doing?" |
| Undefined edge cases | Happy path only | Apply "3 AM Test" |
| Policy contradiction | Rule A conflicts with Rule B | Document precedence |
| Stakeholder conflict | User A vs User B needs | Explicit prioritization |

---

## Integration Points

### After requirements-discovery
```
Discovery Interview Complete
    -> Draft *_FEATURE.md
    -> spec-validation (this skill)
    -> Identify gaps
    -> Follow-up questions
    -> Final draft
```

### Before implementation
```
*_FEATURE.md Finalized
    -> spec-validation final check
    -> Engineering review
    -> Implementation begins
```

---

## Quick Checklist (Copy/Paste)

```markdown
### Pre-Finalization Checklist
- [ ] Problem is specific, not vague
- [ ] Success metrics are quantified
- [ ] Non-goals are explicitly stated
- [ ] No TBD/TODO items remain
- [ ] Acronyms defined
- [ ] Edge cases documented
- [ ] Error messages are user-actionable
- [ ] No policy contradictions
- [ ] Trade-offs explicitly documented
- [ ] Priorities clear (must-have vs nice-to-have)
- [ ] Technical constraints validated
- [ ] Dependencies identified
- [ ] Risks have mitigation plans
```
