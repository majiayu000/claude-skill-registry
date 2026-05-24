---
name: coder-workspace-management
description: Coder CLI commands for workspace management, templates, and platform operations
updated: 2026-01-15
---

# Coder Workspace Management Skill

Comprehensive knowledge of Coder CLI commands for managing workspaces, templates, and the Coder platform. This skill enables you to help users interact with their Coder deployment from the command line.

## What is Coder?

**Coder** is a self-hosted cloud development environment (CDE) platform that allows organizations to provision secure, consistent, and efficient remote development workspaces. Key features:

- **Self-hosted**: Deploy on your own cloud or on-premises infrastructure
- **Terraform-based**: Templates define infrastructure as code
- **Multiple IDEs**: VS Code, JetBrains, Jupyter, and more
- **Kubernetes-native**: Built for scalable containerized environments
- **AI-Ready**: Built-in support for AI coding agents (like Claude Code)

## Core Concepts

| Component | Description | Analogy |
|-----------|-------------|---------|
| **Templates** | Terraform blueprints defining dev environments (OS, tools, resources) | Recipe |
| **Workspaces** | Running environments created from templates | Cooked meal |
| **Users** | Developers who launch and work in workspaces | People eating |
| **Tasks** | AI-powered coding agents running inside workspaces | Smart kitchen appliance |

## Coder CLI Overview

The `coder` CLI is the primary interface for interacting with Coder deployments.

### Basic Usage

```bash
coder [global-flags] <subcommand>
```

### Global Flags

| Flag | Environment Variable | Description |
|------|---------------------|-------------|
| `--url <url>` | `$CODER_URL` | Coder deployment URL |
| `--token <string>` | `$CODER_SESSION_TOKEN` | Authentication token |
| `-v, --verbose` | `$CODER_VERBOSE` | Enable verbose output |
| `--no-version-warning` | `$CODER_NO_VERSION_WARNING` | Suppress version mismatch warnings |
| `--global-config <path>` | `$CODER_CONFIG_DIR` | Config directory (default: `~/.config/coderv2`) |

### Authentication

```bash
# Log in to a Coder deployment
coder login <deployment-url>

# Log out
coder logout

# Check who you are authenticated as
coder whoami
```

## Workspace Commands

### Creating Workspaces

```bash
# Create a workspace from a template
coder create --template="<template-name>" <workspace-name>

# Create with specific parameters
coder create --template="<template-name>" --var="key=value" <workspace-name>

# Create with rich parameters (JSON)
coder create --template="<template-name>" --rich-parameter-file=params.json <workspace-name>
```

**Workspace naming rules:**
- Must start and end with a letter or number
- Only letters, numbers, and hyphens allowed
- 1-32 characters
- Case-insensitive (lowercase recommended)
- Cannot use `new` or `create` as names
- Must be unique within your workspaces

### Listing Workspaces

```bash
# List all workspaces
coder list

# List with filters
coder list owner:me
coder list status:running
coder list template:my-template
coder list owner:me status:running

# Available filters:
# - owner:me or owner:<username>
# - name:<workspace-name>
# - template:<template-name>
# - status:<status> (e.g., running, stopped, failed)
# - outdated:true
# - dormant:true
# - has-agent:connecting|connected|timeout
# - id:<uuid>
```

### Viewing Workspace Details

```bash
# Show workspace resources and connection info
coder show <workspace-name>

# Display resource usage for current workspace
coder stat
```

### Starting and Stopping Workspaces

```bash
# Start a workspace
coder start <workspace-name>

# Stop a workspace
coder stop <workspace-name>

# Restart a workspace (stop then start)
coder restart <workspace-name>
```

### Updating Workspaces

```bash
# Update a workspace to latest template version
coder update <workspace-name>

# Force re-entry of template variables (useful for broken workspaces)
coder update <workspace-name> --always-prompt

# Update without starting
coder update <workspace-name> --dry-run
```

### Workspace Lifecycle

```bash
# Rename a workspace
coder rename <old-name> <new-name>

# Delete a workspace
coder delete <workspace-name>

# Open a workspace in browser
coder open <workspace-name>

# Ping a workspace (check connectivity)
coder ping <workspace-name>
```

### Workspace Scheduling

```bash
# Schedule automated start/stop times
coder schedule <workspace-name> <schedule>

# Example: Mon-Fri, 9 AM to 5 PM UTC
coder schedule my-workspace "09:00-17:00 America/Los_Angeles"
```

### SSH Access

```bash
# Start a shell into a workspace
coder ssh <workspace-name>

# Run a command in a workspace
coder ssh <workspace-name> -- command

# Configure SSH host entries
coder config-ssh

# Port forwarding
coder port-forward <workspace-name> <local-port>:<workspace-port>
```

### Background Services

```bash
# Show resource usage for current workspace
coder stat

# Run network speed test
coder speedtest <workspace-name>
```

## Template Commands

### Managing Templates

