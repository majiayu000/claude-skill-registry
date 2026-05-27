# design-to-project

---
description: Full AI-AGENT-PLAYBOOK orchestration - transforms a design specification into project artifacts and begins implementation
tags: [design, planning, project-init, tasks, implementation, orchestration]
techStack: [all]
appliesTo: ["projects/*/spec.md", "implement spec", "design to project"]
alwaysApply: false
---

## Purpose

Orchestrates the complete transformation of a Detailed Design Specification into executable project artifacts. This is the master skill that sequences `project-init`, `task-create`, and implementation workflows following the 5-phase AI-AGENT-PLAYBOOK.

## When to Use

- User provides a design specification (.docx, .md, or inline text)
- User says "implement this spec", "turn this into a project", or "follow the playbook"
- Explicitly invoked with `/design-to-project {spec-path}`
- Starting a new feature from a completed design document

## Inputs Required

| Input | Required | Source |
|-------|----------|--------|
| Project path | Yes | Path to `projects/{project-name}/` folder (must contain spec.md) |
| Target completion date | No | User provided or infer from spec |
| Project owner | No | User name or "unassigned" |

### Design Spec Location Convention

Design specs live **with their project** at `projects/{project-name}/spec.md`.

**Workflow:**
1. Operator creates folder: `projects/{descriptive-name}/`
2. Operator places spec: `projects/{project-name}/spec.md`
3. Invoke: `/design-to-project projects/{project-name}`
4. Skill derives project name from folder and runs full pipeline

## Phase Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESIGN-TO-PROJECT PIPELINE                   │
├─────────────────────────────────────────────────────────────────┤
│ Phase 1: INGEST      → Extract key info from design spec       │
│ Phase 2: CONTEXT     → Gather ADRs, architecture, existing code │
│ Phase 3: GENERATE    → Create README, plan.md, task files       │
│ Phase 4: VALIDATE    → Cross-reference checklist before coding  │
│ Phase 5: IMPLEMENT   → Execute tasks with context management    │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow

### Phase 1: Ingest Design Specification

#### Step 1.1: Acquire Spec
```
IF project path provided (e.g., projects/sdap-fileviewer-enhancements-1):
  EXTRACT project-name from folder name
  VERIFY projects/{project-name}/spec.md exists
  LOAD spec.md
ELSE:
  ASK: "Please provide the project path (e.g., projects/my-feature)"

IF spec.md not found:
  STOP: "spec.md not found at projects/{project-name}/spec.md
         Please create the project folder and add spec.md first."
```

#### Step 1.2: Extract Key Information
```
PARSE spec for these sections:

| Field | Look For | Required |
|-------|----------|----------|
| Feature Name | Title, "Overview" section | Yes |
| Problem Statement | "Problem", "Background", "Current State" | Yes |
| Solution Approach | "Solution", "Approach", "Design" | Yes |
| Data Model | "Data Model", "Entities", "Schema" | If applicable |
| API Endpoints | "API", "Endpoints", "Contracts" | If applicable |
| UI Components | "UI", "Screens", "Components" | If applicable |
| Acceptance Criteria | "Acceptance Criteria", "Requirements" | Yes |
| NFRs | "NFRs", "Performance", "Security" | If specified |
```

#### Step 1.3: Summarize Understanding
```markdown
## Design Spec Summary

**Feature**: {Feature Name}
**Problem**: {1-2 sentence problem statement}
**Solution**: {1-2 sentence solution approach}

**Key Components**:
- {Component 1 - type: API/PCF/Plugin/etc.}
- {Component 2}
- {Component 3}

**Estimated Complexity**: {Low | Medium | High}
**Basis**: {Why this complexity level}

Proceeding to Phase 2: Context Gathering...
```

### Phase 2: Gather Context

#### Step 2.1: Discover Related Resources

**Search for related skills and knowledge docs:**

1. **Extract keywords from spec.md:**
   - Technology names (e.g., "Azure OpenAI", "Dataverse", "React", "PCF")
   - Feature types (e.g., "API endpoint", "PCF control", "plugin")
   - Operations (e.g., "deploy", "authentication", "caching")

