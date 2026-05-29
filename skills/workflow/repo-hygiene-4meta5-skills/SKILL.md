---
name: repo-hygiene
description: Comprehensive repository housekeeping: pre-work checks, documentation updates,
writing style, and cleanup. Use when: (1) starting work on a repo, (2) completing
tasks, (3) editing markdown files, (4) cleaning up test artifacts.

category: habits
user-invocable: true
---

# Repo Hygiene

Comprehensive repository housekeeping: pre-work validation, documentation updates, writing style, and cleanup.

---

## Pre-Work Checks

**MANDATORY** before adding files or making structural changes.

### Before Adding Files

1. **Find existing examples** of similar files
2. **State the correct location** based on those examples
3. **Tell the user your plan** and wait for confirmation
4. **Send updates** during work

If you skip any step: **BLOCKED**

### Finding Patterns

```bash
# For skills
ls -la .claude/skills/ | head -10
find . -name "SKILL.md" -type f | head -10

# For any file type
find . -name "*.ts" -type f | head -10
```

### Self-Check Before File Creation

1. Did I check existing patterns?
2. Did I tell the user my plan?
3. Did I wait for confirmation?
4. Did I send updates during work?

If any answer is "no": **STOP and fix it.**

---

## Documentation Updates

Automatically update project documentation after task completion.

### Trigger Conditions

Invoke after:
- Completing any task
- Adding a new feature
- Fixing a bug
- Refactoring code

### PLAN.md Updates

All plan updates go to root `PLAN.md`. This is the single source of truth.

**Mark completed items:**
```markdown
## Current Sprint
- [x] Implement user authentication  # Was [ ]
```

**Add discovered work:**
```markdown
## Backlog
- [ ] (discovered) New task from implementation
```

**Move completed items with timestamp:**
```markdown
## Completed
- [x] Task description (2026-01-30)
```

### README.md Updates

Update when:
- New user-facing feature added
- API changed
- New command available
- Installation steps changed

### Alphabetical Ordering

All skill lists and tables in documentation (README.md, CLAUDE.md) must be sorted alphabetically by skill name. Within categorized sections, sort alphabetically within each category.

**Check after any skill addition or rename:**
```bash
# Verify alphabetical order in markdown tables
grep '^\| \[' README.md  # Visual check: names should be A-Z within each section
grep '^\|' CLAUDE.md     # Visual check: names should be A-Z
```

If out of order: **fix before committing.**

### Link Validation

Verify all markdown links resolve before committing:

```bash
# Find all markdown links and check they exist
grep -oE '\[.*?\]\(\.?/?[^)]+\)' README.md | \
  sed -E 's/.*\(([^)]+)\)/\1/' | \
  while read link; do
    [ -e "$link" ] || echo "BROKEN: $link"
  done
```

Check for:
- **Relative links** (./path/to/file.md): Must resolve from README location
- **Anchor links** (#section): Must match a heading in the target file
- **External links**: Verify with curl if critical

Run validation after any documentation update.

### Pre-Merge Cleanup

When preparing to merge:

```bash
# 1. Sync CLAUDE.md with installed skills
skills claudemd sync

# 2. Scan for test artifacts and slop
skills hygiene scan

# 3. If slop found, clean it
skills hygiene clean --confirm

# 4. Update PLAN.md with completed work

# 5. Commit and push
git add -A && git commit -m "chore: pre-merge cleanup" && git push
```

---

## Writing Style

Use for all markdown files: README.md, PLAN.md, documentation.

### Voice

- Write like speaking to an intelligent friend
- Short sentences. Direct claims. No hedging.
- Active voice, not passive
- State claims confidently

### Punctuation Rules

- **Never use em dashes (—)**
- Use periods and new sentences for separate thoughts
- Use commas for simple asides
- Use parentheses for clarifying information
- Use colons for lists or elaboration

### Structure

- Start with the point, not background
- One idea per paragraph
- Headers should be claims, not topics
- End sections when the point is made

### Quality Checklist

- [ ] No em dashes in content
- [ ] Sentences are short and direct
- [ ] Opens with the main point
- [ ] Code examples are minimal
- [ ] Tables used for structured data

---

## Slop Cleanup

Detect and clean AI-generated slop from your project.

### Quick Start

```bash
# Scan for slop
skills hygiene scan

# Preview what would be deleted
skills hygiene clean --dry-run

# Actually delete slop
skills hygiene clean --confirm
```

### What is Slop?

| Pattern | Example | Action |
|---------|---------|--------|
| `test-skill-*` | `test-skill-1234567890` | Delete |
| Timestamped | `my-skill-1706625000000` | Review |
| `_temp_*` | `_temp_claude-svelte5-skill` | Review |
| Placeholder | "NEW content with improvements!" | Delete |

### CLAUDE.md Cleanup

Check for:
- **Stale references**: Skills listed but not installed
- **Duplicate references**: Same skill listed multiple times

Run `skills claudemd sync` to fix.

### Decision Tree

```
Found test-skill-*?
├─ YES → Delete (safe)
└─ NO
   ├─ Found _temp_* with good content?
   │  └─ Rename to proper name, delete _temp_ version
   ├─ Found placeholder content?
   │  └─ Delete or rewrite
   └─ Found stale CLAUDE.md refs?
      └─ Run: skills claudemd sync
```

---

## Related Commands

- `skills validate` - Check skill quality
- `skills claudemd sync` - Sync CLAUDE.md with installed skills
- `skills list` - Show installed skills

---

## Rationalizations (Do Not Skip)

| Excuse | Why It's Wrong | Required Action |
|--------|----------------|-----------------|
| "I know where it goes" | You were wrong last time | Check existing patterns |
| "Too small to document" | Small changes accumulate | Update PLAN.md |
| "I'll remember" | Context is lost between sessions | Write it down |
| "It's obvious" | Clearly it wasn't | Confirm with user |
| "Just a bug fix" | Bugs deserve tracking | Mark complete |

---

## Reference Files

For README writing guidelines, see:
- `references/readme-structure.md` - Section ordering
- `references/readme-badges.md` - Badge patterns
- `references/readme-cli-docs.md` - CLI documentation
- `references/readme-checklist.md` - Full checklist

For prose quality and markdown rewriting support, use:
- `../paul-graham/SKILL.md` - Direct, high-signal writing and editing workflow