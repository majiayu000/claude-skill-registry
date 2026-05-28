---
name: prd-taskmaster
description: >-
  Smart PRD generator with TaskMaster integration. Detects existing PRDs and offers execute/update/replace options.
  Generates comprehensive technical PRDs optimized for task breakdown, validates with 13 automated checks,
  and optionally executes tasks autonomously with datetime tracking and rollback support. Use when user requests
  "PRD", "product requirements", or mentions task-driven development. Defaults to PRD generation with
  handoff to TaskMaster. Optionally supports autonomous execution with 4 modes.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# PRD Generator for TaskMaster v3.0

Smart PRD generation with deterministic operations handled by `script.py`.
AI handles judgment (questions, content, decisions); script handles mechanics.

**Script location**: `~/.claude/skills/prd-taskmaster/script.py`
**All script commands output JSON.**

## When to Use

Activate when user says: PRD, product requirements, taskmaster, task-driven development.
Do NOT activate for: API docs, test specs, project timelines, PDF creation.

## Core Principles

- **Quality Over Speed**: Planning is 95% of the work
- **Taskmaster Required**: Blocks if not detected
- **Engineer-Focused**: Technical depth, code examples, architecture
- **Validation-Driven**: 13 automated checks via script
- **User Testing Checkpoints**: Every 5 tasks

---

## Workflow (12 Steps)

### Step 1: Preflight & Resume Detection

```bash
python3 ~/.claude/skills/prd-taskmaster/script.py preflight
```

Returns JSON: `has_taskmaster`, `prd_path`, `task_count`, `tasks_completed`, `tasks_pending`, `taskmaster_method`, `has_claude_md`, `has_crash_state`, `crash_state`.

**If `has_crash_state` is true**: Present resume options to user:
1. Continue from last subtask
2. Restart current task
3. Resume from last checkpoint
4. Start fresh

**Then proceed to Step 2.**

---

### Step 2: Detect Existing PRD

Use preflight JSON: if `prd_path` is not null and `task_count > 0`, an existing PRD is found.

**If existing PRD found**, use AskUserQuestion:
- **Execute tasks** from existing PRD (skip to Step 11)
- **Update/refine** existing PRD (edit and re-parse)
- **Create new PRD** (replace - backup first via `script.py backup-prd --input <path>`)
- **Review** existing PRD (display summary, then exit)

**If no PRD found**: Proceed to Step 3.

---

### Step 3: Detect Taskmaster

Use preflight JSON field `taskmaster_method`: `mcp`, `cli`, or `none`.

**If `none`**: Block and show installation instructions:
- Option 1 (recommended): Install MCP Task-Master-AI
- Option 2: `npm install -g task-master-ai`
- Wait for user to install and confirm, then re-run: `script.py detect-taskmaster`

**No proceeding without taskmaster detected.**

---

### Step 4: Discovery Questions

Ask detailed questions to build comprehensive PRD. Use AskUserQuestion for structured input.

**Essential (5):**
1. What problem does this solve? (user pain point, business impact)
2. Who is the target user/audience?
3. What is the proposed solution or feature?
4. What are the key success metrics?
5. What constraints exist? (technical, timeline, resources)

**Technical (4):**
6. Existing codebase or greenfield?
7. Tech stack?
8. Integration requirements?
9. Performance/scale requirements?

**TaskMaster-specific (3):**
10. Used taskmaster before?
11. Estimated complexity? (simple/typical/complex)
12. Timeline expectations?

**Open-ended (1):**
13. Anything else? (edge cases, constraints, context)

**Smart defaults**: If user provides minimal answers, use best guesses and document assumptions.

---

### Step 5: Initialize Taskmaster

Only if `.taskmaster/` doesn't exist (check preflight `has_taskmaster`).

```bash
python3 ~/.claude/skills/prd-taskmaster/script.py init-taskmaster --method <cli|mcp>
```

For MCP: use the returned params to call `mcp__task-master-ai__initialize_project`.
For CLI: script runs `taskmaster init` directly.

---

### Step 6: Generate PRD

Load template:
```bash
python3 ~/.claude/skills/prd-taskmaster/script.py load-template --type <comprehensive|minimal>
```

Returns JSON with `content` field containing the template.

**AI judgment**: Fill template with user's answers from Step 4:
- Replace placeholders with actual content
- Expand examples with project-specific details
- Add technical depth based on discovery answers

Write completed PRD to `.taskmaster/docs/prd.md`.

---

### Step 7: Validate PRD Quality

```bash
python3 ~/.claude/skills/prd-taskmaster/script.py validate-prd --input .taskmaster/docs/prd.md
```

Returns JSON: `score`, `max_score`, `grade`, `checks` (13 items), `warnings`.

**Grading**: EXCELLENT (91%+), GOOD (83-90%), ACCEPTABLE (75-82%), NEEDS_WORK (<75%).

**AI judgment**: If warnings exist, offer user three options:
1. Proceed with current PRD
2. Auto-fix warnings
3. Review and fix manually

If grade is NEEDS_WORK, strongly recommend fixing before proceeding.

