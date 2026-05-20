---
title: "Facets Modules Validate"
description: "Validate changed Facets modules: lint against all rules defined in rules.md AND run raptor dry-run. Auto-detects changed modules from git diff."
triggers: ["facets-modules-validate", "validate against rules", "check rules", "rules validation", "lint modules", "module lint"]
version: "1.0"
category: "validation"
tags: ["validation", "rules", "module", "quality"]
icon: "shield"
---

# Facets Modules Validation

**IMPORTANT:** This skill does TWO things: (1) validates modules against all rules in `rules.md` by reading and analyzing the module files directly, and (2) runs `raptor create iac-module --dry-run` for each module. Both checks must pass.

Validate changed Facets modules against the project's `rules.md` validation ruleset.

---

## Step 1: Determine which modules to validate

Identify the set of modules to validate, in priority order:

1. **If the user passed a module path as argument** → use that path directly
2. **If on a PR branch** (not `main`) → run `git diff origin/main --name-only` to get all changed files vs main, then extract unique module directories
3. **Otherwise** → run `git diff --name-only` (unstaged) and `git diff --cached --name-only` (staged) to get locally changed files, then extract unique module directories

**Extracting module paths:** A module directory is any directory that contains a `facets.yaml` file. For each changed file, walk up its path to find the nearest `facets.yaml`. The module path is that directory (e.g., `modules/datastore/postgres/aws-rds/1.0/`).

Deduplicate the list. If no modules are found, inform the user and stop.

Print the list of modules that will be validated before proceeding.

---

## Step 2: Read rules.md and module files

1. **Read `rules.md`** from the repo root — this contains all validation rules
2. **For each module**, read:
   - `facets.yaml`
   - All `.tf` files in that module directory (`variables.tf`, `main.tf`, `outputs.tf`, `locals.tf`, `versions.tf`, etc.)
   - The relevant **output type schemas** from `outputs/` based on the output types declared in `facets.yaml` outputs section (e.g., if output type is `@facets/eks`, check `outputs/eks/outputs.yaml`; if `@outputs/postgres`, check `outputs/postgres/outputs.yaml`)

---

## Step 3: Validate each module against applicable rules

For each module, check **every rule** from `rules.md` (RULE-001 through the last defined rule). Use the rule's category and description to determine if it applies to the module being validated:

- **Skip** rules whose category doesn't apply (e.g., skip "output schema" rules if the module has no output type schemas in `outputs/`)
- **Check** all applicable rules and record PASS/FAIL/SKIP with a brief finding

The rules in `rules.md` contain all the detail needed — category, description, and good/bad examples. Do NOT hardcode rule numbers or descriptions here; always read `rules.md` at validation time to pick up any newly added rules.

---

## Step 4: Run raptor dry-run validation

For each detected module, run:

```bash
export FACETS_PROFILE=1155708878 && raptor create iac-module -f <module-path> --dry-run
```

- If the raptor dry-run **fails due to security scan**, retry with `--skip-security-scan` but report the security findings to the user in a table
- If the raptor dry-run fails for other reasons (provider issues, schema errors, etc.), report the error
- Record each module's raptor result (PASS / FAIL + error details) for the final report

---

## Step 5: Report results

### Per-module report

For each validated module, output a report in this format:

```
## modules/datastore/postgres/aws-rds/1.0

| Rule | Status | Finding |
|------|--------|---------|
| RULE-001 | PASS | — |
| RULE-002 | PASS | — |
| RULE-003 | SKIP | No sample values to check |
| RULE-004 | FAIL | var.inputs uses `type = any` instead of explicit object type |
| RULE-005 | PASS | — |
| ... | ... | ... |
| RULE-024 | SKIP | No cloud resources with names |
| Raptor dry-run | PASS/FAIL | Result or error details |

X passed, Y failed, Z skipped.
```

**Status values:**
- **PASS** — Rule checked and satisfied
- **FAIL** — Rule checked and violation found (include specific finding)
- **SKIP** — Rule not applicable to this module (include brief reason)

### Summary (if multiple modules)

After all per-module reports, output a summary:

```
## Summary

| Module | Passed | Failed | Skipped |
|--------|--------|--------|---------|
| modules/datastore/postgres/aws-rds/1.0 | 18 | 2 | 4 |
| modules/service/aws/1.0 | 20 | 0 | 4 |
| **Total** | **38** | **2** | **8** |
```

If all modules pass, add a confirmation message. If any fail, list the critical failures that should be fixed before commit.

---

## Step 6: Recommend new rules (if applicable)

During validation, if you encounter any of the following that are NOT covered by existing rules in `rules.md`:
- A new anti-pattern seen across multiple modules
- A validation gap (something raptor catches but rules.md doesn't cover)
- A convention that modules follow inconsistently

Propose a new rule to the user in the standard format:
- Rule number: next available (RULE-025, RULE-026, etc.)
- Category, description, bad example, good example
- Do NOT modify rules.md automatically — present the proposal and wait for approval
