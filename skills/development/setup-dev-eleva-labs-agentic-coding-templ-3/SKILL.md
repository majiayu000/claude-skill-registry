---
name: setup-dev
description: >-
  Set up the complete development environment for the mobile app.
  Use when onboarding, setting up a new machine, or troubleshooting
  environment issues.
  Invoked by: "setup", "dev setup", "environment setup", "install dependencies".
---

# Development Environment Setup SOP

> **Note**: This is a template. Replace placeholders like `{PROJECT_NAME}`, `{REPO_DIRECTORY}`, and `{BUNDLE_ID}` with your actual project values.

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

---

## Overview

### Purpose
This SOP guides developers through setting up the complete development environment for the mobile app. It ensures consistent environments across the team and enables productive development from day one.

### When to Use
**ALWAYS**: New developer onboarding, setting up a new machine, clean reinstall, troubleshooting environment issues
**SKIP**: Already have working environment, only need platform-specific setup (use `setup-ios` or `setup-android`)

---

## Process Workflow

### Flow Diagram
```
[Prerequisites] --> [Automated Setup] --> [Verification] --> [First Run]
```

### Phase Summary
| Phase | Objective | Deliverable |
|-------|-----------|-------------|
| 1. Prerequisites | Ensure required tools installed | macOS, Xcode, Command Line Tools |
| 2. Setup | Install development tools | Volta, Node.js 20, pnpm, dependencies |
| 3. Verification | Confirm environment works | `task check-prereqs` passes |
| 4. First Run | Run the app | App running in simulator |

---

## Quick Start

### Option 1: Fully Automated Setup (5 minutes)

```bash
# Clone the repository
git clone <repository-url>
cd {REPO_DIRECTORY}

# Run automated setup (installs everything)
./scripts/setup-development.sh
```

The script handles:
- Volta installation
- Node.js 20 setup
- Project dependency installation
- Development environment configuration

### Option 2: Manual Setup (10 minutes)

```bash
# 1. Install Volta
curl https://get.volta.sh | bash

# 2. Restart terminal, then setup Node
volta install node@20
volta pin node@20

# 3. Install dependencies
pnpm install

# 4. Setup development environment
task setup-dev

# 5. Verify setup
task check-prereqs
```

### Option 3: One-Command Full Setup (Fastest)

If you already have the repository cloned and just need to complete setup:

```bash
task setup-full
```

This does everything in one command:
1. Install all dependencies (`pnpm install`)
2. Create local environment config (`.env.local`)
3. Pull development settings from EAS
4. Verify all patches applied correctly

---

## Detailed Guide

For comprehensive setup instructions including prerequisites and troubleshooting, see:
- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Detailed setup steps

---

## Quick Reference

### Common Commands
```bash
# Verify environment
task check-prereqs

# Start iOS development
task run-ios

# Start Android development
task run-android

# Run tests
task test

# Clean and regenerate
task clean && task generate
```

### Local Environment Setup

```bash
task setup-local-env    # Creates .env.local
task verify-patches     # Check patches are applied
task setup-full         # Complete setup in one command
```

### Key Environment Variables
```bash
# Check Node version (should be v20.x.x)
node --version

# Check Volta version
volta --version

# Check pnpm version
pnpm --version
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Volta not found after install | Restart terminal or source shell config |
| Wrong Node version | Run `volta pin node@20` in project directory |
| pnpm not found | Install via `volta install pnpm` |
| Metro bundler errors | Run `task clean-cache` |
| iOS build fails | See `setup-ios` skill or [SETUP_GUIDE.md](./SETUP_GUIDE.md) |
| Android build fails | See `setup-android` skill or [SETUP_GUIDE.md](./SETUP_GUIDE.md) |
| `.env.local` missing | Run `task setup-local-env` |
| SIMULATOR variable undefined | Run `task setup-local-env` to recreate `.env.local` |

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/setup-env` | Configure environment variables | After initial setup |
| `/setup-ios` | iOS-specific setup | For iOS development |
| `/setup-android` | Android-specific setup | For Android development |
| `/help` | Troubleshooting guide | When encountering issues |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
