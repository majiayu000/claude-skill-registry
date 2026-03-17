---
name: terraform
description: Writes Terraform infrastructure code following strict module abstraction principles, proper file structure, and quality standards. Modules are never thin resource wrappers — each represents a meaningful level of abstraction. Always uses the latest stable Terraform and provider releases. Always looks up provider documentation before writing code. Always runs format, init (no backend), and validate before committing. Use when user asks to write, create, add, update, or refactor Terraform code or modules, or mentions "terraform", "IaC", or "infrastructure as code".
user-invocable: true
---

# Terraform — Infrastructure as Code Writer

Writes Terraform code following strict module abstraction, file structure, and quality standards. Every module must represent a meaningful level of abstraction, use the latest stable releases, and pass format/init/validate before any commit.

## Input Format

```
/terraform <task description>
```

- Describe the infrastructure to create, modify, or refactor
- Include the target provider (AWS, GCP, Azure, etc.) if known
- Include any specific constraints or existing module paths if relevant

## Core Principles

### Module Abstraction

Modules must represent **meaningful levels of abstraction** — never thin wrappers around a single resource. A module's value is in encoding an opinionated, complete infrastructure pattern that a caller treats as a single concept.

**Wrong:** A module that only wraps `aws_s3_bucket` and passes through a handful of arguments.

**Right:** A module that creates a bucket with server-side encryption, versioning, lifecycle rules, and optional replication — a complete, reusable pattern with sensible defaults.

Every module must have **low complexity at its own level**. If `main.tf` is growing hard to scan, delegate that complexity to sub-modules or shared modules. Each level should be easy to comprehend on its own without tracing through many moving parts.

### Module Hierarchy

Terraform modules form a hierarchy. Each level has a defined responsibility:

| Level | Responsibility |
|-------|---------------|
| **Root module** | Wires type modules together. Contains only `module` blocks and `locals`. No resource blocks. |
| **Type modules** | Implement one infrastructure concern at a moderate abstraction level. `main.tf` should be readily understandable at a glance. |
| **Sub-modules / shared modules** | Handle specific reusable patterns delegated from type modules. Still not thin resource wrappers. |

The rule: if reading `main.tf` at any level requires tracking many moving parts to understand what it does, that level has too much complexity. Extract a sub-module.

### File Structure

Every module uses this structure:

```
module-name/
├── main.tf        # Resource definitions and module calls
├── variables.tf   # Input variable declarations with descriptions and types
├── outputs.tf     # Output value declarations with descriptions
└── versions.tf    # terraform block with required_version and required_providers
```

Add files beyond this set only when a distinct logical concern warrants separation:
- `locals.tf` — when local value expressions are extensive
- `data.tf` — when many data source lookups would clutter `main.tf`

**File naming rules (strictly enforced):**
- Never prefix files numerically (`01-network.tf`, `02-compute.tf` — forbidden)
- Never name files after infrastructure types (`ec2.tf`, `rds.tf`, `vpc.tf`, `iam.tf` — forbidden)
- File names describe logical role in the module, not the resource types inside them

---

## Step 1: Look Up Versions Before Writing Any Code

Always use the **latest stable release** of Terraform and every provider. Never pin to an old version unless the user explicitly requires it.

Before writing any `.tf` file, fetch current versions:

1. Check the latest Terraform release at https://github.com/hashicorp/terraform/releases — use the highest non-prerelease version tag.
2. Check each required provider in the Terraform Registry at https://registry.terraform.io/browse/providers — navigate to the provider, confirm the latest published version.
3. Write `versions.tf` with those versions before writing any other file.

**`versions.tf` template:**

```hcl
terraform {
  required_version = "~> <latest_major.minor>"

  required_providers {
    <provider> = {
      source  = "<namespace>/<provider>"
      version = "~> <latest_major>"
    }
  }
}
```

Use `~>` (pessimistic constraint operator) to allow patch updates within the pinned minor version for `required_version`, and patch/minor updates within the pinned major version for providers.

---

## Step 2: Look Up Provider Documentation Before Writing Resources

Never write resource blocks or data source blocks from memory. Provider schemas change between versions — arguments are added, renamed, or deprecated.

For every resource or data source you write:

1. Navigate to the provider's documentation page in the Terraform Registry: `https://registry.terraform.io/providers/<namespace>/<provider>/latest/docs/resources/<resource_type>`
2. Verify the current argument names, required vs. optional fields, and any deprecation notices.
3. Copy argument names exactly as documented — do not guess or abbreviate.

If the registry page for a resource is unavailable, use the provider's GitHub repository under `website/docs/r/`.

---

## Step 3: Write the Module

Apply these rules as you write each file:

### `main.tf`

- Contains resource blocks and calls to sub-modules only
- No variable declarations, no output declarations, no provider configuration
- Should be readable top-to-bottom without needing to cross-reference other files constantly
- If it exceeds ~80 lines and is difficult to scan, delegate blocks to a sub-module

### `variables.tf`

