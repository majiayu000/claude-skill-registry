---
name: generate-tasks
description: |
  Task generation and breakdown workflow. Use when decomposing a PRD or complex feature
  into implementable subtasks with clear acceptance criteria and dependencies.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Skill: Generate Task List from PRD

## Overview

Guide AI in creating detailed, step-by-step task list in Markdown format based on existing PRD. The task list should guide a developer through implementation with built-in quality checkpoints.

**Use When**: PRD created, ready to plan implementation
**4D Phase**: Develop (planning implementation steps)

## Prerequisites

✅ **Before using this skill:**
- PRD exists in `.claude/tasks/NNNN-prd-feature-name.md`
- PRD reviewed and approved by user
- `CLAUDE.md` exists (or will be created during this process)
- Current codebase reviewed for context

## Process Overview

### Two-Phase Approach

**Phase 1**: Generate parent tasks → Present to user → Wait for "Go"
**Phase 2**: Generate detailed sub-tasks → Save file → Inform user

This ensures high-level plan approved before diving into details.

## Phase 1: Analysis & High-Level Planning

### Step 1: Receive PRD Reference
User points AI to specific PRD file.

**Example**:
```
"Generate tasks for @.claude/tasks/0001-prd-user-authentication.md using @.claude/skills/generate-tasks/SKILL.md"
```

### Step 2: Read PRD
AI reads and analyzes:
- Functional requirements
- User stories
- Technical considerations
- Guardrails affected
- Success metrics

### Step 3: Assess Current State
**CRITICAL**: Review existing codebase before planning.

**AI must:**

1. **Check `CLAUDE.md`** for:
   - Tech stack and framework choices
   - Existing architecture patterns
   - Testing framework and conventions
   - Deployment configuration

2. **Scan codebase** for:
   - Existing directory structure
   - Similar features (auth, API routes, etc.)
   - Naming conventions
   - Test file patterns
   - Component organization

3. **Identify reusable components**:
   - Existing utilities that can be leveraged
   - UI components from design system
   - Database connection patterns
   - Error handling patterns
   - Validation utilities

