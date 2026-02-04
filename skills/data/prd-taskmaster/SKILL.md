---
name: PRD Generator for TaskMaster
description: Smart PRD generator with TaskMaster integration. Detects existing PRDs and offers execute/update/replace options. Generates comprehensive technical PRDs optimized for task breakdown, validates with 13 automated checks, and optionally executes tasks autonomously with datetime tracking and rollback support. Use when user requests "PRD", "product requirements", or mentions task-driven development. Default: PRD generation + handoff to TaskMaster. Optional: autonomous execution with 4 modes.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion]
---

# PRD Generator for TaskMaster v2.0

Smart PRD generation system that detects existing PRDs and offers flexible workflows. Primarily generates comprehensive, engineer-focused product requirements documents optimized for TaskMaster task breakdown. Optionally executes tasks autonomously with quality control, datetime tracking, and validation checkpoints.

## When to Use This Skill

Activate when user:
- Requests a PRD or product requirements document
- Says "I want a PRD", "create requirements", "write requirements"
- Mentions taskmaster or task-driven development
- Asks to document product/feature requirements for engineering

Do NOT activate for:
- Code documentation (API docs, technical reference)
- Test specifications or QA documentation
- Project management timelines without product context
- PDF document creation

## Core Principles

**Quality Over Speed**: Planning is 95% of the work. Take time to create comprehensive PRDs that enable successful implementation.

**Taskmaster Required**: This skill REQUIRES taskmaster (MCP or CLI). Will block and prompt for installation if not detected.

**Engineer-Focused**: Primary audience is engineering teams. Include technical depth, code examples, architecture considerations, and implementation details.

**Validation-Driven**: Automated checks ensure PRD quality before delivery. 13 validation checks run automatically.

**User Testing Checkpoints**: Every 5 tasks, insert user validation checkpoint to catch issues early.

**Complete Automation**: Provides 4 autonomous execution modes with git policies, progress logging, and datetime tracking.

## Workflow Overview (13 Steps)

1. **Enable Plan Mode & Check State** - Resume detection + interactive prompts
2. **Detect Existing PRD** - Smart detection with execute/update/replace options
3. **Detect Taskmaster** - MCP > CLI > Block if missing
4. **Discovery Questions** - 12+ detailed questions (if generating new PRD)
5. **Initialize Taskmaster** - Via MCP/CLI (if not already initialized)
6. **Generate PRD** - Load template and fill with discovery answers
7. **Validate Quality** - 13 automated checks
8. **Parse & Expand** - Combined operation with research
9. **Insert User Tests** - Checkpoint every 5 tasks
10. **Setup Tracking** - DateTime, rollback, accuracy scripts
10.5. **Generate CLAUDE.md** - TDD workflow guide from template
11. **Choose Next Action** - Handoff to TaskMaster OR autonomous execution
12. **Summary & Start** - Present overview and begin work

---

## Detailed Implementation

### Step 1: Enable Plan Mode & Check for Incomplete Work

**FIRST ACTION** when skill activates:

```
1. Check for incomplete work from previous session:
   - Run: python3 .taskmaster/scripts/execution-state.py (if exists)
   - If incomplete work found: Offer to resume

2. Enable plan mode (if not already enabled):
   - This ensures AskUserQuestion tool works properly
   - Inform user: "Enabling plan mode for interactive prompts..."

3. Proceed to Step 2
```

**Auto-Resume if Crash Detected:**

```
If execution-state.py reports incomplete work:

🔍 Detected incomplete work from previous session

📍 Last Activity:
  - Mode: {mode}
  - Task: {task_id}
  - Subtask: {subtask_id}
  - Last updated: {timestamp}
  - Completed: Tasks {completed_list}

Resume from:
  1. Last subtask (continue where crashed)
  2. Restart current task
  3. Last checkpoint
  4. Start fresh

Type: 1, 2, 3, or 4
```

---

### Step 2: Detect Existing PRD (Smart Detection)

**SECOND ACTION**: Check if PRD already exists before generating new one.

**Detection Logic:**

```
1. Check if .taskmaster/ exists:
   - Use Glob: .taskmaster/
   - NO → New project, proceed to Step 3 (detect taskmaster)
   - YES → Continue to check for PRD

2. Check for existing PRD:
   - Use Glob: .taskmaster/docs/*.md or .taskmaster/docs/prd.*
   - Read .taskmaster/tasks/tasks.json to get task count and status
   - Found PRD → Show existing PRD options (below)
   - No PRD → Proceed to Step 3 (detect taskmaster)
```

**If Existing PRD Found:**

```
🔍 Found existing PRD: {filename}

📄 PRD Details:
  - Created: {date from file}
  - Location: .taskmaster/docs/{filename}
  - Tasks: {X total} ({Y completed}, {Z pending})
  - Status: {% complete}

What would you like to do?

  1. Execute tasks from existing PRD
     → Skip to Step 11 (choose execution mode)
     → Start working on pending tasks

  2. Update/refine existing PRD
     → Edit current PRD with new requirements
     → Re-parse to update tasks
     → Merge with existing task list

  3. Create new PRD (replace current)
     → Confirm: "This will replace existing PRD. Continue?"
     → Proceed to Step 3 (full PRD generation workflow)

  4. Review existing PRD
     → Show summary of current PRD
     → Display task breakdown
     → Exit skill

Type: 1, 2, 3, or 4
```

