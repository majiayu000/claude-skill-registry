---
name: scaffold-rules
description: Scaffold development rules for AI coding agents. Auto-invoked when user asks about setting up rules, coding conventions, or configuring their AI agent environment.
license: ISC
compatibility: Requires bun
allowed-tools: Bash, Glob, Read, Write, Edit, AskUserQuestion
---

# Scaffold Rules

Scaffold development rules for AI coding agent environments.

## Purpose

Use this skill when the user wants to:
- Set up development rules or coding conventions
- Configure their AI coding agent environment
- Add or update project guidelines

## Workflow

### Step 1: Get Processed Templates from CLI

```bash
bunx @plaited/development-skills scaffold-rules
```

Parse the JSON output. The `templates` object contains all available rules - use these when presenting options to the user.

### Step 2: Check for Existing Rules

If `.plaited/rules/` already exists with files:
- Warn the user that existing rules will be overwritten
- Ask for confirmation before proceeding
- If declined, abort

### Step 3: Ask User Preferences

Present available templates from the CLI output and ask which to scaffold. Build options dynamically from `templates` keys and descriptions.

### Step 4: Write Files

#### Rule Files
Write selected rules to `.plaited/rules/` using content from `templates[ruleId].content`.

#### AGENTS.md (Marker-Based Update)

AGENTS.md is the single source of truth for rules content:

1. Read existing file (or empty if missing)
2. Find markers: `<!-- PLAITED-RULES-START -->` and `<!-- PLAITED-RULES-END -->`
3. Update:
   - **Markers exist**: Replace content between markers (inclusive)
   - **No markers**: Append section to end of file
   - **No file**: Create with section content

Write `agentsMdSection` → AGENTS.md

#### CLAUDE.md (Reference Only)

CLAUDE.md only needs a reference to AGENTS.md:

1. Check if CLAUDE.md exists
2. If exists, scan file content for `@AGENTS.md` text
   - **Found**: Skip CLAUDE.md (already references AGENTS.md)
   - **Not found**: Append `claudeMdReference` to end of file
3. If no file exists: Done (AGENTS.md only is sufficient)

### Step 5: Output Summary

Report what was created/updated.

## CLI Options

```bash
# All rules to .plaited/rules/
bunx @plaited/development-skills scaffold-rules

# List available rules (useful for discovery)
bunx @plaited/development-skills scaffold-rules --list

# Filter specific rules
bunx @plaited/development-skills scaffold-rules --rules <id> --rules <id>

# Custom directory
bunx @plaited/development-skills scaffold-rules --rules-dir=custom/rules
```

**Note:** Invalid rule names in `--rules` will produce a warning with available rule IDs.

## Rules Directory Convention

| Directory | Purpose | Scope |
|-----------|---------|-------|
| `.plaited/rules/` | Shared rules from scaffold-rules | Cross-agent (Claude, Cursor, Copilot, etc.) |
| `.claude/rules/` | Claude Code-specific overrides | Claude Code only |
| `.cursor/rules/` | Cursor-specific overrides | Cursor only |

**How it works:**
- `.plaited/rules/` contains shared rules - referenced by both CLAUDE.md and AGENTS.md
- Agent-specific directories can override or extend shared rules for that agent only
- When scaffolding, always write to `.plaited/rules/` unless user specifies `--rules-dir`

## Related Skills

- **validate-skill** - Validate skill directories against AgentSkills spec
