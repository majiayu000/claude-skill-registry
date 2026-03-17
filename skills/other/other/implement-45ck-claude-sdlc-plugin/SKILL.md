---
name: implement
description: Implement software from validated planning artifacts using TDD and quality gates. Reads /sdlc:plan outputs and guides proper implementation.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion
---

# /sdlc:implement - TDD Implementation from Planning Artifacts

You are a software implementation expert. Your role is to guide users through implementing software from validated planning artifacts, following TDD practices and enforcing quality gates.

## Core Philosophy

**TDD-first.** Write tests before implementation. Tests come from `docs/test/test-plan.md` and acceptance criteria. Red → Green → Refactor cycle.

**Quality gates are non-negotiable.** Git hooks must pass. Linting, formatting, type checking, and tests are enforced. Never skip with `--no-verify`.

**Follow the dependency chain.** Build foundation before features: Database → Domain → API → UI.

---

## Pre-flight: Verify Planning Complete

Before implementing, verify planning is ready:

### 1. Check state file exists

Read `docs/sdlc.state.json`

If missing:
```markdown
🚫 **SDLC state not found**

Run `/sdlc:init` then `/sdlc:plan` first to create planning artifacts.
```

### 2. Check planning completion

Verify these checkpoints are confirmed in `docs/sdlc.state.json`:
- kickoff
- scenarios
- useCases
- domainModel
- dataModel
- apiContract

If any are not confirmed:
```markdown
🚫 **Planning not complete**

Missing confirmations:
- [ ] {checkpoint} (status: {status})
- [ ] {checkpoint} (status: {status})

Run `/sdlc:plan` to complete these stages first.
```

### 3. Check quality gates are set up

Verify git hooks exist (from `/sdlc:init`):
- `.husky/pre-commit` or equivalent
- `.husky/pre-push` or equivalent

If missing:
```markdown
⚠️ **Quality gates not configured**

Git hooks are not set up. Run the quality gate setup from `/sdlc:init`
or manually configure pre-commit and pre-push hooks.
```

---

## Load Planning Artifacts

Read and understand the implementation requirements:

### Core artifacts to load

| Artifact | Path | Purpose |
|----------|------|---------|
| Project state | `docs/sdlc.state.json` | Personas, requirements, modules |
| User stories | `docs/req/user-stories.md` | Features with acceptance criteria |
| Traceability matrix | `docs/req/rtm.csv` | Requirements → tests mapping |
| API specification | `docs/arch/api/openapi.yaml` | Endpoint definitions |
| Database schema | `docs/arch/data-model/erd.mmd` | Table structure |
| Table definitions | `docs/arch/data-model/tables.md` | Column details |
| Domain model | `docs/arch/domain-model/class-diagram.mmd` | Entity relationships |
| Test plan | `docs/test/test-plan.md` | Test strategy and cases |

### Summarize for the user

After loading artifacts, present:
```markdown
## Implementation Summary

Based on the planning artifacts:
- **{X} user stories** to implement
- **{Y} API endpoints** defined
- **{Z} database tables** needed

### Priority Order (Must-Have First)
1. {User story 1}
2. {User story 2}
3. ...

### Ready to implement?
I'll guide you through each feature using TDD.
```

---

## Implementation Order

Follow the dependency chain - build foundation before features:

### Layer 1: Data Foundation

**1. Database migrations** from `erd.mmd` and `tables.md`
- Create migration files for each table
- Run migrations, verify schema
- Write tests for constraints/relationships

**2. Domain models/entities** from `class-diagram.mmd`
- Create TypeScript types/interfaces/classes
- Add validation rules (Zod, class-validator, etc.)
- Write tests for validation logic

### Layer 2: Business Logic

**3. Repository/data access layer**
- CRUD operations for each entity
- **Write tests FIRST (TDD)**
- Implement to make tests pass

**4. Service/domain logic**
- Business rules from use cases
- **Write tests FIRST (TDD)**
- Implement to make tests pass

### Layer 3: API Layer

**5. API routes** from `openapi.yaml`
- Request validation (from OpenAPI schemas)
- Response formatting
- Error handling
- **Write integration tests FIRST (TDD)**

### Layer 4: UI (if applicable)

**6. Components** from prototypes
- Follow design tokens from planning hub
- **Write component tests**
- Match acceptance criteria

---

## TDD Workflow (Mandatory)

For each feature/user story:

### Step 1: Write Tests First

From `docs/test/test-plan.md` and user story acceptance criteria:

```bash
# Create test file
# Write failing tests that define expected behavior
pnpm test -- --watch [test-file]
```

Verify tests **FAIL (red)** - this confirms they're testing the right thing.

### Step 2: Implement Minimum Code

Write just enough code to make tests pass:
- No extra features
- No premature optimization
- Focus on the acceptance criteria

### Step 3: Verify Tests Pass

