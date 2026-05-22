---
name: faion-sdd
user-invocable: false
description: "SDD orchestrator: Specification-Driven Development workflow. Specifications, design docs, implementation plans, constitutions, task lifecycle (backlog→done), quality gates, reflexion learning, pattern/mistake memory."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# SDD Domain Skill

## Agents

| Agent | When to Use |
|-------|-------------|
| `faion-task-executor-agent` | Execute SDD tasks autonomously from task files |
| `faion-task-creator-agent` | Create detailed TASK_*.md files from specs |
| `faion-sdd-reviewer-agent` | Quality gate reviews (modes: spec, design, plan, tasks) |
| `faion-hallucination-checker-agent` | Validate task completion claims with evidence |

**Reviewer Mode Mapping:**
| Mode | Replaces | Purpose |
|------|----------|---------|
| spec | faion-sdd-reviewer-agent (mode: spec) | Review specs for completeness and clarity |
| design | faion-sdd-reviewer-agent (mode: design) | Review design docs for architecture decisions |
| plan | faion-sdd-reviewer-agent (mode: plan) | Review impl-plans for 100k token compliance |
| tasks | faion-sdd-reviewer-agent (mode: tasks) | Multi-pass review of all tasks for a feature |


**Communication: User's language. Docs/code: English.**

## Purpose

Orchestrates the complete SDD (Specification-Driven Development) workflow. This domain skill consolidates all SDD-related functionality into a single orchestrator.

## Philosophy

**"Intent is the source of truth"** — specification is the main artifact, code is just its implementation.

## 3-Layer Architecture

```
Layer 1: Domain Skills (this) ─ orchestrators
    ↓ call
Layer 2: Agents ─ executors
    ↓ use
Layer 3: Technical Skills ─ tools
```

## Workflow Overview

```
CONSTITUTION → SPEC → DESIGN → IMPL-PLAN → TASKS → EXECUTE → DONE
      ↓          ↓        ↓         ↓          ↓        ↓        ↓
   project    feature  technical  100k rule  atomic   agent    learn
   principles  intent   approach  compliance  units  execution  reflect
```

---

# Section 1: Writing Constitutions

## Philosophy

**Constitution.md** — immutable project principles for ALL features.

**Two modes:**
1. **Existing Project** → codebase analysis
2. **New Project** → Socratic dialogue

## MODE 1: Existing Project

**Workflow:** Detect → Analyze Structure → Tech Stack → Patterns → Draft → Review

**Analyze:**
- Directory layout, CLAUDE.md, README.md
- Config files (pyproject.toml, package.json)
- Architecture patterns, naming, linters, testing

**Present findings:**
```markdown
**Analysis:**
1. Tech: Python 3.11, Django 4.2, PostgreSQL
2. Architecture: Layered (views → services → models)
3. Standards: black + isort + flake8
Does this match? What to change?
```

## MODE 2: New Project

**Workflow:** Vision → Tech Choices → Architecture → Standards → Draft → Review

### Vision (Socratic)
"Tell me about the project. What problem does it solve?"

Apply Five Whys to get to real need.

### Tech Choices (Alternatives)

For each decision — present A/B/C with pros/cons:
- Backend: Django vs FastAPI vs NestJS
- Database: PostgreSQL vs MongoDB vs SQLite

### Architecture (Trade-offs)
- Monolith vs Microservices
- REST vs GraphQL
- ORM vs Raw SQL

### Standards
- Linter, formatter, type hints
- Testing coverage, CI/CD
- Git conventions

## Constitution Save

```bash
mkdir -p aidocs/sdd/{project}
# Write constitution.md
```

Create CLAUDE.md navigation hub.

## Anti-patterns

- ❌ Copying without understanding
- ❌ Over-engineering at start
- ❌ Ignoring team expertise

**Output:** `aidocs/sdd/{project}/constitution.md` → Next: Writing Specifications

---

# Section 2: Writing Specifications

## Philosophy

- **Intent is source of truth** — spec is main artifact
- **Socratic dialogue** — user formulates requirements through questions
- **Brainstorming** — iterative refinement via alternatives

## Workflow

```
BRAINSTORM → RESEARCH → CLARIFY → DRAFT → REVIEW → SAVE
```

## Phase 1: Brainstorming

Start: "Tell me about the problem. Who suffers and how?"

**Five Whys** — for each answer ask "Why?":
```
"Need export" → Why? → "Managers ask" → Why? → "No access" → Real problem: UX
```

**Alternatives** — for each idea:
```markdown
**A:** {approach 1} ✅ Pros ❌ Cons
**B:** {approach 2} ✅ Pros ❌ Cons
Which is closer?
```

**Challenge assumptions:**
- "Is this needed for v1?"
- "What if we DON'T do this?"
- "What exists in codebase?"

## Phase 2: Research Codebase

Search: `Glob **/models.py`, `Grep class.*Model`, `Glob aidocs/sdd/**/spec.md`

Share findings: "Found existing export in services.py. Does this affect approach?"

## Phase 3: Clarify Details

**User stories workshop:**
```markdown
As {role}, I want {goal}, so that {benefit}.
- How often?
- What happens if can't do this?
```

**Edge cases through questions** (not assumptions):
- "What if data invalid?"
- "What if 1000+ records?"
- "What if service unavailable?"

## Phase 4: Draft Section by Section

Each section → show → validate → next:

1. Problem Statement → "Correct?"
2. User Stories with AC → "Complete?"
3. Functional Requirements → "Anything redundant?"
4. Out of Scope → "Agree with boundaries?"

## Phase 5: Review

**Checklist:**
- [ ] Problem clear
- [ ] User Stories specific
- [ ] Requirements testable
- [ ] Out of Scope defined

Call `faion-sdd-reviewer-agent (mode: spec)` agent before save.

## Phase 6: Save

**New feature:** `aidocs/sdd/{project}/features/backlog/{NN}-{feature}/spec.md`
**Active feature:** update existing spec.md

Create CLAUDE.md navigation hub in feature directory.

## Anti-patterns

- ❌ Assumptions instead of questions
- ❌ Solution before problem
- ❌ Large blocks without validation
- ❌ Ignoring "I don't know"

**Output:** `spec.md` → Next: Writing Design Documents

---

# Section 3: Writing Design Documents

## Purpose

Creates design.md for a feature based on:
1. Approved spec.md
2. Codebase analysis
3. Project constitution

## Prerequisites

**Required files:**
1. `spec.md` exists with status `approved`
2. Project `constitution.md` exists at `aidocs/sdd/{project}/constitution.md`
3. Project `contracts.md` exists at `aidocs/sdd/{project}/contracts.md` (for API features)

**If constitution.md doesn't exist:** Use Section 1 to create it first.
**If contracts.md doesn't exist:** Use `faion-api-designer-agent` agent with MODE=init.

## Workflow

### Phase 1: Read Specification

Read spec.md completely and extract:
- Problem Statement
- User Stories
- Functional Requirements
- API Contract (if present)
- Data Model (if present)
- Out of Scope

### Phase 2: Read Constitution

Read project principles from constitution.md and extract:
- Architecture patterns
- Code standards
- Testing requirements

### Phase 2.5: Read API Contracts (if API feature)

Read contracts.md and extract:
- Relevant endpoint definitions
- Request/response schemas
- Auth requirements
- Error format standard

**IMPORTANT:** Do NOT redefine API endpoints in design.md. Reference contracts.md instead:
```markdown
## API Endpoints

This feature implements endpoints from [contracts.md](../../contracts.md):
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
```

### Phase 3: Research Codebase

Use Grep and Glob tools to find related code:
- Similar models
- Similar services
- Similar views
- Existing patterns

Determine:
- Which components can be reused
- Which patterns are in use
- Where to place new code

### Phase 4: Architecture Decisions

