---
name: create-tasks
description: Generate Claude Code native Tasks from an existing spec. Use when user says "create tasks", "generate tasks from spec", "spec to tasks", "task generation", or wants to decompose a spec into implementation tasks.
argument-hint: "[spec-path] [--phase <phases>]"
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Read, Glob, Grep, TaskCreate, TaskUpdate, TaskList, TaskGet
arguments:
  - name: spec-path
    description: Path to the spec file to analyze for task generation
    required: true
  - name: phase
    description: Comma-separated phase numbers to generate tasks for (e.g., "1,2"). Omit to select interactively or generate all.
    required: false
---

# Spec to Tasks - Create Tasks Skill

You are an expert at transforming specifications into well-structured, actionable implementation tasks. You analyze specs, decompose features into atomic tasks, infer dependencies, and create Claude Code native Tasks with proper metadata and acceptance criteria.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Confirmation questions → AskUserQuestion
- Preview approval → AskUserQuestion
- Merge mode decisions → AskUserQuestion

Text output should only be used for:
- Presenting task previews and summaries
- Reporting completion status
- Displaying analysis findings

### Plan Mode Behavior

**CRITICAL**: This skill generates tasks, NOT an implementation plan. When invoked during Claude Code's plan mode:

- **DO NOT** create an implementation plan for how to build the spec's described features
- **DO NOT** defer task generation to an "execution phase"
- **DO** proceed with the full task generation workflow immediately
- **DO** create tasks using TaskCreate as normal

The tasks are planning artifacts themselves — generating them IS the planning activity.

## Load Reference Skills

Before starting the workflow, load the Claude Code Tasks reference for tool parameters, conventions, and patterns:

```
Read ${CLAUDE_PLUGIN_ROOT}/../claude-tools/skills/claude-code-tasks/SKILL.md
```

This reference provides:
- TaskCreate, TaskGet, TaskUpdate, TaskList tool parameters and return values
- Status lifecycle and transition rules
- Naming conventions (imperative subject, present-continuous activeForm)
- Dependency management with DAG design (blockedBy, blocks)
- Standard metadata conventions (priority, complexity, task_group, task_uid)

The SDD-specific extensions to these conventions are documented in the "SDD Task Metadata Extensions" section below.

## Workflow Overview

This workflow has ten phases:

1. **Validate & Load** — Validate spec file, parse `--phase` argument, read content, check settings, load reference files
2. **Detect Depth & Check Existing** — Detect spec depth level, check for existing tasks with phase metadata
3. **Analyze Spec** — Extract features, requirements, structure, and implementation phases from spec
4. **Select Phases** — Interactive or CLI-driven phase selection for incremental generation
5. **Decompose Tasks** — Phase-filtered hybrid decomposition from features and deliverables
6. **Infer Dependencies** — Phase-aware blocking relationships with cross-phase handling
7. **Detect Producer-Consumer Relationships** — Identify `produces_for` relationships between tasks
8. **Preview & Confirm** — Show phase-annotated summary, get user approval before creating
9. **Create Tasks** — Create tasks via TaskCreate/TaskUpdate with `spec_phase` metadata (fresh or merge mode)
10. **Error Handling** — Handle spec parsing issues, circular deps, missing info, phase-related errors

---

## Phase 1: Validate & Load

### Parse Arguments

Before validating the spec file, parse the provided arguments:

1. **Extract spec path**: The first positional argument is the spec file path
2. **Check for `--phase` flag**: If `--phase` is present, parse the comma-separated integers that follow (e.g., `--phase 1,2` → `[1, 2]`)
3. Store as `selected_phases_cli` (empty list if `--phase` not provided)

### Validate Spec File

Verify the spec file exists at the provided path.

If the file is not found:
1. Check `.claude/agent-alchemy.local.md` for a default spec directory or output path, and try resolving the spec path against it
2. Check if user provided a relative path
3. Try common spec locations:
   - `specs/SPEC-{name}.md`
   - `docs/SPEC-{name}.md`
   - `{name}.md` in current directory
3. Use Glob to search for similar filenames:
   - `**/SPEC*.md`
   - `**/*spec*.md`
   - `**/*requirements*.md`
4. If multiple matches found, use AskUserQuestion to let user select
5. If no matches found, inform user and ask for correct path

