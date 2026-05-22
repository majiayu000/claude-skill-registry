---
name: generating-commit-messages
description: MANDATORY skill for ALL commits. Must be used EVERY TIME before creating any git commit. No exceptions.
---

# Generating Commit Messages

## ⚠️ CRITICAL REQUIREMENT ⚠️

**THIS SKILL MUST BE USED FOR EVERY SINGLE COMMIT**

The CLAUDE.md file explicitly states: "Before committing changes, **ALWAYS** use the @.claude/skills/generating-commit-messages skill to generate commit messages"

## Mandatory Process

**BEFORE ANY `git commit` COMMAND:**

1. **ALWAYS** run `git diff --staged` first to see changes
2. **ALWAYS** analyze the staged changes thoroughly
3. **ALWAYS** generate a commit message following the format below
4. **NEVER** commit without following this process

## Required Commit Message Format

1. **Summary line** (under 50 characters)
   - Use present tense imperative mood
   - Be specific and descriptive

2. **Detailed description**
   - Explain WHAT was changed
   - Explain WHY it was changed
   - List affected components/files
   - Include any important context

## Best Practices

- Use clear, descriptive commit messages
- Use present tense ("Add feature" not "Added feature")
- Include the "why" not just the "what"
- Start summary with action verb (Add, Update, Fix, Remove, etc.)
- Be specific about what components/files are affected

## FORBIDDEN Elements

- **NEVER** include "Generated with [Claude Code](https://claude.ai/code)"
- **NEVER** include "Co-Authored-By: Claude <noreply@anthropic.com>"
- **NEVER** use generic messages like "Update files" or "Fix issues"

## Example Good Commit Message

```
Refactor authentication system for better security

- Replace deprecated JWT library with more secure alternative
- Add input validation for user credentials
- Update authentication middleware to handle edge cases
- Fix memory leak in session management

This change improves security posture and resolves crashes
reported in production when handling malformed requests.
```

## Reminder

**If you find yourself about to run `git commit` without having followed this skill, STOP immediately and use this skill first.**

## Version History

- v1.1.0 (2025-11-18): Enhanced with mandatory usage requirements and better formatting
- v1.0.0 (2025-11-14): Initial release
