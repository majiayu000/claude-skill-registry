---
name: atmos-functions
description:
  Use when wiring cross-component dependencies in stack YAML. Covers !terraform.state syntax for passing outputs between
  components without remote-state lookups.
---

# Cross-Component Dependencies with Atmos Functions

**Preferred approach: Atmos Functions** - Use Atmos template functions in stack YAML to pass values between components
at plan/apply time. This avoids Terraform remote state lookups entirely.

## `!terraform.state` Syntax

Two-parameter form (current stack):

```yaml
!terraform.state <component> <output>
```

Three-parameter form (specific stack):

```yaml
!terraform.state <component> <stack> <output>
```

## Examples

```yaml
components:
  terraform:
    my-component:
      vars:
        # Current stack lookups (component output)
        vpc_id: !terraform.state vpc vpc_id
        subnet_ids: !terraform.state vpc private_subnet_ids

        # Cross-stack lookup (component stack output)
        grafana_role_arn: !terraform.state grafana core-use2-auto workspace_iam_role_arn

        # Nested output with YQ expression
        role_arn: !terraform.state iam-role/my-role plat-use2-dev .role.arn
```

## `!terraform.output` Alternative

There's also `!terraform.output` which has the same syntax but different behavior:

```yaml
# Same syntax as !terraform.state
vpc_id: !terraform.output vpc vpc_id
```

**Key differences:**

| Aspect       | `!terraform.state` (preferred)      | `!terraform.output`                        |
| ------------ | ----------------------------------- | ------------------------------------------ |
| How it works | Reads directly from S3 state bucket | Runs `terraform init` + `terraform output` |
| Speed        | Fast (direct S3 read)               | Slow (full Terraform initialization)       |
| Use case     | Default choice                      | When state file format differs             |

**Always prefer `!terraform.state`** - it's significantly faster because it reads the state file directly from S3
without running Terraform commands.

## Best Practices

- **Use `!terraform.state` over `!terraform.output`** - Direct S3 access is much faster than running Terraform.
- **Define lookups in catalog defaults** - Put `!terraform.state` expressions in
  `stacks/catalog/<component>/defaults.yaml` rather than in stack files. The function automatically resolves based on
  the current stack context.
- **Use current-stack lookups when possible** - Omit the stack parameter to look up components in the same stack, making
  configs more portable.
- **Cross-stack lookups for shared resources** - Use the three-parameter form when referencing centralized resources
  (e.g., Grafana in core-auto from plat accounts).

## Legacy Approach (Being Phased Out)

Some older components still use Cloud Posse's `remote-state` Terraform module with `remote-state.tf` files. This pattern
is being phased out in favor of Atmos functions. The tfstate backend is in the core-auto account.

When you encounter `remote-state.tf` files, prefer converting them to `!terraform.state` expressions in the catalog.