2. **Search `.claude/skills/INDEX.md`:**
   - Look for skills with matching `tags` or `techStack` in their YAML frontmatter
   - Read relevant skill files for patterns and procedures
   - Example: If spec mentions "PCF control" → load relevant PCF skills

3. **Search `docs/ai-knowledge/`:**
   - Look for guides matching technologies or patterns in spec
   - Load relevant architecture docs, guides, and standards

**Output:** List of discovered skills and knowledge docs to use throughout pipeline.

#### Step 2.2: Check ADRs
```
READ: docs/ai-knowledge/CLAUDE.md for relevant articles
READ: docs/reference/adr/ index

FOR each technology in spec:
  MATCH to relevant ADRs:
    - PCF control → ADR-006, ADR-011, ADR-012
    - API endpoint → ADR-001, ADR-007, ADR-008, ADR-010
    - Dataverse plugin → ADR-002
    - Caching → ADR-009
    - Authorization → ADR-003, ADR-008

OUTPUT:
  | ADR | Title | Constraint for This Project |
  |-----|-------|----------------------------|
  | ... | ... | {specific constraint} |
```

#### Step 2.2: Find Reusable Code
```
SEARCH src/ for similar implementations:
  - PCF controls: src/client/pcf/
  - API patterns: src/server/api/
  - Shared libraries: src/client/shared/, src/server/shared/

OUTPUT:
  | Component | Location | How to Reuse |
  |-----------|----------|--------------|
  | ... | ... | ... |
```

#### Step 2.3: Load Knowledge Articles
```
BASED ON technologies in spec, load:
  - PCF: docs/ai-knowledge/guides/ PCF-related
  - Auth: docs/ai-knowledge/standards/oauth-*, auth-*
  - SDAP: docs/ai-knowledge/architecture/sdap-*

TRACK context usage - if > 50%:
  → Summarize key points
  → Reference file paths for later
  → Don't load full content
```

#### Step 2.4: Context Summary
```markdown
## Context Summary

**Applicable ADRs**: ADR-006, ADR-008, ADR-012 (etc.)

**Reusable Components**:
- {Component}: {brief description}
- {Component}: {brief description}

**Key Knowledge Articles**:
- `docs/ai-knowledge/architecture/{article}` - {key insight}
- `docs/ai-knowledge/standards/{article}` - {key insight}

**Architecture Fit**:
{How this feature fits into existing system}

Proceeding to Phase 3: Generate Artifacts...
```

### Phase 3: Generate Project Artifacts

#### Step 3.1: Invoke project-init
```
INVOKE: /project-init {project-name}

WITH context:
  - Design spec summary from Phase 1
  - ADR constraints from Phase 2
  - Complexity estimate from Phase 1

VERIFY outputs:
  - projects/{project-name}/spec.md (input - already existed)
  - projects/{project-name}/README.md
  - projects/{project-name}/plan.md
  - projects/{project-name}/CLAUDE.md
  - projects/{project-name}/tasks/
```

#### Step 3.2: Enrich README.md
```
ENHANCE README.md with Phase 2 findings:
  - Add "Key Decisions" section linking ADRs
  - Add "Dependencies" section with reusable components
  - Add "Risks" section based on complexity and dependencies
```

#### Step 3.3: Complete plan.md
```
ENHANCE plan.md with:
  - Executive Summary from spec
  - Solution Overview with architecture fit
  - WBS phases based on spec sections:

| Spec Section | Generates Phase |
|--------------|-----------------|
| Data Model | Phase: Entity/Schema Setup |
| API Endpoints | Phase: API Development |
| UI Components | Phase: UI Development |
| Integration | Phase: Integration & Wiring |
| Security | Phase: Auth Implementation |
| Testing | Phase: Validation |

APPLY estimation heuristics:
  - Simple CRUD endpoint: 0.5-1 day
  - Complex endpoint with auth: 1-2 days
  - PCF component (simple): 2-3 days
  - PCF component (complex): 3-5 days
  - Integration: 1-2 days
  - Unit tests: 0.5 day per component
  - Integration tests: 1-2 days
```

