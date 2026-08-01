---
name: project-manager
description: 'Manage project planning, documentation, and ticket coordination. Use
  this skill for: (1) Project planning and roadmap management, (2) Creating and coordinating
  tickets (T0000N), (3) Managing docs/ dir'
---

---
name: project-manager
description: Manage project planning, documentation, and ticket coordination. Use this skill for: (1) Project planning and roadmap management, (2) Creating and coordinating tickets (T0000N), (3) Managing docs/ directory structure and CRUD operations, (4) Post-ticket completion tasks (export tests, update planning docs).
---

# Project Manager

High-level project planning, documentation management, and ticket coordination.

## Responsibilities

| Area | Description |
|------|-------------|
| **Planning** | Manage roadmap, features, and priorities |
| **Tickets** | Create tickets, coordinate implementation, verify completion |
| **Docs** | CRUD operations on docs/ directory |
| **Completion** | Export tests, update planning docs, archive tickets |

## Directory Structure

```
docs/
├── 0-patterns/        # Coding patterns (MUST follow)
├── 1-prd/             # Product Requirements (READ-ONLY)
├── 2-current/         # Planning and status documents
│   ├── 00-overall-plan.md      # Roadmap and next tickets
│   ├── 01-deferred-features.md # Postponed features
│   ├── 02-completed.md         # Completed features
│   └── 03-failed-tests.md      # Failed test tracking
├── 3-tests/           # Test cases by layer
│   ├── smoke/         # Quick health checks
│   │   └── backend-smoke/
│   │       ├── tests-definition.json
│   │       └── tests-results.json
│   ├── core/          # Application-level feature tests
│   │   ├── backend/{feature}/
│   │   └── desktop/{feature}/
│   └── tickets/       # Ticket test suites
│       └── T0000N/
│           ├── tests-definition.json       # READ-ONLY source
│           ├── tests-in-progress.json      # run-tests stage
│           ├── tests-in-verification.json  # verify-tests stage
│           ├── tests-results.json          # Final merged results
│           └── test_*.py
├── 4-reference/       # External references
├── 5-server/          # Server maintenance
├── issues/            # Issue tracking (I0000N)
└── tickets/           # Ticket tracking (T0000N)
    ├── archive/
    ├── T0000N/
    └── index.md
```

## Test Layers

| Layer | Purpose | Count |
|-------|---------|-------|
| **Smoke** | App launches, critical paths work | 3-5 per app |
| **Core** | Feature works end-to-end | 5-10 per feature |
| **Tickets** | All ticket tests | All from tickets |

See `references/test-structure.md` for detailed test organization.

## CRUD Rules

See `references/crud-rules.md` for details.

| Directory | Create | Read | Update | Delete |
|-----------|--------|------|--------|--------|
| `0-patterns/` | Rare | Frequent | Rare | Never |
| `1-prd/` | User only | Frequent | User only | Never |
| `2-current/` | Yes | Frequent | Frequent | Replace |
| `3-tests/` | On complete | Yes | On re-export | Rare |
| `tickets/` | New work | Frequent | Workflow | Archive |

## Supervisor Workflow

When user mentions a ticket, follow these steps:

### 1. Get Bearings
- Read ticket documents in `docs/tickets/T0000N/`
- Check git history for recent commits
- Read `5-progress-and-issues.md` for current status
- **Capture current app state visually** to understand starting point:
  - Desktop: Use `screenshot-capture` skill
  - Web: Use `mcp chrome-devtools take_screenshot`

### 2. Implement Ticket

Work on ticket implementation using available skills:

**Use skills for specific tasks:**
- `run-tests` - Execute tests and record trajectory
- `verify-tests` - Verify tests by following recorded trajectory
- `builder` - Compile apps before testing (if needed)
- `code-mapper` - Document code execution flows

**Implementation loop:**
1. Run `run-tests` skill to execute tests
2. Read `5-progress-and-issues.md` for status
3. Check termination conditions:
   - **COMPLETED**: `6-final.md` exists and all tests pass → Go to Step 3
   - **BLOCKED**: Blocking issues found → Analyze and attempt resolution (see below)
   - **IN PROGRESS**: Tests remaining → Continue implementation
4. Repeat until COMPLETED or truly blocked

**Handling blocking issues:**
1. Read the blocking issue details from `5-progress-and-issues.md`
2. Analyze root cause - is this solvable without user input?
   - Missing information → Search codebase, docs, or web
   - Technical problem → Research solutions, try alternative approaches
   - Ambiguous requirement → Check PRD, past tickets, or infer from context
3. If solution found → Continue with resolution
4. Only report to user if issue **truly requires** their input:
   - Business decision needed (e.g., which behavior is correct?)
   - Access/credentials required
   - External dependency on user action
   - Multiple valid approaches needing user preference

### 3. Verify Completion
When implementation is complete:
- Confirm all `ticket-completion: true` tests pass in `docs/3-tests/tickets/T0000N/tests-results.json`
- Verify `6-final.md` exists
- Check all 6 ticket documents complete
- **Capture final app state** as visual confirmation:
  - Desktop: Use `screenshot-capture` skill
  - Web: Use `mcp chrome-devtools take_screenshot`

### 4. Post-Completion Tasks

Use `post-ticket-completion` skill for:
- Exporting core tests (if applicable)
- Updating smoke tests (rare)
- Updating planning docs
- Reflecting on learnings
- Recording changes to history

See `post-ticket-completion` skill for detailed steps.

## Creating New Tickets

1. Determine next ticket number from `docs/tickets/index.md`
2. Create `docs/tickets/T0000N/1-definition.md`
3. Create `2-plan.md` and add to `index.md`
4. Implement ticket (see Supervisor Workflow step 2)

See `references/ticket-templates.md` for document templates.

## Planning Documents

| Document | Purpose | When to Update |
|----------|---------|----------------|
| `00-overall-plan.md` | Roadmap, next tickets | Ticket completion |
| `01-deferred-features.md` | Postponed features | Feature defer |
| `02-completed.md` | One-liner summaries | Ticket completion |

See `references/index-formats.md` for formats.

## Available Skills and Agents

| Name | Type | When to Use |
|------|------|-------------|
| `run-tests` | Skill | Execute tests (run_tests stage) |
| `verify-tests` | Skill | Verify tests (verify stage) |
| `builder` | Skill | Compile apps before testing |
| `code-mapper` | Skill | Document code execution flows |
| `post-ticket-completion` | Skill | After ticket passes all tests |
