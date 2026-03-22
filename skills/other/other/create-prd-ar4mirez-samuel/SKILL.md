---
name: create-prd
description: |
  Product Requirements Document (PRD) creation workflow. Use when defining implementation
  requirements for complex features, new subsystems, or any task affecting more than 10 files.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Product Requirements Document (PRD) Creation

Structured approach to defining complex features before implementation.

**Use When**: COMPLEX mode triggered (affects >10 files, new subsystem, unclear scope)
**4D Phase**: Deconstruct → Diagnose (planning stage)

---

## Goal

Guide AI in creating a detailed Product Requirements Document (PRD) in Markdown format based on user's feature request. The PRD should be clear, actionable, and suitable for junior developers to understand and implement.

## When to Use This Workflow

✅ **Use PRD workflow when:**
- Feature affects >10 files
- Building new subsystem or major component
- Requirements are unclear or ambiguous
- Multiple stakeholders need alignment
- Feature will take >1 week to implement
- Breaking changes to existing architecture

❌ **Skip PRD for:**
- Atomic tasks (single file changes)
- Bug fixes with clear scope
- Small features affecting <5 files
- Refactoring with defined boundaries

## Process

### Step 1: Receive Initial Request
User provides brief description or request for new feature.

**Example**:
```
"Build user authentication with email/password and OAuth"
```

### Step 2: Check Project Context
Before asking questions, AI should:

1. Read `CLAUDE.md` (if exists) for:
   - Tech stack and framework choices
   - Existing architecture patterns
   - Authentication/authorization approach

2. Scan codebase for:
   - Existing auth-related code
   - Database schemas (user tables)
   - API patterns and conventions

3. Review relevant guardrails from CLAUDE.md:
   - Security requirements (input validation, parameterized queries)
   - Testing coverage targets
   - File length limits
   - Performance requirements

### Step 3: Ask Clarifying Questions

**IMPORTANT**: Ask clarifying questions to gather detail. Focus on "what" and "why", not "how" (developer figures that out).

**Provide numbered/lettered options for easy user responses.**

#### Template Questions (adapt based on feature):

**1. Problem/Goal**
- "What problem does this feature solve for users?"
- "What is the main goal we want to achieve?"

**2. Target Users**
- "Who is the primary user of this feature?"
- Which user types: a) End users, b) Admins, c) Both, d) Other

**3. Core Functionality**
- "What are the key actions users should be able to perform?"
- Must-haves vs. nice-to-haves?

**4. User Stories**
- "Can you provide 2-3 user stories?"
- Format: "As a [user type], I want to [action] so that [benefit]"

**5. Acceptance Criteria**
- "How will we know this feature is successfully implemented?"
- "What are the key success criteria?"

**6. Scope/Boundaries**
- "What should this feature NOT do (non-goals)?"
- "Any features we should defer to future versions?"

**7. Data Requirements**
- "What data does this feature need to display or manipulate?"
- "Any data privacy/security considerations?"

**8. UI/UX Expectations**
- "Are there design mockups or UI guidelines to follow?"
- "Describe the desired look and feel"
- Options: a) Use existing design system, b) Create new design, c) Minimal/functional only

**9. Integration Points**
- "Does this integrate with existing features/systems?"
- "Any third-party services involved?"

**10. Edge Cases & Errors**
- "Any potential edge cases or error conditions to consider?"
- "How should errors be handled and communicated?"

**11. Performance & Scale**
- "Expected number of users/requests?"
- "Any specific performance requirements?"

**12. Security Requirements**
- "Any sensitive data involved?"
- "Authentication/authorization needed?"
- "Compliance requirements (GDPR, HIPAA, etc.)?"

### Step 4: Generate PRD

Based on initial request and clarifying question answers, generate PRD using structure below.

**Target audience**: Junior developer (clear, explicit, no jargon)

### Step 5: Validate Against Guardrails

Before presenting PRD, check:
- [ ] Requirements align with security guardrails (input validation, parameterized queries)
- [ ] Testing approach defined (coverage targets clear)
- [ ] Performance requirements specified
- [ ] File organization won't violate length limits (suggest component breakdown if needed)
- [ ] API design follows RESTful/GraphQL conventions

### Step 6: Save PRD

Save as: `.claude/tasks/[NNNN]-prd-[feature-name].md`

**Numbering**: Zero-padded 4-digit sequence (0001, 0002, etc.)

**Examples**:
- `.claude/tasks/0001-prd-user-authentication.md`
- `.claude/tasks/0002-prd-dashboard-analytics.md`

### Step 7: Next Steps

