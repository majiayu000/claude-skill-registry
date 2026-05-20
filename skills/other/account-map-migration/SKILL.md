---
name: account-map-migration
description: >-
  Use when fixing legacy account-map component references or creating new components. Covers migration from dynamic
  account-map lookups to static account_map variable. Use when you see account-map remote-state references or need to
  set up provider configuration for a new component.
---

# Account Map Migration

This repository has migrated away from the `account-map` component to use Atmos Auth for authentication. Instead of
dynamically looking up account IDs via the account-map component's remote state, we use a static `account_map` variable
defined in `stacks/orgs/acme/_defaults.yaml`.

## Why We Migrated

The legacy `account-map` component pattern required:

1. Deploying account-map component first (chicken-and-egg problem)
2. Remote state lookups for every component that needed account IDs
3. Complex `providers.tf` with remote-state module calls
4. Cross-account state access permissions

The new pattern:

1. Static account map defined once in stack defaults
2. No remote state dependencies for account lookups
3. Simpler provider configuration
4. Works with Atmos Auth for authentication

## Key Configuration

### Stack Defaults

The account map is defined in `stacks/orgs/acme/_defaults.yaml`:

```yaml
vars:
  account_map_enabled: false
  account_map:
    full_account_map:
      acme-core-root: "111111111111"
      acme-core-audit: "222222222222"
      acme-core-auto: "333333333333"
      acme-plat-dev: "444444444444"
      acme-plat-staging: "555555555555"
      acme-plat-prod: "666666666666"
      # ... all accounts
    iam_role_arn_templates:
      terraform: "arn:aws:iam::%s:role/acme-core-gbl-auto-terraform"
    audit_account_account_name: "acme-core-audit"
    root_account_account_name: "acme-core-root"
```

### Vendored providers.tf

Components use a vendored `providers.tf` from Atmos mixins that includes:

- `account_map_enabled` and `account_map` variables
- Provider configuration that uses the static account map
- Dummy `iam_roles` module for legacy compatibility

**Vendoring is configured in each component's `component.yaml`:**

```yaml
# components/terraform/<component-name>/component.yaml
apiVersion: atmos/v1
kind: ComponentVendorConfig
spec:
  source:
    uri: github.com/cloudposse-terraform-components/aws-<component>.git//src?ref={{ .Version }}
    version: v1.x.x
    included_paths:
      - "**/**"
    excluded_paths:
      - "providers.tf" # Exclude upstream providers.tf
  mixins:
    # Vendor the providers.tf with account-map support
    - uri: https://raw.githubusercontent.com/cloudposse-terraform-components/mixins/{{ .Version }}/src/mixins/provider-without-account-map.tf
      version: v0.3.0
      filename: providers.tf
    - uri: https://raw.githubusercontent.com/cloudposse-terraform-components/mixins/{{ .Version }}/src/mixins/account-verification.mixin.tf
      version: v0.3.0
      filename: account-verification.mixin.tf
```

**Key points:**

- The upstream `providers.tf` is excluded via `excluded_paths`
- The `provider-without-account-map.tf` mixin is vendored as `providers.tf`
- This mixin includes the `account_map_enabled` and `account_map` variables

**To vendor (or re-vendor) the component:**

```bash
atmos vendor pull -c <component-name>
```

The vendored `providers.tf` handles all account map logic automatically. You don't need to manually add these variables
to `variables.tf` - they're included in `providers.tf`.

## Migration Checklist

When migrating a component or creating a new one:

1. **Vendor providers.tf** - Run `atmos vendor pull -c <component-name>` to get the latest providers.tf with account map
   support
2. **Update remote-state.tf** - If the component has a `remote-state.tf` that references account-map, update it to use
   the bypass pattern (see below)
3. **Verify catalog** - Ensure `account_map_enabled: false` is set (inherited from `_defaults.yaml`)
4. **Test** - Run `atmos terraform plan` to verify

### Bypass Pattern for remote-state.tf

If a component has a `remote-state.tf` with an account-map lookup, update it to use `bypass` and `defaults`:

```hcl
module "account_map" {
  source  = "cloudposse/stack-config/yaml//modules/remote-state"
  version = "1.8.0"

  component   = "account-map"
  tenant      = var.account_map_enabled ? coalesce(var.account_map_tenant, module.this.tenant) : null
  environment = var.account_map_enabled ? var.account_map_environment : null
  stage       = var.account_map_enabled ? var.account_map_stage : null

  context = module.this.context

  # When account_map is disabled, bypass remote state and use the static account_map variable
  bypass   = !var.account_map_enabled
  defaults = var.account_map
}
```

**Key points:**

- `bypass = !var.account_map_enabled` - Skips remote state lookup when disabled
- `defaults = var.account_map` - Uses the static account_map variable instead
- `module.account_map.outputs` works the same regardless of bypass - returns `defaults` when bypassed

## Identifying Legacy References

Search for components still using the old pattern:

```bash
# Find remote-state references to account-map
grep -r "account-map" components/terraform/*/remote-state.tf

# Find components without account_map_enabled variable
for dir in components/terraform/*/; do
  if ! grep -q "account_map_enabled" "$dir/variables.tf" 2>/dev/null; then
    echo "Missing: $dir"
  fi
done
```

## Reference Implementations

See these components for the current pattern:

- `components/terraform/vpc/` - Standard component with account_map
- `components/terraform/ecr/` - Component with cross-account access

## New Components

When creating new components, the migrated pattern is automatic:

1. **Vendor providers.tf** - Run `atmos vendor pull -c <component-name>` to get providers.tf with account map support
2. **Inherit stack defaults** - `account_map_enabled: false` is inherited from `_defaults.yaml`
3. **Use Atmos functions** - Use `!terraform.state` for cross-component dependencies instead of remote-state.tf

See the `developing-components` skill for full component creation guidance.
