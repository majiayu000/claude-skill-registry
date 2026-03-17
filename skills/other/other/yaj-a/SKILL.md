---
name: yajña
aliases: [yajna, autonomous, loop, agentic-loop, coordinate, ritual]
description: Autonomous development ritual with role-based coordination. Loops until complete using specialized agents (hotṛ→research, adhvaryu→implement, udgātṛ→test).
execution: direct
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(*), Task, mcp__chitta-mcp__*
---

# Yajña (यज्ञ) - Autonomous Development Ritual

**Truly autonomous** development loop. Runs continuously until done. NO manual coordination.

## Critical Rules

1. **NEVER ask user for routine decisions** - just do it
2. **NEVER pause between iterations** - loop automatically
3. **STOP ONLY for**: Blockers | Completion | User interrupt
4. **Blockers require user**: Daemon down, permissions, unresolvable errors

## Pre-Flight Check (REQUIRED)

Before EVERY iteration, verify daemon is alive:

```javascript
health = mcp__chitta-mcp__health_check();
if (health.error || health.status !== "OK") {
  // BLOCKER - stop and report
  output("[BLOCKER] Daemon unreachable. Run: pkill -9 chittad && chittad daemon");
  long_task_event({ event_type: "blocker", description: "Daemon down" });
  STOP;  // Do not continue
}
```

## The Loop (Execute Without Pausing)

```
WHILE tasks_remain AND no_blocker:

  1. PRE-FLIGHT
     health_check → if fail → STOP with blocker

  2. LOAD CONTEXT (silent, no output)
     long_task_snapshot
     read fix_plan.md
     count remaining tasks

  3. HOTṚ - Research (if needed)
     Task(Explore) for complex tasks
     VALIDATE: Did agent find correct files?
     If wrong files → retry with explicit paths

  4. ADHVARYU - Implement
     Task(general-purpose) with EXPLICIT file paths
     Prompt MUST include: "Edit file X at path Y"
     VALIDATE: Check file was actually modified
     If not modified → retry or mark blocker

  5. UDGĀTṚ - Test
     Task(general-purpose) for validation
     Syntax checks, tests, verification
     If FAIL → log, continue (not a blocker)

  6. CHECKPOINT (silent)
     long_task_update
     Update fix_plan.md

  7. EVALUATE
     All done? → COMPLETION
     Same error 3x? → STAGNATION (blocker)
     Else → continue loop (NO pause, NO output)
```

## Agent Prompts Must Be Explicit

**BAD** (vague, leads to wrong files):
```
"Add pattern detection to the hooks"
```

**GOOD** (explicit paths, clear instructions):
```
"Edit /home/user/.claude/hooks/prompt-hook.sh
Add these lines after line 25:
[exact code]
Verify the file exists first with: ls -la /home/user/.claude/hooks/"
```

## Validation After Each Agent

```javascript
// After Adhvaryu returns
result = Task({ ... });

// Validate the work
if (result.includes("Error") || result.includes("not found")) {
  // Retry with more explicit instructions
  retry_count++;
  if (retry_count >= 3) {
    // BLOCKER
    long_task_event({ event_type: "blocker", description: result });
    STOP;
  }
  continue;  // Retry this iteration
}

// Check file was actually modified
file_check = Bash(`ls -la ${target_file}`);
if (file_check.error) {
  // File doesn't exist - agent edited wrong path
  retry_count++;
  continue;
}
```

## Output Rules

**During loop**: Minimal output. Just status lines:
```
━━━ ITERATION 3 ━━━
[HOTṚ] ✓ Found 2 patterns
[ADHVARYU] ✓ Modified 3 files
[UDGĀTṚ] ✓ Tests passing
[4/7 tasks done]
```

**On blocker**: Full details + stop:
```
━━━ BLOCKER ━━━
[ERROR] Daemon not responding
[ACTION] Run: pkill -9 chittad && chittad daemon
[STATUS] Yajna paused at iteration 3
```

**On completion**: Summary only:
```
━━━ PŪRṆĀHUTI ━━━
Complete in 5 iterations.
Files: 8 | Tests: passing | Learnings: 3
```

## Blocker Conditions

These STOP the loop and require user:

| Condition | Action |
|-----------|--------|
| Daemon health_check fails | Stop, show restart command |
| File not found after 3 retries | Stop, ask user for correct path |
| Same error 3 consecutive times | Stop, show stagnation |
| Build/compile fails critically | Stop, show error |
| Permission denied | Stop, ask user |

## NOT Blockers (Continue Automatically)

| Condition | Action |
|-----------|--------|
| Test fails | Log, continue to next task |
| Agent returns partial result | Use what's there, retry rest |
| Minor validation warning | Log, continue |
| Task takes long | Wait, don't timeout |

## Spawn Agents Correctly

**Parallel** (independent tasks, ONE tool call):
```javascript
// Send ALL parallel agents in SINGLE message
Task({ description: "Task 1", prompt: "..." });
Task({ description: "Task 2", prompt: "..." });
Task({ description: "Task 3", prompt: "..." });
// Wait for all, then continue
```

**Sequential** (dependent):
```javascript
result1 = Task({ description: "Task 1", prompt: "..." });
// Validate result1
result2 = Task({ description: "Task 2", prompt: `Using ${result1}...` });
// Validate result2
```

## Quick Reference

```bash
/yajna              # Start/continue (runs until done)
/yajna init GOAL    # New ritual with explicit goal
/yajna status       # Check progress without running
/yajna pause        # Stop after current iteration
```

## Example: Correct Autonomous Flow

```
User: /yajna init "Add dark mode"

[PRE-FLIGHT] Daemon OK
[INIT] yajna-myapp-1234
[PLAN] 4 tasks generated

━━━ ITERATION 1 ━━━
[HOTṚ] ✓ Found ThemeProvider, CSS variables
[ADHVARYU] ✓ src/theme/dark.css, src/context/Theme.tsx
[UDGĀTṚ] ✓ Builds, renders
[2/4 done]

━━━ ITERATION 2 ━━━
[ADHVARYU] ✓ Toggle component, localStorage
[UDGĀTṚ] ✓ Tests passing
[4/4 done]

━━━ PŪRṆĀHUTI ━━━
Complete in 2 iterations.
Files: 4 | Tests: 6 passing

[NO USER INTERACTION NEEDED - FULLY AUTONOMOUS]
```

## Anti-Patterns (NEVER DO)

❌ "Let me check with you before proceeding..."
❌ "Should I continue to the next task?"
❌ "I'll wait for your confirmation..."
❌ Outputting between every agent call
❌ Asking which file to edit
❌ Pausing after each iteration

## MCP Tools

| Tool | Purpose |
|------|---------|
| `health_check` | Pre-flight daemon check |
| `long_task_start` | Initialize ritual |
| `long_task_active` | Check for existing |
| `long_task_snapshot` | Load context |
| `long_task_update` | Record progress |
| `long_task_event` | Log blockers/checkpoints |
| `long_task_complete` | Mark done |
