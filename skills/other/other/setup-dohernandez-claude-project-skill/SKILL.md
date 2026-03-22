---
name: setup
description: Project setup for ci-core-e2e-runner. Use when onboarding, setting up the repo, or troubleshooting setup issues.
user-invocable: true
allowed-tools: [Read, Bash, Grep, Glob]
---

# Setup

## Purpose

Guide setup of the ci-core-e2e-runner project for local development and contribution. This is a shell/YAML project with GitHub Actions workflows and shell scripts -- no Node.js, no npm, no task runner.

## Prerequisites

| Tool | Version | Install | Verify |
|------|---------|---------|--------|
| Git | Any | `brew install git` | `git --version` |
| GitHub CLI | Any | `brew install gh` | `gh --version` |
| Bash | 4+ | (pre-installed on macOS/Linux) | `bash --version` |

### Optional (for VM provisioning work)

| Tool | Version | Install | Verify |
|------|---------|---------|--------|
| Docker | Any | `brew install --cask docker` | `docker --version` |
| shellcheck | Any | `brew install shellcheck` | `shellcheck --version` |

## Setup Procedure

```
Step 0: (If new) Clone repository
        git clone git@github.com:genlayerlabs/ci-core-e2e-runner.git
        cd ci-core-e2e-runner
        (Skip if you already have the repo)

Step 1: Verify GitHub CLI authentication
        gh auth status
        (If not authenticated: gh auth login)

Step 2: Review project documentation
        Read CLAUDE.md for project overview, architecture, and commands

Step 3: Verify repository structure
        ls .github/workflows/    # Should contain run-e2e.yml
        ls scripts/              # Should contain setup-runner.sh, run-e2e.sh
```

**Quick setup for existing clone:**
```bash
gh auth status && cat CLAUDE.md
```

## Project Structure

This is a minimal project:

| Directory | Contents |
|-----------|----------|
| `.github/workflows/` | GitHub Actions workflow files (run-e2e.yml) |
| `scripts/` | Shell scripts for VM provisioning and E2E orchestration |
| `.claude/skills/` | Claude Code skill definitions |
| `CLAUDE.md` | Project documentation and Claude instructions |

## What This Project Does

ci-core-e2e-runner receives `repository_dispatch` events from target repos (e.g., genlayer-node) and runs the full E2E test pipeline on a self-hosted VM:

1. Clone target repo at the PR branch
2. Deploy network, start WebDriver, run tests
3. Post signed report back to the PR
4. Signal pass/fail via reaction on the trigger comment

## Troubleshooting

### "gh: command not found"
Install GitHub CLI:
```bash
brew install gh
```

### "gh auth status" shows not logged in
Authenticate with GitHub:
```bash
gh auth login
```

### Scripts not executable
```bash
chmod +x scripts/*.sh
```

## Automation
See `skill.yaml` for patterns and procedure.
See `sharp-edges.yaml` for common pitfalls.