- Every variable must have a `description`
- Every variable must have an explicit `type`
- Provide `default` values only where a sensible, safe default exists
- Use `validation` blocks for values with known constraints (e.g., allowed regions, name length limits)

```hcl
variable "environment" {
  description = "Deployment environment name (e.g. production, staging)."
  type        = string

  validation {
    condition     = contains(["production", "staging", "development"], var.environment)
    error_message = "environment must be one of: production, staging, development."
  }
}
```

### `outputs.tf`

- Every output must have a `description`
- Export values that callers will need to wire modules together or reference externally
- Do not export internal implementation details that no caller would use

### Dependency Injection

Modules must not resolve their own dependencies via internal `data` source lookups. The caller is responsible for providing all external resource references as input variables.

**Wrong:** A module that uses `data "aws_vpc" "main"` to look up the VPC by a name tag or environment convention.

**Right:** The caller passes `var.vpc_id` directly. The module declares a `vpc_id` variable and uses it without performing any lookup.

Apply this rule to any externally-owned resource: VPCs, IAM roles, KMS keys, Route 53 zones, etc. `data` sources are appropriate only for fetching provider-owned metadata (e.g. `data "aws_availability_zones"`, `data "aws_ami"`) or resources created within the same module call chain.

### Polymorphism

A module should adapt its behaviour based on input variables rather than requiring callers to use different modules for different environments. Use conditional expressions and feature flags to produce distinct configurations from a single module.

```hcl
variable "high_availability" {
  description = "When true, deploys a multi-AZ, multi-instance configuration."
  type        = bool
  default     = false
}

resource "aws_instance" "this" {
  count = var.high_availability ? 3 : 1
  # ...
}
```

This keeps the module surface small and ensures that production and development environments exercise the same code paths.

### Sub-modules

Create a sub-module when:
- A logical group of resources within a type module makes `main.tf` hard to scan
- The same pattern is needed in more than one place

Place sub-modules in a `modules/` directory within the parent module:

```
type-module/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
└── modules/
    └── sub-concern/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

---

## Step 4: Pre-Commit Workflow

Run these three commands in order inside **every module directory that was created or modified**. Do not commit until all three pass cleanly.

### 4a — Format

```bash
terraform fmt -recursive
```

Apply all reported formatting changes. Re-run until the command exits with no output (no changes needed).

### 4b — Init (no backend)

```bash
terraform init -backend=false
```

Downloads providers and validates the `required_providers` block without configuring a remote backend. Required before validate can run.

If init fails due to a version constraint conflict, re-check the registry for current versions and update `versions.tf`.

### 4c — Validate

```bash
terraform validate
```

All modules must pass with `Success! The configuration is valid.` — no errors, no warnings. Fix every issue before committing.

### 4d — Commit

Only after all three commands pass cleanly across every modified module directory.

---

## Module Abstraction Checklist

Work through this before considering any module done:

- [ ] Does the module represent a meaningful abstraction, not a thin resource wrapper?
- [ ] Can you read `main.tf` top-to-bottom and understand what it does without deep investigation?
- [ ] Are all files named without numeric prefixes or infrastructure-type names?
- [ ] Is `versions.tf` present with the latest stable versions looked up from the registry?
- [ ] Did you fetch and verify provider docs for every resource and data source written?
- [ ] Are all variables typed and described?
- [ ] Are all outputs described?
- [ ] Does complex logic inside this module delegate to a sub-module rather than bloating `main.tf`?
- [ ] Does the module receive all external resource references as input variables rather than resolving them via internal `data` source lookups?
- [ ] Does the module use conditional logic or feature flags to adapt behaviour, rather than requiring separate modules per environment?
- [ ] Does the module avoid relying on naming conventions, environment names, or global state to locate resources?
- [ ] Have `fmt`, `init -backend=false`, and `validate` all passed cleanly?

---

## Error Handling

| Scenario | Action |
|----------|--------|
| **`terraform fmt` reports changes** | Apply changes, re-run until no output |
| **`terraform init` fails on version constraint** | Re-fetch current versions from registry, update `versions.tf`, retry |
| **`terraform validate` fails** | Fix all errors; never suppress with `ignore_changes` or workarounds unless the resource genuinely requires it |
| **Resource argument unknown or deprecated** | Fetch current provider docs from registry; update to the current schema |
| **`main.tf` exceeds ~80 lines and is hard to scan** | Extract a sub-module; do not keep complexity at the current level |
| **Same pattern used in multiple places** | Extract a shared module; do not duplicate resource blocks |
| **Registry documentation is unavailable** | Use the provider's GitHub `website/docs/r/` directory as fallback |
| **Module uses a `data` source to look up an externally-owned resource** | Remove the lookup; add an input variable and require the caller to pass the ID |
| **Module behaviour varies only by environment name or hard-coded convention** | Replace with a feature-flag variable; remove the environmental assumption |
| **Module references a specific naming convention or global tag to find resources** | This is tight coupling — inject the resource reference as a variable instead |
