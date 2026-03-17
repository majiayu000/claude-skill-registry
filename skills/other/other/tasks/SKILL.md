---
name: tasks
description: "Generate dependency-ordered user stories and tasks from plan. Use after creating plan. Triggers on: create tasks, generate user stories, break down implementation."
---

# User Story & Task Generator

Generate actionable, dependency-ordered user stories from technical plans.

---

## The Job

1. Read spec.md and plan.md
2. Extract user stories from spec
3. Break down into implementation tasks
4. Order by dependencies
5. Create tasks.md with structured user stories
6. **Auto-convert to prd.json** with routing classification

**Important:** tasks.md contains the actual user stories that convert to prd.json!

---

## SpecKit Workflow

This skill is **Step 3 of 5** in the Relentless workflow:

```
specify → plan → tasks → analyze → implement
                   ↓
            (optional: checklist)
```

This skill now **auto-runs convert** at the end, generating prd.json.
Manual convert is only needed if tasks.md is edited manually.
Checklist is optional but recommended for complex features.

---

## Step 1: Locate Feature Files

Find the current feature directory and verify:
- `spec.md` exists
- `plan.md` exists
- Feature directory: `relentless/features/NNN-feature/`

---

## Step 2: Load Context

Read:
1. `relentless/constitution.md` - Testing and quality requirements
2. `relentless/features/NNN-feature/spec.md` - User requirements
3. `relentless/features/NNN-feature/plan.md` - Technical design

Extract **Routing Preference** from spec.md or plan.md (if present) and include it near the top of tasks.md so it can be carried into prd.json.

---

## Step 3: Extract User Stories

From spec.md, identify distinct user stories:
- Each major functional requirement becomes a user story
- Group related functionality
- Typical: 3-8 user stories per feature

**User Story Format:**
```markdown
### US-001: [Title]
**Description:** As a [user], I want [goal] so that [benefit].

**Acceptance Criteria:**
- [ ] Criterion 1 (testable, specific)
- [ ] Criterion 2
- [ ] Criterion 3
- [ ] Typecheck passes
- [ ] Tests pass

**Dependencies:** (if any)
**Phase:** Foundation / Stories / Polish
```

---

## Step 4: Generate Tasks

For each user story, create implementation tasks using format:

```markdown
## User Stories

### US-001: Create User Registration Endpoint

**Description:** As a new user, I want to register with email/password so that I can create an account.

**Acceptance Criteria:**
- [ ] POST /api/auth/register endpoint exists
- [ ] Email validation works
- [ ] Password requirements enforced (min 8 chars)
- [ ] Password is hashed before storage
- [ ] Confirmation email sent
- [ ] Returns 201 with user ID
- [ ] Returns 400 for invalid input
- [ ] Typecheck passes
- [ ] Unit tests pass
- [ ] Integration test passes

**Dependencies:** None
**Phase:** Foundation
**Priority:** 1

---

### US-002: Create User Login Endpoint

**Description:** As a registered user, I want to log in with email/password so that I can access my account.

**Acceptance Criteria:**
- [ ] POST /api/auth/login endpoint exists
- [ ] Validates credentials against database
- [ ] Returns JWT token on success
- [ ] Returns 401 for invalid credentials
- [ ] Returns 403 for unconfirmed accounts
- [ ] Token expires after 24 hours
- [ ] Typecheck passes
- [ ] Unit tests pass
- [ ] Integration test passes

**Dependencies:** US-001
**Phase:** Stories
**Priority:** 2

---

### US-003: Email Confirmation Flow

**Description:** As a new user, I want to confirm my email so that my account is activated.

**Acceptance Criteria:**
- [ ] Confirmation email sent on registration
- [ ] Email contains confirmation link
- [ ] GET /api/auth/confirm/:token endpoint exists
- [ ] Token validates and marks account as confirmed
- [ ] Expired tokens return appropriate error
- [ ] Confirmed users can log in
- [ ] Typecheck passes
- [ ] E2E test passes

**Dependencies:** US-001
**Phase:** Stories
**Priority:** 3
```
If you have any doubts or suggestions about any specific task, interview the user about them to improve your execution.

---

## Step 5: Order by Dependencies

Ensure user stories are ordered so dependencies come first:
1. **Phase 0: Setup** - Infrastructure, configuration
2. **Phase 1: Foundation** - Core models, base functionality
3. **Phase 2: Stories** - User-facing features (ordered by dependencies)
4. **Phase 3: Polish** - Optimization, edge cases

