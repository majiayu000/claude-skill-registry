---
name: code-review
description: Base code review guidelines with prioritized focus on correctness, safety, and maintainability
category: development
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review Guidelines

This guide defines how the reviewer evaluates a pull request.

## Baseline Assumptions
- The code compiles.
- All tests pass.

## Normative Words
- MUST: Mandatory. Not following this is a violation of the guide.
- MUST NOT: Forbidden.
- SHOULD: Recommended in almost all cases; exceptions need a strong reason.
- SHOULD NOT: Generally discouraged; only do it with clear justification.
- MAY: Optional; use judgment.

## Scope and Priorities

The reviewer MUST:
- Focus on the actual diff and its impact.
- Prioritize in this order:
  1. Correctness and safety (including error handling policy).
  2. Public API and external behavior.
  3. Concurrency and performance issues with real impact.
  4. Readability, idioms, maintainability.

The reviewer MUST NOT:
- Invent business logic or protocol rules not implied by the code or docs.
- Demand large unrelated refactors unless there is a clear correctness or safety concern.

## Review Process

1. Read the PR description and understand the intent
2. Review the diff file by file
3. For each change, consider:
   - Does this introduce bugs or security issues?
   - Is the API appropriate?
   - Are edge cases handled?
   - Is error handling adequate?
4. Provide actionable, specific feedback
5. Distinguish blocking issues from suggestions

## Feedback Format

Use clear prefixes:
- **MUST FIX**: Blocking issue that needs resolution
- **SHOULD FIX**: Strong recommendation
- **CONSIDER**: Optional improvement
- **QUESTION**: Clarification needed
