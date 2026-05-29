---
description: Load a skill's full content into context
argument-hint: <skill-name-or-path>
---

# Load Skill

Load the complete content of a skill by name or path.

## Usage

```
/goodvibes:load-skill <skill-name-or-path>
```

## Instructions

1. If $ARGUMENTS looks like a path (contains `/`), use it directly
2. Otherwise, search for the skill using `search_skills`
3. Use `get_skill_content` to load the full SKILL.md content
4. Display the skill content to the user

If multiple skills match, show a list and ask the user to specify.

## Arguments

$ARGUMENTS