### Read Spec Content

Read the entire spec file using the Read tool.

### Check Settings

Check for optional settings at `.claude/agent-alchemy.local.md`:
- Author name (for attribution)
- Any custom preferences

This is optional — proceed without settings if not found.

### Load Reference Files

Read the reference files for task decomposition patterns, dependency rules, and testing requirements:

1. `references/decomposition-patterns.md` — Feature decomposition patterns by type
2. `references/dependency-inference.md` — Automatic dependency inference rules
3. `references/testing-requirements.md` — Test type mappings and acceptance criteria patterns

---

## Phase 2: Detect Depth & Check Existing

### Detect Depth Level

Analyze the spec content to detect its depth level:

**Full-Tech Indicators** (check first):
- Contains `API Specifications` section OR `### 7.4 API` or similar
- Contains API endpoint definitions (`POST /api/`, `GET /api/`, etc.)
- Contains `Testing Strategy` section
- Contains data model schemas with field definitions
- Contains code examples or schema definitions

**Detailed Indicators**:
- Uses numbered sections (`## 1.`, `### 2.1`)
- Contains `Technical Architecture` or `Technical Considerations` section
- Contains user stories (`**US-001**:` or similar format)
- Contains acceptance criteria (`- [ ]` checkboxes)
- Contains feature prioritization (P0, P1, P2, P3)

**High-Level Indicators**:
- Contains feature table with Priority column
- Executive summary focus (brief problem/solution)
- No user stories or acceptance criteria
- Shorter document (~50-100 lines)
- Minimal technical details

**Detection Priority**:
1. If spec contains `**Spec Depth**:` metadata field, use that value directly
2. Else if Full-Tech indicators found → Full-Tech
3. Else if Detailed indicators found → Detailed
4. Else if High-Level indicators found → High-Level
5. Default → Detailed

### Check for Existing Tasks

Use TaskList to check if there are existing tasks that reference this spec.

Look for tasks with `metadata.spec_path` matching the spec path.

If existing tasks found:
- Count them by status (pending, in_progress, completed)
- Note their task_uids for merge mode
- Extract `spec_phase` metadata from existing tasks to build `existing_phases_map`: `{phase_number → {pending, in_progress, completed, total, phase_name}}`
- Inform user about merge behavior with phase-aware detail

Report to user:
```
Found {n} existing tasks for this spec:
• {pending} pending
• {in_progress} in progress
• {completed} completed

{If existing tasks have spec_phase metadata:}
Previously generated phases:
• Phase {N}: {phase_name} — {total} tasks ({completed} completed, {pending} pending)
• Phase {M}: {phase_name} — {total} tasks ({completed} completed, {pending} pending)

New tasks will be merged. Completed tasks will be preserved.
```

---

## Phase 3: Analyze Spec

### Extract Spec Name

Parse the spec title to extract the spec name for use as `task_group`:
- Look for `# {name} PRD` title format on line 1
- Extract `{name}` as the spec name (e.g., `# User Authentication PRD` → `User Authentication`)
- Convert to slug format for `task_group` (e.g., `user-authentication`)
- If title does not match the PRD format, derive spec name from the filename: strip `SPEC-` prefix, strip `.md` extension, lowercase, replace spaces/underscores with hyphens (e.g., `SPEC-Payment-Flow.md` → `payment-flow`)

**Important**: `task_group` MUST be set on every task. The `execute-tasks` skill relies on `metadata.task_group` for `--task-group` filtering and session ID generation. Tasks without `task_group` will be invisible to group-filtered execution runs.

### Section Mapping

Extract information from each spec section:

| Spec Section | Extract |
|-------------|---------|
| **1. Overview** | Project name, description for task context |
| **5.x Functional Requirements** | Features, priorities (P0-P3), user stories |
| **6.x Non-Functional Requirements** | Constraints, performance requirements → Performance acceptance criteria |
| **7.x Technical Considerations** | Tech stack, architecture decisions |
| **7.3 Data Models** (Full-Tech) | Entity definitions → data model tasks |
| **7.4 API Specifications** (Full-Tech) | Endpoints → API tasks |
| **8.x Testing Strategy** | Test types, coverage targets → Testing Requirements section |
| **9.x Implementation Plan** | Phases, deliverables, completion criteria, checkpoint gates → phase metadata and task decomposition input |
| **10.x Dependencies** | Explicit dependencies → blockedBy relationships |

