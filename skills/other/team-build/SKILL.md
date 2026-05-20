---
description: "Preset-driven team building — spawn coordinated multi-agent teams from battle-tested presets for full-stack, review, testing, TDD, and migration workflows"
---

# Team Build

Spawn a coordinated team of agents from a preset configuration. Each preset defines agent roles, skill assignments, ownership boundaries, and execution order so you get a production-grade team in one command.

## Quick Start

```
/sw:team-build --preset full-stack "Build checkout flow"
/sw:team-build --preset review "Review auth module"
/sw:team-build --preset testing "Test payment service"
/sw:team-build --preset tdd "Implement rate limiter"
/sw:team-build --preset migration "Migrate users to v2 schema"
```

**Note:** For the complete 9-domain skill mapping table, see `/sw:team-lead`.

## How It Works

1. Parse the `--preset` flag to select a team configuration
2. Read the active increment from `.specweave/increments/` for context
3. Spawn agents with assigned skills, ownership scopes, and dependencies
4. Coordinate execution order (sequential gates or parallel fan-out)
5. Each agent operates via `/sw:do` or `/sw:auto` within its ownership boundary
6. Quality gates run `/sw:grill` before any agent marks work complete

---

## Presets

### 1. `full-stack` — Contract-First Full-Stack Development

**Agents**: 3
**Execution order**: Sequential gate then parallel fan-out

Build features end-to-end with a shared-types-first contract approach. Agent 1 establishes the contract (types, shared utilities, interfaces) before backend and frontend agents work in parallel against that contract.

#### Agent Composition

| # | Role | Skill(s) | Owns | Responsibility |
|---|------|----------|------|----------------|
| 1 | Shared/Types | `sw:architect` | `src/types/`, `src/utils/`, `src/shared/` | Define TypeScript interfaces, shared validators, utility functions, and API contracts |
| 2 | Backend | `sw:architect` + `sw-infra:devops` | `src/api/`, `src/services/` | Implement API endpoints, service layer, database queries, and infrastructure config |
| 3 | Frontend | `sw-frontend:frontend-architect` | `src/components/`, `src/pages/` | Build UI components, pages, state management, and client-side logic |

#### Execution Chain

```
Agent 1 (Shared/Types)
    |
    v
   GATE — types and contracts must compile
    |
    +-------+-------+
    |               |
    v               v
Agent 2          Agent 3
(Backend)        (Frontend)
    |               |
    v               v
  /sw:grill       /sw:grill
```

**Why contract-first**: Backend and frontend agents import from `src/types/` and `src/shared/`. By resolving the contract first, both downstream agents work against stable interfaces — no integration surprises.

#### Example

```
/sw:team-build --preset full-stack "Build user profile page with avatar upload"
```

This spawns:
- **Shared/Types** agent defines `UserProfile`, `AvatarUploadRequest`, `AvatarUploadResponse` types
- **Backend** agent implements `/api/users/:id/profile` and `/api/users/:id/avatar` endpoints
- **Frontend** agent builds `<ProfilePage>`, `<AvatarUploader>` components consuming those types

---

### 2. `review` — Parallel Multi-Perspective Code Review

**Agents**: 3
**Execution order**: All parallel (independent, no dependencies)

Three specialized reviewers examine the codebase simultaneously from different angles. Each agent produces findings independently — no agent blocks another.

#### Agent Composition

| # | Role | Skill(s) | Owns | Responsibility |
|---|------|----------|------|----------------|
| 1 | Security | `sw:security` + `sw:security-patterns` | All files (read-only analysis) | Audit for vulnerabilities, injection vectors, auth flaws, secrets exposure, dependency CVEs |
| 2 | Quality | `sw:grill` + `sw:code-simplifier` | All files (read-only analysis) | Review code quality, complexity, naming, duplication, SOLID violations, performance anti-patterns |
| 3 | Docs | `sw:docs-updater` | All files (read-only analysis) | Check doc coverage, stale comments, missing JSDoc, README accuracy, spec-to-code alignment |

#### Execution Chain

```
+---------------+---------------+---------------+
|               |               |               |
v               v               v               |
Agent 1         Agent 2         Agent 3         |
(Security)      (Quality)       (Docs)          |
|               |               |               |
v               v               v               |
Report          Report          Report          |
+---------------+---------------+---------------+
                |
                v
        Merged review summary
```

**All agents run in parallel.** Each produces an independent report. Reports are merged into a single review summary upon completion.

#### Example

```
/sw:team-build --preset review "Review auth module before release"
```

This spawns three parallel reviewers:
- **Security** agent checks for token leakage, CSRF, injection, and insecure defaults
- **Quality** agent evaluates code structure, test coverage gaps, and complexity hotspots
- **Docs** agent verifies API docs, inline comments, and spec alignment

---

### 3. `testing` — Parallel Test Suite Generation

**Agents**: 3
**Execution order**: All parallel (independent, no dependencies)

