---
name: new-skill
description: Scaffold a new skill with correct directory structure, frontmatter, naming, plugin symlink, and validation
---

# New Skill Scaffolder

Create a new skill in the kungfu repository with the correct structure and
conventions.

## Usage

When the user asks to create a new skill, follow these steps in order.

### Step 1: Gather Info

Ask the user for:

- **Skill name** (kebab-case, e.g. `my-new-skill`)
- **Description** (single line, no newlines, max 1024 chars)
- **Subdirectories needed** (`references/`, `scripts/`, `examples/`,
  `templates/`, `assets/` -- all optional)

### Step 2: Create Directory and SKILL.md

```bash
mkdir -p skills/<skill-name>
```

Write `skills/<skill-name>/SKILL.md` with this template:

```markdown
---
name: <skill-name>
description: <single-line description>
license: MIT
---

# <Skill Title>

<Brief overview of what the skill does and when to use it.>
```

### Step 3: Create Requested Subdirectories

If the user wants `references/`, `scripts/`, etc., create them with a
`.gitkeep`:

```bash
mkdir -p skills/<skill-name>/references
touch skills/<skill-name>/references/.gitkeep
```

### Step 4: Add Plugin Symlink

Create a symlink in the business plugin so the skill is discoverable:

```bash
ln -s ../../../skills/<skill-name> plugins/business/skills/<skill-name>
```

### Step 5: Validate

Run validation to confirm everything is correct:

```bash
just validate
```

Fix any issues reported before continuing.

### Step 6: Update README Table

```bash
just readme-table --write
```

## Conventions

- **Name**: Must be kebab-case, must match the directory name exactly
- **Description**: Single line, no `\n` or `\r`, no YAML block scalars (`|`,
  `>`)
- **Orphan rule**: Every file in subdirectories must be referenced from SKILL.md
  via markdown link or backtick
- **Word count**: Keep under 1500 words
- **Sources**: Use `[Title](url)` markdown link format
