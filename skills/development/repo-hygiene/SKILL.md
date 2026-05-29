---
name: repo-hygiene
description: |
  Detect and clean AI-generated slop from skills directories. Use when: (1) test-skill-*
  directories accumulate from testing, (2) CLAUDE.md has stale skill references,
  (3) placeholder content exists in skills. Provides scan, clean, and CLAUDE.md sync.
category: development
user-invocable: true
---

# Repo Hygiene

Detect and clean AI-generated slop (test skills, placeholder content) from your project.

## Quick Start

```bash
# Scan for slop
skills hygiene scan

# Scan including package subdirectories
skills hygiene scan -r

# Preview what would be deleted
skills hygiene clean --dry-run

# Actually delete slop
skills hygiene clean --confirm
```

## What is Slop?

Slop is auto-generated or placeholder content that shouldn't be committed:

| Pattern | Example | Action |
|---------|---------|--------|
| `test-skill-*` | `test-skill-1234567890` | Delete |
| Timestamped | `my-skill-1706625000000` | Review |
| `_temp_*` | `_temp_claude-svelte5-skill` | Review (may need rename) |
| Placeholder | "NEW content with improvements!" | Delete |

## Detection Patterns

### test-skill-* (Auto-Delete)

Skills matching `/^test-skill-\d+$/` are auto-generated test data.
These are always safe to delete.

### Timestamped Names (Review)

Skills ending with 13-digit timestamps (`-1706625000000`) may be
auto-generated. Review before deleting.

### _temp_ Prefix (Review)

Skills starting with `_temp_` were likely created as temporary work.
They may contain valuable content that needs proper naming.

**Recommended action**: Rename to remove prefix if content is valuable,
or delete if it's truly temporary.

### Placeholder Content (Auto-Delete)

Skills containing these patterns are incomplete:
- `# Test Skill` (exact match)
- `NEW content with improvements!`

## Slop Locations

The scan checks these locations:

1. `.claude/skills/` - Root project skills
2. `packages/*/\.claude/skills/` - Package-level skills (with `-r`)

## CLAUDE.md Cleanup

The scan also checks CLAUDE.md for:

- **Stale references**: Skills listed but not installed
- **Duplicate references**: Same skill listed multiple times

Run `skills claudemd sync` to fix CLAUDE.md references.

## Workflow

### Daily Cleanup

After testing or development:

```bash
skills hygiene scan
skills hygiene clean --confirm
skills claudemd sync
```

### Pre-Commit Check

Add to your workflow:

```bash
# Check for slop before committing
skills hygiene scan
if [ $? -ne 0 ]; then
  echo "Slop detected! Run: skills hygiene clean --confirm"
  exit 1
fi
```

## Decision Tree

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

## Safety

- `--dry-run` shows what would happen without changes
- `--confirm` is required for actual deletion
- `_temp_*` skills are never auto-deleted (review required)
- Timestamped skills are flagged for review, not auto-deleted

## Related Commands

- `skills validate` - Check skill quality
- `skills claudemd sync` - Sync CLAUDE.md with installed skills
- `skills list` - Show installed skills

## Skill Chaining

Works with:
- **skill-maker**: Create clean skills to replace slop
- **claudeception**: Extract learnings before deleting temp skills
- **workflow-orchestrator**: Include hygiene in project workflow

## Terminal Chain (Always Run Last)

This skill runs after testing workflows complete:

| After Skill | Cleanup Needed |
|-------------|----------------|
| tdd | test-skill-* directories |
| suggest-tests | Analysis artifacts |
| unit-test-workflow | Generated test stubs |
| property-based-testing | Fast-check artifacts |
| doc-maintenance | Stale references |
| gitignore-hygiene | Final verification |

When any testing skill completes, run:
- `skills hygiene scan`
- `skills hygiene clean --confirm` (if slop detected)

### Testing Pipeline Position

repo-hygiene is the terminal step in the testing pipeline:

```
tdd → suggest-tests → unit-test-workflow → property-based-testing → repo-hygiene
                                                                         ↑
                                                                    (TERMINAL)
```

All testing workflows should end with repo-hygiene to ensure clean state.

### Feature Completion Flow

In feature completion contexts, repo-hygiene chains to doc-maintenance:

```
feature done → dogfood-skills → repo-hygiene → doc-maintenance
```

After cleanup, doc-maintenance updates PLAN.md to mark tasks complete.