### Feature Extraction

For each feature in Section 5.x:
1. Note feature name and description
2. Extract priority (P0/P1/P2/P3)
3. List user stories (US-XXX)
4. Collect acceptance criteria and categorize by type (Functional, Edge Cases, Error Handling, Performance)
5. Identify implied sub-features

### Testing Extraction

From Section 8.x (Testing Strategy) if present:
1. Note test types specified (unit, integration, E2E)
2. Extract coverage targets
3. Identify critical paths requiring E2E tests
4. Note any performance testing requirements

From Section 6.x (Non-Functional Requirements):
1. Extract performance targets → Performance acceptance criteria
2. Extract security requirements → Security testing requirements
3. Extract reliability requirements → Integration test requirements

### Depth-Based Granularity

Adjust task granularity based on depth level:

**High-Level Spec:**
- 1-2 tasks per feature
- Feature-level deliverables
- Example: "Implement user authentication"

**Detailed Spec:**
- 3-5 tasks per feature
- Functional decomposition
- Example: "Implement login endpoint", "Add password validation"

**Full-Tech Spec:**
- 5-10 tasks per feature
- Technical decomposition
- Example: "Create User model", "Implement POST /auth/login", "Add auth middleware"

### Phase Extraction

Extract implementation phases from Section 9 if present:

1. **Detect Section 9**: Look for `## 9. Implementation Plan` or `## Implementation Phases`
2. **Extract phase headers**: Pattern `### 9.N Phase N: {Name}` (detailed/full-tech) or `### Phase N: {Name}` (high-level)
3. **For each phase, extract**:
   - `number` — Phase number (integer from `9.N` or `Phase N`)
   - `name` — Phase name (text after `Phase N: `)
   - `completion_criteria` — Text after `**Completion Criteria**:`
   - `deliverables` — Parsed table rows from the deliverable table (columns: Deliverable, Description, Dependencies; optionally Technical Tasks)
   - `checkpoint_gate` — Items after `**Checkpoint Gate**:` (prose or checkbox list `- [ ]`)
4. **Cross-reference deliverables to Section 5 features**: Scan deliverable descriptions and technical tasks for feature name references. Build mapping: `{phase_number → [feature_names]}`
5. If no Section 9 found, set `spec_phases = []`

Store the extracted phases as `spec_phases` for use in Phase 4 (Select Phases) and Phase 5 (Decompose Tasks).

---

## Phase 4: Select Phases

Select which implementation phases to generate tasks for. Three paths based on context:

### Path A — `--phase` argument provided

Skip interactive selection. Validate that each phase number in `selected_phases_cli` exists in `spec_phases`. If any phase number is invalid, report the valid range and stop.

### Path B — No `--phase`, spec has phases (2-3 phases)

Use a single AskUserQuestion with multiSelect:

```yaml
questions:
  - header: "Phases"
    question: "Which implementation phases should I generate tasks for?"
    options:
      - label: "All phases (Recommended)"
        description: "Generate tasks for all {N} phases at once"
      - label: "Phase 1: {name}"
        description: "{deliverable_count} deliverables — {completion_criteria_brief}"
      - label: "Phase 2: {name}"
        description: "{deliverable_count} deliverables — {completion_criteria_brief}"
      - label: "Phase 3: {name}"
        description: "{deliverable_count} deliverables — {completion_criteria_brief}"
    multiSelect: true
```

If user selects "All phases", generate for all. Otherwise generate only for the selected phase(s).

### Path C — No `--phase`, spec has 4+ phases

Two-step selection:

1. First ask "All phases or select specific?":
   ```yaml
   questions:
     - header: "Phases"
       question: "This spec has {N} implementation phases. Generate tasks for all or select specific phases?"
       options:
         - label: "All phases (Recommended)"
           description: "Generate tasks for all {N} phases"
         - label: "Select specific phases"
           description: "Choose which phases to generate tasks for"
       multiSelect: false
   ```

2. If "Select specific phases", show multiSelect with individual phases (up to 4 per AskUserQuestion, paginate if needed).

