---
name: dk-changelog
description: Generate changelog entries from git diffs, prepend to CHANGELOG.md, and optionally commit + PR. Use when the user wants to update the changelog.
argument-hint: [--dry-run | --commit]
allowed-tools: Bash, Read, Edit, Write, Task
---

# Changelog Creator

Generate a changelog entry from git changes, prepend it to `CHANGELOG.md`, and optionally commit + raise a PR.

## Usage

```
/dk-changelog              → full flow: write + commit + PR
/dk-changelog --dry-run    → print the entry only (no file changes)
/dk-changelog --commit     → write + commit (no PR)
```

Arguments are passed via `$ARGUMENTS`.

## Instructions

### Step 1: Parse arguments

Check `$ARGUMENTS` for `--dry-run` or `--commit`. Default behavior (no args) is the full flow: write, commit, and open a PR.

### Step 2: Gather raw git data

Run these commands to collect the raw material. This is mechanical — just capture the output:

```bash
# What branch are we on?
git rev-parse --abbrev-ref HEAD

# Commits on this branch that aren't on main
git log main..HEAD --oneline --no-merges 2>/dev/null

# File-level summary
git diff --stat main...HEAD 2>/dev/null
git diff main...HEAD --name-status 2>/dev/null

# Unstaged/untracked
git diff --stat HEAD
git diff --name-status HEAD
git status --short | grep "^??"
```

If there are no commits diverging from main AND no staged/unstaged changes, tell the user there's nothing to changelog and stop.

If on `main` with no diverging commits, fall back to diffing against the previous commit:
```bash
git log -1 --oneline
git diff HEAD~1 --stat
git diff HEAD~1 --name-status
```

Also read the existing `CHANGELOG.md` so the subagent can match the format.

### Step 3: Delegate to haiku subagent

**Use the Task tool** with `subagent_type: "general-purpose"` and `model: "haiku"` to do the heavy lifting. The subagent reads diffs, understands the changes, and generates the changelog entry.

Pass the subagent a prompt containing:
1. All the git output from Step 2
2. The existing `CHANGELOG.md` content (for format reference)
3. The full generation rules below
4. A clear instruction: "Read the actual diffs by subsystem, then generate a changelog entry. Return ONLY the markdown entry, nothing else."

The subagent prompt must include these instructions:

---

**Read actual diffs by subsystem.** File names alone are not enough — read the actual diffs to understand what changed. Group by subsystem:

```bash
# Backend / orchestrator / CLI
git diff HEAD -- odin/src/ taskit/taskit-backend/

# Frontend — read separately, easy to miss
git diff HEAD -- taskit/taskit-frontend/src/

# Types, models, migrations
git diff HEAD -- taskit/taskit-frontend/src/types/ taskit/taskit-backend/tasks/models.py taskit/taskit-backend/tasks/migrations/

# Docs and config
git diff HEAD -- odin/docs/ odin/AGENTS.md odin/claude.md odin/README.md docs/

# Tests
git diff HEAD -- odin/tests/ taskit/taskit-backend/tests/
```

For new untracked files, read them to understand what they add. If a diff group is very large (>500 lines), skim the first 300 lines and the `--stat` for that group.

**Generate a changelog entry** in this format:

```markdown
## YYYY-MM-DD — [Short Human-Friendly Title]
**`<short-hash>`** — [plain-English summary of the theme]

### Added
- [what's new, described in terms of capability]

### Changed
- [what works differently now — user/developer impact]

### Deleted
- [what's gone]

---
```

**Rules:**

- **Completeness over brevity.** Every meaningful change should appear. Someone reading the changelog should understand everything that shipped without looking at the diff.
- Use today's date and the latest commit's short hash (or "unstaged" for uncommitted work)
- Only include sections (Added/Changed/Deleted) that have entries — omit empty ones
- **Write for humans, not machines.** Say "Added executing time tracking to task cards" not "Added `executingTimeMs` field to `Task` type in `types/index.ts`"
- Describe *what changed and why it matters*, not which files were touched
- **Scale detail to changeset size:**
  - Small changeset (1-5 files): 2-4 bullets
  - Medium changeset (5-20 files): 5-10 bullets
  - Large changeset (20+ files): 10-20 bullets, organized by area if helpful
- **Don't collapse distinct changes into one bullet.** If the frontend got a new component AND the backend got a new comment type AND the CLI got restructured, those are three bullets.
- **Frontend changes deserve their own bullets.** New components, UX changes (e.g. multi-select → single-select), new fields on forms, visual changes (badges, icons, colors) — each gets called out.
- **Backend and API changes deserve their own bullets.** New fields on models/types, new API parameters, changed parsing logic, new migrations.
- Include file paths only when the file IS the feature (e.g. a new config module, a new migration)
- Match the tone and format of the existing CHANGELOG.md entries provided

Return ONLY the markdown entry (from `## ` to `---`), nothing else.

---

### Step 4: Apply the entry

Take the entry returned by the subagent.

**If `--dry-run`**: Print the generated entry to the user and stop. Do not modify any files.

**Otherwise**: Prepend the new entry to `CHANGELOG.md` immediately after the `# Changelog — harness-kit` title line (line 1) and its following blank line. Use the Edit tool to insert the new content.

### Step 5: Commit (unless `--dry-run`)

```bash
# Create a changelog branch if not already on one
git checkout -b changelog/$(date +%Y-%m-%d) 2>/dev/null || true

# Stage and commit
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG.md"
```

### Step 6: Open PR (default mode only)

Only if running in default mode (no `--dry-run`, no `--commit`):

```bash
git push -u origin HEAD

gh pr create \
  --title "docs: update CHANGELOG.md" \
  --body "$(cat <<'EOF'
## Summary
- Auto-generated changelog entry from recent changes

## Content
[Paste the generated changelog entry here]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Return the PR URL to the user.

### Step 7: Summary

Tell the user what was done:
- **dry-run**: "Here's your changelog entry. Run `/dk-changelog` to write and PR it."
- **commit**: "Changelog updated and committed on branch `changelog/YYYY-MM-DD`."
- **default**: "Changelog updated, committed, and PR opened: [URL]"
