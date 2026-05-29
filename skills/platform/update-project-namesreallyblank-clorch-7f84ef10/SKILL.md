---
description: Update project to latest Clorch standards (agents, hooks, settings)
---

# Update Project

Bring an existing project's Clorch configuration up to date with the latest standards.

## Process

### Step 1: Detect What Needs Updating

Run these checks in parallel:

```bash
# Check for project agents
ls -la .claude/agents/ 2>/dev/null | head -20

# Check for project hooks
ls -la .claude/hooks/ 2>/dev/null | head -10

# Check for project settings
cat .claude/settings.json 2>/dev/null | head -20

# Check global Clorch version
cat ~/.claude/VERSION 2>/dev/null || echo "No global VERSION"
```

### Step 2: Report Findings

Present what was found:

```
Project Clorch Status:

| Component | Status | Action |
|-----------|--------|--------|
| Project agents (.claude/agents/) | {count} found | Will update |
| Project hooks (.claude/hooks/) | {count} found | Will sync |
| Project settings | {exists/missing} | Will check |

Proceed with update?
```

### Step 3: Update Components

#### 3a. Update Project Agents (if exist)

Spawn the `agent-updater` agent:

```python
Task(
    subagent_type="agent-updater",
    prompt="""Update all agents in .claude/agents/ to latest Clorch standards.

Add these sections if missing:
- OUTPUT LIMITS (50-100 lines max)
- Ecosystem awareness (what tools/patterns the project uses)
- Iron laws (no mocks, no stubs, production code only)

Preserve all project-specific context.
Report: which agents updated, what was added.""",
    run_in_background=False
)
```

#### 3b. Sync Global Skills (optional)

If user wants to sync new skills from global:

```bash
# List new skills in global that aren't in project
comm -23 <(ls ~/.claude/skills/ | sort) <(ls .claude/skills/ 2>/dev/null | sort) | head -20
```

#### 3c. Check Settings Compatibility

Verify project settings work with latest Clorch:

```bash
# Check for deprecated settings
cat .claude/settings.json 2>/dev/null | grep -E "deprecated|old_format" || echo "No deprecated settings"
```

### Step 4: Report Results

```
Update Complete!

| Component | Result |
|-----------|--------|
| Agents | {N} updated, {M} unchanged |
| Hooks | {synced/skipped} |
| Settings | {compatible/updated} |

Note: Restart Claude Code to apply agent changes.
```

## Parameters

- `/update-project` - Full update (agents + hooks + settings)
- `/update-project agents` - Only update project agents
- `/update-project --dry-run` - Show what would be updated without changing

## What Gets Updated

### Agent Updates
- **Output limits** - Ensures agents don't flood context
- **Ecosystem awareness** - Project tech stack context
- **Iron laws** - No mocks, no stubs, production code only
- **MCP integration** - context7, perplexity references

### Hook Updates
- Sync any new hook patterns from global
- Preserve project-specific hooks

### Settings Updates
- Check for deprecated configuration
- Add new recommended settings

## Safety

- All changes are additive (won't remove existing content)
- Project-specific context is preserved
- Creates backup before modifying: `.claude/agents/*.md.bak`

## Post-Update

After running this skill:

1. **Restart Claude Code** - Required for agent changes to take effect
2. **Test agents** - Run a quick task to verify agents work
3. **Check hooks** - Verify hooks fire correctly

## Example

```
User: /update-project

Claude: Checking project Clorch status...

Found:
- 5 project agents in .claude/agents/
- 2 project hooks in .claude/hooks/
- settings.json present

Proceeding with update...

[Spawns agent-updater]

Update complete!
- 3 agents updated (added output limits)
- 2 agents unchanged (already current)
- Hooks: compatible
- Settings: compatible

Restart Claude Code to apply changes.
```
