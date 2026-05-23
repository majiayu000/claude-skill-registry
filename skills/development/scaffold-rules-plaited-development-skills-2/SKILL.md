---
name: scaffold-rules
description: Scaffold development rules for AI coding agents. Auto-invoked when user asks about setting up rules, coding conventions, or configuring their AI agent environment.
license: ISC
compatibility: Requires bun
allowed-tools: Bash
---

# Scaffold Rules

Scaffold shared development rules for AI coding agent environments.

## When to Use

Use when the user wants to:
- Set up development rules or coding conventions
- Configure their AI coding agent environment
- Add project guidelines for Claude, Cursor, or other agents

## Workflow

### Step 1: Preview Changes (Optional)

```bash
bunx @plaited/development-skills scaffold-rules --dry-run
```

Review the `actions` array to see what will be created.

### Step 2: Run Scaffold

```bash
bunx @plaited/development-skills scaffold-rules
```

This will:
1. Write rules into `AGENTS.md` (creates if missing, updates between markers if present)
2. Add `@AGENTS.md` reference to `CLAUDE.md` if it exists without one

### Step 3: Report to User

Tell the user what was created based on the `actions` output.

## CLI Options

| Flag | Description |
|------|-------------|
| `--list`, `-l` | List available rules without scaffolding |
| `--dry-run`, `-n` | Preview actions without making changes |

## How It Works

Rules are written directly into `AGENTS.md` between markers:

```
<!-- PLAITED-RULES-START -->

## Rules

(rule content inlined here)

<!-- PLAITED-RULES-END -->
```

- **No AGENTS.md**: Creates one with rules section
- **AGENTS.md without markers**: Appends rules section with markers
- **AGENTS.md with markers**: Replaces content between markers (preserves user content outside)
- **CLAUDE.md exists**: Adds `@AGENTS.md` reference if not already present

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Rules duplicated in AGENTS.md | Markers were manually deleted | Remove duplicate section, re-run `scaffold-rules` |
| Update didn't apply | Only one marker present (start or end) | Ensure both `<!-- PLAITED-RULES-START -->` and `<!-- PLAITED-RULES-END -->` exist, or delete both to get a fresh append |
| `@AGENTS.md` not added to CLAUDE.md | CLAUDE.md doesn't exist | Create CLAUDE.md first, then re-run |

**Do not** manually edit content between the `PLAITED-RULES-START` and `PLAITED-RULES-END` markers — it will be overwritten on next run.

## Related Skills

- **validate-skill** - Validate skill directories against AgentSkills spec