**Option 1: Execute Existing Tasks**
```
User selects: 1

✅ Using existing PRD: {filename}
📋 Remaining tasks: {Z} pending tasks
📍 Next checkpoint: {next USER-TEST}

→ Skip to Step 11 (choose execution mode)
```

**Option 2: Update Existing PRD**
```
User selects: 2

📝 What changes would you like to make?

[User provides changes]

✅ Updating PRD...
→ Edit existing PRD file with changes
→ Re-run parse-prd with --append flag
→ Continue to Step 8 (insert user tests for new tasks only)
→ Proceed to Step 11
```

**Option 3: Replace PRD**
```
User selects: 3

⚠️  WARNING: This will replace your existing PRD and task list.

Current work:
  - {Y} tasks completed
  - {Z} tasks pending
  - All completed work will be preserved in git history
  - Task files will be regenerated

Type "yes" to confirm replacement, or "no" to cancel.

[If yes]
✅ Creating new PRD (old PRD backed up to .taskmaster/docs/prd-backup-{timestamp}.md)
→ Proceed to Step 3 (full workflow)
```

**Option 4: Review**
```
User selects: 4

📄 Current PRD Summary:
  - Title: {title}
  - Created: {date}
  - Goals: {list top 3 goals}
  - Requirements: {count functional requirements}
  - Tasks: {X total} ({Y completed}, {Z pending})

[Display executive summary and key sections]

✅ Review complete. Skill exiting.
```

**If No PRD Found (but .taskmaster/ exists):**
```
🔍 Found .taskmaster/ directory (initialized)
📄 No PRD found

Creating PRD for TaskMaster...
→ Proceed to Step 3 (detect taskmaster, already initialized)
```

---

### Step 3: Detect Taskmaster (MANDATORY - Blocks if Missing)

**CRITICAL**: Must detect taskmaster BEFORE proceeding with PRD generation.

**Detection Priority:**

```
1. Check for MCP Task-Master-AI (PREFERRED):
   - Attempt: mcp__task-master-ai__get_tasks with projectRoot
   - If successful: TASKMASTER_METHOD="MCP" ✅
   - Note: MCP provides superior integration (direct function calls)

2. Fallback to CLI:
   - Run: which taskmaster
   - Run: taskmaster --version
   - If found: TASKMASTER_METHOD="CLI" ✅

3. Neither Available:
   - TASKMASTER_METHOD="NONE" ❌
   - BLOCK and display installation instructions
```

**If Taskmaster Not Found:**

```
⚠️ Taskmaster Required

This skill REQUIRES taskmaster (MCP or CLI) to function properly.

I didn't detect taskmaster in your environment.

Option 1 (RECOMMENDED): Install MCP Task-Master-AI
  • Add to Claude Code MCP settings
  • Provides seamless integration with direct function calls
  • See: https://github.com/cyanheads/task-master-ai
  • Installation: Add to your MCP config, restart Claude Code

Option 2: Install CLI
  • Run: npm install -g task-master-ai
  • Use command-line interface
  • See: https://github.com/cyanheads/task-master-ai

Please install taskmaster and type 'done' when ready.

[WAIT for user to install and confirm]
[RE-DETECT after user confirms]
[PROCEED only if detection successful]
```

**NO PROCEEDING WITHOUT TASKMASTER DETECTED**

---

### Step 4: Discovery (Comprehensive Requirements Gathering)

Ask detailed questions to ensure comprehensive PRD:

**Essential Questions (5):**
1. What problem does this solve? (user pain point, business impact)
2. Who is the target user/audience?
3. What is the proposed solution or feature?
4. What are the key success metrics? (how we measure success)
5. What constraints exist? (technical, timeline, resources)

**Technical Context (4):**
6. Is this for an existing codebase or greenfield project?
7. What tech stack? (if known)
8. Any integration requirements? (third-party services, internal systems)
9. Performance/scale requirements? (users, data volume, latency)

**Taskmaster Specific (3):**
10. Have you used taskmaster before? (helps calibrate detail level)
11. What's the estimated complexity? (simple feature, typical project, complex system)
12. Timeline expectations? (helps with phasing and task breakdown)

**Open-Ended (1):**
13. Anything else I should know? (edge cases, constraints, context)

**Smart Defaults:**
- If user provides minimal answers, use best guesses and document assumptions
- Default to comprehensive detail
- Assume engineer audience unless specified otherwise

---

### Step 5: Initialize Taskmaster Project

**CRITICAL**: Initialize ONLY via taskmaster MCP/CLI. NEVER create .taskmaster/ manually.

#### If TASKMASTER_METHOD="MCP":