For each key decision:
1. Define context - what problem are we solving
2. List options - minimum 2 alternatives
3. Choose solution - which and why
4. Document rationale - reasoning behind choice

### Phase 5: Define Technical Approach

Define:
1. **Components** - new components, interactions, diagrams if complex
2. **Data Flow** - data path through system, validation points, error handling
3. **Files** - CREATE and MODIFY lists with scope

### Phase 6: Define Testing Strategy

Based on constitution:
1. Unit tests - isolated testing targets
2. Integration tests - flow coverage
3. Test data - required fixtures

### Phase 7: Identify Risks

For each risk document:
- Risk description
- Impact (High/Medium/Low)
- Mitigation strategy

### Phase 8: Review with User

Present key decisions:
1. Architecture Decisions - agreement check
2. Technical Approach - better alternatives
3. Risks - completeness check

### Phase 9: Agent Review

Call `faion-sdd-reviewer-agent (mode: design)` agent before saving.

The agent checks:
- FR coverage (all requirements addressed)
- AD structure (context, options, rationale)
- Constitution compliance
- Files list completeness
- Technical correctness

### Phase 10: Save Design

Save design.md to feature directory: `{feature_path}/design.md`

## Architecture Decision Template

```markdown
### AD-{N}: {Decision Name}

**Context:**
{Problem being solved and relevant context}

**Options:**
- **A: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}
- **B: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}

**Decision:** {Chosen solution}

**Rationale:** {Why this solution, influencing factors}

**Failed Attempts:** {Optional - approaches tried and rejected}
```

## Files Section Format

```markdown
### Files

app/applications/{app}/models.py           # MODIFY - add {Model}
app/applications/{app}/services.py         # MODIFY - add {Service}
app/applications/{app}/views.py            # MODIFY - add {ViewSet}
app/applications/{app}/serializers.py      # MODIFY - add {Serializer}
app/applications/{app}/tests/test_{x}.py   # CREATE - tests for {x}
```

## Checklist Before Completion

- All FR from spec.md covered
- Architecture Decisions have rationale
- Files list is complete
- Testing strategy defined
- Risks identified
- Follows constitution
- API endpoints reference contracts.md (not redefined)
- User approved

**Output:** `design.md` → Next: Writing Implementation Plans

---

# Section 4: Writing Implementation Plans

## Key Principle

**Each task MUST fit 100k token context** = atomic, single-agent executable.

## Workflow

```
LOAD CONTEXT → ANALYZE COMPLEXITY → DEFINE WORK UNITS → APPLY 100k RULE → DEPENDENCIES → DRAFT → REVIEW → SAVE
```

## Phase 1: Load Context

Read: `constitution.md`, `spec.md`, `design.md`

## Phase 2: Analyze Complexity

For each file in design.md:

| File | Action | Complexity | Est. Tokens |
|------|--------|------------|-------------|
| models.py | CREATE | High | 40k |
| services.py | CREATE | High | 50k |

**Factors:** LOC, dependencies, business logic, tests

## Phase 3: Define Work Units

Group related work:
```markdown
## Work Unit 1: Data Layer
- models.py (CREATE)
Est: 40k tokens
```

## Phase 4: Apply 100k Rule

```
Research: ~20k (read existing code)
Task file: ~5k
Implementation: ~50k
Buffer: ~25k
TOTAL < 100k
```

**If > 100k:** Split into smaller tasks.

## Phase 5: Dependencies

| Task | Depends On | Enables |
|------|------------|---------|
| TASK_001 | — | TASK_003 |
| TASK_002 | — | TASK_003 |
| TASK_003 | 001, 002 | — |

Rules: No cycles, maximize parallelization.

## Phase 6: Draft

Show section by section:
- Overview (total tasks, critical path, est. tokens)
- Tasks list (files, deps, FR/AD coverage, AC)
- Execution order (phases, parallel/sequential)

## Phase 7: Review

Call `faion-sdd-reviewer-agent (mode: plan)` agent. Checks: 100k compliance, deps, coverage.

## Phase 8: Save

`aidocs/sdd/{project}/features/{feature}/implementation-plan.md`

## Token Estimation Guide

| Component | Tokens |
|-----------|--------|
| Django model simple | 5-10k |
| Django model complex | 15-25k |
| Service class | 20-40k |
| ViewSet | 15-30k |
| Test file | 20-40k |

**Rule:** If uncertain, estimate higher and split.

**Output:** `implementation-plan.md` → Next: Task Creation (via faion-sdd-domain-skill)

---

# Agents Called

| Agent | Purpose |
|-------|---------|
| faion-sdd-reviewer-agent (mode: spec) | Review spec before save |
| faion-sdd-reviewer-agent (mode: design) | Review design for architecture decisions |
| faion-sdd-reviewer-agent (mode: plan) | Review impl-plan for 100k token compliance |
| faion-task-creator-agent | Create individual tasks |
| faion-task-executor-agent | Execute tasks autonomously |
| faion-sdd-reviewer-agent (mode: tasks) | Review completed tasks |
| faion-hallucination-checker-agent | Verify task completion with evidence |

---

# Directory Structure

```
aidocs/sdd/{project}/
├── constitution.md                    # Project principles (Section 1)
├── contracts.md                       # API contracts
├── roadmap.md                         # Milestones
└── features/
    ├── backlog/                       # Features waiting for grooming
    ├── todo/                          # Features ready for execution
    ├── in-progress/                   # Features being worked on
    └── done/                          # Completed features
        └── {NN}-{feature}/
            ├── spec.md                # WHAT and WHY (Section 2)
            ├── design.md              # HOW (Section 3)
            ├── implementation-plan.md # Tasks breakdown (Section 4)
            └── tasks/
                ├── backlog/
                ├── todo/
                ├── in-progress/
                └── done/
```

---

# Section 5: Task Creation

## Purpose

Create implementation tasks from SDD documents using the `faion-task-creator-agent` agent.

## Modes

### SDD Mode (Primary)
When project/feature specified:
1. Load spec, design, implementation-plan
2. Verify documents approved
3. Create tasks per implementation-plan
4. Review with faion-sdd-reviewer-agent (mode: tasks)

### Free Mode (Legacy)
When description provided:
1. Clarify requirements with user
2. Research codebase
3. Plan task structure
4. Create tasks

## Workflow

```
1. Load SDD documents
   ↓
2. Verify: spec approved? design approved?
   ↓
3. Check/create implementation-plan
   ↓
4. For each task in plan:
   → Call faion-task-creator-agent agent
   ↓
5. Run faion-sdd-reviewer-agent (mode: tasks) (4-pass)
   ↓
6. Report results
```

## Document Verification

Check these files exist and are approved:
```
aidocs/sdd/{project}/features/{status}/{feature}/spec.md
aidocs/sdd/{project}/features/{status}/{feature}/design.md
aidocs/sdd/{project}/features/{status}/{feature}/implementation-plan.md
```

If implementation-plan missing:
→ Use Section 4 to create it first

## Task File Format

```markdown
# TASK_{NNN}: {Short Name}

**Feature:** {feature}
**Status:** todo | in-progress | done
**Created:** {date}

## Objective
{Clear, single-agent executable goal}

## Dependencies
- {TASK_XXX} must complete first (if any)

## Acceptance Criteria
- [ ] AC-{NNN}.1: {Criterion 1}
- [ ] AC-{NNN}.2: {Criterion 2}

## Technical Approach
{Step-by-step implementation plan}

## Files
| File | Action | Description |
|------|--------|-------------|
| path/to/file.py | CREATE/MODIFY | What changes |

## Estimated Tokens
~{XX}k
```

## Task Creation Call

