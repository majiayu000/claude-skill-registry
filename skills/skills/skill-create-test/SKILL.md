---
name: skill-create-test
description: "Design-first test creation workflow with validation"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
metadata:
  type: implementation
  agents:
    - -test-designer
    - -test-reviewer
---

# Skill: Create Tests

This skill implements a design-first test creation workflow for Go codebases. You will design a comprehensive test plan before writing any code, generate tests following the plan, and validate them for quality and determinism.

The workflow ensures proper test coverage by classifying tests, enforcing deterministic execution, and validating documentation before implementation.

## Prerequisites

- Files or folders to test identified
- Understanding of Go testing patterns
- Go 1.25+ environment
- Familiarity with test classification types

## Overview

1. Receive and analyze input files/folders
2. Design test plan (invoke -test-designer agent)
3. Ask "Ready to Build?" - wait for confirmation
4. Generate test files following the plan
5. Validate tests (invoke -test-reviewer agent)
6. Update test index

## Step 1: Receive Input

User drags files or folders into the conversation.

### Action

Read provided files to understand:
- Package purpose and public API
- Existing tests (if any)
- Dependencies and complexity

## Step 2: Design Test Plan

Invoke the -test-designer agent to create a comprehensive test plan.

### Action

Use the -test-designer agent with the provided files to produce:
- Behaviors to test with classifications (unit/integration/simulation/e2e/benchmark)
- Edge cases and error paths
- Test naming and structure
- Mock requirements and infrastructure needs

## Step 3: Ask "Ready to Build?"

**MANDATORY: Never generate tests without explicit confirmation.**

Present the test plan summary and ask:

```
## Test Plan Summary

### Behaviors to Test
[List from test designer]

### Test Classifications
- Unit Tests: X
- Integration Tests: Y
- Simulation Tests: Z
- E2E Tests: W

### Estimated Test Files
[File list with naming]

**Ready to Build?** (yes/no)
```

Wait for explicit "yes" before proceeding.

## Step 4: Generate Tests

Create test files following the approved plan.

### Execution Environment

- Language: **Go 1.25+**
- Testing framework: Go `testing` package
- Style: idiomatic Go, table-driven tests where appropriate

### Test Categories

#### Unit Tests

Small, isolated, table-driven when appropriate.

**Core Principles:**
- **One behavior or aspect per test function**
- Include success, edge, and error paths
- Must demonstrate primary usage patterns so tests can serve as examples

**Placement Rules:**
- <250 LOC + <10 functions → `*_test.go` in same directory
- Otherwise → `tests/` directory

**Size Limits:**
- Large test files >500 LOC must be split
- Keep total tests per folder manageable; partition >100 files
- **CRITICAL**: Always run `wc -l` after generating to verify line count

**Asciidoc Tags (for examples):**

```go
// tag::<name>[]
// end::<name>[]
```

#### Integration Tests

Tests using real AWS infrastructure.

**Filename Pattern:** `integration_<name>_test.go`

**Requirements:**
- Use real AWS infra via `go-core/managers/*`
- Full provision + teardown to avoid cost leaks
- Verify all resources are cleaned up

**Local AWS Simulators:**
- `dynamodb_local.go` - DynamoDB local testing
- `sqs_local.go` - SQS local testing
- `s3_local.go` - S3 local testing
- `dynamodb.go` - Real table simplification

#### Simulation Tests

Advanced driver tests pushing many events for different scenarios.

**Filename Pattern:** `simulation_<name>_test.go`

**Definition:** A simulation uses an advanced driver that pushes many events, allowing different tests to realize different scenarios.

**Use Cases:**
- Multi-step workflows
- Timed logic
- State machines

**Determinism Requirements:**
- Mock clocks for time control
- Fixed random seeds
- Ordered events

**Simulator Locations:**
- `tests/simulator.go`
- `tests/simulator/*`

#### E2E Tests

Multi-component orchestration tests.

