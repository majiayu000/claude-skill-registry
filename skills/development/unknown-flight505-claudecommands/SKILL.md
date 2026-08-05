---
name: unknown
description: 'description: Create reusable command or Skill scaffolds tailored to
  your project''s recurring tasks.'
---

description: Create reusable command or Skill scaffolds tailored to your project's recurring tasks.
argument-hint: <description>
allowed-tools: Filesystem
---

# Create New Custom Skill

You are tasked with creating a new custom Skill for Claude based on the user's description. Follow the process below carefully to ensure the Skill is well-structured, follows best practices, and is ready for immediate use.

## User's Skill Description

$ARGUMENTS

## Your Task

Create a complete, production-ready custom Skill following the structure and best practices outlined below. Use chain of thought reasoning to ensure the Skill is well-designed.

<thinking>

Before creating the Skill, think through the following systematically:

1. **Understand the purpose**: What specific problem does this Skill solve? What workflows does it enable?

2. **Determine scope**: Is this Skill focused enough? Does it try to do one thing well, or is it too broad?

3. **Identify when to use it**: In what situations should Claude invoke this Skill? What keywords or contexts should trigger it?

4. **Plan the structure**:
   - What metadata is required (name, description, version, dependencies)?
   - Should this Skill include additional resource files?
   - Does it need executable scripts or code?
   - What examples would be helpful?

5. **Consider the user's workflow**: How will this Skill integrate with their existing processes?

6. **Think about completeness**: What information needs to be included to make this Skill immediately useful?

</thinking>

## Skill Structure Guidelines

### Required Components

1. **Metadata (YAML frontmatter)**:
   - `name`: Human-friendly name (64 chars max)
   - `description`: Clear description of what the Skill does and when to use it (200 chars max) - CRITICAL for Claude to know when to invoke this Skill
   - `version`: Optional version tracking (e.g., 1.0.0)
   - `dependencies`: Optional software packages required

2. **Markdown Body**:
   - Overview section explaining the Skill's purpose
   - Clear instructions for Claude
   - When to apply guidelines
   - Examples (when helpful)
   - Any specific workflows or processes

### Best Practices

- **Keep it focused**: Solve one specific, repeatable task well
- **Write clear descriptions**: Be specific about when the Skill applies
- **Include examples**: Show what success looks like when helpful
- **Use clear structure**: Organize with headers and sections
- **Be explicit**: Don't assume Claude knows your workflows or preferences

### Progressive Disclosure

The Skill system uses progressive disclosure:
1. **First level (metadata)**: Claude reads this to determine IF the Skill should be used
2. **Second level (markdown body)**: Claude accesses this WHEN executing the Skill
3. **Third level (resources)**: Additional files Claude can reference if needed

## Creation Process

1. **Analyze the description**: Understand what the user needs
2. **Design the Skill structure**: Plan metadata, sections, and content
3. **Create the directory**: Make a folder named after the Skill (lowercase with hyphens)
4. **Write SKILL.md**: Include frontmatter and well-organized markdown content
5. **Add resources if needed**: Create additional files only if the Skill is complex enough to warrant them
6. **Present the result**: Show the user the complete Skill structure

## Output Format

After your thinking, create the Skill with the following structure:

```
skill-name/
├── SKILL.md          (Required: main Skill file)
├── REFERENCE.md      (Optional: supplemental information)
├── EXAMPLES.md       (Optional: detailed examples)
└── resources/        (Optional: scripts, templates, etc.)
```

For most Skills, a single well-crafted SKILL.md file is sufficient.

## Example SKILL.md Template

```markdown
---
name: Skill Name
description: Brief description of what this Skill does and when to use it
version: 1.0.0
dependencies: package>=version (if needed)
---

## Overview

Explain the Skill's purpose and value. When should Claude use this Skill? What problem does it solve?

## Instructions

Provide clear, specific instructions for Claude to follow when executing this Skill. Be detailed but organized.

### Section 1
[Detailed guidance]

### Section 2
[More guidance]

## When to Apply

List specific situations where this Skill should be used:
- Condition 1
- Condition 2
- Condition 3

## Examples

### Example 1: [Scenario]
Input: [Example input]
Expected output: [What success looks like]

### Example 2: [Another scenario]
[Another example if helpful]

## Additional Guidelines

Any other important information, constraints, or best practices.
```

## Important Reminders

- The `description` field is CRITICAL - Claude uses it to determine when to invoke your Skill
- Keep Skills focused on one workflow rather than trying to do everything
- Start simple - you can always expand the Skill later
- Include examples when they would help Claude understand the expected output
- Use clear, unambiguous language
- Test with example prompts after creation

## Now Execute

Based on the user's description: "$ARGUMENTS"

1. Think through the Skill design using the structured thinking process above
2. Create the appropriate directory structure
3. Write a complete, production-ready SKILL.md file
4. Add any necessary resource files if the Skill requires them
5. Present the complete Skill to the user with:
   - The directory structure
   - The full SKILL.md content
   - Any additional files created
   - A brief explanation of how to install and use it

Create the Skill files in the current directory under a new folder with an appropriate name (lowercase with hyphens).

