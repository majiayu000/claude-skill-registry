---
name: make-skill
description: Create a new Claude Code skill with proper structure, YAML frontmatter, and documentation. Use when user asks to "create a skill", "make a skill", "build a new skill", or "add a skill".
---

# Make Skill

## Overview

This skill helps you create new Claude Code skills following best practices and proper structure. It generates the skill directory, SKILL.md file with correct YAML frontmatter, and any supporting files needed.

## When to Use

Invoke this skill when the user:
- Says "create a skill" or "make a skill"
- Asks to "build a new skill" or "add a skill"
- Wants to create a new automated workflow or capability
- Mentions creating something that could be a skill

## Skill Creation Process

### 1. Gather Requirements

Ask the user for key information:
- **Skill name**: lowercase-with-hyphens (max 64 characters)
- **Purpose**: What does the skill do?
- **Trigger phrases**: What would a user say to invoke it?
- **Tools needed**: Which Claude Code tools will it use?
- **Workflow**: What are the step-by-step instructions?

### 2. Determine Skill Location

Skills can be:
- **Project skills**: `.claude/skills/skill-name/` (shared with team via git)
- **Personal skills**: `~/.claude/skills/skill-name/` (local to user)

For miso project work, default to project skills unless user specifies otherwise.

### 3. Create Directory Structure

Create the skill directory:
```bash
mkdir -p .claude/skills/skill-name/
```

Or for personal skills:
```bash
mkdir -p ~/.claude/skills/skill-name/
```

### 4. Gather Relevant Documentation

Before writing the skill, identify and read relevant documentation that provides context:
- Project documentation (README, CLAUDE.md, etc.)
- Related feature specifications
- Platform guides or technical references
- API documentation
- Process guides

Include this context directly in the SKILL.md so future invocations don't require re-explaining.

### 5. Generate SKILL.md

Create `SKILL.md` with:

**Required YAML Frontmatter**:
```yaml
---
name: skill-name
description: Brief description of what this skill does and when to use it (max 1024 chars)
---
```

**Optional YAML Fields**:
```yaml
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]  # Restrict tools if needed
```

**Content Sections**:
1. **Overview**: What the skill does
2. **When to Use**: Specific triggers and user phrases
3. **Instructions**: Step-by-step workflow
4. **Prerequisites**: Requirements or setup needed
5. **Expected Behavior**: What should happen
6. **Troubleshooting**: Common issues (if applicable)
7. **Notes**: Additional context

### 6. Create Supporting Files (Optional)

Add any helper files the skill might need:
- Documentation files (`.md`)
- Scripts (`.sh`, `.py`, etc.)
- Templates
- Configuration files

### 7. Test the Skill

After creating:
1. Verify the YAML frontmatter is valid
2. Check that the description is clear and specific
3. Test invocation with sample user phrases
4. Ensure the workflow is complete and actionable

## SKILL.md Template

```markdown
---
name: skill-name
description: Brief description including what it does and trigger phrases
---

# Skill Name

## Overview

[What this skill does in 1-2 sentences]

## When to Use

Invoke this skill when the user:
- [Trigger phrase 1]
- [Trigger phrase 2]
- [Trigger phrase 3]

## Prerequisites

- [Requirement 1]
- [Requirement 2]

## Instructions

### 1. [Step Name]

[Detailed instructions for this step]

```bash
# Example commands
```

### 2. [Next Step]

[More instructions]

## Expected Behavior

- [What should happen]
- [Observable outcomes]

## Troubleshooting

If [problem]:
- [Solution 1]
- [Solution 2]

## Notes

- [Important context]
- [Limitations]
- [Related skills or tools]
```

## Best Practices

1. **Focused Purpose**: One skill = one capability
2. **Specific Description**: Include both functionality and trigger terms
3. **Clear Instructions**: Step-by-step, actionable guidance
4. **Tool Restrictions**: Use `allowed-tools` to limit scope if needed
5. **Examples**: Show concrete command examples
6. **Embed Context**: Include relevant documentation directly in the skill so users don't have to repeatedly explain the same information
7. **Self-Contained**: The skill should have everything needed to execute autonomously

## Naming Conventions

- Use lowercase letters, numbers, and hyphens only
- Be descriptive but concise: `deploy-ios` not `ios-deployment-tool-v2`
- Avoid generic names: `analyze-logs` not `helper`
- Max 64 characters

## Description Writing Tips

Good descriptions:
- "Deploy iOS app to connected device via USB. Use when user asks to 'deploy to iPhone', 'install on device', or 'push to iOS'."
- "Generate API documentation from TypeScript types. Invoke when user mentions 'generate docs', 'create API docs', or 'document endpoints'."

Poor descriptions:
- "Helps with deployment" (too vague)
- "iOS tool" (not descriptive enough)
- Missing trigger phrases

## Example: Creating a Git Commit Skill

1. User says: "create a skill to make standardized git commits"
2. Gather: Name = "git-commit-standard", needs Bash tool, workflow is format check → commit → push
3. Create: `.claude/skills/git-commit-standard/SKILL.md`
4. Write frontmatter with description including "standardized commit", "make commit", "commit changes"
5. Document the commit message format in instructions
6. Add examples of good vs bad commit messages
7. Test by saying "make a standardized commit"

## Integration with Other Skills

Consider how the new skill interacts with existing ones:
- Does it complement another skill?
- Should it be invoked as part of a larger workflow?
- Can it use outputs from other skills?

Note these relationships in the skill documentation.
