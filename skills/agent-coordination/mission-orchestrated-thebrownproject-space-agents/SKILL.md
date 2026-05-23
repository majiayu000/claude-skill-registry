---
name: mission-orchestrated
description: "HOUSTON spawns Task agents: Worker, Inspector, Analyst per task. Best for medium features (4-10 tasks)."
---

# /mission-orchestrated - Agents-Per-Task Execution

HOUSTON coordinates execution by spawning fresh agents for each task. Prevents context rot.

## The Process

1. **Load feature** - Run `bd show FEATURE_ID` to get details
2. **Activate feature** - Run `bd update FEATURE_ID --status in_progress`
3. **Task loop** - For each task:
   - Get next task: `bd list --parent FEATURE_ID --status open` (pick highest priority)
   - Spawn Scout agent (explores codebase for context)
   - Spawn Worker agent (include scout report)
   - Wait for Worker completion
   - Spawn Inspector agent (verifies requirements met)
   - Spawn Analyst agent (reviews code quality)
   - HOUSTON decides: continue, fix issues, or escalate
   - Mark task complete: `bd close TASK_ID`
4. **Complete feature** - Run `bd close FEATURE_ID`

## Spawning Agents

Use Task tool with `run_in_background: false` (wait for completion).

**CRITICAL:** Always pass task_id and feature_id explicitly. Agents will run `bd show` to fetch authoritative details from Beads.

**Scout** (`subagent_type: "Explore"`):
```
"Scout the codebase for task: [title]
 Task: [description]
 Feature: [feature summary]

 Report ONLY facts - no suggestions or ideas:
 directories, files, patterns, dependencies."
```

**Worker** (`subagent_type: "space-agents:mission-worker"`):
```
"Execute task [TASK_ID] for feature [FEATURE_ID].

 Run `bd show [TASK_ID]` and `bd show [FEATURE_ID]` first to get full context.

 Scout report:
 [output from Scout agent]"
```

**Inspector** (`subagent_type: "space-agents:mission-inspector"`):
```
"Review task [TASK_ID] for feature [FEATURE_ID].

 Run `bd show [TASK_ID]` and `bd show [FEATURE_ID]` first to get requirements.

 Verify: requirements met, tests pass, acceptance criteria satisfied."
```

**Analyst** (`subagent_type: "space-agents:mission-analyst"`):
```
"Analyze task [TASK_ID] for feature [FEATURE_ID].

 Run `bd show [TASK_ID]` and `bd show [FEATURE_ID]` first to understand scope.

 Check: patterns followed, no regressions, maintainable."
```

## Decision Points

After Inspector/Analyst return, HOUSTON decides:

| Result | Action |
|--------|--------|
| All pass | Mark complete, continue to next task |
| Minor issues | Log warning, continue |
| Blocker found | Create bug via `bd create -t bug`, ask user |
| Critical issue | Halt, escalate to user |

## On Completion

```
HOUSTON: Feature complete. {N} tasks executed via orchestrated mode.
         Worker/Inspector/Analyst cycle completed for each task.
```
