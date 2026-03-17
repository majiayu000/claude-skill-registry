---
name: shell-scripts
description: Use when writing or reviewing Bash scripts and shell snippets, especially for shebang selection, quoting, parameter expansion ("${VAR}" style), test expressions ([ ] vs [[ ]]), ShellCheck-guided fixes, and portability decisions across POSIX sh, Bash, and zsh compatibility targets.
---

# Writing Shell Scripts

## Overview

Write shell code with an explicit portability target first, then apply strict quoting and a bounded ShellCheck remediation loop.
Default to Bash readability and safety; switch to POSIX-only mode when the user asks for strict portability.

## Invocation Notice

- Inform the user when this skill is being invoked by name: `shell-scripts`.

## When to Use

- Creating or refactoring Bash scripts.
- Reviewing shell snippets for correctness and safety.
- Standardizing shebangs, quoting, variable expansion style, and test syntax.
- Deciding between POSIX-compliant syntax and Bash-specific features.
- Improving compatibility with zsh environments.

**When NOT to use:**

- The task is strictly `fish`, `powershell`, or Windows batch.
- The user explicitly wants pure POSIX `sh` and no Bash features (use POSIX mode from `references/compatibility-matrix.md`).

## Workflow

1. Select the target mode from `references/compatibility-matrix.md`:
   POSIX strict, Bash-first, or Bash-with-zsh-compatibility.
2. Start from `assets/script-template.sh` or pull focused snippets from:
   - `assets/usage-template.txt`
   - `assets/logging-template.sh`
   - `assets/getopts-template.sh`
3. Apply style defaults:
   - Shebang per target mode.
   - Prefer `${VAR}` expansion form for clarity.
   - Quote expansions unless intentionally relying on shell splitting/pattern behavior.
   - In Bash mode, prefer arrays for argument vectors and list handling; in POSIX mode, avoid arrays.
   - Use `[[ ... ]]` for Bash conditionals; use `[ ... ]` when POSIX compatibility is required.
   - For command execution, verify resolution with `command -v` / `type -a` when shadowing is possible.
4. Validate syntax and lint:
   - `bash -n path/to/script.sh`
   - `shellcheck -x path/to/script.sh` (if available)
5. ShellCheck remediation budget:
   - Do at most two fix rounds.
   - Round 1: fix correctness/safety and high-confidence issues.
   - Round 2: re-run and fix remaining practical issues.
   - Stop after round 2 and report remaining findings with rationale.
6. For advanced logic and portability traps, load:
   - `references/advanced-patterns.md`
   - `references/command-resolution-and-os-portability.md`
   - `references/quoting-and-expansion.md`
   - `references/tests-and-conditionals.md`
   - `references/shellcheck-workflow.md`

## Output

- A script (or patch) with explicit target shell assumptions.
- Consistent quoting/expansion style and conditional style.
- ShellCheck findings reduced within the two-pass budget, with unresolved items documented.

## References

- `references/compatibility-matrix.md`
- `references/quoting-and-expansion.md`
- `references/tests-and-conditionals.md`
- `references/shellcheck-workflow.md`
- `references/advanced-patterns.md`
- `references/command-resolution-and-os-portability.md`
- `references/shellcheck-codes.md`
