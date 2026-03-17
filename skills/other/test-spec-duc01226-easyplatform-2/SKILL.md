---
name: test-spec
version: 2.1.0
description: '[Testing] Generate test specifications, test cases, and coverage analysis from PBIs or codebase. Comprehensive test planning with GWT format, evidence requirements, and traceability. Triggers on: test spec, test cases, qa, test plan, test coverage, test matrix, test strategy, what to test, Given When Then, BDD.'
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Plan tests, generate specifications, create detailed test cases, and analyze coverage — from PBIs/acceptance criteria OR from codebase analysis.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` -- project patterns and structure
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Two Modes:**

| Mode              | Entry Point                     | Depth                                                    | Output                       |
| ----------------- | ------------------------------- | -------------------------------------------------------- | ---------------------------- |
| **From PBI**      | User provides PBI, story, or AC | Lighter — extract criteria, categorize, generate         | `team-artifacts/test-specs/` |
| **From Codebase** | User specifies feature/module   | Deep — analyze code, build knowledge model, traceability | `.ai/workspace/specs/`       |

**Workflow:**

0. **Business & Code Investigation** — **CRITICAL FIRST STEP.** Understand business logic, entities, and code paths BEFORE writing any test spec
1. **Test Planning** — Define scope, strategy, environments, identify test types needed
2. **Test Specification** — Extract/analyze scenarios, categorize (positive/negative/edge/security)
3. **Approval Gate** — Present test plan for user confirmation before generating cases
4. **Test Case Generation** — Create TC-{SVC}-{NNN} cases with GWT, evidence, priority
5. **Coverage Analysis** — Map cases to requirements, identify gaps, traceability matrix
6. **Validation** — Interview user to confirm coverage, priorities, test data needs

**Key Rules:**

- **⚠️ MUST READ** `.claude/skills/shared/references/module-codes.md` for TC ID formats and module codes
- **⚠️ MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing
- **⚠️ INVESTIGATE FIRST** — NEVER generate test specs without completing Phase 0 (Business & Code Investigation). You must understand the business logic and code paths before writing any test case.
- **⚠️ ALWAYS PLAN TASKS** — Use `TaskCreate` to break work into granular todo items BEFORE starting. Must include a final review task.
- Every test case must have `Evidence: {FilePath}:{LineNumber}`
- NEVER proceed past approval gate without explicit user confirmation
- Minimum 3 test categories: positive, negative, edge cases

---

## Task Planning (MANDATORY)

Before starting ANY work, create todo tasks using `TaskCreate`:

1. Create tasks for each phase you'll execute (Phase 0 through Phase F as needed)
2. Break large phases into sub-tasks (e.g., "Investigate entities", "Read business docs", "Generate test cases for CheckIns")
3. **MUST include a final review task** — verify all test cases have evidence, IDs are correct, coverage is complete, and no placeholders remain
4. Mark each task `in_progress` before starting, `completed` when done
5. Only ONE task `in_progress` at a time

---

## Phase 0: Business & Code Investigation (CRITICAL — DO NOT SKIP)

**Purpose:** Understand the business logic, code structure, and domain context BEFORE writing any test spec. Test specs written without this understanding will miss critical scenarios and contain incorrect assumptions.

### Step 1: Read Business Feature Documentation

Locate and read the relevant business docs in `docs/business-features/`:

| Service  | Docs Path                          |
| -------- | ---------------------------------- |
| ServiceB | `docs/business-features/ServiceB/` |
| ServiceA | `docs/business-features/ServiceA/` |
| ServiceC | `docs/business-features/ServiceC/` |
| ServiceD | `docs/business-features/ServiceD/` |
| Auth     | `docs/business-features/Accounts/` |

Read: `INDEX.md` → relevant `detailed-features/*.md` → `API-REFERENCE.md`

### Step 2: Investigate Code — Entities, Commands, Queries, Handlers

Search and read ALL related code artifacts:

```
grep/glob for the feature name in:
├── Entities/           → Domain models, business rules, validation logic
├── UseCaseCommands/    → Command + Result + Handler (side effects, validation)
├── UseCaseQueries/     → Query + Result + Handler (data retrieval, filtering)
├── UseCaseEvents/      → Entity Event Handlers (notifications, sync, side effects)
├── BackgroundJobs/     → Scheduled tasks, recurring jobs
├── Consumers/          → Message bus consumers (cross-service events)
├── Repositories/       → Data access, query extensions
└── Controllers/        → API endpoints, request/response contracts
```

**For each file found, note:**

- What business rule does it enforce?
- What validation does it perform?
- What side effects does it trigger?
- What edge cases exist in the logic?

### Step 3: Write Investigation Notes to Temp Report

**MANDATORY IMPORTANT MUST** create a temp investigation report BEFORE generating test specs:

```
plans/reports/test-investigation-{YYMMDD}-{HHMM}-{feature-slug}.md
```

**Report structure:**

```markdown
# Test Investigation: {Feature Name}

## Business Context

- Summary of business requirements from docs
- Key business rules identified

## Code Artifacts Found

| Type           | File   | Key Logic                  | Test-Relevant Notes         |
| -------------- | ------ | -------------------------- | --------------------------- |
| Entity         | {path} | {business rules}           | {edge cases}                |
| Command        | {path} | {validation, side effects} | {error paths}               |
| Query          | {path} | {filtering, permissions}   | {empty results, pagination} |
| Event Handler  | {path} | {side effects triggered}   | {failure scenarios}         |
| Background Job | {path} | {scheduling, batch logic}  | {concurrency, idempotency}  |

## Business Rules to Test

1. {Rule from entity/command — with file:line evidence}
2. {Rule from validation — with file:line evidence}

## Identified Edge Cases

1. {Edge case from code analysis}
2. {Edge case from business doc gaps}

## Cross-Service Dependencies

- {Service} via {message bus event} — {what to verify}

## Open Questions

- {Anything unclear from investigation}
```

**This report becomes the foundation for all subsequent phases.** Reference it throughout test spec generation.

### Phase 0 Completion Criteria

- [ ] Read ALL relevant business feature docs
- [ ] Found and analyzed ALL entities related to the feature
- [ ] Found and analyzed ALL commands/queries/event-handlers/background-jobs
- [ ] Investigation report written to `plans/reports/`
- [ ] Business rules listed with `file:line` evidence
- [ ] Edge cases identified from code analysis

**ONLY proceed to Phase A after completing ALL criteria above.**

---

## Phase A: Test Planning

Define scope and strategy (using Phase 0 investigation report as input):

1. Reference the investigation report from `plans/reports/test-investigation-*.md`
2. Define test types needed based on code artifacts found (unit, integration, E2E, regression, smoke, performance)
3. Define test environments and data needs
4. Plan regression test suite impact
5. Estimate testing effort

### Test Categories

| Category    | Purpose                 |
| ----------- | ----------------------- |
| Positive    | Happy path verification |
| Negative    | Error handling          |
| Boundary    | Edge values             |
| Integration | Component interaction   |
| Security    | Auth, injection, XSS    |

---

## Phase B: Test Specification

### From PBI Mode (lighter)

1. Extract acceptance criteria from PBI/stories
2. Identify test scenarios (positive/negative/edge)
3. Define coverage requirements and test data needs
4. Create test spec artifact

### From Codebase Mode (deep analysis)

Build structured knowledge model in `.ai/workspace/analysis/[feature-name].analysis.md`:

1. **Discovery** — Search all feature-related files (entities, commands, queries, event handlers, controllers, BG jobs, consumers, components)
2. **Systematic analysis** — For each file document: `coverageTargets`, `edgeCases`, `businessScenarios`, `detailedTestCases`
3. **Overall analysis** — Map end-to-end workflows, business logic, integration points, cross-service dependencies

### Spec Structure

1. Feature Overview (epic, user stories, acceptance criteria, business requirements, roles/permissions)
2. Entity Relationship Diagram (core entities, mermaid diagram)
3. Test Scope and Categories
4. Test Scenarios (high-level)
5. Coverage Requirements
6. Test Data Needs

---

## Phase C: Approval Gate (MANDATORY)

**CRITICAL:** Present test plan with coverage analysis for explicit user approval. **DO NOT** proceed to case generation without it.

---

## Phase D: Test Case Generation

Generate test cases in **4 priority groups**: Critical (P0), High (P1), Medium (P2), Low (P3).

### Test Case Format

```markdown
#### TC-{SVC}-{NNN}: {Descriptive title}

- **Priority:** P0 | P1 | P2 | P3
- **Type:** Positive | Negative | Boundary | Integration | Security

**Preconditions:** {Setup required}
**Test Data:** {Data requirements}

**Given** {precondition}
**And** {additional context}
**When** {action performed}
**Then** the system should:

- {Expected outcome 1}
- {Expected outcome 2}

**Evidence:** `{FilePath}:{LineNumber}`
```

### Component Interaction Flow (for deep mode)

```
Frontend → Controller → Command/Query → Repository → Event → Consumer
```

### Edge Case Categories

**Input Validation:** Empty/null, boundary values (min, max, min-1, max+1), invalid formats, SQL injection, XSS payloads

**State-Based:** First use (empty state), maximum capacity, concurrent access, session timeout

**Integration:** Service unavailable, network timeout, partial data response, rate limiting

---

## Phase E: Coverage Analysis

1. Map test cases to requirements (bidirectional traceability matrix)
2. Identify coverage gaps
3. Calculate coverage percentage per category
4. Multi-dimensional coverage validation

### Traceability Matrix (for deep mode)

Bidirectional mapping: Test Case ↔ Business Requirement ↔ Source Component

---

## Phase F: Validation (MANDATORY)

After generating test cases, validate with user:

### Question Categories

| Category        | Example Question                                            |
| --------------- | ----------------------------------------------------------- |
| **Coverage**    | "Is the test coverage adequate for critical paths?"         |
| **Priority**    | "Which test categories should be prioritized?"              |
| **Test Data**   | "Are the test data requirements realistic and available?"   |
| **Edge Cases**  | "Any additional edge cases or error scenarios to consider?" |
| **Integration** | "Are cross-service integration points covered?"             |

### Process

1. Generate 2-4 questions focused on coverage completeness, priorities, and test data
2. Use `AskUserQuestion` tool to interview
3. Document in test spec under `## Validation Summary`
4. Update test spec based on answers

**This step is NOT optional.**

---

## Output Conventions

### File Naming

```
team-artifacts/test-specs/{YYMMDD}-testspec-{feature}.md        # From PBI mode
.ai/workspace/specs/[feature-name].ai_spec_doc.md              # From Codebase mode
```

### ID Patterns

Refer to `shared/references/module-codes.md` for full code tables.

- **Spec-level:** `TS-{SVC}-{NNN}` (e.g., TS-GRO-001)
- **Test case:** `TC-{SVC}-{NNN}` (e.g., TC-GRO-015)

---

## Quality Checklist

Before completing test artifacts:

- [ ] Every test case has `TC-{SVC}-{NNN}` ID
- [ ] Every test case has `Evidence` field with `file:line`
- [ ] Test summary counts match actual test case count
- [ ] At least 3 categories: positive, negative, edge
- [ ] Regression impact identified
- [ ] Test data requirements documented
- [ ] No template placeholders remain

---

## Related

- `test-specs-docs` — Write test specs to `docs/test-specs/` (permanent docs)
- `qc-specialist` — Quality gates after test case generation
- `tasks-test-generation` — Autonomous unit/integration test code generation
- `integration-test` — the project CQRS integration test code generation
