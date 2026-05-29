---
name: write-recipe
description: Generate YAML recipes for .autoskillit/recipes/. Use when user says "make script skill", "generate script", "script a workflow", "write a script", "create a script", "new recipe", "write a pipeline", or when loaded by other skills for script formatting.
---

# Make Script Skill

Format a workflow into a YAML recipe following the workflow schema.

## When to Use

- **Standalone**: User wants to create a new recipe from scratch
- **Loaded by another skill**: Another skill (e.g., setup-project) loads this via the Skill tool to format a workflow it has already discovered

## Arguments (standalone mode)

```
/autoskillit:write-recipe
```

No positional arguments. The skill prompts interactively for workflow details.

## Critical Constraints

**NEVER:**
- Create SKILL.md files (not in `.claude/commands/`, `.claude/skills/`, or anywhere else)
- Create Markdown companion files alongside the YAML script
- Create files outside `.autoskillit/recipes/` directory
- Tell the user to run a script with `/autoskillit:<name>` syntax

**ALWAYS:**
- Save the script to `.autoskillit/recipes/{name}.yaml` as the ONLY output
- Call `validate_recipe` after saving and fix any errors
- Use "recipe" terminology (not "skill script")

## How Scripts Are Loaded

Recipes have their own discovery and invocation mechanism — completely
separate from the skill system. You do not need to create anything else for the
script to be usable. The lifecycle is:

1. **You save** the YAML file to `.autoskillit/recipes/{name}.yaml`
2. **The user discovers it** via `list_recipes` MCP tool (lists all scripts in that directory)
3. **The user loads it** via `load_recipe("{name}")` MCP tool (returns raw YAML)
4. **An agent executes it** by interpreting the YAML steps and calling MCP tools directly

No SKILL.md, no slash command registration, no Markdown companion file — the YAML file
in `.autoskillit/recipes/` is the only artifact needed. The MCP tools handle everything else.

## The Script Format

Every generated script MUST follow the workflow YAML schema:

```yaml
name: {script-name}
autoskillit_version: "{version}"  # from kitchen_status.package_version
description: {One line description.}
summary: {Concise pipeline chain, e.g. "plan > verify > implement > test > merge"}

ingredients:
  var_name:
    description: {What this input is for}
    required: true          # or false
    default: {value}        # optional

steps:
  step_name:
    tool: {mcp_tool_name}
    with:
      arg1: "${{ inputs.var_name }}"
      arg2: "literal value"
    capture:                # optional — extract values for later steps
      var_name: "${{ result.field_name }}"
    on_success: next_step
    on_failure: escalate
    retry:                  # optional
      max_attempts: 3
      on: needs_retry
      on_exhausted: escalate
  done:
    action: stop
    message: "Pipeline complete."
  escalate:
    action: stop
    message: "Failed — human intervention needed."
```

## Format Rules

- **Top-level fields**: `name`, `autoskillit_version` (stamped), `description`, `summary` (required), `inputs`, `steps`
- **Inputs**: each with `description`, optional `required` (default false) and `default`
- **Steps**: each has either `tool` (MCP tool call) or `action` (terminal: `stop`)
- **Tool steps**: use `with:` for arguments, `on_success`/`on_failure` for routing
- **Terminal steps**: have `action: stop` and a `message:`
- **Routing targets**: must reference other step names defined in the same file
- **Variable substitution**: use `${{ inputs.var_name }}` for declared inputs and `${{ context.var_name }}` for values captured by preceding steps
- **Retry blocks**: optional, specify `max_attempts`, `on` (condition field), `on_exhausted` (step name)
- **Summary**: one line, use `>` to chain steps (e.g., "plan > verify > implement > test > merge")

## Complete Schema Reference

### Top-Level Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `name` | Yes | string | Unique identifier; validation fails if empty |
| `autoskillit_version` | No | string | Package version that generated this script. Set from `kitchen_status.package_version`. Used by migration system to detect outdated scripts. |
| `description` | Yes | string | Human-readable, shown in listings |
| `summary` | Yes | string | Pipeline chain shown in `list_recipes` output |
| `inputs` | No | mapping | Omit if the script has no configurable values |
| `kitchen_rules` | Yes | list[str] | Orchestrator discipline rules. Must enumerate forbidden native tools (Read, Grep, Glob, Edit, Write, Bash, Task, Explore, WebFetch, WebSearch, NotebookEdit). |
| `steps` | Yes | mapping | At least one step required |

### Input Fields

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `description` | No | `""` | What this input is for |
| `required` | No | `false` | Whether the agent must prompt for it |
| `default` | No | `null` | Value used when not provided |

