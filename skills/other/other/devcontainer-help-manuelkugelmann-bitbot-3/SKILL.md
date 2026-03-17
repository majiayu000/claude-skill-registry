---
name: devcontainer-help
description: Help users customize devcontainers by adding packages, extensions, features, and settings. Use when users ask about adding tools, languages, or configuring their development environment. Focus on practical devcontainer customization, not BitBot internals.
---

# DevContainer Customization Helper

This skill helps users customize their devcontainer by providing examples and guidance for common tasks.

## Common Customization Patterns

### Adding Packages to Dockerfile

```dockerfile
RUN apt-get update && apt-get install -y \
    package-name \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
```

### Adding VS Code Extensions

```json
{
  "customizations": {
    "vscode": {
      "extensions": ["publisher.extension-name"]
    }
  }
}
```

### Adding DevContainer Features

```json
{
  "features": {
    "ghcr.io/devcontainers/features/feature-name:version": {}
  }
}
```

### Setting Environment Variables

```json
{
  "remoteEnv": {
    "VAR_NAME": "value"
  }
}
```

## Language-Specific Examples

### Python Development
- Feature: `ghcr.io/devcontainers/features/python:1`
- Extensions: `ms-python.python`, `ms-python.vscode-pylance`
- Tools: `python3-pip`, `python3-venv`

### Node.js Development
- Feature: `ghcr.io/devcontainers/features/node:1`
- Extensions: `dbaeumer.vscode-eslint`, `esbenp.prettier-vscode`
- Tools: npm, yarn, pnpm

### Database Tools
- PostgreSQL: `ghcr.io/devcontainers/features/postgres:1`
- Extensions: `ms-ossdata.vscode-postgresql`

### Docker-in-Docker
- Feature: `ghcr.io/devcontainers/features/docker-in-docker:2`

## When to Use This Skill

- User asks "how do I add Python to my devcontainer?"
- User wants to install a specific tool or language
- User needs help with VS Code extensions
- User wants to set up databases or services
- User asks about devcontainer configuration

## What NOT to Explain

- BitBot's internal template merging system
- How BitBot copies files during init
- Container orchestration internals
- SPARC methodology or BitBot development

## Focus

Help users accomplish their customization goals with practical, working examples that follow devcontainer standards.
