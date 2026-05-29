---
name: onboarding
description: Developer environment setup guides for Windows, macOS, Linux, and WSL. Use when setting up development machines, installing tools, configuring environments, or following platform-specific setup guides. Covers package management, shell/terminal, code editors, AI tooling, containerization, databases, and more.
allowed-tools: Read, Glob, Grep, Bash
---

# Developer Onboarding

Complete developer environment setup guides across all major platforms.

## Overview

This skill provides step-by-step onboarding documentation for setting up:

- **Package managers** (winget, Homebrew, apt, pacman)
- **Runtime environments** (NVM for Node.js)
- **Shell & terminal** (PowerShell, Zsh, Bash customization)
- **Code editors** (VS Code, JetBrains, Neovim)
- **AI tooling** (Claude Code, Cursor, LM Studio, Gemini CLI)
- **Containerization** (Docker setup)
- **Cloud platforms** (Azure CLI)
- **Database tools** (DBeaver, Azure Data Studio)
- **Security tools** (GPG, SSH, Windows Sandbox)
- **Productivity tools** (Figma, various utilities)

## When to Use This Skill

Use this skill when:

- Setting up a new development machine
- Onboarding new developers to a team
- Finding platform-specific installation instructions
- Configuring developer tools across Windows, macOS, Linux, or WSL
- Looking for best practices in environment setup
- Troubleshooting developer tool installations

## Quick Start by Platform

### Windows

Main Guide: [references/windows-onboarding.md](references/windows-onboarding.md)

Follow the ordered steps covering WSL, package management, Git (via git skills), runtime environments, shell configuration, and development tools.

### macOS

Main Guide: [references/macos-onboarding.md](references/macos-onboarding.md)

Follow the ordered steps covering Homebrew, Git (via git skills), runtime environments, shell configuration, and development tools.

### Linux

Main Guide: [references/linux-onboarding.md](references/linux-onboarding.md)

Follow the ordered steps covering package management, Git (via git skills), runtime environments, shell configuration, and development tools.

## Topics Index

| Topic | Windows | macOS | Linux | WSL |
| --- | --- | --- | --- | --- |
| Package Management | [Windows](references/package-management/package-managers-windows.md) | [macOS](references/package-management/package-managers-macos.md) | [Linux](references/package-management/package-managers-linux.md) | - |
| WSL Setup | [Windows](references/wsl/wsl-setup-windows.md) | - | - | - |
| Linux Fundamentals | - | - | [Linux](references/linux-fundamentals/common-commands-linux.md) | [WSL](references/linux-fundamentals/common-commands-wsl.md) |
| Runtime Environments | [Windows](references/runtime-environments/nvm-setup-windows.md) | [macOS](references/runtime-environments/nvm-setup-macos.md) | [Linux](references/runtime-environments/nvm-setup-linux.md) | - |
| PowerShell | [Windows](references/shell-terminal/powershell-setup-windows.md) | [macOS](references/shell-terminal/powershell-setup-macos.md) | [Linux](references/shell-terminal/powershell-setup-linux.md) | - |
| Shell Customization | [Windows](references/shell-terminal/shell-customization-windows.md) | [macOS](references/shell-terminal/shell-customization-macos.md) | [Linux](references/shell-terminal/shell-customization-linux.md) | - |
| Alternative Shells | [Windows](references/shell-terminal/alternative-shells-windows.md) | [macOS](references/shell-terminal/alternative-shells-macos.md) | [Linux](references/shell-terminal/alternative-shells-linux.md) | - |
| Code Editors | [Windows](references/code-editors/code-editors-windows.md) | [macOS](references/code-editors/code-editors-macos.md) | [Linux](references/code-editors/code-editors-linux.md) | - |
| AI Tooling | [Windows](references/ai-tooling/ai-tooling-windows.md) | [macOS](references/ai-tooling/ai-tooling-macos.md) | [Linux](references/ai-tooling/ai-tooling-linux.md) | - |
| Docker | [Windows](references/containerization/docker-setup-windows.md) | [macOS](references/containerization/docker-setup-macos.md) | [Linux](references/containerization/docker-setup-linux.md) | - |
| API Tools | [Windows](references/api-development/api-tools-windows.md) | [macOS](references/api-development/api-tools-macos.md) | [Linux](references/api-development/api-tools-linux.md) | [WSL](references/api-development/api-tools-wsl.md) |
| Web Browsers | [Windows](references/web-browsers/browsers-windows.md) | [macOS](references/web-browsers/browsers-macos.md) | [Linux](references/web-browsers/browsers-linux.md) | - |
| Azure CLI | [Windows](references/cloud-platforms/azure-cli-setup-windows.md) | [macOS](references/cloud-platforms/azure-cli-setup-macos.md) | [Linux](references/cloud-platforms/azure-cli-setup-linux.md) | - |
| Database Tools | [Windows](references/database-tools/database-tools-windows.md) | [macOS](references/database-tools/database-tools-macos.md) | [Linux](references/database-tools/database-tools-linux.md) | - |
| Productivity | [Windows](references/productivity/productivity-tools-windows.md) | [macOS](references/productivity/productivity-tools-macos.md) | [Linux](references/productivity/productivity-tools-linux.md) | - |
| Figma | [Windows](references/productivity/figma-setup-windows.md) | [macOS](references/productivity/figma-setup-macos.md) | [Linux](references/productivity/figma-setup-linux.md) | - |
| Security Tools | [Windows](references/security/security-tools-windows.md) | [macOS](references/security/security-tools-macos.md) | [Linux](references/security/security-tools-linux.md) | - |
| Windows Sandbox | [Windows](references/security/windows-sandbox.md) | - | - | - |
| System Utilities | [Windows](references/system-tools/system-utilities-windows.md) | [macOS](references/system-tools/system-utilities-macos.md) | [Linux](references/system-tools/system-utilities-linux.md) | - |
| Other | [Windows](references/other/other-windows.md) | [macOS](references/other/other-macos.md) | [Linux](references/other/other-linux.md) | - |

## Cross-Platform Content

- [Database Tools Overview](references/database-tools/database-tools.md) - Platform-agnostic database tools guide
- [GitHub Spec Kit](references/ai-tooling/github-spec-kit.md) - AI-assisted specification development

## Git and Version Control

Git documentation has been consolidated into dedicated Claude Code skills for better maintainability:

- **git:setup** skill: Git installation and basic configuration
- **git:line-endings** skill: Cross-platform line ending configuration
- **git:gui-tools** skill: Git GUI client recommendations
- **git:git-config** skill: Comprehensive Git configuration
- **git:gpg-signing** skill: Commit signing setup

Invoke these skills directly for Git-related guidance.

## Platform Detection

When helping users, detect their platform via:

- **Windows**: `$env:OS` contains "Windows", PowerShell, `winget`
- **macOS**: `uname -s` returns "Darwin", `brew`
- **Linux**: `uname -s` returns "Linux", `apt`/`dnf`/`pacman`
- **WSL**: Linux kernel + `/mnt/c/` paths

## Reference Loading Guide

All references are **conditionally loaded** based on detected platform:

1. Load `references/{platform}-onboarding.md` for platform entry point
2. Load topic-specific references as needed from `references/{topic}/`
3. Cross-reference with git skills for version control setup

**Token efficiency**: Entry point + 2-3 topic references is typical load (~200-400 lines)

---

**Last Updated:** 2025-12-01

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
