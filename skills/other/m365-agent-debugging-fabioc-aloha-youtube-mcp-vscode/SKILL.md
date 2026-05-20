---
name: "M365 Declarative Agent Debugging Skill"
description: "Debug non-functional M365 Copilot declarative agents."
user-invokable: false
---

# M365 Declarative Agent Debugging Skill

> Debug non-functional M365 Copilot declarative agents.

## ⚠️ Staleness Warning

M365 Copilot and Teams platform APIs are in rapid evolution. Schema versions, capabilities, and tooling change frequently.

**Refresh triggers:**

- New declarativeAgent schema versions
- M365 Agents Toolkit updates (formerly Teams Toolkit)
- New M365 Copilot capabilities
- Developer Portal changes

**Last validated:** February 2026 (Schema v1.6+, M365 Agents Toolkit with `@m365agents` chat participant)

**Check current state:** [Declarative Agent Schema](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/declarative-agent-manifest), [M365 Agents Toolkit](https://github.com/OfficeDev/TeamsFx)

---

## Available MCP Tools

The **M365 Agents Toolkit** exposes MCP tools via the `@m365agents` chat participant. Use these **before manual debugging**:

| Tool | When to Use |
| ---- | ----------- |
| `mcp_m365agentstoo_get_schema` | Validate manifest structure — get the **current** app manifest (v1.19), declarative agent (v1.0), or API plugin (v2.1) schema |
| `mcp_m365agentstoo_troubleshoot` | Diagnose common issues — schema validation failures, sideloading errors, conditional access blocks |
| `mcp_m365agentstoo_get_knowledge` | Look up M365 Copilot development knowledge — capabilities, limits, best practices |
| `mcp_m365agentstoo_get_code_snippets` | Find working examples — Teams AI, Teams JS, botbuilder code samples |

**Workflow integration**: Always try `mcp_m365agentstoo_troubleshoot` first when a user reports an M365 agent issue. Use `mcp_m365agentstoo_get_schema` to verify manifest structure before manual schema checks.

---

## Schema Version Validation

**Critical**: Schema versions and their capabilities:

| Version | Status | Key Additions |
| ------- | ------ | ------------- |
| v1.0 | Original baseline | Core capabilities |
| v1.2 | Stable | WebSearch sites, GraphicArt, CodeInterpreter |
| v1.5 | Extended | TeamsMessages, Email, People |
| v1.6 | **LATEST** | Dataverse, Meetings, EmbeddedKnowledge, worker_agents |

**v1.3 and v1.4 DO NOT EXIST** — unrecognized schema makes entire document invalid.

## Capability Compatibility

| Capability | v1.2 | v1.5 | v1.6 |
| ---------- | ---- | ---- | ---- |
| OneDriveAndSharePoint | ✅ | ✅ | ✅ |
| WebSearch | ✅ | ✅ | ✅ |
| GraphicArt | ✅ | ✅ | ✅ |
| CodeInterpreter | ✅ | ✅ | ✅ |
| GraphConnectors | ✅ | ✅ | ✅ |
| TeamsMessages | ❌ | ✅ | ✅ |
| Email | ❌ | ✅ | ✅ |
| People | ❌ | ✅ | ✅ |
| Meetings | ❌ | ❌ | ✅ |
| Dataverse | ❌ | ❌ | ✅ |
| EmbeddedKnowledge | ❌ | ❌ | ✅ (not yet available) |
| ScenarioModels | ❌ | ❌ | ✅ |

**Lesson**: v1.5/v1.6 capabilities with v1.2 schema = silent failure.

## Manifest Limits (v1.6)

| Property | Limit |
| -------- | ----- |
| `name` | 100 characters |
| `description` | 1,000 characters |
| `instructions` | 8,000 characters |
| `conversation_starters` | **6 items max** (was 12 in v1.2) |
| `actions` | 1-10 items |
| `WebSearch.sites` | 4 items |
| `TeamsMessages.urls` | 5 items |
| `Meetings.items_by_id` | 5 items |

## Icon Requirements

**color.png**: 192×192px, solid background, logo in center 120×120 safe zone

**outline.png**: 32×32px, white only (#FFFFFF), transparent background (Alpha=0)

**Common error**:

```text
Error: Outline icon is not transparent. Alpha,R,G,B: 255,X,X,X
```

Alpha=255 means opaque. Background pixels must be Alpha=0.

## Debugging Workflow

1. **MCP first**: Call `mcp_m365agentstoo_troubleshoot` with the error message or symptom — this often resolves the issue immediately

2. **Schema check**: Call `mcp_m365agentstoo_get_schema` with the relevant schema type (`app_manifest`, `declarative_agent_manifest`, `api_plugin_manifest`) to verify structure

3. **Validate package**: `teamsapp validate --package-file <zip>` (must pass all checks)

4. **Use `@m365agents` chat participant**: Ask `@m365agents` in VS Code Copilot Chat for interactive troubleshooting — it has scaffolding, schema help, and guided debugging

5. **Manual schema check** (fallback):
   - ✅ `.../declarative-agent/v1.2/schema.json`
   - ❌ `.../declarative-agent/v1.3/schema.json` (doesn't exist)

6. **Verify capabilities match schema version**

7. **Test icon transparency**:

```powershell
Add-Type -AssemblyName System.Drawing
$bmp = New-Object System.Drawing.Bitmap("outline.png")
$pixel = $bmp.GetPixel(0, 0)
$bmp.Dispose()
"Alpha: $($pixel.A)"  # Should be 0
```

## Package Checklist

- [ ] `manifest.json` — Teams app manifest (v1.19)
- [ ] `declarativeAgent.json` — Agent config (v1.2)
- [ ] `color.png` — 192×192 solid
- [ ] `outline.png` — 32×32 white on transparent

## Symptom → Cause

| Symptom | Likely Cause | MCP Tool |
| ------- | ------------ | -------- |
| Agent not responding | Invalid schema version | `mcp_m365agentstoo_troubleshoot` |
| Only 1 conversation starter | Schema validation failed | `mcp_m365agentstoo_get_schema` |
| Validation errors on icon | Wrong transparency/size | — (manual check) |
| Capability not working | Schema version mismatch | `mcp_m365agentstoo_get_knowledge` |
| Sideloading fails | Admin policy or manifest error | `mcp_m365agentstoo_troubleshoot` |

## Memory via OneDrive

Agent reads from OneDrive using `OneDriveAndSharePoint` capability:

1. User creates `Alex-Memory/` folder in OneDrive
2. User shares folder link in chat
3. Agent reads cognitive files from shared folder
4. For writes: Alex generates content → user pastes

**Benefits**: No Azure Functions, no API costs, user controls data.

## Deployment Flow

```powershell
npx teamsapp package --env local
npx teamsapp validate --package-file appPackage/build/*.zip
# Upload to Developer Portal → Preview in Teams
```

## Synapses

See [synapses.json](synapses.json) for connections.