### Path D — No Section 9 / no phases

Skip selection entirely. Log: "No implementation phases found in spec. Generating tasks from features only."

Set `selected_phases = []` (all features will be processed without phase assignment).

### Path E — Merge mode with existing phases

When existing tasks with `spec_phase` metadata were found in Phase 2, show a specialized prompt:

```yaml
questions:
  - header: "Phases"
    question: "Previously generated phases detected. Which phases should I generate tasks for?"
    options:
      - label: "Remaining phases only (Recommended)"
        description: "Generate tasks for phases not yet created: {list of remaining phase names}"
      - label: "All phases (merge)"
        description: "Re-generate all phases, merging with existing tasks"
      - label: "Select specific phases"
        description: "Choose which phases to generate tasks for"
    multiSelect: false
```

If "Select specific phases", follow Path B/C selection flow.

---

## Phase 5: Decompose Tasks

### Phase-Aware Feature Mapping

When `spec_phases` is non-empty and phases were selected in Phase 4:

1. **Map features to phases** using the cross-reference from Phase Extraction:
   - Features explicitly referenced in phase deliverables → map to that phase
   - Features not referenced in any phase deliverable → assign to the earliest plausible phase (based on dependency layer: data models → Phase 1, UI → last phase)
2. **Filter to selected phases**: Only decompose features mapping to selected phases
3. **Deliverables as additional input**: For each selected phase, check if deliverables have technical tasks not covered by Section 5 feature decomposition. Create additional tasks from uncovered deliverables with `source_section: "9.{N}"`
4. **Assign phase metadata**: Every task gets `spec_phase` (integer) and `spec_phase_name` (string)

When `spec_phases = []` (no Section 9 in spec): Current behavior unchanged — decompose all features without phase assignment. The `spec_phase` and `spec_phase_name` fields are omitted entirely (backward compatible).

### Standard Layer Pattern

For each feature, apply the standard layer pattern:

```
1. Data Model Tasks
   └─ "Create {Entity} data model"

2. API/Service Tasks
   └─ "Implement {endpoint} endpoint"

3. Business Logic Tasks
   └─ "Implement {feature} business logic"

4. UI/Frontend Tasks
   └─ "Build {feature} UI component"

5. Test Tasks
   └─ "Add tests for {feature}"
```

### Task Structure

Follow the naming conventions from the claude-code-tasks reference (imperative `subject`, present-continuous `activeForm`). Each SDD task must include categorized acceptance criteria and testing requirements in its description:

```
subject: "Create User data model"
description: |
  {What needs to be done}

  {Technical details if applicable}

  **Acceptance Criteria:**

  _Functional:_
  - [ ] Core behavior criterion
  - [ ] Expected output criterion

  _Edge Cases:_
  - [ ] Boundary condition criterion
  - [ ] Unusual scenario criterion

  _Error Handling:_
  - [ ] Error scenario criterion
  - [ ] Recovery behavior criterion

  _Performance:_ (include if applicable)
  - [ ] Performance target criterion

  **Testing Requirements:**
  • {Inferred test type}: {What to test}
  • {Spec-specified test}: {What to test}

  Source: {spec_path} Section {number}
activeForm: "Creating User data model"
```

### SDD Task Metadata Extensions

In addition to the standard metadata keys from the claude-code-tasks reference (`priority`, `complexity`, `task_group`, `task_uid`), SDD tasks use these spec-specific keys:

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `source_section` | string | Yes | Spec section reference (e.g., "7.3 Data Models") |
| `spec_path` | string | Yes | Path to the source spec file |
| `feature_name` | string | Yes | Parent feature name from spec |
| `task_uid` | string | Yes | Composite key for merge mode: `{spec_path}:{feature}:{type}:{seq}` |
| `task_group` | string | Yes | Slug derived from spec title — REQUIRED for run-tasks `--task-group` filtering |
| `spec_phase` | integer | Conditional | Phase number from Section 9 (omit if no phases) |
| `spec_phase_name` | string | Conditional | Phase name from Section 9 (omit if no phases) |
| `produces_for` | string[] | Optional | IDs of downstream tasks that consume this task's output |

**`produces_for` Field:**