4. **Check guardrails compliance**:
   - Current file lengths (don't add to files approaching limits)
   - Existing test coverage patterns
   - Security patterns in use
   - Performance considerations

**Output**: Brief summary for user review before generating tasks.

**Example**:
```markdown
## Current State Assessment

**Existing Infrastructure:**
- Express.js backend with TypeScript
- Prisma ORM with PostgreSQL
- Jest for testing (78% coverage currently)
- React frontend with Tailwind CSS

**Reusable Components:**
- `lib/validation.ts` - Input validation utilities (use Zod)
- `components/Form.tsx` - Form component (reuse for auth forms)
- `lib/errors.ts` - Centralized error handling (extend for auth errors)

**Patterns to Follow:**
- API routes in `src/api/<feature>/` structure
- Tests alongside code (`*.test.ts`)
- Repository pattern for data access
- Environment variables via `.env` with fallbacks

**Guardrails Note:**
- `src/api/user/user.controller.ts` is 285 lines (near 300 limit - don't modify)
- Create new auth module instead of extending user module
```

### Step 4: Generate Parent Tasks
Based on PRD and current state, create high-level tasks.

**Guidelines:**
- Typically 4-7 parent tasks
- Each parent = logical phase of implementation
- Order by dependency (database → backend → frontend → tests)
- Include setup, implementation, testing, documentation

**Save to**: `.claude/tasks/tasks-NNNN-prd-feature-name.md`

**Present to user** in this format:

```markdown
## High-Level Tasks

- [ ] 1.0 Database Schema & Migrations
- [ ] 2.0 Backend Authentication Service
- [ ] 3.0 API Routes & Middleware
- [ ] 4.0 Frontend Auth Components
- [ ] 5.0 OAuth Integration
- [ ] 6.0 Testing & Validation
- [ ] 7.0 Documentation & Deployment

**Relevant Files** (identified):
- `src/db/schemas/user.schema.ts` - Create
- `src/auth/auth.service.ts` - Create
- `src/api/auth/auth.controller.ts` - Create
... (full list in task file)
```

**Then inform user**:
```
"High-level tasks generated. Review the task structure above.
Ready to generate detailed sub-tasks? Respond with 'Go' to proceed."
```

### Step 5: Wait for User Confirmation
**PAUSE** - Do not proceed until user responds with "Go" or equivalent.

This checkpoint ensures high-level plan aligns with expectations before diving into details.

---

## Phase 2: Detailed Task Breakdown

### Step 6: Generate Sub-Tasks
Once user confirms "Go", break down each parent task into actionable sub-tasks.

**Sub-task Guidelines:**

1. **Granularity**: Each sub-task = 30-60 min of work (3,000-6,000 tokens)
2. **Atomicity**: Complete in one session, one commit
3. **Testability**: Each sub-task includes verification step
4. **Dependency**: Clear which sub-tasks depend on others
5. **Guardrails**: Each task validates against relevant guardrails

**Sub-task Naming Convention:**
- Use present tense verbs: "Create", "Implement", "Add", "Update", "Test"
- Be specific: "Create user schema" not "Setup database"
- Include success criterion: "Create user schema (with email, password_hash, created_at fields)"

**Example Parent → Sub-tasks**:
```markdown
- [ ] 1.0 Database Schema & Migrations
  - [ ] 1.1 Create user schema with Prisma (email, password_hash, oauth_provider, created_at, updated_at)
  - [ ] 1.2 Create session schema with Prisma (user_id FK, token, expires_at, created_at)
  - [ ] 1.3 Generate and run Prisma migration for user and session tables
  - [ ] 1.4 Verify schema in PostgreSQL (check indexes, constraints)
  - [ ] 1.5 Update .env.example with DATABASE_URL placeholder
```

### Step 7: Add Guardrail Validation Per Task
For each sub-task, identify which guardrails must be validated.

**Format**: Add guardrail checklist as comment under relevant tasks.

**Example**:
```markdown
- [ ] 2.3 Implement password hashing service (bcrypt, cost factor 12)
  <!-- Guardrails:
    ✓ All environment variables have secure defaults (BCRYPT_ROUNDS=12)
    ✓ All exported functions have type signatures and JSDoc
    ✓ Function ≤50 lines (hash, verify, validate strength as separate functions)
    ✓ Edge cases tested (null, empty, too short, invalid chars)
  -->
```

### Step 8: Add Complexity Estimates
For each sub-task, estimate complexity in tokens (not time).

**Complexity Levels:**
- **Simple**: <2,000 tokens (single function, straightforward logic)
- **Medium**: 2,000-5,000 tokens (multiple functions, some complexity)
- **Complex**: 5,000-10,000 tokens (multiple files, integration, edge cases)

**Example**:
```markdown
- [ ] 2.3 Implement password hashing service [~3,000 tokens - Medium]
```

### Step 9: Identify Relevant Files
List all files that will be created or modified, including tests.

**Format**: See `references/process.md` for detailed file listing format.

### Step 10: Add Implementation Notes
Provide guidance for each task section.

**Include:**
- Testing requirements specific to this feature
- Performance considerations
- Security reminders
- Integration points
- Common pitfalls to avoid

**Example**:
```markdown
## Implementation Notes

### Testing Requirements
- All auth logic must have >95% coverage (business-critical)
- Test files alongside code (e.g., `auth.service.ts` + `auth.service.test.ts`)
- Use `npm test src/auth` to run auth module tests only
- Integration tests must test actual JWT validation, not mocks

### Security Checklist (verify before each commit)
- [ ] All passwords hashed (never store plain text)
- [ ] All JWT secrets from environment variables
- [ ] All inputs validated with Zod schemas
- [ ] All SQL queries parameterized (use Prisma)
- [ ] Rate limiting on login/register endpoints
- [ ] Authentication events logged

### Performance Targets
- Login/register: <200ms (p95)
- JWT validation: <50ms (p95)
- Password hashing: 100-300ms (bcrypt cost 12)

### Common Pitfalls
- ❌ Don't validate JWT in database query (use middleware)
- ❌ Don't store tokens in localStorage (use httpOnly cookies)
- ❌ Don't return sensitive data in error messages
- ❌ Don't skip rate limiting (prevents brute force)
```

### Step 11: Generate Final Output
Combine all sections into final task list structure.

See `references/process.md` for complete output format template.

---

## Output Location

**File**: `.claude/tasks/tasks-NNNN-prd-feature-name.md`
**Format**: Markdown
**Naming**: Match PRD filename (e.g., PRD is `0001-prd-user-auth.md` → tasks are `tasks-0001-prd-user-auth.md`)

---

## Implementation Workflow

### During Implementation

User will say: "Start on task 1.1" or "Continue with next task"

AI should:
1. Implement the specific sub-task
2. Write tests alongside code
3. Validate against guardrails in task comment
4. Run tests
5. Verify success criteria
6. Commit with message: `feat(auth): task 1.1 - create user schema`
7. Mark task complete in task list file
8. Ask: "Task 1.1 complete. Review changes? Or continue with 1.2?"

---

## Guardrails Integration

For each sub-task, identify which of CLAUDE.md's 30+ guardrails apply.

**Common guardrails per task type:**

### Database Schema Tasks
- ✓ All environment variables have secure defaults
- ✓ Parameterized queries (Prisma enforces this)

### Service/Logic Tasks
- ✓ No function exceeds 50 lines
- ✓ Cyclomatic complexity ≤10 per function
- ✓ All exported functions have type signatures and JSDoc
- ✓ All user inputs validated before processing

### API/Route Tasks
- ✓ All API boundaries have input validation (Zod schemas)
- ✓ All async operations have timeout/cancellation
- ✓ API responses <200ms for simple queries

### Test Tasks
- ✓ Coverage targets: >95% for auth (business-critical)
- ✓ All public APIs have unit tests
- ✓ Edge cases tested (null, empty, boundary values)
- ✓ No test interdependencies

### Security Tasks (Auth-related)
- ✓ All user inputs validated before processing
- ✓ All database queries parameterized
- ✓ All environment variables have secure defaults
- ✓ Dependencies checked for vulnerabilities

---

## Final Instructions

### For AI Assistant:

**Phase 1 (High-Level)**:
1. ✅ Read PRD thoroughly
2. ✅ Assess current codebase (scan for existing patterns)
3. ✅ Generate 4-7 parent tasks
4. ✅ Identify all relevant files
5. ✅ Present to user
6. ❌ **WAIT for "Go" before Phase 2**

**Phase 2 (Detailed)**:
1. ✅ Break each parent into 3-8 sub-tasks
2. ✅ Add guardrail validation per task
3. ✅ Add complexity estimates
4. ✅ Add implementation notes
5. ✅ Save task list file
6. ✅ Inform user: "Task list ready at [path]. Ready to start task 1.1?"

**During Implementation**:
1. ✅ Implement one sub-task at a time
2. ✅ Validate guardrails for that specific task
3. ✅ Write tests alongside code
4. ✅ Commit after each task (atomic commits)
5. ✅ Update task list (mark completed)
6. ✅ Ask user to review before continuing

### Target Audience

**Primary**: Junior developer with AI assistance
**Assumption**: Developer knows fundamentals but needs clear guidance on:
- Where to create files
- What patterns to follow
- Which guardrails to validate
- How to test properly

---

## References

See `references/process.md` for:
- Complete output format template
- Detailed file listing examples
- Extended implementation notes
- Full task breakdown examples

---

**Remember**: Good task breakdown = clear roadmap. Each sub-task should be:
- **Atomic**: Complete in one session
- **Testable**: Has clear success criterion
- **Guarded**: Validates specific guardrails
- **Estimated**: Complexity known upfront
- **Dependent**: Dependencies clear (order matters)

---

## Autonomous Execution (Optional)

If the project uses autonomous AI coding loops (Ralph Wiggum methodology),
the generated task list can be converted to machine-readable format for
unattended execution.

After generating the markdown task list:

```bash
samuel auto init --prd .claude/tasks/NNNN-prd-feature.md
```

This converts the PRD and task list into `.claude/auto/prd.json` and
generates the loop orchestration files. See `.claude/skills/auto/SKILL.md`
for the full autonomous workflow.