```
Use mcp__task-master-ai__initialize_project:
  - projectRoot: ${PWD} (absolute path)
  - yes: true (skip prompts)
  - storeTasksInGit: true
  - initGit: false (if git already exists)
  - skipInstall: false
  - rules: ["claude"]

Result: .taskmaster/ structure created by taskmaster
```

#### If TASKMASTER_METHOD="CLI":

```bash
taskmaster init --yes --store-tasks-in-git --rules=claude
```

**Output:**
```
✅ Taskmaster Initialized
   Created: .taskmaster/docs/
   Created: .taskmaster/tasks/
   Created: .taskmaster/reports/
   Created: .taskmaster/state/
   Updated: .gitignore
```

---

### Step 6: Generate Comprehensive PRD

**IMPORTANT**: Use the PRD template from `templates/` directory as the base structure.

**Template Selection:**
```
1. Read PRD template based on project complexity:
   - Complex/Standard projects: Use Read tool to load templates/taskmaster-prd-comprehensive.md
   - Simple features: Use Read tool to load templates/taskmaster-prd-minimal.md

2. Template provides:
   - Complete section structure with placeholders
   - Examples for each section
   - Taskmaster-specific hints and formatting
```

**Generation Process:**
```
1. Load template:
   - Use Read tool: templates/taskmaster-prd-comprehensive.md (default)
   - Or: templates/taskmaster-prd-minimal.md (if user requested minimal)

2. Fill template with user's answers from Step 4:
   - Replace [placeholders] with actual content
   - Expand examples with project-specific details
   - Add technical depth based on discovery answers

3. Write completed PRD:
   - Output to: .taskmaster/docs/prd.md
   - Preserve template structure and formatting
```

**Template contains 12 sections:**
1. Executive Summary
2. Problem Statement
3. Goals & Success Metrics
4. User Stories
5. Functional Requirements
6. Non-Functional Requirements
7. Technical Considerations
8. Implementation Roadmap
9. Out of Scope
10. Open Questions & Risks
11. Validation Checkpoints
12. Appendix: Task Breakdown Hints

**Output:**
```
✅ PRD Generated from template
   Template: taskmaster-prd-comprehensive.md
   Output: .taskmaster/docs/prd.md
   Sections: 12 (all populated)
```

---

### Step 7: Validate PRD Quality (13 Automated Checks)

**Required Elements (5 checks):**
1. ✅ Executive summary exists (2-3 sentences)
2. ✅ Problem statement includes user AND business impact
3. ✅ All goals have SMART metrics (Specific, Measurable, Achievable, Relevant, Time-bound)
4. ✅ User stories have acceptance criteria (minimum 3 per story)
5. ✅ Out of scope explicitly defined

**Functional Requirements (3 checks):**
6. ✅ All functional requirements are testable (not vague)
7. ✅ Each requirement has priority (Must/Should/Could)
8. ✅ Requirements are numbered (REQ-001, REQ-002, etc.)

**Technical Considerations (2 checks):**
9. ✅ Technical considerations address architecture
10. ✅ Non-functional requirements include specific targets (not "fast" but "< 200ms p95")

**Taskmaster-Specific (3 checks):**
11. ✅ Requirements have task breakdown hints
12. ✅ Dependencies identified for task sequencing
13. ✅ Acceptance criteria are concrete (can become task completion checks)

**Validation Output:**
```
✅ PRD Quality Validation: 13/13 PASSED
  ✅ All required elements present
  ✅ All functional requirements testable
  ✅ Taskmaster optimization complete

Quality Score: 60/60 (EXCELLENT)
Safe to proceed with task generation.

OR

⚠️ PRD Quality Validation: 11/13 (2 warnings)
  ✅ Required elements: 5/5
  ✅ Functional requirements: 3/3
  ✅ Technical considerations: 2/2
  ⚠️ Taskmaster optimization: 1/3

  Warnings:
    - REQ-007: "should be performant" is vague
      Suggestion: Replace with "< 200ms response time for 95th percentile"
    - User Story 2: Only 2 acceptance criteria (minimum 3 recommended)
      Suggestion: Add edge case criterion

Quality Score: 55/60 (GOOD - minor improvements suggested)
```

---

### Step 8: Parse PRD & Expand Tasks (Single Combined Operation)

**IMPORTANT**: Combine parse-prd + expand-all with research into ONE operation.

**Auto-Calculate Task Count:**
```
numTasks = (count of functional requirements × 1.5) rounded
Minimum: 10 tasks
Maximum: 40 tasks
```

#### If TASKMASTER_METHOD="MCP":

```
1. Parse PRD with research:
   Use mcp__task-master-ai__parse_prd:
     - projectRoot: ${PWD}
     - input: ".taskmaster/docs/prd.md"
     - numTasks: Auto-calculated based on requirements count
     - research: true (ALWAYS use research for better quality)
     - append: false

2. Immediately expand ALL tasks with research:
   Use mcp__task-master-ai__expand_all:
     - projectRoot: ${PWD}
     - research: true (ALWAYS use research)
     - force: false
```

