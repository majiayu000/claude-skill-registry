# project-pipeline

---
description: Automated pipeline from SPEC.md to ready-to-execute tasks with human-in-loop confirmation
tags: [project-pipeline, orchestration, automation]
techStack: [all]
appliesTo: ["projects/*/", "start project", "initialize project"]
alwaysApply: false
---

## Prerequisites

### Claude Code Extended Context Configuration

**CRITICAL**: This orchestrator skill REQUIRES extended context settings:

```bash
MAX_THINKING_TOKENS=50000
CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000
```

**Why Extended Context is Critical**:
- **Resource Discovery (Step 2)**: Loads ADRs, skills, knowledge docs, and existing code patterns
- **Artifact Generation (Step 2)**: Calls `project-setup` which generates README, PLAN, CLAUDE.md
- **Task Decomposition (Step 3)**: Creates 50-200+ task files with tag-to-knowledge mapping
- **Context Enrichment**: Each task file includes applicable ADRs and knowledge docs
- **Pipeline Orchestration**: Chains multiple component skills sequentially

**Example Context Load**:
For AI Document Intelligence R1 project:
- spec.md: 2,306 words
- 4 ADRs loaded (ADR-013, ADR-014, ADR-015, ADR-016)
- 8 knowledge docs discovered
- 178 tasks generated with full context

**Verify settings before proceeding**:
```bash
# Windows PowerShell
echo $env:MAX_THINKING_TOKENS
echo $env:CLAUDE_CODE_MAX_OUTPUT_TOKENS

# Should output: 50000 and 64000
```

