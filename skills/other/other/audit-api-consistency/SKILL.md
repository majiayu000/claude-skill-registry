---
name: audit-api-consistency
description: Audit existing API endpoints for consistency when the user asks to check API quality, review API patterns, audit endpoints, or find API inconsistencies
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[optional: specific area or endpoint pattern to audit]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: audit, api, consistency
---

# Audit API Consistency

## Overview

Scan the codebase for API route definitions and analyze them for consistency across naming, HTTP method usage, error response shapes, pagination, auth patterns, and versioning. Produce a structured report with severity-rated findings and concrete fix recommendations. This is an audit skill -- it analyzes what exists, it does not create new APIs.

## Workflow

1. **Read project context** -- Read `.chalk/docs/engineering/` for:
   - Existing API design documents that define the intended conventions
   - Architecture docs describing the API layer
   - Any API style guides or conventions documents
   - Prior audit reports to check if previously flagged issues were resolved

2. **Discover route definitions** -- Scan the codebase to find all API endpoints:
   - Use Grep to search for route registration patterns:
     - Express/Koa: `router.get`, `router.post`, `app.use`, etc.
     - Django: `path(`, `url(`, `@api_view`
     - Spring: `@GetMapping`, `@PostMapping`, `@RequestMapping`
     - FastAPI: `@app.get`, `@router.post`
     - Rails: `resources :`, `get '`, `post '`
     - Next.js: files in `app/api/` or `pages/api/`
   - Build a complete inventory of endpoints with: method, path, handler file, and handler function

3. **Analyze each consistency category** -- For each category below, compare every endpoint against the dominant pattern. The dominant pattern is the convention used by the majority of endpoints.

4. **Classify findings by severity** -- Each inconsistency gets one of:
   - **Critical**: Will cause client errors or security issues (e.g., missing auth on a protected endpoint)
   - **High**: Breaks client assumptions or developer experience (e.g., different error shapes)
   - **Medium**: Inconsistency that causes confusion but no runtime issues (e.g., mixed naming conventions)
   - **Low**: Minor deviation that could be addressed opportunistically (e.g., inconsistent sort defaults)

5. **Generate fix recommendations** -- For each finding, provide:
   - The current state (what is inconsistent)
   - The expected state (what it should be, based on dominant pattern)
   - A concrete code change or migration path
   - Whether it is a breaking change for existing clients

6. **Output the report** -- Present the report in conversation or write to `.chalk/docs/engineering/<n>_api_audit.md` if the user requests a persisted report.

7. **Summarize** -- Provide an executive summary with total findings by severity, the most impactful issues, and a recommended prioritization for fixes.

## Consistency Categories

### 1. URL Naming Patterns

Check for:
- **Plural vs. singular nouns**: `/users` vs. `/user` (pick one, apply everywhere)
- **Casing consistency**: `/user-profiles` vs. `/userProfiles` vs. `/user_profiles`
- **Nesting depth**: Are some resources nested 3+ levels while others are flat?
- **Verb usage**: `/api/getUsers` (RPC-style) mixed with `/api/users` (REST-style)
- **ID format in paths**: `:id` vs. `:userId` vs. `{id}` -- consistent parameter naming
- **Trailing slashes**: Some paths with `/`, some without

### 2. HTTP Method Usage

Check for:
- **GET with side effects**: GET endpoints that modify data (should be POST/PATCH/DELETE)
- **POST for retrieval**: POST used to fetch data that should be a GET with query params
- **PUT vs. PATCH confusion**: PUT used for partial updates (should be PATCH) or PATCH used for full replacement (should be PUT)
- **DELETE semantics**: Some DELETEs return the deleted resource, others return 204 No Content -- pick one
- **Correct status codes**: POST returning 200 instead of 201, DELETE returning 200 instead of 204

### 3. Error Response Format

Check for:
- **Shape consistency**: Do all endpoints return errors in the same JSON structure?
- **Error code presence**: Do all errors include a machine-readable error code?
- **Validation error format**: Are field-level validation errors structured consistently?
- **HTTP status code accuracy**: 400 vs. 422 for validation, 401 vs. 403 for auth
- **Error middleware**: Is error formatting centralized or scattered across handlers?
- **Stack traces in production**: Are internal details leaked in error responses?

### 4. Pagination Approach

Check for:
- **Pagination presence**: Are all list endpoints paginated? Flag any that return unbounded results
- **Pagination style**: Cursor vs. offset -- is it consistent across all list endpoints?
- **Parameter naming**: `page`/`limit` vs. `offset`/`count` vs. `cursor`/`size`
- **Default values**: Are default page sizes consistent?
- **Maximum limits**: Do all paginated endpoints enforce a maximum page size?
- **Response meta shape**: Is pagination metadata structured the same way everywhere?

### 5. Authentication and Authorization