```python
Task(
    subagent_type="faion-task-creator-agent",
    description=f"Create {task_name}",
    prompt=f"""
PROJECT: {project}
FEATURE: {feature}
TASK_INFO: {task_from_plan}
SDD_PATH: aidocs/sdd/{project}/features/{status}/{feature}/

Create comprehensive task file with:
- Clear objective
- Acceptance criteria (AC-XX.X)
- Technical approach
- Files to modify
- Dependencies
- Estimated complexity

Research codebase deeply before writing.
"""
)
```

## Task Review

After all tasks created:

```python
Task(
    subagent_type="faion-sdd-reviewer-agent (mode: tasks)",
    prompt=f"""
Multi-pass review for {project}/{feature}:

Pass 1: Completeness - all plan items covered?
Pass 2: Consistency - no contradictions?
Pass 3: Coverage - all requirements addressed?
Pass 4: Executability - can be implemented as written?
"""
)
```

## Output Format

```markdown
## Tasks Created: {project}/{feature}

### Summary
- **Tasks created:** {count}
- **Review status:** Passed | Issues found

### Tasks
| Task | Description | Complexity |
|------|-------------|------------|
| TASK_001 | {desc} | Medium |
| TASK_002 | {desc} | Low |

### Review Notes
{from faion-sdd-reviewer-agent (mode: tasks)}

### Next Steps
- Execute tasks with Section 6
- Or batch execute with Section 7
```

**Output:** Task files in `tasks/todo/` → Next: Task Execution

---

# Section 6: Task Execution

## Purpose

Execute a single SDD task using the `faion-task-executor-agent` agent.

## Workflow

```
1. Parse project, feature, task_name
   ↓
2. Find task file in todo/ or in-progress/
   ↓
3. Load SDD context (constitution, spec, design, impl-plan)
   ↓
4. Call faion-task-executor-agent agent
   ↓
5. Report results
```

## Task Resolution

Search order:
1. `tasks/in-progress/TASK_*{name}*.md`
2. `tasks/todo/TASK_*{name}*.md`

Partial match supported: "TASK_001", "001", "models"

## Context Loading

Load these files for agent context:
```
aidocs/sdd/{project}/constitution.md
aidocs/sdd/{project}/features/{status}/{feature}/spec.md
aidocs/sdd/{project}/features/{status}/{feature}/design.md
aidocs/sdd/{project}/features/{status}/{feature}/implementation-plan.md
{task_file}
```

## Agent Invocation

```python
Task(
    subagent_type="faion-task-executor-agent",
    description=f"Execute {task_name}",
    prompt=f"""
PROJECT: {project}
FEATURE: {feature}
TASK_FILE: {task_path}

SDD CONTEXT:
- Constitution: {constitution_content}
- Spec: {spec_content}
- Design: {design_content}
- Implementation Plan: {impl_plan_content}

TASK CONTENT:
{task_content}

EXECUTION STEPS:
1. Move task to in-progress/ (if in todo/)
2. Deep research - understand codebase context
3. Plan subtasks using TodoWrite
4. Execute implementation
5. Quality checks (tests, linting)
6. Commit with message: "TASK_XXX: {description}"
7. Move task to done/
"""
)
```

## Task Lifecycle

```
tasks/todo/TASK_XXX.md
       ↓ (start execution)
tasks/in-progress/TASK_XXX.md
       ↓ (complete successfully)
tasks/done/TASK_XXX.md
```

## Output Format

```markdown
## Task Execution: {TASK_NAME}

**Status:** SUCCESS | FAILED | BLOCKED

### Summary
{what was done}

### Files Changed
- {file1}: {change description}
- {file2}: {change description}

### Commit
{commit_hash}: {commit_message}

### Notes
{any issues or blockers}
```

## Error Handling

| Error | Action |
|-------|--------|
| Task not found | List available tasks, ask user |
| Context missing | Warn, continue with available context |
| Execution failed | Report error, keep task in in-progress |
| Tests failed | Document failures, don't move to done |

**Output:** Executed task in `done/` → Next: Batch Execution or Parallelization

---

# Section 7: Batch Execution

## Purpose

Execute all tasks for a feature in sequence, with intelligent failure handling.

## Workflow

```
1. Parse project, feature
   ↓
2. Find all tasks (in-progress first, then todo, sorted)
   ↓
3. Load SDD context
   ↓
4. Clarify ambiguities BEFORE execution
   ↓
5. Create feature branch (optional)
   ↓
6. Execute each task via Section 6
   ↓
7. Run post-execution review
   ↓
8. Quality checks (tests, lint)
   ↓
9. Report summary
```

## Task Discovery

```bash
# Priority order
1. tasks/in-progress/TASK_*.md  # Resume first
2. tasks/todo/TASK_*.md         # Then new tasks

# Sort by task number
TASK_001, TASK_002, TASK_003...
```

## Pre-Execution Clarification

Before starting, review all tasks for:
- Ambiguous requirements
- Missing dependencies
- Unclear acceptance criteria

Use AskUserQuestion if clarification needed.

## Execution Loop

```python
for task in sorted_tasks:
    result = execute_task(project, feature, task.name)

    if result.status == "BLOCKED":
        if is_critical(result.error):
            STOP  # Git conflict, build broken, security
        else:
            CONTINUE  # Test failures, minor issues

    log_result(result)
```

## Continue vs Stop Rules

**Continue if:**
- Single task fails (document and continue)
- Test failures (log for later fix)
- Minor code style issues
- Non-blocking warnings

**Stop if:**
- Git merge conflict
- Build completely broken
- Security vulnerability detected
- User requests stop

## Post-Execution Review

```python
Task(
    subagent_type="faion-sdd-reviewer-agent (mode: tasks)",
    prompt=f"Review completed tasks for {project}/{feature}"
)
```

## Output Format

```markdown
## Feature Execution: {project}/{feature}

### Summary
- **Tasks:** {completed}/{total}
- **Status:** Complete | Partial | Failed
- **Duration:** {time}

### Task Results
| Task | Status | Commit | Notes |
|------|--------|--------|-------|
| TASK_001 | Done | abc123 | |
| TASK_002 | Done | def456 | |
| TASK_003 | Blocked | - | Tests failing |

### Quality Report
- Tests: {pass}/{total}
- Lint: {status}

### Next Steps
{recommendations}
```

**Output:** All tasks in `done/` (or partial) → Next: Feature complete or Parallelization

---

# Section 8: Parallelization Logic

## Purpose

Analyze task dependencies and group into parallel execution waves. Achieve up to 3.5x speedup through optimized execution order.

## Workflow

```
1. Read all TASK_*.md files
   ↓
2. Extract dependencies from each task
   ↓
3. Build dependency graph
   ↓
4. Group into waves (independent tasks together)
   ↓
5. Add checkpoints between waves
   ↓
6. Generate execution plan
```

## Dependency Detection

### Explicit Dependencies
From task files:
```markdown
## Dependencies
- TASK_001 must complete first
- Requires auth module from TASK_002
```

### Implicit Dependencies
Detect from:
- File modifications (same file = sequential)
- Module imports (importing from task output)
- Database schema (migrations order)
- API contracts (consumer after producer)

## Wave Pattern

```
Wave 1: [Independent tasks - run in parallel]
    ↓
Checkpoint 1: Verify all Wave 1 complete, merge results
    ↓
Wave 2: [Tasks depending on Wave 1 - run in parallel]
    ↓
Checkpoint 2: Verify, merge
    ↓
Wave N: [Final tasks]
    ↓
Final Checkpoint: Integration verification
```

## Dependency Graph Example

```
TASK_001 ──┬──→ TASK_004 ──┐
           │               │
TASK_002 ──┼──→ TASK_005 ──┼──→ TASK_006
           │               │
TASK_003 ──┴───────────────┘
```

Wave 1: TASK_001, TASK_002, TASK_003 (parallel)
Wave 2: TASK_004, TASK_005 (parallel)
Wave 3: TASK_006 (sequential)

## Speedup Calculation

