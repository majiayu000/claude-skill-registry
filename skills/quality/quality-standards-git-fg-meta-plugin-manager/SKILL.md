---
name: quality-standards
description: "Verify completion with evidence using 6-phase gates and three-way audits. Use when claiming task completion, committing code, or validating components. Not for skipping verification or bypassing quality gates."
context: fork
agent: Explore
---

# Quality Standards

## Core Principle: Evidence Over Assertion

**NO CLAIMS WITHOUT EVIDENCE.**

Every assertion requires fresh verification output. Every gate must pass sequentially.

| Instead of... | Use This Evidence... |
| ------------- | -------------------- |
| "I fixed the bug" | `Test auth_login_test.ts passed (Exit Code 0)` |
| "Build should work" | `npm run build: SUCCESS` |
| "TypeScript is fine" | `tsc --noEmit: 0 errors, 0 warnings` |
| "Tests pass" | `47 passed, 0 failed` |
| "Linting is clean" | `ESLint: no errors` |

## The 6-Phase Gate

**BUILD → TYPE → LINT → TEST → SECURITY → DIFF**

Gates pass in sequence. Stop on first failure.

| Phase | Checks | Typical Command |
| ----- | ------ | --------------- |
| BUILD | Compilation succeeds | `npm run build` |
| TYPE | Type safety | `tsc --noEmit` |
| LINT | Code style | `eslint . --max-warnings 0` |
| TEST | Tests pass | `npm test` |
| SECURITY | No secrets/vulns | `npm audit` |
| DIFF | Intentional changes | `git diff --stat` |

## Three-Way Audit

Before claiming completion, compare:

| Dimension | Question |
| --------- | -------- |
| **Request** | What did the user explicitly ask for? |
| **Delivery** | What was actually implemented? |
| **Standards** | What do quality standards specify? |

## Component Validation

| Check | How |
| ----- | --- |
| Structure | Read frontmatter, confirm valid YAML |
| Portability | Zero external `.claude/rules` references |
| Content | Critical constraint footer present |

## Recognition Questions

| Question | Answer |
| -------- | ------ |
| All gates passed with evidence? | Yes/No |
| Three-way audit complete? | Yes/No |
| Every claim backed by output? | Yes/No |

---

<critical_constraint>
**IRON LAW:** No claims without evidence. Run commands, capture output, report results.

Gates pass in sequence—stop on first failure.
Each claim requires fresh verification output.
Compare Request vs Delivery vs Standards in audits.
</critical_constraint>
