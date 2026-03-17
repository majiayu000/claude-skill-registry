---
name: heal-skill
description: 'Automated skill maintenance. Detects and fixes common skill issues: missing frontmatter, name mismatches, unlinked references, empty directories, dead references. Triggers: "heal-skill", "heal skill", "fix skills", "skill maintenance", "repair skills".'
metadata:
  tier: meta
  dependencies: []
---

# /heal-skill — Automated Skill Maintenance

> **Purpose:** Detect and auto-fix common skill hygiene issues across the skills/ directory.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

---

## Quick Start

```bash
/heal-skill                    # Check all skills (report only)
/heal-skill --fix              # Auto-repair all fixable issues
/heal-skill skills/council     # Check a specific skill
/heal-skill --fix skills/vibe  # Fix a specific skill
```

---

## What It Detects

Six checks, run in order:

| Code | Issue | Auto-fixable? |
|------|-------|---------------|
| `MISSING_NAME` | No `name:` field in SKILL.md frontmatter | Yes -- adds name from directory |
| `MISSING_DESC` | No `description:` field in SKILL.md frontmatter | Yes -- adds placeholder |
| `NAME_MISMATCH` | Frontmatter `name` differs from directory name | Yes -- updates to match directory |
| `UNLINKED_REF` | File in references/ not linked in SKILL.md | Yes -- converts bare backtick refs to markdown links |
| `EMPTY_DIR` | Skill directory exists but has no SKILL.md | Yes -- removes empty directory |
| `DEAD_REF` | SKILL.md references a non-existent references/ file | No -- warn only |

---

## Execution Steps

### Step 1: Run the heal script

```bash
# Check mode (default) -- report only, no changes
bash skills/heal-skill/scripts/heal.sh --check

# Fix mode -- auto-repair what it can
bash skills/heal-skill/scripts/heal.sh --fix

# Target a specific skill
bash skills/heal-skill/scripts/heal.sh --check skills/council
bash skills/heal-skill/scripts/heal.sh --fix skills/council
```

### Step 2: Interpret results

- **Exit 0:** All clean, no findings.
- **Exit 1:** Findings reported. In `--fix` mode, fixable issues were repaired; re-run `--check` to confirm.

### Step 3: Report to user

Show the output. If `--fix` was used, summarize what changed. If `DEAD_REF` findings remain, advise the user to remove or update the broken references manually.

---

## Output Format

One line per finding:

```
[MISSING_NAME] skills/foo: No name field in frontmatter
[MISSING_DESC] skills/foo: No description field in frontmatter
[NAME_MISMATCH] skills/foo: Frontmatter name 'bar' != directory 'foo'
[UNLINKED_REF] skills/foo: refs/bar.md not linked in SKILL.md
[EMPTY_DIR] skills/foo: Directory exists but no SKILL.md
[DEAD_REF] skills/foo: SKILL.md links to non-existent refs/bar.md
```

---

## Notes

- The script is **idempotent** -- running `--fix` twice produces the same result.
- `DEAD_REF` is warn-only in `--fix` mode because the correct resolution (delete reference, create file, or update link) requires human judgment.
- When run without a path argument, scans all directories under `skills/`.

## Examples

### Running a health check across all skills

**User says:** `/heal-skill`

**What happens:**
1. The heal script scans every directory under `skills/`, checking each for the six issue types (missing name, missing description, name mismatch, unlinked references, empty directories, dead references).
2. Findings are printed one per line with issue codes (e.g., `[NAME_MISMATCH] skills/foo: Frontmatter name 'bar' != directory 'foo'`).
3. The script exits with code 1 if any findings exist, or 0 if all skills are clean.

**Result:** A diagnostic report showing all skill hygiene issues across the repository, with no files modified.

### Auto-fixing a specific skill

**User says:** `/heal-skill --fix skills/vibe`

**What happens:**
1. The heal script inspects only `skills/vibe/`, running all six checks against that skill.
2. For each fixable issue found (e.g., `MISSING_NAME`, `UNLINKED_REF`), the script applies the repair automatically -- adding the name from the directory, converting bare backtick references to markdown links, etc.
3. Any `DEAD_REF` findings are reported as warnings since they require human judgment to resolve.

**Result:** The `skills/vibe/SKILL.md` is repaired in place, with a summary of changes applied and any remaining warnings.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `DEAD_REF` findings persist after `--fix` | Dead references are warn-only because the correct fix (delete, create, or update) requires human judgment | Manually inspect each dead reference and either create the missing file, remove the link from SKILL.md, or update the path |
| Script reports `EMPTY_DIR` for a skill in progress | The skill directory was created but SKILL.md has not been written yet | Either add a SKILL.md to the directory or remove the empty directory. Running `--fix` will remove it automatically |
| `NAME_MISMATCH` fix changed the wrong name | The script always updates the frontmatter `name` to match the directory name, not the other way around | If the directory name is wrong, rename the directory first, then re-run `--fix` |
| Script exits 0 but a skill still has issues | The issue type is not one of the six checks the heal script detects | The heal script covers structural hygiene only. Content quality issues require manual review or `/council` validation |
| Running `--fix` twice produces different output | This should not happen -- the script is idempotent | File a bug. Check if another process modified the skill files between runs |
