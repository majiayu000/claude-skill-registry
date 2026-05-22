---
name: terraform-station-test
description: Write and maintain Terraform tests for the Station module. Use this skill whenever the user asks to add, update, fix, or run Station tests in tests/*.tftest.hcl, validate module behavior across minimum/maximum configurations, wire setup-* modules into test runs, or align test changes with Station CI selective test execution.
---

# Terraform Station Test Skill

Use this skill for testing this repository's root Terraform module (`Station`) with Terraform's built-in test framework.

Station is consumed as a module. Tests must validate behavior through module inputs and outputs, not by treating the root as a standalone deployment.

## What this skill covers

- Writing new Station test files in `tests/*.tftest.hcl`
- Updating existing feature tests (`application`, `group`, `tfe`, `connectivity`, `identity`, `user_assigned_identities`)
- Correct use of setup modules in `tests/setup-*/`
- Correct variable override patterns using prior `run` outputs
- Running tests locally with `terraform test` / `terraform test -filter=...`
- Aligning test changes with CI selective test execution

## Station test ground rules

1. Always inspect the module inputs before writing assertions:
	 - `variables.tf`
	 - `variables.applications.tf`
	 - `variables.identity.tf`
	 - relevant child-module variable files when needed
2. Prefer expanding an existing `run` block in a test file instead of creating new blocks unless logic is meaningfully different.
3. The first `run` blocks in Station tests should be setup/bootstrap runs (for dynamic IDs/resources needed by main runs).
4. Use setup outputs to override placeholder values in the main test `variables` block(s).
5. Validate both minimum and maximum configurations for each feature (plus extra scenarios when options are mutually exclusive).
6. Run `terraform fmt -recursive` before finishing.
7. Do **not** run `terraform validate` for this repository (module + provider alias limitation).

## Expected Station test structure

Use this shape unless a feature needs a justified variation:

1. Provider declarations:
	 - `provider "tfe" {}`
	 - `provider "azuread" {}`
	 - `provider "azurerm" { features {} }`
	 - `provider "azurerm" { alias = "connectivity" ... }`
2. `test { parallel = true }`
3. Bootstrap/setup `run` blocks
4. File-level `variables` with placeholders such as `"# Overridden"` or `"This has to be overridden"`
5. Main `run` block(s) with:
	 - `module { source = "./" }`
	 - `variables` overrides using `merge(...)` and values from setup runs
	 - `assert` blocks with clear `error_message`

## Setup modules and when to use them

- `tests/setup-common`:
	- common tenant/subscription/identity data
	- frequently used for Graph/service principal data and current caller context
- `tests/setup-tfe-project`:
	- creates a dedicated TFC project for the test
	- output `id` is used to override `var.tfe.project.id`
- `tests/setup-application`:
	- bootstraps resource object IDs used by `required_resource_access`
- `tests/setup-groups`:
	- creates user/group fixtures for group membership scenarios
- `tests/setup-entraid`:
	- creates Entra ID fixtures for identity-related tests
- `tests/setup-peering-networks`:
	- creates remote VNet used by connectivity peering tests
- `tests/setup-uai`:
	- creates fixtures for UAI role/group assignment scenarios

## Canonical override patterns

Use these exact ideas when placeholders exist in file-level variables.

### Override TFC project ID

In main runs:

`tfe = merge(var.tfe, { project = merge(var.tfe.project, { id = run.bootstrap_create_tfc_test_project.id }) })`

### Override setup-generated object IDs

For app tests and similar cases, map outputs from setup runs into nested feature objects with `merge(...)`.

Examples:
- owners from current identity object ID
- `required_resource_access.*.resource_object_id` from setup run outputs
- connectivity peering `remote_virtual_network_id` from setup network output

## How to add or update a Station feature test

1. Identify affected feature inputs and outputs in root module files.
2. Reuse an existing feature test file if one exists.
3. Ensure setup runs exist for all dynamic dependencies.
4. Add/adjust file-level `variables` to include:
	 - minimal scenario
	 - maximum scenario
	 - extra scenario(s) only when needed
5. In main run `variables`, override placeholders from setup outputs.
6. Add assertions for:
	 - input-to-resource/output mapping
	 - default behavior
	 - optional behavior in maximum scenario
	 - required identity/app role/directory role behavior where relevant
7. Keep assertion messages specific and actionable.
8. Format and run targeted tests.

## Assertions guidance (Station-specific)

- Prefer deterministic checks over brittle string comparisons.
- Use `alltrue([...])` when validating repeated patterns across maps.
- For sensitive TFE vars, assert unreadable value behavior (`value == ""`) and `sensitive == true`.
- Where appropriate, assert role assignments required by configured feature blocks (for example when `var.applications` or `var.groups` is set).
- If comparing structured HCL-like serialized output, normalize/parse before assertion (as done in existing `tests/tfe.tftest.hcl`).

## Commands

### Local prerequisites

- Azure CLI authenticated to correct tenant/subscription
- Terraform CLI installed
- Terraform Cloud credentials available
- Environment variables provided through a repo-root `.agent.test.env` file (copy from `.agent.test.env.example`)

### Environment variable policy (required)

To avoid polluting shell state, never rely on globally exported variables for test runs.

Use this policy:
1. Keep all required variables in `./.agent.test.env` (repo root).
2. For **every** Terraform command, source `.agent.test.env` inside a short-lived shell.
3. Do not run `export ...` directly in the interactive terminal session.

Agent workflow when asked to run tests:
1. Check whether `./.agent.test.env` exists.
2. If missing, create it from `./.agent.test.env.example`.
3. Stop and ask the user to fill real values in `./.agent.test.env` before continuing.
4. Run Azure context preflight check (`.agents/skills/terraform-station-test/scripts/check-az-context.sh`) before Terraform commands.
5. Run Terraform commands only via the short-lived shell pattern below.

Existence/bootstrap command:

```bash
if [ ! -f ./.agent.test.env ]; then cp ./.agent.test.env.example ./.agent.test.env; echo "Created .agent.test.env from template. Fill values and re-run."; exit 1; fi
```

Azure context preflight command:

```bash
sh ./.agents/skills/terraform-station-test/scripts/check-az-context.sh ./.agent.test.env
```

This check ensures all of the following before tests proceed:
- `az` is installed
- user is logged in
- logged-in tenant matches `TF_VAR_tenant_id`
- active subscription matches `TF_VAR_subscription_id`
- `TF_VAR_subscription_id` equals `ARM_SUBSCRIPTION_ID`
- `TFE_TOKEN` is set for Terraform Cloud operations (including teardown)

Important: this does **not** force re-login each test. It only validates current context and fails fast when mismatched.

Preferred command pattern:

```bash
sh -c '. ./.agent.test.env; terraform <command>'
```

This keeps the environment scoped to that command only.

### Typical workflow

```bash
sh ./.agents/skills/terraform-station-test/scripts/check-az-context.sh ./.agent.test.env
sh -c '. ./.agent.test.env; terraform init'
sh -c '. ./.agent.test.env; terraform fmt -recursive'
sh -c '. ./.agent.test.env; terraform test -filter=tests/<feature>.tftest.hcl'
```

Run all tests only when needed:

```bash
sh -c '. ./.agent.test.env; terraform test'
```

Quick preflight check:

```bash
sh -c '. ./.agent.test.env; env | grep -E "^(ARM_SUBSCRIPTION_ID|TF_VAR_subscription_id|TF_VAR_tenant_id|TFE_ORGANIZATION|TF_VAR_tfc_organization_name|TF_VAR_tfc_project_name)="'

