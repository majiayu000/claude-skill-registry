# Skill Creator

A meta-skill that helps you create new skills for your portfolio website project.

## Trigger Phrases

This skill activates when the user wants to create a new skill:
- "create a new skill"
- "make a skill"
- "generate a skill"
- "help me create a skill"
- "add a new skill"

## Instructions

When this skill is invoked, follow these steps to help the user create a new skill:

### Step 1: Gather Skill Information

Use the AskUserQuestion tool to gather the following information:

1. **Skill Name**: Ask "What should we name this skill?"
   - Explain that the name should be lowercase with hyphens (e.g., "project-creator", "responsive-nav")

2. **Skill Purpose**: Ask "What will this skill do?"
   - Get a clear description of what the skill accomplishes
   - Examples: "Create a new project card", "Generate a responsive navigation", "Add a contact form section"

3. **Trigger Phrases**: Ask "What phrases should trigger this skill?"
   - Request 3-5 trigger phrases that should activate the skill
   - Examples: "create project card", "add project", "new project"

### Step 2: Generate the SKILL.md File

Once you have all the information, create the skill directory and SKILL.md file:

1. Create directory: `.claude/skills/{skill-name}/`
2. Create file: `.claude/skills/{skill-name}/SKILL.md`

### Step 3: SKILL.md Template

Use this template structure for the generated SKILL.md:

```markdown
# {Skill Name}

{Brief description of what this skill does}

## Trigger Phrases

This skill activates when the user wants to {action}:
- "{trigger phrase 1}"
- "{trigger phrase 2}"
- "{trigger phrase 3}"
- "{trigger phrase 4}"
- "{trigger phrase 5}"

## Instructions

When this skill is invoked, follow these steps:

### Step 1: {First Major Step}

{Detailed instructions for this step}

1. {Substep 1}
2. {Substep 2}
3. {Substep 3}

### Step 2: {Second Major Step}

{Detailed instructions for this step}

### Step 3: {Third Major Step}

{Detailed instructions for this step}

## File Structure

If this skill creates files, specify the structure:

```
{directory}/
├── {file1}
├── {file2}
└── {file3}
```

## Code Templates

If applicable, include code templates or patterns:

```html
<!-- Example HTML structure -->
```

```css
/* Example CSS styles */
```

```javascript
// Example JavaScript code
```

## Best Practices

- {Best practice 1}
- {Best practice 2}
- {Best practice 3}

## Notes

- {Important note 1}
- {Important note 2}
```

### Step 4: Customize the Template

Based on the user's responses:

1. **Replace placeholders** with the actual skill information
2. **Add specific instructions** relevant to the skill's purpose
3. **Include code templates** if the skill involves generating code
4. **Add file structure** if the skill creates multiple files
5. **Include best practices** specific to this skill's domain

### Step 5: Create the Skill

1. Use the Bash tool to create the skill directory
2. Use the Write tool to create the SKILL.md file with the generated content
3. Confirm the skill has been created successfully

### Step 6: Provide Usage Instructions

After creating the skill, tell the user:

1. How to activate the skill (the trigger phrases)
2. Where the skill file is located
3. How to edit or customize it further if needed

## Example Interaction

**User**: "Create a new skill"

**Assistant**:
1. Asks: "What should we name this skill?"
2. Asks: "What will this skill do?"
3. Asks: "What phrases should trigger this skill?"
4. Creates the directory structure
5. Generates the SKILL.md file
6. Confirms creation and explains how to use it

## Tips for Creating Good Skills

- **Be specific**: Skills should have a clear, focused purpose
- **Use clear triggers**: Choose trigger phrases that are natural and intuitive
- **Provide context**: Include enough detail in instructions for consistent execution
- **Include examples**: Show code templates, file structures, and patterns
- **Think step-by-step**: Break down complex tasks into manageable steps
- **Reference the design system**: For portfolio-related skills, reference colors, spacing, and component patterns from CLAUDE.md

## Integration with Portfolio Project

When creating skills for this portfolio website:

- Reference the design system in CLAUDE.md
- Use the established color palette (blue primary, purple secondary)
- Follow the 8px spacing scale
- Maintain the minimal, modern aesthetic
- Ensure dark mode compatibility
- Use vanilla JavaScript (no frameworks)
- Follow accessibility best practices

## Notes

- Skills are stored in `.claude/skills/{skill-name}/SKILL.md`
- Each skill should be self-contained and focused on one task
- Skills can reference other skills if needed
- Keep instructions clear and actionable
- Test the skill after creation to ensure it works as expected
