---
name: implementation-review
description: Verify implemented code matches design and implementation documentation. Detects spec deviations, missing implementations, doc inconsistencies, and outdated docs. Use after implementing tasks or mid-way through a feature to ensure code and docs are in sync.
---

# Implementation Review

## Overview

Systematically compare implemented code against a feature's `design.md`, `implementation.md`, and `tasks.md` in `/docs/wip/[feature]/`. Works both mid-implementation (reviewing completed tasks only) and post-implementation (full feature review).

Findings go in **both directions** — code that deviates from spec AND spec that is wrong or outdated given the code.

## Finding Types

Each finding is classified by type (what kind of mismatch) and severity (how urgent).

| Type | Code | Description | Example |
|------|------|-------------|---------|
| Missing Implementation | `MISSING_IMPL` | Spec describes something that was not implemented | Design says "rate limiting on /api/auth" but no rate limiter exists |
| Extra Implementation | `EXTRA_IMPL` | Code implements something not in the spec | A caching layer was added that design docs don't mention |
| Spec Deviation | `SPEC_DEV` | Code implements the feature but differently than specified | Design says "bcrypt cost 12" but code uses cost 10 |
| Doc Inconsistency | `DOC_INCON` | Documentation contradicts itself or is internally inconsistent | design.md says JWT tokens, implementation.md says session cookies |
| Outdated Doc | `OUTDATED_DOC` | Code is correct but docs haven't been updated to reflect reality | Endpoint was renamed during implementation but docs still reference old name |
| Ambiguous Spec | `AMBIGUOUS` | Spec is unclear enough that multiple interpretations are valid | "Support pagination" without specifying cursor vs offset |

## Severity Levels

Same P0–P3 scale as `solid-code-review`, adapted for spec conformance:

| Level | Name | Description | Action |
|-------|------|-------------|--------|
| **P0** | Critical | Missing core functionality, security spec violated, data model mismatch | Must fix before merge |
| **P1** | High | Significant behavioral deviation from spec, missing error handling that spec requires | Should fix before merge |
| **P2** | Medium | Minor deviation, doc inconsistency, partial implementation of a spec requirement | Fix or create follow-up |
| **P3** | Low | Naming mismatch, doc typo, cosmetic deviation from spec | Optional |

## Confidence Levels

Each finding gets a confidence score (1–10) with **mandatory reasoning** explaining what was checked, what evidence supports the finding, and what uncertainty remains.

| Score | Meaning |
|-------|---------|
| 9–10 | Certain — direct, unambiguous contradiction between spec and code |
| 7–8 | Strong — clear evidence but minor room for interpretation |
| 5–6 | Moderate — likely issue but spec is somewhat vague or code has plausible alternative reading |
| 3–4 | Uncertain — possible issue, needs human judgment |
| 1–2 | Speculative — gut feeling, very ambiguous spec or indirect evidence |

## Workflow

See [review-process.md](./review-process.md) for the detailed step-by-step process.

**Phases:**

1. Load feature documents
2. Determine review scope (mid-implementation vs post-implementation)
3. Per-task verification against spec
4. Cross-cutting concern check
5. Self-check and confidence assessment
6. Present findings

## Invocation

Use the `/implementation-review [feature-name]` command, or invoke naturally when a user asks to verify implementation against docs.
