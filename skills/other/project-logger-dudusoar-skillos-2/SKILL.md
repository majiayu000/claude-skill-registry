---
name: project-logger
description: Manages project progress tracking and maintains a chronological log of completed tasks, decisions, and updates. Use when completing milestones, making architectural decisions, or documenting project evolution. Creates and updates LOG.md file based on CLAUDE.md context.
---

# Project Logger

## Overview

This skill maintains a structured project log (LOG.md) that tracks progress, completed tasks, decisions, and important updates. It reads CLAUDE.md to understand project context and creates timestamped entries documenting the project's evolution.

## When to Use This Skill

Use this skill when:
- Completing a significant task or milestone
- Making important architectural or technical decisions
- Encountering and resolving issues
- Adding new features or capabilities
- Updating project dependencies or configuration
- Need to review project history

## Workflow

### Step 1: Locate CLAUDE.md

Find and read the project's CLAUDE.md file to understand:
- Project name and goals
- Current phase and milestones
- Technical architecture
- Known issues

Default location: `./.claude/CLAUDE.md`

### Step 2: Determine Log Entry Type

Identify what type of entry to create:

**Task Completion:**
- Feature implemented
- Bug fixed
- Refactoring completed
- Tests added

**Decision:**
- Architectural choice made
- Technology/library selected
- Design pattern adopted
- Convention established

**Update:**
- Dependency upgraded
- Configuration changed
- Documentation updated
- Milestone reached

**Issue:**
- Problem encountered
- Workaround applied
- Known limitation documented

### Step 3: Create or Update LOG.md

Check if LOG.md exists in `.claude/` directory:

**If LOG.md doesn't exist:**
- Create it using the template in `references/log_template.md`
- Add project header with name from CLAUDE.md
- Create first entry

**If LOG.md exists:**
- Read existing content
- Add new entry at the top (reverse chronological order)
- Preserve existing entries

### Step 4: Format Log Entry

Each entry should include:

```markdown
## YYYY-MM-DD HH:MM

### [TYPE] Title

**Context:** Brief explanation of why this happened

**What Changed:**
- Specific change 1
- Specific change 2
- Specific change 3

**Impact:**
- How this affects the project
- Any breaking changes
- Follow-up actions needed

**Related:**
- Links to commits, PRs, or issues (if applicable)
- References to relevant files or documentation
```

**Entry Types:**
- `[FEAT]` - New feature
- `[FIX]` - Bug fix
- `[DECISION]` - Architectural/technical decision
- `[REFACTOR]` - Code refactoring
- `[DOCS]` - Documentation update
- `[DEPS]` - Dependency update
- `[CONFIG]` - Configuration change
- `[MILESTONE]` - Milestone reached
- `[ISSUE]` - Problem or limitation

### Step 5: Add Entry Example

**Good entry:**
```markdown
## 2025-12-30 15:30

### [FEAT] Added skill-analyzer meta-skill

**Context:** Need automated skill selection when starting projects. Manual skill
discovery is time-consuming and error-prone.

**What Changed:**
- Created skill-analyzer meta-skill in `.claude/skills/`
- Implemented workflow to scan SkillOS library
- Added skill matching heuristics based on project context
- Updates CLAUDE.md sections 5 (Available Skills) and 6 (Missing Skills)

**Impact:**
- Automates skill selection for new projects
- Identifies gaps requiring project-specific skills
- Completes the project setup workflow (works with project-context-generator)

**Related:**
- Commit: b27c2ea
- Files: `.claude/skills/skill-analyzer/SKILL.md`
```

**Avoid vague entries:**
```markdown
## 2025-12-30

Updated some files.
```

### Step 6: Update Maintenance Notes in CLAUDE.md

After logging, optionally update the "Maintenance Notes" section in CLAUDE.md:
- Update "Last Updated" date
- Add entry to "Recent Changes"
- Update "Known Issues" if relevant

## Log Organization

### Reverse Chronological Order

Most recent entries appear first:
```markdown
# Project Log: SkillOS

## 2025-12-30 16:00
[Most recent]

## 2025-12-30 14:00

## 2025-12-29 10:00
[Oldest at bottom]
```

### Grouping by Date

For multiple entries on the same day, use subheadings:
```markdown
## 2025-12-30

### 16:00 - [FEAT] Added feature X
...

### 14:00 - [FIX] Fixed bug Y
...
```

## Best Practices

### Be Specific

- Include file paths, function names, or specific components
- Mention exact version numbers for dependencies
- Reference commits, PRs, or issues

### Explain "Why"

- Document the rationale behind decisions
- Explain trade-offs considered
- Note what alternatives were rejected

### Track Impact

- Note what breaks (breaking changes)
- Identify follow-up work needed
- Update known issues

### Regular Updates

- Log after completing significant work
- Don't batch too many changes into one entry
- Update while details are fresh

## Example LOG.md Structure

See `references/log_template.md` for the complete template and examples.

## Resources

### references/log_template.md

Template for creating LOG.md files with:
- Header structure
- Entry format examples
- Best practices
- Sample entries for different types