After saving PRD:
1. Inform user: "PRD created at `.claude/tasks/NNNN-prd-feature-name.md`"
2. Ask: "Ready to generate task list? Use `@.claude/skills/generate-tasks/SKILL.md` with this PRD."
3. **DO NOT START IMPLEMENTING** (wait for task breakdown)

---

## PRD Structure

The generated PRD must include these sections:

### 1. Introduction/Overview
- Briefly describe the feature
- State the problem it solves
- State the primary goal

**Example**:
```markdown
## Introduction

This feature adds user authentication to the platform, allowing users to create accounts, log in securely, and access personalized content. Currently, the application has no user identity management, limiting personalization and security.

**Goal**: Enable secure user authentication with email/password and social OAuth providers.
```

### 2. Goals
List specific, measurable objectives for this feature.

**Format**: Numbered list, actionable, measurable

**Example**:
```markdown
## Goals

1. Allow users to create accounts with email and password
2. Enable login via Google and GitHub OAuth
3. Implement secure session management with JWT
4. Achieve <200ms authentication response time
5. Support password reset flow
6. Maintain >95% test coverage for auth logic
```

### 3. User Stories
Detail user narratives describing feature usage and benefits.

**Format**: "As a [user type], I want to [action] so that [benefit]"

**Example**:
```markdown
## User Stories

**US-001**: As a new user, I want to create an account with my email and password so that I can access personalized features.

**US-002**: As a returning user, I want to log in quickly with my Google account so that I don't have to remember another password.

**US-003**: As a user who forgot their password, I want to reset it via email so that I can regain access to my account.

**US-004**: As an admin, I want to view user authentication logs so that I can monitor security events.
```

### 4. Functional Requirements
List specific functionalities the feature must have.

**Format**: Numbered, clear, concise (e.g., "The system must allow X")

**Example**:
```markdown
## Functional Requirements

### Authentication
FR-001: The system must allow users to register with email and password
FR-002: The system must validate email format and password strength (min 8 chars, 1 number, 1 special char)
FR-003: The system must support OAuth login via Google and GitHub
FR-004: The system must generate and validate JWT tokens for session management
FR-005: The system must implement token refresh mechanism (1h expiration, 7d refresh)

### Password Management
FR-006: The system must hash passwords using bcrypt (cost factor: 12)
FR-007: The system must provide password reset via email link (1h expiration)
FR-008: The system must prevent password reuse (last 3 passwords)

### Security
FR-009: The system must implement rate limiting (5 failed attempts = 15min lockout)
FR-010: The system must validate all inputs against XSS and SQL injection
FR-011: The system must log all authentication events (success, failure, logout)
```

### 5. Non-Goals (Out of Scope)
Clearly state what this feature will NOT include to manage scope.

**Example**:
```markdown
## Non-Goals

- ❌ Two-factor authentication (2FA) - Deferred to v2
- ❌ Single Sign-On (SSO) integration - Future enhancement
- ❌ Biometric authentication - Not in scope
- ❌ Account deletion workflow - Separate feature
- ❌ Social media posting permissions - OAuth login only
```

### 6. Technical Considerations
Mention technical constraints, dependencies, or implementation suggestions.

**Check `CLAUDE.md` for existing tech stack before suggesting**

**Example**:
```markdown
## Technical Considerations

### Tech Stack Integration
- Backend: Use existing Express.js framework
- Database: Add `users` and `sessions` tables to PostgreSQL
- ORM: Use Prisma (already in project)
- Validation: Use Zod for input validation (project standard)

### Architecture
- Follow repository pattern (existing project convention)
- Create `/api/auth` route group
- Implement middleware for JWT validation
- Use existing error handling patterns

### Dependencies
- New: `bcrypt`, `jsonwebtoken`, `passport`, `passport-google-oauth20`, `passport-github2`
- Check: All dependencies for known vulnerabilities before adding

### File Organization (respecting guardrails)
- `src/auth/` - Main auth module (<300 lines per file)
  - `auth.controller.ts` - Route handlers
  - `auth.service.ts` - Business logic
  - `auth.middleware.ts` - JWT validation
  - `auth.types.ts` - TypeScript types
- `src/db/schemas/` - Database schemas
  - `user.schema.ts`
  - `session.schema.ts`
- Tests alongside each file
```

### 7. Design Considerations
Link to mockups, describe UI/UX requirements, or mention components/styles.

