---
name: bdd-driven-development
description: "Use after requirement-analysis, tech-stack-confirmation, and project-architecture-init skills have all been completed — PRD, BDD JSON files, architecture design document, and walking skeleton must already exist. This skill first generates a prioritized execution plan document in docs/plans/, then drives the full development cycle for each feature using BDD-guided TDD based on that plan. Technology-stack agnostic — all tech-specific details (build commands, test frameworks, directory paths) are read from the architecture document at runtime. Triggers on requests like 'start development', 'execute BDD features', 'implement features from PRD', 'run bdd-driven development', or when BDD JSON files exist and implementation has not started."
---

# BDD-Driven Development

## Overview

Drive feature development from BDD acceptance criteria using the complete artifact chain produced by upstream skills. The walking skeleton and project architecture already exist; this skill focuses purely on implementing business features one at a time using BDD-guided TDD.

**Two-phase workflow:**
1. **Planning phase** (Step 0 ~ Step 1) — Read all artifacts, generate a prioritized execution plan document in `docs/plans/`
2. **Development phase** (Step 2 ~ Step 9) — Implement features one by one based on the execution plan, PRD, and BDD JSON files

Each feature follows the cycle: BDD-to-test translation (RED) → minimal implementation (GREEN) → refactor → BDD verification → git commit → next feature.

**Core principle:** BDD scenarios define WHAT to verify; TDD discipline ensures HOW code is written. Never write production code without a failing test derived from a BDD scenario.

**Technology-stack agnostic:** This skill contains zero hardcoded technology choices. All tech-specific details (build commands, test frameworks, directory structure, assertion libraries, mock tools) are read from the architecture document and tech-stack document at the start of each session.

**Announce at start:** "I'm using the bdd-driven-development skill to implement features from BDD acceptance criteria."

## Prerequisites

Before using this skill, verify ALL of the following artifacts exist (produced by upstream skills in order):

1. **PRD document** — `docs/requirements/*-prd.md` (from `requirement-analysis`)
2. **BDD JSON files** — `docs/requirements/*-bdd/*.json` (from `requirement-analysis`)
3. **Tech stack document** — `docs/architecture/*-tech-stack.md` (from `tech-stack-confirmation`)
4. **Architecture design document** — `docs/architecture/architecture.md` (from `project-architecture-init`)
   - Contains module mapping (PRD feature → module → package/directory path)
   - Contains dependency rules (layering and module boundaries)
   - Contains test architecture (test pyramid, frameworks, coverage targets)
5. **Walking skeleton** — Project compiles, health check passes, baseline tests pass (from `project-architecture-init`)
6. **Coding rules** — `.claude/rules/*.md` (from `rules-generation`, if completed)

**If any prerequisite is missing, stop and inform the user which upstream skill needs to run first.**

## Input Artifacts

### BDD JSON Format

Each BDD file contains one feature with multiple scenarios:

```json
[
  {
    "category": "functional",
    "feature": "F-001 Feature Name",
    "description": "Feature description",
    "overallPass": false,
    "bdd": [
      {
        "scenario": "Scenario name",
        "description": "Scenario description",
        "steps": {
          "given": ["Precondition 1", "Precondition 2"],
          "when": ["Action to perform"],
          "then": ["Expected result 1", "Expected result 2"]
        },
        "passes": false
      }
    ]
  }
]
```

### Architecture Document as Runtime Config

The architecture document (`docs/architecture/architecture.md`) serves as the **runtime configuration** for this skill. Read it at the start of every session to extract:

| Information Needed | Where to Find |
|--------------------|---------------|
| Feature → module mapping | Architecture doc: feature-to-module table |
| Source directory structure | Architecture doc: directory structure section |
| Test directory structure | Architecture doc: test directory mirroring rules |
| Layering rules | Architecture doc: dependency rules section |
| Test frameworks and tools | Architecture doc: test architecture section |
| Coverage targets | Architecture doc: coverage targets table |
| Build command | Infer from build config file (pom.xml / package.json / Cargo.toml / go.mod / pyproject.toml) |
| Test command | Architecture doc: test architecture section or infer from build tool |

**Never assume tech-specific defaults. Always read from the architecture document.**

## The Process

### Step 0: Set Up Isolated Workspace

