---
name: codespaces
description: Create, manage, and optimize GitHub Codespaces cloud development environments. Configure devcontainers, manage resources, and streamline cloud-based development. Use when setting up cloud development environments, configuring devcontainers, or managing Codespaces. Triggers on codespace, devcontainer, cloud IDE, remote development, development environment, container development.
---

# GitHub Codespaces

Cloud development environments that work anywhere.

## Prerequisites

- **GitHub Account**: With Codespaces access
- **gh CLI**: Install from https://cli.github.com/
- **Authentication**: Run `gh auth login`

## Quick Reference

### Core Commands

| Action | Command |
|--------|---------|
| Create codespace | `gh codespace create -r owner/repo` |
| List codespaces | `gh codespace list` |
| Open in VS Code | `gh codespace code -c <name>` |
| Open in browser | `gh codespace view -c <name> -w` |
| SSH into codespace | `gh codespace ssh -c <name>` |
| Stop codespace | `gh codespace stop -c <name>` |
| Delete codespace | `gh codespace delete -c <name>` |

### Machine Types

| Type | vCPUs | RAM | Storage | Best For |
|------|-------|-----|---------|----------|
| Basic | 2 | 8GB | 32GB | Simple projects, docs |
| Standard | 4 | 16GB | 32GB | Most development |
| Large | 8 | 32GB | 64GB | Full-stack, multiple services |
| XL | 16 | 64GB | 128GB | Data science, ML |
| GPU | 4+ | 16GB+ | 64GB+ | ML training, CUDA |

## DevContainer Configuration

### Directory Structure

```
.devcontainer/
+-- devcontainer.json           # Default configuration
+-- web-frontend/
|   +-- devcontainer.json       # Frontend-specific
+-- backend-api/
|   +-- devcontainer.json       # Backend-specific
+-- data-science/
    +-- devcontainer.json       # Data science config
```

### Basic devcontainer.json

```json
{
  "name": "Project Dev Environment",
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {},
    "ghcr.io/devcontainers/features/python:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "ms-python.python"
      ]
    }
  },
  "postCreateCommand": "npm install",
  "forwardPorts": [3000, 5000]
}
```

## Lifecycle Scripts

### postCreateCommand
Runs once when container is created:
```json
"postCreateCommand": "npm install && npm run setup"
```

### postStartCommand
Runs every time codespace starts:
```json
"postStartCommand": "npm run dev:services"
```

### postAttachCommand
Runs when VS Code attaches:
```json
"postAttachCommand": "echo 'Welcome! Run npm start to begin.'"
```

## Secrets Management

### Setting Secrets

```bash
# For a specific repo
gh secret set API_KEY --repo owner/repo

# For Codespaces specifically
gh secret set DB_PASSWORD --app codespaces

# For user (all Codespaces)
gh secret set NPM_TOKEN --user
```

### Using Secrets in devcontainer.json

```json
{
  "containerEnv": {
    "DATABASE_URL": "${localEnv:DATABASE_URL}"
  },
  "secrets": {
    "API_KEY": {
      "description": "API key for external service"
    }
  }
}
```

## Port Forwarding

### Automatic Forwarding

```json
{
  "forwardPorts": [3000, 5000, 8080],
  "portsAttributes": {
    "3000": {
      "label": "Frontend",
      "onAutoForward": "openBrowser"
    },
    "5000": {
      "label": "API",
      "onAutoForward": "notify"
    }
  }
}
```

### Manual Forwarding

```bash
gh codespace ports forward 3000:3000 -c <codespace-name>
```

## Common Workflows

### Quick Start New Feature

```bash
# Create codespace for feature branch
gh codespace create -r owner/repo -b feature-branch -m standardLinux

# Open in VS Code
gh codespace code
```

### PR Review in Codespace

```bash
# Create codespace from PR
gh codespace create -r owner/repo --branch pr-branch

# Or use the PR directly
gh pr checkout 123
gh codespace create
```

### Share Environment

```bash
# Export port with visibility
gh codespace ports visibility 3000:public -c <name>

# Get shareable URL
gh codespace ports -c <name>
```

## Performance Optimization

### Prebuilds

Enable prebuilds for faster startup:

```json
// .github/codespaces/prebuild.json
{
  "triggers": {
    "branches": ["main", "develop"],
    "paths": ["package.json", ".devcontainer/**"]
  }
}
```

### Dotfiles Repository

Configure personal dotfiles in GitHub Settings > Codespaces.

## Cost Management

### Auto-stop Settings

Configure in GitHub Settings > Codespaces:
- Default idle timeout: 30 minutes
- Retention period: 7 days

### Best Practices

1. **Stop when not in use**: `gh codespace stop`
2. **Delete completed work**: `gh codespace delete`
3. **Use appropriate machine size**: Don't over-provision
4. **Enable prebuilds**: Faster startup, less billing

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow startup | Enable prebuilds |
| Out of storage | Delete unused files, increase disk |
| Extension not working | Check devcontainer extensions config |
| Port not accessible | Check forwardPorts configuration |
| Environment variables missing | Verify secrets are set |

## When to Use This Skill

- Setting up cloud development environments
- Configuring devcontainers for team consistency
- Managing Codespaces via CLI
- Optimizing development environment performance
- Sharing development environments
- PR reviews in isolated environments
