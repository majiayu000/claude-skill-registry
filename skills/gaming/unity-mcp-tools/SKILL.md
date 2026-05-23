---
name: unity-mcp-tools
description: This skill should be used when the user asks about "MCP tools", "Unity MCP", "enable tool groups", "which MCP tools", "create GameObject", "add component", "run Unity tests", "check scene hierarchy", "spawn agent for Unity", "MCP not working", or needs to coordinate Unity Editor operations via MCP.
version: 0.2.0
---

# Unity MCP Tools

Expert knowledge for coordinating Unity MCP operations, including tool enablement, agent orchestration, and direct MCP tool usage.

## Quick Start: MCP Workflow

### 1. Inspect First (Always Available)

The MCP Resource is always enabled - no tool enablement needed:

- Command: `/unity-mcp-scene-info {path}`
- Returns: components, properties, children, transform data
- Example: `/unity-mcp-scene-info GameplayScene/TileManager`

### 2. Enable Tools When Modification Needed

Run `/unity-mcp-enable [groups]` before spawning agents that need MCP.

### 3. Spawn Agent with Skills

Include `unity-mcp-tools` skill for agents doing MCP work:

| Task                      | Enable Groups         | Spawn Agent           |
| ------------------------- | --------------------- | --------------------- |
| Create/modify GameObjects | gameobject, component | scene-builder         |
| Add UI elements           | gameobject, component | ui-ux-developer       |
| Run tests                 | testing               | test-engineer         |
| Work with scripts         | script                | code-architect        |
| Create prefabs            | prefab, gameobject    | scene-builder         |
| Deploy build              | (none)                | deployment-specialist |

### 4. Cleanup After MCP Work

Run `/unity-mcp-reset` to disable tools and save context.

## When to Consult mcp-advisor

Spawn the mcp-advisor advisory agent when:

- Unsure which tool groups are needed
- MCP tools returning errors
- Complex multi-step Unity operations
- Need troubleshooting help

Example prompt: "What MCP tool groups do I need to add a health bar UI?"

The mcp-advisor returns recommendations - it does not execute commands.

## Agent Skill Assignments

When spawning agents, include these skills:

| Agent                 | Skills to Include                                  |
| --------------------- | -------------------------------------------------- |
| scene-builder         | unity-mcp-tools, layout-sizing, visual-style-guide |
| test-engineer         | unity-mcp-tools, unity-testing                     |
| ui-ux-developer       | layout-sizing, visual-style-guide                  |
| input-developer       | board-sdk, unity-mcp-tools                         |
| code-architect        | project-architecture                               |
| game-designer         | zero-day-rules                                     |
| deployment-specialist | (none - uses Bash)                                 |
| project-producer      | documentation                                      |
| mcp-advisor           | unity-mcp-tools                                    |

## Subagent MCP Access

Subagents can use MCP tools directly when:

1. Tools are enabled in `AI-Game-Developer-Config.json`
2. Agent inherits tools (omit `tools:` field in frontmatter)

To give MCP access, omit the tools field:

```yaml
---
name: scene-builder
skills: unity-mcp-tools, layout-sizing
# No tools field = inherits ALL including MCP
---
```

## Tool Groups Reference

Use `/unity-mcp-enable [group]` to enable. Multiple: `/unity-mcp-enable gameobject component`

### Core Groups (11 total)

| Group       | Tools                                                                                                                                                                                        | Use Case                |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| scene-read  | scene-get-data, scene-list-opened, console-get-logs                                                                                                                                          | Inspect scene hierarchy |
| scene-write | scene-create, scene-save, scene-open, scene-set-active, scene-unload, console-get-logs                                                                                                       | Modify scenes           |
| gameobject  | gameobject-create, gameobject-find, gameobject-modify, gameobject-destroy, gameobject-duplicate, gameobject-set-parent, scene-save, console-get-logs                                         | GameObject operations   |
| component   | gameobject-component-add, gameobject-component-get, gameobject-component-modify, gameobject-component-destroy, component-list, scene-save, console-get-logs                                  | Component operations    |
| script      | script-read, script-update-or-create, script-delete, script-execute, assets-refresh, editor-application-get-state, console-get-logs                                                          | Script operations       |
| prefab      | assets-prefab-create, assets-prefab-instantiate, assets-prefab-open, assets-prefab-save, assets-prefab-close, assets-refresh, editor-application-get-state, console-get-logs                 | Prefab operations       |
| assets      | assets-find, assets-create-folder, assets-copy, assets-move, assets-delete, assets-get-data, assets-modify, assets-refresh, assets-material-create, assets-shader-list-all, console-get-logs | Asset management        |
| testing     | tests-run, editor-application-get-state, console-get-logs                                                                                                                                    | Run Unity tests         |
| editor      | editor-application-get-state, editor-application-set-state, console-get-logs, editor-selection-get, editor-selection-set                                                                     | Full editor control     |
| packages    | package-list, package-add, package-remove, package-search, console-get-logs                                                                                                                  | Package management      |
| reflection  | reflection-method-find, reflection-method-call, console-get-logs                                                                                                                             | Advanced operations     |

### Cross-cutting Utilities (Auto-included)

| Tool                         | Auto-included with      |
| ---------------------------- | ----------------------- |
| console-get-logs             | ALL groups              |
| editor-application-get-state | script, testing, prefab |
| assets-refresh               | script, prefab          |
| scene-save                   | gameobject, component   |

## Common Patterns

### Create GameObject with Components

1. Enable: `/unity-mcp-enable gameobject component`
2. Use `gameobject-create` to create object
3. Use `gameobject-component-add` to add components
4. Use `gameobject-component-modify` to configure

### Run Tests After Code Changes

1. Enable: `/unity-mcp-enable testing`
2. Use `tests-run` with testMode: "EditMode" or "PlayMode"
3. Check results, fix failures

### Inspect Before Modifying

Always use MCP Resource first (no enablement):

- `/unity-mcp-scene-info {path}` to understand structure
- Then enable tools only if modification needed

## Configuration

Config file: `Assets/Resources/AI-Game-Developer-Config.json`

Structure:

```json
{
  "tools": [{ "name": "tool-name", "enabled": true/false }],
  "resources": [{ "name": "GameObject from Current Scene by Path", "enabled": true }]
}
```

The MCP Resource is always enabled. Tools default to disabled.

## Commands Reference

| Command                        | Purpose                  |
| ------------------------------ | ------------------------ |
| `/unity-mcp-status`            | Show enabled groups      |
| `/unity-mcp-enable [groups]`   | Enable tool groups       |
| `/unity-mcp-enable-all`        | Enable all tools         |
| `/unity-mcp-reset`             | Disable all tools        |
| `/unity-mcp-scene-info [path]` | Query scene via Resource |

## Additional Resources

### Reference Files

For complete tool documentation:

- **`references/tool-reference.md`** - All 50 tools with parameters and examples
- **`references/tool-groups.md`** - Tool group definitions with JSON arrays for each group
- **`references/troubleshooting.md`** - Common issues and solutions

### Related Documentation

- **Documentation/Unity-MCP-Documentation.md** - Full MCP setup guide
- **.mcp.json** - Connection configuration
