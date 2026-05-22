---
name: sentry-fix-issues
description: Find and fix issues from Sentry using MCP. Use when asked to fix Sentry errors, debug production issues, investigate exceptions, or resolve bugs reported in Sentry. Methodically analyzes stack traces, breadcrumbs, traces, and context to identify root causes.
---

# Fix Sentry Issues

Discover, analyze, and fix production issues using Sentry's full debugging capabilities.

## Invoke This Skill When

- User asks to "fix Sentry issues" or "resolve Sentry errors"
- User wants to "debug production bugs" or "investigate exceptions"
- User mentions issue IDs, error messages, or asks about recent failures
- User wants to triage or work through their Sentry backlog

## Prerequisites

- Sentry MCP server configured and connected
- Access to the Sentry project/organization

## Phase 1: Issue Discovery

Use Sentry MCP to find issues. Confirm with user which issue(s) to fix before proceeding.

| Search Type | MCP Call |
|-------------|----------|
| Recent unresolved | `sentry_search_issues` query: `"is:unresolved"` sort: `"date"` |
| Specific error type | `sentry_search_issues` query: `"is:unresolved error.type:TypeError"` |
| By ID | `sentry_get_issue` issue_id: `"PROJECT-123"` |

## Phase 2: Deep Issue Analysis

Gather ALL available context for each issue:

| Data Source | MCP Call | Extract |
|-------------|----------|---------|
| **Core Error** | `sentry_get_issue` | Exception type/message, full stack trace, file paths, line numbers, function names |
| **Event Details** | `sentry_get_event` | Breadcrumbs, tags, custom context, request data |
| **Trace** (if available) | `sentry_get_trace` | Parent transaction, spans, DB queries, API calls, error location |
| **Replay** (if available) | `sentry_get_replay` | User actions, UI state, network requests |

## Phase 3: Root Cause Hypothesis

Before touching code, document:

1. **Error Summary**: One sentence describing what went wrong
2. **Immediate Cause**: The direct code path that threw
3. **Root Cause Hypothesis**: Why the code reached this state
4. **Supporting Evidence**: Breadcrumbs, traces, or context supporting this
5. **Alternative Hypotheses**: What else could explain this? Why is yours more likely?

Challenge yourself: Is this a symptom of a deeper issue? Check for similar errors elsewhere, related issues, or upstream failures in traces.

## Phase 4: Code Investigation

| Step | Actions |
|------|---------|
| **Locate Code** | Read every file in stack trace from top down |
| **Trace Data Flow** | Find value origins, transformations, assumptions, validations |
| **Error Boundaries** | Check for try/catch - why didn't it handle this case? |
| **Related Code** | Find similar patterns, check tests, review recent commits (`git log`, `git blame`) |

## Phase 5: Implement Fix

Before writing code, confirm your fix will:
- [ ] Handle the specific case that caused the error
- [ ] Not break existing functionality
- [ ] Handle edge cases (null, undefined, empty, malformed)
- [ ] Provide meaningful error messages
- [ ] Be consistent with codebase patterns

**Apply the fix:** Prefer input validation > try/catch, graceful degradation > hard failures, specific > generic handling, root cause > symptom fixes.

**Add tests** reproducing exact Sentry event conditions and verifying edge cases.

## Phase 6: Verification Audit

Complete before declaring fixed:

| Check | Questions |
|-------|-----------|
| **Evidence** | Does fix address exact error message? Handle data state shown? Prevent ALL events? |
| **Regression** | Could fix break existing functionality? Other code paths affected? Backward compatible? |
| **Completeness** | Similar patterns elsewhere? Related Sentry issues? Add monitoring/logging? |
| **Self-Challenge** | Root cause or symptom? Considered all event data? Will handle if occurs again? |

## Phase 7: Report Results

Format:
```
## Fixed: [ISSUE_ID] - [Error Type]
- Error: [message], Frequency: [X events, Y users], First/Last: [dates]
- Root Cause: [one paragraph]
- Evidence: Stack trace [key frames], breadcrumbs [actions], context [data]
- Fix: File(s) [paths], Change [description]
- Verification: [ ] Exact condition [ ] Edge cases [ ] No regressions [ ] Tests [y/n]
- Follow-up: [additional issues, monitoring, related code]
```

## Quick Reference

**MCP Tools:** `sentry_search_issues`, `sentry_get_issue`, `sentry_get_event`, `sentry_get_trace`, `sentry_get_replay`, `sentry_list_projects`, `sentry_get_project`

**Common Patterns:** TypeError (check data flow, API responses, race conditions) • Promise Rejection (trace async, error boundaries) • Network Error (breadcrumbs, CORS, timeouts) • ChunkLoadError (deployment, caching, splitting) • Rate Limit (trace patterns, throttling) • Memory/Performance (trace spans, N+1 queries)