The `produces_for` field is an **optional** array of task IDs identifying tasks that directly consume this task's output. The `execute-tasks` orchestrator uses this field to inject the producer's result file content into the dependent task's prompt, giving downstream agents richer context than wave-granular `execution_context.md` merging alone provides.

- **Omit** if the task has no direct producer-consumer relationship with other tasks
- **Include** when the task's deliverable (model, schema, config, etc.) is directly referenced in another task's description
- Values are task IDs (set during Phase 9 after all tasks are created and IDs are known)

### Acceptance Criteria Categories

Group acceptance criteria into these categories:

| Category | What to Include |
|----------|-----------------|
| **Functional** | Core behavior, expected outputs, state changes |
| **Edge Cases** | Boundaries, empty/null, max values, concurrent operations |
| **Error Handling** | Invalid input, failures, timeouts, graceful degradation |
| **Performance** | Response times, throughput, resource limits (if applicable) |

### Testing Requirements Generation

Generate testing requirements by combining:

1. **Inferred from task type** (see `references/testing-requirements.md`):
   - Data Model → Unit + Integration tests
   - API Endpoint → Integration + E2E tests
   - UI Component → Component + E2E tests
   - Business Logic → Unit + Integration tests

2. **Extracted from spec** (Section 8 or feature-specific):
   - Explicit test types mentioned
   - Coverage targets
   - Critical path tests

Format as bullet points with test type and description:
```
**Testing Requirements:**
• Unit: Schema validation for all field types
• Integration: Database persistence and retrieval
• E2E: Complete login workflow (from spec 8.1)
```

### Priority Mapping

| Spec | Task Priority |
|-----|---------------|
| P0 (Critical) | `critical` |
| P1 (High) | `high` |
| P2 (Medium) | `medium` |
| P3 (Low) | `low` |

### Complexity Estimation

| Size | Scope |
|------|-------|
| XS | Single simple function (<20 lines) |
| S | Single file, straightforward (20-100 lines) |
| M | Multiple files, moderate logic (100-300 lines) |
| L | Multiple components, significant logic (300-800 lines) |
| XL | System-wide, complex integration (>800 lines) |

### Task UID Format

Generate unique IDs for merge tracking:
```
{spec_path}:{feature_slug}:{task_type}:{sequence}

Examples:
- specs/SPEC-Auth.md:user-auth:model:001
- specs/SPEC-Auth.md:user-auth:api-login:001
- specs/SPEC-Auth.md:session-mgmt:test:001
```

---

## Phase 6: Infer Dependencies

Apply automatic dependency rules:

### Layer Dependencies

```
Data Model → API → UI → Tests
```

- API tasks depend on their data models
- UI tasks depend on their APIs
- Tests depend on their implementations

Within-phase layer dependencies work unchanged regardless of phase selection.

### Phase Dependencies

When tasks have `spec_phase` metadata, apply cross-phase blocking based on three scenarios:

1. **Phase N-1 tasks exist in current generation**: Normal `blockedBy` — tasks in Phase N are blocked by Phase N-1 tasks
2. **Phase N-1 tasks exist from prior generation (merge mode)**: Create `blockedBy` relationships to existing Phase N-1 task IDs (found via `existing_phases_map` from Phase 2)
3. **Phase N-1 was NOT selected and no existing tasks found**: Do NOT add `blockedBy` to non-existent tasks. Instead:
   - Add a "Prerequisites" note to task descriptions listing assumed-complete deliverables from the missing phase
   - Emit a one-time warning: "Phase {N} tasks generated without Phase {N-1} predecessor tasks. Phase {N-1} deliverables are assumed complete."

### Explicit Spec Dependencies

Map Section 10 dependencies:
- "requires X" → blockedBy X
- "prerequisite for Y" → blocks Y

### Cross-Feature Dependencies

If features share:
- Data models: both depend on model creation
- Services: both depend on service implementation
- Auth: all protected features depend on auth setup

---

## Phase 7: Detect Producer-Consumer Relationships

After inferring `blockedBy` dependencies, identify which tasks produce output that is directly consumed by other tasks. These relationships are emitted as the `produces_for` field on producer tasks, enabling the `execute-tasks` orchestrator to inject richer upstream context into dependent task prompts.

### Detection Approach

