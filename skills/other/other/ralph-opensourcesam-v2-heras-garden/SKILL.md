---
name: ralph
description: Ralph autonomous coding loop with MiniMax subagent delegation. Managed loop (not recursive) with progress tracking, completion detection, and circuit breakers.
---

# Ralph - Autonomous Coding with MiniMax Subagent Delegation

## Core Loop Algorithm

```
WHILE NOT complete AND iterations < max_iterations:
    1. Decompose remaining task into independent chunks
    2. For each chunk:
       a. Spawn MiniMax subagent via Task tool
       b. Collect result
       c. Validate (tests pass, lint passes)
    3. Detect completion via MiniMax semantic analysis
    4. Update progress file
    5. Check circuit breakers (max iterations, failures)
    6. If HITL mode and iteration % hitl_interval == 0:
       Request human review
    7. iterations++
END WHILE
```

## Input Parsing

Parse `$ARGUMENTS` to extract:
- **task_description**: The main task (required)
- **--mode**: `hitl` or `autonomous` (default: `hitl`)
- **--max**: Maximum iterations (default: 10)
- **--hitl-interval**: Review every N iterations (default: 3)

## P0 Implementation (MVP)

### Step 1: Initialize Progress File

```javascript
Create temp/ralph-[timestamp].json:
{
  "session_id": "ralph-20260124-HHMMSS",
  "started_at": ISO timestamp,
  "task_description": "...",
  "mode": "hitl|autonomous",
  "max_iterations": N,
  "current_iteration": 0,
  "tasks": [],
  "circuit_breakers": {
    "calls_this_hour": 0,
    "consecutive_failures": 0
  }
}
```

### Step 2: Main Execution Loop

**For each iteration:**

1. **Task Decomposition** (apply subagent-best-practices):
   - Break remaining work into independent chunks
   - Define clear deliverables for each chunk
   - Ensure parallel independence

2. **Spawn MiniMax Subagents** (use Task tool in parallel):
   ```
   Task(prompt="Subtask 1: {specific chunk}...")
   Task(prompt="Subtask 2: {specific chunk}...")
   Task(prompt="Subtask 3: {specific chunk}...")
   ```

3. **Aggregate Results**:
   - Collect all subagent outputs
   - WITHOUT re-running their searches
   - Synthesize into next actions

4. **Validation** (basic for P0):
   - Did subagents complete their tasks?
   - Were outputs in expected format?
   - Any failures to retry?

5. **Progress Update**:
   - Update progress file with completed tasks
   - Increment iteration counter
   - Log files modified

6. **Completion Check** (basic for P0):
   - All chunks completed?
   - Task description satisfied?
   - Max iterations reached?

7. **Circuit Breaker Check** (basic for P0):
   - Reached max_iterations? → Stop
   - 5 consecutive failures? → Stop

### Step 3: HITL Checkpoint (if hitl mode)

```
IF current_iteration % hitl_interval == 0:
    Present summary:
    - What's been done
    - What's remaining
    - Any concerns
    Wait for user: CONTINUE / MODIFY / CANCEL
```

## MiniMax Integration (P0)

**For spawning subagents:**

Use `Task` tool with explicit prompts:
```
Task(
  subagent_type="general-purpose",
  prompt="You are Subagent tasked with: {specific task}
          Search scope: {directories}
          Output format: {table/list}
          Return ONLY the specified output."
)
```

**For completion detection (P0 - basic):**

Use MiniMax MCP if available, otherwise use heuristic:
```
IF has MiniMax MCP:
    Use mcp__MiniMax-Wrapper__coding_plan_general
    Prompt: "Is this task complete? {task_description}
              Work done: {summary}
              Remaining: {remaining}"
ELSE:
    Heuristic: All chunks completed + no explicit failures
```

## Circuit Breakers (P0 - Basic)

**Layer 1: Iteration Limit**
```python
if iteration >= max_iterations:
    stop("Max iterations reached")
```

**Layer 2: Failure Counting**
```python
if consecutive_failures >= 5:
    stop("Too many consecutive failures")
```

**Layer 3: Completion Criteria Gate (CRITICAL)**
```python
# NEVER stop early without meeting ALL criteria
if user_specified_time:
    if elapsed_time < user_specified_time:
        continue_working("Time commitment not yet fulfilled")

if visual_quality_required:
    if not screenshots_captured:
        continue_working("Visual proof required")
    if not quality_surpasses_reference:
        continue_working("Quality gate not met")

if narrative_consistency_required:
    if not checked_against_storyline_md:
        continue_working("Narrative verification required")

if success_criteria_defined:
    if not all_criteria_verified:
        continue_working("Completion criteria not satisfied")
```

**Completion Criteria Enforcement:**
- Document explicit criteria in progress file at START
- Verify each criterion with evidence before marking complete
- Visual work requires visual proof (screenshots)
- Narrative work requires Storyline.md cross-reference
- Time commitments MUST be honored (no early stopping)
- "Good enough" is not a completion criterion

**Anti-Pattern Prevention:**
Track and prevent these early-exit justifications:
- ❌ "I've made good progress" → Continue until criteria met
- ❌ "No blockers found" → Continue until work complete
- ❌ "Let me summarize" → Continue working, summarize at true end
- ❌ "This seems done" → Verify against criteria list first

## Quick Reference

**When to decompose:** Task has multiple independent chunks
**When to spawn:** For each independent chunk
**When to aggregate:** After all subagents return
**When to stop:** Complete OR max_iterations OR 5 failures

**Remember:** Main agent = orchestrator, NOT worker. Delegate, don't re-run.

---

[Codex - 2026-01-24]
