---
name: claude-desktop
description: Central authority for Claude Desktop application - the native desktop app for running Claude Code sessions. Covers installation (macOS/Windows), Git worktrees for parallel sessions, .worktreeinclude file configuration, cloud session launch, environment configuration, MCP Desktop Extensions (.mcpb), and Desktop vs CLI comparison. Assists with Desktop setup, worktree configuration, cloud sessions, and troubleshooting. Delegates 100% to docs-management skill for official documentation.
user-invocable: false
allowed-tools: Read, Glob, Grep, Skill
---

# Claude Desktop Meta Skill

## MANDATORY: Invoke docs-management First

> **STOP - Before providing ANY response about Claude Desktop:**
>
> 1. **INVOKE** `docs-management` skill
> 2. **QUERY** for the user's specific topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded
>
> **Skipping this step results in outdated or incorrect information.**

### Verification Checkpoint

Before responding, verify:

- [ ] Did I invoke docs-management skill?
- [ ] Did official documentation load?
- [ ] Is my response based EXCLUSIVELY on official docs?

If ANY checkbox is unchecked, STOP and invoke docs-management first.

---

## Overview

Central authority for Claude Desktop - the native desktop application for running Claude Code sessions locally or on cloud infrastructure. This skill uses **100% delegation to docs-management** - it contains NO duplicated official documentation.

**Architecture:** Pure delegation with keyword registry. All official documentation is accessed via docs-management skill queries.

## When to Use This Skill

**Keywords:** Claude Desktop, desktop app, desktop application, worktree, worktrees, .worktreeinclude, parallel sessions, cloud session, cloud execution, remote environment, desktop extensions, .mcpb, MCP bundle, bundled version, claude.ai/download, Desktop vs CLI

**Use this skill when:**

- Installing or setting up Claude Desktop
- Configuring Git worktrees for parallel sessions
- Creating .worktreeinclude files
- Starting cloud sessions from Desktop
- Configuring environment variables in Desktop
- Installing Desktop Extensions (.mcpb)
- Understanding Desktop vs CLI differences
- Troubleshooting Desktop-specific issues
- Configuring worktree location

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill for official documentation:

### Installation and Setup

| Topic | Keywords |
| --- | --- |
| Download | "Claude Desktop download", "claude.ai/download" |
| System Requirements | "Desktop system requirements", "macOS Windows requirements" |
| First Launch | "bundled Claude Code version", "Desktop first launch" |
| Version Management | "Desktop version updates", "bundled version" |

### Git Worktrees

| Topic | Keywords |
| --- | --- |
| Parallel Sessions | "parallel local sessions", "Git worktrees Desktop" |
| Worktree Location | "worktree location", "~/.claude-worktrees" |
| .worktreeinclude | ".worktreeinclude file", "copy gitignored files" |
| Worktree Patterns | ".worktreeinclude patterns", ".env worktree" |

### Cloud Sessions

| Topic | Keywords |
| --- | --- |
| Cloud Execution | "cloud session launch", "remote environment Desktop" |
| Teleport | "/teleport command", "teleport cloud session" |
| Remote Environments | "/remote-env", "remote execution" |

### Environment Configuration

| Topic | Keywords |
| --- | --- |
| PATH Extraction | "Desktop PATH extraction", "shell configuration" |
| Custom Variables | "Desktop environment variables", "custom env vars" |
| Multiline Values | "multiline environment variables", "CERT environment" |

### Desktop Extensions

| Topic | Keywords |
| --- | --- |
| MCPB Format | "Desktop extensions", ".mcpb files", "MCP bundle" |
| Installing Extensions | "install Desktop extension", "drag extension" |
| Extension Overview | "one-click MCP installation", "bundled Node.js" |

### Desktop vs CLI

| Topic | Keywords |
| --- | --- |
| Comparison | "Desktop vs CLI", "Claude Desktop comparison" |
| When to Use | "when to use Desktop", "Desktop use cases" |
| Interface | "Desktop interface", "graphical interface" |

### Configuration Files

| Topic | Keywords |
| --- | --- |
| Desktop Config | "claude_desktop_config.json", "Desktop MCP config" |
| Config Location macOS | "~/Library/Application Support/Claude" |
| Config Location Windows | "%APPDATA%\\Claude" |

## Quick Decision Tree

**What do you want to do?**