Generate comprehensive test coverage across all test levels simultaneously. Each agent focuses on a different testing layer and operates independently.

> **Note:** `sw-testing:qa-engineer` is the primary orchestration skill for testing workflows. This preset splits its responsibilities into specialized agents for parallel execution.

#### Agent Composition

| # | Role | Skill(s) | Owns | Responsibility |
|---|------|----------|------|----------------|
| 1 | Unit | `sw-testing:unit-testing` | `tests/unit/` | Write unit tests for individual functions, classes, and modules with proper mocking |
| 2 | E2E | `sw-testing:e2e-testing` | `tests/e2e/` | Write end-to-end tests for user flows, API sequences, and cross-service interactions |
| 3 | Coverage | `sw-testing:qa-engineer` | `tests/` (analysis scope) | Analyze coverage gaps, generate missing test cases, ensure threshold compliance |

#### Execution Chain

```
+---------------+---------------+---------------+
|               |               |               |
v               v               v               |
Agent 1         Agent 2         Agent 3         |
(Unit)          (E2E)           (Coverage)      |
|               |               |               |
v               v               v               |
unit tests      e2e tests       coverage report |
+---------------+---------------+---------------+
                |
                v
        All tests pass + coverage met
```

**All agents run in parallel.** Unit and E2E agents write tests while the Coverage agent analyzes gaps and generates supplementary tests for uncovered paths.

#### Example

```
/sw:team-build --preset testing "Test payment service end to end"
```

This spawns:
- **Unit** agent writes tests for `PaymentService`, `InvoiceCalculator`, `TaxResolver`
- **E2E** agent writes flow tests: checkout -> payment -> confirmation -> receipt
- **Coverage** agent identifies untested edge cases and generates additional tests

---

### 4. `tdd` — Strict Sequential TDD Cycle

**Agents**: 3
**Execution order**: Strict sequential (Agent 1 -> Agent 2 -> Agent 3)

Enforce the RED-GREEN-REFACTOR discipline with dedicated agents for each phase. Each agent must complete before the next begins — no shortcuts, no phase skipping.

#### Agent Composition

| # | Role | Skill(s) | Owns | Responsibility |
|---|------|----------|------|----------------|
| 1 | Red | `sw:tdd-red` | `tests/` | Write failing tests that define the expected behavior. Tests MUST fail before proceeding. |
| 2 | Green | `sw:tdd-green` | `src/` | Write the minimal implementation to make all failing tests pass. No extra features. |
| 3 | Refactor | `sw:tdd-refactor` | `src/`, `tests/` | Improve code quality, extract abstractions, reduce duplication — all tests must stay green. |

#### Execution Chain

```
Agent 1 (Red)
    |
    v
   GATE — tests must exist AND fail
    |
    v
Agent 2 (Green)
    |
    v
   GATE — all tests must pass
    |
    v
Agent 3 (Refactor)
    |
    v
   GATE — all tests still pass + /sw:grill
```

**Strict sequential execution.** Agent 2 cannot start until Agent 1's tests are verified failing. Agent 3 cannot start until Agent 2's implementation passes all tests. This enforces true TDD discipline.

#### TDD Integration

When `testing.defaultTestMode: "TDD"` is set in `.specweave/config.json`, this preset automatically enables strict enforcement (`testing.tddEnforcement: "strict"`). Tasks in `tasks.md` are tagged with `[RED]`, `[GREEN]`, `[REFACTOR]` phase markers.

#### Example

```
/sw:team-build --preset tdd "Implement rate limiter with sliding window"
```

This spawns sequentially:
- **Red** agent writes tests: `rateLimiter.allows(100, '1m')`, `rateLimiter.rejects(101, '1m')`, sliding window decay tests
- **Green** agent implements `RateLimiter` class with minimal sliding window logic to pass
- **Refactor** agent extracts `SlidingWindow` abstraction, adds TimeProvider injection, cleans up

---

### 5. `migration` — Contract-First Data Migration

**Agents**: 3
**Execution order**: Sequential gate then parallel fan-out

Migrate data schemas safely with a schema-first approach. The schema agent defines the new structure and writes migration scripts before backend and frontend agents adapt to the changes in parallel.

#### Agent Composition

| # | Role | Skill(s) | Owns | Responsibility |
|---|------|----------|------|----------------|
| 1 | Schema | `sw:architect` | `src/types/`, `migrations/`, `prisma/`, `drizzle/` | Define new schema, write migration scripts, update type definitions, ensure backward compatibility |
| 2 | Backend | `sw:architect` | `src/api/`, `src/services/` | Update API endpoints, service logic, queries, and serializers to work with new schema |
| 3 | Frontend | `sw-frontend:frontend-architect` | `src/components/`, `src/pages/` | Update UI components, forms, and state to reflect schema changes |

#### Execution Chain

```
Agent 1 (Schema)
    |
    v
   GATE — migration runs, types compile, rollback tested
    |
    +-------+-------+
    |               |
    v               v
Agent 2          Agent 3
(Backend)        (Frontend)
    |               |
    v               v
  /sw:grill       /sw:grill
```

