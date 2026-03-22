---
name: dk-local-run-spec
description: "Plan and execute an odin spec. Handles working directory, auth, nested-session detection, and post-run diagnostics. Use whenever the user wants to run a spec, test a spec, or do a smoke test. Triggers on: 'run this spec', 'test this spec', 'odin plan', 'smoke test', or /dk-local-run-spec."
argument-hint: <spec_path> [--mock] [--quick] [--exec-only <task_id>]
allowed-tools: Bash, Read
---

# /dk-local-run-spec — Spec Runner

Run the full odin spec workflow: plan, review, execute. Handles the gotchas so you don't have to remember them.

## Usage

```
/dk-local-run-spec ../sample_specs/poem_spec.md
/dk-local-run-spec ../sample_specs/poem_spec.md --quick
/dk-local-run-spec ../sample_specs/poem_spec.md --mock
/dk-local-run-spec --exec-only a1b2
```

## Arguments

Parse `$ARGUMENTS` to extract:
- **spec_path** (required unless `--exec-only`): path to the spec markdown file
- **--quick**: use `--quiet` mode (non-interactive, spinner only)
- **--mock**: pass `--mock` to exec (no backend writes)
- **--exec-only <task_id>**: skip planning, just execute a specific task

## The critical gotcha

**Odin plan/exec invokes `claude -p` as a subprocess. It cannot run from inside another Claude Code session.** Nested Claude Code calls fail silently or hang.

This skill detects the nested session and provides the user with copy-paste commands instead of trying to run them directly.

## Execution

### Step 1: Detect environment

Check if we're inside a Claude Code session:

```bash
# Claude Code sets this env var when running
echo "${CLAUDE_CODE_ENTRYPOINT:-not_set}"
```

If we're inside Claude Code (the var is set or we detect we're in an agent context), we **cannot** run odin plan/exec directly. Instead, provide copy-paste commands.

### Step 2: Resolve paths

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
WORK_DIR="$REPO_ROOT/odin/temp_test_dir"
```

Check that `temp_test_dir/` exists and has a `.env`:

```bash
ls "$WORK_DIR/.env" 2>/dev/null
```

If missing, tell the user:
```
temp_test_dir/ not found or missing .env.
Create it: cd odin && mkdir -p temp_test_dir && cp .env.example temp_test_dir/.env
Then edit temp_test_dir/.env with your ODIN_ADMIN_USER and ODIN_ADMIN_PASSWORD.
```

### Step 3: Generate commands

Build the commands based on arguments:

**Plan phase** (skip if `--exec-only`):
```bash
cd "$WORK_DIR" && odin plan <spec_path> --quiet
```

If `--quick` was passed, use `--quiet` (which implies `--auto`). Otherwise default to `--auto` for non-interactive execution.

**Review phase** (skip if `--exec-only`):
```bash
cd "$WORK_DIR" && odin specs
cd "$WORK_DIR" && odin status
```

**Exec phase**:
```bash
cd "$WORK_DIR" && odin exec <task_id> [--mock]
```

### Step 4: Output

Since we're almost always inside Claude Code (that's where this skill runs), output the commands for the user to copy-paste into a regular terminal:

```
## Spec Run Commands

Run these from a regular terminal (not inside Claude Code):

### 1. Plan
cd <WORK_DIR> && odin plan <spec_path> --auto

### 2. Review
cd <WORK_DIR> && odin specs
cd <WORK_DIR> && odin status

### 3. Execute (run for each task)
cd <WORK_DIR> && odin exec <task_id> [--mock]

### 4. Post-run diagnostic
cd <REPO_ROOT>/taskit/taskit-backend && python testing_tools/spec_trace.py <spec_id> --brief
```

If `--exec-only` was passed, skip the plan/review sections and only show the exec + diagnostic commands.

### Step 5: Post-run diagnostic hint

Always remind the user to run the diagnostic after execution:

```
After execution completes, check results with:
  /dk-local-inspect spec <spec_id> --brief
```

This connects the two skills into a natural workflow.
