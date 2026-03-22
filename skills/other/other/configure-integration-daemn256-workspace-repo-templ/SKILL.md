---
name: configure-integration
description: Set up a new MCP server, tool integration, or workspace extension
---

# Configure Integration

Uses **Workspace Configurator** (primary) with **Planner** support. When a new tool becomes available in the workspace (MCP server enabled, CLI installed, extension activated), scaffold the appropriate prompts and configuration to integrate it with the agentic system.

**Prerequisites:** Integration is available (MCP server running, CLI installed, etc.), `workspace.config.yaml` exists

---

## Phase 1: Discover

### Identify Capabilities

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
- **Phase:** 1 — Discover

## Discovered Capabilities

| Tool/Command | Category   | Description    |
| ------------ | ---------- | -------------- |
| <name>       | <category> | <what it does> |

## Next Step

Confirm discovered capabilities are correct.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human explicitly approves:

- Discovered capabilities are correct
- Classification is accurate
- No important tools were missed

---

## Phase 2: Map to Kernel Operations

### Determine Integration Points

1. Map discovered tools to kernel operation categories:

| Kernel Operation    | Integration Provides? |
| ------------------- | --------------------- |
| Create issue        | Yes / No              |
| Update board status | Yes / No              |
| Create PR           | Yes / No              |
| Read file contents  | Yes / No              |
| Search code         | Yes / No              |
| Manage releases     | Yes / No              |
| CI operations       | Yes / No              |

2. Identify which existing forge operations this integration can replace or supplement
3. Note any new capabilities not covered by current kernel operations

### Output

```markdown
## Context Anchors

- **Integration:** <name and type>
- **Phase:** 2 — Map to Kernel Operations

## Capability Mapping

| Tool        | Maps To            | Notes   |
| ----------- | ------------------ | ------- |
| <tool name> | <kernel operation> | <notes> |

## New Capabilities

- <capability not covered by current kernel>

## Next Step

Continue to scaffold integration artifacts.

**Approval Required:** No
```

---

## Phase 3: Scaffold

### Generate Integration Artifacts

1. Update `workspace.config.yaml` with integration settings:
   ```yaml
   forge:
     tooling:
       preferred: mcp # or update if this integration changes preference
       <provider>:
         mcp-server: <server-identifier>
         cli: <cli-name>
   ```
2. Generate prompts for mapped operations
3. Update or create forge-ops agent with new tool awareness
4. If the integration replaces an existing tool, note the migration

### Output

```markdown
## Context Anchors

- **Integration:** <name and type>
- **Phase:** 3 — Scaffold

## Proposed Changes

### Configuration Updates

<Changes to workspace.config.yaml>

### Generated Artifacts

| File   | Purpose       |
| ------ | ------------- |
| <path> | <description> |

## Next Step

Review generated artifacts before writing.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not write files until human explicitly approves:

- Configuration changes are correct
- Generated artifacts are appropriate
- No conflicts with existing integrations

---

## Phase 4: Test and Validate

### Verify Integration

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

**Approval Required:** No
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