Mark parallel stories with:
```markdown
**Parallel:** Yes
```

---

## Step 6: Validate Completeness

Check that:
- [ ] Every functional requirement from spec has a user story
- [ ] Each user story has specific, testable acceptance criteria
- [ ] Dependencies are valid (no circular references)
- [ ] Each story is independently testable
- [ ] Typecheck/test criteria included
- [ ] Priority order makes sense

---

## Step 6.5: Pre-Conversion Validation

Before saving and converting, validate the format manually:

**Story ID Format:**
- [ ] Every story uses `US-XXX` format (e.g., `US-001`, not `Story 1`)
- [ ] Story IDs are unique and sequential

**Acceptance Criteria Format:**
- [ ] Criteria are full sentences, not just file paths
- [ ] File paths include context (e.g., "`src/queue/types.ts` contains Zod schemas")
- [ ] No standalone file paths like `` `src/file.ts` ``

**Dependencies Format:**
- [ ] Dependencies use `US-XXX` with dashes, not underscores
- [ ] Example: `**Dependencies:** US-001, US-002` (correct)
- [ ] Example: `**Dependencies:** US_001` (incorrect - will warn)

**Common Mistakes to Avoid:**
- ❌ `- [ ] \`src/file.ts\`` (file path only - will be filtered)
- ✅ `- [ ] \`src/file.ts\` contains the queue interface`
- ❌ `**Files:**` inside acceptance criteria (will end criteria parsing)
- ✅ Put **Files:** section after acceptance criteria

---

## Step 7: Save & Validate

1. Save to `relentless/features/NNN-feature/tasks.md`
2. **Run the validator to ensure tasks.md is correctly formatted:**
   ```bash
   .claude/skills/validators/scripts/validate-tasks.sh "relentless/features/NNN-feature/tasks.md"
   ```
   - If validation fails (especially PRD-convertible format), fix errors and re-run
   - Warnings are acceptable but should be reviewed
3. Update progress.txt
4. Report:
   - Total user stories: N
   - Dependency order: [list]
   - Parallel opportunities: N
   - Validation: PASS/FAIL

---

## Step 8: Auto-Convert to prd.json

**CRITICAL: You MUST execute the CLI command below. Do NOT generate prd.json manually.**

After tasks.md is saved, run this command to convert to prd.json with routing:

```bash
relentless convert relentless/features/NNN-feature/tasks.md --feature <feature-name>
```

**⚠️ IMPORTANT:** Execute this bash command using the Bash tool. Do NOT:
- Generate the prd.json file yourself
- Skip this step
- Use any other method

The CLI will:
1. Parse tasks.md and validate structure
2. Classify complexity for each story
3. Route to optimal harness/model per story
4. Generate prd.json with routing metadata
5. Copy to prd.md for reference

**After running the command, report:**
- The routing table from CLI output (story → complexity → harness/model → cost)
- Total estimated cost
- Confirm prd.json was created

**Optional but Recommended:** `/relentless.checklist`
- Generates validation checklist with quality gates
- Helps ensure nothing is missed during implementation
- Especially useful for complex features

**Next Step:** `/relentless.analyze` (or `/relentless.checklist` first if desired)

---

## TDD is MANDATORY

Every user story MUST include test acceptance criteria:

1. **Unit Tests** - For business logic and utilities
2. **Integration Tests** - For API endpoints and data flows
3. **E2E Tests** - For user-facing flows (use Playwright when applicable)

### TDD Workflow

The Relentless agent will verify:
1. Tests are written FIRST (before implementation)
2. Tests FAIL before implementation
3. Implementation makes tests PASS
4. Typecheck and lint pass

### Required Test Criteria

Every story acceptance criteria should include:
- [ ] Unit tests pass
- [ ] Integration test passes (for API stories)
- [ ] Typecheck passes
- [ ] Lint passes

---

## Key Guidelines

**User Story Size:**
- Each story completable in one session
- If too large, split into multiple stories
- Typical: 30-90 minutes of work per story

**Acceptance Criteria:**
- Specific and testable
- No vague terms ("works well", "good UX")
- Include quality checks (typecheck, lint, test)
- Verifiable in browser/tests
- **MUST include test criteria**

**Dependencies:**
- Only list direct dependencies
- Ensure no circular dependencies
- Consider data dependencies (user must exist before profile)

---

## Notes

- tasks.md is the source of truth for user stories
- This file will be converted to prd.json by `relentless convert`
- Make acceptance criteria detailed and specific
- Each story should be independently deployable and testable
