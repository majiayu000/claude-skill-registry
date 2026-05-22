---
name: solve-issue
version: "1.0.0"
description: "Complete issue lifecycle with Python-driven continuous execution (no AI pauses)"
last-updated: "2026-03-18"
---

# Solve Issue - Python-Driven Continuous Automation

**EXPERIMENTAL** - True continuous automation using Python coordinator + AI executor architecture.

## Overview

Solves the "random pause" problem in /work-issue by using a Python script as the decision-making coordinator, driving continuous execution without AI returning to user between phases.

**Architecture:**
```
┌─────────────────┐
│  solve-issue    │  (AI Skill - YOU)
│  (Executor)     │
└────────┬────────┘
         │ 1. Launches coordinator
         ▼
┌─────────────────┐
│  coordinator.py │  (Python Script, background)
│  (Decision)     │
└────────┬────────┘
         │ 2. Writes instructions
         ▼
┌─────────────────┐
│ instructions    │  (JSON file)
│ .json           │
└────────┬────────┘
         │ 3. AI reads instructions
         ▼
┌─────────────────┐
│  solve-issue    │  (AI Executor - YOU)
│  Execution Loop │
└────────┬────────┘
         │ 4. Calls skills
         ▼
┌─────────────────┐
│ start-issue     │
│ eval-plan       │  (Other Skills)
│ execute-plan    │
│ review          │
│ finish-issue    │
└─────────────────┘
```

**What it does:**
1. Launches Python coordinator in background
2. Coordinator writes skill execution instructions to JSON file
3. AI reads instructions continuously and calls corresponding skills
4. Coordinator waits for AI completion, decides next phase
5. Repeats until all 5 phases complete

**Difference from /work-issue:**
- work-issue: AI orchestration (stops after each Skill call)
- solve-issue: Python orchestration (continuous loop, no stops)

**When to use:**
- You want true automation without manual intervention
- Issue is well-defined with good plan/code quality
- You trust the validation scores (eval-plan, review)

**When NOT to use:**
- Want manual control at checkpoints → use /work-issue --interactive
- Experimental nature concerns you → use /work-issue (stable)
- First time with a complex issue → use /work-issue to learn workflow

## Arguments

```bash
/solve-issue [issue-number] [options]
/solve-issue [issue1,issue2,issue3] [options]  # Batch mode
```

**Common usage:**
```bash
# Single issue
/solve-issue #253                      # Auto mode (default)
/solve-issue #253 --interactive        # Stop at checkpoints
/solve-issue #253 --resume             # Resume from saved state

# Batch mode (multiple issues)
/solve-issue [128,184,33]              # Process 3 issues sequentially
/solve-issue [45,67] --continue-on-error  # Continue even if one fails
```

**Options:**
- `[issue-number]` - Single issue to work on
- `[issue1,issue2,issue3]` - Batch mode: multiple issues (comma-separated)
- `--auto` - Auto mode (default) - score-based checkpoints
- `--interactive` - Stop at both checkpoints for manual review
- `--resume` - Resume from saved state (single issue only)
- `--stop-on-error` - Stop batch on first error (default for batch mode)
- `--continue-on-error` - Continue batch even if errors occur

## AI Execution Instructions

**CRITICAL: Execution loop pattern**

When executing `/solve-issue`, AI MUST follow this continuous loop:

### Step 1: Launch Coordinator (Background)

```python
import subprocess
import sys

# Launch Python coordinator in background
coordinator_script = ".claude/skills/solve-issue/scripts/coordinator.py"
mode = "auto"  # or "interactive" from arguments

# Start coordinator process (non-blocking)
process = subprocess.Popen(
    [sys.executable, coordinator_script, str(issue_number), mode],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print(f"✅ Coordinator launched (PID: {process.pid})")
```

### Step 2: Enter Execution Loop