Check for:
- **Auth middleware coverage**: Are all non-public endpoints protected by auth middleware?
- **Auth header format**: Consistent use of `Authorization: Bearer <token>` or API key headers
- **Missing auth on sensitive endpoints**: POST/PUT/PATCH/DELETE without auth checks
- **Role/scope checking**: Is authorization granularity consistent?
- **Public endpoint documentation**: Are intentionally public endpoints clearly marked?

### 6. Versioning

Check for:
- **Version presence**: Is API versioning used at all? If so, is it consistent?
- **Version format**: URL-based (`/api/v1/`) vs. header-based (`Accept: application/vnd.api.v1+json`)
- **Unversioned endpoints**: Endpoints that bypass the versioning scheme
- **Deprecated versions**: Are old versions still active without deprecation headers?

### 7. Response Envelope

Check for:
- **Wrapper consistency**: Do all endpoints use the same response wrapper (`{ data }`, `{ data, meta }`, or raw)?
- **Single vs. collection distinction**: Single resources returning arrays or collections returning unwrapped objects
- **Null handling**: `null` vs. absent key vs. empty string for missing optional fields
- **Timestamp format**: ISO 8601 everywhere or mixed formats?

## Report Format

```markdown
# API Consistency Audit Report

Date: <YYYY-MM-DD>
Scope: <All endpoints | Specific area>
Total endpoints scanned: <count>

## Executive Summary

<2-3 sentences. Overall consistency score, most impactful issues, recommended priority.>

### Findings by Severity

| Severity | Count |
|----------|-------|
| Critical | <n> |
| High | <n> |
| Medium | <n> |
| Low | <n> |

## Dominant Patterns (Established Conventions)

<Document the patterns used by the majority of endpoints. These are the "correct" baseline.>

| Category | Dominant Pattern | Adoption Rate |
|----------|-----------------|---------------|
| URL casing | kebab-case | 85% (34/40) |
| Pluralization | Plural nouns | 90% (36/40) |
| Error shape | `{ error: { code, message, status, details } }` | 75% (30/40) |
| Pagination | Offset with `page`/`limit` | 100% (8/8 list endpoints) |
| Auth | Bearer token via middleware | 92% (37/40) |

## Findings

### Critical

**[C-1]** Missing auth on `POST /api/v1/admin/settings`
- **File**: `src/routes/admin.ts:45`
- **Issue**: Endpoint modifies system settings but has no auth middleware
- **Expected**: Auth middleware with `admin` role check
- **Fix**: Add `requireAuth('admin')` middleware
- **Breaking**: No

### High

**[H-1]** Inconsistent error shape in billing endpoints
- **File**: `src/routes/billing.ts`
- **Issue**: Returns `{ "message": "error" }` instead of standard `{ "error": { "code": "...", "message": "..." } }`
- **Expected**: Use shared error middleware
- **Fix**: Replace manual error returns with `throw new AppError('BILLING_ERROR', message)`
- **Breaking**: Yes -- clients parsing billing errors will need to update

### Medium

...

### Low

...

## Migration Recommendations

### Priority 1: Critical and High (do now)

<Ordered list of fixes with estimated effort>

### Priority 2: Medium (next sprint)

<Ordered list>

### Priority 3: Low (opportunistic)

<Fixes to apply when touching these files for other reasons>

## Legacy Endpoints

<List endpoints that are intentionally inconsistent due to backwards compatibility. Document why they are exempt and whether a migration is planned.>
```

## Scanning Strategy

When scanning a large codebase, follow this order for efficiency:

1. **Find the router/route files first** -- Grep for the framework's routing pattern to locate all route files
2. **Extract the endpoint inventory** -- Build the full list before analyzing
3. **Check error middleware/handler** -- Find the centralized error handling to understand the intended pattern
4. **Spot-check endpoints** -- Read 3-5 endpoint handlers in full to understand the actual implementation pattern
5. **Compare outliers** -- Focus analysis time on endpoints that deviate from the dominant pattern

## Anti-patterns

- **Only checking names, not behavior** -- URL naming is the easiest thing to audit but the least impactful. Inconsistent error shapes and missing auth are far more dangerous. Always audit behavior (error handling, auth, pagination) before cosmetic naming.
- **Ignoring legacy endpoints** -- Old endpoints that predate current conventions should still be cataloged. Document them as "legacy, migration planned" or "legacy, exempt" -- but do not pretend they do not exist.
- **Not suggesting a migration path** -- Flagging inconsistencies without explaining how to fix them is not useful. Every finding must include a concrete fix and whether it is a breaking change.
- **Auditing against an ideal, not the project's own conventions** -- The correct convention is whatever the majority of the codebase uses, not what a blog post says. If the project uses `snake_case` URLs, do not flag them as wrong because REST guides prefer `kebab-case`.
- **Missing auth gaps** -- The single most valuable finding in an API audit is an endpoint that should require auth but does not. Always prioritize auth coverage analysis.
- **One-time audit with no follow-up** -- An audit is only valuable if issues get fixed. Include a prioritized action plan and suggest re-running the audit after fixes are applied.