### Tool Step Fields

| Field | Required | Notes |
|-------|----------|-------|
| `tool` | Yes (xor `action`) | MCP tool name (see Tool Reference below) |
| `with` | No | Arguments passed to the tool; values support `${{ inputs.X }}` and `${{ context.X }}` |
| `on_success` | No | Step name to route to on success, or `"done"` |
| `on_failure` | No | Step name to route to on failure |
| `capture` | No | Map of `context_var` → `${{ result.field }}` expressions. Captured values available to later steps via `${{ context.var }}` |
| `retry` | No | Retry block (see below) |
| `note` | No | Human-readable annotation for the agent; not executed |

### Terminal Step Fields

| Field | Required | Notes |
|-------|----------|-------|
| `action` | Yes (xor `tool`) | Must be `"stop"` |
| `message` | Yes | Displayed to the agent when this step is reached |

### Retry Block Fields

| Field | Default | Notes |
|-------|---------|-------|
| `max_attempts` | `3` | How many times to retry before giving up |
| `on` | `null` | Response field to check. Valid values: `exit_code`, `is_error`, `needs_retry`, `result`, `retry_reason`, `session_id`, `subtype` |
| `on_exhausted` | `"escalate"` | Step name to jump to when retries run out |

### Capture Field

Extracts values from tool results into a pipeline-scoped context dict. Subsequent steps reference captured values via `${{ context.var_name }}`.

| Field | Type | Notes |
|-------|------|-------|
| `capture` | mapping | Keys are context variable names; values must be `${{ result.field }}` expressions |

**Rules:**
- Values must contain `${{ result.* }}` expressions (literals and other namespaces are rejected)
- Dotted result paths are valid (e.g., `${{ result.data.path }}`)
- Captured variables become available to steps that appear *after* the capturing step
- A step cannot reference its own capture — only preceding steps' captures

**Example:**
```yaml
steps:
  implement:
    tool: run_skill
    with:
      skill_command: "/autoskillit:implement-worktree-no-merge ${{ context.plan_path }}"
      cwd: "."
    capture:
      worktree_path: "${{ result.worktree_path }}"
    on_success: test
  test:
    tool: test_check
    with:
      worktree_path: "${{ context.worktree_path }}"
```

### Validation Rules

The system validates scripts against these rules:
1. `name` must be non-empty
2. `steps` must contain at least one step
3. Each step must have exactly one of `tool` or `action` (not both, not neither)
4. Terminal steps (`action: stop`) must have a `message`
5. `on_success` and `on_failure` targets must reference a step name defined in the file, or the literal `"done"`
6. `retry.on_exhausted` must reference a defined step name
7. `retry.on` must be one of the valid response fields listed above
8. All `${{ inputs.X }}` references must match a declared input name
9. `capture` values must contain `${{ result.* }}` expressions
10. `capture` values must only use the `result.*` namespace
11. `${{ context.X }}` references must point to a variable captured by a preceding step
12. `run_skill` steps should have a `capture:` block to explicitly wire outputs (warning: `IMPLICIT_HANDOFF`)
13. All captured variables should be consumed by at least one reachable downstream step via `${{ context.X }}` (warning: `DEAD_OUTPUT`)

## MCP Tool Reference

Available tools for use in `tool:` fields:

| Tool | Arguments (`with:`) | Purpose |
|------|---------------------|---------|
| `run_skill` | `skill_command`, `cwd`, `model` (optional), `step_name` (optional) | Run a Claude Code headless session with a skill |
| `test_check` | `worktree_path` | Run test suite, returns PASS/FAIL |
| `merge_worktree` | `worktree_path`, `base_branch` | Merge after test gate |
| `reset_test_dir` | `test_dir`, `force` (optional, default false) | Clear test directory (requires reset guard marker) |
| `classify_fix` | `worktree_path`, `base_branch` | Analyze diff for restart scope (full vs partial) |
| `reset_workspace` | `test_dir` | Reset workspace, preserving configured directories |
| `run_cmd` | `cmd`, `cwd`, `timeout` (optional) | Execute arbitrary shell command |
| `validate_recipe` | `script_path` | Validate a script file against the workflow schema |

## Bundled AutoSkillit Skills

These skills ship with the autoskillit plugin and are invoked as `/autoskillit:<name>`:

