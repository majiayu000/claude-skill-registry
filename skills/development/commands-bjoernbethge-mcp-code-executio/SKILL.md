---
name: commands-bjoernbethge-mcp-code-executio
description: Create a new reusable skill pattern for future tasks.
---

# /create-skill

Create a new reusable skill pattern for future tasks.

This command will:
- Prompt for skill name and description
- Collect the implementation code
- Create Python and/or TypeScript versions
- Add to skills registry
- Generate documentation

**Usage:**
```
/create-skill [skill-name] [--python] [--typescript]
```

**Examples:**
- `/create-skill extract-emails` - Create Python + TypeScript versions
- `/create-skill parse-json --python` - Python-only skill
- `/create-skill transform-csv --typescript` - TypeScript-only skill

**Skill Template:**
```python
def my_skill(input_data):
    """
    Skill description.

    Args:
        input_data: Description

    Returns:
        Processed result
    """
    # Implementation
    return result
```

**See Also:**
- `/list-skills` - Browse existing skills
