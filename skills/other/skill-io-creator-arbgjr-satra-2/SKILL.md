---
name: skill-io-creator
description: Create skills using the agentskills.io framework with init, validate, and package scripts. Use when users want to create distributable .skill packages, use the init_skill.py scaffolding, or follow the agentskills.io workflow with scripts, references, and assets directories.
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
---

# Skill IO Creator (agentskills.io Framework)

This skill provides the agentskills.io framework for creating distributable skill packages with initialization scripts, validation, and packaging tools.

> **Note:** This is the agentskills.io framework, separate from the official Claude Code skills format. Use `skill-creator` for official Claude Code skills.

## When to Use This vs skill-creator

| Use Case | Use This (skill-io-creator) | Use skill-creator |
|----------|----------------------------|-------------------|
| Distributable .skill packages | Yes | No |
| Script-based scaffolding | Yes | No |
| Official Claude Code format | No | Yes |
| Frontmatter with hooks/context | No | Yes |

## Framework Overview

The agentskills.io framework provides:

1. **init_skill.py** - Scaffold new skill directories with templates
2. **quick_validate.py** - Validate skill structure and content
3. **package_skill.py** - Package skills into distributable .skill files

## Skill Structure

```
skill-name/
├── SKILL.md                 # Required: frontmatter + instructions
├── scripts/                 # Executable code
│   └── helper.py
├── references/              # Documentation loaded into context
│   └── api_reference.md
└── assets/                  # Files used in output (templates, images)
    └── template.pptx
```

## Creating a New Skill

### Step 1: Initialize

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

Example:
```bash
python scripts/init_skill.py pdf-editor --path ~/.claude/skills
```

This creates:
- `SKILL.md` with TODO placeholders
- `scripts/example.py` - sample executable
- `references/api_reference.md` - sample documentation
- `assets/example_asset.txt` - sample asset placeholder

### Step 2: Edit SKILL.md

Complete the frontmatter:

```yaml
---
name: skill-name
description: What it does and WHEN to use it. Include trigger scenarios.
---
```

Choose a structure pattern:

| Pattern | Best For | Example |
|---------|----------|---------|
| Workflow-Based | Sequential processes | PDF: Analyze -> Map -> Fill -> Verify |
| Task-Based | Tool collections | PDF: Merge, Split, Extract |
| Reference/Guidelines | Standards | Brand: Colors, Typography |
| Capabilities-Based | Integrated features | PM: numbered capabilities |

### Step 3: Add Resources

**scripts/** - Executable code
- Python scripts, shell scripts
- Must be tested before packaging
- Can be executed without loading into context

**references/** - Documentation
- API docs, schemas, policies
- Loaded into context when needed
- Keep SKILL.md lean by moving details here

**assets/** - Output files
- Templates, images, fonts
- NOT loaded into context
- Copied/used in final output

### Step 4: Validate

```bash
python scripts/quick_validate.py <path/to/skill-folder>
```

Checks:
- YAML frontmatter format
- Required fields (name, description)
- Directory structure
- Naming conventions

### Step 5: Package

```bash
python scripts/package_skill.py <path/to/skill-folder> [output-dir]
```

Creates `skill-name.skill` file (zip with .skill extension).

## Core Principles

### 1. Concise is Key

Context window is shared. Only add what Claude doesn't already know.

### 2. Progressive Disclosure

1. **Metadata** (always loaded) - name + description
2. **SKILL.md body** (on trigger) - instructions
3. **Resources** (on demand) - scripts, references, assets

Keep SKILL.md under 500 lines.

### 3. Degrees of Freedom

| Level | When | Example |
|-------|------|---------|
| High | Multiple valid approaches | Text guidelines |
| Medium | Preferred pattern | Pseudocode with params |
| Low | Fragile operations | Specific scripts |

## What NOT to Include

- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- User documentation
- Setup procedures

## Design Patterns

### Workflow Patterns

For sequential processes, provide overview:

```markdown
1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
```

For conditional workflows:

```markdown
1. Determine type:
   **Creating?** → Follow Creation workflow
   **Editing?** → Follow Editing workflow
```

See [references/workflows.md](references/workflows.md) for more patterns.

### Output Patterns

For strict output format:

```markdown
ALWAYS use this exact template:

# [Title]
## Executive summary
## Key findings
## Recommendations
```

For flexible output:

```markdown
Here is a sensible default, adapt as needed:
...
```

See [references/output-patterns.md](references/output-patterns.md) for more patterns.

## Example: Creating a PDF Editor Skill

```bash
# 1. Initialize
python scripts/init_skill.py pdf-editor --path ~/.claude/skills

# 2. Edit SKILL.md
# - Update description with trigger scenarios
# - Add workflow steps
# - Reference scripts

# 3. Add scripts
# - scripts/rotate_pdf.py
# - scripts/extract_text.py

# 4. Add references
# - references/pdf_api.md

# 5. Validate
python scripts/quick_validate.py ~/.claude/skills/pdf-editor

# 6. Package
python scripts/package_skill.py ~/.claude/skills/pdf-editor ./dist
```

## Script Usage Reference

### init_skill.py

```
Usage: init_skill.py <skill-name> --path <path>

Skill name requirements:
  - Hyphen-case (e.g., 'data-analyzer')
  - Lowercase letters, digits, hyphens only
  - Max 40 characters
```

### quick_validate.py

```
Usage: quick_validate.py <path/to/skill-folder>

Validates:
  - Frontmatter syntax
  - Required fields
  - Directory structure
```

### package_skill.py

```
Usage: package_skill.py <path/to/skill-folder> [output-directory]

Creates .skill file (zip format) for distribution.
```
