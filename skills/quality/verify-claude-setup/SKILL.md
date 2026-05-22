---
name: verify-claude-setup
description: Verify .claude directory configuration is complete and correct. Use when checking if agents, hooks, rules, and memory are properly set up, or after making changes to .claude configuration.
allowed-tools: [Read, Bash, Grep, Glob]
---

# Verify .claude Setup

Quick verification that .claude directory is properly configured.

## When to Use

- After updating agents, rules, hooks, or memory
- Before starting complex work (ensure system is ready)
- User asks "is everything set up correctly?"
- Troubleshooting configuration issues

## Verification Checklist

### 1. Agents (should have 6)
```bash
ls .claude/agents/ | wc -l
```

Verify all agents have:
- Proper YAML frontmatter
- Research-First Protocol section
- Clear responsibilities

### 2. Hooks (should have 11 scripts + README)
```bash
ls .claude/hooks/scripts/*.ts | wc -l
```

Check:
- All scripts executable (`chmod +x`)
- All have Bun shebang (`#!/usr/bin/env bun`)
- settings.json has all hooks configured
- Pre-tool and Post-tool hooks exist

### 3. Rules (should have research-first-protocol.md)
```bash
ls .claude/rules/*.md
```

Verify:
- research-first-protocol.md exists
- Has `alwaysApply: true`

### 4. Memory (should have 8 files)
```bash
ls .claude/memory/ | wc -l
```

Check CLAUDE.md imports all:
- research-first-enforcement.md
- coding-standards.md
- testing-standards.md
- architecture-patterns.md
- common-workflows.md
- build-commands.md
- asset-forge-guide.md
- security-protocols.md

### 5. Settings
```bash
grep -c "hooks" .claude/settings.json
```

Verify:
- SessionStart, UserPromptSubmit hooks
- PreToolUse (Bash, Write, Edit) hooks
- PostToolUse (Write, Edit, Read, Grep, Glob) hooks
- PreCompact, Stop, SubagentStop, SessionEnd hooks

### 6. Commands (should have ~20)
```bash
find .claude/commands -type f -name "*.md" | wc -l
```

## Quick Verification

Run all checks:
```bash
echo "Agents: $(ls .claude/agents/ | wc -l)"
echo "Hooks: $(ls .claude/hooks/scripts/*.ts | wc -l)"
echo "Rules: $(ls .claude/rules/*.md | wc -l)"
echo "Memory: $(ls .claude/memory/ | wc -l)"
echo "Commands: $(find .claude/commands -type f -name "*.md" | wc -l)"
echo "Skills: $(ls .claude/skills/ | wc -l)"
```

## Expected Counts

- Agents: 6
- Hook Scripts: 11
- Rules: 2 (README + research-first-protocol)
- Memory: 8
- Commands: ~20
- Skills: ~40

## Report Format

Provide summary:
```
✅ Agents: 6/6 with Research-First Protocol
✅ Hooks: 11/11 executable, all configured
✅ Rules: research-first-protocol.md active
✅ Memory: 8/8 files, all imported in CLAUDE.md
✅ Commands: 20 organized slash commands
✅ Skills: 40 skills ready

Status: .claude configuration VERIFIED
```

Or if issues found:
```
⚠️ Agents: Missing Research-First Protocol in database-specialist.md
⚠️ Hooks: pre-tool-write.ts not executable
❌ Memory: research-first-enforcement.md not imported in CLAUDE.md

Status: Configuration INCOMPLETE - needs fixes
```
