---
name: create-skill-files
description: "Worker skill that creates skill files from parameters. Use ONLY within Task() invoked by skill-manager. Not for direct invocation."
agent: general-purpose
---

# Create Skill Files

This skill creates a skill directory and SKILL.md file from parameters.

## Input Expected

```markdown
skill_name: {name}
description: {description}
skills_to_load: (optional) {skill-1, skill-2}
fix_guidance: (optional) {what to fix from previous attempt}
```

## What to Create

### Directory Structure

```
.claude/skills/{skill_name}/
└── SKILL.md
```

### SKILL.md Template

```markdown
---
name: {skill_name}
description: "{description}"
context: fork    # If this skill orchestrates others
agent: general-purpose
skills:          # If context: fork
  - {skills_to_load}
---

# {skill_name}

## Quick Start

{1-2 sentences on when to use}

## Navigation

| If you need... | Read this section... |
| :------------- | :------------------- |
| Topic A | ## PATTERN: A |
| Topic B | ## PATTERN: B |

## PATTERN: Main Content

{content}

---

<critical_constraint>
{non-negotiable rules}
</critical_constraint>
```

## If fix_guidance Provided

Address the specific issues mentioned:
- Read the guidance
- Fix ONLY the issues
- Keep other parts as-is

## If First Attempt (no fix_guidance)

Create a complete skill with:
1. Frontmatter (name + description)
2. Quick Start section
3. Navigation table
4. Main content sections
5. critical_constraint footer

## Output

Return the created file paths and a summary of what was created.
