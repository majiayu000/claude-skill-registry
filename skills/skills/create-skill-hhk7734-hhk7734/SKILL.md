---
name: create-skill
description: Create a new agent skill following the Agent Skills specification. Use this when the user asks to create a new skill or update an existing one to match the standard.
---

# Create Skill

## When to use this skill

Use this skill when the user wants to create a new agent skill or explicitly asks to "create a skill". This skill provides the standard procedure and specification for creating high-quality, compliant agent skills.

## Prerequisite: Understand the Goal

1.  **Identify the Skill Name**:
    - must be 1-64 characters.
    - only lowercase alphanumeric (a-z, 0-9) and hyphens (-).
    - cannot start or end with a hyphen.
    - cannot have consecutive hyphens (`--`).
2.  **Identify the Purpose**: Understand what task the skill is solving to write a good description.

## Step 1: Create Directory Structure

Create a new directory with the exact name of the skill.

```
<skill-name>/
  ├── SKILL.md  (Required)
  ├── scripts/  (Optional: executable code)
  ├── references/ (Optional: docs, forms)
  └── assets/   (Optional: templates, images)
```

## Step 2: Create SKILL.md

The `SKILL.md` file is the core of the skill. It MUST strictly follow this format:

### Frontmatter

The file must start with a YAML frontmatter block:

```yaml
---
name: <skill-name>
description: <text description of what the skill does and when to use it>
# Optional fields:
# license: <license type>
# compatibility: <system requirements>
# metadata:
#   author: <name>
#   version: "1.0"
---
```

**Critical Rules:**

- `name` in frontmatter MUST match the directory name.
- `description` should include keywords to help agents find the skill (1-1024 chars).

### Body

The body should be standard Markdown containing:

- **Header**: `# Title of Capability`
- **When to use**: A section explaining the specific scenarios where this skill is applicable.
- **Instructions**: Step-by-step procedures the agent should follow.
  - Be prescriptive and clear.
  - Reference scripts or assets using relative paths (e.g., `scripts/my-script.py`).

## Step 3: Populate Optional Directories (If needed)

- **scripts/**: For code that needs to be executed (e.g., Python scripts). Ensure they are self-contained.
- **references/**: For static knowledge, cheat sheets, or lookup tables.
- **assets/**: For templates the agent should copy or use.

## Validation

After creating the files, ensure:

1.  The directory name and `name` field match exactly.
2.  The YAML frontmatter is valid.
3.  The description clearly explains _when_ to use the skill.
