---
name: tzst
description: Use when the user needs to create, extract, flatten, list, test, install, script, or troubleshoot `tzst` CLI workflows for `.tzst` or `.tar.zst` archives, including compression levels, streaming mode, extraction filters, conflict resolution, JSON output, or standalone binary setup, even if they describe the archive task without naming `tzst`.
---

# tzst

Use this skill for the `tzst` command-line interface. Default to execution when the user clearly wants a real archive action and the required paths or archive names are already known.

This skill is CLI-only. If the user is asking about Python code such as `from tzst import ...`, treat that as a general Python library or API documentation task instead of using this skill as the main guide.

## When to Use

Use this skill when the user:

- mentions `.tzst` or `.tar.zst` archives
- wants to create, extract, flatten, list, or test a `tzst` archive
- needs help installing `tzst` or choosing CLI flags
- wants machine-readable `tzst` output for scripting or automation
- needs safe conflict handling or extraction filter guidance

Do not use this skill for generic `tar`, `zip`, or Python API questions unless `tzst` is actually part of the request.

## Preflight

1. Check whether `tzst` is available with `tzst --version` or `tzst --help`.
2. If it is missing, prefer one of these installation paths:
   - `uv tool install tzst`
   - `pip install tzst`
   - a standalone release binary from <https://github.com/xixu-me/tzst/releases/latest> when the user does not want a Python installation
3. Re-run `tzst --version` or `tzst --help` before doing real work.

## Workflow

1. Decide whether the request is execution or guidance.
   Requests like "archive these files", "extract this backup", "list what is inside", "test this archive", or "install tzst" are execution intent.
2. Choose the command that matches the request:
   - `a`, `add`, `create` for archive creation
   - `x`, `extract` for normal extraction with directory structure preserved
   - `e`, `extract-flat` only when the user explicitly wants flattened output
   - `l`, `list` for archive inspection
   - `t`, `test` for integrity checks
3. If the user wants to extract only a few members and the member names are uncertain, list first.
4. Load [`references/cli-reference.md`](./references/cli-reference.md) when you need the command matrix, exact flag names, or copy-paste examples.

## Safe Defaults

- Prefer `x` over `e` unless flattening is explicitly requested.
- Keep `--filter data` as the default extraction mode.
- Use `--filter tar` only when the user needs standard tar-style compatibility.
- Use `--filter fully_trusted` only when the user explicitly says the archive source is completely trusted.
- Keep atomic archive creation enabled. Only reach for `--no-atomic` when the user explicitly wants it.
- Prefer `--streaming` for large archives or memory-constrained environments.
- For automation or pipelines, prefer `tzst --json --no-banner ...`.
- For automated extraction, require an explicit non-interactive `--conflict-resolution` choice such as `replace_all`, `skip_all`, or `auto_rename_all`.
- Do not combine `--json` with interactive conflict prompting.

## Scripting Notes

- Put global flags before the subcommand in examples, such as `tzst --json --no-banner l archive.tzst`.
- Use exit codes in scripts: `0` for success, `1` for operation errors, `2` for argument parsing errors, and `130` for interruption.
- When archive naming matters, tell the user that `tzst` may normalize a creation target to `.tzst` or `.tar.zst`.

## Common Mistakes

- Using `e` when the user expected the original directory structure to be preserved
- Recommending `fully_trusted` for archives from an unknown or untrusted source
- Forgetting an explicit conflict strategy for non-interactive extraction
- Treating a Python API question as a CLI question
- Guessing flags from `tar` habits instead of checking the bundled reference or the installed CLI help
