---
name: hello-world
description: A simple introductory skill that demonstrates basic OpenCode skill functionality and provides a starting template
license: MIT
metadata:
  category: tutorial
  audience: beginners
  complexity: basic
---

## What I do
- Provide a basic welcome message
- Demonstrate skill loading and execution
- Show how to structure skill instructions
- Offer guidance for creating more complex skills

## When to use me
Use this skill when learning about OpenCode skills or testing skill functionality.
This is a beginner-friendly skill for understanding the skill system.

## Instructions

### 1. Welcome Message
When activated, provide a friendly greeting that confirms the skill is working.

### 2. Basic Functionality Demo
Show how skills can provide structured guidance and step-by-step instructions.

### 3. Learning Resources
Point to additional resources for skill development:
- Read the AGENTS.md file for development guidelines
- Check OpenCode documentation at https://opencode.ai/docs/skills/
- Explore other skills in the repository for examples

### 4. Next Steps
Suggest creating a more specialized skill based on your needs:
- Code review skills
- Project setup automation
- Testing and quality assurance
- Documentation generation

## Example Usage
```
skill({ name: "hello-world" })
```

This will load the skill and provide these instructions to help you get started with OpenCode skills development.

## Skill Development Tips
- Keep instructions clear and actionable
- Use markdown formatting for better readability
- Include specific examples when possible
- Test your skills by restarting OpenCode and using the skill tool
- Reference supporting files with relative paths when needed

## Supporting Files (Optional)
You can add supporting files to this directory:
- `scripts/setup.sh` - Automation scripts
- `templates/config.md` - Reusable templates
- `docs/advanced.md` - Additional documentation</content>
<parameter name="filePath">hello-world/SKILL.md