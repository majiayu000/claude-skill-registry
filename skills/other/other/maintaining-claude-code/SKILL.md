---
name: maintaining-claude-code
description: Create, validate, and improve Claude Code configuration — SKILL.md files, CLAUDE.md, rules, hooks, and settings.json. Use when creating a new skill, writing a SKILL.md, adding a hook, editing rules, auditing skill descriptions, checking config quality, debugging hook behavior, or deciding between skills vs rules vs CLAUDE.md. Also auto-loads when working in ~/.claude/ on skills, rules, hooks, or settings.
---

# Maintaining Claude Code

Validate, organize, and improve Claude Code configurations.

## Modes of Operation

### Audit Mode

**Use when**: Checking config quality, validating skills work

Checklist:

- CLAUDE.md: Specific, structured, actionable
- Skills: Valid YAML, good descriptions (What + When formula)
- Commands: Clear purpose, not duplicating skills
- Hooks: Proper exit codes, reasonable timeouts

### Organize Mode

**Use when**: .claude directory is messy, too many similar skills

Guidelines:

- Split CLAUDE.md into rules when >150 lines
- Consolidate similar skills (don't have 3 "code review" skills)
- Use subdirectories in rules/ for large projects

### Advise Mode

**Use when**: Deciding what entity type to create

Decision tree:

- Needs to run automatically before/after actions? -> **Hook**
- Claude should auto-detect and use? -> **Skill**
- Needs isolated context for heavy work? -> **Skill with `context: fork`**
- Always-on behavioral guidance? -> **CLAUDE.md**
- Path-specific rules? -> **.claude/rules/**

## Quick Reference

### Entity Type Decision Matrix

| Need                       | Best Entity            | Alternative            |
| -------------------------- | ---------------------- | ---------------------- |
| Global behavior guidelines | CLAUDE.md              | Rules if >150 lines    |
| Path-specific rules        | .claude/rules/         | CLAUDE.md if universal |
| Auto-detected capabilities | Skills                 | Rules if always-on     |
| Heavy isolated workflows   | Skills (context: fork) | Regular skill          |
| Pre/post action validation | Hooks                  | Nothing else does this |
| External API integration   | MCP Servers            | Bash calls if simple   |

### Skill Description Formula

`<What it does>. Use when <trigger1>, <trigger2>, or <trigger3>.`

Good: "Extract text and tables from PDF files. Use when working with PDFs, forms, or document extraction."

Bad: "Helps with documents"

### YAML Validation

- `---` on line 1 (required)
- `name:` max 64 chars
- `description:` max 1024 chars, must include triggers
- `---` before content

### Common Anti-Patterns

- Vague descriptions: "Helps with stuff"
- Nested references: SKILL.md -> REF.md -> DETAILS.md
- Overloaded skills: Does 5 unrelated things
- Missing triggers: No "Use when..." clause

## Validation Steps

1. Check YAML syntax in all skills
2. Verify descriptions include trigger phrases
3. Ensure no duplicate capabilities across skills
4. Confirm CLAUDE.md content won't quickly grow stale
5. Check hooks have reasonable timeouts

## Resources

See [REFERENCE.md](REFERENCE.md) for detailed examples and troubleshooting.
