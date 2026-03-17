---
name: create-tasks
description: Generate Claude Code native Tasks from an existing spec. Use when user says "create tasks", "generate tasks from spec", "spec to tasks", "task generation", or wants to decompose a spec into implementation tasks.
argument-hint: "[spec-path]"
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Read, Glob, Grep, TaskCreate, TaskUpdate, TaskList, TaskGet
arguments:
  - name: spec-path
    description: Path to the spec file to analyze for task generation
    required: true
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

## Workflow Overview

This workflow has eight phases:

1. **Validate & Load** — Validate spec file, read content, check settings, load reference files
2. **Detect Depth & Check Existing** — Detect spec depth level, check for existing tasks
3. **Analyze Spec** — Extract features, requirements, and structure from spec
4. **Decompose Tasks** — Break features into atomic tasks with acceptance criteria
5. **Infer Dependencies** — Map blocking relationships between tasks
6. **Preview & Confirm** — Show summary, get user approval before creating
7. **Create Tasks** — Create tasks via TaskCreate/TaskUpdate (fresh or merge mode)
8. **Error Handling** — Handle spec parsing issues, circular deps, missing info

---

## Phase 1: Validate & Load

### Validate Spec File

Verify the spec file exists at the provided path.

If the file is not found:
1. Check `.claude/claude-alchemy.local.md` for a default spec directory or output path, and try resolving the spec path against it
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

Check for optional settings at `.claude/claude-alchemy.local.md`:
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
- Inform user about merge behavior

Report to user:
```
Found {n} existing tasks for this spec:
• {pending} pending
• {in_progress} in progress
• {completed} completed

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
| **9.x Implementation Plan** | Phases → task grouping |
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

---

## Phase 4: Decompose Tasks

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

Each task must have categorized acceptance criteria and testing requirements:

```
subject: "Create User data model"              # Imperative mood
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
activeForm: "Creating User data model"         # Present continuous
metadata:
  priority: critical|high|medium|low           # Mapped from P0-P3
  complexity: XS|S|M|L|XL                      # Estimated size
  source_section: "7.3 Data Models"            # Spec section
  spec_path: "specs/SPEC-Example.md"            # Source spec
  feature_name: "User Authentication"          # Parent feature
  task_uid: "{spec_path}:{feature}:{type}:{seq}" # Unique ID
  task_group: "{spec-name}"                    # REQUIRED — Group from spec title
```

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

## Phase 5: Infer Dependencies

Apply automatic dependency rules:

### Layer Dependencies

```
Data Model → API → UI → Tests
```

- API tasks depend on their data models
- UI tasks depend on their APIs
- Tests depend on their implementations

### Phase Dependencies

If spec has implementation phases:
- Phase 2 tasks blocked by Phase 1 completion
- Phase 3 tasks blocked by Phase 2 completion

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

## Phase 6: Preview & Confirm

Before creating tasks, present a summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK GENERATION PREVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Spec: {spec_name}
Depth: {depth_level}

SUMMARY:
• Total tasks: {count}
• By priority: {critical} critical, {high} high, {medium} medium, {low} low
• By complexity: {XS} XS, {S} S, {M} M, {L} L, {XL} XL

FEATURES:
• {Feature 1} → {n} tasks
• {Feature 2} → {n} tasks
...

DEPENDENCIES:
• {n} dependency relationships inferred
• Longest chain: {n} tasks

FIRST TASKS (no blockers):
• {Task 1 subject} ({priority})
• {Task 2 subject} ({priority})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

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

## Phase 7: Create Tasks

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
```

**Important**: Track the mapping between task_uid and returned task ID for dependency setup.

#### Step 2: Set Dependencies

After all tasks are created, use TaskUpdate to set dependencies:

```
TaskUpdate:
  taskId: "{api_task_id}"
  addBlockedBy: ["{model_task_id}"]
```

#### Step 3: Report Completion

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK CREATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created {n} tasks from {spec_name}
Set {m} dependency relationships

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

## Error Handling

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

---

## Example Usage

### Basic Usage
```
/claude-alchemy-sdd:create-tasks specs/SPEC-User-Authentication.md
```

### With Relative Path
```
/claude-alchemy-sdd:create-tasks SPEC-Payments.md
```

### Re-running (Merge Mode)
```
/claude-alchemy-sdd:create-tasks specs/SPEC-User-Authentication.md
```
If tasks already exist for this spec, they will be intelligently merged.

---

## Important Notes

- Never create duplicate tasks — check task_uid before creating
- Preserve completed task status during merge — never modify completed tasks
- Flag uncertainty for human review rather than guessing
- Always use imperative mood for subjects ("Create X" not "X creation")
- Always include activeForm in present continuous ("Creating X")
- Always include source section reference in description

## Reference Files

- `references/decomposition-patterns.md` — Feature decomposition patterns by type
- `references/dependency-inference.md` — Automatic dependency inference rules
- `references/testing-requirements.md` — Test type mappings and acceptance criteria patterns
