---
name: start-task
description: "Start working on a beads task (claim, gather context, define acceptance criteria)"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, AskUserQuestion, TaskList, SendMessage
---

# Start Beads Task: $ARGUMENTS

You are starting work on a beads task. Follow this checklist precisely.

## 0. Parse Arguments

The command format is: `/start-task <task-id> [--handoff "<context>"]`

Parse `$ARGUMENTS` to extract:
- `task_id`: The beads task ID (everything before any flags)
- `handoff_context`: Optional inline handoff text (content in quotes after `--handoff` flag)

Examples:
- `/start-task MoneyPrinter-46j.1` → task_id = `MoneyPrinter-46j.1`
- `/start-task MoneyPrinter-46j.1 --handoff "Use 3% tolerance"` → with handoff context

## 1. Validate and Claim Task (FIRST!)

**CRITICAL: Claim the task immediately to prevent race conditions with parallel workers.**

```bash
# Validate task exists
bd show <task_id>
```

If the task doesn't exist, stop and report the error.

If the task is already `in_progress` or `closed`, warn the user:
- If `in_progress`: "This task is already claimed. Another worker may be on it. Proceed anyway?"
- If `closed`: "This task is already closed. Did you mean a different task?"

**Claim it immediately:**

```bash
bd update <task_id> --status in_progress
bd sync
```

This must happen BEFORE any other setup (branch creation, context gathering, etc.) to minimize the window where two workers might claim the same task.

## 2. Display Handoff Context (if provided)

If handoff context was provided, display it prominently:

```
==============================================
HANDOFF CONTEXT FROM PREVIOUS SESSION
==============================================
<handoff_context>
==============================================
```

**Note**: This is supplementary guidance from an orchestrating session. Still gather full project context and read the task directly — the handoff supplements but doesn't replace normal setup.

## 3. Rename Conversation

Rename this conversation to the task ID and title for easy reference later:

```
/rename <task_id>: <task title>
```

For example: `/rename frq: Implement backtest engine`

## 4. Gather Project Context

Read these files to understand the project:
- `CLAUDE.md` - Development guidelines
- `PROJECT_SPEC.md` - Project specification (if exists)
- `AGENTS.md` - Agent workflow documentation (if exists)
- `README.md` - Project overview

## 5. Check Recent Work

```bash
bd list --all | head -20
git log --oneline -10
```

Understand what's been done recently and what state the project is in.

## 6. Check Task Dependencies

```bash
bd show <task_id>
```

Look at the "Blocked by" section. If this task has unmet dependencies, warn the user and ask if they want to proceed anyway.

### 6.1 Sibling Task Awareness (Team Context)

If you are on a team (check if TaskList returns results):

1. Run TaskList to see sibling tasks and their owners
2. Identify tasks that produce output you consume or vice versa
3. If found, message that teammate to coordinate on shared interfaces:
   - Use SendMessage with type="message" and the peer's teammate name
   - Briefly describe what you'll need from them or provide to them
   - Don't block on a response — continue with your work

## 6.5 Research Phase (Conditional)

### High-Risk Indicators (Research First)

Research is recommended when the task involves:
- **Security**: authentication, authorization, encryption, secrets
- **Payments**: billing, subscriptions, transactions, financial data
- **External APIs**: third-party integrations, webhooks, OAuth
- **Data migrations**: schema changes, data transformations
- **New frameworks/libraries**: unfamiliar dependencies

### Research Agents to Consider

1. **framework-docs-researcher**
   - Read: `~/.claude/agents/research/framework-docs-researcher.md`
   - Use when: Task involves libraries or frameworks
   - Checks: Documentation, deprecation warnings, best practices

2. **best-practices-researcher**
   - Read: `~/.claude/agents/research/best-practices-researcher.md`
   - Use when: Architectural decisions needed
   - Provides: Industry best practices, pattern recommendations

### Launch Research (if needed)

```
Use Task tool with subagent_type=general-purpose:

Task: [appropriate-researcher]
- Read agent definition from ~/.claude/agents/research/
- Provide task context and requirements
- Return: Relevant findings, recommendations, warnings
```

### Skip Research If

- Internal refactoring only (no new patterns)
- Strong patterns already documented in CLAUDE.md
- Established team conventions for this type of work
- Simple bug fix with clear scope

### Document Research Findings

If research was conducted, update the task:
```bash
bd update <task_id> --notes "Research: <brief summary of findings>"
```

---

## 7. Verify Branch Isolation