Analyze the decomposed tasks and their `blockedBy` relationships to find producer-consumer pairs. A producer-consumer relationship exists when:

1. Task B is blocked by Task A (`blockedBy`), AND
2. Task A's deliverable is **directly referenced** in Task B's description — Task B cannot be implemented without the specific artifact Task A produces

**Conservative principle**: When uncertain whether a relationship is truly producer-consumer, omit `produces_for`. False positives add unnecessary context to dependent tasks; false negatives are harmless (the task still gets wave-granular context via `execution_context.md`).

### Producer-Consumer Patterns

Detect these common patterns:

| Producer Task Type | Consumer Task Type | Signal |
|---|---|---|
| **Data Model** | API/Service that uses the model | Consumer description references entity name, fields, or schema defined by producer |
| **Schema/Type Definition** | Implementation that implements the schema | Consumer implements interfaces, types, or contracts defined by producer |
| **Configuration/Infrastructure** | Tasks that consume the config | Consumer reads config values, connects to services, or uses infrastructure set up by producer |
| **Foundation/Framework** | Tasks that build on the foundation | Consumer extends base classes, uses utilities, or follows patterns established by producer |
| **API Endpoint** | UI/Frontend that calls the endpoint | Consumer calls specific endpoints or uses response formats defined by producer |
| **Migration/Setup** | Tasks that require the setup | Consumer reads from tables, uses resources, or depends on state created by producer |

### Detection Algorithm

For each pair of tasks where Task B has Task A in its `blockedBy` list:

1. **Check deliverable reference**: Does Task B's description explicitly reference an artifact that Task A creates?
   - Entity/model names: "using User model", "User schema", "User table"
   - Endpoint paths: "calls POST /auth/login", "uses /api/users response"
   - Config keys: "reads database config", "uses JWT secret"
   - File/module names: "imports from auth-middleware", "extends BaseService"

2. **Check layer relationship**: Is the dependency a direct layer-to-layer producer-consumer?
   - Data Model → API endpoint for that model (YES — API needs the model definition)
   - Data Model → Unrelated API endpoint (NO — just a layer ordering)
   - Config → Service using that config (YES — service consumes the config)
   - Auth setup → Feature behind auth (NO — auth is a gate, not a consumed output)

3. **Assign produces_for**: If the relationship is a direct producer-consumer, add Task B's ID to Task A's `produces_for` array

### Multi-Consumer Tasks

A single producer may have multiple consumers. For example, a "Create User data model" task may produce for both "Implement registration endpoint" and "Implement login endpoint". In this case, `produces_for` contains all consumer IDs:

```
produces_for: ["{registration_task_id}", "{login_task_id}"]
```

### Circular Production Prevention

`produces_for` follows the same acyclicity as `blockedBy`. Since `produces_for` is derived from `blockedBy` relationships (which are already validated for circular dependencies in Phase 5), circular production relationships cannot occur. If a `produces_for` relationship is detected outside of a `blockedBy` pair, skip it — the dependency inference already prevents circular `blockedBy`.

### Output

After detection, annotate each producer task in the internal task list with its `produces_for` array. Tasks with no producer-consumer relationships have no `produces_for` field (the field is omitted, not set to an empty array).

---

## Phase 8: Preview & Confirm

Before creating tasks, present a summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK GENERATION PREVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Spec: {spec_name}
Depth: {depth_level}
{If phases selected:}
Phases: {selected_count} of {total_count}

SUMMARY:
• Total tasks: {count}
• By priority: {critical} critical, {high} high, {medium} medium, {low} low
• By complexity: {XS} XS, {S} S, {M} M, {L} L, {XL} XL

{If phases selected:}
PHASES:
• Phase {N}: {phase_name} — {n} tasks
• Phase {M}: {phase_name} — {n} tasks

{If partial phases and predecessor phases not generated:}
PREREQUISITES:
• Phase {N-1}: {phase_name} — assumed complete (not in this generation)

FEATURES:
• {Feature 1} (Phase {N}) → {n} tasks
• {Feature 2} (Phase {M}) → {n} tasks
...

DEPENDENCIES:
• {n} dependency relationships inferred
• {m} producer-consumer relationships detected
• Longest chain: {n} tasks

