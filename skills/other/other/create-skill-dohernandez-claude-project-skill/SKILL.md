---
name: create-skill
description: Scaffold a new skill directory using the multi-YAML pattern. Use when user says /create-skill.
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
hooks:
  Stop:
    - type: command
      command: "task claude:validate-skill -- --skill create-skill"
---

# Create Skill

## Purpose
Create a new `.claude/skills/{folder-name}/` skill scaffold that follows the multi-YAML pattern.
This skill produces the canonical file set for a new skill in the ci-core-e2e-runner project.

## Quick Reference
- Creates: SKILL.md, skill.yaml, collaboration.yaml, sharp-edges.yaml
- Requires: folder name, kind, description
- No task runner or hooks -- this is a shell/YAML project

## Procedure

1. **Gather inputs** from the user:
   - `folder_name` -- directory name under `.claude/skills/`
   - `title` -- human title for H1 header in SKILL.md
   - `description` -- one-line description for trigger matching (frontmatter)
   - `purpose` -- 2-3 sentences for the SKILL.md purpose section
   - `kind` -- one of: action, workflow, gate, helper, meta
   - `user_invocable` -- true or false
   - `allowed_tools` -- list of tools the skill needs

2. **Create folder**: `mkdir -p .claude/skills/{folder-name}/`

3. **Write SKILL.md** (thin wrapper):
   - Frontmatter: name, description, user-invocable, allowed-tools
   - Purpose section (2-3 sentences)
   - Quick Reference (creates/requires pointers)
   - Automation section pointing to skill.yaml / sharp-edges.yaml / collaboration.yaml

4. **Write skill.yaml**:
   - Canonical patterns, anti-patterns, ownership, procedure
   - All rule details live here, not in SKILL.md

5. **Write collaboration.yaml**:
   - Dependencies, composition sequences, triggers

6. **Write sharp-edges.yaml**:
   - Common gotchas with detection hints, impact, and fixes

7. **Document in CLAUDE.md**:
   - Add the skill to the skills table in CLAUDE.md
   - Format: appropriate section with skill name and description

## File Layout

```
.claude/skills/{folder-name}/
  SKILL.md              # Thin wrapper with frontmatter + pointers
  skill.yaml            # Canonical patterns, procedure, ownership
  collaboration.yaml    # Dependencies, triggers, composition
  sharp-edges.yaml      # Common failure modes and fixes
```

## Automation
See `skill.yaml` for the full procedure and patterns.
See `sharp-edges.yaml` for common failure modes.
