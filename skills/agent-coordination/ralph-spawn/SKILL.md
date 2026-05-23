---
name: ralph-spawn
description: Spawn parallel agents in git worktrees for automated feature implementation. Creates isolated development environments for ready tasks from Linear.
triggers:
  - /ralph.spawn
  - spawn agents
  - start automated implementation
---

# /ralph.spawn [epic]

Create worktrees for all ready tasks in an epic and start parallel agent execution.

## Prerequisites

**CRITICAL**: Run `/ralph.preflight` before spawning agents. If Linear MCP is not
authenticated, spawn will BLOCK with recovery instructions.

## Process

0. **Pre-Flight Check (REQUIRED)**

   Run `/ralph.preflight` to verify:
   - Linear MCP is authenticated (REQUIRED)
   - Git repository is valid (REQUIRED)
   - Cognee is available (OPTIONAL - will buffer locally if not)

   If pre-flight BLOCKS, fix the issue and resume with `/ralph.resume`.

1. **Query Linear for ready tasks**
   ```
   mcp__plugin_linear_linear__list_issues({
     "team": "floe",
     "project": "floe-{epic_number}-{slug}",
     "state": "backlog"
   })
   ```

2. **Build dependency graph** from blockedBy relations

3. **Detect file overlaps** to determine parallelization
   - Tasks modifying different files → parallel
   - Tasks modifying same files → sequential (waves)

4. **Create worktrees** for non-overlapping tasks
   ```bash
   git worktree add "../floe-agent-{epic}-{task_slug}" -b "feature/{epic}-{task}" main
   ```

5. **Enable direnv in each worktree** (CRITICAL for environment setup)
   ```bash
   cd "../floe-agent-{epic}-{task_slug}" && direnv allow
   ```

   **Why**: Without `direnv allow`, the worktree won't load .envrc and environment
   variables (like PYRIGHT_PYTHON_FORCE_VERSION) won't be set. This causes:
   - Type checking warnings/failures
   - Missing environment variables
   - Inconsistent development environment

6. **Initialize agent state** in each worktree
   - Copy `.ralph/templates/plan.json` → `.agent/plan.json`
   - Copy `.ralph/templates/activity.md` → `.agent/activity.md`
   - Copy `.ralph/templates/PROMPT.md` → `.agent/PROMPT.md`
   - Copy `.specify/memory/constitution.md` → `.agent/constitution.md`

7. **Claim tasks in Linear**
   ```
   mcp__plugin_linear_linear__update_issue({
     "id": task_id,
     "state": "started",
     "assignee": "me"
   })
   ```

8. **Update manifest.json** with active agents

## Output

```
RALPH WIGGUM SPAWN - EP001

Created Worktrees: 4
Wave 1: [T001 (auth), T003 (catalog), T005 (tests)]
Wave 2: [T002 (models)] - depends on T001

Worktree Details:
- ../floe-agent-ep001-auth    T001  FLO-33  feature/ep001-auth
- ../floe-agent-ep001-catalog T003  FLO-35  feature/ep001-catalog
- ../floe-agent-ep001-tests   T005  FLO-37  feature/ep001-tests

Next: Run /ralph.status to monitor progress
```

## Configuration

See `.ralph/config.yaml`:
- `max_parallel_agents`: Maximum concurrent worktrees
- `worktree_pattern`: Naming convention for worktrees

## Agent Loop (Per Worktree)

Each agent runs the Ralph Wiggum pattern:

1. **Read state** - `.agent/plan.json`, `.agent/activity.md`
2. **Identify next subtask** - First with `passes: false`
3. **Implement** - Make atomic, focused changes
4. **Run quality gates** - lint, type, test, security, constitution
5. **Update state** - Mark subtask complete, commit, log
6. **Repeat** until all subtasks pass or BLOCKED

## Error Handling

- If worktree exists: Remove and recreate
- If branch exists: Delete and recreate
- If Linear unavailable: Signal error, don't start
- If no ready tasks: Report "No ready tasks for epic"

## Related Commands

- `/ralph.status` - Monitor agent progress
- `/ralph.integrate` - Prepare for PR after completion
- `/ralph.cleanup` - Remove worktrees after merge
