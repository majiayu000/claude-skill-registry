---
name: session-checkpoint
description: >-
  This skill should be used when the user says "save checkpoint", "checkpoint",
  "continue", "resume", "resume work", "save my progress", "clear checkpoint",
  or "clear all checkpoints". Saves and resumes named session checkpoints to
  preserve progress across Claude Code sessions. Tracks accomplishments, failed
  approaches, and modified files. IMPORTANT:
  When the user says bare "continue" or "resume" at session start and MEMORY.md
  lists active checkpoints, always invoke this skill.
---

# Session Checkpoint

> **CRITICAL: This skill runs near context window limits. Minimize tool calls — no subagents, no file exploration. Use only conversation context. Write files in one shot.**

## Commands

- **Save:** `save checkpoint {name}`, `save checkpoint` (auto-picks name from context)
- **Resume:** `continue`, `continue {name}`, `resume` (auto-select if one checkpoint, list if many)
- **Cleanup:** `clear checkpoint {name}`, `clear all checkpoints`

---

## Save Procedure

### 1. Determine Name

If user gave a name, use it.

If no name given:
- Pick a short descriptive name from the current work (2-4 words, e.g., "my-feature") and use it directly — don't ask for confirmation. The user sees the name in the output.

Sanitize final name: lowercase, replace spaces/`/` with `-`, strip leading `-`.

### 2. Locate Memory Directory

Find the auto memory directory path from the system prompt line:
`You have a persistent auto memory directory at <path>`

### 3. Gather State

Run in a single bash call:

```bash
git branch --show-current && git status --short | head -10 && date '+%Y-%m-%d %H:%M'
```

From conversation context, determine:
- What was accomplished this session
- What failed or was abandoned (and why)
- Where work left off — don't infer next steps, but DO capture all actionable context the next session needs: pending decisions, proposed options, open questions
- Which files were modified

### 4. Find Active Plan

If the system prompt or conversation already references a plan file (`~/.claude/plans/*.md`), note its path and determine step N of M. Otherwise skip. **Do NOT search for or glob plan files.**

### 5. Write Checkpoint File

If `checkpoint-{name}.md` already exists, use `AskUserQuestion` to confirm — show the existing checkpoint's **Saved** date and **Left Off** summary, with options: "Overwrite" / "Different name" (user provides new name via "Other"). If they choose a different name, continue from this step with the new name.

Write `<memory_dir>/checkpoint-{name}.md`:

```markdown
# Checkpoint: {name}

- **Branch:** `{branch}`
- **Saved:** {YYYY-MM-DD HH:MM}
- **Plan:** `~/.claude/plans/{file}` (step N of M)

## Left Off
{1-3 lines describing where work stopped}

## Done This Session
- {accomplishments}

## Failed Approaches
- {what + why — or "None"}

## Modified Files
- {list}
```

Omit the **Plan:** line if no plan file exists.

### 6. Update MEMORY.md Index

**Always use `Edit` (not `Write`) for MEMORY.md changes** — parallel sessions would clobber each other with `Write`.

Read MEMORY.md. Find the `## Active Checkpoints` section.

- If checkpoint name already in index: update its line.
- If not: add a new bullet.
- If no `## Active Checkpoints` section exists: insert it after the first `#` heading. If MEMORY.md doesn't exist, create it with `# Project Memory` as the heading.

Bullet format:
```
- **{name}** ({branch}, {Mon DD}) — {one-line summary}
```

Keep the ``Resume any: `continue` or `continue {name}` `` line after the bullets.

Do NOT touch any other sections in MEMORY.md.

### 7. Output

Keep output minimal — this often runs near end of context window.

```
Checkpoint "{name}" saved. Resume anytime: `continue {name}`
```

That's it. Don't ask follow-up questions. Don't suggest `/compact` or `/clear` — the user manages their own context window.

---

## Resume Procedure

### 1. Determine Name

If user gave a name, use it.
If no name given:
- List `checkpoint-*.md` files in memory directory
- If exactly one: use it automatically
- If multiple: use `AskUserQuestion` with checkpoint names as options (include branch and date in each option's description)
- If none: report "No saved checkpoints found." and stop

### 2. Read Checkpoint File

Read `<memory_dir>/checkpoint-{name}.md`.
If file missing: remove the orphaned bullet from MEMORY.md's `## Active Checkpoints`, report "Checkpoint file missing (cleaned up stale entry)", and stop.

### 3. Check Branch

```bash
git branch --show-current
```

If current branch differs from checkpoint's branch, warn:
```
Warning: You're on `{current}` but checkpoint was saved on `{saved}`. Switch with: git checkout {saved}
```

Continue regardless — user decides.

### 4. Load Plan

If checkpoint references a plan file, read it.

### 5. Present and Begin

Output the checkpoint summary and last context. If **Failed Approaches** is non-empty, include them:
```
⚠ Previously failed: {approach} — {why}
```

### 6. Auto-Clear

The checkpoint is now consumed — context is live. Delete the checkpoint file and remove its bullet from MEMORY.md's `## Active Checkpoints` (same as Cleanup steps 1-2). If no bullets remain, remove the entire section.

Do NOT mention the cleanup to the user. They see only the summary from step 5, then wait for their direction.

---

## Cleanup Procedure

### 1. Delete File

Remove the checkpoint file via Bash:
```bash
rm <memory_dir>/checkpoint-{name}.md
```

### 2. Update MEMORY.md

Remove the bullet for `{name}` from `## Active Checkpoints`.
If no bullets remain, remove the entire section (header + resume line).

### 3. Output

```
Cleared checkpoint "{name}"
```

### `clear all checkpoints`

Glob `checkpoint-*.md` in memory directory. Delete all matches. Remove the entire `## Active Checkpoints` section (header + bullets + resume line) from MEMORY.md. Output:

```
Cleared {N} checkpoint(s)
```