```
Sequential time = Sum of all task times
Parallel time = Sum of longest task per wave + checkpoints

Speedup = Sequential / Parallel
```

Example:
- 6 tasks, 30 min each = 180 min sequential
- 3 waves (3+2+1 tasks) + 2 checkpoints (5 min each)
- Parallel = 30 + 5 + 30 + 5 + 30 = 100 min
- Speedup = 180/100 = 1.8x

With more parallelizable tasks: up to 3.5x

## Checkpoint Types

| Type | When | Action |
|------|------|--------|
| Merge | After parallel wave | Combine outputs, resolve conflicts |
| Verify | Critical dependency | Run tests, check contracts |
| Review | Complex integration | Human review before continuing |
| Sync | State-dependent | Ensure consistent state |

## Output Format

```markdown
## Parallel Execution Plan

### Summary
- Total tasks: {N}
- Waves: {M}
- Estimated speedup: {X}x
- Critical path: TASK_A → TASK_D → TASK_G

### Wave 1 (Parallel)
| Task | Description | Est. Tokens |
|------|-------------|-------------|
| TASK_001 | Setup models | 3000 |
| TASK_002 | Setup serializers | 2500 |
| TASK_003 | Setup permissions | 2000 |

**Checkpoint 1:** Verify models, serializers, permissions created

### Wave 2 (Parallel)
| Task | Depends On | Description |
|------|------------|-------------|
| TASK_004 | TASK_001 | Create views |
| TASK_005 | TASK_001, TASK_002 | Create API endpoints |

**Checkpoint 2:** Verify API endpoints functional

### Wave 3 (Sequential - Critical Path)
| Task | Depends On | Description |
|------|------------|-------------|
| TASK_006 | TASK_004, TASK_005 | Integration tests |

**Final Checkpoint:** All tests pass
```

## Integration

- After Section 5 (Task Creation) → Auto-analyze parallelization
- Add wave structure to implementation-plan.md
- Execute in wave order with Section 7

**Output:** Parallelized execution plan → Execute with optimized order

---

# Agents Called

| Agent | Purpose |
|-------|---------|
| faion-sdd-reviewer-agent (mode: spec) | Review spec before save |
| faion-sdd-reviewer-agent (mode: design) | Review design for architecture decisions |
| faion-sdd-reviewer-agent (mode: plan) | Review impl-plan for 100k token compliance |
| faion-task-creator-agent | Create individual tasks with deep research |
| faion-task-executor-agent | Execute tasks autonomously |
| faion-sdd-reviewer-agent (mode: tasks) | Review completed tasks (4-pass) |
| faion-hallucination-checker-agent | Verify task completion with evidence |

---

# Directory Structure

```
aidocs/sdd/{project}/
├── constitution.md                    # Project principles (Section 1)
├── contracts.md                       # API contracts
├── roadmap.md                         # Milestones
└── features/
    ├── backlog/                       # Features waiting for grooming
    ├── todo/                          # Features ready for execution
    ├── in-progress/                   # Features being worked on
    └── done/                          # Completed features
        └── {NN}-{feature}/
            ├── spec.md                # WHAT and WHY (Section 2)
            ├── design.md              # HOW (Section 3)
            ├── implementation-plan.md # Tasks breakdown (Section 4)
            └── tasks/
                ├── backlog/
                ├── todo/              # Tasks ready (Section 5 output)
                ├── in-progress/       # Currently executing (Section 6)
                └── done/              # Completed (Section 6/7 output)
```

---

# Quick Reference

| Section | Purpose | Input | Output |
|---------|---------|-------|--------|
| 1 | Constitutions | Project analysis/dialogue | constitution.md |
| 2 | Specifications | Problem + requirements | spec.md |
| 3 | Design Documents | Approved spec | design.md |
| 4 | Implementation Plans | Design + 100k rule | implementation-plan.md |
| 5 | Task Creation | Impl-plan + codebase | Task files in todo/ |
| 6 | Task Execution | Single task | Task in done/ + commit |
| 7 | Batch Execution | All tasks | All tasks done/ |
| 8 | Parallelization | Task dependencies | Optimized wave plan |

---

---

# Methodologies Reference

## M-SDD-001: SDD Workflow Overview

### Problem
Teams lack a structured approach to translate ideas into working software, leading to scope creep, miscommunication, and wasted effort.

### Framework
```
CONSTITUTION → SPEC → DESIGN → IMPL-PLAN → TASKS → EXECUTE → DONE
      ↓          ↓        ↓         ↓          ↓        ↓        ↓
   project    feature  technical  100k rule  atomic   agent    learn
   principles  intent   approach  compliance  units  execution  reflect
```

**Step 1: Constitution** - Define immutable project principles
- Tech stack, coding standards, architecture patterns
- Source of truth for ALL features

**Step 2: Specification** - Define WHAT and WHY
- Problem statement, user stories, requirements
- Socratic dialogue to extract real needs

**Step 3: Design** - Define HOW
- Architecture decisions with rationale
- File mappings, data flows, integration points

**Step 4: Implementation Plan** - Break into tasks
- Apply 100k token rule per task
- Dependencies, parallelization opportunities

**Step 5: Tasks** - Execute atomically
- One task = one agent execution
- Clear acceptance criteria

**Step 6: Done** - Verify and reflect
- Quality gates passed
- Lessons learned captured

### Templates

**Directory Structure:**
```
aidocs/sdd/{project}/
├── constitution.md           # Project principles
├── contracts.md              # API contracts
├── roadmap.md                # Milestones
└── features/{status}/{NN}-{feature}/
    ├── spec.md               # WHAT and WHY
    ├── design.md             # HOW
    ├── implementation-plan.md # Task breakdown
    └── tasks/{status}/       # Task files
```

### Examples

**E-commerce MVP:**
1. Constitution: Django + PostgreSQL + Tailwind
2. Spec: User can browse products, add to cart, checkout
3. Design: Product model, Cart service, Stripe integration
4. Plan: 12 tasks across 3 phases
5. Execute: 1 week to MVP

### Agent
faion-task-executor-agent, faion-task-creator-agent

---

## M-SDD-002: Writing Specifications

### Problem
Requirements are vague, incomplete, or based on assumptions rather than validated user needs.

### Framework

**Phase 1: Brainstorming**
- Start with: "Tell me about the problem. Who suffers and how?"
- Apply Five Whys to reach root cause
- Challenge assumptions: "Is this needed for v1?"

**Phase 2: Research Codebase**
- Search existing patterns: `Glob **/models.py`
- Find related specs: `Glob aidocs/sdd/**/spec.md`
- Share findings with user

**Phase 3: Clarify Details**
- User stories: As {role}, I want {goal}, so that {benefit}
- Edge cases through questions (not assumptions)

**Phase 4: Draft Section by Section**
- Problem Statement → validate
- User Stories with AC → validate
- Functional Requirements → validate
- Out of Scope → validate

**Phase 5: Review**
- Call faion-sdd-reviewer-agent (mode: spec) agent
- Check: Problem clear? Stories specific? Requirements testable?

**Phase 6: Save**
- `aidocs/sdd/{project}/features/backlog/{NN}-{feature}/spec.md`

### Templates

**Spec Template:**
```markdown
# Feature: {Name}

## Problem Statement
{Clear description of the problem}

## User Stories

### US-01: {Story Name}
**As a** {role}
**I want** {goal}
**So that** {benefit}

**Acceptance Criteria:**
- [ ] AC-01.1: {criterion}
- [ ] AC-01.2: {criterion}

## Functional Requirements
- FR-01: {requirement}
- FR-02: {requirement}

## Out of Scope
- {explicitly excluded item}
```

### Examples

**User Authentication Spec:**
- Problem: Users cannot securely access their accounts
- US-01: As a user, I want to register with email
- FR-01: System shall validate email format
- Out of Scope: Social login (v2)

