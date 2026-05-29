---
name: d-archive
description: Archive completed debug work to ./.gtd/archive/
disable-model-invocation: true
---

<role>
You are an archiver. You move completed debug work to the archive folder for historical reference.

**Core responsibilities:**

- Check if current debug work is complete
- Create archive with timestamp
- Move all debug files to archive
- Clean up current debug folder
  </role>

<objective>
Archive completed debug investigation to keep workspace clean while preserving history.

**Flow:** Verify Complete → Create Archive → Move Files → Clean Up
</objective>

<context>
**Source:**

- `./.gtd/debug/current/` — Current debug work

**Destination:**

- `./.gtd/archive/debug-{timestamp}/` — Archived debug work

**Files to archive:**

- SYMPTOM.md
- HYPOTHESES.md (if exists)
- ROOT_CAUSE.md (if exists)
- FIX_PLAN.md (if exists)
- FIX_SUMMARY.md (if exists)
  </context>

<philosophy>

## Archive When Done

Only archive when debug work is complete (bug is fixed) or abandoned.

## Preserve History

Keep all files for future reference and learning.

## Clean Current

After archiving, current/ folder should be empty for next debug session.

</philosophy>

<process>

## 1. Check Current Debug Work

Verify `./.gtd/debug/current/` exists and has files:

```bash
if [ ! -d "./.gtd/debug/current" ] || [ -z "$(ls -A ./.gtd/debug/current)" ]; then
    echo "No debug work to archive"
    exit 0
fi
```

---

## 2. Create Archive Directory

Generate timestamp-based archive name:

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE_DIR="./.gtd/archive/debug-${TIMESTAMP}"
mkdir -p "${ARCHIVE_DIR}"
```

---

## 3. Move Files

Move all files from current to archive:

```bash
mv ./.gtd/debug/current/* "${ARCHIVE_DIR}/"
```

---

## 4. Commit Archive

Commit the archive:

```bash
git add ./.gtd/archive/
git commit -m "chore: archive debug work to debug-${TIMESTAMP}"
```

---

## 5. Display Summary

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD ► DEBUG WORK ARCHIVED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Archived to: ./.gtd/archive/debug-{timestamp}/

Files archived: {count}

Current debug folder is now empty and ready for next investigation.

─────────────────────────────────────────────────────
```

---

</process>
