---
name: setup
description: Complete guide to installing Git and performing basic configuration across all platforms (Windows, macOS, Linux, WSL). Use when setting up Git for the first time, installing Git on new systems, configuring user identity, setting default branch, choosing editor, verifying installation, or troubleshooting Git installation issues. Covers platform-specific installation methods, basic required configuration, and verification steps.
allowed-tools: Read, Bash, Glob, Grep
---

# Git Setup

Complete guidance for installing Git and performing essential initial configuration across Windows, macOS, Linux, and WSL environments.

## Table of Contents

- [Quick Start](#quick-start) - Windows, macOS, Linux
- [Platform Detection](#platform-detection) - Identify your platform
- [Installation Guides](#windows-installation) - Windows, macOS, Linux, WSL
- [Basic Configuration](#basic-configuration-all-platforms) - User identity, default branch, editor
- [Verification](#verification) - Test your Git installation
- [Configuration Files](#configuration-file-locations) - Where Git stores settings
- [Reference Loading](#reference-loading-guide) - How references are loaded
- [Next Steps](#next-steps) - Advanced configuration with other skills

## Overview

This skill helps you:

- Install Git using the best method for your platform
- Configure essential Git settings (user identity, default branch, editor)
- Verify your installation is working correctly
- Understand platform-specific considerations
- Get started quickly with recommended defaults

**For advanced configuration** (aliases, performance tuning, credential management, maintenance), see the **git-config** skill.

## When to Use This Skill

Use this skill when:

- Installing Git on a new development machine
- Setting up Git for the first time on any platform
- Configuring user identity and basic Git settings
- Verifying Git installation is working correctly
- Troubleshooting Git installation issues
- Understanding platform-specific Git installation options
- Setting up Git on Windows, macOS, Linux, or WSL

## Quick Start

**Fastest path to getting Git installed and configured:**

### Windows

```powershell
# Install Git
winget install --id Git.Git -e --source winget

# Configure identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main

# Verify
git --version
```

### macOS

```bash
# Install Git
brew install git

# Configure identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main

# Verify
git --version
```

### Linux

```bash
# Install Git (Ubuntu/Debian)
sudo apt update && sudo apt install git

# Configure identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main

# Verify
git --version
```

---

## Platform Detection

When helping users with Git installation, detect their platform using environment indicators:

- **Windows**: `$env:OS` contains "Windows", PowerShell commands, `winget`, file paths like `C:\`
- **macOS**: `uname -s` returns "Darwin", Homebrew (`brew`), `~/.zshrc`
- **Linux**: `uname -s` returns "Linux", package managers (`apt`, `dnf`, `pacman`), `~/.bashrc`
- **WSL**: Linux kernel + Windows integration (e.g., `/mnt/c/`), `wsl.exe` available

Provide platform-specific guidance automatically based on detected or stated platform.

---

## Windows Installation

Two installation options: **Git for Windows Installer** (full control, recommended) or **winget** (quick install). Includes Windows-specific configuration (long paths, system-level settings) and troubleshooting.

📚 **Full guide:** [references/install-windows.md](references/install-windows.md)

Topics covered: Installation options, verification, Windows-specific configuration, Win32 long paths, troubleshooting, Git Bash history issues

---

## macOS Installation

Two installation options: **Xcode Command Line Tools** (quick, built-in) or **Homebrew** (latest version, recommended). Includes macOS-specific configuration, shell integration (Zsh/Bash), and global gitignore setup.

📚 **Full guide:** [references/install-macos.md](references/install-macos.md)

Topics covered: Installation options, verification, line ending configuration, Zsh/Bash shell integration, global gitignore

---

## Linux Installation

Installation via package manager: **apt** (Ubuntu/Debian), **dnf** (Fedora/RHEL), or **pacman** (Arch Linux). Includes Linux-specific configuration, shell integration (Bash/Zsh), and global gitignore setup.

📚 **Full guide:** [references/install-linux.md](references/install-linux.md)

Topics covered: Distribution-specific installation, verification, line ending configuration, Bash/Zsh shell integration, global gitignore

---

## WSL (Windows Subsystem for Linux)

WSL runs Linux (Ubuntu by default), so Git installation is identical to native Linux. Includes WSL-specific configuration and performance considerations.

📚 **Full guide:** [references/install-wsl.md](references/install-wsl.md)

Topics covered: Installation (same as Linux), verification, WSL-specific configuration, filesystem performance notes, Windows integration, credential sharing

---

## Basic Configuration (All Platforms)

After installing Git, configure these essential settings:

### Set User Identity (Required)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Important**: This information is included in every commit. Use your real name and work/personal email.

### Set Default Branch Name

```bash
git config --global init.defaultBranch main
```

**Note**: Modern standard is `main` (replacing older `master` convention).

### Set Preferred Editor (Optional)

Choose one:

```bash
# VS Code (must be in PATH)
git config --global core.editor "code --wait"

# Notepad (Windows)
git config --global core.editor "notepad"

# Vim
git config --global core.editor "vim"

# Nano (Linux/macOS)
git config --global core.editor "nano"
```

**Note**: If not set, Git uses system default editor (usually Vim on Linux/macOS, Notepad on Windows).

---

## Verification

After installation and configuration, verify everything is working:

### Check Git Version

```bash
git --version
```

### Verify Configuration

```bash
# View all configuration with source files
git config --list --show-origin

# View specific values
git config user.name
git config user.email
git config init.defaultBranch
```

### Test Basic Git Operations

```bash
# Create test repository
mkdir test-repo
cd test-repo
git init

# Create and commit a file
echo "# Test Repository" > README.md
git add README.md
git commit -m "Initial commit"

# View commit history
git log

# Clean up
cd ..
rm -rf test-repo
```

**Expected result**: Repository created, commit successful, log shows your commit.

---

## Configuration File Locations

For comprehensive details on configuration file locations, hierarchy, conditional includes, and troubleshooting, see [Configuration Details](references/configuration-details.md).

**Quick reference:**

- **System**: `/etc/gitconfig` (all users, requires sudo)
- **Global**: `~/.config/git/config` or `~/.gitconfig` (current user)
- **Local**: `.git/config` (current repository)
- **Hierarchy**: Local > Global > System

---

## Unsetting Config Values

To remove/unset a config value:

```bash
# Unset system config value (requires admin/sudo)
git config --system --unset status.aheadbehind

# Unset global/user config value
git config --global --unset status.aheadbehind

# Unset local config value (inside a repo)
git config --unset status.aheadbehind
```

---

## Reference Loading Guide

All references in this skill are **conditionally loaded** based on platform detection or troubleshooting context. This progressive disclosure strategy keeps the skill efficient by loading only relevant content when needed.

### Always Load (Core)

- None - all references are contextual and loaded on-demand

### Conditional Load

- `references/install-windows.md` - Load when user is on Windows platform (install workflow)
- `references/install-macos.md` - Load when user is on macOS platform (install workflow)
- `references/install-linux.md` - Load when user is on Linux platform (install workflow)
- `references/install-wsl.md` - Load when user is on WSL platform (install workflow)
- `references/git-bash-history-troubleshooting.md` - Load when troubleshooting Git Bash command history issues on Windows Terminal

**Token efficiency**: Most users follow the Quick Start path (~3k tokens). Platform-specific deep dives load only the relevant reference (~3.5-4k tokens total).

---

## Next Steps

After completing basic Git setup, consider:

1. **Advanced Configuration**: Use the **git-config** skill for:
   - Comprehensive global configuration (performance, aliases, maintenance)
   - Credential management (GitHub CLI, Windows Credential Manager)
   - Clone shortcuts (save typing for common repos)

2. **Line Ending Management**: Use the **line-endings** skill for:
   - Understanding line ending configuration
   - Setting up `.gitattributes` for cross-platform teams
   - Troubleshooting line ending issues
   - Git LFS setup for large files

3. **Commit Signing**: Use the **gpg-signing** skill for:
   - Setting up GPG commit signing
   - Generating and managing GPG keys
   - Adding GPG keys to GitHub/GitLab
   - Troubleshooting signing issues

4. **GUI Tools**: Use the **gui-tools** skill for:
   - Installing Git GUI clients (GitKraken, Sourcetree, GitHub Desktop)
   - Configuring GUI tools
   - Choosing the right GUI for your workflow

---

## Related Skills

- **config**: Comprehensive Git configuration (aliases, performance, credentials, maintenance)
- **line-endings**: Line ending configuration, `.gitattributes`, Git LFS
- **gpg-signing**: GPG commit signing setup and troubleshooting
- **gui-tools**: Git GUI client installation and configuration

---

## Testing and Evaluations

For comprehensive test scenarios, multi-model testing notes, formal evaluations, and development methodology, see [Testing and Evaluations](references/testing-evaluations.md).

**Evaluation Summary**: 3/3 evaluations passed - Tested with Claude Sonnet 4.5 and Claude Sonnet 3.5

---

## References

**Installation Guides:**

- [Windows Installation](references/install-windows.md) - winget, Git for Windows installer, Win32 long paths
- [macOS Installation](references/install-macos.md) - Xcode Command Line Tools, Homebrew, Zsh integration
- [Linux Installation](references/install-linux.md) - apt, dnf, pacman, Bash/Zsh integration
- [WSL Installation](references/install-wsl.md) - Same as Linux, WSL2 performance, credential sharing

**Configuration:**

- [Configuration Details](references/configuration-details.md) - File locations, hierarchy, conditional includes, troubleshooting

**Troubleshooting:**

- [Git Bash History Troubleshooting](references/git-bash-history-troubleshooting.md) - Windows Terminal command history issues

**Testing:**

- [Testing and Evaluations](references/testing-evaluations.md) - Test scenarios, multi-model testing, formal evaluations

---

## Version History

- v1.3.0 (2025-11-28): Token optimization - extracted configuration details and testing to references/, reduced SKILL.md from 526 to ~400 lines
- v1.2.0 (2025-11-25): Comprehensive audit improvements - enhanced WSL reference, updated Git versions to 2.47.0+
- v1.1.0 (2025-01-11): Added Windows Terminal Git Bash command history troubleshooting reference
- v1.0.0 (2025-01-06): Initial release with comprehensive Git installation and configuration guidance

---

## Official Documentation

- [Git Official Site](https://git-scm.com/)
- [Git for Windows](https://git-scm.com/install/windows)
- [Getting Started - First-Time Git Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
- [Git Configuration Documentation](https://git-scm.com/docs/git-config)

---

## Last Updated

**Date:** 2025-11-28
**Model:** claude-opus-4-5-20251101
