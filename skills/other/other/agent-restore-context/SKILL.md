---
name: agent-restore-context
description: Manage restore context files so skills can survive /clear and /compact. Use to write, delete, check, or list .agent-restore-context-* files.
disable-model-invocation: false
argument-hint: <action> <skill-name> [content]
allowed-tools: Bash, Grep, Glob, Read, Edit, Write
---

# Agent Restore Context

Manage `.agent-restore-context-<skill-name>` files in the project root. These
files are automatically injected into context after `/clear` or `/compact` by
a `SessionStart` hook, allowing skills to resume where they left off.

## Arguments

- `action` (required): One of `write`, `delete`, `check`, or `status`
- `skill-name` (required for write/delete): The skill name used as the file suffix
- `content` (required for write): The full prompt content to inject after a
  context reset

## Usage Examples

- `/agent-restore-context write jira-implement-task` — create or overwrite a
  restore context file with the provided content
- `/agent-restore-context delete jira-implement-task` — remove the file when
  the workflow is complete
- `/agent-restore-context check` — verify the hook is set up, offer to install
  if not
- `/agent-restore-context status` — list all active restore context files

## Process

### 1. Verify Hook Setup

Read `.claude/settings.json` and `.claude/settings.local.json` (if it exists).
Search both for `restore-context`. If not found:

- If the action is `check`, invoke `/agent-restore-context-setup` and stop.
- For any other action, warn the user that the hook is not configured and ask
  if they want to run `/agent-restore-context-setup` first. Do not proceed
  with write until the hook is confirmed.

### 2. Execute Action

#### `write <skill-name>`

1. Write `.agent-restore-context-<skill-name>` to the project root with the
   provided content (creates or overwrites). The content should be a complete,
   self-contained prompt that tells the model how to resume. Recommended
   structure (callers may use any format):

   ```
   === <SKILL-NAME> — RESUMED AFTER CONTEXT RESET ===

   <Key state: ticket, branch, current task, etc.>

   You MUST do the following before any other work:
   1. Invoke /<skill-name> <arguments> to reload the full skill instructions.
   2. <Read relevant plan/state files>
   3. <Read relevant source/test files>
   4. Continue from where you left off.

   Do NOT start any work until you have completed the above steps.
   === END RESUMED CONTEXT ===
   ```

2. Confirm the file was written and its path.

#### `delete <skill-name>`

1. Delete `.agent-restore-context-<skill-name>` from the project root.
2. If the file does not exist, report that it was already removed (not an error).
3. Confirm the deletion.

#### `check`

1. Report whether the hook is configured (found in settings).
2. List any active `.agent-restore-context-*` files in the project root.
3. If the hook is not configured, invoke `/agent-restore-context-setup`.

#### `status`

1. List all `.agent-restore-context-*` files in the project root.
2. For each file, show the skill name (derived from the filename suffix) and
   the first few lines of content as a preview.
3. If no files exist, report that no active restore contexts were found.

## Guidelines

- Always read target files before modifying them
- All actions are idempotent (check/status/delete are safe to repeat;
  write silently overwrites)
- Do not create `.agents/` directories — only use them if they already exist

---

**Agent restore context: $ARGUMENTS**