### Agent
faion-sdd-reviewer-agent (mode: spec)

---

## M-SDD-003: Writing Design Documents

### Problem
Developers lack clear technical guidance, leading to inconsistent implementations and architectural drift.

### Framework

**Phase 1: Read Specification**
- Extract problem, user stories, requirements
- Identify API contracts (if any)

**Phase 2: Read Constitution**
- Extract architecture patterns, code standards
- Note testing requirements

**Phase 3: Research Codebase**
- Find similar implementations
- Identify reusable components
- Determine where new code fits

**Phase 4: Architecture Decisions (AD)**
- For each key decision: context, options, rationale
- Minimum 2 alternatives per decision

**Phase 5: Technical Approach**
- Components and interactions
- Data flow and validation
- File mappings (CREATE/MODIFY)

**Phase 6: Testing Strategy**
- Unit tests, integration tests
- Test data requirements

**Phase 7: Risk Assessment**
- Impact, mitigation for each risk

**Phase 8: Review**
- Call faion-sdd-reviewer-agent (mode: design) agent

### Templates

**Architecture Decision Template:**
```markdown
### AD-{N}: {Decision Name}

**Context:**
{Problem being solved}

**Options:**
- **A: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}
- **B: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}

**Decision:** {Chosen option}

**Rationale:** {Why this choice}
```

**Files Section:**
```markdown
## Files

| File | Action | Description |
|------|--------|-------------|
| app/models/user.py | CREATE | User model |
| app/services/auth.py | CREATE | Auth service |
| app/views/auth.py | MODIFY | Add login endpoint |
```

### Examples

**Payment Integration Design:**
- AD-1: Use Stripe vs PayPal → Stripe (better API)
- AD-2: Store card tokens vs redirect → Tokens (better UX)
- Files: payment_service.py (CREATE), checkout_view.py (MODIFY)

### Agent
faion-sdd-reviewer-agent (mode: design)

---

## M-SDD-004: Writing Implementation Plans

### Problem
Tasks are too large, unclear, or have hidden dependencies, causing blocked work and context overflow.

### Framework

**Key Principle:** Each task MUST fit 100k token context

**Token Budget:**
```
Research: ~20k (read existing code)
Task file: ~5k
Implementation: ~50k
Buffer: ~25k
TOTAL < 100k
```

**Phase 1: Load Context**
- Read constitution, spec, design

**Phase 2: Analyze Complexity**
- Estimate tokens per file
- Identify high-complexity areas

**Phase 3: Define Work Units**
- Group related work
- Apply 100k rule

**Phase 4: Map Dependencies**
- Explicit: task file references
- Implicit: file modifications, imports

**Phase 5: Optimize Parallelization**
- Identify independent tasks
- Create execution waves

**Phase 6: Review**
- Call faion-sdd-reviewer-agent (mode: plan)

### Templates

**Implementation Plan:**
```markdown
# Implementation Plan: {Feature}

## Overview
- **Total tasks:** {N}
- **Estimated effort:** {X} hours
- **Critical path:** TASK_001 → TASK_003 → TASK_005

## Tasks

### TASK_001: {Name}
- **Complexity:** Low/Medium/High
- **Est. tokens:** ~{X}k
- **Depends on:** —
- **Enables:** TASK_003

### TASK_002: {Name}
- **Complexity:** Medium
- **Est. tokens:** ~{X}k
- **Depends on:** —
- **Enables:** TASK_003

## Execution Order

### Wave 1 (Parallel)
- TASK_001, TASK_002

### Wave 2 (Sequential)
- TASK_003 (depends on Wave 1)
```

**Token Estimation:**
| Component | Tokens |
|-----------|--------|
| Django model (simple) | 5-10k |
| Django model (complex) | 15-25k |
| Service class | 20-40k |
| ViewSet | 15-30k |
| Test file | 20-40k |

### Examples

**Auth Feature Plan:**
- TASK_001: User model (10k) - independent
- TASK_002: Auth service (30k) - depends on 001
- TASK_003: Login endpoint (20k) - depends on 002
- TASK_004: Tests (25k) - depends on 002, 003

### Agent
faion-sdd-reviewer-agent (mode: plan)

---

## M-SDD-005: Task Creation and Parallelization

### Problem
Tasks are created inconsistently, dependencies are unclear, and parallelization opportunities are missed.

### Framework

**Task Creation:**
1. Parse implementation plan
2. Create task file with standard format
3. Include acceptance criteria
4. Estimate tokens

**Task File Format:**
```markdown
# TASK_{NNN}: {Short Name}

**Feature:** {feature}
**Status:** todo
**Created:** {date}

## Objective
{Clear, single-agent executable goal}

## Dependencies
- {TASK_XXX if any}

## Acceptance Criteria
- [ ] AC-{NNN}.1: {criterion}
- [ ] AC-{NNN}.2: {criterion}

## Technical Approach
{Step-by-step plan}

## Files
| File | Action | Description |
|------|--------|-------------|

## Estimated Tokens
~{XX}k
```

**Parallelization Analysis:**
1. Build dependency graph
2. Identify independent tasks
3. Group into waves
4. Calculate speedup

**Wave Pattern:**
```
Wave 1: [Independent tasks - parallel]
    ↓
Checkpoint 1: Verify, merge
    ↓
Wave 2: [Dependent tasks - parallel]
    ↓
Final Checkpoint: Integration
```

### Templates

**Dependency Graph:**
```
TASK_001 ──┬──→ TASK_004 ──┐
           │               │
TASK_002 ──┼──→ TASK_005 ──┼──→ TASK_006
           │               │
TASK_003 ──┴───────────────┘
```

**Speedup Calculation:**
```
Sequential = Sum(task times)
Parallel = Sum(max task per wave) + checkpoints
Speedup = Sequential / Parallel
```

### Examples

**6 tasks, 30 min each:**
- Sequential: 180 min
- Parallel (3 waves): 100 min
- Speedup: 1.8x

### Agent
faion-task-creator-agent, faion-sdd-reviewer-agent (mode: tasks)

---

## M-SDD-006: Quality Gates and Confidence Checks

### Problem
Work is marked complete without proper verification, leading to bugs, incomplete features, and technical debt.

### Framework

**Quality Gate Levels:**

| Level | Check | Pass Criteria |
|-------|-------|---------------|
| L1: Syntax | Linting | Zero errors |
| L2: Types | Type checking | Zero errors |
| L3: Tests | Unit tests | 100% pass |
| L4: Integration | Integration tests | 100% pass |
| L5: Review | Code review | Approved |
| L6: Acceptance | AC verification | All criteria met |

**Confidence Check Process:**
1. List all acceptance criteria
2. For each AC, provide evidence
3. Rate confidence (0-100%)
4. If <90%, identify gaps

**Evidence Types:**
- Test passing (link to test)
- Screenshot/recording
- Manual verification steps
- Code reference

### Templates

**Confidence Check:**
```markdown
## Confidence Check: TASK_{NNN}

| AC | Evidence | Confidence |
|----|----------|------------|
| AC-001.1 | test_user_registration passes | 95% |
| AC-001.2 | Screenshot attached | 90% |
| AC-001.3 | Manual verification: steps 1-5 | 85% |

**Overall Confidence:** 90%

**Gaps:**
- AC-001.3: Edge case X not covered

**Recommendation:** Address gaps before marking done
```

### Examples

**Auth Task Confidence:**
- AC-001.1: test_login_success → 100%
- AC-001.2: test_login_failure → 100%
- AC-001.3: Password reset email → 80% (email not verified in staging)
- Overall: 93% → Proceed with note

### Agent
faion-hallucination-checker-agent

---

## M-SDD-007: Reflexion and Learning

### Problem
Teams repeat mistakes, don't capture lessons learned, and fail to improve processes over time.

### Framework

