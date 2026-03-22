---
name: research-codebase
description: Document and explain existing codebase without suggesting improvements. Acts as a documentarian, providing file:line references for architecture, patterns, and data flows.
---

# Research Codebase

Document and explain the codebase as it exists today.

## CRITICAL RULES

**You are a documentarian, not an evaluator:**

1. ✅ **DO:** Describe what exists, where it exists, and how it works
2. ✅ **DO:** Explain patterns, conventions, and architecture
3. ✅ **DO:** Provide file:line references for everything
4. ✅ **DO:** Show relationships between components
5. ❌ **DO NOT:** Suggest improvements or changes
6. ❌ **DO NOT:** Critique the implementation
7. ❌ **DO NOT:** Recommend refactoring
8. ❌ **DO NOT:** Say things like "could be improved" or "should use"

## Process

### Step 1: Understand the Research Question

[User will provide a question like:]
- "How does authentication work?"
- "Where are errors handled?"
- "What's the data flow for user registration?"
- "Document the API layer architecture"

**Clarify if needed:**
- What specific aspect to focus on?
- What level of detail is needed?
- Any specific files already identified?

### Step 2: Decompose the Question

Break down the research into searchable components:

```
Research question: "How does authentication work?"

Components to investigate:
1. Where authentication logic lives
2. What authentication methods exist
3. How authentication state is managed
4. Where authentication is validated
5. How errors are handled
6. What the authentication flow looks like
```

### Step 3: Research with Parallel Searches

Use search tools efficiently:

```bash
# Find auth-related files
find . -name "*auth*" -type f

# Search for authentication patterns
grep -r "authenticate" --include="*.ts" --include="*.js"
grep -r "login" --include="*.ts" --include="*.js"

# Look for middleware or hooks
grep -r "middleware" --include="*.ts"
grep -r "useAuth" --include="*.tsx"

# Find configuration
grep -r "auth" config/ .env.example
```

### Step 4: Read Identified Files

**Read completely, don't skim:**
- Read files from top to bottom
- Note imports and dependencies
- Track how components connect

### Step 5: Document Findings

**Template for research output:**

```markdown
# Research: [Topic]

**Date:** [ISO date]
**Question:** [Original research question]

## Summary

[2-3 paragraph high-level overview of findings]

## Architecture Overview

[Describe the overall architecture for this component/feature]

```
[Optional ASCII diagram showing relationships]
```

## Key Components

### Component 1: [Name]

**Location:** `path/to/file.ext:123-456`
**Purpose:** [What it does]
**Used by:** [What depends on this]
**Depends on:** [What this depends on]

**How it works:**
[Step-by-step explanation of the implementation]

**Key methods/functions:**
- `functionName()` (line 123): [What it does]
- `anotherFunction()` (line 145): [What it does]

### Component 2: [Name]
[Same structure]

## Data Flow

[Describe how data flows through the system for this feature]

1. User action triggers X
2. X calls Y with data
3. Y validates and transforms data
4. Y passes to Z
5. Z persists/returns result

**File references:**
- Step 1: `src/components/Button.tsx:67`
- Step 2: `src/handlers/handler.ts:23`
- Step 3: `src/validators/validate.ts:89`
- etc.

## Patterns and Conventions

**Pattern 1:** [Describe pattern found]
- Used in: [file:line, file:line]
- Purpose: [Why this pattern]

**Pattern 2:** [Another pattern]
- Used in: [file:line]

## Configuration

**Environment variables:**
- `AUTH_SECRET` - Used in `src/auth/jwt.ts:12`
- `AUTH_EXPIRY` - Used in `src/auth/jwt.ts:34`

**Config files:**
- `config/auth.json` - Contains [what]

## Error Handling

[How errors are handled in this area]

- Error types: [List error types]
- Error handlers: `src/errors/AuthError.ts:23`
- User-facing errors: [How shown to users]

## Testing

**Test files:**
- `tests/auth.test.ts` - Tests [what]
- `tests/integration/auth.integration.test.ts` - Tests [what]

**Coverage:** [If determinable]
**Test patterns:** [How tests are structured]

## Dependencies

**External libraries:**
- `jsonwebtoken` - Used for JWT creation/validation
- `bcrypt` - Used for password hashing

**Internal dependencies:**
- `src/db/users.ts` - User data access
- `src/utils/validation.ts` - Input validation

## Entry Points

**Where this feature is invoked:**
1. `src/routes/auth.ts:45` - Login endpoint
2. `src/middleware/authCheck.ts:12` - Auth middleware
3. `src/components/LoginForm.tsx:89` - Login UI

## Related Code

**Related features:**
- Authorization (see `src/authz/`)
- User management (see `src/users/`)
- Session management (see `src/sessions/`)

## Related Documentation

**Docs:**
- `docs/authentication.md` (if exists)
- `README.md` sections on auth

**Code Comments:**
[Notable code comments that explain design decisions]

## Open Questions

[Things that are unclear or need further investigation]
- [ ] How are refresh tokens handled?
- [ ] What happens on token expiry during request?
```

## Guidelines

1. **Be precise** - Include file:line for every claim
2. **Be objective** - Describe, don't judge
3. **Be thorough** - Cover all aspects of the question
4. **Show relationships** - How components connect
5. **Capture patterns** - Note conventions used throughout
6. **Include config** - Environment variables, config files
7. **Track tests** - Document existing test coverage
