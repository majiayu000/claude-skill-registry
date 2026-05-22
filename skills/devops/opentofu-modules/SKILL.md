---
name: opentofu-modules
description: |
  Write OpenTofu/Terraform modules and comprehensive tests for homelab infrastructure.

  Use when: (1) Creating new OpenTofu or Terraform modules, (2) Writing or modifying .tftest.hcl test files,
  (3) Adding variables, outputs, or resources to modules, (4) Debugging test failures,
  (5) Understanding module testing patterns, (6) Writing infrastructure unit tests,
  (7) Questions about tftest syntax or assertions.

  Triggers: "opentofu module", "terraform module", "tofu module", "create module",
  ".tftest.hcl", "tftest", "test my module", "module test", "infrastructure test",
  "test infrastructure", "variables.tf", "outputs.tf", "module testing", "assertion",
  "task tg:test", "test-config", "test failures"

  This skill covers OpenTofu v1.11 testing syntax, variable inheritance patterns,
  assertion best practices, and repository-specific conventions in infrastructure/modules/.
---

# OpenTofu Modules & Testing

Write OpenTofu modules and tests for the homelab infrastructure. Modules live in `infrastructure/modules/`, tests in `infrastructure/modules/<name>/tests/`.

## Quick Reference

```bash
# Run tests for a module
task tg:test-<module>          # e.g., task tg:test-config

# Format all HCL
task tg:fmt

# Version pinned in .opentofu-version (currently 1.11.2)
```

## Module Structure

Every module MUST have:
```
infrastructure/modules/<name>/
├── variables.tf    # Input definitions with descriptions and validations
├── main.tf         # Primary resources and locals
├── outputs.tf      # Output definitions
├── versions.tf     # Provider and OpenTofu version constraints
└── tests/          # Test directory
    └── *.tftest.hcl
```

## Test File Structure

Use `.tftest.hcl` extension. Define top-level `variables` for defaults inherited by all `run` blocks.

```hcl
# Top-level variables set defaults for ALL run blocks
variables {
  name     = "test-cluster"
  features = ["gateway-api", "longhorn"]

  networking = {
    id           = 1
    internal_tld = "internal.test.local"
    # ... other required fields
  }

  # Default machine - inherited unless overridden
  machines = {
    node1 = {
      cluster = "test-cluster"
      type    = "controlplane"
      install = { selector = "disk.model = *" }
      interfaces = [{
        id           = "eth0"
        hardwareAddr = "aa:bb:cc:dd:ee:01"
        addresses    = [{ ip = "192.168.10.101" }]
      }]
    }
  }
}

run "descriptive_test_name" {
  command = plan  # Use plan mode - no real resources created

  variables {
    features = ["prometheus"]  # Only override what differs
  }

  assert {
    condition     = output.some_value == "expected"
    error_message = "Descriptive failure message"
  }
}
```

## Key Patterns

### Use `command = plan`
Always use plan mode for tests. This validates configuration without creating resources.

### Variable Inheritance
Only include variables in `run` blocks when they differ from defaults. Minimizes duplication.

```hcl
# CORRECT: Override only what changes
run "feature_enabled" {
  command = plan
  variables {
    features = ["prometheus"]
  }
  assert { ... }
}

# AVOID: Repeating all variables
run "feature_enabled" {
  command = plan
  variables {
    name     = "test-cluster"      # Unnecessary - inherited
    features = ["prometheus"]
    machines = { ... }             # Unnecessary - inherited
  }
}
```

### Assert Against Outputs
Reference module outputs in assertions, not internal resources.

```hcl
assert {
  condition     = length(output.machines) == 2
  error_message = "Expected 2 machines"
}

assert {
  condition     = output.talos.kubernetes_version == "1.32.0"
  error_message = "Version mismatch"
}
```

### Test Feature Flags
Test both enabled and disabled states:

```hcl
run "feature_enabled" {
  command = plan
  variables { features = ["longhorn"] }

  assert {
    condition = alltrue([
      for m in output.talos.talos_machines :
      contains(m.install.extensions, "iscsi-tools")
    ])
    error_message = "Extension should be added when feature enabled"
  }
}

run "feature_disabled" {
  command = plan
  variables { features = [] }

  assert {
    condition = alltrue([
      for m in output.talos.talos_machines :
      !contains(m.install.extensions, "iscsi-tools")
    ])
    error_message = "Extension should not be present without feature"
  }
}
```

### Test Validations
Use `expect_failures` to verify variable validation rules:

```hcl
run "invalid_version_rejected" {
  command = plan
  variables {
    versions = {
      talos = "1.9.0"  # Missing v prefix - should fail
      # ...
    }
  }
  expect_failures = [var.versions]
}
```

## Common Assertions

```hcl
# Check length
condition = length(output.items) == 3

# Check key exists
condition = contains(keys(output.map), "expected_key")

# Check value in list
condition = contains(output.list, "expected_value")

# Check string contains
condition = strcontains(output.config, "expected_substring")

# Check all items match
condition = alltrue([for item in output.list : item.enabled == true])

# Check any item matches
condition = anytrue([for item in output.list : item.name == "target"])

# Nested check with labels/annotations
condition = anytrue([
  for label in output.machines["node1"].labels :
  label.key == "expected-label" && label.value == "expected-value"
])
```

## Test Organization

Organize tests by concern:
- `plan.tftest.hcl` - Basic structure and output validation
- `validation.tftest.hcl` - Input validation rules
- `feature_<name>.tftest.hcl` - Feature flag behavior
- `edge_cases.tftest.hcl` - Boundary conditions

## Detailed Reference

For OpenTofu testing syntax, mock providers, and advanced patterns, see:
[references/opentofu-testing.md](references/opentofu-testing.md)