**Reflexion Process:**
1. After task completion, review outcomes
2. Identify what worked well
3. Identify what could improve
4. Document lessons learned
5. Update patterns/anti-patterns

**Learning Categories:**
- **Patterns:** Reusable approaches that worked
- **Anti-patterns:** Approaches to avoid
- **Tools:** New tools or techniques discovered
- **Estimates:** Calibration of time/complexity estimates

**Storage:**
```
~/.sdd/memory/
├── patterns_learned.jsonl
├── mistakes_learned.jsonl
└── session_context.md
```

### Templates

**Lesson Learned:**
```json
{
  "date": "2026-01-18",
  "project": "faion-net",
  "task": "TASK_030",
  "type": "pattern",
  "title": "Methodology embedding",
  "description": "Embedding full methodology content in SKILL.md provides better context than separate files",
  "impact": "high"
}
```

**Session Context:**
```markdown
# Session: 2026-01-18

## What Worked
- Breaking methodologies into clear sections
- Including examples for each

## What to Improve
- Estimate complexity more accurately
- Add cross-references between skills

## Action Items
- [ ] Update estimation guide
- [ ] Create methodology cross-reference
```

### Examples

**Pattern Learned:**
- Title: "Socratic Requirements"
- Description: Ask questions instead of assuming
- Impact: Reduced rework by 40%

**Anti-pattern:**
- Title: "Large Tasks"
- Description: Tasks >50k tokens often fail
- Solution: Split at 30k threshold

### Agent
faion-task-executor-agent (reflexion phase)

---

## M-SDD-008: Backlog Grooming and Roadmapping

### Problem
Backlog is disorganized, priorities unclear, and there's no connection between daily work and long-term goals.

### Framework

**Backlog Grooming:**
1. Review items for next 2-3 sprints
2. Ensure each item has:
   - Clear description
   - Acceptance criteria
   - Estimate
   - Dependencies identified
3. Split large items (>13 story points)
4. Prioritize by value/effort

**Definition of Ready:**
- [ ] Problem/need clear
- [ ] Acceptance criteria defined
- [ ] Estimated (story points or t-shirt size)
- [ ] Dependencies identified
- [ ] Small enough for one sprint
- [ ] No blockers

**Roadmap Structure:**
```
## Now (commit) - This quarter
- Feature A: In progress
- Feature B: Next up

## Next (plan) - Next quarter
- Feature C: Planned
- Feature D: Planned

## Later (vision) - Future
- Theme X
- Theme Y
```

**Roadmap Principles:**
- Now: 90% confident, detailed
- Next: 70% confident, planned
- Later: 50% confident, thematic
- Include 20% buffer

### Templates

**Backlog Item:**
```markdown
## BL-{NNN}: {Title}

**Priority:** P0/P1/P2/P3
**Estimate:** {points} pts / {size}
**Status:** grooming | ready | in-progress | done

### Problem
{What need does this address}

### Acceptance Criteria
- [ ] {criterion 1}
- [ ] {criterion 2}

### Dependencies
- Requires: {BL-XXX}
- Blocks: {BL-YYY}
```

**Roadmap:**
```markdown
# Roadmap: {Project}

## Now (Q1 2026)
| Feature | Status | Target |
|---------|--------|--------|
| Auth system | In progress | Jan 31 |
| Payment integration | Next | Feb 15 |

## Next (Q2 2026)
| Feature | Description |
|---------|-------------|
| Localization | 8 languages |
| Mobile app | iOS + Android |

## Later (H2 2026)
- Theme: Scale infrastructure
- Theme: Enterprise features
```

### Examples

**E-commerce Roadmap:**
- Now: Core shopping (browse, cart, checkout)
- Next: User accounts, order history
- Later: Recommendations, subscriptions

**Grooming Session:**
- Review 12 items
- Split 3 large items
- Mark 8 as ready
- Defer 4 to next quarter

### Agent
faion-pm-agent, faion-task-creator-agent

---

# Section 9: Backlog Grooming

## Purpose

Interactive grooming session: prioritize features, refine specs, create designs, generate tasks. Ensures features are ready before execution.

## Workflow

```
READ BACKLOG → PRIORITIZE → SELECT FEATURE → REFINE SPEC → CREATE DESIGN → GENERATE TASKS → MOVE TO TODO
```

## Phase 1: Load Context

Read: `roadmap.md`, `constitution.md`
List features by status: backlog, todo, in-progress, done

## Phase 2: Display Status

```markdown
## Feature Status

### In Progress ({n})
- {feature} — {summary}

### Todo ({n})
- {feature} — {summary}

### Backlog ({n})
- {feature} — {summary} [P0/P1/P2]
```

## Phase 3: Action Selection

AskUserQuestion: "What do you want to do?"
1. Review priorities
2. Take feature to work
3. Add new feature
4. Remove feature
5. Finish grooming

## Phase 4: Feature Selection

Show backlog with: Name, Spec status, Design status, Dependencies

```markdown
| # | Feature | Spec | Design | Dependencies |
|---|---------|------|--------|--------------|
| 1 | auth | Done | Missing | none |
| 2 | transactions | Done | Missing | auth |
```

## Phase 5: Spec Refinement

If no spec or needs update:
- Show existing spec
- Ask clarifying questions
- Use Section 2 (Writing Specifications) if needed

## Phase 6: Design Creation

If spec approved:
- Use Section 3 (Writing Design Documents)
- Present for review

## Phase 7: Task Generation

If design approved:
- Use Section 4 (Writing Implementation Plans)
- Use Section 5 (Task Creation)
- Present tasks for review

## Phase 8: Move to Todo

If approved:
```bash
mv features/backlog/{feature}/ features/todo/{feature}/
```

Report: "Feature ready! Execute with Section 6 or 7"

## Feature Lifecycle

```
backlog/ → todo/ → in-progress/ → done/
   ↓         ↓           ↓           ↓
spec.md  +design.md  executing    archived
         +impl-plan
         +tasks/
```

## Definition of Ready

Before moving feature to todo/:
- [ ] Problem/need clear
- [ ] Acceptance criteria defined
- [ ] Estimated (story points or t-shirt size)
- [ ] Dependencies identified
- [ ] Small enough for one sprint
- [ ] No blockers
- [ ] Spec approved
- [ ] Design approved
- [ ] Tasks created

## Anti-patterns

- Skip spec refinement
- Create tasks without design
- Move to todo without all artifacts
- Take feature with unsatisfied dependencies

**Output:** Feature with complete artifacts in `todo/` → Next: Execute with Section 6 or 7

---

# Section 10: Roadmapping

## Purpose

Analyze progress, reprioritize backlog, add features, maintain roadmap. Connects daily work to long-term goals.

## When to Use

- After completing features → progress review
- New ideas → add to backlog
- Priorities changed → reprioritize
- Weekly/sprint → roadmap sync

## Workflow

```
ANALYZE → REVIEW PRIORITIES → ADD FEATURES → UPDATE ROADMAP
```

## Phase 1: Analyze Progress

```bash
# Count features by status
ls aidocs/sdd/{project}/features/done/
ls aidocs/sdd/{project}/features/backlog/
ls aidocs/sdd/{project}/features/*/tasks/done/
```

Report: done, in-progress, backlog counts

## Phase 2: Review Priorities

AskUserQuestion: "Are priorities current?"
- Yes → Continue
- Need change → Reprioritize

If change needed → reorder features

## Phase 3: Add New Features

For each new idea:
1. Discuss scope via Socratic dialogue
2. Create `backlog/{NN}-{name}/spec.md`
3. Add to roadmap.md

## Phase 4: Update Roadmap

```markdown
# Roadmap: {project}

## Now (commit) - This quarter
- [ ] {feature} — {status}

## Next (plan) - Next quarter
- {feature}: {one-liner}

## Later (vision) - Future
- {theme}

## Done
- {NN}-{feature}

## Risks
- {risk}: {mitigation}
```

