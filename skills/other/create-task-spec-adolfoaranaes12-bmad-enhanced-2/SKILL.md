---
name: create-task-spec
description: Create hyper-detailed task specifications with embedded context, eliminating implementation lookups. This skill should be used for breaking features into implementable tasks with complete architecture references.
acceptance:
  - task_file_created: "Task specification file created in configured location"
  - context_embedded: "All technical context embedded with source references"
  - tasks_defined: "3-15 sequential tasks with validation checkpoints"
  - user_approved: "User reviewed and approved specification"
inputs:
  requirement:
    type: string
    required: true
    description: "Feature or requirement to implement"
  priority:
    type: string
    required: false
    description: "Priority level (P0/P1/P2/P3)"
    default: "P2"
outputs:
  task_file:
    type: string
    description: "Path to created task specification file"
  task_id:
    type: string
    description: "Generated task ID (e.g., task-006)"
  task_count:
    type: number
    description: "Number of tasks in breakdown"
  status:
    type: string
    description: "Task status (Draft or Approved)"
telemetry:
  emit: "skill.create-task-spec.completed"
  track:
    - task_id
    - task_count
    - subtask_count
    - priority
    - status
    - duration_ms
---

# Create Task Specification Skill

## Purpose

Create hyper-detailed task specifications that embed ALL context needed for implementation, eliminating the need for developers to search for information during coding.

**Core Capabilities:**
- Requirement gathering and clarification
- Architecture context extraction with source references
- Component analysis (data models, APIs, UI)
- Sequential task breakdown with validation checkpoints
- Self-contained specifications

**BMAD Pattern (Key Innovation):**
- SM reads PRD + Architecture + Previous task notes
- Creates detailed task spec with embedded context
- Dev reads ONLY task spec (no architecture lookup)
- Result: Context never lost, implementation never blocked

## Prerequisites

- Configuration file (`.claude/config.yaml`) with task settings
- Task template (`.claude/templates/task-spec.md`)
- Architecture documentation (optional but recommended)
- Project coding standards

---

## Workflow

### Step 0: Load Configuration and Validate Prerequisites

**Action:** Load configuration and verify prerequisites.

**Execute:**
```bash
python .claude/skills/bmad-commands/scripts/read_file.py \
  --path .claude/config.yaml \
  --output json
```

**Extract:** documentation.architecture, development.alwaysLoadFiles, development.taskLocation, templates.taskSpec

**Verify:** Task location exists, template exists, determine next task ID

**Halt if:** Config missing, template missing, cannot determine task ID

**See:** `references/templates.md` for configuration format and `references/requirements-gathering-guide.md` for requirement clarification

---

### Step 1: Gather Requirements from User

**Action:** Clarify requirement, acceptance criteria, and priority.

**Ask user:**
1. **What needs to be implemented?**
   - Feature description
   - Problem it solves
   - Primary user/beneficiary

2. **What defines "done"?**
   - Testable outcomes
   - Acceptance criteria (2-5 specific criteria)
   - Edge cases to consider

3. **Priority and complexity?**
   - Priority: P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)
   - Complexity: Simple | Medium | Complex
   - Related epic/feature

**Confirm understanding:**
- Restate as user story: As a [role], I want [action], so that [benefit]
- Verify acceptance criteria
- Get approval to proceed

**Halt if:**
- User cannot articulate requirement clearly
- Acceptance criteria are ambiguous
- User does not approve proceeding

**See:** `references/requirements-gathering-guide.md` for detailed gathering techniques

---

### Step 2: Load Architecture Context

**Action:** Load architecture documentation and previous task learnings.

**Load files:**

1. **Always-required files** (coding standards):
   ```bash
   python .claude/skills/bmad-commands/scripts/read_file.py \
     --path {always_load_file} \
     --output json
   ```

2. **Architecture documentation**:
   - Read `documentation.architecture` files
   - Extract: System design, patterns, conventions

3. **Previous task insights**:
   - Read most recent task file from `taskLocation`
   - Extract: Completion notes, lessons learned, patterns

**Context categories:** Tech stack, project structure, coding standards, testing strategy, data models, API specs, component specs, patterns

**CRITICAL RULES:** ONLY use information from source documents, NEVER invent details, ALWAYS cite sources, note when info missing

**See:** `references/context-extraction-guide.md` for detailed extraction strategies and `references/templates.md` for context format examples

---

### Step 3: Analyze Relevant Components

**Action:** Identify affected components and extract specific technical details.

**Identify components:**
- What data models are involved?
- What API endpoints need creation/modification?
- What UI components are affected?
- What external services are used?

**Extract details:** Data models (schemas, validation, relationships), API specs (endpoints, request/response, auth, errors), component specs (location, props, state, styling), file locations (exact paths), constraints (performance, security, reliability, testing)