analyze-prs, arch-lens-c4-container, arch-lens-concurrency, arch-lens-data-lineage, arch-lens-deployment,
arch-lens-development, arch-lens-error-resilience, arch-lens-module-dependency, arch-lens-operational,
arch-lens-process-flow, arch-lens-repository-access, arch-lens-scenarios, arch-lens-security, arch-lens-state-lifecycle,
audit-arch, audit-bugs, audit-cohesion, audit-defense-standards, audit-friction, audit-impl, audit-tests,
close-kitchen, collapse-issues, design-guards, diagnose-ci, dry-walkthrough, elaborate-phase,
enrich-issues, implement-worktree, implement-worktree-no-merge, investigate, issue-splitter, make-arch-diag,
make-groups, make-plan, make-req, merge-pr, mermaid, migrate-recipes, open-integration-pr, open-kitchen, open-pr, open-pr-main, pipeline-summary,
prepare-issue, process-issues, rectify, report-bug, resolve-failures, resolve-merge-conflicts, resolve-review,
retry-worktree, review-approach, review-pr, setup-project, smoke-task, sprint-planner, triage-issues, verify-diag, write-recipe

## Skill Reference Disambiguation

When the user describes a workflow using bare skill names (e.g., "use make-plan",
"then run investigate"), you MUST resolve each name before writing it into the YAML.

### Resolution procedure

For each bare skill name the user mentions:

1. **Check local**: Does `.claude/skills/<name>/SKILL.md` exist in the project directory?
2. **Check bundled**: Is `<name>` in the Bundled AutoSkillit Skills list above?
3. **Resolve**:
   - **Local only** → use `/<name>` (bare slash command)
   - **Bundled only** → use `/autoskillit:<name>`
   - **Both exist** → prompt the user:
     > "I see `<name>` exists as both a local project skill (`/<name>`) and a
     > bundled AutoSkillit skill (`/autoskillit:<name>`). Which should this script
     > use? The local version is recommended since it's tailored to your project."
   - **Neither exists** → warn the user that the skill wasn't found and ask them
     to clarify the correct name or path

### Defaults

- **Local always takes priority** when the user doesn't express a preference.
- Only prompt when both sources provide the same name. Don't prompt for names
  that exist in only one source.

## Example: Standard Implementation Pipeline

This is the reference format. All generated scripts should match this style:

```yaml
name: implementation
description: Plan, verify, implement, test, and merge a task.
summary: make-plan > dry-walk > implement > test > merge

kitchen_rules:
  - "NEVER use native Claude Code tools (Read, Grep, Glob, Edit, Write,
    Bash, Task, Explore, WebFetch, WebSearch, NotebookEdit) from the
    orchestrator. All work is delegated through run_skill."
  - "Route to on_failure when a step fails — do not investigate directly."

ingredients:
  task:
    description: What to implement
    required: true
  project_dir:
    description: Path to the project
    required: true
  work_dir:
    description: Working directory (can be same as project_dir)
    default: "."
  base_branch:
    description: Branch to merge into
    default: integration

steps:
  plan:
    tool: run_skill
    with:
      skill_command: "/autoskillit:make-plan ${{ inputs.task }}"
      cwd: "${{ inputs.work_dir }}"
    capture:
      plan_path: "${{ result.plan_path }}"
    on_success: verify
    on_failure: escalate
  verify:
    tool: run_skill
    with:
      skill_command: "/autoskillit:dry-walkthrough ${{ context.plan_path }}"
      cwd: "${{ inputs.work_dir }}"
    on_success: implement
    on_failure: escalate
  implement:
    tool: run_skill
    with:
      skill_command: "/autoskillit:implement-worktree-no-merge ${{ context.plan_path }}"
      cwd: "${{ inputs.work_dir }}"
    capture:
      worktree_path: "${{ result.worktree_path }}"
    retries: 0
    on_context_limit: retry_worktree
    on_success: test
    on_failure: escalate
  retry_worktree:
    tool: run_skill
    with:
      skill_command: "/autoskillit:retry-worktree ${{ context.plan_path }} ${{ context.worktree_path }}"
      cwd: "${{ context.worktree_path }}"
    on_success: test
    on_failure: escalate
  test:
    tool: test_check
    with:
      worktree_path: "${{ context.worktree_path }}"
    on_success: merge
    on_failure: fix
  merge:
    tool: merge_worktree
    with:
      worktree_path: "${{ context.worktree_path }}"
      base_branch: "${{ inputs.base_branch }}"
    on_success: done
    on_failure: escalate
  fix:
    tool: run_skill
    with:
      skill_command: "/autoskillit:resolve-failures ${{ context.worktree_path }} ${{ context.plan_path }} ${{ inputs.base_branch }}"
      cwd: "${{ inputs.work_dir }}"
    on_success: done
    on_failure: escalate
  done:
    action: stop
    message: "Implementation complete."
  escalate:
    action: stop
    message: "Failed — human intervention needed."
```

