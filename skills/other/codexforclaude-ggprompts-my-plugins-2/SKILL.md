---
name: codexforclaude
description: "OpenAI Codex CLI configuration guide for Claude. Use when users ask about: codex config, ~/.codex/config.toml, codex sandbox policies, codex approval modes, creating codex skills, codex mcp servers, codex model settings, local LLM providers, or integrating tools with Codex."
---

# Codex CLI Configuration Guide

Configure and extend OpenAI Codex CLI for optimal development workflows.

## Quick Reference

| Task | Command/Location |
|------|------------------|
| Config file | `~/.codex/config.toml` |
| Add MCP server | `codex mcp add <name> -- <command>` |
| View MCP servers | `/mcp` in TUI |
| Skills location | `~/.codex/skills/` or `.codex/skills/` |
| Create skill | Use `$skill-creator` in Codex |

## Core Configuration

Edit `~/.codex/config.toml` for all settings:

```toml
# Model settings
model = "gpt-5-codex"
model_reasoning_effort = "medium"  # minimal|low|medium|high|xhigh

# Security
sandbox_mode = "workspace-write"   # read-only|workspace-write|danger-full-access
approval_policy = "on-failure"     # untrusted|on-failure|on-request|never

# Trust specific projects
[projects."/path/to/project"]
trust_level = "trusted"
```

**For detailed config options:** See `references/config-toml.md`

## Sandbox and Approval Policies

**Sandbox modes** control file system access:
- `read-only` - Can only read files, no writes
- `workspace-write` - Write within project directory only
- `danger-full-access` - Full system access (use carefully)

**Approval policies** control command execution:
- `untrusted` - Only trusted commands run without approval
- `on-failure` - Auto-run, ask approval only on failures
- `on-request` - Model decides when to ask
- `never` - Never ask (dangerous)

**For security deep dive:** See `references/sandbox-approval.md`

## Adding MCP Servers

### Via CLI (Recommended)
```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
codex mcp add myserver --env API_KEY=xxx -- node server.js
```

### Via config.toml
```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
```

**For full MCP options:** See `references/mcp-servers.md`

## Creating Codex Skills

Skills extend Codex with specialized knowledge. Structure:

```
~/.codex/skills/my-skill/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs
└── assets/           # Optional: templates
```

**Minimal SKILL.md:**
```yaml
---
name: my-skill
description: When to trigger this skill
---

Instructions for Codex when using this skill.
```

**Quick start:** Ask Codex to use `$skill-creator` to bootstrap a new skill.

**For skill development guide:** See `references/creating-skills.md`

## Model and Provider Settings

```toml
# Use specific model
model = "gpt-5-codex"

# Reasoning effort (Responses API)
model_reasoning_effort = "high"  # minimal|low|medium|high|xhigh

# Verbosity (GPT-5)
model_verbosity = "medium"  # low|medium|high

# Use local provider (LM Studio/Ollama)
model_provider = "oss"
```

**For local LLM setup:** See `references/model-providers.md`

## Feature Flags

Enable experimental features in `[features]`:

```toml
[features]
# Stable
shell_tool = true
parallel = true
view_image_tool = true

# Beta
unified_exec = true
shell_snapshot = true

# Experimental
skills = true
tui2 = true
```

## Common Workflows

### Full Autonomous Mode
```bash
codex --full-auto "implement feature X"
# Equivalent to: -a on-request --sandbox workspace-write
```

### Dangerous Bypass (CI/sandboxed environments only)
```bash
codex --dangerously-bypass-approvals-and-sandbox "run tests"
```

### Project-Specific Trust
```toml
[projects."/home/user/trusted-project"]
trust_level = "trusted"
```

## Codex vs Claude Code

| Aspect | Codex | Claude Code |
|--------|-------|-------------|
| Provider | OpenAI | Anthropic |
| Config | `~/.codex/config.toml` | `~/.claude/settings.json` |
| Skills | `~/.codex/skills/` | `~/.claude/skills/` + plugins |
| MCP | `config.toml` sections | `.mcp.json` or plugin |
| Agents | N/A | Plugin agents |
| Hooks | N/A | Plugin hooks |

## Reference Files

- `references/config-toml.md` - Complete config.toml reference
- `references/sandbox-approval.md` - Security policies deep dive
- `references/mcp-servers.md` - MCP server configuration
- `references/creating-skills.md` - Skill development guide
- `references/model-providers.md` - Model and provider settings
