---
name: behavior-preserving-simplification
description: |-
  Use when simplifying code, reducing duplication, or clarifying flow while preserving behavior with tests.
  Triggers:
practices:
- pragmatic-programmer
skill_api_version: 1
user-invocable: false
hexagonal_role: supporting
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  tier: execution
  stability: experimental
  dependencies:
  - standards
  - refactor
  - validate
output_contract: 'refactor_result with sections: behavior_baseline, invariants, changes, verification, rollback_plan.'
---
# Simplify And Refactor Code Isomorphically

Make code simpler without changing what callers, users, persisted data, or
integrations can observe. Treat every edit as a behavior-preserving
transformation until evidence proves otherwise.

## Operating Rules

- Start by naming the behavior surface: public APIs, CLI flags, wire formats,
  database effects, files, environment variables, logs that tests assert, and
  user-visible UI states.
- Establish characterization tests before changing unclear or under-tested
  behavior. Prefer narrow tests that lock down current outputs, side effects,
  ordering, and error cases.
- Write down invariants that must remain true after the refactor. Include both
  domain invariants and mechanical invariants such as idempotence, ordering,
  resource cleanup, and concurrency assumptions.
- Make one reversible transformation at a time. Keep each diff small enough to
  review and roll back without losing unrelated work.
- Verify after each meaningful step with the smallest relevant test command.
  Broaden verification when the refactor crosses module boundaries.
- Do not combine behavior changes with simplification. If a bug is discovered,
  capture it separately unless the user explicitly asks to fix it now.

## Workflow

1. Inspect the target code and its call sites. Identify the observable contract,
   risky dependencies, and the smallest safe scope for the first change.
2. Build a behavior baseline. Run existing tests and add characterization tests
   for unprotected behavior before structural edits.
3. State invariants in the work notes or final report. Make the intended
   preservation target explicit enough for another engineer to audit.
4. Apply a single isomorphic transformation, such as extracting a pure helper,
   replacing duplicated branches with a shared path, simplifying conditionals,
   renaming for clarity, or moving code behind an equivalent interface.
5. Compare the diff against the invariants. Remove incidental churn, formatting
   noise, and unrelated cleanup.
6. Run targeted verification. If verification fails, rollback the latest
   transformation or isolate the behavioral difference before continuing.
7. Repeat only while the next simplification remains clearly valuable and low
   risk. Stop when additional cleanup would outgrow the evidence available.

## Characterization Tests

Good characterization tests describe what the current system does, not what the
system should ideally do. Cover representative success paths, boundary inputs,
known odd behavior, failure modes, and side effects. Use fixtures or golden
outputs only when they make behavioral drift easier to detect than assertions.

When tests are expensive, add a narrow harness around the refactor target and
keep the full suite for final confirmation. When tests cannot be added, document
the manual or command-line probes used as the baseline and keep the refactor
smaller.

## Diff Discipline

- Avoid broad reformatting unless the formatter is already the local standard
  and the target file is expected to be formatted.
- Preserve names, exported symbols, error text, and ordering unless the baseline
  proves they are not part of the contract.
- Prefer mechanical moves and extraction before semantic rewrites.
- Keep generated files, lockfiles, and unrelated dependency changes out of the
  refactor unless they are required for verification.
- Re-read the final diff as a reviewer looking for hidden behavior changes.

## Rollback

Every step needs a clear rollback point. If a transformation becomes tangled,
revert that step and choose a smaller path. If the baseline is too weak to prove
equivalence, stop and report the missing evidence instead of pushing through on
intuition.

## Output

Report the behavior baseline, invariants, changed files, verification commands,
and any residual risk. If rollback was needed, say what was rolled back and why.
