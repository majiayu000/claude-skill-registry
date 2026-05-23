---
name: documentation-updates
description: Update documentation based on lessons learned. Use after completing work to capture learnings and prevent future issues.
---

# Documentation Updates

Update documentation based on lessons learned from the conversation.

## When to Use This Skill

Use this skill when:
- You made a mistake or misunderstanding that could have been prevented
- You discovered something that should be documented for future reference
- The user asks you to "reflect" on what happened
- After completing work where documentation gaps were discovered

## Process

Momentarily pause any other actions to review the conversation and
reflect on any mistakes or misunderstandings. Update any/all of the
following as appropriate:

### Files to Update

1. **Project-level documentation**:
   - `AGENTS.md` in the current project
   - `CLAUDE.md` in the current project
   - Any project-specific documentation

2. **Global documentation**:
   - Global `AGENTS.md` (`~/.claude/AGENTS.md` or similar)
   - Global `CLAUDE.md`

3. **Agent settings**:
   - Per-project settings (`.claude/settings.json`, `opencode.json`)
   - Global settings (`~/.config/opencode/opencode.json`, `~/.claude/settings.json`)

4. **Other project documentation**:
   - README.md
   - Design documents
   - Architecture guides

### What to Document

- Common pitfalls encountered and how to avoid them
- Important constraints or requirements discovered
- Useful patterns or approaches found effective
- Mistakes made and what should have been done differently
- Configuration or setup nuances

## Important Rule

Do NOT resume ANY previous actions until the user is satisfied that the
docs have been appropriately updated.

## Output

After updating documentation:
- List the files that were modified
- Summarize the changes made
- Confirm with the user that the updates are adequate
