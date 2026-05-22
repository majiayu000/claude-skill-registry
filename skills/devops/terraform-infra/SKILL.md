---
name: terraform-infra
description: Terraform infrastructure operations with safety controls
allowed-tools: [Bash, Read, Glob]
---

# Terraform Infrastructure Skill

## Overview

Provides 90%+ context savings vs raw Terraform MCP server. Includes critical safety controls for infrastructure operations.

## Requirements

- Terraform CLI (v1.0+)
- Cloud provider credentials configured
- Working directory with .tf files

## Tools (Progressive Disclosure)

### Planning & Validation

| Tool     | Description             | Confirmation |
| -------- | ----------------------- | ------------ |
| plan     | Generate terraform plan | No           |
| validate | Validate configuration  | No           |
| fmt      | Format terraform files  | No           |

### State Operations

| Tool     | Description            | Confirmation |
| -------- | ---------------------- | ------------ |
| show     | Display current state  | No           |
| list     | List state resources   | No           |
| state-mv | Move resource in state | Yes          |

### Workspace Operations

| Tool             | Description      | Confirmation |
| ---------------- | ---------------- | ------------ |
| workspace-list   | List workspaces  | No           |
| workspace-select | Select workspace | No           |
| workspace-new    | Create workspace | Yes          |

### Execution (⚠️ Dangerous)

| Tool  | Description   | Confirmation |
| ----- | ------------- | ------------ |
| apply | Apply changes | **REQUIRED** |

### Blocked Operations

| Tool     | Status      |
| -------- | ----------- |
| destroy  | **BLOCKED** |
| state-rm | **BLOCKED** |

## Quick Reference

```bash
# Initialize
terraform init

# Plan changes
terraform plan -out=tfplan

# Validate
terraform validate

# Apply (requires -auto-approve for automation)
terraform apply tfplan
```

## Configuration

- Working directory: Must contain terraform files
- TF*VAR*\*: Variable values via environment
- TF_WORKSPACE: Active workspace

## Safety Controls

⚠️ **terraform apply ALWAYS requires confirmation**
⚠️ **terraform destroy is BLOCKED by default**
⚠️ **State modifications require confirmation**
⚠️ **Review plan output before apply**

## Agent Integration

- **devops** (primary): Infrastructure management
- **architect** (secondary): Infrastructure design
- **cloud-integrator** (secondary): Cloud provisioning

## Troubleshooting

| Issue        | Solution                      |
| ------------ | ----------------------------- |
| Init failed  | Check provider credentials    |
| State locked | Check for other operations    |
| Plan failed  | Review error output carefully |
