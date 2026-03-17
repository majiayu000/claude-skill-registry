---
name: skill-creator
description: Scaffold new skills with standard directory structure
version: 1.1.0
tags: [meta, scaffolding]
owner: orchestration
status: active
---

# Skill Creator Skill

## Overview

Create a new skill directory and template with required sections.

## Usage

```
/new-skill <skill-name>
```

## Identity
**Role**: Skill Architect
**Objective**: Create the file structure and template for a *new* skill.

## Workflow
**Command**: `/new-skill <skill-name>`

### 1. Structure
Create directory: `.claude/skills/<skill-name>/`

### 2. Template
Create file `.claude/skills/<skill-name>/SKILL.md` with:
```markdown
---
name: <skill-name>
description: <short-description>
version: 1.0.0
tags: [tag1, tag2]
---

# <Skill Title> Skill

## Identity
**Role**: <Role Name>
**Objective**: <What does this skill do?>

## Workflow
1. Step 1...

## Constraints
- ...
```

### 3. Register
**Action**: Determine the next free `SKILL-ID` in `AGENTS.md`.
**Update**: Append the new skill to the registry table.

## Best Practices
- **Naming**: Kebab-case (`my-new-skill`).
- **Granularity**: One skill = one coherent set of abilities.

## Outputs

- New skill directory with `SKILL.md` template and registry entry update.

## Related Skills

- `/skills` - Discover available skills
