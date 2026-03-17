---
name: git-config
description: Comprehensive Git configuration guide covering global settings, aliases, performance tuning, credential management, maintenance, .gitattributes, clone shortcuts, and troubleshooting. Use when configuring Git beyond basic setup, optimizing Git performance, setting up aliases, managing credentials (GitHub CLI, Windows Credential Manager), configuring line ending strategy, setting up .gitattributes, enabling Git maintenance, or troubleshooting configuration issues. Cross-platform guidance for Windows, macOS, and Linux.
allowed-tools: Read, Bash, Glob, Grep
---

# Git Configuration

Comprehensive guidance for configuring Git beyond basic installation. This skill covers global configuration, performance optimization, aliases, credential management, maintenance, and advanced configuration topics.

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use-this-skill)
- [Quick Start](#quick-start)
- [Configuration Files](#configuration-file-locations)
- [Global Settings](#global-configuration-settings)
- [Rerere](#managing-rerere-reuse-recorded-resolution)
- [Line Endings](#line-ending-strategy-defense-in-depth)
- [Aliases](#aliases)
- [Clone Shortcuts](#clone-shortcuts)
- [Repository-Level Config](#repository-level-configuration)
- [Maintenance](#maintenance)
- [Git Attributes](#git-attributes)
- [Credentials](#git-credential-management)
- [Troubleshooting](#troubleshooting)
- [Test Scenarios](#test-scenarios)

## Overview

This skill helps you:

- Configure Git globally for optimal performance and workflow
- Set up powerful aliases to streamline common operations
- Manage Git credentials securely (GitHub CLI, Windows Credential Manager)
- Configure `.gitattributes` for line ending control
- Enable Git maintenance for better repository performance
- Understand repository-level vs global configuration
- Troubleshoot common configuration issues

**For basic Git installation and setup**, see the **setup** skill.

## Example Use Cases

This skill activates for questions like:

- "How do I set up Git aliases for common operations?"
- "Configure Git to use GitHub CLI for authentication"
- "My Git is slow on large repos - how can I optimize performance?"
- "Set up .gitattributes for cross-platform development"
- "Enable Git background maintenance"
- "Troubleshoot 'refusing to allow OAuth App to create workflow' error"
- "Configure Git credential helpers on Windows"
- "Set up clone shortcuts for frequently-used repositories"
- "Configure rerere to remember merge conflict resolutions"

## When to Use This Skill

Use this skill when:

- Configuring Git beyond basic user identity
- Setting up aliases for common Git operations
- Optimizing Git performance (fsmonitor, untrackedCache, parallel operations)
- Managing Git credentials (HTTPS, SSH, token scopes)
- Setting up GitHub CLI as credential helper
- Configuring `.gitattributes` for cross-platform line ending control
- Enabling Git background maintenance
- Setting up clone shortcuts for frequently-used repositories
- Troubleshooting credential issues or line ending errors
- Understanding Git configuration hierarchy (system/global/local)

## Quick Start

**Most impactful configuration settings to apply immediately:**

```bash
# Performance improvements
git config --global core.fsmonitor true
git config --global core.untrackedCache true
git config --global fetch.parallel 8
git config --global checkout.workers 8

# Better pull/rebase workflow
git config --global pull.rebase true
git config --global rebase.autoStash true
git config --global rebase.updateRefs true

# Auto-prune deleted remote branches
git config --global fetch.prune true
git config --global fetch.pruneTags true

# Better merge conflict resolution
git config --global merge.conflictstyle zdiff3

# Auto-setup remote tracking on first push
git config --global push.autoSetupRemote true

# Better diff algorithm
git config --global diff.algorithm histogram
git config --global diff.colorMoved zebra

# Line ending safety check
git config --global core.safecrlf warn
```

---

## Quick Reference

Common Git configuration settings organized by category for quick lookup (performance, pull/rebase, fetch, push, diff, merge, line endings, sorting, maintenance).

**📚 Complete Quick Reference Table:** [references/quick-reference.md](references/quick-reference.md)

The quick reference table provides copy-paste commands for all common settings with category organization and purpose explanations.

---

## Configuration File Locations

For detailed information about Git configuration file locations, hierarchy, and viewing configuration, see [references/configuration-basics.md](references/configuration-basics.md).

**Quick summary:**

- **System**: `/etc/gitconfig` (or Git install dir on Windows) - All users
- **Global**: `~/.gitconfig` or `~/.config/git/config` - Current user
- **Local**: `.git/config` - Single repository only
- **Priority**: Local > Global > System

**View configuration:**

```bash
# View all configuration with source files
git config --list --show-origin

# View specific value
git config user.name
```

---

## Global Configuration Settings

These settings are cross-platform and recommended for all users. They should be set at the **global** level unless you need repository-specific overrides.

**Most Essential Settings (Quick Start):**

```bash
# Pull & rebase (cleaner history)
git config --global pull.rebase true
git config --global rebase.autoStash true

# Fetch (auto-prune deleted branches/tags)
git config --global fetch.prune true
git config --global fetch.pruneTags true
git config --global fetch.parallel 8

# Push (auto-setup remote tracking)
git config --global push.autoSetupRemote true

# Diff & merge (better algorithms and conflict display)
git config --global diff.algorithm histogram
git config --global diff.colorMoved zebra
git config --global merge.conflictstyle zdiff3

# Performance (filesystem monitoring)
git config --global core.fsmonitor true
git config --global core.untrackedCache true

# Sorting (newest first)
git config --global branch.sort -committerdate
git config --global tag.sort -taggerdate
```

**📚 Complete Global Configuration Guide:** [references/global-configuration.md](references/global-configuration.md)

Topics covered: Pull & rebase strategy, fetch strategy, push strategy, checkout/switch strategy, commit settings, status settings, diff settings, merge settings, rerere (conflict resolution memory), color settings, sorting, log settings, performance settings, submodule strategy, miscellaneous settings, and advanced configuration options.

---

## Managing rerere (Reuse Recorded Resolution)

Git's rerere feature remembers how you resolved merge conflicts and can reapply those resolutions automatically.

**Enable rerere:**

```bash
git config --global rerere.enabled true
git config --global rerere.autoUpdate true
```

**For detailed information about how rerere works, safety considerations, and management commands**, see [references/configuration-basics.md](references/configuration-basics.md#managing-rerere-reuse-recorded-resolution)

## Line Ending Strategy (Defense in Depth)

**Cross-platform line ending management uses a layered approach:**

1. **System level (autocrlf)**: Platform-specific default (Windows: `true`, macOS/Linux: `input`)
2. **Global level (safecrlf)**: Warns about MIXED endings (actual problems) but allows legitimate conversions
3. **Repository level (.gitattributes)**: Explicit control per file type

**Defense in depth:** These settings are **complementary, not conflicting**:

- `autocrlf` handles the conversion automatically
- `safecrlf=warn` warns about PROBLEMS (mixed line endings) but doesn't block .gitattributes conversions
- `.gitattributes` provides per-repo fine-grained control

**Important:** Don't use `safecrlf=true` when you have `.gitattributes` - it will block legitimate conversions and cause constant errors!

**Platform-specific autocrlf settings:**

- **Windows**: `git config --global core.autocrlf true` (converts LF→CRLF on checkout, CRLF→LF on commit)
- **macOS/Linux**: `git config --global core.autocrlf input` (converts CRLF→LF on commit, no conversion on checkout)
- **WSL**: `git config --global core.autocrlf input` (same as Linux)

**Global safecrlf setting (all platforms):**

```bash
# Warn about mixed line endings (safeguard against problems)
# Use 'warn' not 'true' - allows .gitattributes to work without constant errors
git config --global core.safecrlf warn
```

**For detailed .gitattributes setup and comprehensive line ending guidance**, see the **line-endings** skill.

---

## Aliases

Aliases provide shortcuts for common Git operations. Categories include: information & inspection, navigation, branch operations, staging/unstaging, committing, history editing, remote operations, and tag pushing workflows.

**Most Common Aliases:**

```bash
# Status and branch info
git config --global alias.st "status -sb"
git config --global alias.br "branch -vv"

# Modern branch switching
git config --global alias.co "switch"
git config --global alias.cob "switch -c"

# Quick amend
git config --global alias.amend "commit --amend --no-edit"

# Safe force push
git config --global alias.pfwl "push --force-with-lease"
```

**📚 Complete Alias Guide:** [references/aliases.md](references/aliases.md)

Topics covered: Information & inspection aliases, navigation utilities, branch operations, staging/unstaging shortcuts, committing helpers, history editing (DANGER!), remote operations, tag pushing workflows, clone shortcuts with `url.insteadOf`, organization/personal shorthand patterns, and customization templates.

---

## Clone Shortcuts

Git's `url.insteadOf` feature creates shorthand prefixes for clone URLs. Example: `git clone gh:username/repo` instead of `git clone git@github.com:username/repo.git`.

**Quick Example:**

```bash
# Universal GitHub shorthand
git config --global url."git@github.com:".insteadOf "gh:"
# Usage: git clone gh:microsoft/vscode
```

**📚 Complete Clone Shortcuts Guide:** [references/aliases.md#clone-shortcuts](references/aliases.md#clone-shortcuts)

Topics covered: Universal GitHub shorthand, organization/personal shortcuts, corporate Git servers, custom namespace templates, and usage examples.

---

## Repository-Level Configuration

**These settings are context-specific** - use them in individual repos when needed, NOT as global defaults.

**When to use repo-level config:**

- Repo-specific requirements (submodules, performance, size)
- Overriding global settings for specific workflows
- Team-specific conventions for that repository

**Examples:**

```bash
# Enable submodule recursion in a specific repo
git config submodule.recurse true

# Disable ahead/behind in a massive repo (performance)
git config status.aheadBehind false

# Override line ending strategy (with .gitattributes)
git config core.autocrlf false
```

---

## Maintenance

Git can perform background maintenance to keep repositories fast (commit-graph updates, incremental repacking, loose object cleanup).

**Quick Setup:**

```bash
# Enable background maintenance once for your account
git maintenance start

# Register each active repo for maintenance
git maintenance register

# Enable commit-graph generation globally
git config --global gc.writeCommitGraph true
```

**Common Commands:**

```bash
# Run maintenance now
git maintenance run

# See which repos are registered
git config --global --get-all maintenance.repo

# Unregister a repo
git maintenance unregister
```

**📚 Complete Maintenance Guide:** [references/global-configuration.md#maintenance](references/global-configuration.md#maintenance)

Topics covered: Background maintenance tasks, scheduling (hourly/daily/weekly), task configuration, disabling full gc, maintenance.auto setting, per-task enablement, troubleshooting maintenance issues.

---

## Git Attributes

`.gitattributes` provides explicit control over line endings per file type. This is the recommended approach for cross-platform teams.

**Best practice:** Control endings in `.gitattributes` and use platform-appropriate `autocrlf` settings with `safecrlf=warn`.

**Quick Example:**

```gitattributes
# Auto-detect text files and normalize line endings
* text=auto

# Force LF for scripts/config (shell and CI tools expect LF)
*.sh      text eol=lf
*.yml     text eol=lf
*.json    text eol=lf

# Force CRLF for Windows-specific files
*.ps1     text eol=crlf
*.cmd     text eol=crlf
*.bat     text eol=crlf

# Mark binaries
*.png binary
*.jpg binary
*.pdf binary
```

**Normalize existing repos with mixed endings:**

```bash
git add --renormalize .
git commit -m "Normalize line endings"
```

**📚 For comprehensive .gitattributes setup, Git LFS patterns, and line ending strategy**, see the **line-endings** skill.

---

## Git Credential Management

Git uses credential helpers to store and retrieve authentication credentials for remote operations (clone, fetch, push). Understanding credential management is essential for secure, efficient Git workflows.

**For comprehensive credential management guidance**, see [references/credential-management.md](references/credential-management.md).

**Quick overview:**

- **Windows**: Default credential helper is Windows Credential Manager (`manager`)
- **macOS**: Default is macOS Keychain (`osxkeychain`)
- **Linux**: Default is memory cache (`cache`) or `libsecret` for persistent storage
- **GitHub users**: Hybrid setup recommended (gh CLI for GitHub, OS credential manager for others)

**Quick setup for GitHub (hybrid approach):**

```bash
# 1. Authenticate with gh CLI
gh auth login --scopes "repo,read:org,workflow" --git-protocol https

# 2. Configure gh CLI as credential helper for GitHub only
gh auth setup-git

# 3. Verify hybrid setup
git config --list | grep credential
# Should show:
# - credential.helper=manager (or osxkeychain/cache - OS default)
# - credential.https://github.com.helper=!gh auth git-credential (GitHub-specific)
```

**Common credential issues:**

- "refusing to allow OAuth App to create or update workflow" → Need `workflow` scope
- Git still uses old/wrong credentials → Clear OS credential cache
- SSH vs HTTPS confusion → Check remote URL with `git remote -v`

For detailed troubleshooting, credential helper options, security best practices, and platform-specific guidance, see [references/credential-management.md](references/credential-management.md).

---

## Troubleshooting

For comprehensive troubleshooting guidance, see [references/troubleshooting.md](references/troubleshooting.md).

**Quick links:**

- [Line Ending Errors](references/troubleshooting.md#line-ending-errors) - "LF would be replaced by CRLF" warnings
- [Credential Issues](references/troubleshooting.md#credential-issues) - OAuth errors, stale credentials, SSH vs HTTPS
- [Performance Problems](references/troubleshooting.md#performance-problems) - Slow git status, fetch timeouts
- [Common Real-World Scenarios](references/troubleshooting.md#common-real-world-scenarios) - Corporate proxies, WSL issues, rerere problems

---

## Related Skills

- **setup**: Basic Git installation and initial configuration
- **line-endings**: Comprehensive line ending configuration, `.gitattributes`, Git LFS
- **gpg-signing**: GPG commit signing setup and troubleshooting
- **gui-tools**: Git GUI client installation and configuration

---

## Test Scenarios

For test scenarios validating skill activation and response quality, see [references/test-scenarios.md](references/test-scenarios.md).

**Coverage:** 9 scenarios covering basic use (aliases, performance, maintenance), advanced use (credentials, line endings, repo config), troubleshooting (credential issues, rerere), and shortcuts (clone shortcuts, url.insteadOf).

---

## Version History

- v1.3.0 (2025-11-25): Audit compliance improvements
  - Extracted Test Scenarios to references/test-scenarios.md
  - Reduced SKILL.md from 539 to ~475 lines (under 500-line recommendation)
  - Improved progressive disclosure compliance
- v1.2.0 (2025-11-12): Quality improvements based on audit recommendations
  - Extracted Configuration File Locations to references/configuration-basics.md
  - Extracted Managing rerere to references/configuration-basics.md
  - Extracted Troubleshooting to references/troubleshooting.md
  - Added multi-model testing notes
  - Added common real-world usage scenarios
  - Reduced SKILL.md line count from 959 to ~700 lines (improved performance)
  - Added tables of contents to all reference files for better navigation
  - Created references/troubleshooting.md with comprehensive troubleshooting guidance
- v1.1.0 (2025-11-12): Usability enhancements based on audit feedback
  - Added Example Use Cases section with concrete activation examples
  - Added Quick Reference Table for quick lookup of common settings
  - Improved autonomous activation reliability
- v1.0.0 (2025-11-09): Initial release with comprehensive Git configuration guidance

---

## Official Documentation

- [Git Configuration Documentation](https://git-scm.com/docs/git-config)
- [Git Attributes Documentation](https://git-scm.com/docs/gitattributes)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Git Credential Helpers](https://git-scm.com/docs/gitcredentials)
- [Git Maintenance](https://git-scm.com/docs/git-maintenance)

---

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101
