---
name: "Teams App Patterns Skill"
description: "Full Teams app development patterns."
applyTo: "**/*teams*,**/*manifest*,**/*m365*"
---

# Teams App Patterns Skill

> Full Teams app development patterns.

## ⚠️ Staleness Warning

Teams platform evolves rapidly. **Last validated:** February 13, 2026 (M365 Agents Toolkit CLI 3.1.0, Manifest v1.19, DA v1.6)

**Check:** [Teams Docs](https://learn.microsoft.com/en-us/microsoftteams/platform/), [M365 Agents Toolkit](https://github.com/OfficeDev/TeamsFx)

> 💡 Use `@m365agents` chat participant in VS Code Copilot Chat for scaffolding, schema help, and troubleshooting.

---

## Available MCP Tools

The `@m365agents` chat participant exposes MCP tools. **Use these programmatically** before falling back to manual docs:

| Tool | Purpose | Example Use |
| ---- | ------- | ----------- |
| `mcp_m365agentstoo_get_schema` | Get current manifest schemas | Validate app manifest (v1.19), DA manifest (v1.0), API plugin (v2.1), M365 agents YAML |
| `mcp_m365agentstoo_get_code_snippets` | Working code samples | Teams AI library, Teams JS SDK, botbuilder patterns |
| `mcp_m365agentstoo_get_knowledge` | Development knowledge base | Copilot extensibility, capabilities, best practices |
| `mcp_m365agentstoo_troubleshoot` | Diagnose issues | Sideloading, conditional access, schema errors |

**When to use**: Any M365/Teams development task — call the relevant MCP tool first, then supplement with skill knowledge.

---

## ⚠️ Critical: Declarative Agent v1.6 Schema

**declarativeAgent.json** for M365 Copilot agents has specific schema requirements:

| Field | Wrong (Pre-v1.6) | Correct (v1.6) |
|-------|------------------|----------------|
| `disclaimer` | `"text string"` | `{ "text": "..." }` |
| `behavior_overrides.suggestions` | `false` | `{ "disabled": false }` |
| `behavior_overrides.special_instructions` | `"text string"` | `{ "discourage_model_knowledge": false }` |
| `user_overrides` | `{ "capabilities": [...] }` | `[ { "path": "$.capabilities[?(@.name=='X')]", "allowed_actions": ["remove"] } ]` |

**CLI Version Matters:**
- **v2.x**: `--app-package-file` flag, may NOT include declarativeAgent.json in zip (bug)
- **v3.x**: `--package-file` flag, correctly includes declarativeAgent.json

**Upgrade CLI if packaging fails:**
```powershell
npm install -g @microsoft/teamsapp-cli@latest
teamsapp --version  # Should be 3.x
```

---

## App Package

```text
appPackage/
├── manifest.json        # Teams app manifest (schema v1.19+)
├── outline.png          # 32x32, transparent bg, white only
├── color.png            # 192x192, no transparency
└── declarativeAgent.json # Required for M365 Copilot agents (DA v1.6)
```

### Icon Requirements (CRITICAL)
| Icon | Size | Background | Content |
|------|------|------------|---------|
| color.png | 192×192 | Any | Full color logo |
| outline.png | 32×32 | **Transparent** (Alpha=0) | **White only** (255,255,255) |

**❌ Common failures:** Wrong dimensions, outline has gray background, outline uses colors

### Icon Generation from SVG (Brand Consistency)

When syncing icons from VS Code assets to M365:

```powershell
# Install sharp if needed
npm install sharp

# Generate color.png (192x192) from logo.svg
node -e "const sharp = require('sharp'); sharp('vscode-extension/assets/logo.svg').resize(192, 192).png().toFile('appPackage/color.png')"

# Generate outline.png (32x32) from monochrome SVG
node -e "const sharp = require('sharp'); sharp('vscode-extension/assets/logo-mono.svg').resize(32, 32).png().toFile('appPackage/outline.png')"
```

**Source of truth**: `platforms/vscode-extension/assets/logo.svg` and `logo-mono.svg`

---

## Manifest Required Fields

- `$schema`, `manifestVersion`, `version`, `id`
- `name.short`, `name.full`
- `description.short`, `description.full`
- `icons.outline`, `icons.color`
- `developer.*`, `validDomains`

## Bot Handler

```typescript
class MyBot extends TeamsActivityHandler {
    constructor() {
        super();
        this.onMessage(async (context, next) => { ... });
    }
}
```

## Adaptive Card Structure

```json
{ "type": "AdaptiveCard", "version": "1.5", "body": [...], "actions": [...] }
```

## Teams SDK

```typescript
await microsoftTeams.app.initialize();
const context = await microsoftTeams.app.getContext();
```

## SSO

```typescript
const token = await microsoftTeams.authentication.getAuthToken();
```

## Toolkit Commands

The M365 Agents Toolkit (formerly Teams Toolkit) provides:

**CLI commands:**
```powershell
npx teamsapp package --env local
npx teamsapp validate --package-file ...
npx teamsapp preview --env local
```

**MCP tools** (available when M365 Agents Toolkit extension is installed):
```
mcp_m365agentstoo_get_schema("app_manifest")       # Get Teams app manifest schema
mcp_m365agentstoo_get_schema("declarative_agent_manifest")  # Get DA schema
mcp_m365agentstoo_get_code_snippets("adaptive cards")       # Find code samples
mcp_m365agentstoo_troubleshoot("sideloading fails")         # Diagnose issues
```

**`@m365agents` chat participant** — ask in VS Code Copilot Chat:
- "I want to create a declarative agent"
- "How to add SSO?"
- "My Teams app doesn't sideload"
- "Generate a manifest for my scenario"

## Common Issues

| Issue | Solution | MCP Tool |
| ----- | -------- | -------- |
| Manifest fails | Check schema version | `mcp_m365agentstoo_get_schema` |
| Bot not responding | Verify endpoint/tunnel | `mcp_m365agentstoo_troubleshoot` |
| Sideload fails | Enable custom apps in admin | `mcp_m365agentstoo_troubleshoot` |
| Need code samples | Find working patterns | `mcp_m365agentstoo_get_code_snippets` |
| **Conditional access blocks CLI** | `@m365agents` for guidance or manual Developer Portal upload | `mcp_m365agentstoo_troubleshoot` |

### Conditional Access Workaround

Microsoft orgs with strict conditional access policies may block `teamsapp auth login m365`. Error: `AADSTS530084`.

**Fallback: Manual Developer Portal Upload**
1. Build package: `npm run package:dev`
2. Validate: `npx teamsapp validate --package-file ./appPackage/build/appPackage.dev.zip`
3. Open: https://dev.teams.microsoft.com/apps
4. Import app package → Upload zip
5. Publish to org catalog

---

## Store Description Strategy

**Key insight**: Same product, different audiences require different messaging.

| Platform | Audience | Focus |
|----------|----------|-------|
| VS Code Marketplace | Developers | Code acceleration, syntax, debugging |
| M365/Teams | Knowledge workers | Research, analysis, productivity |

**M365 Positioning Example**:
- ❌ "Accelerate your Python development"
- ✅ "Your AI research partner. Remembers context, grows with you."

## Synapses

See [synapses.json](synapses.json) for connections.