**Schema-first ensures safety.** The migration and new types must be validated before downstream agents modify application code. Both backend and frontend work against the finalized schema in parallel.

#### Example

```
/sw:team-build --preset migration "Migrate users to v2 schema with address normalization"
```

This spawns:
- **Schema** agent creates `migrations/20240315_users_v2.sql`, updates `UserV2` type, writes rollback
- **Backend** agent updates `/api/users` endpoints to read/write `UserV2`, adds address normalization service
- **Frontend** agent updates `<UserForm>`, `<AddressInput>` components to use new address fields

---

## Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--preset` | Yes | One of: `full-stack`, `review`, `testing`, `tdd`, `migration` |
| `--increment` | No | Increment ID to operate on (defaults to active increment) |
| `--dry-run` | No | Show what agents would be spawned without actually spawning them |
| `--max-agents` | No | Override max concurrent agents (default: 3) |

## Execution Order Summary

| Preset | Order | Pattern |
|--------|-------|---------|
| `full-stack` | Sequential gate + parallel | Agent 1 first, then [Agent 2 + Agent 3] in parallel |
| `review` | All parallel | [Agent 1 + Agent 2 + Agent 3] simultaneously |
| `testing` | All parallel | [Agent 1 + Agent 2 + Agent 3] simultaneously |
| `tdd` | Strict sequential | Agent 1 -> Agent 2 -> Agent 3 (no parallelism) |
| `migration` | Sequential gate + parallel | Agent 1 first, then [Agent 2 + Agent 3] in parallel |

## SpecWeave Workflow Integration

Each spawned agent integrates with the standard SpecWeave workflow:

1. **Increment context** — agents read `spec.md` and `tasks.md` from the active increment
2. **Task execution** — agents use `/sw:do` or `/sw:auto` to work through their assigned tasks
3. **Quality gates** — agents run `/sw:grill` before marking tasks complete
4. **Progress tracking** — task status updates flow back to `tasks.md` with AC linkage
5. **Ownership boundaries** — agents only modify files within their assigned directories
6. **Conflict prevention** — ownership scopes are non-overlapping to prevent merge conflicts

### Organization Discovery (resolve BEFORE spawning agents)

Resolve the `{ORG}` placeholder from `.specweave/config.json` (in priority order):
1. `repository.organization` field
2. `sync.profiles[*].config.owner` (GitHub) or `.config.organization` (ADO)
3. Parse from `umbrella.childRepos[0].path` (strip `repositories/` prefix, take first segment)
4. Check filesystem: `ls repositories/*/` and use the org folder name
5. If all fail, ask the user. **NEVER use .env files for org.**

### Multi-Repo Increment Placement

**In umbrella projects with a `repositories/` folder:**
- Each agent MUST create its increment in its assigned repo's `.specweave/increments/`
- The umbrella root `.specweave/` is for config ONLY, not for agent increments
- Run `specweave init` in each repo if `.specweave/` doesn't exist
- Agent working directory = `repositories/{ORG}/{repo-name}/` (replace `{ORG}` with discovered value)

### Agent Lifecycle

```
Spawn → Load increment context → Claim tasks → /sw:do or /sw:auto → /sw:grill → Report completion
```

### Error Handling

- If a gate agent (Agent 1 in `full-stack`, `migration`, or `tdd`) fails, downstream agents are NOT spawned
- If a parallel agent fails, other parallel agents continue — failures are collected and reported
- Agents retry transient failures (build errors, flaky tests) up to 2 times before reporting failure
- On failure, the agent produces a diagnostic report explaining what went wrong and suggested fixes

#### Invalid Preset Name

If user provides an unknown preset name:

```
Error: Unknown preset "xyz". Available presets: full-stack, review, testing, tdd, migration.
Use /sw:team-build --help to see preset details.
```

## Custom Presets

To define custom presets, add a `teamPresets` section to `.specweave/config.json`:

```json
{
  "teamPresets": {
    "my-preset": {
      "agents": [
        {
          "role": "Analyst",
          "skills": ["sw:architect"],
          "owns": ["src/analysis/"],
          "dependsOn": []
        },
        {
          "role": "Implementer",
          "skills": ["sw:architect"],
          "owns": ["src/core/"],
          "dependsOn": ["Analyst"]
        }
      ]
    }
  }
}
```

Custom presets follow the same execution rules: agents with no `dependsOn` run in parallel; agents with dependencies wait for their predecessors to complete.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Agent fails to spawn | Check that required skills are installed: `claude plugin list` |
| Gate agent blocks forever | Kill the stuck agent and check its output for errors |
| Ownership conflict | Ensure no two agents in the same preset share directory ownership |
| TDD gate rejects Green | Agent 1 (Red) tests must genuinely fail — check for accidentally passing tests |
| Agents out of sync | Run `/sw:progress` to see per-agent task status and identify blockers |