**REQUIRED SUB-SKILL:** Use `superpowers:using-git-worktrees`

Create a worktree for the development session. Branch naming convention:

```
feature/<prd-basename>-impl
```

Example: PRD file `2026-02-12-market-api-prd.md` → branch `feature/market-api-impl`

After worktree is ready, verify baseline:

```bash
<build-command>   # Must succeed
<test-command>    # Must pass
```

If baseline fails, report and stop — do not proceed with failing baseline.

### Step 0.5: Read Project Context

Before implementing any feature, read the architecture document and tech-stack document to establish the working context for this session:

1. **Read `docs/architecture/architecture.md`** — extract:
   - Directory structure (source root, test root, module paths)
   - Dependency/layering rules
   - Feature → module mapping table
   - Test pyramid (unit / integration / e2e classification)
   - Test frameworks and mock/stub tools
   - Coverage targets per layer
   - Architecture fitness function tools

2. **Read `docs/architecture/*-tech-stack.md`** — extract:
   - Language and framework
   - Build tool and commands
   - Test runner and assertion library
   - HTTP mock/stub tool (if applicable)
   - Coverage tool

3. **Read `.claude/rules/*.md`** (if exists) — note coding standards to follow

4. **Establish command cheat sheet** for the session:

```
Build:          <detected-build-command>
Test (all):     <detected-full-test-command>
Test (single):  <detected-single-test-command>
Test (e2e):     <detected-e2e-test-command>
Coverage:       <detected-coverage-command>
Source root:    <detected-source-root>
Test root:      <detected-test-root>
```

5. **Identify E2E test environment requirements**

   Determine whether E2E smoke tests require any environment preparation that the user must handle before tests can run. Common requirements include:
   - External service credentials or API keys (environment variables)
   - Docker containers or test databases that must be running
   - Network access to test endpoints
   - Special build profiles or test profiles to activate
   - Port availability for the test server

   **If E2E tests require environment preparation, inform the user immediately before writing any E2E test code.** Present a clear checklist of what needs to be set up:

   ```
   E2E smoke tests require the following environment setup:
   - [ ] <env-var-1>: <purpose>
   - [ ] <service>: <how to start>
   - [ ] <config>: <what to configure>

   Please confirm these are available before I proceed with E2E test implementation.
   ```

   If E2E tests can run self-contained (e.g., using embedded servers and HTTP stubs only), note this and proceed without user confirmation.

**This step ensures all subsequent steps use project-appropriate commands and paths, not hardcoded defaults.**

### Step 1: Generate Execution Plan Document

This step produces a persistent execution plan document at `docs/plans/bdd-execution-plan.md`. This document becomes the **single source of truth** for development ordering and progress tracking throughout the entire BDD development cycle.

**Step 1.1: Load and analyze all BDD features**

1. Read ALL BDD JSON files from the BDD directory
2. Read the PRD Feature List to get MoSCoW priority per feature
3. Read the architecture module mapping to associate features with modules
4. Filter features where `overallPass` is `false`
5. Sort by priority using PRD MoSCoW:

| Priority | Criteria |
|----------|----------|
| P1 | `Must` features — implement first |
| P2 | `Should` features — implement second |
| P3 | `Could` features — implement last |
| P4 | `Won't` features — skip |

Within the same priority level, follow feature ID order (F-001, F-002, ...).

**Step 1.2: Review BDD scenarios critically**

