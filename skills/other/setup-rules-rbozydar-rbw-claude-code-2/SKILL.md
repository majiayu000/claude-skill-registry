---
name: setup-rules
description: Set up Claude Code rules in a project by symlinking from the rbw-claude-code templates. Use this skill when users want to add Python coding standards, anti-slop rules, or other shared rules to their projects.
---

# Setup Rules

This skill helps you set up Claude Code rules in your project by creating symlinks to shared rule templates. This allows you to maintain consistent coding standards across multiple projects.

## Available Rule Sets

### Python Rules

Comprehensive Python coding standards extracted from best practices:

| Rule | Description |
|------|-------------|
| `asyncio.md` | Structured concurrency, TaskGroup, fault isolation |
| `typing.md` | Modern type hints, Protocols, TypeVar |
| `architecture.md` | SOLID principles, dependency injection |
| `testing.md` | TDD, pytest patterns, fixtures |
| `prohibited.md` | Banned practices checklist |

### General Rules

| Rule | Description |
|------|-------------|
| `anti-slop.md` | Prevent AI-generated code slop |

## Quick Setup

### Option 1: Link All Python Rules

```bash
# Create .claude/rules directory in your project
mkdir -p .claude/rules

# Get the path to rbw-claude-code (adjust as needed)
RBW_CLAUDE_CODE="${HOME}/.claude/plugins/marketplaces/rbw-claude-code"

# Symlink all Python rules
for rule in asyncio typing architecture testing prohibited; do
  ln -sf "${RBW_CLAUDE_CODE}/templates/rules/python/${rule}.md" .claude/rules/
done

# Optionally add anti-slop
ln -sf "${RBW_CLAUDE_CODE}/templates/rules/anti-slop.md" .claude/rules/
```

### Option 2: Link Specific Rules

```bash
mkdir -p .claude/rules

RBW_CLAUDE_CODE="${HOME}/.claude/plugins/marketplaces/rbw-claude-code"

# Just asyncio and typing
ln -sf "${RBW_CLAUDE_CODE}/templates/rules/python/asyncio.md" .claude/rules/
ln -sf "${RBW_CLAUDE_CODE}/templates/rules/python/typing.md" .claude/rules/
```

### Option 3: Use the Setup Script

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/setup-rules/scripts/setup-rules.sh
```

The script will interactively guide you through selecting which rules to install.

## Manual Installation (Copy Instead of Symlink)

If you prefer to customize rules per-project:

```bash
mkdir -p .claude/rules

RBW_CLAUDE_CODE="${HOME}/.claude/plugins/marketplaces/rbw-claude-code"

# Copy rules (can be modified)
cp "${RBW_CLAUDE_CODE}/templates/rules/python/"*.md .claude/rules/
cp "${RBW_CLAUDE_CODE}/templates/rules/anti-slop.md" .claude/rules/
```

## Verify Installation

Check your rules are properly linked:

```bash
ls -la .claude/rules/
```

You should see symlinks pointing to the template files, or copied files if you chose that option.

## Project Structure After Setup

```
your-project/
├── .claude/
│   └── rules/
│       ├── asyncio.md -> /path/to/templates/rules/python/asyncio.md
│       ├── typing.md -> /path/to/templates/rules/python/typing.md
│       ├── architecture.md -> ...
│       ├── testing.md -> ...
│       ├── prohibited.md -> ...
│       └── anti-slop.md -> /path/to/templates/rules/anti-slop.md
├── src/
└── ...
```

## Updating Rules

When rules are updated in rbw-claude-code:

- **Symlinked rules**: Automatically get updates when you pull the latest rbw-claude-code
- **Copied rules**: Need to be manually updated or re-copied

## Removing Rules

```bash
# Remove specific rule
rm .claude/rules/asyncio.md

# Remove all rules
rm -rf .claude/rules/
```

## Troubleshooting

### Symlink shows as broken

The target path may have changed. Re-run the setup:

```bash
rm .claude/rules/*.md
# Re-run setup commands
```

### Rules not being applied

1. Check the rules directory exists: `ls .claude/rules/`
2. Verify file permissions: `ls -la .claude/rules/`
3. Ensure symlinks point to valid targets: `file .claude/rules/*`

### Want to override a specific rule

Copy just that rule instead of symlinking:

```bash
# Remove symlink
rm .claude/rules/asyncio.md

# Copy and customize
cp "${RBW_CLAUDE_CODE}/templates/rules/python/asyncio.md" .claude/rules/
# Edit .claude/rules/asyncio.md as needed
```
