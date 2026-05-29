---
name: iterate
description: Self-referential iteration mode for completing complex tasks autonomously. Use when a task requires multiple attempts, trial-and-error, or persistent effort until success. Based on the Ralph Wiggum methodology. Trigger words: iterate, keep trying, until it works, autonomous, persist, retry.
context: fork
---

# Autonomous Iteration Mode

Enable self-referential iteration to complete complex tasks that require multiple attempts, trial-and-error exploration, or persistent effort until success.

## The Ralph Wiggum Methodology

This skill implements key insights from the Ralph Wiggum methodology:

1. **Stop Hook Iteration**: Don't exit until success criteria are met
2. **Completion Promises**: Explicit signals when task is complete
3. **Failures as Data**: Each failure informs the next attempt
4. **Deterministic Retry**: Systematic approach to retrying

## Process

### 1. Define Success Criteria

Before iterating, establish clear success criteria:

```markdown
## Iteration Goal
[What are we trying to achieve?]

## Success Criteria
- [ ] Criterion 1 (e.g., "tests pass")
- [ ] Criterion 2 (e.g., "no type errors")
- [ ] Criterion 3 (e.g., "feature works as expected")

## Max Attempts
[Number, typically 5-10]
```

Write this to: `~/.claude-mind/state/iteration-goal.md`

### 2. Create Iteration State

Track progress in: `~/.claude-mind/state/iteration-state.json`

```json
{
  "goal": "Description of goal",
  "criteria": ["criterion 1", "criterion 2"],
  "maxAttempts": 5,
  "currentAttempt": 0,
  "status": "in_progress",
  "attempts": [],
  "startedAt": "ISO8601",
  "updatedAt": "ISO8601"
}
```

### 3. Iteration Loop

For each attempt:

1. **Increment attempt counter**
2. **Execute the task**
3. **Evaluate against criteria**
4. **Record outcome**:
   - What was tried
   - What happened
   - What was learned
   - What to try next (if not successful)

5. **Decide next action**:
   - If ALL criteria met → Mark SUCCESS, exit
   - If max attempts reached → Mark FAILED, summarize learnings, exit
   - Otherwise → Continue to next attempt with adjusted approach

### 4. Attempt Record Format

Add to the `attempts` array:

```json
{
  "number": 1,
  "action": "What was done",
  "outcome": "What happened",
  "criteria_met": ["criterion 1"],
  "criteria_failed": ["criterion 2"],
  "learning": "What this taught us",
  "next_approach": "What to try differently"
}
```

### 5. Completion Signals

When complete, update state:

```json
{
  "status": "success" | "failed" | "abandoned",
  "completedAt": "ISO8601",
  "summary": "Final outcome description",
  "total_attempts": 3,
  "key_learnings": ["learning 1", "learning 2"]
}
```

## Commands

### Start Iteration
```bash
# Initialize new iteration
~/.claude-mind/bin/iterate-start "goal description" --max-attempts 5 --criteria "tests pass" --criteria "builds clean"
```

### Check Status
```bash
# View current iteration state
~/.claude-mind/bin/iterate-status
```

### Record Attempt
```bash
# Record an attempt outcome
~/.claude-mind/bin/iterate-record --success | --failure --action "what was done" --learning "what was learned"
```

### Complete Iteration
```bash
# Mark iteration complete
~/.claude-mind/bin/iterate-complete --success | --failed "summary"
```

## Guidelines

- **Be systematic**: Don't repeat the exact same approach
- **Learn from failures**: Each failure should inform the next attempt
- **Stay focused**: Don't drift from the original goal
- **Know when to stop**: Max attempts prevents infinite loops
- **Document everything**: Future iterations benefit from past learnings

## Integration with Stop Hook

The iteration system works with Claude Code's Stop hook. When iteration is active:

1. Stop hook checks `~/.claude-mind/state/iteration-state.json`
2. If status is `in_progress` and criteria not met:
   - Hook provides feedback: "Iteration in progress, X criteria remaining"
   - Suggests next action based on last attempt
3. This creates a self-referential loop until success or max attempts

## Example Usage

```
User: I need you to fix the build errors, keep trying until it compiles

Claude: I'll enter iteration mode for this task.

[Creates iteration state with goal "fix build errors" and criterion "build succeeds"]

Attempt 1: Fixed missing import
- Outcome: 3 errors remain
- Learning: Type errors in DataProcessor.swift

Attempt 2: Fixed type mismatches
- Outcome: 1 error remains
- Learning: Optional unwrapping issue

Attempt 3: Added nil check
- Outcome: Build succeeds!
- All criteria met

[Marks iteration SUCCESS]

The build now compiles cleanly after 3 attempts.
```

## Anti-Patterns

- Don't iterate without clear success criteria
- Don't continue iterating if fundamentally stuck (ask for help instead)
- Don't use for tasks that need human decision-making
- Don't exceed max attempts without human approval
