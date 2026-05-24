---
name: parallel-run
description: Orchestrate parallel agent execution with git worktrees
argument-hint: <parallel-dir> [--validate] [--status]
---

# parallel-run

**Category**: Parallel Development

## Usage

```bash
/parallel-run <parallel-dir> [options]
```

## Arguments

- `<parallel-dir>`: Required - Path to decomposed parallel folder (e.g., `parallel/TS-0042-inventory/`)
- `--validate`: Only validate the directory without executing
- `--status`: Show current execution status

## Purpose

Execute parallel agent development tasks using the `cpo` (Claude Parallel Orchestrator) CLI tool. This command:
1. Validates the parallel directory and manifest.json
2. Executes parallel agents using git worktrees
3. Monitors progress and reports results

## Prerequisites

- Run `/parallel-decompose` first (creates tasks, prompts, manifest.json)
- `cpo` tool installed: `pip install claude-parallel-orchestrator` or `pipx install claude-parallel-orchestrator`
- Git working tree is clean (no uncommitted changes)
- Claude Code CLI available: `claude --version`

---

## Execution Instructions for Claude Code

When this command is run, Claude Code should delegate to the `cpo` CLI tool.

### 0. Parse Arguments

Extract from user input:
- `PARALLEL_DIR`: The parallel directory path
- `VALIDATE_ONLY`: Boolean, true if `--validate` specified
- `STATUS_ONLY`: Boolean, true if `--status` specified

### 1. Check cpo Tool Availability

```bash
cpo --help
```

If `cpo` is not installed, display:
```
ERROR: cpo (Claude Parallel Orchestrator) not found

Install with:
  pip install claude-parallel-orchestrator
  # or
  pipx install claude-parallel-orchestrator

Documentation: https://github.com/jpoutrin/claude-parallel-orchestrator
```

### 2. Handle --validate Option

If `--validate` is specified:

```bash
cpo validate "$PARALLEL_DIR"
```

Display the validation output and stop.

### 3. Handle --status Option

If `--status` is specified:

```bash
cpo status "$PARALLEL_DIR"
```

Display the status output and stop.

### 4. Run Parallel Execution

For default execution (no special flags):

```bash
cpo run "$PARALLEL_DIR"
```

The `cpo run` command will:
1. Validate the manifest.json
2. Create git worktrees for each task
3. Launch Claude agents in parallel (respecting wave dependencies)
4. Monitor progress and handle failures
5. Generate execution logs in `$PARALLEL_DIR/logs/`
6. Create final report in `$PARALLEL_DIR/report.json`

### 5. Monitor and Report Progress

The `cpo run` command outputs progress to stdout. Parse and display:

```
=== Parallel Execution Started ===

Wave 1:
  task-001-users: RUNNING
  task-002-products: RUNNING
  task-003-shared: RUNNING

[... cpo output continues ...]

=== Execution Complete ===

Results:
  Completed: 5/5 tasks
  Failed: 0 tasks

Next step: /parallel-integrate --parallel-dir $PARALLEL_DIR
```

---

## cpo Manifest Format

The `cpo` tool expects `manifest.json` with this structure:

```json
{
  "tech_spec_id": "TS-0042",
  "waves": [
    {
      "number": 1,
      "tasks": [
        {
          "id": "task-001-users",
          "agent": "python-experts:django-expert",
          "prompt_file": "prompts/task-001.txt"
        },
        {
          "id": "task-002-products",
          "agent": "python-experts:django-expert",
          "prompt_file": "prompts/task-002.txt"
        }
      ],
      "validation": "python -c 'from apps.users.models import User'"
    },
    {
      "number": 2,
      "tasks": [
        {
          "id": "task-004-orders",
          "agent": "python-experts:django-expert",
          "prompt_file": "prompts/task-004.txt"
        }
      ],
      "validation": "pytest apps/orders/tests/ -v"
    }
  ]
}
```

**Key fields:**
- `tech_spec_id`: Links to Tech Spec for traceability
- `waves[].number`: Wave execution order (1, 2, 3...)
- `waves[].tasks[].id`: Unique task identifier
- `waves[].tasks[].agent`: Agent type from product-forge (e.g., `python-experts:django-expert`)
- `waves[].tasks[].prompt_file`: Path to task prompt file
- `waves[].validation`: Optional command to validate wave completion

---

## Error Handling

### cpo Not Installed

```
ERROR: cpo command not found

Install with:
  pip install claude-parallel-orchestrator

Or check PATH if already installed:
  which cpo
```

### Invalid Manifest

```
ERROR: manifest.json validation failed

Missing required fields:
  - tech_spec_id
  - waves

Run '/parallel-decompose' to regenerate the manifest.
```

### Execution Failures

The `cpo` tool handles:
1. Agent process failure -> marks task as failed, continues with independent tasks
2. Validation failure -> stops wave, reports error
3. Git conflicts -> aborts with message

Check `$PARALLEL_DIR/logs/` for detailed agent output.
Check `$PARALLEL_DIR/report.json` for execution summary.

---

## Examples

```bash
# Execute parallel tasks (default)
/parallel-run parallel/TS-0042-inventory/

# Validate manifest without executing
/parallel-run parallel/TS-0042-inventory/ --validate

# Check current execution status
/parallel-run parallel/TS-0042-inventory/ --status
```

---

## Related Commands

- `/parallel-setup` - One-time project initialization
- `/parallel-decompose` - Create tasks and prompts (run before this)
- `/parallel-validate-prompts` - Validate prompts have required sections
- `/parallel-integrate` - Verify integration (run after this)

## cpo CLI Reference

For advanced usage, use `cpo` directly:

```bash
# Initialize new parallel directory
cpo init parallel/TS-0042-feature -t TS-0042 -n feature-name

# Validate directory structure
cpo validate parallel/TS-0042-feature

# Run parallel execution
cpo run parallel/TS-0042-feature

# Check execution status
cpo status parallel/TS-0042-feature
```
