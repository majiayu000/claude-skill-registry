---
name: gui-tools
description: Provides guidance for installing, configuring, and choosing Git graphical interface clients (GitKraken, Sourcetree, GitHub Desktop) across platforms. Compares features, licensing, and workflows. Troubleshoots graphical tool configuration and setup issues. Use when installing Git graphical clients, setting up Git visualization tools, configuring graphical commit tools, choosing between options, or troubleshooting configuration. Covers Windows, macOS, and Linux. All tools are optional and based on user preference.
allowed-tools: Read, Bash, Glob, Grep
---

# Git GUI Tools

Optional graphical user interface tools for Git. These tools provide visual interfaces for Git operations, making it easier to stage changes, review diffs, manage branches, and visualize repository history.

## Overview

This skill helps you:

- Choose the right Git GUI tool for your workflow
- Install popular Git GUI clients on Windows, macOS, and Linux
- Configure GUI tools properly
- Understand licensing and subscription requirements
- Troubleshoot common configuration issues

**Important**: All GUI tools are **optional**. They complement the command-line interface but are not required for Git usage. Many developers prefer command-line Git exclusively.

## When to Use This Skill

Use this skill when:

- Installing Git GUI clients for the first time
- Choosing between GitKraken, Sourcetree, GitHub Desktop, or other tools
- Configuring GUI tools after installation
- Troubleshooting GUI tool configuration (Sourcetree gitignore, etc.)
- Understanding licensing requirements for commercial GUI tools
- Looking for platform-specific GUI recommendations

## First Use: Detection and Setup

Before installing new GUI tools, check what's already installed on your system.

**Check for existing GUI tools:**

```bash
# Check if GitKraken is installed
which gitkraken           # macOS/Linux
where.exe gitkraken       # Windows PowerShell

# Check if Sourcetree is installed
# Windows: Check "C:\Users\<user>\AppData\Local\SourceTree"
# macOS: Check "/Applications/Sourcetree.app"
test -d "/Applications/Sourcetree.app" && echo "Sourcetree installed" || echo "Sourcetree not found"

# Check if GitHub Desktop is installed
which github-desktop      # macOS/Linux (as 'github')
where.exe GitHubDesktop   # Windows PowerShell

# Check built-in Git GUI tools (come with Git)
git gui --version         # Git GUI (built-in with Git)
gitk --version            # gitk (built-in repository browser)
```

**If no GUI tools are installed, proceed with Quick Start below.**

## Quick Start

**Windows - Quick Install:**

```powershell
# GitKraken (cross-platform, modern UI, requires license for private repos)
winget install --id Axosoft.GitKraken -e --source winget

# Sourcetree (free, Atlassian, Windows/macOS only)
winget install --id Atlassian.Sourcetree -e --source winget

# GitHub Desktop (free, simple, GitHub-focused)
winget install --id GitHub.GitHubDesktop -e --source winget

# Fork (free evaluation, fast and modern)
winget install --id Fork.Fork -e --source winget
```

**macOS - Quick Install:**

```bash
# GitKraken (via Homebrew Cask)
brew install --cask gitkraken

# Sourcetree (via Homebrew Cask)
brew install --cask sourcetree

# GitHub Desktop (via Homebrew Cask)
brew install --cask github

# Fork (via Homebrew Cask)
brew install --cask fork
```

**Linux - Quick Install:**

```bash
# GitKraken (download .deb or .rpm from website)
# https://www.gitkraken.com/download

# GitHub Desktop (community fork)
# https://github.com/shiftkey/desktop

# GitAhead (open source, lightweight)
# https://github.com/gitahead/gitahead
```

---

## Tool Comparison Quick Reference

| Tool | Platforms | License | Best For |
| --- | --- | --- | --- |
| **GitKraken** | Windows, macOS, Linux | Free (public repos), Pro (private) | Teams, visual learners, complex workflows |
| **Sourcetree** | Windows, macOS | Free | Atlassian users, feature-rich GUI |
| **GitHub Desktop** | Windows, macOS, Linux (fork) | Free | GitHub users, simplicity |
| **Fork** | Windows, macOS | Free (evaluation) | Modern alternative to Sourcetree |
| **Git GUI/gitk** | All (comes with Git) | Free (GPL) | Lightweight, no installation |
| **GitAhead** | Windows, macOS, Linux | Free (MIT) | Lightweight, open source |

**📖 For detailed comparison:** See [references/tool-comparison.md](references/tool-comparison.md) for comprehensive feature analysis, licensing details, and official documentation links.

---

## Platform-Specific Installation

For detailed installation instructions for each platform, see:

- **Windows**: [references/windows-installation.md](references/windows-installation.md)
- **macOS**: [references/macos-installation.md](references/macos-installation.md)
- **Linux**: [references/linux-installation.md](references/linux-installation.md)