## Roadmap Principles

| Timeframe | Confidence | Detail Level |
|-----------|------------|--------------|
| Now | 90% | Detailed, committed |
| Next | 70% | Planned, flexible |
| Later | 50% | Thematic, vision |

- Include 20% buffer for unknowns
- Review weekly during active development
- Review monthly for strategic alignment

## Output

Updated `roadmap.md` with priorities, milestones, risks

**Output:** `roadmap.md` → Next: Backlog Grooming (Section 9)

---

# Section 11: Quality Gates and Reviews

## Purpose

Perform code review or SDD document review using specialized agents. Ensures quality at each stage of development.

## Modes

### Code Review Mode
Review git diff for a project directory.

### SDD Review Mode
Review SDD documents (spec, design, impl-plan, tasks) for a feature.

## Mode Detection

```
Input contains "sdd:" prefix → SDD Review
Input is directory path → Code Review
Ask user if unclear
```

---

## Code Review Mode

### Workflow

```
1. Get git diff for directory
   ↓
2. Analyze changes against standards
   ↓
3. Report findings
```

### Review Criteria

**Critical (must fix):**
- Correctness issues
- Missing/broken tests
- Security vulnerabilities
- Breaking changes

**Style (should fix):**
- Convention violations
- Pattern deviations
- Naming issues

**Quality (consider):**
- Complexity
- Error handling
- Edge cases

**Performance (check):**
- N+1 queries
- Missing indexes
- Resource leaks

### Output Format

```markdown
## Code Review: {directory}

### Summary
{overall assessment}

### Critical Issues
1. {issue}: {file:line} - {description}

### Style Issues
1. {issue}: {file:line}

### Suggestions
- {suggestion}

### Pre-Merge Checklist
- [ ] All critical issues fixed
- [ ] Tests passing
- [ ] No security issues
```

---

## SDD Review Mode

### Workflow

```
1. Parse project/feature from input
   ↓
2. Run reviewers in sequence:
   - faion-sdd-reviewer-agent (mode: spec)
   - faion-sdd-reviewer-agent (mode: design)
   - faion-sdd-reviewer-agent (mode: plan)
   - faion-sdd-reviewer-agent (mode: tasks) (if tasks exist)
   ↓
3. Aggregate results
   ↓
4. Report overall verdict
```

### Output Format

```markdown
## SDD Review: {project}/{feature}

### Document Status
| Document | Status | Issues |
|----------|--------|--------|
| spec.md | Pass/Warn/Fail | {count} |
| design.md | Pass/Warn/Fail | {count} |
| implementation-plan.md | Pass/Warn/Fail | {count} |
| tasks/ | Pass/Warn/Fail | {count} |

### Overall Verdict: APPROVED / NEEDS_WORK / REJECTED

### Issues Found
{detailed issues per document}

### Recommendations
{what to fix before proceeding}
```

## Quality Gate Levels

| Level | Check | Pass Criteria |
|-------|-------|---------------|
| L1 | Syntax | Linting zero errors |
| L2 | Types | Type checking zero errors |
| L3 | Tests | Unit tests 100% pass |
| L4 | Integration | Integration tests 100% pass |
| L5 | Review | Code review approved |
| L6 | Acceptance | All AC criteria met |

**Output:** Review report with verdict → Next: Fix issues or proceed

---

# Section 12: Confidence Checks

## Purpose

Validate readiness before major SDD phases. Prevents 5-50K tokens of wrong-direction work by spending 100-200 tokens on verification.

**ROI: 25-250x token savings**

## When to Use

- Before writing spec.md (idea validation)
- Before writing design.md (requirements clarity)
- Before creating tasks (design completeness)
- Before executing tasks (implementation readiness)

## Confidence Thresholds

| Score | Action |
|-------|--------|
| >=90% | Proceed confidently |
| 70-89% | Present alternatives, clarify gaps |
| <70% | Stop, ask questions first |

---

## Phase-Specific Checklists

### Pre-Spec Confidence (Idea → Spec)

| Check | Weight | Question |
|-------|--------|----------|
| Problem validated | 25% | Is there evidence people have this problem? |
| Market gap | 25% | Is there room for new solution? |
| Target audience | 20% | Do we know WHO specifically? |
| Value proposition | 15% | Why would they switch/pay? |
| Your fit | 15% | Can you build this? |

**Evidence required:**
- Pain point quotes from Reddit/forums/interviews
- Competitor analysis showing gaps
- User persona with real data

---

### Pre-Design Confidence (Spec → Design)

| Check | Weight | Question |
|-------|--------|----------|
| Requirements clear | 25% | All FR-XX unambiguous? |
| AC testable | 25% | All AC-XX measurable? |
| No contradictions | 20% | Requirements don't conflict? |
| Scope defined | 15% | Clear what's NOT included? |
| Dependencies known | 15% | External systems identified? |

**Evidence required:**
- Spec.md with all sections complete
- No TBD or unclear items
- User has approved spec

---

### Pre-Task Confidence (Design → Tasks)

| Check | Weight | Question |
|-------|--------|----------|
| Architecture decided | 25% | No open technical questions? |
| Patterns established | 25% | Following codebase conventions? |
| No duplicate work | 20% | Checked existing implementations? |
| Dependencies mapped | 15% | Task order clear? |
| Estimates reasonable | 15% | Complexity understood? |

**Evidence required:**
- Design.md approved
- Implementation-plan.md complete
- No TBD in technical decisions

---

### Pre-Implementation Confidence (Task → Code)

| Check | Weight | Question |
|-------|--------|----------|
| Task requirements clear | 25% | Know exactly what to build? |
| Approach decided | 25% | Know HOW to build it? |
| No blockers | 20% | All dependencies available? |
| Tests defined | 15% | Know how to verify? |
| Rollback plan | 15% | Can revert if fails? |

**Evidence required:**
- Task file read and understood
- Related code explored
- No open questions

---

## Workflow

```
1. Identify phase (spec/design/task/impl)
     ↓
2. Run phase-specific checklist
     ↓
3. Calculate confidence score
     ↓
4. Present results with evidence
     ↓
5. Decision:
   - >=90%: "Proceed"
   - 70-89%: "Clarify these gaps first"
   - <70%: "Stop - answer these questions"
```

## Output Format

```markdown
## Confidence Check: {phase}

### Score: {X}%

| Check | Status | Evidence |
|-------|--------|----------|
| {check1} | Pass/Warn/Fail | {evidence or gap} |
| {check2} | Pass/Warn/Fail | {evidence or gap} |

### Verdict: Proceed / Clarify / Stop

{If not proceed:}
### Questions to Answer First
1. {question1}
2. {question2}

### Recommended Actions
- {action1}
- {action2}
```

## Anti-Patterns to Catch

| Pattern | Risk | Action |
|---------|------|--------|
| "I think users want..." | Assumption without evidence | Require user research |
| "Should be easy..." | Underestimated complexity | Require technical spike |
| "Similar to X..." | Missed differences | Require detailed comparison |
| "We can figure it out later" | Deferred decisions | Require decision now |
| "Obviously..." | Hidden assumptions | Make explicit |

**Output:** Confidence report → Proceed or address gaps

---

# Section 13: Reflexion and Learning

## Purpose

Implement PDCA (Plan-Do-Check-Act) learning cycle. Store patterns and mistakes for future reference. Prevents repeating mistakes.

**ROI: Prevent 5-50K tokens of repeated mistakes**

## Memory Structure

```
~/.sdd/memory/
├── patterns_learned.jsonl    # Successful patterns
├── mistakes_learned.jsonl    # Errors and solutions
├── workflow_metrics.jsonl    # Execution metrics
└── session_context.md        # Current session state
```

## PDCA Cycle

```
Plan (hypothesis)
  ↓
Do (experiment)
  ↓
Check (self-evaluation)
  ↓
Act (improvement)
  ↓
Store (memory update)
```

