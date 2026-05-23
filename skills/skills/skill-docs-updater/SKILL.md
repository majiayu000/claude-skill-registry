---
name: skill-docs-updater
description: Synchronize skill documentation. Use after creating or modifying any skill. Updates SKILLS-INDEX.md with the full skills table.
---

# Skill Docs Updater

Keeps the skills table in `SKILLS-INDEX.md` in sync.

## When to Use

- After creating a new skill with skill-writer
- After modifying an existing skill's name or description
- When skills are added, removed, or renamed

## Process

### Step 1: Scan Skills Directory

List all directories in `arsenal/dot-claude/skills/`:

```bash
ls arsenal/dot-claude/skills/
```

### Step 2: Read Each SKILL.md

For each skill directory, read the `SKILL.md` file and extract:
- `name` from YAML frontmatter
- `description` from YAML frontmatter

If no frontmatter exists, derive name from directory name and description from first paragraph.

### Step 3: Generate Skills Table

Create a markdown table with all skills:

```markdown
| Skill | When to Use |
|-------|-------------|
| `skill-name` | Short description of when to use |
```

### Step 4: Replace Content Between Markers

Look for these markers in `arsenal/dot-claude/skills/SKILLS-INDEX.md` and replace content between them:

```html
<!-- AUTO-GENERATED:SKILLS-TABLE:START -->
(replace this content)
<!-- AUTO-GENERATED:SKILLS-TABLE:END -->
```

### Step 5: Sync to .claude/

After updating the index, run:

```bash
./arsenal/install.sh
```

This copies the updated SKILLS-INDEX.md to `.claude/skills/`.

## Target File

`arsenal/dot-claude/skills/SKILLS-INDEX.md`

## Notes

- Preserve all content outside the markers
- Sort skills alphabetically by name
- Keep descriptions concise (one line)
- Always scan `arsenal/dot-claude/` (source of truth), not `.claude/` (generated copy)
- Run `./arsenal/install.sh` after to sync changes
