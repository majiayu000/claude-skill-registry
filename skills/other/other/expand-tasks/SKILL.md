---
name: expand-tasks
description: >-
  Expand all TaskMaster tasks with deep research before coding begins.
  Reads tasks.json, launches parallel research agents per task using whatever
  research provider you have configured (Gemini by default, any task-master
  provider via --set-research, or any MCP research tool registered in
  ~/.claude.json). Writes findings back to tasks.json. Part of the prd-taskmaster
  toolkit. Use after PRD is parsed and before implementation. Invoke with
  /expand-tasks or "expand tasks", "research all tasks".
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

Expands TaskMaster tasks with research before coding begins.
Deterministic operations handled by `script.py`; AI handles judgment.

**Script location**: `~/.claude/skills/expand-tasks/script.py`
**Part of**: prd-taskmaster toolkit
**Depends on**: research-before-coding skill (pattern), any research provider configured via `task-master models --set-research` or registered as an MCP research tool

## When to Use

Activate when user says: expand tasks, research tasks, research before coding for all, expand subtasks.
Do NOT activate for: single task research (use /research-before-coding), PRD generation (use /prd-taskmaster).

## Prerequisites

- TaskMaster tasks.json must exist (run /prd-taskmaster first)
- A research provider is configured — either (a) `task-master models --set-research <model> --<provider>` for any task-master provider family, or (b) an MCP research tool registered in `~/.claude.json` that Claude Code can call directly
- At least 1 task in tasks.json

---

## Workflow (5 Steps)

### Step 1: Preflight

```bash
python3 ~/.claude/skills/expand-tasks/script.py read-tasks
```

Returns JSON: `total`, `expanded`, `pending_expansion`, `tasks[]`.

**If `pending_expansion` is 0**: Report all tasks already expanded. Exit skill.

**If research provider is not configured**: Check via `task-master models` and verify a research role is set. If none, tell the user to configure one (`task-master models --set-research <model> --<provider>`) and exit. The skill does not assume any specific research backend — it uses whatever is configured.

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
- Max 5 agents per wave to avoid overwhelming the configured research backend

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
2. Agent runs 3-5 targeted queries against the user's configured research provider. The agent is tool-agnostic: it picks up whichever research tools are available in the current Claude Code session. This may be `task-master research`, an MCP search/reason tool from `~/.claude.json`, WebSearch as a last resort, or whatever the user has bound. The skill does not hard-code any specific research MCP.
3. Agent distills results into structured summary
4. Summary returns to main context (~25-40 lines per task)

**Critical**: prefer structured research tools (task-master research, MCP search/reason tools) over raw WebSearch/WebFetch when available — they produce cleaner outputs with citations.

---

## Error Handling

| Error | Action |
|-------|--------|
| Research provider unreachable or rate-limited | Exit skill, tell user to verify `task-master models` research role is set and reachable |
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
- Each research agent typically completes in ~30s depending on research backend and query depth; 15 tasks ≈ 3 waves ≈ 2-3 minutes total
