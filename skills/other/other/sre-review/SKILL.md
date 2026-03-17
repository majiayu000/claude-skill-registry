---
name: sre-review
version: 1.0.0
description: '[Code Quality] Production readiness review for service-layer and API changes'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

> **Critical Purpose:** Ensure quality — no flaws, no bugs, no missing updates, no stale content. Verify both code AND documentation.

## Quick Summary

**Goal:** Assess production readiness of service-layer and API changes by scoring observability, reliability, and operational preparedness.

**When to use:** After implementing backend service or API changes, before committing.

**Scope:** Service-layer and API changes only — frontend-only changes exempt.

**Why this exists:** Code that works but can't be debugged, monitored, or rolled back is technical debt in disguise.

## Your Mission

<task>
$ARGUMENTS
</task>

## Review Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking. Every claim needs traced proof.**

- Do NOT accept operational readiness at face value — verify by reading actual implementations
- Every score must include `file:line` evidence (grep results, read confirmations)
- If you cannot prove a score with a code trace, score it 0
- Question assumptions: "Is this really handled?" → trace the error/retry/timeout path to confirm
- Challenge completeness: "Are all failure modes covered?" → check what happens when dependencies fail
- Verify observability: "Can we actually debug this in production?" → check logging, correlation, metrics
- No "looks fine" without proof — state what you verified and how

## Scope Resolution

1. If arguments specify files/directories → review those
2. Else review uncommitted changes (`git diff --name-only`)
3. Focus on: `*.cs` files in `src/Services/`, API controllers, service classes
4. Skip: frontend files, test files, documentation, configuration-only changes

## Production Readiness Checklist

Review the changed files and score each criterion 0-2:

- **0** = Not addressed
- **1** = Partially addressed
- **2** = Fully addressed

### Observability (max 8 points)

| #   | Criterion              | What to Check                                                                                                 |
| --- | ---------------------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | **Structured Logging** | External API calls and critical operations log errors with context (request ID, user, parameters)             |
| 2   | **Error Context**      | Exceptions include enough context to diagnose without reproducing (entity IDs, operation type, input summary) |
| 3   | **Metrics Awareness**  | Operations >100ms consider tracking duration. New endpoints consider latency monitoring                       |
| 4   | **Correlation**        | Cross-service calls include or propagate correlation IDs for distributed tracing                              |

### Reliability (max 8 points)

| #   | Criterion                 | What to Check                                                                                                 |
| --- | ------------------------- | ------------------------------------------------------------------------------------------------------------- |
| 5   | **Retry Strategy**        | Transient failures (HTTP, DB timeouts) have retry logic or documented reason for not retrying                 |
| 6   | **Timeout Configuration** | HTTP clients and external calls have explicit timeout (not relying on defaults)                               |
| 7   | **Error Handling**        | Errors handled gracefully — no swallowed exceptions, no generic catch-all without logging                     |
| 8   | **Fallback Behavior**     | Critical paths define what happens when dependencies fail (degraded mode, cached response, user-facing error) |

## Scoring

| Score | Verdict        | Recommendation                                                                            |
| ----- | -------------- | ----------------------------------------------------------------------------------------- |
| 12-16 | **PASS**       | Production-ready. Proceed to commit.                                                      |
| 8-11  | **NEEDS WORK** | Address gaps before deploying to production. OK for dev/staging.                          |
| 0-7   | **NOT READY**  | Significant operational gaps. Review Operational Readiness rules in code-review-rules.md. |

## Output Format

```markdown
## SRE Review Results

**Scope:** {files reviewed}
**Date:** {date}
**Score:** {X}/16
**Verdict:** PASS / NEEDS WORK / NOT READY

### Observability ({X}/8)

| #   | Criterion          | Score | Evidence                   |
| --- | ------------------ | ----- | -------------------------- |
| 1   | Structured Logging | 0/1/2 | {file:line or "not found"} |
| 2   | Error Context      | 0/1/2 | ...                        |
| 3   | Metrics Awareness  | 0/1/2 | ...                        |
| 4   | Correlation        | 0/1/2 | ...                        |

### Reliability ({X}/8)

| #   | Criterion         | Score | Evidence |
| --- | ----------------- | ----- | -------- |
| 5   | Retry Strategy    | 0/1/2 | ...      |
| 6   | Timeout Config    | 0/1/2 | ...      |
| 7   | Error Handling    | 0/1/2 | ...      |
| 8   | Fallback Behavior | 0/1/2 | ...      |

### Gaps to Address

- {specific actionable item}

### Recommendation

{Proceed / Address gaps first}
```

## Important Notes

- Advisory only — provides awareness, does not block commits
- Evidence-based — cite specific file:line for each score
- Proportional — small bug fixes need less rigor than new endpoints
- Check for project framework patterns (background job handlers, base controller error handling)