#### If TASKMASTER_METHOD="CLI":

```bash
# Combined operation:
taskmaster parse-prd --input .taskmaster/docs/prd.md --research --num-tasks auto && \
taskmaster expand-all --research
```

**Result:**
```
✅ Tasks Generated: 22 tasks from PRD
✅ Tasks Expanded: 94 subtasks created
  - Phase 1: 5 tasks, 18 subtasks
  - Phase 2: 6 tasks, 28 subtasks
  - Phase 3: 5 tasks, 22 subtasks
  - Phase 4: 4 tasks, 18 subtasks
  - Phase 5: 2 tasks, 8 subtasks
```

---

### Step 9: Insert User Testing Tasks (Every 5 Tasks)

**CRITICAL NEW REQUIREMENT**: After tasks are expanded, insert user-facing testing tasks.

**Logic:**
```
For every 5 tasks:
  - Insert a new task: "USER-TEST-{N}"
  - Title: "User Validation Checkpoint {N}"
  - Description: "Manually test functionality from Tasks {start} to {end}"

Example:
  - TASK-001 to TASK-005 → Insert USER-TEST-1 after TASK-005
  - TASK-006 to TASK-010 → Insert USER-TEST-2 after TASK-010
```

**User Testing Task Template:**

```markdown
# USER-TEST-{N}: User Validation Checkpoint {N}

## Purpose
Manual testing of functionality implemented in Tasks {start}-{end}

## Prerequisites
All subtasks in Tasks {start}-{end} must be completed and merged to main branch.

## Testing Checklist

### Functionality Tests
[For each requirement covered in these 5 tasks, add:]
- [ ] Test Requirement REQ-{X}: [Description]
  - Expected: [What should happen]
  - Actual: [User fills in]

### Integration Tests
- [ ] Test integration between components
- [ ] Verify no regressions in existing features

### Performance Tests
- [ ] Measure response time (should be < [target])
- [ ] Test under expected load

## Acceptance Criteria
- ✅ All functionality tests pass
- ✅ No critical bugs found
- ✅ Performance meets targets

## If Tests Fail
1. Document issue in .taskmaster/docs/progress.md
2. Type "issues" and describe what failed
3. I'll create fix tasks before proceeding
4. Do NOT continue to next tasks until fixed

## When Complete
Type "passed" to continue to next tasks.
```

**Implementation:**

#### If TASKMASTER_METHOD="MCP":
```
Use mcp__task-master-ai__add_task for each checkpoint:
  - projectRoot: ${PWD}
  - title: "User Validation Checkpoint {N}"
  - description: "Manually test functionality from Tasks {start} to {end}"
  - details: [Full testing checklist template above]
  - dependencies: "{end}" (depends on last task in group)
  - priority: "high"
```

#### If TASKMASTER_METHOD="CLI":
```bash
taskmaster add-task \
  --title="User Validation Checkpoint {N}" \
  --description="Manual testing checkpoint" \
  --dependencies="{end}" \
  --priority=high
```

**Result:**
```
✨ Inserted user validation checkpoints:
   ✅ USER-TEST-1 (after Task 5)
   ✅ USER-TEST-2 (after Task 10)
   ✅ USER-TEST-3 (after Task 15)
   ✅ USER-TEST-4 (after Task 20)

📊 Updated task count: 26 tasks (22 implementation + 4 user tests)
```

---

### Step 10: Setup Tracking Scripts

Create automation scripts in `.taskmaster/scripts/`:

**Scripts to Create:**

1. **track-time.py** - Real datetime tracking with UTC timestamps
2. **rollback.sh** - Git rollback to any task checkpoint
3. **learn-accuracy.py** - Estimation accuracy learning
4. **security-audit.py** - Auto-generate security checklist
5. **execution-state.py** - Crash recovery state management

**All scripts are included in this skill's implementation and will be auto-generated.**

See sections below for complete script implementations.

---

### Step 10.5: Generate CLAUDE.md (TDD Workflow Guide)

**IMPORTANT**: Generate a TDD workflow guide for the project using the template, but only if one doesn't already exist.

**Pre-Check (REQUIRED):**
```
1. Check if CLAUDE.md already exists:
   - Use Glob tool: ./CLAUDE.md
   - If EXISTS → Skip generation, show message:
     "ℹ️ CLAUDE.md already exists. Skipping generation to preserve your configuration."
   - If NOT EXISTS → Proceed with generation

2. Check if codex.md already exists (for later):
   - Use Glob tool: ./codex.md
   - Store result for Step 4 below
```

