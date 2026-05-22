---
name: simplify-code
description: Simplify recently changed code for clarity and maintainability while preserving behavior. Use when the user says "simplify", "simplify code", "make this simpler", "clean up", or after implementing a logical chunk.
compatibility: Assumes filesystem read/write access; uses git if available to scope changes; does not require network.
---

# Simplify Code

Refine code to reduce unnecessary complexity while preserving behavior.

## Scope

- Default scope is **recently modified code** in the current session (prefer `git diff` / staged changes to identify).
- Do not perform broad refactors (renaming across the repo, architecture rewrites) unless the user explicitly requests it.

## Process

1. Identify the target scope:
   - Prefer staged changes: `git diff --staged`
   - Otherwise: `git diff` or user-provided file paths
2. Establish constraints:
   - Preserve public APIs and observable behavior unless the user asks otherwise
   - Preserve performance characteristics unless improvements are explicit and verified
   - Keep changes small and reviewable (multiple small commits/patches > one large rewrite)
3. Simplify with these priorities (highest to lowest):
   - Reduce nesting and control-flow complexity (guard clauses, clearer branching)
   - Remove redundancy and dead code (duplicate logic, unused variables, unreachable branches)
   - Improve names to match intent (avoid renaming beyond the touched surface area)
   - Split overly long functions into cohesive helpers where it reduces cognitive load
   - Replace ad-hoc patterns with existing local conventions (follow `AGENTS.md` / repo style)
4. Avoid “compression” patterns that reduce readability:
   - Nested ternaries
   - Dense one-liners that hide control flow or side effects
   - Over-general abstractions introduced solely to reduce line count
5. Validate:
   - Run the narrowest available checks/tests for the modified area
   - Re-check diffs to confirm only intended files changed
6. Report:
   - Summarize the simplifications as a short list of behavioral-preserving refactors
   - Call out any remaining complexity that was intentionally left in place (and why)

## Avoid

- Nested ternaries — prefer if/else or early returns
- Dense one-liners that hide control flow or side effects
- Abstractions introduced solely to reduce line count
- Renaming beyond the touched surface area
- Changes that require updating unrelated code

## Output Format

Provide:

- **What changed**: 3-8 bullets of the key simplifications
- **Why it is simpler**: 1-2 bullets focused on reduced branching/nesting, clearer invariants, or reduced duplication
- **Verification**: commands run (or “not run”) and the reasoning