#### Step 3.4: Invoke task-create
```
INVOKE: /task-create {project-name}

VERIFY outputs:
  - tasks/TASK-INDEX.md exists
  - Task files created for each WBS phase
  - Dependencies mapped correctly
```

#### Step 3.5: Create Feature Branch
```
CREATE feature branch for this project:

git checkout -b feature/{project-name}

WHY at this point:
  - All artifacts created (README, plan, tasks)
  - Ready for commits that represent meaningful work
  - PR can be created as draft for visibility

NAMING convention:
  - feature/{project-name}  ← matches project folder name
  - Example: feature/ai-document-summary

COMMIT initial artifacts:
  git add projects/{project-name}/
  git commit -m "feat({scope}): initialize {project-name} project"
  git push -u origin feature/{project-name}

OPTIONAL - Create draft PR:
  gh pr create --draft --title "feat({scope}): {project-name}" \
    --body "## Summary\nImplementation of {project-name}\n\n## Status\n- [x] Project initialized\n- [ ] Implementation in progress\n- [ ] Code review\n- [ ] Ready for merge"
```

### Phase 4: Validate Before Implementation

#### Step 4.1: Cross-Reference Checklist
```
VALIDATE all items:
  
□ ADR Compliance
  - Plan phases don't violate ADR constraints
  - Technology choices align with ADRs
  - Example: PCF uses v9 Fluent UI (ADR-006)

□ Reuse Maximized
  - Shared components referenced in tasks
  - No reinventing existing utilities
  - @spaarke/ui-components used where applicable

□ Scope Clear
  - In-scope items listed in README
  - Out-of-scope explicitly stated
  - No ambiguous deliverables

□ Acceptance Testable
  - Each criterion in README is measurable
  - Tasks include verification steps
  - "Done" is unambiguous

□ Dependencies Identified
  - All external dependencies listed
  - Blocking dependencies noted in tasks
  - Environment requirements documented

□ Risks Mitigated
  - High/Critical risks have mitigation plans
  - Technical debt acknowledged
  - Unknowns surfaced
```

#### Step 4.2: Output Ready Summary
```markdown
## ✅ Ready for Development

**Project**: {feature-name}
**Location**: docs/projects/{feature-name}/

## ✅ Ready for Development

**Project**: {project-name}
**Location**: projects/{project-name}/

**Documents Created**:
- ✅ spec.md - Design specification (source of truth - input)
- ✅ README.md - Project overview, scope, graduation criteria
- ✅ plan.md - Implementation plan with WBS
- ✅ CLAUDE.md - AI context file
- ✅ tasks/TASK-INDEX.md - Task tracker
- ✅ {N} task files in tasks/

**Applicable ADRs**: {list}

**Reusable Components**:
- {component} ({purpose})
- {component} ({purpose})

**Estimated Effort**: {X} days ({Y} tasks)

**First Task**: `tasks/001-{slug}.md` - {title}

**Validation Checklist**: All items passed ✅

---

Ready to begin implementation? Reply "go" to start Phase 5.
```

### Phase 5: Implement (Task Execution)

#### Step 5.0: Context Management (CRITICAL)
```
BEFORE each task and AFTER each subtask:

CHECK context usage:
  < 50%  → ✅ Proceed normally
  50-70% → ⚠️ Monitor, wrap up current subtask soon
  > 70%  → 🛑 STOP - Create handoff summary
  > 85%  → 🚨 CRITICAL - Immediate handoff

IF context reset needed:
  CREATE handoff summary (see Handoff Protocol below)
  OUTPUT: "Context limit reached. Handoff created. Start new chat."
```

#### Step 5.1: Execute Tasks
```
FOR each task in execution order:
  1. LOAD task file from tasks/{NNN}-{slug}.md
  2. CHECK dependencies are met
  3. GATHER resources (ADRs, patterns, related code)
  4. EXECUTE steps from <steps> section
  5. VERIFY outputs from <outputs> section
  6. UPDATE task status to "completed"
  7. CHECK context → reset if > 70%
```