```python
import json
import time
from pathlib import Path

instructions_file = Path(".claude/skills/solve-issue/.temp/instructions.json")
completions_file = Path(".claude/skills/solve-issue/.temp/completions.json")

while True:
    # Read instruction from coordinator
    if not instructions_file.exists():
        time.sleep(1)
        continue

    with open(instructions_file) as f:
        data = json.load(f)
        instruction = data["instruction"]

    instr_type = instruction["type"]

    # Handle different instruction types
    if instr_type == "call_skill":
        # Call the specified skill
        skill_name = instruction["skill_name"]
        skill_args = instruction["skill_args"]

        print(f"📞 Calling /{skill_name} {skill_args}")
        Skill(skill_name, args=skill_args)

        # Mark completion
        write_completion(instruction["phase"], "success")

    elif instr_type == "checkpoint":
        # Stop for user review
        checkpoint_data = instruction["checkpoint_data"]
        score = checkpoint_data.get("score", 0)

        print(f"⏸️  Checkpoint: {instruction['message']}")
        print(f"   Score: {score}/100")
        print(f"   Review results and decide:")
        print(f"   - [C]ontinue anyway")
        print(f"   - [E]dit plan/code")
        print(f"   - [S]top workflow")

        # Wait for user decision (return to user)
        return

    elif instr_type == "complete":
        # All phases done
        print(instruction["message"])
        cleanup_temp_files()
        return

    elif instr_type == "error":
        # Error occurred
        print(f"❌ Error: {instruction['message']}")
        cleanup_temp_files()
        return

    # Clear instruction (prevent re-reading)
    instructions_file.unlink()
```

### Step 3: Write Completion Helper

```python
def write_completion(phase: str, status: str = "success"):
    """Write completion marker for coordinator"""
    completion = {
        "phase": phase,
        "status": status,
        "timestamp": time.time()
    }

    completions_file = Path(".claude/skills/solve-issue/.temp/completions.json")
    with open(completions_file, "w") as f:
        json.dump(completion, f, indent=2)
```

### Step 4: Cleanup Helper

```python
def cleanup_temp_files():
    """Clean up temporary instruction files"""
    instructions_file = Path(".claude/skills/solve-issue/.temp/instructions.json")
    completions_file = Path(".claude/skills/solve-issue/.temp/completions.json")

    instructions_file.unlink(missing_ok=True)
    completions_file.unlink(missing_ok=True)
```

## Workflow Steps

Copy this checklist to track progress:

```
Task Progress:
- [ ] Step 1: Launch Python coordinator
- [ ] Step 2: Enter execution loop
- [ ] Step 3: Execute Phase 1 (start-issue)
- [ ] Step 4: Execute Phase 1.5 (eval-plan)
- [ ] Step 5: Checkpoint 1 (if score ≤ 90)
- [ ] Step 6: Execute Phase 2 (execute-plan)
- [ ] Step 7: Execute Phase 2.5 (review)
- [ ] Step 8: Checkpoint 2 (if score ≤ 90)
- [ ] Step 9: Execute Phase 3 (finish-issue)
- [ ] Step 10: Cleanup and report
```

Execute these steps in the continuous loop without returning to user (unless checkpoint).

## Integration

**Compared to /work-issue:**

| Feature | work-issue | solve-issue |
|---------|-----------|-------------|
| **Orchestrator** | AI | Python |
| **Execution** | Stops after each Skill | Continuous loop |
| **Pauses** | 5+ (after each phase) | 0-2 (checkpoints only) |
| **Maturity** | Stable | Experimental |
| **Use Case** | General | Maximum automation |

**When to use each:**
- work-issue: Default choice, stable, well-tested
- solve-issue: Need maximum speed, trust automation

## Error Handling

**Coordinator fails to start:**
```
❌ Failed to launch coordinator

Error: {error message}

Fallback: Use /work-issue #253 instead
```

**Instruction file read error:**
```
⚠️ Instruction file corrupted

Options:
1. Restart: /solve-issue #253 --resume
2. Fallback: /work-issue #253
3. Manual cleanup: rm .claude/skills/solve-issue/.temp/*
```

**Checkpoint triggered:**
```
⏸️  Checkpoint: Score 75/100 ≤ 90

Review and decide:
[C]ontinue - Proceed despite low score
[E]dit - Fix issues first
[S]top - Pause workflow

Your choice: _
```

## Examples

### Example 1: Successful Auto Execution

**User says:**
> "/solve-issue #253"

**Workflow:**
1. Launch coordinator.py in background
2. Coordinator writes instruction: call_skill(start-issue, 253)
3. AI reads instruction, calls /start-issue #253
4. AI writes completion marker
5. Coordinator writes instruction: call_skill(eval-plan, 253 --mode=auto)
6. AI calls /eval-plan #253 --mode=auto → Score: 95/100
7. Coordinator checks score > 90 → Continue automatically
8. ... continues through all phases ...
9. Final: All complete, cleanup

**Time:** 35-65 minutes (no pauses)
**Pauses:** 0 (score > 90 in both checkpoints)

