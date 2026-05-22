---
name: terraform-station-module
description: Maintain the Station Terraform module itself (not test authoring). Use this skill whenever the user asks to add, change, refactor, or troubleshoot Station module behavior in root *.tf files or child module folders (application/, group/, user_assigned_identity/, hashicorp/tfe/), update variables/outputs/validations, or adjust provider/resource wiring for module consumers.
---

# Terraform Station Module Skill

Use this skill when working on Station module implementation logic.

This skill is for **module code changes**. For Terraform test authoring/execution in `tests/*.tftest.hcl`, use `terraform-station-test`.

## What this skill covers

- Adding/changing behavior in root module files (`*.tf` at repo root)
- Updating child modules:
  - `application/`
  - `group/`
  - `user_assigned_identity/`
  - `hashicorp/tfe/`
- Updating module interfaces:
  - `variables.tf`
  - `variables.applications.tf`
  - `variables.identity.tf`
  - `outputs.tf`
- Keeping Station compatible as a **called module** (consumer-facing contract)
- Updating documentation where interface/behavior changes

## Station module invariants

1. Treat Station as a module consumed by parent configurations.
2. Preserve backward compatibility unless the user explicitly requests a breaking change.
3. Keep variable schemas, validation rules, and defaults aligned with actual implementation.
4. Keep outputs aligned with resources and child module wiring.
5. Prefer extending existing patterns over introducing new structure.
6. Keep changes focused and minimal.

## Required discovery before changing code

Always inspect these first for impact analysis:

- `variables.tf`
- `variables.applications.tf`
- `variables.identity.tf`
- `outputs.tf`
- relevant feature files (for example `applications.tf`, `groups.tf`, `connectivity.tf`, `tfe.tf`)
- relevant child module `variables.tf` and `outputs.tf`

Then map your change to:

- inputs consumed
- resources/data affected
- outputs exposed
- tests likely impacted

## Implementation workflow

1. Locate feature entry points in root module files.
2. Identify whether behavior belongs in root module or child module.
3. Update variable definitions/validations if interface changed.
4. Update implementation (`resource`, `data`, `locals`, `module` calls).
5. Update outputs if exposed behavior changed.
6. Update docs/examples if user-visible behavior changed.
7. Run formatting.
8. Run relevant tests (or hand off to `terraform-station-test` flow).

## Validation and formatting rules

- Run:

```bash
terraform fmt -recursive
```

- Do **not** rely on `terraform validate` for this repository due provider alias/module limitations.

- Prefer targeted Terraform tests for affected feature areas:
  - `tests/application.tftest.hcl`
  - `tests/group.tftest.hcl`
  - `tests/tfe.tftest.hcl`
  - `tests/connectivity.tftest.hcl`
  - `tests/identity.tftest.hcl`
  - `tests/user_assigned_identities.tftest.hcl`

## Compatibility checklist for module changes

Before finishing a change, verify:

- Input object shape matches actual references in code
- Optional fields are guarded with `try(...)`, `lookup(...)`, `coalesce(...)`, or conditional logic where needed
- Validation error messages still describe the true constraint
- Resource naming/location/tag defaults still follow Station conventions
- Identity and role-assignment side effects remain correct for enabled feature blocks
- Outputs still reference valid resource/module attributes

## Common Station-specific pitfalls

- Adding new required fields to existing input objects without defaults
- Changing map keys that tests/consumers depend on
- Forgetting to propagate variable changes into child modules
- Breaking app/group/identity auto-assignment behavior
- Updating logic but not adjusting outputs/docs

## CI-aware change planning

Station uses selective test execution in CI.

When changing module files, anticipate which tests are triggered using:

- `.github/scripts/README.md`
- `.github/workflows/terraform.yaml`

If core/shared files are touched, expect full-suite runs.

## Use with testing skill

After module edits:

1. format with `terraform fmt -recursive`
2. invoke `terraform-station-test` for test updates/execution
3. ensure feature tests cover minimum + maximum scenarios when behavior changed

## Done criteria for module tasks

- Code change implemented at correct module boundary
- Variable/validation/output updates included where needed
- Formatting completed
- Relevant tests run (or explicitly delegated)
- No unrelated refactors bundled into the change
