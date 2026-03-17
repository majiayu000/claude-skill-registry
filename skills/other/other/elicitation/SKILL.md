---
name: elicitation
description: Auto-review skill for expert agents. After coding, expert applies elicitation techniques to self-correct before sniper validation. Inspired by BMAD-METHOD.
argument-hint: "[--auto] [--manual] [--skip]"
color: purple
user-invocable: false
---

# Elicitation Skill

## Purpose

Enable expert agents to **self-review and self-correct** their code before external validation (sniper). Based on BMAD-METHOD's 75 elicitation techniques.

---

## 3 Execution Modes

### Mode 1: MANUAL (default)
```
Expert presents 5 relevant techniques → User chooses → Expert applies
```

### Mode 2: AUTO (--auto)
```
Expert auto-detects code type → Auto-selects techniques → Applies silently
```

### Mode 3: SKIP (--skip)
```
Skip elicitation → Go directly to sniper validation
```

---

## Quick Start

**After Execute phase, expert runs:**
```bash
# Manual mode (default)
> Apply elicitation skill

# Auto mode (no prompts)
> Apply elicitation skill --auto

# Skip self-review
> Apply elicitation skill --skip
```

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────┐
│              ELICITATION WORKFLOW                       │
│                                                         │
│  Step 0: Init           → Load context                 │
│  Step 1: Analyze Code   → Detect code type             │
│  Step 2: Select         → Choose techniques (or auto)  │
│  Step 3: Apply Review   → Execute techniques           │
│  Step 4: Self-Correct   → Fix own issues               │
│  Step 5: Report         → Summary before sniper        │
└─────────────────────────────────────────────────────────┘
```

---

## Auto-Detection Matrix

| Code Type Detected | Auto-Selected Techniques |
|--------------------|--------------------------|
| Authentication/Security | Security Audit, OWASP Check, Input Validation |
| API Endpoints | Error Handling, Type Coverage, API Contracts |
| Database/ORM | N+1 Detection, Migration Safety, Data Integrity |
| UI Components | Accessibility, Edge Cases, Loading States |
| Business Logic | SOLID Compliance, Unit Test Coverage, Edge Cases |
| Refactoring | Breaking Changes, Regression Analysis, Backward Compat |
| Performance Critical | Profiling, Memory Analysis, Complexity Check |

---

## Technique Categories (12)

Full catalog: `references/techniques-catalog.md`

1. **Code Quality** (7): Code review, Pattern detection, Complexity analysis...
2. **Security** (7): OWASP audit, Input validation, Auth check...
3. **Performance** (6): Profiling, N+1 detection, Memory analysis...
4. **Architecture** (6): SOLID check, Dependency analysis, Coupling review...
5. **Testing** (6): Edge cases, Boundary testing, Error paths...
6. **Documentation** (6): API review, Comment check, Type coverage...
7. **UX** (6): Accessibility, Error messages, Loading states...
8. **Data** (6): Schema validation, Migration safety, Data integrity...
9. **Concurrency** (6): Race conditions, Deadlock analysis, State sync...
10. **Integration** (7): API contracts, Backward compat, Breaking changes...
11. **Observability** (6): Logging, Metrics, Error tracking...
12. **Maintainability** (6): Readability, Naming, File organization...

**Total: 75 techniques**

---

## Integration with APEX

```
A-nalyze → P-lan → E-xecute → [ELICIT] → X-amine
                       │          │           │
                       ▼          ▼           ▼
                    Expert    Expert       sniper
                     code    self-review   (final)
```

**Benefits:**
- Expert catches own mistakes before sniper
- Faster validation (less sniper corrections)
- Knowledge retention (expert learns from self-review)

---

## Forbidden

- ❌ Skip init step (must load context)
- ❌ Apply techniques without understanding code type
- ❌ Self-correct without documenting changes
- ❌ Report without listing applied techniques
- ❌ Use techniques outside expertise domain

---

## Steps Reference

| Step | File | Purpose |
|------|------|---------|
| 0 | `steps/step-00-init.md` | Load context, detect mode |
| 1 | `steps/step-01-analyze-code.md` | Analyze written code |
| 2 | `steps/step-02-select-techniques.md` | Select techniques |
| 3 | `steps/step-03-apply-review.md` | Apply review |
| 4 | `steps/step-04-self-correct.md` | Self-correct |
| 5 | `steps/step-05-report.md` | Generate report |
