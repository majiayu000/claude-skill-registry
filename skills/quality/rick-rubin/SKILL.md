---
name: rick-rubin
description: Enforce scope discipline and simplicity for software agent tasks.
Use when: (1) scope is drifting or requirements are unclear, (2) implementing
from an existing plan with minimal deviation, (3) reviewing changes for
unnecessary complexity or refactor creep, (4) analyzing bugs and root causes
without expanding scope. Select and inject exactly one prompt per task.

category: principles
---

# SKILL: rick-rubin

Apply scope discipline and simplicity. Detect scope drift, force clarity, and apply
the minimum necessary rigor to review, implement, or refactor without turning
every task into a redesign. Select and inject exactly one prompt at a time,
based on context.

## Core Philosophy

- Prefer simplicity over cleverness.
- Treat deletion as progress.
- Defend scope explicitly.
- Allow large refactors only when clearly justified.
- Do not conflate analysis, decision, planning, and execution.

## Goals

- Prevent accidental scope creep.
- Keep diffs small and intention-aligned.
- Force clarity before implementation.
- Make deeper issues explicit and unavoidable.
- Produce plans that other agents cannot reinterpret or evade.

## Non-Goals

- Avoid perpetual refactoring.
- Avoid redesign-by-default.
- Avoid speculative architecture work.
- Avoid auto-escalation without signal.
- Avoid multi-agent orchestration requirements.

## Context Signals to Watch For

1. Directory or planning document review intent
   Keywords: review directory, planning docs, PLAN.md, README, ADR, TODO, design doc, scope
2. Implementation intent from an existing plan
   Keywords: implement this plan, follow the plan, execute, apply feedback
3. Code review with change summary
   Keywords: review changes, diff, PR, patch, summary of changes
4. Bug findings and fix discussion
   Keywords: bug, regression, fix, failure, why did this happen
5. Post-reflection decision to address deeper issues
   Keywords: deeper issues, technical debt, root cause must be fixed
6. Strictness signal
   Explicit: aggressive, ruthless, zero tolerance, scope lockdown
   Implicit: repeated scope creep, repeated rework, frustration signals

## Prompt Registry

### A) Review from Scratch + Moderate Scope Defense

Review this directory and all planning documents within it (e.g., PLAN.md, README, ADRs, TODOs, design docs, notes). Your goal is to tighten scope and improve clarity without breaking the project’s intended outcomes.

Produce:
- A concise description of the project’s intended goal.
- A list of unclear or conflicting requirements.
- High-leverage clarification questions.
- A scope-trim proposal (unused, speculative, premature, redundant items).
- A keep-list of what is clearly required right now.

Guidance:
- Prefer a tight MVP.
- Defer non-essential work to a clear “Later” section.
- Reference concrete files or sections.

### B) Review from Scratch + Aggressive Scope Defense

Audit the directory and all planning documents. Assume scope creep risk.

Produce:
1. One-sentence project goal (or state why it cannot be derived).
2. Hard exclusions (features, abstractions, integrations not required).
3. Dead weight list (unused docs, stale TODOs, speculative sections).
4. Blocking ambiguities that must be resolved.
5. Minimal execution set required for the next milestone.

Rules:
- Default action is delete, archive, or defer.
- No additions.
- No redesigns.
- Reference specific files and sections.

### C) Follow Plan + Moderate Scope Discipline

Implement changes using the plan as the source of truth.

Rules:
- Do not add features or abstractions outside the plan.
- Improvements may be noted but not implemented unless they reduce scope.
- Prefer the smallest diff that fully satisfies the plan.

Execution:
- Implement all steps.
- Include tests only if specified.
- Cleanup only where required by the plan.

### D) Follow Plan + Zero Tolerance Scope Lockdown

The plan is a contract.

Rules:
- No deviations.
- No extra features, refactors, or generalization.
- No cleanup unless explicitly required.

Execution:
- Follow steps in order.
- Make the smallest possible diff.
- If ambiguity exists, report it and proceed with the least-scope option.

### E) Review Implementation + Moderate Scope Defense

Use the provided summary only as a navigation aid.

Review the actual code changes directly.

Identify:
- Scope expansion beyond requirements.
- Unnecessary abstractions or helpers.
- Indirect complexity increases.

For each concern:
1. What changed
2. Why it may be unnecessary
3. Minimal corrective action

Do not propose new features.
Optimize for clarity and minimal diff.

### F) Review Implementation + Aggressive Scope Defense

Treat the summary as potentially inaccurate.

Review changes line by line.

Assume all added behavior is unnecessary until proven required.

Rules:
- No new features.
- No future-proofing.
- No stylistic refactors.
- No new abstractions or indirection.

For violations:
1. Exact code location
2. Why it violates scope
3. Minimal rollback or deletion

If unsure, flag it.

### G) Reflection on Fixes + Moderate Scope Defense

Assess whether fixes address root causes or symptoms.

Identify:
- Design decisions that enabled the bugs.
- Recurring patterns that increase failure likelihood.
- Acceptable tradeoffs vs structural weaknesses.

Describe deeper issues succinctly.
Do not propose redesigns.

### H) Reflection on Fixes + Aggressive Scope Defense

Determine whether fixes address root causes or only symptoms.

Identify:
- Specific architectural decisions involved.
- Concrete patterns and their failure modes.

Do not propose fixes unless strictly necessary.
Explicitly justify deferrals.

### I) Refactor Plan Handoff + Moderate Scope Discipline

Write a clear plan for another agent to implement.

The plan must:
- Fix root causes and reported bugs.
- Address enabling technical debt only where relevant.
- Avoid speculative cleanup.

Structure:
1. Goals
2. Non-goals
3. Ordered steps
4. Validation criteria

The plan must be unambiguous and hard to reinterpret.

### J) Refactor Plan Handoff + Zero Tolerance Scope Lockdown

Write a binding refactor plan.

Requirements:
- Eliminate root causes completely.
- Replace or remove enabling patterns.
- No partial fixes.

Rules:
- No deferrals.
- No alternatives.
- No scope expansion.

Structure:
1. Problem statement
2. Refactor mandate
3. Step-by-step execution
4. Explicit out-of-scope list
5. Completion checklist

## Routing Rules

1. If implementing a plan, use C or D.
2. If reviewing code changes, use E or F.
3. If reviewing docs or scope, use A or B.
4. If analyzing bugs, use G or H.
5. If planning a deep refactor, use I or J.

Default strictness is moderate. Escalate only with signal.

## Guardrails

- For routine execution work, prefer lower-cost model tiers; for ambiguous root-cause reasoning, escalate deliberately. Reference `model-router` when explicit routing guidance is needed.
- Inject one prompt per task.
- Do not stack prompts.
- Do not plan refactors without reflection.
- Prefer deletion over addition.

### Prompt E Exception: Learning-Oriented Anti-Regression Fixes

During Prompt E review, learning-oriented, non-runtime process fixes are allowed when tied to a concrete incident and repeat-risk prevention. This is the only case where a review may include corrective edits beyond the original scope.

Required evidence fields when using this exception:
- **Incident**: What went wrong (specific, not hypothetical).
- **Repeat-risk**: Why it will happen again without the fix.
- **Minimal fix**: The smallest change that prevents recurrence.

## Minimal Usage

Invoke when needed.
Optional: use a “strict” keyword to force aggressive variants.