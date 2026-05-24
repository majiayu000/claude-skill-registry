---
name: github-copilot-cli-expert
version: 2.0.0
description: Expert knowledge of GitHub Copilot CLI - installation, configuration, usage, custom agents, MCP servers, and version management. Use when asking about copilot cli, copilot commands, installing copilot, updating copilot, copilot features.
tags: [github-copilot, cli, installation, mcp, agents, skills]
token_budget: 5000
source_urls:
  - https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli
  - https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli
  - https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli
  - https://github.com/github/copilot-cli
auto_triggers:
  - "copilot cli"
  - "github copilot"
  - "install copilot"
  - "update copilot"
  - "copilot version"
  - "copilot commands"
  - "/mcp"
  - "copilot agents"
  - "copilot skills"
---

# GitHub Copilot CLI Expert

**Comprehensive knowledge of GitHub Copilot CLI - the terminal-native AI coding assistant.**

> **Note**: Command syntax and model availability may change. Run `/help` in Copilot CLI for current options.

## Purpose

This skill provides expert guidance on:

1. Installing and updating GitHub Copilot CLI
2. All slash commands and keyboard shortcuts
3. Custom agents, skills, and MCP server configuration
4. Security, permissions, and trusted directories
5. Integration with GitHub workflows (PRs, issues, Actions)
6. Programmatic and interactive usage modes

## Quick Reference

### Installation (Pick One)

```bash
# Homebrew (macOS/Linux) - Recommended
brew install copilot-cli

# npm (all platforms, requires Node.js 22+)
npm install -g @github/copilot

# WinGet (Windows)
winget install GitHub.Copilot

# Install script (macOS/Linux)
curl -fsSL https://gh.io/copilot-install | bash
```

### Update to Latest Version

```bash
# Homebrew
brew upgrade copilot-cli

# npm
npm update -g @github/copilot

# WinGet
winget upgrade GitHub.Copilot

# Check version
copilot --version
```

### Before First Use

**Requirements**:

- Active GitHub Copilot subscription ([Plans](https://github.com/features/copilot/plans))
- Node.js 22+ (if installing via npm)
- PowerShell v6+ (Windows users)

**Authentication**:

```bash
# On first run, you'll be prompted to login
copilot
# Then: /login

# OR set environment variable
export GH_TOKEN="ghp_xxxxxxxxxxxx"
```

### Essential Slash Commands

| Command     | Description                                      |
| ----------- | ------------------------------------------------ |
| `/help`     | Show all commands and shortcuts                  |
| `/model`    | Select AI model (claude-sonnet-4-5, gpt-5, etc.) |
| `/mcp`      | Manage MCP server configuration                  |
| `/agent`    | Browse and select custom agents                  |
| `/delegate` | Hand off task to Copilot coding agent on GitHub  |
| `/compact`  | Reduce context window usage                      |
| `/context`  | Show token usage visualization                   |
| `/usage`    | Display session metrics                          |
| `/diff`     | Review changes made in session                   |
| `/share`    | Export session to file or gist                   |
| `/skills`   | Manage skills for enhanced capabilities          |

### Keyboard Shortcuts

| Shortcut | Action                           |
| -------- | -------------------------------- |
| `@file`  | Include file contents in context |
| `!cmd`   | Execute shell command directly   |
| `Esc`    | Cancel operation / exit prompt   |
| `Ctrl+C` | Cancel / clear / exit            |
| `Ctrl+L` | Clear screen                     |
| `Ctrl+O` | Expand/collapse timeline         |
| `↑/↓`    | Navigate command history         |

## When to Use This Skill

**Auto-triggers** when user mentions:

- "copilot cli", "github copilot", "install copilot"
- "update copilot", "copilot version", "copilot commands"
- "mcp server", "custom agents", "copilot skills"

**Explicitly invoke** via:

```python
Skill(skill="github-copilot-cli-expert")
```

## Navigation Guide

### When to Read Supporting Files

**reference.md** - Read when you need:

- Complete list of all slash commands with detailed options
- All command-line flags and environment variables
- Detailed security configuration (trusted directories, tool permissions)
- Programmatic mode examples and scripting patterns
- MCP server configuration JSON format

**examples.md** - Read when you need:

- Step-by-step workflow examples (PR creation, code review)
- Custom agent creation and invocation examples
- GitHub integration use cases (issues, Actions, PRs)
- Delegation to Copilot coding agent workflows

## Core Capabilities

### 1. Interactive vs Programmatic Mode

**Interactive** (default):

```bash
copilot
# Then type prompts naturally
```

**Programmatic** (scripting):

```bash
copilot -p "Summarize recent commits" --allow-tool 'shell(git)'
```

### 2. Custom Agents

Built-in agents: `explore`, `task`, `plan`, `code-review`

Custom agent locations:

- User-level: `~/.copilot/agents/`
- Repository: `.github/agents/`
- Org/Enterprise: `.github-private/agents/`

### 3. MCP Servers

GitHub MCP server included by default. Add more:

```bash
/mcp add
# Fill details, Ctrl+S to save
```

Config stored in: `~/.copilot/mcp-config.json`

### 4. Security Model

- **Trusted directories**: Confirmed on first launch
- **Tool approval**: Required for file modifications
- **Path permissions**: Current directory + temp by default
- **URL permissions**: All URLs require approval

## Common Patterns

### Include Files in Prompts

```
Explain @config/settings.yml
Fix the bug in @src/app.js
```

### Delegate to GitHub Agent

```bash
/delegate complete the API tests and create a PR
```

### Resume Previous Session

```bash
copilot --resume    # Cycle through sessions
copilot --continue  # Resume most recent
```

### Allow Tools Without Prompts

```bash
copilot --allow-all-tools
copilot --allow-tool 'shell(git)'
copilot --deny-tool 'shell(rm)'
```

## Version Information

**Current Version**: Check with `copilot --version`

**Prerelease Channels**:

```bash
brew install copilot-cli@prerelease
npm install -g @github/copilot@prerelease
winget install GitHub.Copilot.Prerelease
```

**Releases**: https://github.com/github/copilot-cli/releases/

## Troubleshooting

### Authentication Issues

```bash
/login              # In interactive mode
# Or use PAT with GH_TOKEN/GITHUB_TOKEN env var
```

### Context Window Full

```bash
/compact            # Summarize conversation
/context            # View token usage
```

### MCP Server Not Loading

```bash
/mcp show           # List configured servers
/mcp edit [name]    # Edit configuration
```

### Tool Permission Denied

- Check trusted directories: `~/.copilot/config.json` → `trusted_folders`
- Use `--allow-all-paths` or `--allow-all-urls` flags
- Approve tools individually when prompted

### First-Time Setup Issues

**"Copilot not found" after install**:

- Restart terminal after installation
- Check PATH includes install location
- Run `which copilot` (Unix) or `where copilot` (Windows)

**"No subscription" error**:

- Verify at https://github.com/settings/copilot
- Ensure plan includes CLI access
- Try `/logout` then `/login`

## Related Skills

- **mcp-manager**: Advanced MCP server configuration
- **agent-sdk**: Building custom agents
- **documentation-writing**: Clear documentation practices

## Official Resources

- **Docs**: https://docs.github.com/copilot/concepts/agents/about-copilot-cli
- **Usage Guide**: https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli
- **Installation**: https://docs.github.com/copilot/how-tos/set-up/install-copilot-cli
- **Releases**: https://github.com/github/copilot-cli/releases/
- **Feedback**: Use `/feedback` command in CLI