```bash
# List templates
coder templates list

# Show template details
coder templates show <template-name>

# Create a template from examples
coder templates init

# Push a template to Coder deployment
coder template push <template-name> -d <directory>

# Update an existing template
coder template update <template-name> -d <directory>
```

### Template Development

```bash
# Initialize a new template from examples
coder templates init

# Available examples include:
# - Docker (container-based workspaces)
# - Kubernetes (pod-based workspaces)
# - AWS EC2 (full VM workspaces)
# - Terraform provider examples
```

## State Management

```bash
# Pull Terraform state for debugging
coder state pull <username>/<workspace-name>

# Push modified state (CAUTION: can corrupt state)
coder state push <username>/<workspace-name>

# Used for manual Terraform state repairs
```

## Workspace Metadata

```bash
# Add workspace to favorites
coder favorite <workspace-name>

# Remove from favorites
coder unfavorite <workspace-name>
```

## Auto-Update Management

```bash
# Toggle auto-update policy for a workspace
coder autoupdate <workspace-name> enable
coder autoupdate <workspace-name> disable

# When enabled, workspace auto-updates to latest template version on start
```

## Port Forwarding

```bash
# Forward ports from workspace to local machine
coder port-forward <workspace-name> <local-port>:<workspace-port>

# For reverse port forwarding, use SSH
coder ssh -R <remote-port>:localhost:<local-port> <workspace-name>
```

## Dotfiles Management

```bash
# Apply dotfiles repository to personalize workspace
coder dotfiles <git-repository-url>

# Automatically applied on workspace start if configured
```

## Tokens Management

```bash
# List personal access tokens
coder tokens list

# Create a new token
coder tokens create

# Delete a token
coder tokens delete <token-id>
```

## Server Operations

```bash
# Start a Coder server
coder server

# Server flags include:
# --address <bind-address>
# --port <port>
# --tls-enable
# --tls-cert-file <path>
# --tls-key-file <path>
```

## Troubleshooting Commands

### Network Debugging

```bash
# Print network debug information
coder netcheck

# Tests DERP and STUN connectivity
```

### Logs

Coder stores logs at these locations in workspaces:

| Service | Location |
|---------|----------|
| Startup script | `/tmp/coder-startup-script.log` |
| Shutdown script | `/tmp/coder-shutdown-script.log` |
| Agent | `/tmp/coder-agent.log` |

Logs are truncated at 5MB.

### Common Issues

**1. Workspace won't start after template update**

```bash
# Re-enter template parameters
coder update <workspace-name> --always-prompt
```

**2. State corruption**

```bash
# Manual state repair (admin only)
coder state pull <username>/<workspace-name>
# Make changes
coder state push <username>/<workspace-name>
```

**3. Connection issues**

```bash
# Check connectivity
coder ping <workspace-name>
coder netcheck
```

## Bulk Operations

**Note**: Bulk operations are a Premium feature.

```bash
# In the UI, select multiple workspaces and use Actions dropdown:
# - Bulk start
# - Bulk stop
# - Bulk update
# - Bulk delete
```

## Environment Variables

Key environment variables for Coder CLI:

```bash
export CODER_URL="https://coder.example.com"
export CODER_SESSION_TOKEN="<your-token>"
export CODER_VERBOSE=false
export CODER_CONFIG_DIR="~/.config/coderv2"
```

## Workspace Filtering Examples

```bash
# Find my running workspaces
coder list owner:me status:running

# Find outdated workspaces
coder list outdated:true

# Find dormant workspaces
coder list dormant:true

# Find workspaces with agents connecting
coder list has-agent:connecting

# Combine filters
coder list owner:me status:running template:python-dev
```

## Integration with Development Workflows

### Pre-commit Hooks

```bash
# Example: Run tests in workspace before commit
coder ssh my-workspace -- npm test
```

### CI/CD Integration

```bash
# Start workspace for CI job
coder start ci-workspace --wait

# Run commands
coder ssh ci-workspace -- ./ci-script.sh

# Stop when done
coder stop ci-workspace
```

## Best Practices

1. **Use templates**: Define environments in templates for consistency
2. **Schedule shutdowns**: Reduce costs by auto-stopping idle workspaces
3. **Enable auto-update**: Keep workspaces current with template changes
4. **Monitor resources**: Use `coder stat` to track workspace usage
5. **Use filters**: Efficiently find and manage workspaces
6. **Secure tokens**: Use environment variables for session tokens

## Coder Tasks (AI Agents)

Coder supports AI coding agents running inside workspaces:

```bash
# Tasks require templates with `coder_ai_task` resource
# View tasks in workspace UI under "Tasks" tab
# Tasks can be managed via Coder deployment UI
```

## Additional Resources

- [Workspace Management Guide](https://coder.com/docs/user-guides/workspace-management)
- [CLI Reference](https://coder.com/docs/reference/cli)
- [Quickstart Guide](https://coder.com/docs/tutorials/quickstart)
- [Coder GitHub](https://github.com/coder/coder)