**All extractions must cite:** [Source: filename#section]

**See:** `references/context-extraction-guide.md` for analysis patterns and `references/templates.md` for extraction format examples

---

### Step 4: Create Sequential Task Breakdown

**Action:** Break requirement into 3-15 sequential tasks with subtasks.

**Task breakdown:**

1. **Break into 3-15 tasks:**
   - Each task implements specific functionality
   - Tasks build on each other logically
   - Each task maps to one or more acceptance criteria

2. **Create subtasks for each task:**
   - Specific implementation steps
   - Test writing requirements
   - Validation checkpoints

3. **Structure in implementation order:**
   - Data layer first (models, migrations)
   - Business logic second (services, utilities)
   - API layer third (routes, controllers)
   - UI layer fourth (components, pages)
   - Integration last (E2E tests, documentation)

4. **Link to acceptance criteria:** Example: "Task 1: Create user model (AC: 1, 2)"

**Halt if:** Cannot break down coherently, >15 tasks (too complex), <3 tasks (too simple)

**See:** `references/task-breakdown-guide.md` for detailed strategies and `references/templates.md` for task structure examples

---

### Step 5: Populate Task Specification Template

**Action:** Generate task file from template with all context embedded.

**Load template:**
```bash
python .claude/skills/bmad-commands/scripts/read_file.py \
  --path .claude/templates/task-spec.md \
  --output json
```

**Replace placeholders:** task_id, title, date, priority, status, user_story, acceptance_criteria, context, tasks, validation

**Context must include:** Previous insights, data models, API specs, component specs, file locations, testing requirements, constraints - ALL with [Source: filename#section] references

**See:** `references/templates.md` for placeholder examples and formats

---

### Step 6: Validate Task Specification Completeness

**Action:** Verify all required elements are present and properly formatted.

**Validation checklist:**

**Required Sections:**
- [ ] Status (Draft)
- [ ] Objective (clear user story)
- [ ] Acceptance Criteria (2-5 specific criteria)
- [ ] Context section with embedded details
- [ ] Tasks / Subtasks (3-15 tasks)
- [ ] Implementation Record (empty placeholder)

**Context Completeness:**
- [ ] Previous insights referenced
- [ ] Data models included (if applicable)
- [ ] API specs included (if applicable)
- [ ] Component specs included (if applicable)
- [ ] File locations specified
- [ ] Testing requirements documented
- [ ] All context has [Source: ...] references

**Task Quality:**
- [ ] Tasks in logical implementation order
- [ ] Each task linked to acceptance criteria
- [ ] Subtasks include test writing steps
- [ ] Validation checkpoints included
- [ ] File paths are specific, not generic

**Halt if:**
- Critical sections missing
- Context lacks source references
- Tasks are ambiguous or generic
- No validation checkpoints

**See:** `references/validation-approval-guide.md` for validation details

---

### Step 7: Save Task Specification and Get User Approval

**Action:** Save task file and present summary for approval.

**Save file:**
```bash
python .claude/skills/bmad-commands/scripts/write_file.py \
  --path {taskLocation}/{task_id}.md \
  --content "{task_spec}" \
  --output json
```

**Present summary:** Show task ID, objective, acceptance criteria, task breakdown, embedded context sources, and request approval.

**Update status if approved:** Change from "Draft" to "Approved"

**See:** `references/templates.md` for complete summary format and `references/validation-approval-guide.md` for approval workflow

---

## Output

Return structured output with task file path, task ID, task count, status, and telemetry metrics.

**See:** `references/templates.md` for complete output format

---

## Best Practices

1. **Context Embedding is Critical** - Implementation should never need architecture docs
2. **Be Specific, Not Generic** - Exact file paths, schemas, API specs
3. **Source Everything** - Cite [Source: filename#section] for all technical details
4. **Task Granularity** - 3-15 tasks (>15 too complex, <3 too simple)

**See:** `references/task-breakdown-guide.md` for detailed practices

---

## Routing Guidance

**Use this skill when:**
- Breaking features into implementable tasks
- Creating detailed specifications for development
- Embedding architectural context for implementation
- Need clear, unambiguous work items

**Always use before:**
- execute-task skill (implementation)
- Task must be "Approved" status

**Do not use for:**
- Quick bug fixes (too much overhead)
- Urgent hotfixes (too structured)
- Exploratory coding (too constrained)

---

## Reference Files

- `references/requirements-gathering-guide.md` - Clarifying requirements, acceptance criteria, user stories
- `references/context-extraction-guide.md` - Loading architecture, extracting technical details, sourcing
- `references/task-breakdown-guide.md` - Creating sequential tasks, granularity, validation checkpoints
- `references/validation-approval-guide.md` - Completeness validation, saving, approval workflow
- `references/templates.md` - Task spec template, output format, placeholder examples, configuration format

---

## Using This Skill

Invoked with `requirement` input (feature description) and optional `priority` (P0-P3)

---

*Part of BMAD Enhanced Planning Suite*
