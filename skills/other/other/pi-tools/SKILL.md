---
name: pi-tools
description: View and manage Pi-built extensions synced to Dex. Shows available tools, commands, and sync status.
---

# Pi Tools

View and manage Pi-built extensions that have been synced to Dex.

## Arguments

- `$ACTION`: What to do (optional, defaults to `list`)
  - `list` - Show all synced Pi extensions and their tools
  - `sync` - Force re-sync of Pi extensions
  - `status` - Show sync status and registry info
  - `show [extension]` - Show details for a specific extension

---

## Workflow

### Step 1: Check Registry

Read the Pi extensions registry at `.claude/pi-extensions-registry.json`.

```bash
if [ -f ".claude/pi-extensions-registry.json" ]; then
  echo "Registry found"
else
  echo "No Pi extensions synced yet"
fi
```

### Step 2: Execute Action

#### If `$ACTION == list` or no action specified:

Display all synced extensions:

```markdown
## Pi Extensions

| Extension | Tools | Commands | Last Modified |
|-----------|-------|----------|---------------|
| [name]    | [count] | [count] | [date]      |

### Tools Available

**[extension-name]:**
- `tool_name` - Description
- `tool_name_2` - Description

**[extension-name-2]:**
- ...
```

#### If `$ACTION == sync`:

1. Run the sync hook manually:
   ```bash
   node .claude/hooks/pi-extensions-sync.cjs
   ```

2. Report what changed:
   - New extensions added
   - Extensions updated
   - Extensions removed

#### If `$ACTION == status`:

Display sync metadata:
- Last sync timestamp
- Number of extensions
- Registry file location
- Generated skills location

#### If `$ACTION == show [extension]`:

Read the generated skill file:
```bash
cat ".claude/skills/pi-generated/pi-[extension]/SKILL.md"
```

Display full details:
- Description
- All tools with parameters
- All commands
- Source file location

---

## Output Format

### List View

```
## Pi Extensions Synced to Dex

**Last sync:** 2026-02-03T12:00:00Z

### dex-mcp-bridge

*Bridges Pi to Dex's MCP servers for task and calendar management*

**Tools:**
- `dex_task` - Manage tasks (create, complete, list, suggest)
- `dex_calendar` - Access calendar events (today, upcoming, list)

**Commands:**
- `/dex-tasks` - List current tasks
- `/dex-today` - Show today's events

---

Run `/pi-tools sync` to refresh from .pi/extensions/
```

### Status View

```
## Pi Extensions Status

**Registry:** .claude/pi-extensions-registry.json
**Skills:** .claude/skills/pi-generated/
**Source:** .pi/extensions/

**Stats:**
- Extensions: 1
- Total tools: 2
- Total commands: 2

**Last sync:** 2026-02-03T12:00:00Z

**Sync triggers:**
- SessionStart hook (automatic)
- `/pi-tools sync` (manual)
```

---

## Integration Notes

### How Sync Works

1. **SessionStart hook** runs `pi-extensions-sync.cjs`
2. Scans `.pi/extensions/*.ts` for TypeScript files
3. Parses each file to extract:
   - JSDoc descriptions
   - `pi.registerTool()` calls
   - `pi.registerCommand()` calls
4. Generates skill stubs in `.claude/skills/pi-generated/`
5. Updates registry with metadata
6. Outputs summary to session context

### Skill Naming

Pi extension skills are prefixed with `pi:` to distinguish from native Dex skills:
- `pi:dex-mcp-bridge` - MCP bridge extension
- `pi:custom-tool` - Custom extension

Generated skill folders use `pi-` prefix:
- `.claude/skills/pi-generated/pi-dex-mcp-bridge/SKILL.md`

### When to Use Pi vs Dex

**Use Pi tools when:**
- Working in the Pi environment
- Need direct tool execution
- Building new extensions

**Use Dex context when:**
- Planning work that involves Pi capabilities
- Documenting what tools are available
- Cross-referencing with Dex knowledge

---

## Edge Cases

- **No .pi/extensions/ directory**: Silent - Pi not configured
- **Empty extensions directory**: Report "No Pi extensions found"
- **Parse errors**: Skip malformed files, report warnings
- **Deleted extensions**: Clean up orphaned skill stubs