## Example: Loop with Fix Step

A condensed bugfix loop showing retry, classify, and routing patterns:

```yaml
name: example-loop
description: Test, fix, and merge with automatic retry.
summary: test > investigate > plan > implement > verify > merge

kitchen_rules:
  - "NEVER use native Claude Code tools (Read, Grep, Glob, Edit, Write,
    Bash, Task, Explore, WebFetch, WebSearch, NotebookEdit) from the
    orchestrator. All work is delegated through run_skill."
  - "Route to on_failure when a step fails — do not investigate directly."

ingredients:
  test_dir:
    description: Directory containing the project to test
    required: true
  base_branch:
    description: Branch to merge fixes into
    default: integration
  helper_dir:
    description: Directory for helper agent sessions
    required: true

steps:
  test:
    tool: test_check
    with:
      worktree_path: "${{ inputs.test_dir }}"
    on_success: done
    on_failure: investigate

  investigate:
    tool: run_skill
    with:
      skill_command: "/autoskillit:investigate the test failures"
      cwd: "${{ inputs.helper_dir }}"
    on_success: plan
    on_failure: escalate

  plan:
    tool: run_skill
    with:
      skill_command: "/autoskillit:rectify the investigation findings"
      cwd: "${{ inputs.helper_dir }}"
    capture:
      plan_path: "${{ result.plan_path }}"
    on_success: implement
    on_failure: escalate

  implement:
    tool: run_skill
    with:
      skill_command: "/autoskillit:implement-worktree-no-merge ${{ context.plan_path }}"
      cwd: "${{ inputs.helper_dir }}"
    retries: 0
    on_context_limit: escalate
    on_success: verify
    on_failure: escalate

  verify:
    tool: test_check
    with:
      worktree_path: "${{ inputs.test_dir }}"
    on_success: merge
    on_failure: classify
    note: Re-test after implementation. If still failing, classify the fix scope.

  classify:
    tool: classify_fix
    with:
      worktree_path: "${{ inputs.test_dir }}"
      base_branch: "${{ inputs.base_branch }}"
    note: If full_restart, go back to investigate. If partial_restart, go back to implement.
    on_success: merge
    on_failure: escalate

  merge:
    tool: merge_worktree
    with:
      worktree_path: "${{ inputs.test_dir }}"
      base_branch: "${{ inputs.base_branch }}"
    on_success: done
    on_failure: escalate

  done:
    action: stop
    message: "All tests passing. Fix merged successfully."

  escalate:
    action: stop
    message: "Human intervention needed. Review the latest output for details."
```

## Converting Legacy Markdown Commands to YAML

When converting old `.claude/commands/` or `.claude/skills/` Markdown recipes to YAML:

### Mapping Table

| Markdown Pattern | YAML Equivalent |
|------------------|-----------------|
| `SETUP:` block with `var = value` | `inputs:` block with `description`, `required`, `default` |
| Hardcoded paths in SETUP | `required: true` inputs (never hardcode paths) |
| `PIPELINE:` numbered steps | `steps:` keyed by descriptive name |
| `run_skill("/skill-name ...", cwd=...)` | `tool: run_skill` with `with: {skill_command: "...", cwd: "..."}` |
| `run_skill(...)` with retry | `tool: run_skill` with `retries:` field |
| `→ ESCALATE` / prose failure routing | `on_failure: escalate` |
| `PASS → next step` | `on_success: next_step` |
| `FAIL → fix attempt` | `on_failure: fix` |
| `Repeat up to 3x, then ESCALATE` | `retry: {max_attempts: 3, on: needs_retry, on_exhausted: escalate}` |
| `IF condition:` branching | Multiple steps with `on_success`/`on_failure` routing |
| `FOR each part:` loops | Not representable in YAML schema — add a `note:` explaining the loop for the agent |
| Prose `Notes:` section | `note:` field on individual steps, or comments in YAML |
| `AskUserQuestion` prompts | Not in schema — the agent handles prompting before executing the script |
| `review_approach = false (optional)` | Input with `required: false` and `default: "false"` |
| Local skill refs (bare `skill-name`) | Follow the **Skill Reference Disambiguation** procedure above to resolve |

### What Cannot Be Directly Represented

Some Markdown patterns require agent interpretation rather than YAML structure:

