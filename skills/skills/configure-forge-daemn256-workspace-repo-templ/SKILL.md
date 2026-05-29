---
name: configure-forge
description: Generate workspace-level forge binding prompts and agents from workspace.config.yaml topology
---

# Configure Forge

Uses **Workspace Configurator** to read the workspace's forge topology and tooling preferences, then generate workspace-level prompts and agents that provide concrete forge operations.

**Prerequisites:** `workspace.config.yaml` exists with forge topology and board configuration

---

## Phase 1: Read Configuration

### Extract Forge Topology

1. Read `workspace.config.yaml`
2. Extract the following settings:
   - `forge.topology` — which providers handle repos, boards, CI, releases
   - `forge.tooling.preferred` — preferred tool surface (mcp, cli, api)
   - `forge.tooling.<provider>` — provider-specific tool settings
   - `board.*` — board field IDs and option IDs
   - `adapters.ai-runtimes` — which runtimes need generated artifacts
3. Present extracted configuration for confirmation

### Output

```markdown
## Context Anchors

- **Workspace:** <name>
- **Phase:** 1 — Read Configuration

## Forge Topology

| Setting                   | Value   |
| ------------------------- | ------- |
| `forge.topology.repos`    | <value> |
| `forge.topology.boards`   | <value> |
| `forge.topology.ci`       | <value> |
| `forge.topology.releases` | <value> |
| `forge.tooling.preferred` | <value> |

## Board Configuration

| Field          | ID      |
| -------------- | ------- |
| project_id     | <value> |
| status field   | <value> |
| priority field | <value> |

## Next Step

Confirm topology and preferences before generating artifacts.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human explicitly approves:

- Topology settings are correct
- Tooling preferences are appropriate
- Board configuration is complete

---

## Phase 2: Determine Artifacts

### Artifact Matrix

Based on topology and tooling preferences, determine what to generate:

| Topology Setting | Tool Preference | Generates                                                    |
| ---------------- | --------------- | ------------------------------------------------------------ |
| `boards: github` | `mcp`           | Artifacts using GitHub MCP server for issue/board operations |
| `boards: github` | `cli`           | Artifacts using `gh` CLI for issue/board operations          |
| `boards: ado`    | `cli`           | Artifacts using `az boards` CLI for work item operations     |
| `repos: github`  | `mcp`           | Artifacts using GitHub MCP for repo operations               |
| `repos: github`  | `cli`           | Artifacts using `gh` CLI for repo operations                 |

### Per-Runtime Output

| Runtime        | Output Location                       | Agent Location                      |
| -------------- | ------------------------------------- | ----------------------------------- |
| GitHub Copilot | `.github/prompts/forge-ops.prompt.md` | `.github/agents/forge-ops.agent.md` |
| Claude Code    | `.claude/skills/forge-ops/SKILL.md`   | `.claude/agents/forge-ops.md`       |

---

## Phase 3: Generate

### Create Forge Artifacts

1. Generate forge operation prompts for each declared concern (issues, PRs, board)
2. Generate a forge-ops agent that knows the workspace's specific tooling
3. Include board field IDs and option IDs in generated artifacts
4. Include error handling for authentication and connectivity

### Generated Prompt Structure

```markdown
# Forge: <Operation Name>

> <What this prompt does>

## Configuration

- **Provider:** <from workspace.config.yaml>
- **Tool surface:** <mcp | cli>
- **Board project:** <project_id>

## Operations

### Create Issue

<Provider-specific commands/tool calls for creating an issue>

### Update Board Status

<Provider-specific commands for setting board field values>

### Create PR

<Provider-specific commands for creating a pull request>
```

### Output

```markdown
## Context Anchors

- **Workspace:** <name>
- **Phase:** 3 — Generate
- **Forge topology:** <repos>/<boards>/<ci>/<releases>

## Proposed Artifacts

| File   | Purpose       |
| ------ | ------------- |
| <path> | <description> |

## Next Step

Review generated artifacts before writing.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not write files until human explicitly approves:

- Generated artifacts are correct
- Tooling preferences are correctly reflected
- Board field IDs are properly included

---

## Phase 4: Write and Verify

### Write Generated Artifacts

1. Write generated files to appropriate locations
2. List what was generated
3. Suggest testing the generated prompts

### Output

```markdown
## Context Anchors

- **Workspace:** <name>
- **Forge topology:** <repos>/<boards>/<ci>/<releases>
- **Tooling preference:** <mcp | cli>

## Generated Artifacts

| File   | Purpose       |
| ------ | ------------- |
| <path> | <description> |

## Next Step

Test the generated prompts by running a forge operation.

**Approval Required:** No
```

---

## Error Handling

| Error                         | Recovery                                        |
| ----------------------------- | ----------------------------------------------- |
| workspace.config.yaml missing | Run /setup-workspace first                      |
| forge.tooling section missing | Use defaults (mcp if available, else cli)       |
| Board field IDs missing       | Ask human to fill in board configuration        |
| Unsupported forge provider    | Report limitation, suggest manual configuration |