**If not set**, the pipeline may fail or produce incomplete results. See root [CLAUDE.md](../../../CLAUDE.md#development-environment) for setup instructions.

### Permission Mode: Plan Mode (RECOMMENDED)

**This skill performs planning and analysis. Use Plan Mode for safe exploration.**

```
⏸ PLAN MODE RECOMMENDED

Before starting this skill:
  1. Press Shift+Tab twice to enter Plan Mode
  2. Look for indicator: "⏸ plan mode on"
  3. Plan Mode ensures read-only operations during planning

WHY: Steps 1-3 analyze spec.md, discover resources, and generate artifacts.
     Plan Mode prevents accidental edits during exploration.

WHEN TO SWITCH: After Step 3 completes and you're ready for Step 4 (branch creation),
                press Shift+Tab to return to Auto-Accept Mode for git operations.
```

---

## Purpose

**Tier 2 Orchestrator Skill (RECOMMENDED)** - Streamlined end-to-end project initialization pipeline that chains: SPEC.md validation → Resource discovery → Artifact generation → Task decomposition → Feature branch → Ready to execute Task 001.

**Key Features**:
- Human-in-loop confirmations after each major step
- Automatic resource discovery (ADRs, skills, knowledge docs)
- Calls component skills (project-setup, task-create)
- Creates feature branch for isolation
- Optional auto-start of task 001

**Human-in-Loop**: After each step, present results and ask for confirmation before proceeding. Default to "proceed" (user just says 'y').

## When to Use

- User says "start project", "initialize project from spec", or "run project pipeline"
- Explicitly invoked with `/project-pipeline {project-path}`
- A `spec.md` file exists at `projects/{project-name}/spec.md`

## Pipeline Steps

### Step 1: Validate SPEC.md

**Action:**
```
LOAD: projects/{project-name}/spec.md

VALIDATE:
✓ File exists and is readable
✓ Contains required sections:
  - Executive Summary / Purpose
  - Scope definition
  - Technical approach
  - Success criteria
✓ Minimum 500 words (meaningful content)

IF validation fails:
  → STOP - List missing elements
  → Offer to help complete spec.md
```

**Output to User:**
```
✅ SPEC.md validated:
   - 2,306 words
   - All required sections present
   - Ready for planning

📋 Next Step: Generate PLAN.md from spec

[Y to proceed / refine to make changes / stop to exit]
```

**Wait for User**: `y` (proceed) | `refine {instructions}` | `stop`

---

### Step 1.5: Overlap Detection (Parallel Sessions)

**Purpose:** Detect potential file conflicts with active PRs before investing time in project setup.

**Action:**
```
CHECK for active PRs:
  gh pr list --state open --json number,title,headRefName,files

IDENTIFY likely files from spec.md:
  - Parse spec.md for mentioned components:
    • PCF controls → src/client/pcf/
    • API endpoints → src/server/api/
    • Dataverse plugins → src/solutions/
    • Shared libraries → src/*/shared/
    • Documentation → docs/, .claude/
  - List directories/files likely to be modified

COMPARE with active PRs:
  FOR EACH active PR:
    overlap = intersection(likely_project_files, pr_files)
    IF overlap is not empty:
      ADD to potential_conflicts list

CHECK other worktrees:
  git worktree list
  FOR EACH worktree (excluding current):
    CHECK branch name for active project
```

**Decision Tree:**
```
IF no active PRs with overlapping files:
  → Continue normally (no warning)

IF overlap detected:
  ⚠️ WARN user:
  "Potential file overlap detected with active PRs:

   PR #{number}: {title}
     Branch: {branch}
     Overlapping areas:
       - src/client/pcf/ (both projects touch PCF controls)
       - .claude/skills/ (both modify skills)

   Recommendations:
   1. Coordinate scope to avoid same-file edits
   2. Designate file ownership (Session A owns file X, Session B owns file Y)
   3. Plan to merge PR #{number} first, then rebase this project

   Proceed anyway? [Y to continue / stop to exit]"

  WAIT for user confirmation before continuing
```

**Output to User (if overlaps found):**
```
⚠️ Potential Overlap Detected

Your project (from spec.md) appears to touch:
  - src/client/pcf/ (new PCF control)
  - .claude/skills/ (skill updates)

Active PRs with overlapping files:
──────────────────────────────────
PR #98: chore: project planning updates
  Branch: work/project-planning-and-documentation
  Overlapping: .claude/skills/

Recommendations:
1. If PR #98 is close to merge → Wait for it, then start
2. If both sessions are yours → Coordinate file ownership
3. If proceeding → Plan to rebase after PR #98 merges

[Y to proceed with awareness / stop to wait]
```

**Note:** This step is informational—it doesn't block the pipeline. The goal is awareness so you can plan for sequential merges or file ownership.

---

### Step 2: Comprehensive Resource Discovery & Artifact Generation

**Purpose:** Load ALL implementation context (ADRs, skills, patterns, knowledge docs, code examples) for task creation.

**Action Part 1: Comprehensive Resource Discovery**
```
LOAD context:
  - projects/{project-name}/spec.md

DISCOVER RESOURCES (Comprehensive):
  1. IDENTIFY resource types from spec.md
     - Extract keywords (technologies, operations, feature types)
     - Identify components (API, PCF, plugins, storage, AI, jobs)

  2. LOAD applicable ADRs via adr-aware
     - Based on resource types in spec (API, PCF, Plugin, etc.)
     - Example: PCF control → ADR-006, ADR-011, ADR-012, ADR-021
     - Load FULL ADR content (not just constraints)

  3. SEARCH for applicable skills
     - Search .claude/skills/INDEX.md
     - Match tags, techStack in skill frontmatter
     - Example: "deploy to Dataverse" → dataverse-deploy skill

  4. SEARCH for knowledge docs and patterns
     - Search docs/ai-knowledge/guides/ for relevant procedures
     - Search docs/ai-knowledge/patterns/ for code patterns
     - Match technology names, patterns
     - Example: "Azure OpenAI" → openai, embeddings, streaming patterns

  5. FIND existing code examples
     - Search codebase for similar implementations
     - Identify canonical implementations to follow
     - Example: Existing PCF controls for reference

  6. DISCOVER applicable scripts (via script-aware)
     - READ scripts/README.md for script registry
     - Match spec keywords to script purposes:
       - PCF deployment → Deploy-PCFWebResources.ps1
       - API testing → Test-SdapBffApi.ps1
       - Custom pages → Deploy-CustomPage.ps1
       - Ribbon work → Export-EntityRibbon.ps1
     - Note scripts for inclusion in task files

OUTPUT: Comprehensive resource discovery summary
  - X ADRs loaded (with full content)
  - Y skills applicable (with file paths)
  - Z knowledge docs found (guides + patterns)
  - N code examples identified
  - M scripts available (for deployment/testing steps)

⚠️ **DIFFERENCE from design-to-spec Step 3**:
- design-to-spec: Preliminary (ADR constraints only for spec enrichment)
- project-pipeline: Comprehensive (full ADRs, patterns, code examples for implementation)
```

**Action Part 2: Generate Artifacts with Discovered Resources**
```
PREPARE context for project-setup:
  - spec.md content
  - Discovered resources summary (ADRs, skills, knowledge docs)

INVOKE: project-setup projects/{project-name}

This component skill generates:
  ✅ README.md (project overview, graduation criteria from spec)
  ✅ PLAN.md (implementation plan with WBS from spec)
  ✅ CLAUDE.md (AI context file from spec)
  ✅ current-task.md (active task state tracker - for context recovery)
  ✅ Folder structure (tasks/, notes/ with subdirectories)

AFTER project-setup completes:
  ENHANCE PLAN.md with discovered resources:
    - Insert "Discovered Resources" section in Architecture Context
    - List applicable ADRs with summaries
    - List relevant skills with purpose
    - List knowledge docs with topics
    - Update References section with all resource links

ENHANCE CLAUDE.md with discovered resources:
    - Populate "Applicable ADRs" section
    - Add resource file paths for quick reference
    - VERIFY "🚨 MANDATORY: Task Execution Protocol" section exists
      (should be auto-included from project-setup template)
    - If missing, add the mandatory task execution protocol section
```

**Output to User:**
```
✅ Resources discovered:
   - 4 ADRs identified (ADR-001, ADR-007, ADR-008, ADR-010)
   - 2 skills applicable (dataverse-deploy, adr-aware)
   - 3 knowledge docs found (SPAARKE-ARCHITECTURE.md, ...)
   - 2 scripts available (Deploy-PCFWebResources.ps1, Test-SdapBffApi.ps1)

✅ Artifacts generated:
   - README.md (project overview, graduation criteria)
   - PLAN.md (5 phases, WBS structure)
   - CLAUDE.md (AI context file)
   - Folder structure created

📄 Files created:
   - projects/{project-name}/README.md
   - projects/{project-name}/plan.md
   - projects/{project-name}/CLAUDE.md
   - projects/{project-name}/current-task.md (context recovery)
   - projects/{project-name}/tasks/ (empty, ready for task files)
   - projects/{project-name}/notes/ (with subdirectories)

📋 Next Step: Decompose PLAN.md into executable task files

[Y to proceed / review to view artifacts / refine {file} to edit / stop to exit]
```

**Wait for User**: `y` (proceed) | `review` (open PLAN.md) | `refine {instructions}` | `stop`

---

### Step 3: Generate Task Files

**Action:**
```
LOAD:
  - projects/{project-name}/plan.md (Phase Breakdown section)
  - docs/ai-knowledge/templates/task-execution.template.md (POML format)
  - Tag-to-knowledge mapping (from task-create skill)

REQUIREMENTS (from task-create):
  - Each task file MUST follow the task-execution.template.md structure (root <task id="..." project="...">)
  - Each task MUST include <knowledge><files> and it MUST NOT be empty
  - PCF tasks MUST include docs/ai-knowledge/guides/PCF-V9-PACKAGING.md and src/client/pcf/CLAUDE.md
  - Applicable ADRs MUST be included via docs/reference/adr/*.md (see task-create Step 3.5)

CREATE directory:
  - projects/{project-name}/tasks/

FOR each phase in PLAN.md:
  FOR each deliverable/objective:
    DECOMPOSE into discrete tasks (2-4 hour chunks)
    
    APPLY numbering:
      - Phase 1 → 001, 002, 003...
      - Phase 2 → 010, 011, 012...
      - Phase 3 → 020, 021, 022...
      - (10-gap for insertions)
    
    GENERATE .poml file:
      - Valid POML/XML format
      - <metadata> with tags, phase, estimate
      - <prompt> with goal, context, constraints
      - <knowledge> with auto-discovered files (based on tags)
      - <steps> with concrete actions
      - <tools> with Claude Code capabilities
      - <outputs> with expected artifacts
      - <acceptance-criteria> with verification steps

IDENTIFY task dependencies and parallel opportunities:
  - Mark explicit dependencies in task <metadata><dependencies>
  - Group independent tasks that CAN run in parallel
  - Flag tasks that BLOCK multiple downstream tasks (critical path)
  - See task-create Step 3.8 for parallel task grouping

ADD deployment tasks (per task-create Step 3.6):
  - After each phase that produces deployable artifacts
  - Tag: deploy

ADD UI test definitions for PCF/frontend tasks:
  - For tasks with tags: pcf, frontend, fluent-ui, e2e-test
  - Include <ui-tests> section in task POML with:
    • Test name and URL (environment placeholder if needed)
    • Step-by-step test actions (navigate, click, verify)
    • Expected outcomes
    • ADR-021 dark mode checks (for Fluent UI tasks)
  - Example UI test structure:
    <ui-tests>
      <test name="Component Renders">
        <url>https://{org}.crm.dynamics.com/main.aspx?...</url>
        <steps>
          <step>Navigate to form</step>
          <step>Verify control is visible</step>
          <step>Check console for errors</step>
        </steps>
        <expected>Control renders without console errors</expected>
      </test>
      <test name="Dark Mode Compliance">
        <steps>
          <step>Toggle dark mode in settings</step>
          <step>Verify colors adapt</step>
        </steps>
        <expected>All colors use semantic tokens per ADR-021</expected>
      </test>
    </ui-tests>
  - UI tests are executed by task-execute Step 9.7 via ui-test skill

ADD wrap-up task (mandatory per task-create Step 3.7):
  - Final task: 090-project-wrap-up.poml (or next available)
  - Updates README status to Complete
  - Creates lessons-learned.md
  - Archives project artifacts

CREATE: projects/{project-name}/tasks/TASK-INDEX.md
  - Registry of all tasks with status
  - Dependencies graph (which tasks block which)
  - Critical path (longest dependency chain)
  - High-risk items
  - **Parallel Groups**: Tasks that CAN run simultaneously
    Example format:
    ```markdown
    ## Parallel Execution Groups

    | Group | Tasks | Prerequisite | Notes |
    |-------|-------|--------------|-------|
    | A | 020, 021, 022 | 010 complete | Independent API endpoints |
    | B | 031, 032 | 030 complete | Separate UI components |
    ```
```

**Output to User:**
```
✅ Task files generated:
   - 178 tasks created in tasks/
   - TASK-INDEX.md created
   - All tasks in POML/XML format
   - Tag-to-knowledge mapping applied
   - 4 deployment tasks added (010-deploy, 020-deploy, 030-deploy, 040-deploy)
   - Wrap-up task added (090-project-wrap-up.poml)

📁 Files created:
   - projects/ai-document-intelligence-r1/tasks/TASK-INDEX.md
   - projects/ai-document-intelligence-r1/tasks/001-create-environment-variables.poml
   - ... (176 more tasks)
   - projects/ai-document-intelligence-r1/tasks/090-project-wrap-up.poml

✨ Project Ready for Execution!

📋 Next Step: Execute Task 001

To start: Just say "execute task 001" or "work on task 001"
Task-execute skill will automatically:
  - Load task file
  - Load knowledge files based on tags
  - Load applicable ADRs
  - Execute with full context

[Y to start task 001 / review {task-number} to view task / stop to exit]
```

**Wait for User**: `y` (proceed to branch creation) | `review {task-number}` | `stop`

---

### Step 4: Create Feature Branch

**Action:**
```
CREATE feature branch for this project:

BRANCH NAMING:
  feature/{project-name}  ← matches project folder name
  Example: feature/ai-document-intelligence-r1

GIT OPERATIONS:
  1. Create and checkout branch:
     git checkout -b feature/{project-name}

  2. Stage project files:
     git add projects/{project-name}/

  3. Commit with conventional commit format:
     git commit -m "feat({scope}): initialize {project-name} project

     - Created project artifacts (README, PLAN, CLAUDE.md)
     - Generated {X} task files
     - Project ready for implementation

     🤖 Generated with Claude Code"

  4. Push to remote with tracking:
     git push -u origin feature/{project-name}

  5. OPTIONAL - Create draft PR for visibility:
     gh pr create --draft \
       --title "feat({scope}): {project-name}" \
       --body "## Summary
Implementation of {project-name}

## Status
- [x] Project initialized
- [x] Tasks created ({X} tasks)
- [ ] Implementation in progress
- [ ] Code review
- [ ] Ready for merge

## Quick Links
- [Project README](projects/{project-name}/README.md)
- [Implementation Plan](projects/{project-name}/plan.md)
- [Task Index](projects/{project-name}/tasks/TASK-INDEX.md)

🤖 Generated with Claude Code"

WHY create branch at this point:
  - All artifacts and tasks are created (meaningful commit)
  - Isolates project work from master
  - Enables incremental commits during implementation
  - Draft PR provides team visibility
  - Clean merge when project completes
```

**Output to User:**
```
✅ Feature branch created:
   - Branch: feature/{project-name}
   - Initial commit: "feat({scope}): initialize {project-name} project"
   - Pushed to remote: origin/feature/{project-name}
   - Draft PR created: #{PR-number}

🔗 View PR: https://github.com/{org}/{repo}/pull/{PR-number}

📋 Next Step: Execute Task 001 (optional auto-start)

[Y to start task 001 / stop to exit]
```

**Wait for User**: `y` (start task 001) | `stop`

---

### Step 5: Execute Task 001 (Optional Auto-Start)

**Action:**
```
IF user said 'y':
  → INVOKE task-execute skill with projects/{project-name}/tasks/001-*.poml
  → task-execute will:
    1. UPDATE current-task.md:
       - Task ID: 001
       - Status: in-progress
       - Started: {timestamp}
    2. LOAD context:
       - Task file (POML)
       - Knowledge files (from <knowledge> section)
       - ADRs (via adr-aware based on tags)
       - Context from PLAN.md and README.md
    3. EXECUTE task steps, updating current-task.md after each step

PARALLEL TASK EXECUTION (when dependencies allow):
  If multiple tasks have no dependencies (or all dependencies satisfied):
  → CAN execute in parallel using Task tool with multiple subagent invocations
  → Example: Tasks 020, 021, 022 all have "dependencies: 010" satisfied
  → Send ONE message with THREE Task tool calls (subagent_type: general-purpose)
  → Each subagent runs task-execute for one task independently
  → Monitor completion via TaskOutput tool

  REQUIREMENTS for parallel execution:
  - All tasks must have dependencies satisfied (check TASK-INDEX.md)
  - Tasks must NOT modify the same files (check <relevant-files>)
  - Each task uses its own task-execute invocation
  - Track parallel tasks in current-task.md "Parallel Execution" section

IF user said 'stop':
  → OUTPUT:
    "✅ Project initialized and ready!

     current-task.md is set to:
       - Task ID: none
       - Status: none (waiting for first task)

     When ready to start:
     - Say: `work on task 001` or `execute task 001`
     - task-execute will update current-task.md and load all context

     To check status later: `/project-status {project-name}`"
```

**Note on current-task.md lifecycle:**
- Created by project-setup with status: "none" (no active task yet)
- When task 001 starts → status: "in-progress", steps/files/decisions tracked
- When task 001 completes → RESETS, advances to task 002 (status: "not-started")
- Continues until project complete (status: "none", next action: "run /repo-cleanup")

---

## Error Handling

**If spec.md missing:**
```
❌ SPEC.md not found at: projects/{project-name}/spec.md

Options:
1. If you have a human design document (design.md, .docx, .pdf):
   → Run: /design-to-spec projects/{project-name}
   → This transforms your design doc into an AI-optimized spec.md

2. Write spec.md manually with:
   - Executive Summary / Purpose
   - Scope definition
   - Technical approach
   - Success criteria

Then run: /project-pipeline projects/{project-name}

Need help writing spec.md? I can help with that first.
```

**If PLAN.md generation fails:**
```
⚠️ PLAN.md generation encountered issues.

Options:
1. 'retry' - Try generating again
2. 'manual' - I'll help you write PLAN.md interactively
3. 'stop' - Exit pipeline and address issues manually
```

**If task decomposition fails:**
```
⚠️ Task file generation encountered issues.

This usually means:
- PLAN.md needs more detail in Phase Breakdown section
- Deliverables not concrete enough

Options:
1. 'refine plan' - I'll help improve PLAN.md Phase Breakdown
2. 'manual tasks' - Create task files interactively
3. 'stop' - Exit and address manually
```

---

## Usage Examples

### Example 1: Standard Flow
```
User: "start project ai-document-intelligence-r1"

Agent: ✅ SPEC.md validated (2,306 words)
        📋 Next Step: Generate PLAN.md
        [Y to proceed]

User: "y"

Agent: ✅ PLAN.md generated (487 lines, 5 phases)
        📋 Next Step: Generate task files
        [Y to proceed]

User: "y"

Agent: ✅ 178 tasks generated
        ✨ Project ready!
        📋 Next Step: Execute Task 001
        [Y to start]

User: "y"

Agent: [Executes task 001 with full context loaded]
```

### Example 2: Review Before Proceeding
```
User: "initialize project from projects/new-feature/"

Agent: ✅ SPEC.md validated
        [Y to proceed]

User: "review"

Agent: [Opens SPEC.md for review]
        Ready to generate PLAN.md? [Y to proceed]

User: "y"

Agent: ✅ PLAN.md generated
        [Y to proceed / review to view plan]

User: "review"

Agent: [Opens PLAN.md]
        PLAN.md looks good? [Y to proceed / refine {section}]

User: "refine phase 2 - break down UI tasks more"

Agent: [Updates Phase 2 with more granular tasks]
        ✅ Phase 2 refined
        [Y to proceed]

User: "y"

Agent: ✅ Tasks generated
        [Y to start task 001]
```

### Example 3: Stop and Manual Control
```
User: "start project new-api-feature"

Agent: ✅ SPEC.md validated
        [Y to proceed]

User: "y"

Agent: ✅ PLAN.md generated
        [Y to proceed]

User: "stop"

Agent: ✅ Project initialized up to PLAN.md
        
        Files created:
        - projects/new-api-feature/PLAN.md
        - projects/new-api-feature/README.md
        
        When ready to continue:
        - Run: /task-create new-api-feature
        - Or: /project-pipeline new-api-feature (restart full pipeline)
```

---

## Integration with Existing Skills

This skill **orchestrates** by calling component skills:

- **design-to-spec**: **OPTIONAL PREDECESSOR** - Transforms human design docs into AI-optimized spec.md before this skill runs
- **adr-aware**: Auto-invoked during resource discovery (Step 2) for ADR loading
- **conflict-check**: **INTEGRATED** at Step 1.5 for PR overlap detection (parallel session awareness)
- **project-setup**: **CALLED** at Step 2 for artifact generation (README, PLAN, CLAUDE.md, folders)
- **task-create**: Concepts integrated and called at Step 3 for task decomposition
- **ui-test**: **TASK GENERATION** - Step 3 creates `<ui-tests>` sections for PCF/frontend tasks; executed by task-execute Step 9.7
- **task-execute**: **CALLED** at Step 5 if user confirms auto-start
- **push-to-github**: Concepts used at Step 4 for feature branch and commit

**Orchestration Pattern**:
```
design-to-spec (Tier 1 - Optional Predecessor)
  └─→ Transforms design.md → spec.md (if human design doc exists)
        │
        ▼
project-pipeline (Tier 2 - Orchestrator)
  ├─→ Step 2: CALLS project-setup (Tier 1 - Component)
  │     └─→ Generates artifacts
  ├─→ Step 3: CALLS task-create (Tier 1 - Component)
  │     ├─→ Generates task files
  │     └─→ Adds <ui-tests> sections for PCF/frontend tasks
  ├─→ Step 4: Feature branch creation
  └─→ Step 5: CALLS task-execute (Tier 2 - Orchestrator)
        ├─→ Executes first task
        └─→ Step 9.7: CALLS ui-test for PCF/frontend tasks

Result: Full project initialization with human confirmation at each major step
```

**Why call component skills?**
- Single responsibility: Each skill does one thing well
- Reusability: project-setup can be used standalone or by other orchestrators
- Maintainability: Changes to artifact generation happen in one place (project-setup)
- Testability: Component skills can be tested independently

---

## Success Criteria

Pipeline successful when:
- [ ] SPEC.md validated (Step 1)
- [ ] PR overlap check completed (Step 1.5 - informational)
- [ ] Resources discovered (ADRs, skills, knowledge docs) (Step 2)
- [ ] README.md created with graduation criteria (Step 2)
- [ ] PLAN.md created with all template sections and discovered resources (Step 2)
- [ ] CLAUDE.md created with project context (Step 2)
- [ ] Folder structure created (tasks/, notes/ with subdirs) (Step 2)
- [ ] All task .poml files created (Step 3)
- [ ] TASK-INDEX.md created (Step 3)
- [ ] Deployment tasks added (if applicable) (Step 3)
- [ ] UI test definitions added to PCF/frontend tasks (Step 3 - `<ui-tests>` sections)
- [ ] Wrap-up task added (090-project-wrap-up.poml) (Step 3)
- [ ] Feature branch created and pushed to remote (Step 4)
- [ ] Initial commit made with project artifacts (Step 4)
- [ ] User confirmed ready to execute Task 001 (or declined) (Step 5)

---

*For Claude Code: This is the recommended entry point for new projects with existing spec.md. Provides streamlined UX with human-in-loop confirmation.*