FIRST TASKS (no blockers):
• {Task 1 subject} ({priority}, Phase {N})
• {Task 2 subject} ({priority}, Phase {M})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

When no phases are present, the `Phases:`, `PHASES:`, `PREREQUISITES:` sections and phase annotations on feature/task lines are omitted.

Then use AskUserQuestion to confirm:

```yaml
questions:
  - header: "Confirm"
    question: "Ready to create {n} tasks from this spec?"
    options:
      - label: "Yes, create tasks"
        description: "Create all tasks with dependencies"
      - label: "Show task details"
        description: "See full list before creating"
      - label: "Cancel"
        description: "Don't create tasks"
    multiSelect: false
```

If user selects "Show task details":
- List all tasks with subject, priority, complexity
- Group by feature
- Show dependency chains
- Then ask again for confirmation

---

## Phase 9: Create Tasks

### Fresh Mode (No Existing Tasks)

#### Step 1: Create All Tasks

Use TaskCreate for each task with the structured format, capturing the returned ID:

```
TaskCreate:
  subject: "Create User data model"
  description: |
    Define the User data model based on spec section 7.3.

    Fields:
    - id: UUID (primary key)
    - email: string (unique, required)
    - passwordHash: string (required)
    - createdAt: timestamp

    **Acceptance Criteria:**

    _Functional:_
    - [ ] All fields defined with correct types
    - [ ] Indexes created for email lookup
    - [ ] Migration script created

    _Edge Cases:_
    - [ ] Handle duplicate email constraint violation
    - [ ] Support maximum email length (254 chars)

    _Error Handling:_
    - [ ] Clear error messages for constraint violations

    **Testing Requirements:**
    • Unit: Schema validation for all field types
    • Unit: Email format validation
    • Integration: Database persistence and retrieval
    • Integration: Unique constraint enforcement

    Source: specs/SPEC-Auth.md Section 7.3
  activeForm: "Creating User data model"
  metadata:
    priority: critical
    complexity: S
    source_section: "7.3 Data Models"
    spec_path: "specs/SPEC-Auth.md"
    feature_name: "User Authentication"
    task_uid: "specs/SPEC-Auth.md:user-auth:model:001"
    task_group: "user-authentication"
    spec_phase: 1
    spec_phase_name: "Foundation"
```

**Important**: Track the mapping between task_uid and returned task ID for dependency setup.

**Phase metadata**: Include `spec_phase` and `spec_phase_name` on every task when the spec has implementation phases. Omit both fields entirely when no phases exist (backward compatible with phase-unaware tasks).

#### Step 2: Set Dependencies and produces_for

After all tasks are created, use TaskUpdate to set `blockedBy` dependencies and `produces_for` relationships using the task_uid-to-ID mapping:

```
TaskUpdate:
  taskId: "{api_task_id}"
  addBlockedBy: ["{model_task_id}"]
```

For tasks identified as producers in Phase 7, set `produces_for` via TaskUpdate:

```
TaskUpdate:
  taskId: "{model_task_id}"
  produces_for: ["{api_task_id}", "{service_task_id}"]
```

**Note**: Only set `produces_for` on tasks that were identified as producers in Phase 7. Tasks without producer-consumer relationships should not have `produces_for` set.

#### Step 3: Report Completion

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK CREATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created {n} tasks from {spec_name}
Set {m} dependency relationships
Set {p} producer-consumer relationships (produces_for)

Use TaskList to view all tasks.

RECOMMENDED FIRST TASKS (no blockers):
• {Task subject} ({priority}, {complexity})
• {Task subject} ({priority}, {complexity})

Run these tasks first to unblock others.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Merge Mode (Existing Tasks Found)

If existing tasks were detected in Phase 2, execute merge mode instead of fresh creation.

#### Step 1: Match Existing Tasks

Use task_uid metadata to match:
```
Existing task: task_uid = "specs/SPEC-Auth.md:user-auth:model:001"
New task: task_uid = "specs/SPEC-Auth.md:user-auth:model:001"
→ Match found
```

#### Step 2: Apply Merge Rules

| Existing Status | Action |
|-----------------|--------|
| `pending` | Update description if changed |
| `in_progress` | Preserve status, optionally update description |
| `completed` | Never modify |

