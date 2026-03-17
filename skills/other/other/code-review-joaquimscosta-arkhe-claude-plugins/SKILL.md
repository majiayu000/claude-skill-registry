---
name: code-review
description: >
  Conduct comprehensive code reviews using the Pragmatic Quality framework with
  confidence-based filtering, hierarchical analysis (architecture, security,
  maintainability, testing, performance), and PR-level risk assessment.
  Use when user runs /code-review, /review:code-review, requests a "code review",
  "review my changes", "PR review", or mentions "review diff", "review branch".
disable-model-invocation: true
argument-hint: "[output-directory]"
---

# Code Review

Pragmatic Quality framework — balance rigorous engineering standards with development speed. High-signal findings only.

## Parse Arguments

**Output Path Configuration**:
- If `$ARGUMENTS` is provided and non-empty: Use `$ARGUMENTS` as the output directory
- Otherwise: Use default `./reviews/code/`

Example usage:
- `/review:code-review` → saves to `./reviews/code/`
- `/review:code-review custom/reviews` → saves to `custom/reviews/`

## Git Analysis

Analyze the following outputs to understand the scope and content of the changes.

GIT STATUS:

```
!`git status`
```

FILES MODIFIED:

```
!`git diff --name-only origin/HEAD...`
```

COMMITS:

```
!`git log --no-decorate origin/HEAD...`
```

DIFF CONTENT:

```
!`git diff --merge-base origin/HEAD`
```

Review the complete diff above. This contains all code changes to review.

## Review Philosophy

1. **Net Positive > Perfection**: Determine if the change improves overall code health. Do not block on imperfections if the change is a net improvement.
2. **Focus on Substance**: Prioritize architecture, design, business logic, security, and complex interactions over style.
3. **Grounded in Principles**: Base feedback on SOLID, DRY, KISS, YAGNI — not opinions. Every non-Nit suggestion must cite a named principle.
4. **Signal over Noise**: Better to miss a minor issue than flood the review with low-confidence findings. Target >60% signal ratio.

## Confidence & Signal Quality

Before reporting any finding, score confidence 1-10:

| Confidence | Action | Triage Level |
|------------|--------|--------------|
| 9-10 | Report — clear issue with concrete impact | Blocker or Improvement |
| 7-8 | Report — strong evidence, may need context | Improvement or Question |
| 5-6 | Suppress — too speculative to report | Do not include |
| Below 5 | Discard — likely false positive | Do not include |

**Finding caps**: Max **8 meaningful findings** (Blocker + Improvement + Question) and max **2 Nits** per review. If more exist, keep the highest-confidence items and note "additional observations available on request."

**Self-reflection**: After generating all candidate findings, re-evaluate each in the context of the full set. Remove redundant, low-signal, or style-only items. Apply false positive filtering from [WORKFLOW.md](WORKFLOW.md).

## Phase 0 — PR Assessment

Before line-by-line analysis, assess the PR holistically:

1. **Atomicity**: Is this a single, cohesive change? Flag if it bundles unrelated changes.
2. **Risk Level**: Classify as Low / Medium / High / Critical based on change types (see [WORKFLOW.md](WORKFLOW.md)).
3. **Breaking Changes**: Detect signals — API signature changes, migrations, removed exports, renamed env vars.
4. **Architectural Fit**: Does the approach align with existing patterns and system boundaries?

Include the PR Assessment in the report header.

## Hierarchical Review Framework

Analyze code using this prioritized checklist. See [WORKFLOW.md](WORKFLOW.md) for detailed checklists per category.

| Priority | Category | Focus Areas |
|----------|----------|-------------|
| 1 (Critical) | Architecture & Integrity | Patterns, modularity, SRP, complexity, atomicity |
| 2 (Critical) | Functionality & Correctness | Logic, edge cases, race conditions, state, idempotency |
| 3 (Non-Negotiable) | Security | Input validation, auth, secrets, data exposure, crypto |
| 4 (High) | Maintainability & Readability | Clarity, naming, complexity, comments, duplication |
| 5 (High) | Testing Strategy | Coverage, failure modes, isolation, integration tests |
| 6 (Important) | Performance & Scalability | N+1 queries, bundle size, caching, memory leaks |
| 7 (Important) | Dependencies & Documentation | Third-party risk, license, API docs, config changes |

## Triage Matrix

Categorize every finding using confidence thresholds:

- **[Blocker]**: Must fix before merge — security vulnerability, correctness bug, architectural regression (confidence >=8)
- **[Improvement]**: Strong recommendation for improving the implementation (confidence >=7)
- **[Question]**: Seeks clarification on intent — not a change request (confidence >=6)
- **[Nit]**: Minor polish, optional — max 2 per review
- **[Praise]**: Acknowledge a good design decision — max 1 per review

## Output Instructions

1. **Create output directory** using Bash: `mkdir -p {output-directory}`
2. **Save the report** to: `{output-directory}/{YYYY-MM-DD}_{HH-MM-SS}_code-review.md`

Include this header in the saved file:

```markdown
# Pragmatic Code Review Report

**Date**: {ISO 8601 date}
**Branch**: {current branch name}
**Commit**: {short commit hash}
**Reviewer**: Claude Code (pragmatic-code-review)

## PR Assessment

| Attribute | Value |
|-----------|-------|
| **Risk Level** | {Low / Medium / High / Critical} |
| **PR Type** | {Feature / Bugfix / Refactor / Config / Test-only / Docs} |
| **Atomicity** | {Atomic / Mixed — consider splitting} |
| **Breaking Changes** | {None / Yes — description} |

---
```

3. **Display the full report** to the user in the chat
4. **Confirm the save**: Report saved to: {output-directory}/{filename}

## Automatic Verification

After saving the report and confirming the save to the user, invoke the false-positive verifier:

1. Use the Skill tool to invoke `review:verify-findings` with the saved report path as the argument
2. The verifier runs in an isolated forked context and produces a `.verified.md` report
3. After verification completes, inform the user of both report locations

If the Skill tool is not available (e.g., running inside a subagent), inform the user:
> Run verification manually: `/review:verify-findings {report-path}`

## Content Guidelines

- Provide specific, actionable feedback with file paths and line numbers
- **Blocker and Improvement findings MUST include before/after code blocks** showing current code and suggested fix
- Explain the underlying engineering principle for each non-Nit suggestion
- Be constructive — assume good intent from the author
- See [WORKFLOW.md](WORKFLOW.md) for detailed review checklists, false positive filtering, and confidence scoring guide

## Resources

- [WORKFLOW.md](WORKFLOW.md) - Detailed review checklists, false positive filtering, diff-context probes, confidence scoring guide
- [EXAMPLES.md](EXAMPLES.md) - Sample code review reports demonstrating the full format
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues with git diff, finding quality, and output