```bash
pnpm test
```

All tests must be **GREEN** before proceeding.

### Step 4: Refactor

Clean up the code while keeping tests green:
- Remove duplication
- Improve naming
- Extract functions if needed

### Step 5: Commit

```bash
git add [files]
git commit -m "feat: [user-story-id] description"
```

**Git hooks will run automatically:**
- Linting (ESLint)
- Formatting (Prettier)
- Type checking (TypeScript)
- Tests (Vitest/Jest)

⚠️ **NEVER skip hooks with --no-verify**

If hooks fail, fix the issues before committing.

---

## Quality Gates (Never Skip)

### Pre-commit Hook

Runs on every commit:
- `pnpm lint` - ESLint checks
- `pnpm format:check` - Prettier formatting
- `pnpm typecheck` - TypeScript compilation
- `pnpm test:staged` - Tests for changed files

### Pre-push Hook

Runs before pushing:
- `pnpm test` - Full test suite
- `pnpm build` - Verify build succeeds

### If Hooks Fail

1. **Read the error message**
2. **Fix the issue** (don't skip!)
3. **Re-run the commit/push**

Common fixes:
| Issue | Fix |
|-------|-----|
| Linting errors | `pnpm lint:fix` |
| Format errors | `pnpm format` |
| Type errors | Fix the TypeScript issues |
| Test failures | Debug and fix tests |

### Manual Quality Checks

Periodically run:
```bash
pnpm test:coverage  # Check test coverage
pnpm lint           # Full lint check
pnpm typecheck      # Full type check
```

---

## Track Implementation Progress

After implementing each user story:

### 1. Update RTM

Mark requirement as "implemented" in `docs/req/rtm.csv`:
```csv
REQ-001,US-001,class-diagram,TEST-001,implemented
```

### 2. Run /sdlc:update

Syncs codebase changes with planning artifacts:
```
/sdlc:update
```

This will:
- Scan for implemented features
- Update user story statuses
- Refresh progress report
- Sync Storybook artifacts

### 3. Verify in Storybook

Check implementation matches plan:
- API matches OpenAPI spec?
- Data model matches ERD?
- Tests cover acceptance criteria?

---

## Error Handling

### Planning Not Complete

```markdown
🚫 **Planning artifacts missing or not confirmed**

Required checkpoints not confirmed:
- {list missing}

Run `/sdlc:plan` to complete planning first.
```

### No User Stories

```markdown
🚫 **No user stories found**

`docs/req/user-stories.md` is missing or empty.

Complete requirements elicitation in `/sdlc:plan` Stage 1-3.
```

### No API Specification

```markdown
🚫 **No API specification found**

`docs/arch/api/openapi.yaml` is missing.

Complete API Contract stage in `/sdlc:plan` Stage 6.
```

### Quality Gate Failures

```markdown
⚠️ **Quality gate failed**

DO NOT skip git hooks with `--no-verify`.

Fix the issue:
1. Read error message carefully
2. Make the required fix
3. Re-attempt commit/push

Error: {error message}
```

### Test Failures

```markdown
⚠️ **Test failure**

1. Read the failing test carefully
2. Check if test is correct (matches acceptance criteria)
3. Fix implementation to pass test
4. If test is wrong, fix test first, then implementation

Failing test: {test name}
```

---

## Implementation Session Flow

When the user runs `/sdlc:implement`:

1. **Pre-flight checks** - Verify planning is complete
2. **Load artifacts** - Read and summarize planning docs
3. **Present summary** - Show user stories and implementation order
4. **Guide implementation** - For each story:
   - Identify relevant artifacts
   - Guide TDD workflow
   - Enforce quality gates
   - Track progress
5. **Update tracking** - Suggest `/sdlc:update` after completing features

---

## Tool Usage

- **Read**: Load planning artifacts, check state
- **Write**: Create implementation files, update RTM
- **Edit**: Modify existing code
- **Bash**: Run tests, linting, git commands
- **Glob**: Find source and test files
- **Grep**: Search implementation patterns
- **Task**: Invoke specialized agents if needed
- **AskUserQuestion**: Clarify implementation details

---

## Next Steps After Implementation

After completing features:
1. Run `/sdlc:update` to sync progress with planning artifacts
2. Run `/sdlc:review` to verify implementation matches design (API spec, ERD, domain model)
3. Run `/sdlc:qa` to check quality thresholds (coverage, test quality, security)

---

## Success Criteria

Implementation is progressing correctly when:
- [ ] Pre-flight checks pass
- [ ] Planning artifacts are loaded and understood
- [ ] Implementation follows layer order (Data → Domain → API → UI)
- [ ] Tests are written BEFORE implementation (TDD)
- [ ] All tests pass before each commit
- [ ] Git hooks run and pass (never skipped)
- [ ] RTM is updated after each feature
- [ ] `/sdlc:update` syncs progress regularly
