---
name: skill-share
description: A skill that creates new Claude skills and automatically shares them
  on Slack using Rube for seamless team collaboration and skill discovery.
license: Complete terms in LICENSE.txt
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# Skill Share

## When to use this skill

Use this skill when you need to:

- **Create new Claude skills** with proper structure and metadata
- **Generate skill packages** ready for distribution
- **Automatically share created skills** on Slack channels for team visibility
- **Validate skill structure** before sharing
- **Package and distribute** skills to your team

Also use this skill when:

- **User says he wants to create/share his skill**

This skill is ideal for:

- Creating skills as part of team workflows
- Building internal tools that need skill creation + team notification
- Automating the skill development pipeline
- Collaborative skill creation with team notifications

## Key Features

### 1. Skill Creation

- Creates properly structured skill directories with SKILL.md
- Generates standardized scripts/, references/, and assets/ directories
- Auto-generates YAML frontmatter with required metadata
- Enforces naming conventions (hyphen-case)

### 2. Skill Validation

- Validates SKILL.md format and required fields
- Checks naming conventions
- Ensures metadata completeness before packaging

### 3. Skill Packaging

- Creates distributable zip files
- Includes all skill assets and documentation
- Runs validation automatically before packaging

## How It Works

1. **Initialization**: Provide skill name and description
2. **Creation**: Skill directory is created with proper structure
3. **Validation**: Skill metadata is validated for correctness
4. **Packaging**: Skill is packaged into a distributable format

## Example Usage

```text
When you ask Claude to create a skill called "pdf-analyzer":
1. Creates /skill-pdf-analyzer/ with SKILL.md template
2. Generates structured directories (scripts/, references/, assets/)
3. Validates the skill structure
4. Packages the skill as a zip file
```
