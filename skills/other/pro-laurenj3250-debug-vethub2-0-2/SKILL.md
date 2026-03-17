---
name: pro
description: Professional engineering skill combining senior engineer thinking patterns, adaptive task assessment, and Google-grade standards. Invoke with /pro before any coding task to ensure production-quality work with proper planning, testing, and verification.
---

# /pro - Professional Engineering

Think like a senior engineer. Assess each unique task. Apply concrete standards.

## When to Use

Invoke `/pro` before ANY non-trivial coding task. The skill will:
1. Apply senior engineer thinking patterns
2. Discover what THIS specific task needs
3. Apply relevant engineering standards
4. Verify completion with evidence

## Three Layers

### Layer 1: Thinking Patterns

Think in constraints, not just features. See `references/thinking-patterns/`:

| Pattern | When to Apply |
|---------|---------------|
| **ask-vs-decide** | Unclear requirements, stuck > 30 min |
| **rabbit-hole-detection** | 2+ hours without progress, scope creeping |
| **smell-detection** | Code review, debugging, planning |
| **second-order-effects** | Before ANY change to existing system |
| **mental-models** | Learning new codebase, debugging |
| **debugging-mindset** | Any bug investigation |
| **requirements-validation** | Before starting implementation |

### Layer 2: Assessment Framework

Every task is unique. See `references/assessment-framework/`:

```
STEP 1: UNDERSTAND THIS TASK
├─ What's the actual goal?
├─ What does "done" look like?
└─ What edge cases exist?

STEP 2: DISCOVER PUZZLE PIECES
├─ What code already exists?
├─ What are the integration points?
└─ What constraints apply?

STEP 3: IDENTIFY GOTCHAS
├─ What's unique about THIS task?
└─ What could bite me?

STEP 4: PLAN THE FIT
├─ What order? What dependencies?
└─ What's my rollback plan?

STEP 5: IMPLEMENT WITH AWARENESS
├─ Fit patterns discovered
├─ Handle gotchas identified
└─ Integrate properly (not orphaned)

STEP 6: VERIFY AGAINST REQUIREMENTS
├─ Meet specific acceptance criteria?
├─ Handle edge cases identified?
└─ Evidence gate: tests pass, build succeeds
```

### Layer 3: Engineering Standards

Concrete thresholds. See `references/engineering-standards/`:

| Standard | Key Threshold |
|----------|---------------|
| **design-docs** | Required for > 1 week work, 5 sections, 10-day review |
| **testing-pyramid** | 70% unit / 20% integration / 10% E2E |
| **sre-principles** | SLI/SLO definitions, error budget = 100% - SLO% |
| **api-design** | Resource-oriented, standard methods only |
| **data-modeling** | P95 query < 50ms, migration safety pattern |
| **incremental-delivery** | 0% → 2% → 10% → 50% → 100% rollout |
| **performance-budgets** | API P95 < 200ms, error < 0.01% |
| **adrs** | Document architectural decisions |
| **dependency-management** | Evaluate before adding, security SLAs |

## Quick Reference

### Blocked Patterns (Always)
- Stubs, TODOs, placeholder implementations
- Mock/dummy data instead of real logic
- Happy-path only (no error handling)
- Features not connected (orphaned code)
- "Done" claims without fresh evidence

### Evidence Gate (Iron Law)
```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

1. IDENTIFY → What command proves this?
2. RUN      → Execute it (fresh, not cached)
3. READ     → Check output + exit code
4. VERIFY   → Does output confirm claim?
5. CLAIM    → Only now state completion
```

### Red Flag Language
- "Should work now" → STOP. Run verification.
- "I'm confident" → Confidence ≠ evidence
- "Probably fixed" → VERIFY with output

### Escape Hatches
| Situation | Skip | Follow-up |
|-----------|------|-----------|
| Production down | All | Document + tests after |
| Trivial one-liner | All | None |
| Spike/prototype | Verification | Mark throwaway |
| Time-critical hotfix | Deep discovery | Schedule proper fix |

## Skill Routing

Based on task discovery, auto-invoke:

| Context | Skills |
|---------|--------|
| UI work | `frontend-development`, `frontend-design`, `ui-styling` |
| Backend | `backend-development`, `databases` |
| Bug | `systematic-debugging`, `root-cause-tracing` |
| Complex | `writing-plans`, `sequential-thinking` |
| Before merge | `code-review`, `verification-before-completion` |

## The Formula

```
Philosophy (thinking patterns)
+ Process (assessment framework)
+ Standards (concrete thresholds)
= Professional Engineering
```

Philosophy without process is just advice.
Process without standards is just paperwork.
Standards without philosophy is just bureaucracy.
All three together = production-ready code.