**Template Loading (only if CLAUDE.md doesn't exist):**
```
1. Read the CLAUDE.md template:
   - Use Read tool: templates/CLAUDE.md.template

2. Template contains:
   - TDD workflow instructions (RED → GREEN → REFACTOR)
   - Taskmaster integration commands
   - Agent usage guidelines
   - Validation & quality gates
   - Project-specific placeholders
```

**Placeholder Replacement:**
```
Replace these placeholders with project-specific values from Step 4 discovery:

{{PROJECT_NAME}}        → User's project/feature name
{{TECH_STACK}}          → Tech stack from discovery (e.g., "React, Node.js, PostgreSQL")
{{ARCHITECTURE_OVERVIEW}} → Brief architecture description
{{KEY_DEPENDENCIES}}    → Main dependencies identified
{{TESTING_FRAMEWORK}}   → Testing framework (e.g., "Jest", "Vitest", "pytest")
{{DEV_ENVIRONMENT}}     → Development environment setup
{{TEST_COMMAND}}        → Test command (e.g., "npm test", "pytest")
```

**Generation Process:**
```
1. Pre-check: Skip if CLAUDE.md exists (see Pre-Check above)

2. Load template:
   - Use Read tool: templates/CLAUDE.md.template

3. Fill placeholders with discovery answers:
   - If value unknown, use sensible default or "[To be configured]"

4. Write to project root:
   - Output to: ./CLAUDE.md (project root)

5. Ask about Codex (only if codex.md doesn't exist):
   - Use AskUserQuestion: "Are you using Codex in addition to Claude Code?"
   - If yes AND codex.md doesn't exist: Also write to ./codex.md (identical content)
   - If codex.md exists: Skip, show "ℹ️ codex.md already exists."
```

**Output:**
```
[If CLAUDE.md doesn't exist]
✅ CLAUDE.md Generated
   Template: templates/CLAUDE.md.template
   Output: ./CLAUDE.md
   Contains: TDD workflow, taskmaster integration, quality gates

[If CLAUDE.md exists]
ℹ️ CLAUDE.md already exists - skipped generation

[If Codex selected AND codex.md doesn't exist]
✅ codex.md Generated (identical to CLAUDE.md)
   Output: ./codex.md

[If codex.md exists]
ℹ️ codex.md already exists - skipped generation
```

---

---

### Step 11: Choose Next Action (Handoff vs Autonomous Execution)

**CRITICAL CHOICE**: After PRD and tasks are ready, ask user how they want to proceed.

**Use AskUserQuestion tool** to present two main options:

```
Use AskUserQuestion:

questions:
  - question: "Your PRD and tasks are ready. How would you like to proceed?"
    header: "Next Action"
    multiSelect: false
    options:
      - label: "Show TaskMaster Commands"
        description: "Hand off to TaskMaster. I'll show you the commands to run tasks manually. Full control."

      - label: "Autonomous Execution"
        description: "I'll execute tasks for you autonomously with 4 execution modes to choose from."
```

**Option A: Handoff to TaskMaster (DEFAULT)**

If user selects "Show TaskMaster Commands":

```
✅ PRD Complete: .taskmaster/docs/prd.md
📋 Tasks Ready: {X} tasks ({Y} subtasks)
📍 Next checkpoint: {next USER-TEST}

🚀 TaskMaster Commands (Use these to work on tasks):

Sequential Execution:
  taskmaster next-task        # Get next available task
  taskmaster get-task {id}    # Work on specific task
  taskmaster set-task-status {id} --status=done

Parallel Execution (for independent tasks):
  taskmaster get-tasks --status=pending --with-subtasks
  # Work on multiple tasks simultaneously

Progress Tracking:
  taskmaster get-tasks --with-subtasks    # See all tasks
  python3 .taskmaster/scripts/track-time.py start {task_id}
  python3 .taskmaster/scripts/track-time.py complete {task_id}

Quality & Safety:
  bash .taskmaster/scripts/rollback.sh {task_id}    # Rollback to checkpoint
  python3 .taskmaster/scripts/security-audit.py     # Security check

📚 Documentation:
  - PRD: .taskmaster/docs/prd.md
  - Tasks: .taskmaster/tasks/
  - Progress: .taskmaster/docs/progress.md

💡 Tip: Use TaskMaster MCP tools for the best experience!

Ready to start? Run: taskmaster next-task
```

Then EXIT the skill (skill complete).

---

**Option B: Autonomous Execution**

If user selects "Autonomous Execution":

Ask follow-up question with 4 execution modes:

```
Use AskUserQuestion:

questions:
  - question: "Select autonomous execution mode:"
    header: "Execution Mode"
    multiSelect: false
    options:
      - label: "Sequential to Checkpoint"
        description: "Work autonomously until next user test. Stops for validation. RECOMMENDED for quality control."

      - label: "Parallel to Checkpoint"
        description: "Run independent tasks in parallel until next user test. Faster execution."

      - label: "Full Autonomous"
        description: "Run ALL tasks in parallel without stopping. ⚠️ Skips user validation."

      - label: "Manual Control"
        description: "You decide which tasks to run. Full control over execution."
```

**Execution Mode Details:**

**Mode 1: Sequential to Checkpoint**
- Executes tasks one-by-one until next USER-TEST
- Stops for user validation
- Best for quality control
- RECOMMENDED for first-time features

**Mode 2: Parallel to Checkpoint**
- Executes independent tasks in parallel
- Stops at next USER-TEST
- Faster execution
- Good for experienced users

**Mode 3: Full Autonomous**
- Runs ALL tasks in parallel without stopping
- Auto-completes USER-TEST tasks
- Fastest execution
- WARNING: Skips manual validation

**Mode 4: Manual Control**
- User decides which tasks to run
- Full control over execution
- No autonomous execution

**All execution modes include:**
- Strict git branching policies (branch per task, sub-branch per subtask)
- Commit checkpoints after every task
- Progress logging to .taskmaster/docs/progress.md
- Datetime tracking with track-time.py
- Autonomous execution (no user input except at checkpoints)

**After mode selected:**

1. Store their selection
2. Output the corresponding full execution prompt
3. Recognize if user types "begin" or "start"
4. Begin autonomous execution

**Claude Recommendation:**

Based on context, recommend the best option:
- First-time feature OR critical system → Mode 1 (Sequential)
- Experienced user OR non-critical → Mode 2 (Parallel)
- Trusted implementation OR time-critical → Mode 3 (Full)
- Complex requirements OR learning → Mode 4 (Manual)

Display recommendation: "⭐ Claude Recommends: Mode {N}"

See full execution prompt templates in "EXECUTION PROMPT TEMPLATES" section below.

---

### Step 12: Present Final Summary

**Summary depends on the path taken:**

---

**If Handoff to TaskMaster (Step 11 Option A):**

```
✅ PRD COMPLETE

📄 PRD Created: .taskmaster/docs/prd.md
✅ Taskmaster Initialized: Using {MCP/CLI}
📋 Tasks Generated: {X} tasks ({Y} implementation + {Z} user tests)
🔄 Tasks Expanded: {N} subtasks
📊 Scripts Created: .taskmaster/scripts/ (5 automation scripts)

📊 Overview:
  - Feature: {name}
  - Complexity: {Simple/Medium/Complex}
  - Estimated Effort: {X} tasks, ~{Y} hours
  - Key Goal: {primary success metric}

🎯 Key Requirements:
  1. {Top functional requirement}
  2. {Second functional requirement}
  3. {Third functional requirement}

⚠️ Quality Validation: {score}/60
  ✅ All 13 validation checks passed

📋 Task Breakdown:
  - Phase 1: {X} tasks
  - Phase 2: {X} tasks
  - Phase 3: {X} tasks
  - Phase 4: {X} tasks

👤 User Testing Checkpoints:
  - USER-TEST-1: After Task {N}
  - USER-TEST-2: After Task {N}
  - USER-TEST-3: After Task {N}

🚀 Next Steps:

Run: taskmaster next-task

Or use TaskMaster MCP tools to manage tasks.

See commands above for full TaskMaster usage.

✨ PRD generation complete! Ready to build.
```

Then EXIT skill.

---

**If Autonomous Execution (Step 11 Option B):**

```
✅ PRD COMPLETE - STARTING AUTONOMOUS EXECUTION

📄 PRD: .taskmaster/docs/prd.md
✅ Taskmaster: Using {MCP/CLI}
📋 Tasks: {X} tasks ({Y} implementation + {Z} user tests)
🔄 Subtasks: {N} subtasks
📊 Scripts: Ready (.taskmaster/scripts/)

📊 Overview:
  - Feature: {name}
  - Complexity: {Simple/Medium/Complex}
  - Mode: {Selected execution mode}
  - Next Checkpoint: {next USER-TEST}

⚠️ Quality: {score}/60 ✅

🚀 Execution Starting!

Selected: {execution mode name}

[If Sequential/Parallel:]
Next: Tasks {start}-{end} → USER-TEST-{N}
Working autonomously until checkpoint...

[If Full Autonomous:]
All {X} tasks will execute in parallel
Working autonomously until complete...

[If Manual:]
Awaiting your commands...

Type "begin" or "start" to execute!
```

Then PROCEED to autonomous execution using the selected mode's prompt template (see EXECUTION PROMPT TEMPLATES section).

---

## TOP 5 ENHANCEMENTS

### Enhancement 1: Real DateTime Tracking (B2)

**Script: `.taskmaster/scripts/track-time.py`**

Created automatically during Step 8.

**Features:**
- UTC timestamp tracking (start/end)
- Precise duration calculation
- JSON state persistence
- CLI interface for easy use

**Usage in Execution:**
```bash
# Before task starts:
python3 .taskmaster/scripts/track-time.py start {task_id}

# Before subtask starts:
python3 .taskmaster/scripts/track-time.py start {task_id} {subtask_id}

# After subtask completes:
python3 .taskmaster/scripts/track-time.py complete {task_id} {subtask_id}

# After task completes:
python3 .taskmaster/scripts/track-time.py complete {task_id}
```

**Output:**
```
📅 Started: 2025-01-29 14:23:15 UTC
[... work happens ...]
✅ COMPLETED
📅 Ended: 2025-01-29 14:41:32 UTC
⏱️  Actual: 18 min (18.3 min)
📊 vs Estimate: 18 min - Within 2% ✅
```

See TOP_5_ADDITIONS.md for complete script code.

---

### Enhancement 2: Instant Rollback Command (A1)

**Script: `.taskmaster/scripts/rollback.sh`**

**Trigger:** User types "rollback to task X" at ANY time during execution

**Features:**
- Revert to any checkpoint tag
- Backup current state before rollback
- Update progress.md with rollback note
- Safety confirmation before destructive action

**Usage:**
```
USER: rollback to task 3

CLAUDE:
🔄 Initiating rollback to Task 3...

⚠️  This will:
  - Discard all changes after Task 3
  - Reset to checkpoint-task-003
  - Preserve current work in rollback-backup-{timestamp}

Type "yes" to confirm.

USER: yes

CLAUDE:
💾 Backed up to: rollback-backup-20250129-143045
✅ Rolled back to Task 3
📝 Updated progress.md

What next?
  1. Resume from here
  2. Redo Task 3
  3. Skip to different task
  4. Manual control

Type: 1, 2, 3, or 4
```

See TOP_5_ADDITIONS.md for complete script code.

---

### Enhancement 3: Accuracy Learning System (B3)

**Script: `.taskmaster/scripts/learn-accuracy.py`**

**Trigger:** After every 10 completed tasks (at USER-TEST checkpoints)

**Features:**
- Tracks estimated vs actual time
- Calculates average accuracy percentage
- Generates adjustment factor
- Recommends estimate adjustments

**Usage:**
```
After USER-TEST-2 passes:

📊 Running estimation accuracy analysis...

Tasks Analyzed: 10
Average Accuracy: 123%
Adjustment Factor: 1.23x

Recent Tasks:
  Task 6:  45min (est: 30min) - 150% ⚠️
  Task 7:  22min (est: 25min) - 88% ✅
  Task 8:  38min (est: 35min) - 109% ✅
  Task 9:  67min (est: 45min) - 149% ⚠️
  Task 10: 28min (est: 20min) - 140% ⚠️

⚠️  You're taking 23% longer than estimated.

Apply adjustment to remaining tasks?
  1. Yes, increase all future estimates by 23%
  2. No, keep current estimates
  3. Manually review

Type: 1, 2, or 3
```

See TOP_5_ADDITIONS.md for complete script code.

---

### Enhancement 4: Security Audit Checklist (D2)

**Script: `.taskmaster/scripts/security-audit.py`**

**Trigger:** Before final USER-TEST checkpoint

**Features:**
- Scans codebase for security-relevant patterns
- Auto-generates checklist based on detected features
- Includes standard security checks
- Offers automated security scans

**Usage:**
```
Before USER-TEST-4 (final checkpoint):

🔒 Generating security audit checklist...

### Authentication
- [ ] Passwords hashed with bcrypt (cost ≥ 10)
- [ ] Session tokens cryptographically secure

### OAuth
- [ ] OAuth tokens encrypted at rest
- [ ] OAuth state parameter prevents CSRF

### Database
- [ ] All queries use parameterized statements
- [ ] No SQL injection vulnerabilities

### General Security
- [ ] HTTPS enforced in production
- [ ] CSRF protection enabled
- [ ] Rate limiting on auth endpoints
- [ ] Security headers set (CSP, X-Frame-Options)

Run automated scans?
  1. Yes, run npm audit + recommended scans
  2. Manual review only
  3. Skip for now

Type: 1, 2, or 3
```

See TOP_5_ADDITIONS.md for complete script code.

---

### Enhancement 5: Auto-Resume After Crash (A2)

**Script: `.taskmaster/scripts/execution-state.py`**

**Trigger:** At Step 0 (before anything else) if previous session crashed

**Features:**
- Persistent execution state tracking
- Detects incomplete work
- Offers resume points
- Continues where crashed

**Usage:**
```
[Claude crashes mid-task]
[User restarts 10 minutes later]

USER: continue

CLAUDE:
🔍 Checking for incomplete work...

Found it!

📍 Last Activity:
  - Mode: Sequential to Checkpoint
  - Task: TASK-007 (OAuth callback handler)
  - Subtask: 3/5 (Handle error responses)
  - Last updated: 2025-01-29 16:45:23 UTC (10 min ago)
  - Completed: Tasks 1-6 ✅

Resume from:
  1. Last subtask (continue TASK-007 subtask 3)
  2. Restart current task (redo TASK-007)
  3. Last checkpoint (restart from TASK-006)
  4. Start fresh

Type: 1, 2, 3, or 4
```

See TOP_5_ADDITIONS.md for complete script code.

---

## EXECUTION PROMPT TEMPLATES

### Template 1: Sequential to Checkpoint

```
Execute tasks sequentially from {current_task} until USER-TEST-{N}.

DATETIME TRACKING:
Before each task:
  python3 .taskmaster/scripts/track-time.py start {task_id}
Before each subtask:
  python3 .taskmaster/scripts/track-time.py start {task_id} {subtask_id}
After each subtask:
  python3 .taskmaster/scripts/track-time.py complete {task_id} {subtask_id}
After each task:
  python3 .taskmaster/scripts/track-time.py complete {task_id}

STRICT GIT POLICY:
1. When starting a task:
   - Create feature branch: git checkout -b task-{id}-{slug}

2. For each subtask:
   - Create sub-branch: git checkout -b task-{id}-subtask-{n}
   - Complete subtask implementation
   - Run tests
   - Commit: git commit -m "Complete task-{id} subtask-{n}: [description]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
   - Merge to task branch: git checkout task-{id}-{slug} && git merge task-{id}-subtask-{n}
   - Delete sub-branch: git branch -d task-{id}-subtask-{n}

3. When task complete:
   - Verify ALL subtasks merged
   - Merge to main: git checkout main && git merge task-{id}-{slug}
   - Create checkpoint tag: git tag -a checkpoint-task-{id} -m "Completed task {id}"
   - Delete feature branch: git branch -d task-{id}-{slug}

PROGRESS LOGGING:
After EVERY task completion, append to .taskmaster/docs/progress.md:

## Task {id}: {title} - COMPLETED
**Completed**: {timestamp}
**Duration**: {actual_minutes} min (estimated: {estimated_minutes} min)
**Subtasks**: {n} completed
**Tests**: {pass/fail}
**Issues**: {any issues encountered}
**Git**: Merged to main, tagged as checkpoint-task-{id}

AUTONOMOUS EXECUTION RULES:
- Do NOT ask user for input unless critical error
- If task fails tests: retry once, then log and skip
- If dependency missing: log and skip
- Continue until USER-TEST-{N} reached
- Update execution state after each task

ROLLBACK SUPPORT:
If user types "rollback to task X" at ANY TIME:
  1. STOP current work immediately
  2. Run: bash .taskmaster/scripts/rollback.sh X
  3. Wait for user confirmation
  4. Resume as user directs

WHEN COMPLETE:
Stop and report:
"✅ Tasks {start}-{end} completed
📋 Next: USER-TEST-{N} - User validation required
📝 Progress: .taskmaster/docs/progress.md
🌳 Git: All tasks merged with checkpoints"
```

---

### Template 2: Parallel to Checkpoint

Similar to Template 1 but with:
- Launch up to 3 concurrent tasks
- Handle merge conflicts automatically
- Wait for dependencies before starting dependent tasks
- All tasks still follow git policy (branch per task)

---

### Template 3: Full Autonomous

Similar to Template 2 but:
- No stops for USER-TEST (auto-completes them)
- Maximum parallelization (up to 5 concurrent)
- Runs automated tests for USER-TEST tasks
- Only stops when ALL tasks complete

---

### Template 4: Manual Control

```
Awaiting user commands:
- "next task" - Get next task
- "task {id}" - Work on specific task
- "status" - Show progress
- "parallel {id1,id2}" - Run specific tasks in parallel

Git policies enforced.
Progress logged to progress.md.
Datetime tracking active.
```

---

## Reference

For complete script implementations, see:
- TOP_5_ADDITIONS.md (all 5 automation scripts)
- USER_EXPERIENCE_EXAMPLE.md (user flow walkthrough)
- CHANGES_SUMMARY.md (what changed from v1)

## Tips for Best Results

**Understand the Workflow:**
- This skill PRIMARILY generates PRDs (with optional execution)
- If you already have a PRD, the skill will detect it and offer options
- Default behavior: Generate PRD → Hand off to TaskMaster
- Optional: Choose autonomous execution after PRD is ready

**Provide Context Upfront:**
- More detail in discovery → Better PRD
- Share constraints, dependencies, assumptions
- Mention existing systems to integrate with

**Be Specific About Success:**
- Quantify goals (not "improve UX" but "increase NPS from 45 to 60")
- Define what "done" looks like
- Specify how you'll measure success

**Choose the Right Path:**
- **Handoff to TaskMaster** (Default): Best if you want full control
- **Autonomous Execution**: Best if you trust the process and want speed
  - Sequential to Checkpoint: Quality-focused, stops for validation
  - Parallel to Checkpoint: Faster, stops at checkpoints
  - Full Autonomous: Maximum speed, skips validation
  - Manual Control: You decide every step

**If Using Existing PRD:**
- Option 1: Execute tasks (pick up where you left off)
- Option 2: Update PRD (add new requirements)
- Option 3: Replace PRD (start fresh, old PRD backed up)
- Option 4: Review PRD (just read it)

**Leverage Automation (if using autonomous execution):**
- Use datetime tracking to improve estimates
- Use rollback if you need to undo work
- Let accuracy learning adjust your estimates
- Review security audit before deployment

**Trust the Process:**
- USER-TEST checkpoints catch issues early
- Git checkpoints allow easy rollback
- Progress.md shows exactly what happened
- TaskMaster integration ensures smooth workflow

---

**Remember**: A comprehensive PRD with automated quality control and TaskMaster integration is the foundation of successful implementation. This skill focuses on creating that foundation. Execution is optional - you can always hand off to TaskMaster for more control.

