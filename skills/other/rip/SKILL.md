---
name: rip
description: >-
  Review implementation plan for business value alignment. Use when asked to
  'review my plan', 'walk through implementation', 'check plan against PRD',
  'review technical decomposition', or 'is my plan aligned with requirements'.
  NOT for code review (use /sr), NOT for creating tasks (use /ct),
  NOT for static code analysis (use /code-analysis).
argument-hint: [plan-file-path]
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Review Implementation Plan (RIP)

Step-by-step review of implementation plan. Focus: **business value** through technical understanding.

## Protocol

### Phase 1: Analysis

Before responding:
1. Read the plan completely
2. Study related code (Grep, Read) — verify, don't assume
3. Compare with PRD/business requirements — run alignment checklist:
   - Measurable outcomes/KPIs defined?
   - Scope matches PRD (no creep, no gaps)?
   - Risks or dependencies identified?
   - Each step ties to a user-facing outcome?
4. Determine business value of each step
5. If plan is ambiguous or missing context — use AskUserQuestion to clarify before proceeding

Record mismatches (extra features, missed requirements, logic conflicts) for discussion. Criticism = facts + question.

**Review format:**

```
## Overview

**Business goal:** [what problem it solves]
**Scope:** [components] | [files] | [complexity]
**Plan:** [N steps with names]

**Warning** (if any):
- [Problem] — contradicts [source]

Ready for first step?
```

### Phase 2: Walkthrough

Wait for user confirmation ("ready", "next") before advancing to each step. Verify PRD alignment per step — if mismatch found, flag it and request confirmation before continuing.

**Step format:**

```
### Step [N]: [Name]

**Why:** [business reason]
**What:** [technical essence]
**Concepts:** [term]: [analogy]
**Impact:** [code] → [user-facing change]
**Code:** [if relevant]

**Warning** (if any):
- [PRD issue]
- **Question:** [clarification]

---
Questions? Next?
```

### Phase 3: Summary

```
## Summary

**Covered:** [recap]
**Value:** [why it matters to user]
**Concepts:** [list]

**Self-check:**
1. [Business question]
2. [Technical question]
```

## Rules

| Principle | Action |
|-----------|--------|
| Business-first | Start with "why for the user" |
| Simplicity | Term = analogy |
| Specificity | Real files/endpoints |
| Progress | Every 3-4 steps: "X of N" |
| Criticality | Flag PRD mismatches **only** when present |
| Constructiveness | Facts + question, no dismissiveness |

## Example

**Input:** Progress tracking plan

**Overview:**

> **Business goal:** Users see progress → motivation
> **Scope:** backend + DB | `src/modules/progress/` | medium
> **Plan:** 4 steps (model, API, logic, integration)
>
> **Warning:**
> - Plan doesn't mention visualization — PRD requires charts. Out of scope?
> - PRD: PDF export — not in plan. Include?

**Step 1:**

> **Why:** Store word learning history
> **What:** `WordProgress` table links user+word, stores metrics
> **Concepts:** Prisma schema = DB blueprint as code
> **Impact:** "Progress" screen → word-level stats
>
> **Warning:**
> - PRD: track repetition intervals (spaced repetition). Schema: only `lastSeen`, no history.
> - **Question:** Plan — current state only or full history?

## Related Skills

| Need | Use |
|------|-----|
| Review code before merge | `/sr` |
| Create implementation plan | `/ct` |
| Analyze code architecture | `/code-analysis` |
| Create/update PRD or JTBD | `/product` |