---

### Step 8: Parse & Expand Tasks

Calculate task count:
```bash
python3 ~/.claude/skills/prd-taskmaster/script.py calc-tasks --requirements <count>
```

Returns `recommended` task count.

**For MCP**:
```
mcp__task-master-ai__parse_prd: input=".taskmaster/docs/prd.md", numTasks=<recommended>, research=true
mcp__task-master-ai__expand_all: research=true
```

**For CLI**:
```bash
taskmaster parse-prd --input .taskmaster/docs/prd.md --research --num-tasks <recommended>
taskmaster expand-all --research
```

---

### Step 9: Insert User Test Tasks

```bash
python3 ~/.claude/skills/prd-taskmaster/script.py gen-test-tasks --total <task_count>
```

Returns array of USER-TEST task definitions with `title`, `description`, `dependencies`, `template`.

**For each task in the array**:
- MCP: `mcp__task-master-ai__add_task` with title, description, details=template, dependencies, priority=high
- CLI: `taskmaster add-task --title="..." --description="..." --dependencies="..." --priority=high`

---

### Step 10: Setup Tracking Scripts

```bash
python3 ~/.claude/skills/prd-taskmaster/script.py gen-scripts --output-dir .taskmaster/scripts
```

Creates 5 scripts: track-time.py, rollback.sh, learn-accuracy.py, security-audit.py, execution-state.py.

---

### Step 10.5: Generate CLAUDE.md

**Pre-check**: Use Glob to check if `./CLAUDE.md` exists. If it exists, skip.

If generating:
1. Load template: `script.py load-template` won't work here -- use Read tool on `~/.claude/skills/prd-taskmaster/templates/CLAUDE.md.template`
2. **AI judgment**: Replace placeholders with project-specific values from discovery:
   - `{{PROJECT_NAME}}`, `{{TECH_STACK}}`, `{{ARCHITECTURE_OVERVIEW}}`
   - `{{KEY_DEPENDENCIES}}`, `{{TESTING_FRAMEWORK}}`, `{{DEV_ENVIRONMENT}}`, `{{TEST_COMMAND}}`
3. Write to `./CLAUDE.md`
4. Ask if user uses Codex -- if yes and no `codex.md`, write identical copy

---

### Step 11: Choose Next Action

Use AskUserQuestion:

**Question**: "PRD and tasks ready. How to proceed?"
- **Show TaskMaster Commands** (default): Display command reference, then exit skill
- **Autonomous Execution**: Ask follow-up for execution mode

**If Autonomous Execution selected**, ask execution mode:
- **Sequential to Checkpoint** (recommended): Tasks one-by-one until next USER-TEST
- **Parallel to Checkpoint**: Independent tasks in parallel until USER-TEST
- **Full Autonomous**: All tasks parallel, skip user validation
- **Manual Control**: User decides each task

**AI judgment**: Recommend mode based on context:
- First-time/critical: Sequential
- Experienced/non-critical: Parallel
- Trusted/time-critical: Full Autonomous
- Complex/learning: Manual

---

### Step 12: Summary & Start

**If Handoff**: Display PRD location, task counts, key requirements, validation score, task phases, user test checkpoints, and TaskMaster commands. Then exit skill.

**If Autonomous**: Display same summary plus execution mode, then begin execution using the selected mode's rules.

---

## Execution Mode Rules

### All Modes Include

- **DateTime tracking**: `python3 .taskmaster/scripts/track-time.py start|complete <task_id> [subtask_id]`
- **Progress logging**: `python3 ~/.claude/skills/prd-taskmaster/script.py log-progress --task-id <id> --title "..." --duration "..." --subtasks "..." --tests "..." --issues "..."`
- **Git policy**: Branch per task (`task-{id}-{slug}`), sub-branch per subtask, merge to main with checkpoint tag
- **Rollback**: If user says "rollback to task X", run `bash .taskmaster/scripts/rollback.sh X`
- **State tracking**: `python3 .taskmaster/scripts/execution-state.py start|complete|checkpoint <task_id>`

### Sequential to Checkpoint

Execute tasks one-by-one. For each task:
1. Start time tracking
2. Create feature branch
3. For each subtask: create sub-branch, implement, test, commit, merge to task branch
4. Complete time tracking
5. Log progress
6. Merge to main, create checkpoint tag
7. Stop at next USER-TEST for user validation

### Parallel to Checkpoint

Same as sequential but launch up to 3 concurrent independent tasks.
Handle merge conflicts automatically. Stop at USER-TEST.

### Full Autonomous

Maximum parallelization (up to 5 concurrent). Auto-complete USER-TEST tasks.
Only stop when ALL tasks complete.

### Manual Control

Wait for user commands: "next task", "task {id}", "status", "parallel {id1,id2}".

---

## Tips

- More detail in discovery = better PRD
- Quantify goals: not "improve UX" but "increase NPS from 45 to 60"
- USER-TEST checkpoints catch issues early
- Git checkpoints allow easy rollback
- Use `script.py validate-prd` at any time to re-check PRD quality
