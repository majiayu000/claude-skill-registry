---
name: setup-memory
description: Automatically install, configure, or upgrade ClaudeMemory
---

# ClaudeMemory Setup & Upgrade

This skill automatically sets up or upgrades ClaudeMemory based on your current state.

## What This Skill Does

When invoked, it will:

1. **Check current installation status**
   - Detect installed gem version
   - Check database existence and health
   - Verify configuration files

2. **Determine required action**
   - Fresh install (no databases)
   - Upgrade (version mismatch)
   - Verification (already up to date)

3. **Execute setup/upgrade automatically**
   - Run `claude-memory doctor` for health check
   - Add version markers to `.claude/CLAUDE.md`
   - Run smoke tests
   - Report results

4. **Provide next steps**
   - Restart recommendations if needed
   - Usage guidance

## Instructions

**IMPORTANT**: This skill should take action, not just provide instructions.

### Step 1: Check Installation Status

```bash
gem list claude_memory
claude-memory --version
claude-memory doctor
```

Analyze the output to determine current state.

- If `gem list` shows no `claude_memory` entry, the gem is not installed.
  Guide the user: `gem install claude_memory`
- If running in plugin mode (`CLAUDE_PLUGIN_ROOT` is set), hooks and MCP
  are managed by the plugin — only databases and memory instructions need setup.

### Step 2: Determine Action Required

- **Not installed**: Databases don't exist
  - Action: Run `claude-memory init` (ask user for --global flag preference)
- **Installed but outdated**: Version marker missing or old
  - Action: Run upgrade steps (doctor, add version marker, verify)
- **Up to date**: All healthy
  - Action: Report status only

### Step 3: Execute Required Actions

**For Fresh Install:**
1. Ask user: "Install globally only or with project memory? [project/global]"
2. Run `claude-memory init` (with --global if selected)
3. Run `claude-memory doctor` to verify
4. Add version marker to `.claude/CLAUDE.md`
5. Report success

**For Upgrade:**
1. Run `claude-memory doctor` (auto-runs migrations)
2. Add/update version marker in `.claude/CLAUDE.md`
3. Run `claude-memory stats` for smoke test
4. Report upgrade complete

**For Verification:**
1. Run `claude-memory doctor`
2. Confirm version in `.claude/CLAUDE.md`
3. Report all healthy

### Step 4: Report Results

Provide a clear summary:
- ✅ What was done
- 📊 Current status (facts, schema version, etc.)
- 🔄 Next steps (if any)

## After Setup/Upgrade

Always remind the user:

1. **Restart Claude Code** if configuration files were modified
2. **Test memory tools**: Try `memory.status` or `memory.recall "<topic>"`
3. **Use memory-first workflow**: Check memory before reading files

## What Gets Created

### Databases
- `~/.claude/memory.sqlite3` - Global knowledge (preferences, conventions)
- `.claude/memory.sqlite3` - Project-specific facts and decisions

### Configuration Files
- `.claude/CLAUDE.md` - Workflow instructions for memory-first usage
- `.claude/settings.json` - Hooks for automatic ingestion
- `.claude.json` - MCP server configuration
- `.claude/rules/claude_memory.generated.md` - Published snapshot

### Hooks
ClaudeMemory automatically ingests transcripts on these events:
- SessionStart - Catch up on previous session
- Stop - After each response
- SessionEnd - Final ingestion before closing
- PreCompact - Before context summarization

## Common Scenarios

### Fresh Install
User has never installed ClaudeMemory:
1. Ask installation preference (project vs global)
2. Run `claude-memory init` with appropriate flags
3. Verify with `doctor`
4. Add version marker
5. Report success and next steps

### Upgrade After Gem Update
User updated gem but not configuration:
1. Run `claude-memory doctor` (auto-migrates schema)
2. Update version marker in `.claude/CLAUDE.md`
3. Verify with smoke tests
4. Report upgrade complete

### Verification
User wants to check current status:
1. Run `claude-memory doctor`
2. Run `claude-memory stats`
3. Check version marker in `.claude/CLAUDE.md`
4. Report all findings

## Troubleshooting Guide

If automatic setup fails, provide these solutions:

**Permission Denied**
```bash
chmod +x $(which claude-memory)
```

**Database Locked**
- Close other Claude sessions
- Run `claude-memory recover`

**Missing Ruby**
ClaudeMemory requires Ruby 3.2.0+. Check with:
```bash
ruby --version
```

**Hooks Not Working**
Re-run setup:
```bash
claude-memory init
```

## Memory-First Workflow

After successful setup, always remind users:

1. **Query memory first**: `memory.recall "<topic>"`
2. **Use semantic shortcuts**: `memory.decisions`, `memory.conventions`, `memory.architecture`
3. **Check before exploring**: Memory saves time vs reading files
4. **Combine knowledge**: Merge recalled facts with code exploration

This workflow leverages distilled knowledge from previous sessions.
