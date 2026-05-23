---
name: archive
description: Archive completed task/spec work to ./.gtd/archive/
argument-hint: "[task_name]"
disable-model-invocation: true
---

<role>
You are an archiver. You move completed task work to the archive folder for historical reference.

**Core responsibilities:**

- Verify task work exists
- Create archive with task name and timestamp
- Move all task files to archive
- Clean up task folder
  </role>

<objective>
Archive completed task to keep workspace clean while preserving history.

**Flow:** Verify Exists → Create Archive → Move Files → Clean Up
</objective>

<context>
**Task name:** $ARGUMENTS (if not provided, ask user which task to archive)

**Source:**

- `./.gtd/<task_name>/` — Task work to archive

**Destination:**

- `./.gtd/archive/<task_name>-{timestamp}/` — Archived task work

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

## 3. Create Archive Directory

Generate archive name with timestamp:

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE_DIR="./.gtd/archive/<task_name>-${TIMESTAMP}"
mkdir -p "./.gtd/archive"
```

---

## 4. Move Task Folder

Move entire task folder to archive:

```bash
mv "./.gtd/<task_name>" "${ARCHIVE_DIR}"
```

---

## 5. Commit Archive

Commit the archive:

```bash
git add ./.gtd/archive/
git commit -m "chore: archive task <task_name> to {task_name}-${TIMESTAMP}"
```

---

## 6. Display Summary

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD ► TASK ARCHIVED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {task_name}
Archived to: ./.gtd/archive/{task_name}-{timestamp}/

Phases archived: {count}
Files archived: {count}

Task folder removed from ./.gtd/

─────────────────────────────────────────────────────
```

---

</process>

<forced_stop>
STOP. The workflow is complete. Do NOT automatically run the next command. Wait for the user.
</forced_stop>
