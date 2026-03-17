---
name: terragrunt
description: |
  Homelab infrastructure management with Terragrunt, OpenTofu, and Terraform patterns.

  Use when: (1) Planning or applying infrastructure changes to dev/integration/live clusters,
  (2) Adding/modifying machines in inventory.hcl, (3) Creating or updating units and stacks,
  (4) Working with feature flags, (5) Running validation (fmt, validate, test, plan),
  (6) Understanding the units→stacks→modules architecture, (7) Working with HCL configuration files,
  (8) Bare-metal Kubernetes provisioning or Talos configuration.

  Triggers: "terragrunt", "terraform", "opentofu", "tofu", "infrastructure code", "IaC",
  "inventory.hcl", "networking.hcl", "HCL files", "add machine", "add node", "cluster provisioning",
  "bare metal", "talos config", "task tg:", "infrastructure plan", "infrastructure apply",
  "stacks", "units", "modules architecture"

  Always use task commands (task tg:*) instead of running terragrunt directly.
user-invocable: false
---

# Terragrunt Infrastructure Skill

Manage bare-metal Kubernetes infrastructure from PXE boot to running clusters.

For architecture overview (units vs modules, config centralization), see [infrastructure/CLAUDE.md](../../infrastructure/CLAUDE.md). For detailed unit patterns, see [infrastructure/units/CLAUDE.md](../../infrastructure/units/CLAUDE.md).

## Task Commands (Always Use These)

```bash
# Validation (run in order)
task tg:fmt                    # Format HCL files
task tg:test-<module>          # Test specific module (e.g., task tg:test-config)
task tg:validate-<stack>       # Validate stack (e.g., task tg:validate-integration)

# Operations
task tg:list                   # List available stacks
task tg:plan-<stack>           # Plan (e.g., task tg:plan-integration)
task tg:apply-<stack>          # Apply (REQUIRES HUMAN APPROVAL)
task tg:gen-<stack>            # Generate stack files
task tg:clean-<stack>          # Clean generated files
```

**NEVER** run `terragrunt` or `tofu` directly—always use `task` commands.

## How to Add a Machine

1. Edit `inventory.hcl`:
```hcl
node50 = {
  cluster = "live"
  type    = "worker"
  install = {
    selector     = "disk.model == 'Samsung'"
    architecture = "amd64"
  }
  interfaces = [{
    id           = "eth0"
    hardwareAddr = "aa:bb:cc:dd:ee:ff"  # VERIFY correct
    addresses    = [{ ip = "192.168.10.50" }]  # VERIFY available
  }]
}
```
2. Run `task tg:plan-live`
3. Review plan—config module auto-includes machines where `cluster == "live"`
4. Request human approval before apply

## How to Add a Feature Flag

1. Add version to `versions.hcl` if needed
2. Add feature detection in `modules/config/main.tf`:
```hcl
locals {
  new_feature_enabled = contains(var.features, "new-feature")
}
```
3. Enable in stack's features list:
```hcl
features = ["gateway-api", "longhorn", "new-feature"]
```

## How to Create a New Unit

1. Create `units/new-unit/terragrunt.hcl`:
```hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../../.././/modules/new-unit"
}

dependency "config" {
  config_path = "../config"
  mock_outputs = { new_unit = {} }
}

inputs = dependency.config.outputs.new_unit
```
2. Create corresponding `modules/new-unit/` with `variables.tf`, `main.tf`, `outputs.tf`, `versions.tf`
3. Add output from config module
4. Add `unit` block to stacks that need it

## How to Write Module Tests

Tests use OpenTofu native testing in `modules/<name>/tests/*.tftest.hcl`:

```hcl
# Top-level variables set defaults for ALL run blocks
variables {
  name     = "test-cluster"
  features = ["gateway-api"]
  machines = {
    node1 = {
      cluster = "test-cluster"
      type    = "controlplane"
      # ... complete machine definition
    }
  }
}

run "feature_enabled" {
  command = plan
  variables {
    features = ["prometheus"]  # Only override what differs
  }
  assert {
    condition     = output.prometheus_enabled == true
    error_message = "Prometheus should be enabled"
  }
}
```

Run with `task tg:test-config` or `task tg:test` for all modules.

## Safety Rules

- **NEVER** run apply without explicit human approval
- **NEVER** use `--auto-approve` flags
- **NEVER** guess MAC addresses or IPs—verify against `inventory.hcl`
- **NEVER** commit `.terragrunt-cache/` or `.terragrunt-stack/`
- **NEVER** manually edit Terraform state

## State Operations

When removing state entries with indexed resources (e.g., `this["rpi4"]`), `xargs` strips the quotes causing errors. Use a `while` loop instead:

```bash
# WRONG - xargs mangles quotes in resource names
terragrunt state list | xargs -n 1 terragrunt state rm

# CORRECT - while loop preserves quotes
terragrunt state list | while read -r resource; do terragrunt state rm "$resource"; done
```

This applies to any state operation on resources with map keys like `data.talos_machine_configuration.this["rpi4"]`.

## Validation Checklist

Before requesting apply approval:
- [ ] `task tg:fmt` passes
- [ ] `task tg:test` passes (if module tests exist)
- [ ] `task tg:validate` passes for ALL stacks
- [ ] `task tg:plan-<stack>` reviewed
- [ ] No unexpected destroys in plan
- [ ] Network changes won't break connectivity

## References

- [stacks.md](references/stacks.md) - Detailed Terragrunt stacks documentation
- [units.md](references/units.md) - Detailed Terragrunt units documentation
