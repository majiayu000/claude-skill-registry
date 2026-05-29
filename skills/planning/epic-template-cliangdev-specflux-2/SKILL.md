---
name: epic-template
description: Epic and task structure patterns for SpecFlux. Use when breaking PRDs into epics and tasks. Epics should be self-contained with clear acceptance criteria.
---

# Epic & Task Templates

When breaking down PRDs into epics and tasks, follow these patterns.

## Design Principles

1. **Self-contained epics** - AI should be able to implement from epic alone
2. **Independent first** - Create non-dependent epics before dependent ones
3. **Testable criteria** - Every acceptance criterion must be verifiable
4. **1-4 hour tasks** - Tasks should be completable in one session

## Epic Structure

### API Format

```json
{
  "title": "User Authentication",
  "description": "## Overview\n...",
  "prdRef": "SPEC-P1",
  "acceptanceCriteria": [
    {"criteria": "Users can self-register with email/password"},
    {"criteria": "Users can log in with existing credentials"},
    {"criteria": "Password reset flow works end-to-end"}
  ]
}
```

**CRITICAL**: `acceptanceCriteria` must be `[{"criteria": "..."}, ...]` NOT `["...", ...]`

### Description Template (Agent-Optimized)

Use structured format for efficient agent consumption. Every word costs context window tokens.

```markdown
## Context
- Tech stack: {relevant technologies}
- Database: {relevant tables/schemas with file:line refs}
- Related code: {directory or file paths}

## Scope
- {What's included - bullet points}
- {Another inclusion}

## NOT in scope
- {Explicit exclusion to prevent scope creep}
- {Another exclusion}
```

**Format Principles:**

| Principle | Rationale |
|-----------|-----------|
| Bullet points over paragraphs | Faster to parse, less ambiguity |
| File:line references | Agent can jump directly to code (e.g., `src/auth/User.java:42`) |
| Explicit NOT in scope | Prevents scope creep, saves iterations |
| No redundant context | PRD is linked, don't repeat it |

**Validation:** If description exceeds 500 characters without structured sections, it's likely too verbose.

### Acceptance Criteria Guidelines

**Good criteria (outcome-focused):**
- "Users can complete registration in under 60 seconds"
- "Users can recover access without support intervention"
- "Profile changes persist across sessions"

**Bad criteria (too implementation-focused):**
- "API returns 200 status code" → belongs in task
- "Use bcrypt for password hashing" → belongs in task
- "Add button to header" → too vague

### Epic Dependencies

Order epics by dependencies:

```
E1: User Authentication (independent - foundation)
    ↓
E2: User Profile (depends on E1 - needs auth)
    ↓
E3: Team Management (depends on E1, E2)
```

Create independent epics FIRST, then dependent ones.

## Task Structure

### API Format

```json
{
  "epicRef": "SPEC-E1",
  "title": "Create user database schema",
  "description": "## Objective\n...",
  "priority": "HIGH"
}
```

### Description Template (Agent-Optimized)

Use structured format for agent efficiency. Include specific file paths.

```markdown
## Files
- Modify: {existing file paths}
- Create: {new file paths}
- Reference: {files to read for context}

## Implementation
- {Step 1}
- {Step 2}
```

**Example:**
```markdown
## Files
- Modify: src/controllers/AuthController.java:85
- Modify: src/services/AuthService.java
- Create: src/dto/LoginRequest.java
- Reference: src/config/SecurityConfig.java

## Implementation
- Add POST /auth/login endpoint
- Validate email/password format
- Return JWT on success, 401 on failure
```

**File Reference Conventions:**
- Use `file:line` for specific locations (e.g., `AuthController.java:85`)
- Use `file` for general references (e.g., `AuthService.java`)
- Use directories for broader scope (e.g., `src/auth/`)

### Acceptance Criteria for Tasks

Each criterion should be testable. Tag with test type:

```
[Unit] hashPassword returns bcrypt hash with cost 12
[Integration] POST /auth/register returns 201 for valid input
[Integration] POST /auth/register returns 409 for duplicate email
[E2E] User completes registration and sees dashboard
```