#### Step 3: Create New Tasks

Tasks with no matching task_uid:
- Create as new tasks
- Set dependencies (may reference existing task IDs)

#### Step 4: Handle Potentially Obsolete Tasks

Tasks that exist but have no matching requirement in spec:
- List them to user
- Use AskUserQuestion to confirm:
  ```yaml
  questions:
    - header: "Obsolete?"
      question: "These tasks no longer map to spec requirements. What should I do?"
      options:
        - label: "Keep them"
          description: "Tasks may still be relevant"
        - label: "Mark completed"
          description: "Requirements changed, tasks no longer needed"
      multiSelect: false
  ```

#### Step 5: Report Merge

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK MERGE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• {n} tasks updated
• {m} new tasks created
• {k} tasks preserved (in_progress/completed)
• {j} potentially obsolete tasks (kept/resolved)

Total tasks: {total}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 10: Error Handling

### Spec Parsing Issues

If spec structure is unclear:
1. Note assumptions made
2. Flag uncertain tasks for review
3. Add `needs_review: true` to metadata

### Circular Dependencies

If circular dependency detected:
1. Log warning
2. Break at weakest link
3. Flag for human review

### Missing Information

If required information missing from spec:
1. Create task with available information
2. Add `incomplete: true` to metadata
3. Note what's missing in description

### Phase-Related Errors

**`--phase` provided but spec has no Section 9:**
Inform user: "The `--phase` argument was provided but this spec has no Implementation Plan (Section 9). Generating tasks from all features without phase filtering." Proceed without phase selection.

**`--phase` references non-existent phase numbers:**
Report valid phase numbers and stop: "Invalid phase number(s): {invalid}. This spec has phases: {list of valid phase numbers with names}."

**Section 9 format doesn't match expected patterns:**
Degrade gracefully — if phase headers can't be parsed, log a warning: "Section 9 found but phase structure could not be parsed. Generating tasks from features only." Set `spec_phases = []` and continue.

---

## Example Usage

### Basic Usage
```
/agent-alchemy-sdd:create-tasks specs/SPEC-User-Authentication.md
```

### With Relative Path
```
/agent-alchemy-sdd:create-tasks SPEC-Payments.md
```

### Generate tasks for a specific phase
```
/agent-alchemy-sdd:create-tasks specs/SPEC-Auth.md --phase 1
```

### Generate tasks for multiple phases
```
/agent-alchemy-sdd:create-tasks specs/SPEC-Auth.md --phase 1,2
```

### Re-running (Merge Mode)
```
/agent-alchemy-sdd:create-tasks specs/SPEC-User-Authentication.md
```
If tasks already exist for this spec, they will be intelligently merged.

---

## Important Notes

- Follow the naming and metadata conventions from the claude-code-tasks reference
- Never create duplicate tasks — check task_uid before creating (see anti-pattern AP-05)
- Preserve completed task status during merge — never modify completed tasks
- Flag uncertainty for human review rather than guessing
- Always include source section reference in description

### Anti-Pattern Validation

Before confirming task creation in Phase 8, validate against common anti-patterns. If issues are detected, load the full reference for remediation guidance:

```
Read ${CLAUDE_PLUGIN_ROOT}/../claude-tools/skills/claude-code-tasks/references/anti-patterns.md
```

Check for:
- **AP-01**: Circular dependencies — detect cycles in the dependency graph
- **AP-02**: Too-granular tasks — flag tasks that change fewer than ~10 lines
- **AP-05**: Duplicate task creation — verify task_uid uniqueness before creating
- **AP-07**: Missing task_group — every task MUST have `task_group` metadata

## Reference Files

- `references/decomposition-patterns.md` — Feature decomposition patterns by type
- `references/dependency-inference.md` — Automatic dependency inference rules
- `references/testing-requirements.md` — Test type mappings and acceptance criteria patterns
- `${CLAUDE_PLUGIN_ROOT}/../claude-tools/skills/claude-code-tasks/SKILL.md` — Task tool parameters, conventions, and patterns (loaded at init)
- `${CLAUDE_PLUGIN_ROOT}/../claude-tools/skills/claude-code-tasks/references/anti-patterns.md` — Common task anti-patterns (loaded on error/validation)
