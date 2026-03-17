---
name: archive-skill
model: fast
description: Move a deprecated skill to archive
usage: /archive-skill <name> [category]
---

# /archive-skill

Move a deprecated or obsolete skill to the archive.

## Usage

```
/archive-skill <name> [category]
```

**Arguments:**
- `name` — Skill folder name
- `category` — Category folder (optional if unique)

## Examples

```
/archive-skill old-pattern backend
/archive-skill deprecated-design design-systems
/archive-skill superseded-hooks realtime
```

## When to Use

- Skill is obsolete (replaced by newer pattern)
- Skill is too project-specific (shouldn't have been promoted)
- Skill duplicates another skill
- Skill quality is too low to maintain
- Pattern is no longer recommended

## What It Does

1. **Locates** the skill in `ai/skills/[category]/[name]/`
2. **Verifies** skill exists
3. **Checks** for references in other skills/agents/commands
4. **Creates** `ai/archive/` directory if needed
5. **Moves** skill to `ai/archive/[category]-[name]/`
6. **Adds** archive timestamp and reason to SKILL.md
7. **Reports** any broken references to fix

## Archive Metadata

Adds to archived SKILL.md:

```markdown
---
archived: 2024-01-15
reason: Superseded by [new-skill-name]
---
```

## Reference Check

Before archiving, checks for references in:

- Other skills (Related sections)
- Agents (workflow references)
- Commands (Related sections)
- Meta-skills (component skill references)

If references found:
- Lists files with references
- Suggests updates needed
- Proceeds with archival (references become broken links)

## Output Locations

- Archived skill → `ai/archive/[category]-[name]/`
- Removed from → `ai/skills/[category]/[name]/`

## Related

- **Check first:** `/check-overlaps` (find redundant skills)
- **Update instead:** `/update-skill` (if skill can be improved)