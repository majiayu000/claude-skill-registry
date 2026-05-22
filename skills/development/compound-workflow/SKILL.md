---
name: compound-workflow
description: Structured development workflow: brainstorm, plan, work, review, compound.
Use when: (1) starting a new feature end-to-end, (2) coordinating multi-phase
development work, (3) ensuring each phase completes before the next begins.
Orchestration-thin — routes to existing local skills for phase-specific logic.

category: habits
---

# Workflow

A structured development cycle with five phases. Each phase has a clear purpose and handoff to the next.

## Cycle

```
brainstorm → plan → work → review → compound
   (WHAT)    (HOW)  (DO)  (CHECK)  (LEARN)
```

### Phase Summary

| Phase | Purpose | Output | Routes To |
|-------|---------|--------|-----------|
| Brainstorm | Explore WHAT to build | Decision document | — |
| Plan | Define HOW to build it | Structured plan file | `rick-rubin` (scope discipline) |
| Work | Execute the plan | Working code + tests | `tdd` (test-driven), `rick-rubin` (scope) |
| Review | Verify quality and correctness | Review findings | `diff-review`, `code-review-*` |
| Compound | Document what was learned | Solution document | — |

## Phase Details

### 1. Brainstorm

Explore requirements and approaches before committing to a plan. Answer WHAT to build.

- Understand the idea through collaborative dialogue
- Explore 2-3 concrete approaches
- Capture decisions in a brainstorm document
- Apply YAGNI — prefer simpler approaches

**Exit condition:** Idea is clear, approach chosen, decisions documented.

**Next:** Plan phase auto-detects brainstorm documents.

### 2. Plan

Transform the brainstorm output (or a direct feature request) into a structured plan.

- Research existing codebase patterns
- Choose implementation detail level (minimal, standard, comprehensive)
- Run spec flow analysis for gap detection
- Write plan file with acceptance criteria

**Exit condition:** Plan written, acceptance criteria defined.

**Routes to:** `rick-rubin` for scope discipline during planning.

See [plan-phase.md](references/plan-phase.md) for detail levels and plan structure.

### 3. Work

Execute the plan systematically.

- Read plan and clarify ambiguities upfront
- Break plan into tasks
- Execute in priority order: implement, test, commit incrementally
- Follow existing codebase patterns

**Exit condition:** All tasks complete, tests pass.

**Routes to:** `tdd` for test-driven implementation, `rick-rubin` for scope defense.

See [work-phase.md](references/work-phase.md) for execution workflow.

### 4. Review

Verify quality through multi-angle analysis.

- Run code review against the diff
- Check security, performance, architecture, quality
- Synthesize findings by severity
- Address critical findings before merge

**Exit condition:** No critical findings remain, PR created.

**Routes to:** `diff-review` for security-focused review, `code-review-rust` or `code-review-ts` for language-specific review.

See [review-phase.md](references/review-phase.md) for review structure.

### 5. Compound

Document the solved problem to compound team knowledge.

- Capture problem symptoms, investigation steps, root cause, working solution
- Write structured documentation with searchable frontmatter
- Cross-reference related solutions

**Exit condition:** Solution documented in `docs/solutions/`.

See [compound-phase.md](references/compound-phase.md) for documentation structure.

## Usage

Run phases individually as needed. Not every task requires all five phases.

| Scenario | Start At |
|----------|----------|
| New feature, unclear requirements | Brainstorm |
| Feature with clear requirements | Plan |
| Bug fix with known cause | Work |
| PR ready for review | Review |
| Problem just solved | Compound |

## Routing to Local Skills

This skill is an orchestrator. It does not duplicate the internals of:
- `tdd` — test-driven development logic stays in tdd
- `rick-rubin` — scope discipline stays in rick-rubin
- `diff-review` — security review stays in diff-review
- `code-review-rust` / `code-review-ts` — language review stays in those skills

Cross-link only. Do not expand those skills' responsibilities.