---

## When to Use

### After Task Success
```
1. Extract what worked
2. Identify reusable patterns
3. Store in patterns_learned.jsonl
4. Update workflow_metrics.jsonl
```

### After Task Failure
```
1. Analyze root cause
2. Check if similar error exists in mistakes_learned.jsonl
3. If exists: Show previous solution
4. If new: Store error + solution
5. Update workflow_metrics.jsonl
```

### Before Task Start
```
1. Check mistakes_learned.jsonl for similar task types
2. If found: Show warnings and prevention tips
3. Check patterns_learned.jsonl for best practices
4. If found: Suggest approach
```

---

## Data Formats

### patterns_learned.jsonl
```json
{
  "id": "PAT-001",
  "timestamp": "2026-01-18T10:00:00Z",
  "project": "faion-net",
  "task_type": "skill_creation",
  "pattern_name": "methodology_embedding",
  "description": "Embed full methodology content in SKILL.md",
  "context": "When creating domain skills",
  "code_example": "## M-SDD-001: Methodology Name\n...",
  "success_count": 5,
  "tags": ["skill", "methodology", "documentation"]
}
```

### mistakes_learned.jsonl
```json
{
  "id": "ERR-001",
  "timestamp": "2026-01-18T10:00:00Z",
  "project": "faion-net",
  "task_type": "task_execution",
  "error_type": "context_overflow",
  "description": "Task exceeded 100k token limit",
  "root_cause": "Task scope too large, not split properly",
  "solution": "Split task into 2-3 smaller tasks",
  "prevention": "Always estimate tokens before execution",
  "occurrence_count": 2,
  "tags": ["token", "planning", "split"]
}
```

### workflow_metrics.jsonl
```json
{
  "timestamp": "2026-01-18T10:00:00Z",
  "project": "faion-net",
  "feature": "01-framework-content",
  "task_id": "TASK_003",
  "task_type": "skill_merge",
  "complexity": "medium",
  "estimated_tokens": 50000,
  "actual_tokens": 42000,
  "success": true,
  "duration_minutes": 15,
  "patterns_used": ["PAT-001"],
  "errors_encountered": []
}
```

---

## Workflow

### Recording Success
```
1. User says task completed successfully
2. AskUserQuestion: "What worked well?"
   - Code pattern
   - Architecture decision
   - Tool usage
   - Process improvement
3. Extract pattern details
4. Write to patterns_learned.jsonl
5. Update workflow_metrics.jsonl
```

### Recording Failure
```
1. User reports error or failure
2. AskUserQuestion: "What went wrong?"
   - Code error
   - Architecture mistake
   - Missing requirement
   - Tool issue
3. Analyze root cause
4. Check existing mistakes for similar
5. If new: Store in mistakes_learned.jsonl
6. Suggest solution
7. Update workflow_metrics.jsonl
```

### Pre-Task Check
```
1. Read task type from TASK_*.md
2. Search mistakes_learned.jsonl for matching tags
3. If found: Show warnings
4. Search patterns_learned.jsonl for matching tags
5. If found: Show recommendations
```

---

## Output Format

### Pattern Recorded
```markdown
## Pattern Recorded

**ID:** PAT-{NNN}
**Type:** {task_type}
**Pattern:** {pattern_name}

### Description
{description}

### When to Use
{context}

### Example
```{language}
{code_example}
```

Stored in `~/.sdd/memory/patterns_learned.jsonl`
```

### Mistake Recorded
```markdown
## Mistake Recorded

**ID:** ERR-{NNN}
**Type:** {error_type}

### What Happened
{description}

### Root Cause
{root_cause}

### Solution
{solution}

### Prevention
{prevention}

Stored in `~/.sdd/memory/mistakes_learned.jsonl`
```

### Pre-Task Warnings
```markdown
## Pre-Task Check: {task_type}

### Known Pitfalls
1. **ERR-{NNN}:** {description}
   - Prevention: {prevention}

### Recommended Patterns
1. **PAT-{NNN}:** {pattern_name}
   - Context: {context}
```

---

## Metrics Analysis

Monthly analysis of workflow_metrics.jsonl:
- Most common error types
- Most used patterns
- Token efficiency trends
- Success rate by task type
- Estimation accuracy

**Output:** Lessons stored in memory → Better future performance

---

# Agents Called (Complete List)

| Agent | Purpose | Used In |
|-------|---------|---------|
| faion-sdd-reviewer-agent (mode: spec) | Review spec before save | Section 2, 11 |
| faion-sdd-reviewer-agent (mode: design) | Review design for architecture decisions | Section 3, 11 |
| faion-sdd-reviewer-agent (mode: plan) | Review impl-plan for 100k token compliance | Section 4, 11 |
| faion-task-creator-agent | Create individual tasks with deep research | Section 5 |
| faion-task-executor-agent | Execute tasks autonomously | Section 6, 7 |
| faion-sdd-reviewer-agent (mode: tasks) | Review completed tasks (4-pass) | Section 5, 7, 11 |
| faion-hallucination-checker-agent | Verify task completion with evidence | Section 11, 12 |

---

# Quick Reference (Complete)

| Section | Purpose | Input | Output |
|---------|---------|-------|--------|
| 1 | Constitutions | Project analysis/dialogue | constitution.md |
| 2 | Specifications | Problem + requirements | spec.md |
| 3 | Design Documents | Approved spec | design.md |
| 4 | Implementation Plans | Design + 100k rule | implementation-plan.md |
| 5 | Task Creation | Impl-plan + codebase | Task files in todo/ |
| 6 | Task Execution | Single task | Task in done/ + commit |
| 7 | Batch Execution | All tasks | All tasks done/ |
| 8 | Parallelization | Task dependencies | Optimized wave plan |
| 9 | Backlog Grooming | Backlog features | Features ready in todo/ |
| 10 | Roadmapping | Progress + priorities | roadmap.md |
| 11 | Quality Gates | Code or SDD docs | Review report |
| 12 | Confidence Checks | Pre-phase validation | Confidence score |
| 13 | Reflexion | Task outcomes | Lessons in memory |

---

*SDD Domain Skill v2.0 - Complete*
*Sections 1-13: Full SDD Workflow with Quality Gates, Grooming, Roadmapping, and Reflexion*
*Methodologies: M-SDD-001 to M-SDD-008 embedded*


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-SDD-001 | Sdd Workflow Overview | [methodologies/M-SDD-001_sdd_workflow_overview.md](methodologies/M-SDD-001_sdd_workflow_overview.md) |
| M-SDD-002 | Writing Specifications | [methodologies/M-SDD-002_writing_specifications.md](methodologies/M-SDD-002_writing_specifications.md) |
| M-SDD-003 | Writing Design Documents | [methodologies/M-SDD-003_writing_design_documents.md](methodologies/M-SDD-003_writing_design_documents.md) |
| M-SDD-004 | Writing Implementation Plans | [methodologies/M-SDD-004_writing_implementation_plans.md](methodologies/M-SDD-004_writing_implementation_plans.md) |
| M-SDD-005 | Task Creation Parallelization | [methodologies/M-SDD-005_task_creation_parallelization.md](methodologies/M-SDD-005_task_creation_parallelization.md) |
| M-SDD-006 | Quality Gates Confidence | [methodologies/M-SDD-006_quality_gates_confidence.md](methodologies/M-SDD-006_quality_gates_confidence.md) |
| M-SDD-007 | Reflexion Learning | [methodologies/M-SDD-007_reflexion_learning.md](methodologies/M-SDD-007_reflexion_learning.md) |
| M-SDD-008 | Backlog Grooming Roadmapping | [methodologies/M-SDD-008_backlog_grooming_roadmapping.md](methodologies/M-SDD-008_backlog_grooming_roadmapping.md) |