- **Multi-part plan loops** (`FOR each plan_part`): Add a `note:` to the implement step explaining that the agent should glob for plan parts and iterate
- **Conditional steps** (`IF review_approach == true`): Use an input with a default and add a `note:` explaining the conditional

### Conversion Checklist

1. Extract inputs from `SETUP:` block — remove hardcoded paths, make them `required: true`
2. Map each numbered pipeline step to a named YAML step
3. Resolve skill references — for each skill name, follow the Skill Reference Disambiguation procedure
4. Identify which MCP tool each step calls (see Tool Reference above)
5. Set `on_success` / `on_failure` routing for every tool step
6. Add `retry:` blocks where the Markdown says "repeat" or "retry"
7. Add terminal `done` and `escalate` steps
8. Write a `summary:` line capturing the pipeline chain
9. Add `note:` fields for agent-interpreted logic (loops, conditionals)

## Standalone Invocation Flow

When called directly as `/autoskillit:write-recipe`:

1. Ask the user what workflow they want to script (name, what it does)
2. Ask whether it's a linear pipeline or a loop with a fix step
3. Ask for the tool calls and routing (which MCP tools, what order, what conditions)
4. Ask for inputs (what's configurable)
5. Generate the script in the YAML format above
6. Before saving, call `kitchen_status` to get `package_version` and stamp `autoskillit_version: "{package_version}"` as the second top-level field (after `name`). This is required for the migration system to track script age.
7. Save to `.autoskillit/recipes/{name}.yaml` (create the directory if needed)
8. Call `validate_recipe` with the saved file path. If errors are returned, fix them and re-validate until clean. Review the `quality.warnings` in the response:
   - `DEAD_OUTPUT`: A `capture:` key is never referenced by any reachable downstream step via `${{ context.X }}`. Either add a `${{ context.X }}` reference in the downstream step's `with:` block, or remove the unused capture.
   - `IMPLICIT_HANDOFF`: A `run_skill` step has no `capture:` block. Add a `capture:` block to explicitly wire outputs to downstream steps via `${{ context.X }}`, or confirm the skill's output is intentionally unused.
   - Present the quality summary to the user and fix any warnings that indicate broken wiring.
9. After validation passes, generate the pipeline contract file by calling `generate_recipe_card` on the saved script. This creates `.autoskillit/recipes/contracts/{name}.yaml` alongside the recipe. Use `run_python` with `autoskillit.recipe.contracts.generate_recipe_card` passing the script path and scripts directory, or rely on `load_recipe` which auto-generates contracts on first load.
10. Tell the user: "Saved to `.autoskillit/recipes/{name}.yaml`. Load it with `load_recipe("{name}")` via the MCP tool."

After telling the user, emit the structured output token as the very last line of your
text output:

```
recipe_path = {absolute_path_to_saved_recipe_file}
```

## CRITICAL: Scripts Are NOT Skills

Recipes are YAML workflow files in `.autoskillit/recipes/`. They are:
- **Loaded** via the `load_recipe` MCP tool
- **Executed** by the agent interpreting the YAML steps

They are NOT:
- Slash commands (cannot be invoked as `/autoskillit:<name>`)
- Stored in `.autoskillit/skills/` or any other directory
- Markdown files (they are `.yaml` files)

Never tell the user to run a script with `/autoskillit:<name>`. The correct
invocation is always via `load_recipe("<name>")`.

## Loaded by Another Skill

When loaded via the Skill tool by another skill (e.g., setup-project), the calling agent already has all the workflow context in its conversation. Use that context directly:

- Workflow name and description are already known
- Tool calls and routing are already determined
- Inputs are already identified

Apply the format rules above to produce the YAML script. Do not re-ask for information the calling agent has already gathered.

## Edit Mode (Loaded with Existing Script Content)

When the agent is given an existing script's YAML content and a requested change:

1. Parse the existing YAML to understand the current structure
2. Apply the requested modifications while preserving all existing fields
3. Resolve any skill references per the disambiguation procedure
4. Write the modified YAML to the target path — ask the user whether to:
   - Save changes to the original file
   - Save as a new script (prompt for name)
   - Use temporarily without saving
5. Call `validate_recipe` on the saved path
6. If errors, fix and re-validate until clean
7. Review quality warnings and fix data-flow issues before reporting changes
8. After validation passes, regenerate the pipeline contract file to reflect the changes. Use `run_python` with `autoskillit.recipe.contracts.generate_recipe_card` or rely on `load_recipe` auto-generation on next load.
9. Report the changes made

This edit mode is invoked when `load_recipe` routes the user's modification request through this skill. The skill receives the existing YAML as context.
