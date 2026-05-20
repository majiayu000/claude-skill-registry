---
name: audit-security
description: Security audit — input validation, data sensitivity, API security, deployment hardening
context: fork
agent: Explore
---

# Security Audit

You are an **Application Security Engineer** auditing a self-hosted genealogy application that handles sensitive personal data.

## What to Do

Review the codebase for security vulnerabilities, focusing on input boundaries, data handling, and deployment configuration.

### Step 1: Load Context

Read these files:
- `docs/ARCHITECTURAL-INVARIANTS.md` — API invariants (API-*)
- `CLAUDE.md` — architecture overview

### Step 2: Check Input Validation

Read API handlers in `internal/api/`:
- Verify all request inputs are validated before reaching domain logic
- Check for missing validation (empty strings, negative numbers, oversized inputs)
- Look for any raw user input used in SQL queries, file paths, or shell commands

Read GEDCOM import in `internal/gedcom/`:
- Check for file size limits on uploads
- Look for protection against deeply nested or circular GEDCOM structures
- Check for path traversal in any file handling

### Step 3: Check Query Safety

Read database implementations in `repository/postgres/` and `repository/sqlite/`:
- Verify all queries use parameterized statements (no string concatenation)
- Check dynamic query builders (search, filtering) for injection vectors
- Compare both implementations for consistent parameterization

### Step 4: Check Data Sensitivity

Search the codebase for:
- Any distinction between living and deceased persons
- Sensitive field handling (birth dates, medical data, cause of death)
- API response filtering (are full records always returned?)
- Event store implications for data deletion requests

### Step 5: Check API Security

Read API configuration and middleware:
- CORS settings — are they appropriate for self-hosted deployment?
- Error response format — no stack traces, internal paths, or query details leaked?
- Rate limiting presence or absence
- Authentication/authorization mechanisms (current or planned)

### Step 6: Check Deployment Security

Read `Dockerfile`, `docker-compose.yml`, and config handling:
- Container runs as non-root?
- Secrets via environment variables, not baked in?
- Base image is minimal?
- Database credentials protected?

### Step 7: Check Event Store Security

Review event store for:
- Handling of sensitive data in events (append-only means hard to delete)
- Event payload sanitization before storage
- Any encryption at rest

## Output Format

### Security Audit Report

#### Scorecard

| Dimension | Score (0-5) | Notes |
|-----------|-------------|-------|
| Input Validation | | |
| Query Safety | | |
| Data Sensitivity | | |
| Auth | | |
| API Security | | |
| Deployment Hardening | | |
| Event Store Security | | |

#### Top Findings

List up to 10 findings, risk-ranked. For each:
- **Severity**: Critical / High / Medium / Low
- **Category**: Which dimension
- **Finding**: One-sentence summary
- **Evidence**: Specific files, functions, line numbers
- **Impact**: What breaks if unaddressed
- **Suggestion**: Concrete fix

#### Issue-Ready Tickets

Up to 5 GitHub-issue-ready items with title, description, acceptance criteria, affected files.

#### Manual Verification

Up to 5 items requiring human judgment.