#### Step 5.2: Apply Conventions
```
ALWAYS APPLY spaarke-conventions skill during implementation:
  - File naming conventions
  - Code patterns (.NET, TypeScript)
  - Error handling patterns
  - Async patterns

REFER TO:
  - .claude/skills/spaarke-conventions/SKILL.md
  - Root CLAUDE.md for standards
```

#### Step 5.3: Code Review Gate
```
AFTER implementing code:
  RUN: /code-review {changed-files}
  
IF critical issues found:
  FIX before marking task complete
  
IF warnings found:
  NOTE in task completion summary
```

## Handoff Protocol

When context reaches 70%, create handoff summary:

```markdown
## Handoff Summary - {project-name}

**Context Reset Trigger**: {current-task} at {step}
**Date**: {timestamp}

### Completed
- ✅ Phase 1: Ingest - {summary}
- ✅ Phase 2: Context - {summary}
- ✅ Phase 3: Generate - {artifacts created}
- ✅ Phase 4: Validate - {checklist passed}
- 🔄 Phase 5: Implement - {tasks completed}

### Current State
**Current Task**: {task-id} - {task-title}
**Current Step**: {step number/description}
**Files Modified**: {list}
**Tests Status**: {passing/failing}

### To Continue
1. Load: docs/projects/{project-name}/CLAUDE.md
2. Load: tasks/{current-task-id}.md
3. Resume at step: {step}
4. Remaining tasks: {list task IDs}

### Key Decisions Made
- {decision 1 with rationale}
- {decision 2 with rationale}

### Warnings/Issues
- {any blockers or concerns}
```

## Conventions

### Project Naming
- Derive from design spec title
- Use kebab-case
- Examples: `universal-quick-create`, `document-sync-worker`

### Phase Transitions
- Always output status when moving between phases
- Wait for user confirmation before Phase 5 (implementation)
- Create handoff if interrupted

### Context Efficiency
- Summarize verbose specs, don't quote in full
- Reference file paths instead of loading full content when >50% context
- Prioritize: ADR constraints > reusable code > knowledge articles

## Resources

### Templates Used
- `docs/ai-knowledge/templates/project-README.template.md`
- `docs/ai-knowledge/templates/project-plan.template.md`
- `docs/ai-knowledge/templates/task-execution.template.md`

### Skills Orchestrated
- **project-init**: Phase 3 - folder structure and initial artifacts
- **task-create**: Phase 3 - task decomposition
- **code-review**: Phase 5 - quality gate before task completion
- **spaarke-conventions**: Phase 5 - always-apply during implementation
- **adr-check**: Phase 5 - architecture validation
- **repo-cleanup**: Phase 5 (wrap-up) - repository hygiene after project completion

### Reference Playbook
- `docs/ai-knowledge/templates/AI-AGENT-PLAYBOOK.md` - Full playbook documentation

## Examples

### Example 1: Full Pipeline
**Trigger**: "Here's the design spec for Universal Quick Create PCF. Transform it to a project."

**Process**:
1. Phase 1: Extract PCF feature details, data model, acceptance criteria
2. Phase 2: Identify ADR-006, ADR-011, ADR-012; find existing PCF patterns
3. Phase 3: Create `docs/projects/universal-quick-create/` with all artifacts
4. Phase 4: Validate checklist, output ready summary
5. Phase 5: User confirms, begin task execution

### Example 2: Partial Execution
**Trigger**: "/design-to-project but stop after planning"

**Process**:
1. Execute Phases 1-4 only
2. Output ready summary with "Reply 'go' to begin implementation"
3. Wait for user

### Example 3: Resume from Handoff
**Trigger**: "Continue from the handoff summary you created"

**Process**:
1. Load project CLAUDE.md
2. Load current task file
3. Resume at indicated step
4. Continue Phase 5 execution

## Validation Checklist

Before declaring project ready for implementation:
- [ ] Design spec fully ingested (all sections extracted)
- [ ] All applicable ADRs identified
- [ ] Reusable components catalogued
- [ ] README.md has graduation criteria
- [ ] plan.md has complete WBS with estimates
- [ ] Task files created with POML format
- [ ] Dependencies form valid execution order
- [ ] Cross-reference checklist passed
- [ ] User informed of effort estimate