---

## Built-in Tools (All Platforms)

Git ships with two built-in GUI tools:

- **gitk** - Repository browser for visualizing history
- **Git GUI** - Commit tool for staging changes

```bash
# Open gitk (history browser)
gitk --all

# Open Git GUI (commit tool)
git gui
```

**📖 For detailed usage:** See [references/built-in-tools.md](references/built-in-tools.md) for commands, features, and use cases.

---

## Choosing the Right Tool

**Quick recommendations:**

- **Beginners** → GitHub Desktop
- **GitHub users** → GitHub Desktop or GitKraken
- **Bitbucket users** → Sourcetree
- **Advanced users** → Fork, Tower, or SmartGit
- **Linux users** → GitAhead, SmartGit, or built-in tools
- **Visual learners** → GitKraken
- **Command-line purists** → None (or gitk for quick visualization)

**📖 For detailed guidance:** See [references/choosing-right-tool.md](references/choosing-right-tool.md) for comprehensive decision criteria.

---

## Configuration After Installation

After installing a GUI tool:

1. **Configure Git identity** (if not already done)
2. **Add SSH keys** (for SSH cloning)
3. **Authenticate with Git hosting provider** (GitHub, GitLab, Bitbucket)
4. **Configure diff/merge tool** (optional)

**📖 For detailed steps:** See [references/configuration.md](references/configuration.md) for complete post-installation configuration.

---

## Troubleshooting

**Common issues:**

- **GUI tool not detecting repositories** - Add repository directory in settings
- **Authentication failures** - Check credential helper, refresh auth tokens
- **Merge conflicts not resolving** - Configure merge tool or use command-line
- **Slow performance** - Enable Git performance features, consider Git LFS

**📖 For detailed solutions:** See [references/troubleshooting.md](references/troubleshooting.md) for comprehensive troubleshooting guidance.

---

## Related Skills

- **setup**: Basic Git installation and configuration
- **config**: Comprehensive Git configuration (credentials, performance, aliases)
- **line-endings**: Line ending configuration and Git LFS
- **gpg-signing**: GPG commit signing setup

---

## Test Scenarios

### Scenario 1: Tool installation

- Query: "Install GitKraken on Windows"
- Expected: Provides winget command and licensing information

### Scenario 2: Tool selection guidance

- Query: "Choose between Sourcetree and GitHub Desktop for Bitbucket"
- Expected: Recommends Sourcetree with rationale from comparison table

### Scenario 3: Troubleshooting

- Query: "Troubleshoot Sourcetree global gitignore configuration"
- Expected: Provides configuration fix steps from troubleshooting section

### Scenario 4: Platform-specific setup

- Query: "Set up Fork on macOS"
- Expected: Provides installation command and licensing notes

### Scenario 5: Comparison request

- Query: "Compare all Linux GUI options"
- Expected: Shows GitAhead, SmartGit, and community GitHub Desktop with pros/cons

---

## Multi-Model Testing Notes

**Testing Status**:

| Model | Status | Date Tested | Notes |
| --- | --- | --- | --- |
| **Claude Sonnet** | ✅ VERIFIED | 2025-11-25 | Skill activates correctly, provides appropriate tool recommendations with platform-specific guidance |
| **Claude Haiku** | 🔄 PENDING | — | Recommend testing: Activation reliability, concise recommendations |
| **Claude Opus** | 🔄 PENDING | — | Recommend testing: Over-explanation risk, cross-platform complexity |

**Last Updated**: 2025-11-28

---

## References

**Detailed Guides:**

- [references/tool-comparison.md](references/tool-comparison.md) - Comprehensive tool comparison matrix
- [references/built-in-tools.md](references/built-in-tools.md) - Git GUI and gitk usage
- [references/choosing-right-tool.md](references/choosing-right-tool.md) - Decision guidance by use case
- [references/configuration.md](references/configuration.md) - Post-installation configuration
- [references/windows-installation.md](references/windows-installation.md) - Windows installation guide
- [references/macos-installation.md](references/macos-installation.md) - macOS installation guide
- [references/linux-installation.md](references/linux-installation.md) - Linux installation guide
- [references/troubleshooting.md](references/troubleshooting.md) - Troubleshooting common issues

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

> **💡 Tip for AI Agents:** When helping users choose or install Git GUI tools, consider using available MCP servers for current information:
>
> - **Pricing Updates**: Use `perplexity` MCP with query like "GitKraken 2025 pricing plans" or `firecrawl` to fetch pricing pages directly
> - **License Changes**: Use `ref` MCP to check official vendor documentation for licensing updates
> - **Platform Availability**: Use `web_search` to verify tool availability on specific platforms or regions
