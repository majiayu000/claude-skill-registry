---
name: ralph-calibrate
description: Run Ralph calibration checks to analyze intention drift, technical quality, and self-improvement opportunities. Use when user asks to "ralph calibrate", "check drift", "analyze sessions", or needs to verify work alignment.
---

# Ralph Calibrate

Run calibration checks to ensure code and agent behavior align with planning intentions.

## Execution Instructions

When this skill is invoked, check the ARGUMENTS provided:

### If argument is `intention`:

Run intention drift analysis to verify completed subtasks align with planning chain (Vision → Story → Task → Subtask).

**Prerequisites check first:**
1. Look for `subtasks.json` in the project root
2. If not found, output a helpful message and exit gracefully:
   > "No subtasks.json found. Nothing to analyze for intention drift.
   >
   > To run intention drift analysis, create a subtasks.json file with completed subtasks that have commitHash values."
3. If found but no completed subtasks have `commitHash`, output:
   > "No completed subtasks with commitHash found. Nothing to analyze."

If prerequisites are met, follow: @context/workflows/ralph/calibration/intention-drift.md

### If argument is `technical`:

Run technical quality analysis to check code quality patterns.

**Prerequisites check first:**
1. Look for `subtasks.json` in the project root
2. If not found, output a helpful message and exit gracefully:
   > "No subtasks.json found. Nothing to analyze for technical drift.
   >
   > To run technical drift analysis, create a subtasks.json file with completed subtasks that have commitHash values."
3. If found but no completed subtasks have `commitHash`, output:
   > "No completed subtasks with commitHash found. Nothing to analyze."

If prerequisites are met, follow: @context/workflows/ralph/calibration/technical-drift.md

### If argument is `improve`:

Run self-improvement analysis to identify agent inefficiencies from session logs.

**Prerequisites check first:**
1. Look for `subtasks.json` in the project root
2. If not found, output a helpful message and exit gracefully:
   > "No subtasks.json found. Nothing to analyze for self-improvement.
   >
   > To run self-improvement analysis, create a subtasks.json file with completed subtasks that have sessionId values."
3. If found but no completed subtasks have `sessionId`, output:
   > "No completed subtasks with sessionId found. Nothing to analyze."

**Check configuration:**
Read `ralph.config.json` for the `selfImprovement` setting which controls behavior:
- **`"always"`** (default): Propose-only mode. Creates task files in `docs/planning/tasks/` for proposed improvements. Does NOT apply changes directly.
- **`"auto"`**: Auto-apply mode. Applies changes directly to target files (CLAUDE.md, prompts, skills) without creating task files. Use with caution.
- **`"never"`**: Skip analysis entirely and exit with a message explaining that self-improvement is disabled.

If prerequisites are met, follow: @context/workflows/ralph/calibration/self-improvement.md

### If argument is `all`:

Run all calibration checks in sequence. Execute each check one after another, following the prerequisite checks and prompts for each:

**Step 1: Intention Drift Analysis**
- Check prerequisites: `subtasks.json` exists with completed subtasks having `commitHash`
- If met, follow: @context/workflows/ralph/calibration/intention-drift.md
- Output intention drift summary

**Step 2: Technical Drift Analysis**
- Check prerequisites: `subtasks.json` exists with completed subtasks having `commitHash`
- If met, follow: @context/workflows/ralph/calibration/technical-drift.md
- Output technical drift summary

**Step 3: Self-Improvement Analysis**
- Check prerequisites: `subtasks.json` exists with completed subtasks having `sessionId`
- If met, follow: @context/workflows/ralph/calibration/self-improvement.md
- Output self-improvement summary

**Final Output:**
Combine all results into a unified summary showing:
- Overall status (all checks passed, issues found, skipped checks)
- Summary of each check that ran
- List of task files created (if any)

If `subtasks.json` is missing entirely, output:
> "No subtasks.json found. Cannot run calibration checks.
>
> To run calibration, create a subtasks.json file with completed subtasks."

### If no argument or unknown argument:

Show the usage documentation below.

---

## Usage

```
/ralph-calibrate <subcommand> [options]
```

### Examples

```bash
# Check for intention drift on completed subtasks
/ralph-calibrate intention

# Analyze technical quality patterns
/ralph-calibrate technical

# Analyze session logs for agent inefficiencies
/ralph-calibrate improve

# Run all calibration checks in sequence
/ralph-calibrate all

# Skip approval prompts and create task files automatically
/ralph-calibrate intention --force

# Require approval before creating any task files
/ralph-calibrate all --review
```

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `intention` | Analyze intention drift between planning and implementation |
| `technical` | Analyze technical quality patterns (tests, types, error handling) |
| `improve` | Analyze session logs for agent inefficiencies |
| `all` | Run all calibration checks sequentially |

## Options

| Option | Description |
|--------|-------------|
| `--force` | Skip approval prompts, create task files automatically |
| `--review` | Require approval before creating task files |

## Intention Drift Analysis

Analyzes completed subtasks to detect when code changes have diverged from the intended behavior defined in the planning chain.

### What It Checks

- **Scope Creep** - Code implements more than specified
- **Scope Shortfall** - Code implements less than acceptance criteria require
- **Direction Change** - Code solves a different problem than intended
- **Missing Link** - Code doesn't connect to intended outcome

### Output

- Summary to stdout showing drift analysis results
- Task files created in `docs/planning/tasks/` for any detected drift

## Technical Drift Analysis

Analyzes completed subtasks to detect when code changes have drifted from technical quality standards.

### What It Checks

- **Missing Tests** - Code changes without corresponding test coverage
- **Inconsistent Patterns** - Code that doesn't follow established codebase patterns
- **Missing Error Handling** - Critical paths without proper error handling
- **Documentation Gaps** - Public APIs or complex logic without documentation
- **Type Safety Issues** - Use of `any`, type assertions, or missing types
- **Security Concerns** - Potential security vulnerabilities

### Output

- Summary to stdout showing technical quality analysis results
- Task files created in `docs/planning/tasks/` for detected technical drift

## Self-Improvement Analysis

Analyzes Ralph agent session logs for inefficiencies to propose improvements to prompts, skills, and documentation.

### What It Checks

- **Tool Misuse** - Using Bash for file operations instead of Read/Write/Edit
- **Wasted Reads** - Files read but never used
- **Backtracking** - Edits that cancel each other out
- **Excessive Iterations** - Repeated attempts without changing approach

### Configuration

The `selfImprovement` setting in `ralph.config.json` controls behavior:

| Setting | Mode | Behavior |
|---------|------|----------|
| `"always"` | Propose-only | Creates task files for review, does NOT apply changes |
| `"auto"` | Auto-apply | Applies changes directly to target files |
| `"never"` | Disabled | Skips analysis entirely |

### Output

- Summary to stdout showing inefficiency findings
- **In propose-only mode (`"always"`):** Task files created in `docs/planning/tasks/` for proposed improvements
- **In auto-apply mode (`"auto"`):** Changes applied directly to target files (CLAUDE.md, prompts, skills)

## CLI Equivalent

This skill provides the same functionality as:

```bash
aaa ralph calibrate <subcommand> [options]
```

## References

- **Intention drift prompt:** @context/workflows/ralph/calibration/intention-drift.md
- **Technical drift prompt:** @context/workflows/ralph/calibration/technical-drift.md
- **Self-improvement prompt:** @context/workflows/ralph/calibration/self-improvement.md
