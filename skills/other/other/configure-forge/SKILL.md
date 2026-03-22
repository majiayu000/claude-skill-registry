---
name: configure-forge
description: Generate workspace-level forge binding prompts and agents from workspace.config.yaml topology.
---

# Configure Forge

The Workspace Configurator drives this workflow. Read the workspace's forge topology and tooling preferences, then generate workspace-level prompts and agents that provide concrete forge operations.

**Prerequisites:** `workspace.config.yaml` exists with forge topology and board configuration, AI runtime is active.

---

## Phase 1: Read Configuration

Understand the workspace's forge topology and tooling preferences.

### Steps

1. Read `workspace.config.yaml`
2. Extract:
   - `forge.topology` — which providers handle repos, boards, CI, releases
   - `forge.tooling.preferred` — preferred tool surface (mcp, cli, api)
   - `forge.tooling.<provider>` — provider-specific tool settings
   - `board.*` — board field IDs and option IDs
   - `adapters.ai-runtimes` — which runtimes need generated artifacts

### Output

```markdown
## Context Anchors

- **Workspace:** <name>
- **Forge topology:** <repos>/<boards>/<ci>/<releases>
- **Tooling preference:** <mcp | cli>

## Configuration Detected

| Setting                 | Value   |
| ----------------------- | ------- |
| forge.topology.repos    | <value> |
| forge.topology.boards   | <value> |
| forge.tooling.preferred | <value> |

## Next Step

Confirm topology and preferences before generating.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human confirms topology and preferences.

---

## Phase 2: Determine Artifacts

Decide what forge-specific artifacts to generate.

### Artifact Matrix

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

Create the forge-specific workspace artifacts.

### Steps

1. Generate forge operation prompts for each declared concern (issues, PRs, board)
2. Generate a forge-ops agent that knows the workspace's specific tooling
3. Include board field IDs and option IDs in generated artifacts
4. Include error handling for authentication and connectivity

### ⛔ CHECKPOINT

**STOP.** Review generated artifacts before writing.

---

## Phase 4: Write and Verify

Write generated artifacts and verify they're correct.

### Steps

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
| workspace.config.yaml missing | Run /skill:setup-workspace first                |
| forge.tooling section missing | Use defaults (mcp if available, else cli)       |
| Board field IDs missing       | Ask human to fill in board configuration        |
| Unsupported forge provider    | Report limitation, suggest manual configuration |
