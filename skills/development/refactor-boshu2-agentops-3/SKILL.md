---
name: refactor
description: 'Execute one behavior-preserving structural transformation and report evidence. Triggers: "refactor this", "simplify without changing behavior".'
practices:
- refactoring
- legacy-code-seams
- design-patterns
hexagonal_role: supporting
consumes:
- repo-context
produces:
- code-changes
context_rel: []
skill_api_version: 1
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  capabilities: [refactor]
  effects: []
  canonical_status: canonical
  disposition: keep_specialist
  tier: execution
  dependencies: []
output_contract: code changes with regression evidence
---
# Refactor — one structural experiment

Refactor changes structure while preserving observable behavior. It performs one
caller-selected transformation and reports the result.

## Procedure

1. Name the preserved behavior and the focused acceptance surface.
2. Record an honest baseline, including any reproducible ambient failures.
3. Apply one bounded transformation: extract, rename, inline, simplify,
   encapsulate, move, or delete dead code.
4. Run the focused check and the smallest package-level regression check justified
   by the changed surface.
5. Return the diff summary, commands, results, and behavior not checked.

Do not combine a newly discovered behavior fix with the structural change. A red
result is evidence for the caller; this skill does not revert, narrow, retry,
commit, validate, or route subsequent work automatically.

## References

- [Behavior-preserving simplification](references/behavior-preserving-simplification.md)
- [Behavior scenarios](references/refactor.feature)
