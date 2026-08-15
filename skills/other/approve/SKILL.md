---
name: approve
description: "Request write permission from the user before making file changes. MUST be invoked before any write attempt when the write gate is closed. Creates scoped approval via AskUserQuestion + TaskCreate, opens the write gate, and closes it when work is done. Triggers: write hook blocks an edit, agent is about to write files outside .craft/, agent needs to modify project source files. This skill requires user approval 100% of the time - never bypass AskUserQuestion."
allowed-tools: ["Read", "Bash", "Glob", "Grep", "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskList"]
---

# Write Approval

You are requesting permission to write files. This skill gates ALL writes outside `.craft/` and `.claude/` directories. It requires explicit user approval every single time - no exceptions, no bypass, no auto-approve.

## When to Use

Call this skill BEFORE your first write attempt when:
- The write hook has blocked you (or will block you)
- You're about to modify project source files
- You're about to create new files outside `.craft/`
- Any workflow stage involves writing to the project

Do NOT call this for writes to `.craft/` or `.claude/` directories - those are always allowed.

## The Flow

### Step 1: Describe the Scope

Before asking for approval, gather what you're about to do. Be specific:
- Which files will be created or modified
- What changes will be made (brief, not the full diff)
- Why (what triggered this - workflow stage, fix, feature work)

### Step 2: Ask for Approval (MANDATORY)

Use **AskUserQuestion**. This step CANNOT be skipped. Ever.

```
question: "I need write access to make these changes. Approve?"
header: "Write Access"
options:
  - label: "Approve"
    description: "{summary of what will be changed}"
  - label: "Deny"
    description: "Block these changes"
  - label: "Modify scope"
    description: "I want to adjust what's allowed"
```

**If "Deny"** -> Stop. Do not open the gate. Report to the caller that writes were denied.

**If "Modify scope"** -> Let the user describe the adjusted scope. Re-present the AskUserQuestion with the new scope. Loop until approved or denied.

**If "Approve"** -> Continue to Step 3.

### Step 3: Create Approval Tasks

Create exactly two tasks:

**Task 1 - The approved work:**
```
TaskCreate({
  subject: "Approved: {brief description of changes}",
  description: "Files: {file list}. Scope: {what was approved}.",
  activeForm: "Writing approved changes"
})
```
Set this task to `in_progress` immediately.

**Task 2 - Close the gate:**
```
TaskCreate({
  subject: "Close write gate",
  description: "Set CRAFT_WRITE_ENABLED='' after approved work is done.",
  activeForm: "Closing write gate"
})
```
Set `addBlockedBy` to Task 1's ID so it can't complete before the work is done.

### Step 4: Open the Gate

Run via Bash:
```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/update-global-state.sh CRAFT_WRITE_ENABLED true
```

The write gate is now open. The agent can write files.

### Step 5: Do the Work

The caller (workflow, fix skill, implementer, etc.) performs the approved changes. As work completes, the approved-work task stays `in_progress`.

**This skill does NOT do the writing itself.** It opens the gate and returns control to the caller. The caller writes, then calls back to close.

### Step 6: Close the Gate

When the approved work is done, the caller MUST close the gate:

1. Mark the approved-work task as `completed`:
```
TaskUpdate({ taskId: "{task-1-id}", status: "completed" })
```

2. Close the write gate:
```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/update-global-state.sh CRAFT_WRITE_ENABLED ""
```

3. Mark the close-gate task as `completed`:
```
TaskUpdate({ taskId: "{task-2-id}", status: "completed" })
```

## Safety Rules

1. **AskUserQuestion is mandatory.** Every invocation. No exceptions. If the skill is called 5 times in a session, the user is asked 5 times.
2. **Scope is enforced by visibility.** The user sees exactly what was approved via the Task description. If the agent writes files outside the approved scope, that's visible in the task trail.
3. **Gate closes explicitly.** The gate does not auto-close on a timer. The caller must close it. If the session ends with the gate open, `session-start.sh` will detect CRAFT_WRITE_ENABLED=true with no active story/workflow and reset it.
4. **No nesting.** If the gate is already open (from a story or another approval), this skill is not needed. Check first:
```bash
grep "CRAFT_WRITE_ENABLED" "${CRAFT_PROJECT_ROOT:-.}/.craft/.global-state"
```
If already `true`, skip this skill.