1. **Install Claude Desktop** -> Query docs-management: "Claude Desktop download", "Desktop system requirements"
2. **Set up parallel sessions** -> Query docs-management: "parallel local sessions", "Git worktrees Desktop"
3. **Configure .worktreeinclude** -> Query docs-management: ".worktreeinclude file", ".worktreeinclude patterns"
4. **Start cloud sessions** -> Query docs-management: "cloud session launch", "remote environment Desktop"
5. **Configure environment variables** -> Query docs-management: "Desktop environment variables", "custom env vars"
6. **Install Desktop Extensions** -> Query docs-management: "Desktop extensions", ".mcpb files"
7. **Choose Desktop vs CLI** -> Query docs-management: "Desktop vs CLI", "Desktop use cases"
8. **Configure MCP in Desktop** -> Query docs-management: "claude_desktop_config.json", "Desktop MCP config"
9. **Troubleshoot issues** -> Query docs-management: "Desktop troubleshooting" + specific issue

## Topic Coverage

### Installation

- Download from claude.ai/download
- macOS Universal build (Intel + Apple Silicon)
- Windows x64 and ARM64 versions
- Windows ARM64 limitation (cloud-only)
- First launch bundled version download
- Automatic version management

### Git Worktrees for Parallel Sessions

- Run multiple Claude Code sessions simultaneously
- Isolated worktree per session
- Default location: ~/.claude-worktrees
- Configurable worktree location
- Git initialization requirement

### .worktreeinclude Configuration

- Copy .gitignored files to worktrees
- .gitignore-style pattern syntax
- Must match BOTH .worktreeinclude AND .gitignore
- Common patterns (.env, .env.local, .env.*, settings.local.json)

### Cloud Sessions

- Launch on Anthropic secure infrastructure
- Select remote environment on session creation
- /teleport command for cloud sessions
- /remote-env command for environment configuration
- claude.ai subscriber features

### Environment Configuration

- Automatic PATH extraction from shell
- Access to yarn, npm, node, development tools
- Custom environment variable configuration
- .env format for key-value pairs
- Multiline value support with quotes

### Desktop Extensions (.mcpb)

- One-click MCP server installation
- File format: .mcpb (MCP Bundle)
- No terminal or manual configuration
- Bundled Node.js runtime
- Drag-and-drop installation

### Desktop vs CLI Differences

- Desktop: Graphical interface, higher control, stability-focused
- CLI: Command-line, agentic behavior, newer features first
- Desktop: Beginners, non-coders, deliberate workflows
- CLI: Professional developers, automation, IDE integration
- Worktrees: Built-in GUI (Desktop) vs manual CLI

## Delegation Patterns

### Standard Query Pattern

```text
User asks: "How do I set up Claude Desktop?"

1. Invoke docs-management skill
2. Use keywords: "Claude Desktop download", "Desktop system requirements"
3. Load official documentation
4. Provide guidance based EXCLUSIVELY on official docs
```

### Multi-Topic Query Pattern

```text
User asks: "I want parallel sessions with my .env files copied"

1. Invoke docs-management skill with multiple queries:
   - "parallel local sessions", "Git worktrees Desktop"
   - ".worktreeinclude file", ".worktreeinclude patterns"
2. Synthesize guidance from official documentation
```

### Troubleshooting Pattern

```text
User reports: "Worktree isn't being created"

1. Invoke docs-management skill
2. Use keywords: "Git worktrees Desktop", "worktree requirements"
3. Check official docs for Git initialization requirement
4. Guide user through setup from official docs
```

## Troubleshooting Quick Reference

| Issue | Keywords for docs-management |
| --- | --- |
| Worktree not created | "Git worktrees Desktop", "Git initialization" |
| Cloud sessions unavailable | "cloud session launch", "remote environment" |
| Extension won't install | "Desktop extensions", ".mcpb files" |
| Environment variables not working | "Desktop environment variables", "PATH extraction" |
| Windows ARM64 local sessions | "Windows ARM64", "Desktop limitations" |
| MCP config location | "claude_desktop_config.json" + platform |

## References

**Reference files:**

- [Setup Guide](references/setup-guide.md) - Installation and environment configuration
- [Worktrees](references/worktrees.md) - Parallel sessions and .worktreeinclude
- [MCP Configuration](references/mcp-configuration.md) - Desktop MCP and extensions
- [Cloud Sessions](references/cloud-sessions.md) - Cloud execution and teleport
- [Troubleshooting](references/troubleshooting.md) - Common issues and diagnostics

**Official Documentation (via docs-management skill):**

- Primary: "desktop" documentation
- Related: "mcp", "settings", "quickstart"

## Cross-References

- **MCP Integration**: For detailed MCP configuration, use the `mcp-integration` skill
- **Settings Management**: For general settings, use the `settings-management` skill

## Version History

- **v1.0.0** (2026-01-12): Initial release
  - Pure delegation architecture
  - Comprehensive keyword registry
  - Quick decision tree
  - Topic coverage for all Desktop features
  - Troubleshooting quick reference

---

## Last Updated

**Date:** 2026-01-12
**Model:** claude-opus-4-5-20251101
