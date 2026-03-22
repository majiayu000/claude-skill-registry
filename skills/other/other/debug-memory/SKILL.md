---
name: debug-memory
description: Diagnose ClaudeMemory installation and configuration issues. Use when memory tools fail or setup seems broken.
user_invocable: true
---

# Debug Memory Setup

When invoked with `/debug-memory`, this skill runs comprehensive diagnostics on your ClaudeMemory installation.

## What This Checks

This skill will verify:
- ✅ Database existence (global and project)
- ✅ Schema version compatibility
- ✅ Hook configuration
- ✅ CLAUDE.md setup
- ✅ Published snapshot status
- ✅ MCP server connectivity
- ✅ Recent ingest activity

## Step 1: Run Setup Check

First, check the memory system status using the MCP tool:

```
memory.check_setup
```

This returns:
- **initialized**: true/false
- **version**: ClaudeMemory version
- **issues**: List of problems found
- **recommendation**: Actionable next steps

## Step 2: Analyze Results

Based on the check results:

### If initialized = true
✅ System is healthy! Show the user:
- Version information
- Database stats
- Last successful operations

### If initialized = false
⚠️ System needs setup. Check for:
- **Missing database**: Run `claude-memory init`
- **Missing CLAUDE.md**: Not importing memory snapshot
- **Missing hooks**: Hooks not configured in settings.json
- **Version mismatch**: Need to upgrade with `gem update claude-memory`

## Step 3: Provide Recommendations

Give the user clear next steps:

**For missing setup:**
```bash
# Initialize ClaudeMemory
claude-memory init

# Or use the setup skill
/setup-memory
```

**For configuration issues:**
```bash
# Check system health
claude-memory doctor

# View current status
claude-memory status
```

**For version issues:**
```bash
# Upgrade to latest version
gem update claude-memory
claude-memory init  # Re-run init after upgrade
```

## Step 4: Verify Fix

After user follows recommendations, run `memory.check_setup` again to confirm the issue is resolved.

## Common Issues

### "Database not found"
- **Cause**: ClaudeMemory not initialized
- **Fix**: Run `claude-memory init` or `/setup-memory`

### "Hooks not configured"
- **Cause**: `.claude/settings.json` missing hook definitions
- **Fix**: Run `claude-memory init` to add hooks

### "CLAUDE.md not importing snapshot"
- **Cause**: Missing `@.claude/rules/claude_memory.generated.md` import
- **Fix**: Add import to `.claude/CLAUDE.md`

### "Version mismatch"
- **Cause**: Old ClaudeMemory version installed
- **Fix**: Run `gem update claude-memory`

### "No recent ingest activity"
- **Cause**: Hooks not triggering or failing silently
- **Fix**: Check hook configuration with `claude-memory doctor`

## Example Output

```
Running ClaudeMemory diagnostics...

✅ Global database: healthy
   - Location: ~/.claude/memory.sqlite3
   - Schema: v7
   - Facts: 42

✅ Project database: healthy
   - Location: .claude/memory.sqlite3
   - Schema: v7
   - Facts: 127
   - Last ingest: 2026-01-29T21:47:41Z

✅ Hooks: configured
✅ Snapshot: published
✅ CLAUDE.md: importing snapshot

All systems operational! Memory is working correctly.
```

## When to Use This Skill

Use `/debug-memory` when:
- Memory tools are failing with errors
- Unsure if ClaudeMemory is properly installed
- Hooks don't seem to be running
- Facts aren't being captured
- After upgrading ClaudeMemory
- Setting up a new project

## Related Commands

- `/setup-memory` - Install or upgrade ClaudeMemory
- `claude-memory doctor` - CLI health check
- `claude-memory status` - View system status
- `memory.check_setup` - The underlying MCP tool