### Example 2: Checkpoint Triggered

**User says:**
> "/solve-issue #254"

**Workflow:**
1-6. Same as Example 1
7. /eval-plan #254 → Score: 75/100
8. Coordinator checks score ≤ 90 → Write checkpoint instruction
9. AI reads checkpoint → Display to user and STOP

**User reviews, fixes plan, resumes:**
> "/solve-issue #254 --resume"

10. Coordinator resumes from Phase 2
11. ... continues ...

**Time:** 40-70 minutes + fix time
**Pauses:** 1 (checkpoint at eval-plan)

## Batch Mode (NEW in v1.0.0)

**Process multiple issues sequentially in one command:**

```bash
/solve-issue [128,184,33]
```

**How it works:**
1. Parse issue list: [128, 184, 33]
2. For each issue:
   - Run full 5-phase workflow
   - Auto mode applied (no manual checkpoints)
   - Continue to next issue on success
   - Stop or continue on error (based on flag)
3. Final summary: success/failed counts

**Error handling strategies:**

**Stop on error (default):**
```bash
/solve-issue [128,184,33] --stop-on-error

Issue #128: ✅ Success
Issue #184: ❌ Failed (eval-plan score 65)
Issue #33:  ⏸️  Skipped (stopped due to previous failure)

Result: 1/3 completed
```

**Continue on error:**
```bash
/solve-issue [128,184,33] --continue-on-error

Issue #128: ✅ Success
Issue #184: ❌ Failed (eval-plan score 65)
Issue #33:  ✅ Success

Result: 2/3 completed (1 failed)
```

**When to use batch mode:**
- Daily issue cleanup (multiple small bugs)
- Sprint completion (batch of related features)
- Automation workflows (CI/CD triggered)

**Limitations:**
- Sequential only (no parallel processing)
- Auto mode enforced (no interactive checkpoints)
- All issues must be in same repository

## Performance

| Metric | work-issue | solve-issue | Improvement |
|--------|-----------|-------------|-------------|
| **Pauses** | 5+ | 0-2 | 60-100% reduction |
| **Total time** | 45-75 min | 35-65 min | 20-30% faster |
| **User intervention** | Multiple prompts | Checkpoints only | Cleaner UX |

**Why faster:**
- No AI → user → AI round trips between phases
- Continuous execution in single session
- Python handles decision logic (faster than AI re-evaluation)

## Best Practices

1. **Use for well-defined issues** - Complex/vague issues may fail checkpoints
2. **Trust the scores** - Auto mode relies on eval-plan/review scores
3. **Have fallback** - If issues occur, use /work-issue as backup
4. **Monitor first run** - Watch the continuous execution to build confidence
5. **Provide feedback** - Report bugs/issues to improve the skill

## Task Management

When executing, create high-level tasks:

```python
tasks = [
    TaskCreate("Launch coordinator", ...),
    TaskCreate("Execute Phase 1: start-issue", ...),
    TaskCreate("Execute Phase 1.5: eval-plan", ...),
    TaskCreate("Execute Phase 2: execute-plan", ...),
    TaskCreate("Execute Phase 2.5: review", ...),
    TaskCreate("Execute Phase 3: finish-issue", ...),
    TaskCreate("Cleanup and report", ...)
]
```

Update as each phase completes.

## Final Verification

```
- [ ] All 5 phases completed
- [ ] No errors in coordinator log
- [ ] Temp files cleaned up
- [ ] Issue closed on GitHub
- [ ] PR merged to main
```

## Workflow Skills Requirements

This is a **meta-workflow skill** (orchestrates other workflow skills):

1. **TaskCreate** at start - Track phase progress
2. **Continuous execution** - No stops except checkpoints
3. **Verification checklist** - Final validation before completion

**See**: [WORKFLOW_PATTERNS.md](../WORKFLOW_PATTERNS.md)

## Related Skills

- **/work-issue** - Stable alternative (AI orchestration)
- **/start-issue** - Phase 1 (called by this skill)
- **/eval-plan** - Phase 1.5 (called by this skill)
- **/execute-plan** - Phase 2 (called by this skill)
- **/review** - Phase 2.5 (called by this skill)
- **/finish-issue** - Phase 3 (called by this skill)

---

**Version:** 1.0.0 (MVP)
**Pattern:** Meta-Workflow Orchestrator (Python-driven)
**Status:** Experimental
**Compliance:** ADR-001 ✅
**Last Updated:** 2026-03-18
