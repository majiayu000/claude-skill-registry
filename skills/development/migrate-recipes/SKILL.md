---
name: migrate-recipes
description: Apply versioned migration notes to an AutoSkillit recipe. Use when user confirms migration, called by agent or autoskillit migrate CLI, or invoked directly.
---

# Migrate Scripts Skill

Apply versioned migration notes to an AutoSkillit recipe.

## When to Use

- Called by an agent when user confirms migration (via load_recipe suggestion)
- Called by `autoskillit migrate` CLI command via `run_skill`
- Can be invoked directly by user

## Arguments

The orchestrator provides all context in the prompt:
- `script_path`: Absolute path to the script file
- `script_content`: Current raw YAML of the script
- `migration_notes`: YAML block of all applicable migration notes
- `target_version`: Version to stamp after successful migration

## Critical Constraints

**NEVER:**
- Modify the original script file directly
- Skip validation via validate_recipe
- Apply changes without checking if the pattern exists in the script
- Declare success if validation fails after all retry attempts

**ALWAYS:**
- Save migrated scripts to .autoskillit/temp/migrations/{script_name}.yaml for review
- Validate via validate_recipe before declaring success
- Preserve all existing script fields not targeted by migration changes
- Output a human-readable diff summary of changes applied

## Workflow

1. Parse the migration notes to understand what changes are needed
2. For each change, check if the script contains the outdated pattern described in `detect`:
   - `tool`: Match steps with this tool value
   - `skill_pattern`: Match steps whose `skill_command` in `with:` contains this substring
   - `missing_field`: The field that should be added if absent
3. If changes are needed, use `/autoskillit:write-recipe` in edit mode:
   - Load the skill: invoke `/autoskillit:write-recipe` via the Skill tool
   - Provide the current YAML content
   - Describe all needed changes with the `instruction` text and before/after examples
4. Validate the result with `validate_recipe`
5. On validation failure, retry up to 3 times with error feedback
6. Ensure `autoskillit_version` is set to the `target_version`
7. Save the migrated script to `.autoskillit/temp/migrations/{script_name}.yaml`
8. Output a summary of changes applied

## Error Handling

- If all 3 retry attempts fail validation, output the best attempt with a clear warning
- If no patterns are detected (script already up to date), stamp the version and report no changes needed
- If write-recipe produces unexpected output, report the error and preserve the original script

## Failure Persistence

If all 3 retry attempts are exhausted without a valid result, BEFORE declaring failure
you MUST persist the failure record:

  run_python:
    callable: autoskillit.migration.store.record_from_skill
    args:
      name: {recipe stem, e.g. "my-pipeline"}
      file_path: {absolute path received as script_path argument}
      file_type: recipe
      error: {description of last validation error}
      retries_attempted: 3

After recording, output a clear failure summary and stop.
