---
name: unikit-todo
description: Manage project TODO list in .unikit/TODO.md. Add tasks, mark tasks complete, and view task status. Use when the user says "add todo", "todo", "task", "add task", "complete task", "mark done", "what's left to do", or wants to track work items, reminders, or notes for later. Also trigger when user says things like "remind me to...", "don't forget to...", "we need to...", "later we should...".
argument-hint: "[task description] | complete [description] | list | purge"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UniKit TODO — Task List Manager

Manage a lightweight TODO checklist stored in `.unikit/TODO.md`.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

## File Location

The TODO file is always `.unikit/TODO.md`.

## Workflow

### Step 0: Load Skill Context

Read `.unikit/skill-context/unikit-todo/SKILL.md` if it exists. Treat it as project-level overrides — when it conflicts with this SKILL.md, the skill-context wins.

### Step 1: Determine Mode

Parse the arguments to determine the operating mode:

```
├── No arguments?                        → Mode: Interactive (ask what to add)
├── Exactly "complete" (no description)  → Mode: Complete (Auto-Verify)
├── "complete <description>"             → Mode: Complete (Manual)
├── Starts with "list"                   → Mode: List
├── Starts with "purge"                  → Mode: Purge
└── Otherwise                            → Mode: Add
```

### Step 2: Resolve File Path

1. The file path is always `.unikit/TODO.md`
2. Check if the file exists. If not, create it using the template from `{{skills_dir}}/{{self_name}}/assets/todo-template.md`

### Step 3: Execute Mode

#### Mode: Add

The user provided a task description. Your job is to refine it into a concise, actionable task entry while preserving all important details and meaning.

**Refinement guidelines:**
- Shorten verbose descriptions to 1-2 clear sentences
- Keep technical details, file paths, class names, and specifics intact
- Use imperative form ("Add...", "Fix...", "Refactor...", "Investigate...")
- Remove filler words and conversational tone
- If the description mentions multiple distinct tasks, split them into separate entries

**Adding the task:**
1. Read the TODO file
2. **Duplicate check:** Compare the refined description against all existing tasks (both `- [ ]` and `- [x]`) by semantic similarity. If a task with the same meaning already exists, do NOT add it — instead show the user the existing task with its date and status:
   ```
   ⚠️ Task already exists:
   - [x] Fix item duplication in inventory on rapid sell button clicks `2026-03-10` (completed)
   ```
   or:
   ```
   ⚠️ Task already exists:
   - [ ] Fix item duplication in inventory on rapid sell button clicks `2026-03-10` (pending)
   ```
   Then stop — do not add a duplicate.
3. Read the task entry template from `{{skills_dir}}/{{self_name}}/assets/task-entry-template.md`
4. Fill in the template:
   - `{{date}}` → current date in `YYYY-MM-DD` format
   - `{{description}}` → the refined task description (written in the language from `.unikit/config.yaml`, `language.artifacts`)
5. Append the entry to the end of the TODO file (before any closing markers if present)
6. Confirm to the user what was added

**Example:**

User input: "надо бы потом не забыть поправить тот баг с инвентарём, когда предметы дублируются при быстром нажатии на кнопку продажи"

Refined (if language is `ru`): `Исправить дублирование предметов в инвентаре при быстром нажатии кнопки продажи`

Refined (if language is `en`): `Fix item duplication in inventory on rapid sell button clicks`

#### Mode: Complete (Manual)

The user wants to mark tasks as done. The argument after `complete` is a description of what was completed.

1. Read the TODO file
2. Find all unchecked tasks (`- [ ]`) that are relevant to the description — match by semantic similarity, not exact string match. A task about "fix inventory duplication" should match "completed the inventory bug fix"
3. If exactly one match is found, mark it done: change `- [ ]` to `- [x]`
4. If multiple matches are found, show them to the user and ask which to complete (or offer to complete all)
5. If no matches are found, tell the user no relevant tasks were found
6. Confirm what was completed

#### Mode: Complete (Auto-Verify)

The user typed `complete` with no description. Instead of asking what to complete, proactively scan the codebase to check whether any open tasks have already been resolved.

**Process each task one at a time — do not skip ahead or batch them.**

1. Read the TODO file and collect all unchecked tasks (`- [ ]`)
2. If there are no unchecked tasks, tell the user everything is already done
3. Take the **first** unchecked task and analyze it:
   a. Extract code references from the task text — file names, class names, method names, line numbers, variable names, or any identifiable code artifacts
   b. If the task has no recognizable code references (e.g., it's a pure process/design task like "discuss architecture with team"), skip it and move to the next task
   c. Use `Grep` and `Glob` to locate the relevant code in the codebase
   d. Read the relevant files and assess whether the issue described in the task has been resolved

4. **Evaluation criteria** — consider a task resolved if:
   - The specific code issue mentioned no longer exists (e.g., hardcoded value was replaced, missing feature was added)
   - The file/method mentioned was refactored and the problem described is no longer present
   - The code now implements what the task asked for

5. **If the task appears resolved:**
   - Show the task text to the user
   - Briefly explain what you found in the code that indicates the task is done (include file path and relevant code snippet)
   - Ask: should this task be marked as complete? Wait for the user's response
   - If the user confirms → mark it done (`- [ ]` → `- [x]`) and proceed to the next unchecked task
   - If the user declines → leave it open and proceed to the next unchecked task

6. **If the task appears NOT resolved:**
   - Show the task text to the user
   - Briefly explain what you found (or didn't find) and why the task still seems open
   - Ask: should this task be marked as complete anyway, or keep it open? Wait for the user's response
   - Act on the user's decision, then proceed to the next task

7. **If the relevant code cannot be found** (file deleted, renamed, etc.):
   - Show the task text and explain that the referenced code couldn't be located
   - Ask the user what to do: mark complete, keep open, or remove the task entirely

8. Repeat steps 3–7 for each remaining unchecked task. **Always wait for the user's response before moving to the next task.**

9. After all tasks have been reviewed, show a summary of what changed (how many marked complete, how many kept open, how many skipped)

#### Mode: List

Show all tasks grouped by status:

1. Read the TODO file
2. Display unchecked tasks (`- [ ]`) under a "Pending" header
3. Display checked tasks (`- [x]`) under a "Completed" header
4. Show total counts

#### Mode: Purge

Remove all completed tasks (`- [x]`) from the TODO file to keep it clean.

1. Read the TODO file
2. Collect all completed tasks (`- [x]`)
3. If no completed tasks exist, tell the user there's nothing to purge
4. Show the list of completed tasks that will be removed and ask for confirmation
5. On confirmation, read the entire file, filter out all `- [x]` lines, collapse any resulting consecutive blank lines into a single blank line, and write the cleaned content back using `Write`
6. Confirm how many tasks were purged

#### Mode: Interactive

No arguments were provided. Ask the user what task they'd like to add. Then proceed as Mode: Add.

## Date Handling

Always use the current date. Get it from the system. Format: `YYYY-MM-DD`.