### Task Size Guidelines

| Size | Duration | Scope |
|------|----------|-------|
| Small | 1-2 hours | Single file, clear change |
| Medium | 2-4 hours | Multiple files, one feature |
| Too Large | 4+ hours | Should be split |

If a task takes more than 4 hours, it should be broken down further.

### Task Dependencies

```json
{
  "dependsOnTaskRef": "SPEC-41"
}
```

Create tasks in dependency order:
1. Database schema (no dependencies)
2. Repository layer (depends on schema)
3. Service layer (depends on repository)
4. API endpoints (depends on service)
5. UI components (depends on API)

## Example Breakdown

### PRD Feature
> "Users can register and log in with email/password"

### Epic: User Authentication

```markdown
## Overview
Secure user authentication system. Users register with email/password,
log in to access the platform, and can reset forgotten passwords.

## Scope
**IN:** Email/password registration, login, password reset, JWT sessions
**OUT:** Social login, 2FA, session management UI

## Technical Approach
- bcrypt (cost 12) for password hashing
- JWT tokens (24h expiry)
- httpOnly cookies for token storage
- Rate limiting on auth endpoints

## Reference Documents
- `.specflux/prds/user-management/prd.md` - Requirements
- `.specflux/prds/user-management/user-flows.md` - Auth flows

## Edge Cases
- Duplicate email registration → 409 Conflict
- Invalid credentials → 401 + generic message (no email enumeration)
- Expired reset token → redirect to request new token
```

### Tasks

**Task 1: User database schema**
```
Objective: Create users and password_reset_tokens tables

Files:
- migrations/001_create_users.sql
- migrations/002_create_password_reset_tokens.sql

Acceptance Criteria:
[Unit] users table has id, email, password_hash, created_at, updated_at
[Unit] email column has unique constraint
[Unit] password_reset_tokens has user_id FK, token, expires_at
[Unit] Migration rollback removes tables
```

**Task 2: User repository**
```
Objective: CRUD operations for users table

Files:
- src/repositories/UserRepository.kt
- src/test/repositories/UserRepositoryTest.kt

Acceptance Criteria:
[Unit] create() inserts user and returns with generated ID
[Unit] findByEmail() returns user or null
[Unit] findById() returns user or null
[Unit] updatePassword() updates password_hash
```

**Task 3: Registration endpoint**
```
Objective: POST /api/auth/register

Files:
- src/routes/auth/RegisterRoute.kt
- src/test/routes/auth/RegisterRouteTest.kt

Acceptance Criteria:
[Integration] Returns 201 with user object for valid input
[Integration] Returns 400 for invalid email format
[Integration] Returns 400 for password under 8 characters
[Integration] Returns 409 for duplicate email
[Unit] Password is hashed with bcrypt cost 12
```

## Coverage Verification

Before finishing breakdown, verify 100% PRD coverage:

```markdown
## Coverage Report

| PRD Requirement | Epic | Tasks |
|-----------------|------|-------|
| User registration | E1 | T1, T2, T3 |
| User login | E1 | T4, T5 |
| Password reset | E1 | T6, T7, T8 |
| Profile management | E2 | T9, T10, T11 |

✓ All requirements covered
```

## Quick Reference

### Epic Statuses
- `PLANNING` - Being defined
- `IN_PROGRESS` - Implementation started
- `BLOCKED` - Waiting on dependency
- `COMPLETED` - All tasks done
- `CANCELLED` - Abandoned

### Task Statuses
- `BACKLOG` - Not started
- `READY` - Dependencies met, ready to start
- `IN_PROGRESS` - Being worked on
- `IN_REVIEW` - Awaiting review
- `BLOCKED` - Stuck on something
- `COMPLETED` - Done and verified
- `CANCELLED` - Abandoned

### Task Priorities
- `CRITICAL` - Blocks everything
- `HIGH` - Important for epic completion
- `MEDIUM` - Normal priority
- `LOW` - Nice to have
