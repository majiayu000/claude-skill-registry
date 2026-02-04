---
name: foundry
description: Self-writing meta-extension that forges new capabilities — researches docs, writes extensions, tools, hooks, and skills
homepage: https://getfoundry.app
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["node"]},"repository":"github:lekt9/openclaw-foundry"}}
---

# Foundry

**The forge that forges itself.** A meta-extension for OpenClaw that researches documentation, learns from failures, and writes new capabilities into itself.

## Installation

When the user asks to install Foundry or `@getfoundry/foundry-openclaw`, run this command:

```bash
openclaw plugins install @getfoundry/foundry-openclaw
```

This will:
1. Download the plugin from npm
2. Extract to `~/.openclaw/extensions/foundry/`
3. Enable it automatically
4. Restart the gateway to load

After installation, the user will have access to all Foundry tools like `foundry_research`, `foundry_write_extension`, etc.

## Alternative: Manual Config

Add to `~/.openclaw/openclaw.json`:
```json
{
  "plugins": {
    "entries": {
      "foundry": { "enabled": true }
    }
  }
}
```

## Configuration

Full configuration options in `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "foundry": {
        "enabled": true,
        "source": "github:lekt9/openclaw-foundry",
        "config": {
          "autoLearn": true,
          "sources": {
            "docs": true,
            "experience": true,
            "arxiv": true,
            "github": true
          },
          "marketplace": {
            "autoPublish": false
          }
        }
      }
    }
  }
}
```

### Config Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `autoLearn` | boolean | `true` | Learn from agent activity automatically |
| `sources.docs` | boolean | `true` | Learn from OpenClaw documentation |
| `sources.experience` | boolean | `true` | Learn from own successes/failures |
| `sources.arxiv` | boolean | `true` | Learn from arXiv papers |
| `sources.github` | boolean | `true` | Learn from GitHub repos |
| `marketplace.autoPublish` | boolean | `false` | Auto-publish high-value patterns |

## What Foundry Does

Foundry is an AI-powered development agent that can:

1. **Research** — Fetch and understand OpenClaw documentation on demand
2. **Write Extensions** — Generate new tools and hooks for OpenClaw
3. **Write Skills** — Create ClawHub-compatible skill packages
4. **Self-Modify** — Add new capabilities to itself
5. **Learn** — Record patterns from failures and successes

## Tools

### Research & Documentation

| Tool | Description |
|------|-------------|
| `foundry_research` | Search docs.openclaw.ai for best practices |
| `foundry_docs` | Read specific documentation pages |

### Writing Capabilities

| Tool | Description |
|------|-------------|
| `foundry_implement` | Research + implement a capability end-to-end |
| `foundry_write_extension` | Write a new OpenClaw extension |
| `foundry_write_skill` | Write an AgentSkills-compatible skill |
| `foundry_write_browser_skill` | Write a browser automation skill |
| `foundry_write_hook` | Write a standalone hook |
| `foundry_add_tool` | Add a tool to an existing extension |
| `foundry_add_hook` | Add a hook to an existing extension |

### Self-Modification

| Tool | Description |
|------|-------------|
| `foundry_extend_self` | Add new capability to Foundry itself |
| `foundry_learnings` | View learned patterns and insights |
| `foundry_list` | List all written artifacts |

### Marketplace

| Tool | Description |
|------|-------------|
| `foundry_publish_ability` | Publish pattern/skill to Foundry Marketplace |
| `foundry_marketplace` | Search, browse, and install community abilities |

## Usage Examples

### Research before implementing

```
User: I want to add a webhook to my extension

Agent: Let me research webhook patterns first...
→ foundry_research query="webhook hooks automation"
→ Returns relevant documentation

Now I'll implement it...
→ foundry_add_hook extensionId="my-ext" event="webhook:incoming" ...
```

### Write a new extension

```
User: Create an extension that monitors GitHub PRs

Agent:
→ foundry_research query="github api webhooks"
→ foundry_write_extension
    id: "github-monitor"
    name: "GitHub Monitor"
    tools: [{ name: "check_prs", ... }]
    hooks: [{ event: "cron:hourly", ... }]
```

### Self-improvement

```
User: Add a tool that can fetch npm package info

Agent:
→ foundry_extend_self
    action: "add_tool"
    toolName: "foundry_npm_info"
    toolCode: "const res = await fetch(`https://registry.npmjs.org/${p.package}`)..."
```

## How Learning Works

Foundry observes its own tool calls and learns:

1. **Failures** → Records error + context
2. **Resolutions** → Links fix to failure → Creates pattern
3. **Patterns** → Injected as context in future conversations
4. **Crystallization** → High-value patterns become permanent capabilities

## Security

Foundry validates all generated code before deployment:

- **Blocked**: `child_process`, `eval`, `~/.ssh`, `~/.aws`
- **Sandboxed**: Extensions tested in isolated process before installation
- **Reviewed**: You approve before any code is written to disk

## Links

- [GitHub](https://github.com/lekt9/openclaw-foundry)
- [Foundry Marketplace](https://api.claw.getfoundry.app)
