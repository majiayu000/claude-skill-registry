---
name: configure-integration
description: Set up a new MCP server, tool integration, or workspace extension.
---

# Configure Integration

The Workspace Configurator drives this workflow with Planner support for discovering tool capabilities. When a new tool becomes available in the workspace, scaffold the appropriate prompts and configuration to integrate it with the agentic system.

**Prerequisites:** The integration is available (MCP server running, CLI installed, etc.), `workspace.config.yaml` exists.

---

## Phase 1: Discover

Understand what the new integration provides.

### Steps

1. Identify the integration type (MCP server, CLI tool, VS Code extension, API)
2. Discover available operations/tools:
   - For MCP servers: list available tool names and descriptions
   - For CLI tools: check help/version output
   - For extensions: check contributed commands
3. Classify operations by category (repo, board, CI, deployment, etc.)

### Output

```markdown
## Context Anchors

- **Integration:** <name and type>
- **Workspace:** <name>

## Discovered Capabilities

| Tool        | Category   | Description   |
| ----------- | ---------- | ------------- |
| <tool name> | <category> | <description> |

## Next Step

Confirm discovered capabilities.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human confirms discovered capabilities.

---

## Phase 2: Map to Kernel Operations

Determine how the integration maps to kernel abstract operations.

### Mapping Categories

| Kernel Operation    | Integration Provides? |
| ------------------- | --------------------- |
| Create issue        | Yes / No              |
| Update board status | Yes / No              |
| Create PR           | Yes / No              |
| Read file contents  | Yes / No              |
| Search code         | Yes / No              |
| Manage releases     | Yes / No              |
| CI operations       | Yes / No              |

### Steps

1. Map discovered tools to kernel operation categories
2. Identify which existing forge operations this integration can replace or supplement
3. Note any new capabilities not covered by current kernel operations

---

## Phase 3: Scaffold

Generate integration-specific workspace artifacts.

### Steps

1. Update `workspace.config.yaml` with integration settings (under `forge.tooling`)
2. Generate prompts for mapped operations
3. Update or create forge-ops agent with new tool awareness
4. If the integration replaces an existing tool, note the migration

### Configuration Update

```yaml
forge:
  tooling:
    preferred: mcp # or update if this integration changes preference
    <provider>:
      mcp-server: <server-identifier>
      cli: <cli-name>
```

### ⛔ CHECKPOINT

**STOP.** Review generated artifacts before writing.

---

## Phase 4: Test and Validate

Verify the integration works.

### Steps

1. Execute a simple operation using the new integration
2. Verify the result matches expectations
3. Report success or failure

### Output

```markdown
## Context Anchors

- **Integration:** <name and type>
- **Workspace:** <name>

## Discovered Capabilities

| Tool        | Maps To            | Notes   |
| ----------- | ------------------ | ------- |
| <tool name> | <kernel operation> | <notes> |

## Generated Artifacts

| File   | Purpose       |
| ------ | ------------- |
| <path> | <description> |

## Configuration Changes

<Changes made to workspace.config.yaml>

## Next Step

<Test suggestion or next configuration step>

**Approval Required:** Yes
```

---

## Common Integrations

| Integration       | Type | Typical Mapping                 |
| ----------------- | ---- | ------------------------------- |
| GitHub MCP Server | MCP  | Issues, PRs, repos, code search |
| Azure DevOps CLI  | CLI  | Work items, repos, pipelines    |
| Jira MCP Server   | MCP  | Issues, boards                  |
| Docker CLI        | CLI  | Container operations            |
| Kubernetes CLI    | CLI  | Deployment operations           |

---

## Error Handling

| Error                     | Recovery                                      |
| ------------------------- | --------------------------------------------- |
| MCP server not responding | Verify server is running, check configuration |
| CLI not installed         | Provide installation instructions             |
| Authentication required   | Guide through auth setup                      |
| Capabilities unclear      | Ask human to describe what the tool should do |