Ensure you are on a task-specific branch, not `main` or `master`. Workers must isolate their changes on dedicated branches.

```bash
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
  echo "WARNING: On main branch. Creating task branch..."
  git checkout -b <task_id>
fi
echo "Running on branch $(git branch --show-current)"
```

## 8. Assess Task Size

**Philosophy: Task-sized work** — Tasks should fit comfortably in context.

Now that you can see the codebase, evaluate whether this task is appropriately sized:

**Signs the task is too large:**
- Multiple independent features bundled together
- Requires changes across 10+ files
- Has vague scope like "refactor the entire X system"
- You anticipate needing a handoff mid-task

**If too large**, present options to the user:

```
This task seems large for a single session. Options:

1. **Break it down** — I'll create subtasks and we pick one to start
2. **Proceed anyway** — Work on it knowing we may need a handoff
3. **Scope it down** — Redefine acceptance criteria to a smaller slice

Which approach?
```

**If user chooses "Break it down":**
```bash
# Create subtasks under the parent (--parent = containment, not blocking)
bd create --title="Subtask: <part 1>" --type=task --priority=<same> --parent <parent-task-id>
bd create --title="Subtask: <part 2>" --type=task --priority=<same> --parent <parent-task-id>

# Unclaim the parent (it's now a container)
bd update <parent-task-id> --status open
```

Note: No `bd dep add` needed — subtasks are children, not blocked. If subtasks have ordering between them (part 2 depends on part 1), add `bd dep add <part-2-id> <part-1-id>` explicitly.

Then ask: "Which subtask should we work on? I'll switch to that task."

If they pick a subtask, **start over from step 1** with the subtask ID.

**If appropriately sized**, continue to step 9.

## 9. Define Acceptance Criteria

**Philosophy: Bounded autonomy** — Define "done" before coding.

Work with the user to establish clear acceptance criteria. Use `AskUserQuestion` to confirm:

```
Before I start, let me confirm the acceptance criteria:

1. [ ] <functional requirement 1>
2. [ ] <functional requirement 2>
3. [ ] <edge case or constraint>
4. [ ] Tests pass
5. [ ] /finish-task run (creates PR, session summary, closes task)

Is this complete? Anything to add or change?
```

> **Verification discipline** (from `/verify`): Each criterion must be independently verifiable. For every acceptance criterion, you should be able to name the command that proves it. If you can't, the criterion is too vague — rewrite it.

**IMPORTANT**: Items 4 and 5 are ALWAYS required and non-negotiable:
- **Tests pass** — Code must be verified working
- **`/finish-task` run** — The session is not complete without this. It creates the PR, generates a session summary for the orchestrator, and closes the task. Skipping this breaks the coordination workflow.

**Good acceptance criteria are:**
- **Specific** — "User can log in with email/password" not "authentication works"
- **Testable** — Can be verified with a test or clear manual check
- **Bounded** — Clear what's in scope and what's not

Record the agreed criteria:
```bash
bd update <task_id> --notes "Acceptance: <brief summary of criteria>"
```

## 10. Clarify Ambiguities

**CRITICAL**: Before writing any code, use `AskUserQuestion` to resolve any remaining ambiguities:

- Implementation approach if multiple valid options exist
- Edge cases not covered by acceptance criteria
- Integration points with existing code
- Testing strategy

Keep asking until you have a clear picture. Do NOT proceed with assumptions.

Example questions:
- "The task mentions X but doesn't specify Y - which approach do you prefer?"
- "Should this handle edge case Z, or is that out of scope?"
- "I see two ways to implement this: A or B. Do you have a preference?"

## 11. Begin Implementation

Once:
- Task is appropriately sized (or user approved proceeding)
- Acceptance criteria are defined
- Ambiguities are resolved

Ask: "Ready to begin implementation?"

Only start coding after the user confirms.

---

## 12. CRITICAL: Task Completion Contract

**YOUR WORK IS NOT DONE UNTIL YOU RUN `/finish-task <task-id>`**

When implementation is complete (tests pass, code works), you MUST run:

```
/finish-task <task-id>
```

This command handles everything required to properly close out:
- Creates the PR
- Runs automated code review
- Generates session summary for orchestrator
- Closes the task in beads

**DO NOT**:
- Stop the session without running `/finish-task`
- Tell the user "done!" without running `/finish-task`
- Consider the task complete just because tests pass
- Hand off without `/finish-task` (notify the team lead if work is incomplete)

The orchestrator depends on your session summary to coordinate parallel work. A task without a session summary is invisible to coordination.