**Example**:
```markdown
## Design Considerations

### UI Components
- Use existing `<Form>`, `<Input>`, `<Button>` components from design system
- Create new `<AuthLayout>` component for login/register pages
- Follow existing color scheme and spacing guidelines

### User Flow
1. Landing → Click "Sign Up"
2. Registration form (email, password, confirm password)
3. Email verification sent
4. Verify email → Redirect to dashboard
5. OR: Click "Continue with Google" → OAuth flow → Dashboard

### Error Handling
- Show validation errors inline below each field
- Display auth errors in toast notifications (existing pattern)
- Provide clear, actionable error messages

### Accessibility
- All forms keyboard navigable
- Proper ARIA labels
- Focus management on error states
```

### 8. Guardrails Affected
Identify which CLAUDE.md guardrails are critical for this feature.

**Example**:
```markdown
## Guardrails Affected

### Security (CRITICAL)
- ✓ All user inputs validated before processing
- ✓ All API boundaries have input validation (Zod schemas)
- ✓ All database queries parameterized (use Prisma)
- ✓ All environment variables have secure defaults (JWT_SECRET, OAuth keys)
- ✓ All file operations validate paths (password reset token validation)
- ✓ Dependencies checked for vulnerabilities

### Testing (CRITICAL)
- ✓ Coverage targets: >95% for auth logic (business-critical)
- ✓ All public APIs have unit tests
- ✓ All bug fixes include regression tests
- ✓ Edge cases tested (null, empty, invalid tokens, expired sessions)

### Code Quality
- ✓ No file exceeds 300 lines (split auth.service.ts if needed)
- ✓ Cyclomatic complexity ≤ 10 per function
- ✓ All exported functions have type signatures and JSDoc

### Performance
- ✓ API responses < 200ms for login/register
- ✓ No N+1 queries (eager load user data with sessions)
```

### 9. Success Metrics
How will success be measured?

**Example**:
```markdown
## Success Metrics

### Technical Metrics
- Authentication response time < 200ms (p95)
- Test coverage >95% for auth module
- Zero critical security vulnerabilities
- <1% authentication failure rate (excluding incorrect credentials)

### Business Metrics
- 80% of users complete registration flow
- 50% of users choose OAuth over email/password
- <5% password reset requests (indicates good UX)

### Security Metrics
- Zero successful brute force attacks
- 100% of authentication events logged
- Password reset links expire correctly (100% success rate)
```

### 10. Implementation Estimate
Rough complexity estimate (tokens, not time)

**Example**:
```markdown
## Implementation Estimate

### Complexity Analysis
- **Backend Auth Logic**: ~15,000 tokens (COMPLEX)
- **OAuth Integration**: ~10,000 tokens (FEATURE)
- **UI Components**: ~8,000 tokens (FEATURE)
- **Tests**: ~12,000 tokens (FEATURE)
- **Documentation**: ~3,000 tokens (ATOMIC)

**Total**: ~48,000 tokens (COMPLEX mode justified)

### Recommended Approach
1. Use COMPLEX mode with full task breakdown
2. Implement in phases (email auth → OAuth → password reset)
3. Each phase with its own task list
4. Frequent checkpoints after each subtask
```

### 11. Open Questions
List remaining questions or areas needing clarification.

**Example**:
```markdown
## Open Questions

1. **Email Service**: Which provider? (SendGrid, AWS SES, Mailgun)
2. **Session Storage**: Redis for sessions or JWT-only?
3. **User Roles**: Do we need RBAC (roles/permissions) in this version?
4. **Profile Data**: What user profile fields beyond email/name?
5. **Existing Users**: Migration strategy for existing data (if any)?

**Action**: Clarify these before generating task list.
```

---

## Output Format

**File**: `.claude/tasks/NNNN-prd-feature-name.md`
**Format**: Markdown
**Audience**: Junior developer + AI assistant

---

## Final Instructions

### For AI Assistant:

1. ✅ **DO ask clarifying questions** (don't assume requirements)
2. ✅ **DO provide numbered options** (easy user response)
3. ✅ **DO reference `CLAUDE.md`** (maintain consistency)
4. ✅ **DO validate against CLAUDE.md guardrails**
5. ✅ **DO specify which guardrails are critical**
6. ✅ **DO estimate complexity in tokens**
7. ❌ **DO NOT start implementing** (wait for task generation)
8. ❌ **DO NOT suggest violating guardrails** (propose alternatives instead)

### After PRD Created:

1. Save to `.claude/tasks/NNNN-prd-feature-name.md`
2. Inform user of file location
3. Suggest next step: "Ready to generate tasks? Use `@.claude/skills/generate-tasks/SKILL.md` with this PRD."
4. Wait for user confirmation before proceeding

---

**Remember**: A good PRD prevents scope creep, aligns stakeholders, and makes implementation straightforward. Invest time here to save time later.
