---
name: tofu
description: |
  OpenTofu infrastructure-as-code reference for HCL syntax, state management,
  module design, and provider configuration. Use when working with OpenTofu
  configurations (.tf files), running tofu commands, troubleshooting state
  issues, or designing modules. Includes Proxmox provider patterns.
  Triggers: tofu, opentofu, tfstate, .tf files, HCL, modules, providers.
agent: tofu-expert
---

# OpenTofu Skill

Infrastructure-as-code reference for OpenTofu configurations, state management, and provider patterns.

OpenTofu is the open-source fork of Terraform, maintained by the Linux Foundation. Commands and syntax are nearly identical to Terraform.

## Quick Reference

```bash
# Core workflow
tofu init              # Initialize, download providers
tofu validate          # Syntax validation
tofu fmt -recursive    # Format HCL files
tofu plan              # Preview changes
tofu apply             # Apply changes

# Inspection
tofu state list                    # List resources in state
tofu state show <resource>         # Show resource details
tofu graph | dot -Tsvg > graph.svg # Dependency graph

# Debug
TF_LOG=DEBUG tofu plan 2>debug.log
```

## Core Workflow

```
init → validate → fmt → plan → apply
```

1. **init**: Download providers, initialize backend
2. **validate**: Check syntax and configuration validity
3. **fmt**: Ensure consistent formatting
4. **plan**: Preview what will change (review carefully)
5. **apply**: Execute changes

## Terraform Migration

OpenTofu is a drop-in replacement for Terraform:

```bash
# Replace terraform with tofu in commands
terraform init  →  tofu init
terraform plan  →  tofu plan
terraform apply →  tofu apply

# State files are compatible
# Provider configurations work the same
# Most modules work without changes
```

**Key differences:**
- Different binary name (`tofu` vs `terraform`)
- Some newer Terraform features may not be available yet
- Provider registry defaults differ (can be configured)

## Reference Files

Load on-demand based on task:

| Topic | File | When to Load |
|-------|------|--------------|
| Troubleshooting | [troubleshooting.md](references/troubleshooting.md) | Common errors, debugging |
| State | [state-management.md](references/state-management.md) | Backends, locking, operations |
| Modules | [module-design.md](references/module-design.md) | Module patterns, composition |
| Security | [security.md](references/security.md) | Secrets, state security |
| Migration | [migration.md](references/migration.md) | Terraform → OpenTofu |
| Proxmox Gotchas | [proxmox/gotchas.md](references/proxmox/gotchas.md) | Critical provider issues |
| Proxmox Auth | [proxmox/authentication.md](references/proxmox/authentication.md) | Provider config, API tokens |
| Proxmox VMs | [proxmox/vm-qemu.md](references/proxmox/vm-qemu.md) | proxmox_vm_qemu patterns |

## Validation Checklist

Before `tofu apply`:

- [ ] `tofu init` completed successfully
- [ ] `tofu validate` passes
- [ ] `tofu fmt` applied
- [ ] `tofu plan` reviewed (check destroy/replace operations)
- [ ] Backend configured correctly (for team environments)
- [ ] State locking enabled (if remote backend)
- [ ] Sensitive variables marked `sensitive = true`
- [ ] Provider versions pinned
- [ ] No secrets in version control
- [ ] Blast radius assessed (what could break?)

## Variable Precedence

(highest to lowest)

1. `-var` flag: `tofu apply -var="name=value"`
2. `-var-file` flag: `tofu apply -var-file=prod.tfvars`
3. `*.auto.tfvars` files (alphabetically)
4. `terraform.tfvars` file
5. `TF_VAR_*` environment variables
6. Variable defaults in `variables.tf`

## Provider Configuration

```hcl
# versions.tf
terraform {
  required_version = ">= 1.6.0"  # OpenTofu version

  required_providers {
    proxmox = {
      source  = "Telmate/proxmox"
      version = "~> 3.0"
    }
  }
}
```
