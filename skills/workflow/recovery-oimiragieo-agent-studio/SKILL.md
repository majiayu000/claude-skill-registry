---
name: recovery
description: Workflow recovery protocol for resuming workflows after context loss, session interruption, or errors. Handles state reconstruction, artifact recovery, and seamless workflow continuation.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
error_handling: graceful
streaming: supported
---

# Recovery Skill

<identity>
Recovery Skill - Workflow recovery protocol for resuming workflows after context loss, session interruption, or errors. Handles state reconstruction, artifact recovery, and seamless workflow continuation.
</identity>

<capabilities>
- Resuming workflows after context window exhaustion
- Recovering from session interruptions
- Reconstructing workflow state from artifacts and gate files
- Identifying and continuing from last completed step
- Preventing duplicate work during recovery
</capabilities>

<instructions>
<execution_process>

## When to Use

- Context window exhausted mid-workflow
- Session interrupted or lost
- Need to resume from last completed step
- Workflow state needs reconstruction

## Step 1: Identify Last Completed Step

1. **Check gate files** for last successful validation:
   - Location: `.claude/context/history/gates/{workflow_id}/`
   - Find highest step number with validation_status: "pass"
   - This is the last successfully completed step

2. **Review reasoning files** for progress:
   - Location: `.claude/context/history/reasoning/{workflow_id}/`
   - Read reasoning files up to last completed step
   - Extract context and decisions made

3. **Identify artifacts created**:
   - Check artifact registry: `.claude/context/artifacts/registry-{workflow_id}.json`
   - List all artifacts created up to last step
   - Verify artifact files exist

## Step 2: Load Plan Documents

1. **Read plan document** (stateless):
   - Load `plan-{workflow_id}.json` from artifact registry
   - Extract current workflow state
   - Identify completed vs pending tasks

2. **Load relevant phase plan** (if multi-phase):
   - Check if project is multi-phase (exceeds phase_size_max_lines threshold)
   - Load active phase plan: `plan-{workflow_id}-phase-{n}.json`
   - Understand phase boundaries and dependencies

3. **Understand current state**:
   - Map completed tasks to plan
   - Identify next steps
   - Check for dependencies

## Step 3: Context Recovery

1. **Load artifacts from last completed step**:
   - Read artifact registry
   - Load all artifacts with validation_status: "pass"
   - Verify artifact integrity

2. **Read reasoning files for context**:
   - Load reasoning files from completed steps
   - Extract key decisions and context
   - Understand workflow progression

3. **Reconstruct workflow state**:
   - Combine plan, artifacts, and reasoning
   - Create recovery state document
   - Validate state consistency

## Step 4: Resume Execution

1. **Continue from next step**:
   - Identify next step after last completed
   - Load step requirements from plan
   - Prepare inputs for next step

2. **Planner updates plan status** (stateless):
   - Update plan-{workflow_id}.json with current status
   - Mark completed steps
   - Update progress tracking

3. **Orchestrator coordinates next agents**:
   - Pass recovered artifacts to next step
   - Resume workflow execution
   - Monitor for additional interruptions

</execution_process>

## Failure Classification

When a task fails, classify the failure type:

| Failure Type        | Indicators                                         | Recovery Action                 |
| ------------------- | -------------------------------------------------- | ------------------------------- |
| BROKEN_BUILD        | Build errors, syntax errors, module not found      | ROLLBACK + fix                  |
| VERIFICATION_FAILED | Test failures, validation errors, assertion errors | RETRY with fix (max 3 attempts) |
| CIRCULAR_FIX        | Same error 3+ times, similar approaches repeated   | SKIP or ESCALATE                |
| CONTEXT_EXHAUSTED   | Token limit reached, maximum length exceeded       | Compress context, continue      |
| UNKNOWN             | No pattern match                                   | RETRY once, then ESCALATE       |

## Circular Fix Detection

**Iron Law**: If the same approach has been tried 3+ times without success, STOP.

When circular fix is detected:

1. **Stop** the current approach immediately
2. **Document** what was tried (approaches, errors, files)
3. **Try fundamentally different approach** (different library, different pattern, simpler implementation)
4. **If still failing, ESCALATE** to human intervention

**Detection Algorithm**:

- Extract keywords from current approach (excluding stop words)
- Compare with keywords from last 3 attempts
- If Jaccard similarity > 30% for 2+ attempts, flag as circular

**Example**:

```
Attempt 1: "Using async await for fetch"
Attempt 2: "Using async/await with try-catch"
Attempt 3: "Trying async await pattern again"
=> CIRCULAR FIX DETECTED - Stop and try callback pattern instead
```

## Attempt Count Thresholds

| Failure Type        | Max Attempts | Then Action                      |
| ------------------- | ------------ | -------------------------------- |
| VERIFICATION_FAILED | 3            | SKIP + ESCALATE                  |
| UNKNOWN             | 2            | ESCALATE                         |
| BROKEN_BUILD        | 1            | ROLLBACK (if good commit exists) |
| CIRCULAR_FIX        | 0            | Immediately SKIP                 |

## References

See `references/` for detailed patterns:

- `failure-types.md` - Failure classification details and indicators
- `recovery-actions.md` - Recovery action decision tree and execution
- `merge-strategies.md` - File merge strategies for multi-agent scenarios

<best_practices>

## Recovery Validation Checklist

- [ ] Last completed step identified correctly
- [ ] Plan document loaded and validated
- [ ] All artifacts from completed steps available
- [ ] Reasoning files reviewed for context
- [ ] Workflow state reconstructed accurately
- [ ] No duplicate work will be performed
- [ ] Next step inputs prepared
- [ ] Recovery logged in reasoning file

</best_practices>

<error_handling>

## Error Handling

- **Missing plan document**: Request planner to recreate plan from requirements
- **Missing artifacts**: Request artifact recreation from source agent
- **Corrupted artifacts**: Request artifact recreation with validation
- **Incomplete reasoning**: Use artifact registry and gate files to reconstruct state

</error_handling>
</instructions>

<examples>
<usage_example>
**Recovery after context loss**:

```bash
# 1. Check gate files for last completed step
ls .claude/context/history/gates/{workflow_id}/

# 2. Load plan document
cat .claude/context/artifacts/plan-{workflow_id}.json

# 3. Review reasoning files
cat .claude/context/history/reasoning/{workflow_id}/*.json

# 4. Resume from next step
```

</usage_example>

<usage_example>
**Natural language invocation**:

```
"Resume the workflow from where we left off"
"Recover the workflow state and continue"
"What was the last completed step?"
```

</usage_example>
</examples>

## Related

- Planner Agent: `.claude/agents/core/planner.md`
- Memory files: `.claude/context/memory/`

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