# Optional explicit check for TFE token presence
sh -c '. ./.agent.test.env; test -n "${TFE_TOKEN:-}" && echo "TFE_TOKEN set" || (echo "TFE_TOKEN missing"; exit 1)'
```

## CI behavior you must respect

CI uses selective test execution (`.github/scripts/determine-tests.sh`).

Implications:
- If you change only one feature area, prefer updating only that feature's test file.
- If you change core files or setup modules, expect all tests to run.
- If needed on PRs, maintainers can trigger all tests with `/test-all` or `/test all`.

Reference mapping docs:
- `.github/scripts/README.md`
- `.github/workflows/terraform.yaml`

## Definition of done for test changes

- Test file follows Station structure and style used in existing `tests/*.tftest.hcl`
- Setup runs are present and outputs are used for dynamic overrides
- Minimum + maximum scenarios are covered (plus extra scenarios when justified)
- Assertions verify key behavior and required side effects
- `terraform fmt -recursive` has been run
- Relevant `terraform test -filter=...` command has been run (or command provided if execution is not possible)

## When to ask for clarification

Ask before implementation only if one of these is unclear:
- Which feature/test file should be updated
- Whether new behavior is minimum, maximum, or separate scenario
- Whether setup fixture changes are acceptable
- Whether CI-impacting broad changes are intended

## Copy/paste test skeletons

Use these as starting points and adjust names/variables/assertions to your feature.

### Skeleton 1: New Station feature test file

```hcl
provider "tfe" {}

provider "azuread" {}

provider "azurerm" {
	features {}
}

provider "azurerm" {
	alias = "connectivity"
	features {}
}

test {
	parallel = true
}

run "bootstrap_create_tfc_test_project" {
	variables {
		tfc_project_name = "tests_<feature>"
	}

	module {
		source = "./tests/setup-tfe-project"
	}
}

run "setup" {
	module {
		source = "./tests/setup-common"
	}
}

variables {
	tfe = {
		project = {
			id   = "# Overridden"
			name = "tests_<feature>"
		}
		organization_name     = "<org>"
		workspace_name        = "<feature>-test"
		workspace_description = "Station test for <feature>"
		workspace_settings = {
			execution_mode = "remote"
		}
	}

	<feature> = {
		minimum = {
			# required fields only
		}
		maximum = {
			# required + optional fields
		}
	}
}

run "<feature>-main" {
	variables {
		tfe = merge(var.tfe, {
			project = merge(var.tfe.project, {
				id = run.bootstrap_create_tfc_test_project.id
			})
		})
	}

	module {
		source = "./"
	}

	assert {
		condition     = true
		error_message = "Replace with real assertion for minimum scenario"
	}

	assert {
		condition     = true
		error_message = "Replace with real assertion for maximum scenario"
	}
}
```

### Skeleton 2: Dynamic override pattern from setup outputs

Use this pattern when file-level values must be replaced by IDs from setup runs.

```hcl
run "<feature>-main" {
	variables {
		<feature> = merge(var.<feature>, {
			maximum = merge(var.<feature>.maximum, {
				owners = [run.setup.azuread_client_config.current.object_id]

				required_resource_access = merge(var.<feature>.maximum.required_resource_access, {
					graph = merge(var.<feature>.maximum.required_resource_access.graph, {
						resource_object_id = run.bootstrap_application.MicrosoftGraph.object_id
					})
				})
			})
		})

		tfe = merge(var.tfe, {
			project = merge(var.tfe.project, {
				id = run.bootstrap_create_tfc_test_project.id
			})
		})
	}

	module {
		source = "./"
	}
}
```

### Skeleton 3: Expected failure validation

Use when you intentionally verify input validation behavior.

```hcl
run "<feature>-invalid-input" {
	command = plan

	variables {
		<feature> = {
			minimum = {
				# intentionally invalid value
			}
		}
	}

	module {
		source = "./"
	}

	expect_failures = [
		var.<feature>
	]
}
```

After adapting a skeleton:
- run `sh -c '. ./.agent.test.env; terraform fmt -recursive'`
- run `sh -c '. ./.agent.test.env; terraform test -filter=tests/<feature>.tftest.hcl'`
- add tighter assertions before opening a PR

