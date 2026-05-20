---
name: capture-request
description: Capture user intent as structured work requests without executing. Use when user describes work to be done. Separates intent from execution. Writes to do-work/requests/ queue.
user-invocable: true
argument-hint: "<description of work>"
---

# Capture Request

Captures user intent as structured work requests. **Does not execute work.**

This skill implements intent separation: capture what needs to be done, then hand off to the work-loop for execution.

## Purpose

- Accept raw user input describing work
- Detect if input contains multiple disjoint ideas
- Split into separate requests when appropriate
- Group only when dependency exists
- Write structured request files to queue

## Constraints

**CRITICAL: This skill NEVER:**
- Executes code
- Makes repository changes (beyond writing request files)
- Performs speculative planning
- Implements features

**This skill ONLY:**
- Captures intent
- Structures requests
- Writes to `do-work/requests/`

## Request Contract

Every request must follow this schema:

```markdown
# Request: <short descriptive title>

## Intent
What outcome is desired. Plain language.

## Context
Relevant files, constraints, assumptions.
Explicit exclusions.

## Tasks
- Step 1
- Step 2
- Step 3

## Done When
Objective completion criteria.
```

## Workflow

### 1. Parse User Input

When user provides work description:

1. Identify the core intent(s)
2. Check for multiple disjoint ideas
3. Determine dependencies between ideas

### 2. Splitting Rules

**Split into SEPARATE requests when:**
- UI change AND database change (different domains)
- Unrelated features mentioned together
- No execution dependency between items

**Keep as SINGLE request when:**
- Sequential dependency exists (B requires A)
- Tightly coupled changes (model + its tests)
- User explicitly groups them

### 3. Handle Ambiguity

If input is ambiguous:
- Ask ONE clarification question
- Then proceed with best interpretation
- Do not over-clarify

### 4. Write Request Files

For each request:

1. Generate filename: `YYYYMMDD-HHMMSS-slug.md`
2. Write to `do-work/requests/`
3. Confirm to user what was captured

## Directory Setup

If directories don't exist, create them:

```
do-work/
├── requests/    # Pending work
├── in-progress/ # Currently executing
├── archive/     # Completed
└── errors/      # Failed
```

## Examples

### Example 1: Single Request

**User says:**
> "Add a dark mode toggle to the settings page"

**Output:** `do-work/requests/20260128-143022-dark-mode-toggle.md`

```markdown
# Request: Add dark mode toggle to settings

## Intent
Add a user-facing toggle in the settings page that enables dark mode throughout the application.

## Context
- Settings page exists at src/pages/Settings.tsx
- No existing theme system
- Should persist preference (localStorage acceptable)

## Tasks
- Add theme context/state management
- Create toggle component in Settings
- Apply dark theme styles to existing components
- Persist preference across sessions

## Done When
- Toggle visible in settings
- Clicking toggle switches between light/dark
- Preference persists after page reload
- All existing pages respect theme
```

### Example 2: Split Requests

**User says:**
> "Add user authentication and also fix that bug where the footer overlaps on mobile"

**Output:** TWO files

`do-work/requests/20260128-143022-user-auth.md`:
```markdown
# Request: Add user authentication

## Intent
Implement user login/logout functionality.

## Context
- No existing auth system
- Backend API exists at /api/*

## Tasks
- Add login page
- Add auth state management
- Protect authenticated routes
- Add logout functionality

## Done When
- Users can log in with credentials
- Protected routes redirect to login
- Session persists across page loads
- Users can log out
```

`do-work/requests/20260128-143023-footer-mobile-fix.md`:
```markdown
# Request: Fix footer overlap on mobile

## Intent
Fix visual bug where footer overlaps content on mobile viewports.

## Context
- Bug reported on screens < 768px
- Footer component at src/components/Footer.tsx

## Tasks
- Identify CSS causing overlap
- Fix positioning/spacing
- Verify across mobile breakpoints

## Done When
- Footer does not overlap content on any mobile size
- Desktop layout unchanged
```

### Example 3: Grouped Request (Dependency)

**User says:**
> "Create a User model and then add an API endpoint to fetch users"

**Output:** SINGLE file (endpoint depends on model)

```markdown
# Request: Create User model and fetch endpoint

## Intent
Add User data model and API endpoint to retrieve users.

## Context
- Database: PostgreSQL
- ORM: Prisma
- API framework: Express

## Tasks
- Define User model in Prisma schema
- Run migration
- Create GET /api/users endpoint
- Add basic error handling

## Done When
- User table exists in database
- GET /api/users returns list of users
- Empty list returned when no users exist
```

## Output Format

After capturing, respond:

```
Captured X request(s):

1. do-work/requests/20260128-143022-dark-mode-toggle.md
   Intent: Add dark mode toggle to settings

2. do-work/requests/20260128-143023-footer-fix.md
   Intent: Fix footer overlap on mobile

Run `/work-loop` to begin processing.
```

## Integration

This skill works with:
- `/work-loop` - Processes the request queue
- `/thunderdome` - Shows overall project status

Typical workflow:
1. `/capture-request` - Capture what needs to be done
2. `/work-loop` - Execute the work
3. `/thunderdome debrief` - Verify and close session