**Filename Pattern:** `e2e_<name>_test.go` (**IMPORTANT:** inside a e2e folder and package with tag conditional compile so it won't compile by default)

**Scope:**
- Analytics systems
- Optimization engines
- Message processing pipelines

**Requirements:**
- Deterministic outcomes and consistency
- Validate retries, recovery, and state
- Multi-component interactions

**Flexibility:** E2E tests can be structured as simulation tests or integration tests, depending on whether real infrastructure is involved.

#### Benchmarks

Performance measurement tests.

**Restrictions:**
- Only for local-only logic (no AWS cost)
- Measure throughput/latency and memory

**Cloud Cost Warning:**
If real AWS resources needed, you MUST ask:
**"This benchmark incurs cloud cost. Proceed?"**

Wait for explicit confirmation before proceeding.

### Deterministic Execution

All tests must follow strict determinism rules.

**Forbidden Patterns:**
- No timing assumptions
- No sleeps for synchronization
- No race conditions
- No goroutine ordering dependencies
- No nondeterminism

**When Nondeterminism is Expected:**
- If nondeterministic by design: assert nondeterministic properties
- If deterministic code behaves nondeterministically: identify production bug

### Flakiness Prevention

**Treatment Rule:** Conceptually treat each generated test as if run **multiple times**.

**Requirements:**
- Ensure the result is consistent and stable across runs
- Report and address inconsistencies in test logic or production code
- No timing-dependent assertions

### Error Injection

Mandatory when testing retries/resilience.

**Inject These Failure Types:**

1. **Hard Failures:**
   - Panic conditions
   - Corrupt data scenarios
   - Unrecoverable errors

2. **Retryable AWS Errors:**
   - Throttling responses
   - Timeouts
   - Batch partial failures

3. **Workflow-Level Failures:**
   - Poison messages
   - Retry exhaustion
   - Dead letter queue routing

**AWS Error Injection Tools:**
- `roundtripper_sqs.go` - SQS error injection
- `roundtripper_dynamodb.go` - DynamoDB error injection

**Verification Requirements:**
- Correct retry count/backoff
- Correct terminal states
- E2e remains consistent

### Naming Rules

All test files must follow these naming conventions:

| Test Type   | Pattern                          | Example                      |
|-------------|----------------------------------|------------------------------|
| Unit        | `foo_bar_test.go`                | `user_service_test.go`       |
| Integration | `integration_<name>_test.go`     | `integration_dynamo_test.go` |
| Simulation  | `simulation_<name>_test.go`      | `simulation_workflow_test.go`|
| E2E         | `e2e_<name>_test.go`             | `e2e_analytics_test.go`|

**Rules:**
- All lowercase
- Use underscores as separators
- Descriptive names reflecting test scope

## Step 5: Document Tests

### Documentation Decision Table

| Test Type       | Complexity | Required Docs                                     |
|-----------------|------------|---------------------------------------------------|
| Unit (simple)   | 1-2 steps  | Summary line only                                 |
| Unit (behavior) | 3+ steps   | Summary + Diagram + Test Parameters + Assertions  |
| Unit (edge/bug) | boundary   | Summary + Inline decision (`→ RESULT`)            |
| Simulation      | multi-step | Summary + Scenario Box + Hierarchy + Timeline     |
| Integration     | multi-comp | File Header + Per-test flow diagrams              |
| Bug repro       | fix verify | Summary + "Without fix"/"With fix" comparison     |

### Documentation Update Rules

- **Do NOT** update documentation on each test failure during debugging
- **DO** update documentation when:
  1. Test passes after code/test changes
  2. Test behavior or parameters changed
  3. New assertions added or removed
- **Workflow**: Fix test → Verify passes → Update docs to match final state
- Documentation must reflect the **passing test**, not intermediate failed states

### Required for ALL Tests

**Summary line**: First line of doc comment, starts with verb:
- `validates` - for behavior verification
- `demonstrates` - for example/usage tests
- `verifies` - for state/condition checks
- `exposes` - for bug reproduction

### Add When Helpful

- **Diagram**: Data flow, state transitions, timelines, component design
- **Test Parameters**: Bullet list of key config values
- **Assertions**: Bullet list of expected outcomes
- **Inline decision**: `condition → RESULT` for boundary tests

### For File Groups

**File Header**: `═══` separator + group description + optional summary table

### ASCII Building Blocks

```
Box:       ┌─┬─┐ │ ├─┤ └─┴─┘
Timeline:  [═══════════)  or  ──────E1──────E2──────
Hierarchy: ├── └──
Arrows:    → ← ↑ ↓ ↔ ⇒ ⇐
Table:     ┌───┬───┐ │ │ ├───┼───┤ └───┴───┘
Status:    ✓ (pass)  ✗ (fail)  → PROCESSED  → DROPPED
Interval:  [start, end)  (half-open)
Separator: ═══ (major)  ─── (minor)
Gantt:     ▓▓▓▓ (active)  ░░░░ (waiting)  ──── (idle)
State:     ○ (initial)  ● (current)  ◎ (final)
```

### Diagram Types

**Component Design:**

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Component  │────▶│  Component  │────▶│  Component  │
│      A      │     │      B      │     │      C      │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│   Store     │     │   Queue     │
└─────────────┘     └─────────────┘
```

**Gantt Chart:**

```
Task         T0    T1    T2    T3    T4    T5
─────────────────────────────────────────────────
Task A       ▓▓▓▓▓▓▓▓▓▓░░░░░░
Task B             ░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓
Task C                       ░░░░▓▓▓▓▓▓▓▓
─────────────────────────────────────────────────
```

**Sequence Diagram:**

```
  Client          Server          Database
     │               │               │
     │──── request ──▶               │
     │               │── query ──────▶
     │               │◀── result ────│
     │◀── response ──│               │
```

**State Machine:**

```
        ┌──────────────────────────────┐
        ▼                              │
    ○ IDLE ──event──▶ RUNNING ──done──▶ ● COMPLETE
        │                 │
        │                 │──error──▶ FAILED
        └──────── retry ◀──────────────┘
```

**Decision Tree:**

```
                ┌─────────┐
                │ Input   │
                └────┬────┘
                     ▼
              ┌──────────────┐
              │ Condition A? │
              └──────┬───────┘
             yes/    \no
              ▼       ▼
         ┌───────┐ ┌───────┐
         │ Path1 │ │ Path2 │
         └───────┘ └───────┘
```

**Data Flow / Pipeline:**

```
Input ──▶ [Transform A] ──▶ [Filter B] ──▶ [Aggregate C] ──▶ Output
               │                                │
               └────────── errors ──────────────┘
```

### Documentation Templates

**Unit Test (simple):**

```go
// TestFoo validates [one-sentence behavior description].
func TestFoo(t *testing.T) {
    // ...
}
```

**Unit Test (behavior):**

```go
// TestFoo validates [behavior] when [condition].
//
// Scenario:
// ───────────────────────────────────────────────
//   [ASCII diagram: timeline, flow, or state]
// ───────────────────────────────────────────────
//
// Test Parameters:
//   - Config1: Value1
//   - Config2: Value2
//
// Assertions:
//   - Expected outcome 1
//   - Expected outcome 2
func TestFoo(t *testing.T) {
    // ...
}
```

**Unit Test (edge/boundary):**

```go
// TestFoo validates [edge condition].
//
// ═══════════════════════════════════════════════
// Config: Key = Value
//
// Input → condition check → RESULT
// ═══════════════════════════════════════════════
func TestFoo(t *testing.T) {
    // ...
}
```

**Simulation Test:**

```go
// TestFoo validates [simulation scenario].
//
// Scenario Overview:
// ───────────────────────────────────────────────
//   ┌─────────────────────────────────────────┐
//   │         [System Description]            │
//   │  Input → Component → Output             │
//   └─────────────────────────────────────────┘
// ───────────────────────────────────────────────
//
// Component Hierarchy:
//   root
//   ├── child_a
//   └── child_b
//
// ───────────────────────────────────────────────
//
// Timeline:
//   Step    Scenario              Expected
//   ────────────────────────────────────────────
//   0-1     Initial state         No alerts
//   1-2     Condition changes     Alert triggered
// ───────────────────────────────────────────────
func TestFoo(t *testing.T) {
    // ...
}
```

**Integration Test:**

```go
// TestIntegrationFoo validates [integration scenario].
//
// Infrastructure:
// ───────────────────────────────────────────────
//   ┌─────────┐     ┌─────────┐     ┌─────────┐
//   │ Service │────▶│  Queue  │────▶│  Store  │
//   └─────────┘     └─────────┘     └─────────┘
// ───────────────────────────────────────────────
//
// Provision:
//   - DynamoDB table: test-table
//   - SQS queue: test-queue
//
// Teardown:
//   - All resources deleted on completion
func TestIntegrationFoo(t *testing.T) {
    // ...
}
```

**File Group Header:**

```go
// ═══════════════════════════════════════════════
// [Test Group Name]
//
// [Brief description of what this group tests]
//
// Summary:
// ┌──────┬────────────────────────┬──────────┐
// │ ID   │ Description            │ Status   │
// ├──────┼────────────────────────┼──────────┤
// │ T001 │ Scenario one           │ PASS     │
// │ T002 │ Scenario two           │ PASS     │
// └──────┴────────────────────────┴──────────┘
// ═══════════════════════════════════════════════
```

**Bug Reproduction Test:**

```go
// TestBugFoo exposes [bug description].
//
// Without fix:
// ───────────────────────────────────────────────
//   Input → [expected path] → ✗ [actual wrong result]
// ───────────────────────────────────────────────
//
// With fix:
// ───────────────────────────────────────────────
//   Input → [expected path] → ✓ [correct result]
// ───────────────────────────────────────────────
func TestBugFoo(t *testing.T) {
    // ...
}
```

## Step 6: Validate Tests

Invoke the -test-reviewer agent to validate generated tests.

### Action

Use -test-reviewer to check:
- Determinism compliance
- Flakiness risk
- Documentation completeness
- Structure and naming

Address any issues identified before proceeding.

### Failure Analysis

When tests fail, do not assume the test is wrong or production code is correct by default. Diagnose root cause and propose corrections for test logic, production code, or both.

## Step 7: Update Index

Update `tests/_test_index.md` BEFORE generating test files.

### Index Format

| name | description | type | group | status |
|------|-------------|------|-------|--------|

### Index Rules

- Maximum 500 rows per index file
- Update BEFORE generating or modifying test files
- Include all test functions, not just files

### Example Index Entry

| name | description | type | group | status |
|------|-------------|------|-------|--------|
| TestUserCreate | validates user creation with valid input | unit | user_service | pass |
| TestUserCreate_InvalidEmail | validates rejection of invalid email | unit | user_service | pass |
| integration_dynamo_crud | verifies DynamoDB CRUD operations | integration | storage | pass |
| simulation_order_workflow | validates multi-step order processing | simulation | orders | pass |

## Verification Checklist

Before completing, verify all items:

- [ ] Test plan designed before implementation
- [ ] User confirmed "Ready to Build"
- [ ] Tests follow naming conventions
- [ ] Documentation includes summary lines
- [ ] Line counts within limits (<500 LOC per file)
- [ ] Index file updated BEFORE test generation
- [ ] Reviewer validation passed
- [ ] All tests run with `wc -l` verified
- [ ] Determinism rules followed
- [ ] Error injection implemented where needed
- [ ] All resources cleaned up in integration tests
- [ ] No flakiness detected

## Build Phase Completion

After all tests are generated and validated:
- Generate valid Go test files with proper naming/placement
- Verify determinism and run `wc -l` to check line counts
- Ensure tests are correct, idiomatic Go, deterministic, and maintainable
- Ask: "Do you want deeper performance/memory optimization review?"
