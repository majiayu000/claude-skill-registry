---
name: worktree-setup-hook
description: "Post-checkout git hook for automatic worktree setup. Use when: (1) Setting up automatic configuration for new git worktrees, (2) Creating post-checkout hooks that detect new worktrees and run setup tasks, (3) Configuring worktrees to automatically copy env files and install dependencies"
---

# Worktree Setup Hook

Provides a post-checkout git hook template that automatically configures new git worktrees by detecting new worktree creation and running setup tasks.

## Overview

The hook detects when a new worktree is created (not a regular checkout) and automatically:
- Copies environment files (.env, .env.local, etc.)
- Detects the project's package manager and installs dependencies
- Runs setup scripts if available

## Quick Start

Install the hook template:

```bash
cp .cursor/skills/worktree-setup-hook/assets/hook-templates/post-checkout .git/hooks/post-checkout
chmod +x .git/hooks/post-checkout
```

The hook will automatically run after `git worktree add` completes.

## How It Works

### Worktree Detection

The hook detects new worktrees by checking if the previous HEAD is the null-ref (`0000000000000000000000000000000000000000`). This is how git indicates a new worktree creation.

### Setup Tasks

1. **Environment Files**: Copies `.env.example` to `.env`, `.env.local.example` to `.env.local`, or copies env files from the main worktree
2. **Package Manager Detection**: Automatically detects and installs dependencies:
   - `package.json` → npm or yarn
   - `requirements.txt` → pip
   - `Cargo.toml` → cargo
   - `go.mod` → go
   - `Gemfile` → bundle
3. **Setup Scripts**: Runs `setup.sh` or `scripts/setup.sh` if present and executable

## Installation

See [setup-guide.md](references/setup-guide.md) for detailed installation instructions, including:
- Step-by-step installation
- Handling existing hooks
- Backup procedures
- Troubleshooting

## Customization

The hook is a standard POSIX shell script. Edit `.git/hooks/post-checkout` to add custom setup steps or modify behavior.

## Resources

- **Hook Template**: `assets/hook-templates/post-checkout` - The main hook script
- **Setup Guide**: `references/setup-guide.md` - Detailed installation and configuration instructions
