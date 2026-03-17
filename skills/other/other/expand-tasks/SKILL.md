---
name: expand-tasks
description: >-
  Expand all TaskMaster tasks with deep research via Perplexity before coding begins.
  Reads tasks.json, launches parallel research agents per task, writes findings back.
  Part of the prd-taskmaster toolkit. Use after PRD is parsed into tasks and before
  implementation begins. Invoke with /expand-tasks or when user says "expand tasks",
  "research all tasks", or "research before coding for all tasks".
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - Glob
  - Grep
  - AskUserQuestion
---

# Expand Tasks with Research v1.0

Expands TaskMaster tasks with Perplexity research before coding begins.
Deterministic operations handled by `script.py`; AI handles judgment.

**Script location**: `~/.claude/skills/expand-tasks/script.py`
**Part of**: prd-taskmaster toolkit
**Depends on**: research-before-coding skill (pattern), Perplexity MCP proxy

## When to Use

Activate when user says: expand tasks, research tasks, research before coding for all, expand subtasks.
Do NOT activate for: single task research (use /research-before-coding), PRD generation (use /prd-taskmaster).

## Prerequisites

- TaskMaster tasks.json must exist (run /prd-taskmaster first)
- Perplexity proxy must be running at localhost:8765
- At least 1 task in tasks.json

---

## Workflow (5 Steps)

### Step 1: Preflight

```bash
python3 ~/.claude/skills/expand-tasks/script.py read-tasks
```

Returns JSON: `total`, `expanded`, `pending_expansion`, `tasks[]`.

**If `pending_expansion` is 0**: Report all tasks already expanded. Exit skill.

**If Perplexity is down**: Check health first:
```bash
curl -sf http://localhost:8765/health
```
If down, tell user to start it and exit.

---

### Step 2: Choose Scope

Use AskUserQuestion:
- **All tasks** (default): Expand every task that hasn't been researched yet
- **Specific tasks**: User provides task IDs (comma-separated)
- **By dependency level**: Expand tasks with no dependencies first, then next wave

**AI judgment**: Recommend "All tasks" for initial expansion, "By dependency level" for incremental work.

---

### Step 3: Generate Research Prompts

For each task to expand:

```bash
python3 ~/.claude/skills/expand-tasks/script.py gen-prompt --task-id <ID>
```

Returns JSON with `prompt` field containing the full research agent prompt.

**AI judgment**: Review the auto-generated prompt. Customize research questions if the task needs domain-specific queries. Add project context from the PRD or session-context files if relevant.

---

### Step 4: Launch Parallel Research Agents

Launch research agents in parallel waves. Each wave = up to 5 concurrent agents.

**For each task**, spawn a Task agent:

```
Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Research Task <ID>: <title>",
  run_in_background: true,
  prompt: <prompt from Step 3>
)
```

**Wave strategy**:
- Wave 1: Tasks with no dependencies (they inform downstream tasks)
- Wave 2: Tasks depending on Wave 1
- Wave 3+: Continue until all tasks covered
- Max 5 agents per wave to avoid overwhelming Perplexity proxy

**Wait for each wave to complete before launching the next.**

---

### Step 5: Collect and Write Results

As each agent completes, save its research output:

1. Write agent output to a temp file:
   ```bash
   echo "<agent output>" > /tmp/research-task-<ID>.md
   ```

2. Write research back to tasks.json:
   ```bash
   python3 ~/.claude/skills/expand-tasks/script.py write-research --task-id <ID> --research /tmp/research-task-<ID>.md
   ```

3. After all tasks are written, verify:
   ```bash
   python3 ~/.claude/skills/expand-tasks/script.py status
   ```

**AI judgment**: Review each research result for quality. If a result is too thin (< 5 lines of useful content) or clearly failed, re-run that specific task's research.

---

## Research Agent Prompt Pattern

The `gen-prompt` command generates prompts that follow the research-before-coding pattern:

1. Agent receives task context (title, description, dependencies, subtasks)
2. Agent runs `perplexity_batch` or `mcp__perplexity-api-free__search` with 3-5 targeted queries
3. Agent distills results into structured summary
4. Summary returns to main context (~25-40 lines per task)

**Critical**: Research agents must NEVER use WebSearch or WebFetch. Perplexity MCP only.

---

## Error Handling

| Error | Action |
|-------|--------|
| Perplexity proxy down | Exit skill, tell user to start proxy |
| Agent returns empty/failed | Re-run that specific task with different queries |
| tasks.json not found | Exit skill, tell user to run /prd-taskmaster first |
| Task already expanded | Skip silently unless user forces re-expansion |
| Agent timeout | Mark task as failed, continue with others |

---

## Output

After all tasks are expanded, the skill reports:
- Total tasks expanded
- Any failures that need retry
- Next recommended action (usually: begin implementation)

---

## Integration with prd-taskmaster

This skill fits between Step 8 (Parse & Expand Tasks) and Step 11 (Choose Next Action) of the prd-taskmaster workflow. After PRD is parsed into tasks but before execution begins.

```
/prd-taskmaster → generates PRD → parses into tasks
    ↓
/expand-tasks → researches each task → writes findings back
    ↓
Implementation begins (with research context in each task)
```

---

## Tips

- Run after PRD generation but before any implementation
- Research results are stored in `research_notes` field of each task in tasks.json
- Re-running on already-expanded tasks is safe (will skip unless forced)
- For very large task lists (20+), consider expanding in dependency order to save context
- Each research agent costs ~30s of Perplexity time; 15 tasks ≈ 3 waves ≈ 2-3 minutes total
