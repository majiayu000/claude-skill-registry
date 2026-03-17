---
name: code-review
description: >-
  Three-stage code review protocol: spec compliance, code quality, and domain
  integrity. Activate when reviewing code, preparing PRs, assessing
  implementation quality, or checking that code matches requirements. Triggers
  on: "review this code", "prepare PR", "check implementation", "code quality",
  "does this match the spec".
license: CC0-1.0
compatibility: Designed for any coding agent (Claude Code, Codex, Cursor, OpenCode, etc.)
metadata:
  author: jwilger
  version: "1.0"
  requires: [domain-modeling]
  context: [source-files, test-files, domain-types, git-history]
  phase: ship
  standalone: true
---

# Code Review

**Value:** Feedback and communication -- structured review catches defects that
the author cannot see, and separating review into stages prevents thoroughness
in one area from crowding out another.

## Purpose

Teaches a systematic three-stage code review that evaluates spec compliance,
code quality, and domain integrity as separate passes. Prevents combined
reviews from letting issues slip through by ensuring each dimension gets
focused attention.

## Practices

### Three Stages, In Order

Review code in three sequential stages. Do not combine them. Each stage has a
single focus. A failure in an earlier stage blocks later stages -- there is no
point reviewing code quality on code that does not meet the spec.

**Stage 1: Spec Compliance.** Does the code do what was asked? Not more, not
less.

For each acceptance criterion or requirement:

1. Find the code that implements it
2. Find the test that verifies it
3. Confirm the implementation matches the spec exactly

Mark each criterion: PASS, FAIL (missing/incomplete/divergent), or CONCERN
(implemented but potentially incorrect). Flag anything built beyond
requirements as OVER-BUILT.

If any criterion is FAIL, stop. Return to implementation before continuing.

**Stage 2: Code Quality.** Is the code clear, maintainable, and well-tested?

Review each changed file for:

- **Clarity:** Can you understand what the code does without extra context?
  Are names descriptive? Is the structure obvious?
- **Domain types:** Are semantic types used where primitives appear? (Refer to
  domain-modeling skill for primitive obsession detection.)
- **Error handling:** Are errors handled with typed errors? Are all paths
  covered?
- **Test quality:** Do tests verify behavior, not implementation? Is coverage
  adequate for the changed code?
- **YAGNI:** Is there unused code, speculative features, or premature
  abstraction?

Categorize findings by severity:
- CRITICAL: Bug risk, likely to cause defects
- IMPORTANT: Maintainability concern, should fix before merge
- SUGGESTION: Style or minor improvement, optional

If any CRITICAL issue exists, stop. Return to implementation.

**Stage 3: Domain Integrity.** Final gate -- does the code respect domain
boundaries?

Check for:

1. **Compile-time enforcement opportunities:** Are tests checking things the
   type system could enforce instead?
2. **Domain type consistency:** Are semantic types used at all boundaries, or
   do primitives leak through?
3. **Validation placement:** Is validation at construction (parse-don't-validate),
   not scattered through business logic?
4. **State representation:** Can the types represent invalid states?

Flag issues but do not block on suggestions. Domain integrity flags are
strongly recommended but not required for merge.

### Review Output

Produce a structured summary after all three stages:

```
REVIEW SUMMARY
Stage 1 (Spec Compliance): PASS/FAIL
Stage 2 (Code Quality): PASS/FAIL/PASS with suggestions
Stage 3 (Domain Integrity): PASS/FAIL/PASS with flags

Overall: APPROVED / CHANGES REQUIRED

If CHANGES REQUIRED:
  1. [specific required change]
  2. [specific required change]
```

### Handling Disagreements

When your review finding conflicts with the implementation approach:

1. State the concern with specific code references
2. Explain the risk -- what could go wrong
3. Propose an alternative
4. If no agreement after one round, escalate to the user

You exist to catch what the author missed, not to block progress.

### Business Value and UX Awareness

During Stage 1, also consider:

- Does this slice deliver visible user value?
- Are acceptance criteria specific and testable (not vague)?
- Does the user journey remain coherent after this change?
- Are edge cases and error states handled from the user's perspective?

These are not blocking concerns but should be noted when relevant.

## Enforcement Note

This skill provides advisory guidance. It instructs the agent on correct
review procedure but cannot mechanically prevent skipping stages or merging
without review. On harnesses with plugin support, enforcement plugins can
gate PR creation on review completion. On other harnesses, the agent follows
these practices by convention. If you observe stages being skipped, point it
out. For available enforcement plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After completing a review guided by this skill, verify:

- [ ] All three stages were performed separately, in order
- [ ] Every acceptance criterion was mapped to code and tests in Stage 1
- [ ] Each changed file was assessed for clarity and domain type usage in Stage 2
- [ ] Domain integrity was checked for compile-time enforcement opportunities in Stage 3
- [ ] A structured summary was produced with clear PASS/FAIL per stage
- [ ] Any CHANGES REQUIRED items list specific, actionable fixes

If any criterion is not met, revisit the relevant stage before finalizing.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **domain-modeling:** Provides the primitive obsession and parse-don't-validate
  principles referenced in Stage 2 and Stage 3
- **tdd-cycle:** Reviews often follow a TDD cycle; this skill validates the
  output of that cycle
- **mutation-testing:** Can follow code review as an additional quality gate

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill domain-modeling
```
