---
description: "Create a skill with automatic quality validation. Uses Manager Pattern: Task creates → Forked Skill audits → Retry if needed. Arguments: skill_name, description, skills_to_load (optional)."
argument-hint: "<skill-name> <description> [--skills <skills>]"
---

# Skill Factory Command

This command orchestrates the Manager Pattern for skill creation:

## Workflow

```
!`echo "Creating skill: $1"`
@.claude/skills/create-skill-files/SKILL.md
@.claude/skills/skill-auditor/SKILL.md
```

## Arguments

| Arg | Required | Description |
|:---:|:--------:|:------------|
| `$1` | Yes | Skill name (kebab-case) |
| `$2` | Yes | Description (What-When-Not format) |
| `$3` | No | Skills to load (comma-separated) |

## Usage

```bash
# Create skill
/factory:skill "image-processor" "Process images..."

# With skills
/factory:skill "data-worker" "Handle data tasks..." "file-utils,data-transform"
```

## What Happens

1. **Create**: `Task(create-skill-files)` → writes draft to `.claude/workspace/draft.md`
2. **Audit**: skill-auditor skill (forked) validates the draft
3. **Retry**: If fail, Task creates again with fix guidance
4. **Done**: Skill created, all gates passed