Before generating the plan, perform a thorough review:
- Cross-check each scenario against the PRD — flag contradictions
- Identify ambiguous `given`/`when`/`then` items that may block test writing
- Verify feature dependencies (does F-002 depend on F-001's output?)
- Identify walking skeleton features that need verification (e.g., auth already implemented)
- Note enum values, data format conventions, and API-specific constraints
- If blocking concerns exist: raise them with user **before** generating the plan

**Step 1.3: Scan walking skeleton status**

Inspect the existing codebase to determine:
- Which infrastructure components are already implemented
- Which module directories exist (empty vs. populated)
- Which tests already exist
- Git repository initialization status

**Step 1.4: Write the execution plan document**

Create the file `docs/plans/bdd-execution-plan.md` using the template defined in the `references/execution-plan-template.md` file of this skill. The plan must contain ALL of the following sections:

1. **Document header** — Generation date, PRD/Architecture/Tech-Stack file references
2. **Project Context table** — Language, framework, build tool, test framework, mock tool, coverage tool
3. **Command Cheat Sheet** — All detected build/test/coverage commands
4. **Walking Skeleton Status** — Checklist of implemented vs. pending infrastructure
5. **Feature Execution Order** — Phased tables (Phase 0: infra verification, Phase 1: Must, Phase 2: Should, Phase 3: Could) with feature name, module, MCP tool name, scenario count, and status column
6. **Feature Dependencies** — ASCII diagram showing execution flow and cross-feature dependencies
7. **BDD Review Notes** — Per-feature technical notes (enum conventions, API constraints, cache behavior, etc.)
8. **Per-Feature Development Cycle** — RED → GREEN → REFACTOR → VERIFY → COMMIT → REPORT
9. **Layered Implementation Order** — core → infrastructure → api (read from architecture doc)
10. **Test Classification Rules** — BDD pattern → test type → test location mapping
11. **Coverage Targets** — Per-module thresholds from architecture doc
12. **Progress Log** — Empty append-only table for tracking feature status changes during development
13. **Final Verification Checklist** — All quality gates that must pass before completion

**Step 1.5: Present plan and wait for user confirmation**

After writing the plan document, present a summary to the user:

```
Execution plan generated: docs/plans/bdd-execution-plan.md

Summary:
- Total: N features, M BDD scenarios
- Phase 0 (Infra Verification): X features
- Phase 1 (Must): Y features
- Phase 2 (Should): Z features
- Phase 3 (Could): W features
- Key dependencies: <list critical dependencies>
- BDD review concerns: <list any flagged issues, or "None">

Starting with <first-feature>. Ready to proceed?
```

**Wait for user confirmation before proceeding to Step 2.**

If the user requests changes to the plan (reorder, skip features, add notes), update the plan document accordingly and re-present.

### Step 1.6: Resume from Existing Plan

If `docs/plans/bdd-execution-plan.md` already exists when the skill is invoked:

1. Read the existing plan document
2. Check the Status column of each feature in the execution order tables
3. Read the Progress Log section to review the development history
4. Identify the next `Pending` feature
4. Present a resume summary:

```
Existing execution plan found: docs/plans/bdd-execution-plan.md

Progress:
- Completed: N/M features
- Next: <feature-id> <feature-name> (module: <module>, N scenarios)

Resume from <feature-id>?
```

4. On confirmation, skip to Step 2 with the next pending feature
5. The plan document is the source of truth — do NOT re-read all BDD files to determine progress

### Step 2: BDD-to-Test Translation (RED Phase)

For the current feature (as determined by the execution plan), translate each BDD scenario into a test case.

> **Before starting:** Update the feature's Status in `docs/plans/bdd-execution-plan.md` from `Pending` to `In Progress`. Also **append** a row to the Progress Log section:
> `| <feature-id> <feature-name> | Pending | In Progress | Starting RED phase |`

**Step 2.1: Determine test type per scenario**

Use the test pyramid from the architecture document to classify each scenario:

| BDD `given` Pattern | Test Type |
|---------------------|-----------|
| Pure input validation, no external call | Unit test |
| Data transformation, business rules only | Unit test |
| External API returns specific response | Integration test (with HTTP mock/stub tool) |
| Requires running server / external service | Integration test |
| Full protocol path (client → protocol layer → feature → response) | E2E smoke test |

**Three test levels explained:**

- **Unit test** — Tests business logic in isolation with mocked dependencies. Fast, no framework context.
- **Integration test** — Tests the feature's internal dependency chain (e.g., Tool → Service → Client) with stubbed external APIs. May use `@SpringBootTest` or equivalent, but often excludes the protocol/entry-point layer for speed.
- **E2E smoke test** — Tests the full application stack **including the protocol/entry-point layer** (MCP Server, REST controller, gRPC service, CLI dispatcher, etc.). Verifies that features are actually discoverable and invocable by external clients through the real protocol. **Must NOT exclude any auto-configuration or framework wiring.**

> **Why E2E smoke tests are critical:** Integration tests that exclude the protocol layer (e.g., `@EnableAutoConfiguration(exclude = {McpServerAutoConfiguration.class})`) can pass even when features are completely invisible to real clients. E2E smoke tests catch registration failures, routing issues, serialization bugs, and configuration problems that only manifest in the full stack.

The specific test framework, mock tool, and assertion library come from the architecture document — do not assume.

**Step 2.2: Write test files**

Place tests in the architecture-specified test directory. The directory structure and file naming conventions are defined in the architecture document's test section.

**Translation rules:**

| BDD Element | Test Element |
|-------------|--------------|
| `given` | Test setup: mock/stub configuration, test fixtures, setup methods |
| `when` | Service method call or API/tool invocation |
| `then` | Assertions using the project's assertion library |
| `scenario` | Test method/function name (use language-appropriate naming convention) |

**Test naming:** Derive descriptive names from the `scenario` field. Use the naming convention appropriate to the project's language:
- Java/Kotlin: `camelCase` method names
- Python: `snake_case` function names
- TypeScript/JavaScript: `camelCase` or descriptive strings
- Go: `TestCamelCase` function names
- Rust: `snake_case` function names

**Rules for writing tests:**
- One test per BDD scenario
- Test name must clearly describe the scenario
- Unit tests: mock external dependencies, test business logic in isolation
- Integration tests: use the project's HTTP mock/stub tool, test full request flow
- E2E smoke tests: start the full application with ALL auto-configuration enabled, test through the real protocol layer
- Each test must be independently runnable
- Follow the project's existing test patterns and coding rules (`.claude/rules/`)

**Write ALL tests for the current feature before writing any production code.**

**Step 2.3: Record BDD-to-test mapping**

Maintain a mapping record for the current feature to streamline verification in Step 5:

```
Feature: F-001 Feature Name
  Scenario: "scenario name" → TestClass#testMethodName (unit)
  Scenario: "scenario name" → TestClass#testMethodName (integration)
  ...
```

This mapping avoids redundant re-discovery during BDD verification and ensures every scenario has a corresponding test.

**Step 2.4: Write E2E smoke test (REQUIRED for the first feature; extend for subsequent features)**

For the **first feature** in the execution plan, write at least one E2E smoke test that validates the full protocol stack. For subsequent features, extend the E2E test to cover the new feature's endpoint/tool.

**E2E smoke test requirements:**

1. **Start the full application** — Use the project's integration test infrastructure but **do NOT exclude any auto-configuration**. The entire application stack must be active, including the protocol/entry-point layer (MCP server, REST controllers, gRPC services, etc.).
2. **Verify feature discoverability** — Confirm the feature is visible to external clients through the protocol layer (e.g., MCP `tools/list` returns the expected tool, REST endpoint responds to OPTIONS/GET, gRPC reflection lists the service).
3. **Invoke through the protocol** — Make a real protocol-level request (e.g., MCP `tools/call`, HTTP request to the actual endpoint) and verify the response.
4. **Use real external API stubs** — Stub external dependencies (e.g., Binance API) via the same HTTP mock tool used in integration tests, but let all internal wiring remain real.

**E2E smoke test anti-patterns to avoid:**
- Excluding auto-configuration classes (e.g., `@EnableAutoConfiguration(exclude = {...})`) — this defeats the purpose
- Directly injecting and calling Tool/Service beans instead of going through the protocol layer
- Skipping E2E because "integration tests already cover it" — they may not cover the protocol registration layer

**Technology-agnostic guidance:**
- For MCP servers: verify `tools/list` returns expected tools, then call a tool and assert the response
- For REST APIs: send an HTTP request to the actual endpoint path and assert the response
- For CLI tools: invoke the CLI command and assert stdout/exit code
- For gRPC services: use a gRPC test client to call the service method

> **The E2E smoke test is the final safety net.** If a feature passes unit tests and integration tests but fails the E2E smoke test, it means the wiring between the protocol layer and the business logic is broken. This is exactly the class of bug that E2E tests are designed to catch.

After writing tests, run them:

```bash
<single-test-command> <test-file-or-class>
```

**Verify RED:**
- All new tests MUST fail
- Failure reason must be "feature not implemented" (class/module/function not found), NOT syntax errors or typos
- If a test passes immediately, it is testing existing behavior — remove or rewrite it
- Compilation/import errors are acceptable at RED phase ONLY if caused by missing production code that will be created in GREEN phase

### Step 3: Implement Minimal Code (GREEN Phase)

For each failing test, write the minimum production code to make it pass.

**Layered implementation order (per architecture dependency rules):**

Read the layering rules from the architecture document. Typical order:

1. **Inner/core layer first** — Domain models, service interfaces, business logic (pure, no framework dependencies)
2. **Infrastructure layer second** — External API clients, data access implementations
3. **Outer/API layer last** — Request handlers, tool definitions, wiring

**Rules:**
- Implement one scenario at a time (smallest passing increment)
- Run tests after each implementation change
- Do NOT add features, abstractions, or "improvements" beyond what the current test requires
- Do NOT refactor during GREEN phase
- Follow coding rules in `.claude/rules/` if they exist
- When all tests for the current feature pass, proceed to REFACTOR

```bash
<single-test-command> <test-file-or-class>
```

**If a test fails unexpectedly:**
- Use `superpowers:systematic-debugging` to investigate
- Fix the production code, not the test (unless the test has a genuine defect)

### Step 4: Refactor (REFACTOR Phase)

After GREEN, clean up while keeping all tests passing:

- Remove duplication between scenarios' implementations
- Improve naming to match domain terminology from PRD
- Extract shared logic if warranted by actual repetition
- Ensure code follows project coding standards (`.claude/rules/`)
- Verify layering rules are not violated (as defined in architecture document)

```bash
# Verify feature tests still pass
<single-test-command> <test-file-or-class>

# Run full test suite to catch regressions
<full-test-command>
```

**If any test fails after refactoring:** Undo the refactoring change and retry with a smaller change.

### Step 5: Verify Feature BDD Scenarios

After all scenarios for the current feature pass via automated tests, perform explicit BDD verification to confirm test coverage matches BDD intent.

> **`passes` field rule:** Do NOT update `passes` or `overallPass` in BDD JSON at this step. Only record verification results. Batch update happens in Step 8 after all features pass final verification. This prevents inconsistent state if later features cause regressions.

**Step 5.1: Verify using the BDD-to-test mapping from Step 2.3**

For each scenario in the BDD JSON, use the mapping record to:
1. Confirm the mapped test method/function exists and is runnable
2. Run the test and record pass/fail
3. Verify assertions cover ALL items in `then`

**Step 5.2: Choose verification method by test type**

| Verification Target | Method |
|---------------------|--------|
| Service returns expected value | Run unit test via test runner |
| API endpoint behavior | Run integration test via test runner |
| Feature discoverable and invocable through protocol | Run E2E smoke test via test runner |
| File/config generated correctly | Glob tool or `ls <path>` |
| Code structure (interface, annotation) | Grep for patterns, Read file |
| External API interaction | Run integration test with HTTP mock/stub |

> **E2E verification is mandatory.** If the feature has no E2E smoke test, verification is incomplete. At minimum, confirm the feature is discoverable through the protocol layer (e.g., appears in `tools/list`, responds at its endpoint path).

**Step 5.3: Record and report**

Record verification results per scenario (pass/fail + output summary). Do NOT update BDD JSON yet.

- **If all scenarios verified:** Mark the feature task as completed, proceed to Step 6
- **If any scenario fails:** Stop and report the gap/failure with details, ask for guidance, do NOT proceed

### Step 6: Commit Feature and Update Plan

After the feature's BDD verification passes (Step 5):

> **Note:** Do NOT include BDD JSON files in this commit. The `passes` fields are updated in Step 8 after final verification.

```bash
# Stage source + tests only (specific files, never git add -A)
git add <source-files> <test-files>

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
feat(<module>): implement <feature-id> <feature-name>

- <N> BDD scenarios implemented and verified
- Unit tests: <count>, Integration tests: <count>, E2E tests: <count>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

**After committing, update the execution plan document:**

1. Update the feature's Status in `docs/plans/bdd-execution-plan.md` from `In Progress` to `Done`.
2. **Append** a row to the Progress Log section:
   `| <feature-id> <feature-name> | In Progress | Done | N/N scenarios, commit <short-hash> |`

**Commit rules:**
- One commit per completed feature
- Commit message uses conventional format: `feat(<module>): <description>`
- Only commit when ALL tests pass (both feature tests and full suite)
- Stage specific files, never `git add -A`
- BDD JSON updates are committed separately in Step 8

### Step 7: Report and Loop

After committing the feature:

```
Feature "<feature-id> <feature-name>" complete.
- Module: <module>
- Scenarios: N/N passing
- Tests: X unit + Y integration + Z e2e
- Files changed: <list>
- Commit: <short-hash>
- Verification output:
  ✓ scenario-1: PASS (test method: TestClass#method)
  ✓ scenario-2: PASS (test method: TestClass#method)

Remaining features: M
Next: "<feature-id> <feature-name>" (module: <module>, N scenarios)

Ready for feedback before continuing.
```

Wait for user feedback. Then return to **Step 2** with the next feature from the execution plan.

### Step 8: Final Verification and Batch Update BDD Status

After ALL features in the execution plan are implemented:

1. Run the full project test suite (including architecture fitness function tests if configured):

```bash
<full-test-command>
```

2. **Run E2E smoke tests** to verify all features are discoverable and invocable through the protocol layer:

```bash
<e2e-test-command>
```

> **E2E verification is a hard gate.** If E2E smoke tests fail, the application is not usable by real clients regardless of how many unit/integration tests pass. Fix E2E failures before proceeding.

4. **Re-run all feature tests** to catch cross-feature regressions:

```bash
# Run each feature's tests to confirm no regressions
<single-test-command> <feature-1-test>
<single-test-command> <feature-2-test>
...
```

5. **If all tests pass — batch update BDD JSON files:**

For each implemented feature, update its BDD JSON file:
- Set each `bdd[].passes` to `true` for verified scenarios
- Set `overallPass` to `true` for the feature
- Use Write tool to update the entire file atomically

> **This is the ONLY step where `passes` fields are updated.** This ensures BDD JSON always reflects the true verified state after all features are complete.

6. **Commit the BDD JSON updates:**

```bash
git add docs/requirements/*-bdd/*.json
git commit -m "$(cat <<'EOF'
docs(bdd): mark all implemented features as passing

- Batch update after final verification
- All feature tests and full suite passing

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

7. Verify all BDD JSON files are complete:

```bash
grep -r '"passes": false' docs/requirements/*-bdd/ && echo "FAIL: Some scenarios not passing" || echo "OK: All scenarios passing"
grep -r '"overallPass": false' docs/requirements/*-bdd/ && echo "FAIL: Some features not complete" || echo "OK: All features complete"
```

8. Verify coverage meets architecture targets (if coverage tool configured):

```bash
<coverage-command>
# Compare results against thresholds defined in architecture document
```

9. **Update execution plan:** Mark all features as `Done` in `docs/plans/bdd-execution-plan.md`. Add a final summary section at the bottom of the plan with total test counts, coverage results, and completion timestamp.

**If any verification fails:** Fix before proceeding. Do NOT update `passes` for features with failing tests.

### Step 9: Complete Development

**REQUIRED SUB-SKILL:** Use `superpowers:finishing-a-development-branch`

Follow that skill to present options (merge, PR, keep, discard) and clean up the worktree.

## Priority Decision Table

| Situation | Action |
|-----------|--------|
| Feature depends on shared infrastructure (e.g., HTTP client, cache config) | Verify shared infra exists in walking skeleton; if missing, implement first |
| Feature depends on another feature's output | Implement dependency feature first |
| BDD scenario requires external API stub data | Create stub/mock using the project's HTTP mock tool (from architecture doc) |
| BDD scenario is ambiguous | Stop, cross-check with PRD detail; if still unclear, ask user |
| Test is hard to write for a scenario | Check if the scenario spans multiple layers; split if needed |
| Existing test breaks during implementation | Fix immediately before continuing |
| All feature scenarios pass but full suite fails | Investigate regression, fix before committing |
| User requests to skip a feature | Mark as `Skipped` in execution plan with reason, proceed to next |

## When to Stop and Ask

**STOP immediately when:**
- BDD scenario contradicts PRD specification
- Cannot determine correct mock/stub setup from scenario description
- Implementation requires a new module not defined in architecture document
- Architecture dependency rules would be violated by the implementation approach
- Existing tests break and the cause is unclear
- A project dependency is missing from the build configuration

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

| Situation | Action |
|-----------|--------|
| Architecture doc lacks info needed for implementation | Return to Step 0.5, re-read docs; if still insufficient, stop and ask |
| BDD scenario discovered to be incomplete or ambiguous mid-implementation | Return to Step 1 review; raise with user before continuing |
| Feature dependency not yet implemented | Reorder execution plan, implement dependency feature first |
| Shared infrastructure missing from walking skeleton | Implement infra first (outside feature cycle), then resume |
| Full suite regression after committing a feature | Return to Step 4 (refactor) of the regressing feature, fix before next feature |

## Common Mistakes

### Writing production code before tests
- **Problem:** Violates TDD discipline, tests become verification-after-the-fact
- **Fix:** Delete production code, start with failing test

### Updating `passes` before final verification
- **Problem:** BDD JSON becomes inconsistent if later features cause regressions on earlier features
- **Fix:** Never update `passes` during Step 5. Only batch update in Step 8 after all features pass final verification

### Implementing multiple features in one cycle
- **Problem:** Hard to isolate failures, messy commits, unclear git history
- **Fix:** One feature per cycle, one commit per feature

### Skipping RED verification
- **Problem:** Test may pass immediately (testing existing behavior, not new feature)
- **Fix:** Always run tests and confirm they fail before implementing

### Over-engineering during GREEN phase
- **Problem:** Adding abstractions, patterns, or features not required by current test
- **Fix:** Write the minimum code to pass the failing test, refactor after GREEN

### Violating architecture layering
- **Problem:** Inner layer imports from outer layer; modules reference each other's internals
- **Fix:** Follow dependency rules from architecture document; architecture fitness function tests will catch violations

### Putting all tests as integration tests
- **Problem:** Slow test suite, violates test pyramid
- **Fix:** Unit-test core logic with mocks; integration-test only when running server or external stubs are needed

### Excluding protocol layer in integration tests (no E2E coverage)
- **Problem:** Integration tests that exclude auto-configuration (e.g., `@EnableAutoConfiguration(exclude = {McpServerAutoConfiguration.class})`) test only the inner dependency chain (Tool → Service → Client), but never verify that features are registered and reachable through the actual protocol layer. All tests pass, but the application exposes zero features to real clients.
- **Fix:** Write at least one E2E smoke test per feature that starts the full application stack (no auto-configuration exclusions), verifies the feature is discoverable through the protocol (e.g., `tools/list`, endpoint routing), and invocable end-to-end. The E2E smoke test is the only test that catches wiring/registration failures between the protocol layer and business logic.

### Hardcoding tech-specific commands
- **Problem:** Skill becomes tied to a single tech stack
- **Fix:** Always read build/test/coverage commands from architecture document and build config at session start

### Not updating execution plan status
- **Problem:** Plan document becomes stale, cannot resume sessions reliably
- **Fix:** Always update Status column in plan when starting (In Progress) and finishing (Done) a feature. Always append a row to the Progress Log at each status change

## Integration

**Upstream skills (must complete before this skill, in order):**
1. **requirement-analysis** — Produces PRD and BDD JSON files
2. **tech-stack-confirmation** — Technology decisions, ADRs
3. **project-architecture-init** — Architecture document, walking skeleton, fitness function tests, CI pipeline
4. **rules-generation** (optional) — Project coding rules in `.claude/rules/`

**Sub-skills used during execution:**
- **superpowers:using-git-worktrees** — REQUIRED: Set up isolated workspace (Step 0)
- **superpowers:test-driven-development** — Core TDD discipline for Steps 2-4
- **superpowers:systematic-debugging** — When tests fail unexpectedly
- **superpowers:verification-before-completion** — Before claiming features complete (Step 5, 8)
- **superpowers:finishing-a-development-branch** — REQUIRED: Complete development (Step 9)

**Artifact locations:**
- PRD: `docs/requirements/*-prd.md`
- BDD: `docs/requirements/*-bdd/<feature-name>.json` (updated in-place at Step 8 only)
- Architecture: `docs/architecture/architecture.md` (read-only runtime config)
- Tech stack: `docs/architecture/*-tech-stack.md` (read-only runtime config)
- **Execution plan: `docs/plans/bdd-execution-plan.md`** (generated at Step 1, updated throughout)
- Source and test paths: determined from architecture document at session start
