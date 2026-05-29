---
name: s:archive
description: Archive completed task/spec work to ./.gtd/archive/
argument-hint: "[task_name]"
disable-model-invocation: true
---

<role>
You are an archiver. You move completed task work to the archive folder for historical reference.

**Core responsibilities:**

- Verify task work exists
- Update BACKLOG.md to mark item complete
- Append completion event to JOURNAL.md
- Create archive with task name and timestamp
- Move all task files to archive
- Clean up task folder
  </role>

<objective>
Archive completed task to keep workspace clean while preserving history.

**Flow:** Verify Exists → Update Backlog → Log Journal → Create Archive → Move Files → Clean Up
</objective>

<context>
**Task name:** $ARGUMENTS (if not provided, ask user which task to archive)

**Source:**

- `./.gtd/<task_name>/` — Task work to archive

**Destination:**

- `./.gtd/archive/<task_name>-{timestamp}/` — Archived task work

**Updates:**

- `./.gtd/BACKLOG.md` — Mark item as `[x]` complete
- `./.gtd/JOURNAL.md` — Append completion event

**Files to archive:**

- SPEC.md
- ROADMAP.md (if exists)
- All phase folders with PLAN.md and SUMMARY.md
- Any other task-related files
  </context>

<philosophy>

## Archive When Done

Only archive when task is complete or abandoned.

## Preserve History

Keep all files for future reference and learning.

## Update State

Backlog and Journal must reflect the completion.

## Clean Workspace

After archiving, task folder is removed to keep .gtd/ clean.

</philosophy>

<process>

## 1. Determine Task Name

If no argument provided, ask user:

```text
Which task would you like to archive?

Available tasks:
- {task 1}
- {task 2}
```

---

## 2. Check Task Exists

Verify `./.gtd/<task_name>/` exists:

```bash
if [ ! -d "./.gtd/<task_name>" ]; then
    echo "Error: Task '<task_name>' not found"
    exit 1
fi
```

---

## 3. Update BACKLOG.md

**If `./.gtd/BACKLOG.md` exists:**

- Read the file
- Find the line matching the task name (e.g., `- [ ] **{task_name}**`)
- Change `[ ]` to `[x]`
- Write updated file

**Example:**

```
Before: - [ ] **audio-gateway** — Opus decoding, VAD
After:  - [x] **audio-gateway** — Opus decoding, VAD
```

---

## 4. Append to JOURNAL.md

**If `./.gtd/JOURNAL.md` exists:**

Append a new row to the journal table:

```markdown
| {date} | Task completed: {task_name} | Complete | {task_name} |
```

---

## 5. Create Archive Directory

Generate archive name with timestamp:

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE_DIR="./.gtd/archive/<task_name>-${TIMESTAMP}"
mkdir -p "./.gtd/archive"
```

---

## 6. Move Task Folder

Move entire task folder to archive:

```bash
mv "./.gtd/<task_name>" "${ARCHIVE_DIR}"
```

---

## 7. Commit Archive

Commit the archive and state updates:

```bash
git add ./.gtd/archive/ ./.gtd/BACKLOG.md ./.gtd/JOURNAL.md
git commit -m "chore: archive task <task_name> to {task_name}-${TIMESTAMP}"
```

---

## 8. Display Summary

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD ► TASK ARCHIVED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {task_name}
Archived to: ./.gtd/archive/{task_name}-{timestamp}/

Phases archived: {count}
Files archived: {count}

✓ BACKLOG.md updated
✓ JOURNAL.md updated
✓ Task folder removed from ./.gtd/

─────────────────────────────────────────────────────
```

---

</process>

<forced_stop>
STOP. The workflow is complete. Do NOT automatically run the next command. Wait for the user.
</forced_stop>
