---
name: ast-grep
description: 'Use when asked to run AST-based structural search, lint, or rewrite of code when regex is too fragile. Pattern is validated, blast radius reviewed, and rewrite landed at the correct scope. Don''t use for remote, credential, publish, deploy, or irreversible changes.'
---

# ast-grep

## Contract

| Field | Bound contract |
|---|---|
| Trigger | AST-based modification, structural search, lint, or replacement too fragile for regex. |
| Authority | Reversible local writes to VCS-tracked source files only. Search is read-only; rewrites apply only through the helper after dry-run review. Roll back via version control. |
| Side effect | Local file writes through the helper two-pass validate/dry-run/apply flow; no remote, credential, or published mutation. |
| Done | Pattern validated, blast radius reviewed, and rewrite landed at the correct scope. |

## Inputs

- An ast-grep pattern, single-quoted in the shell so `$VAR` reaches ast-grep unexpanded.
- A language (`--lang`) or a single target path whose extension auto-detects it; required for stdin patterns.
- For rewrites: a rewrite template and one or more target paths (defaults to the current directory).
- Optional: include/exclude globs (repeatable, prefix `!` to exclude), context lines, JSON output mode.

## Procedure

1. Confirm the task is structural (call, function, class, or import shaped like a pattern), not text/regex/filename matching (use grep) or semantic type/reference lookup (use LSP or the compiler). ast-grep matches syntax, not bytes. Done when: the task is confirmed structural.
2. Validate the pattern before searching: `python3 scripts/ast_grep_helper.py validate '<pattern>' --lang <L>`. Exit 0 means ast-grep parses it cleanly; exit 2 means malformed (the helper prints the parsed pattern tree showing the ERROR node). Fix and re-validate. Done when: validate exits 0.
3. For a rewrite, run the dry-run: `python3 scripts/ast_grep_helper.py replace '<pattern>' '<rewrite>' --lang <L> <paths>`. Read the diff and the `N matches across M files` count. If the blast radius is wrong, stop and refine the pattern (tighten meta-variables, add `--lang`, add context); re-run the dry-run. Done when: the dry-run diff and match count are correct.
4. Apply only after the dry-run diff is correct: `python3 scripts/ast_grep_helper.py replace '<pattern>' '<rewrite>' --lang <L> <paths> --apply`. The helper writes via a separate `--update-all` pass. Done when: files are updated via `--update-all`.
5. Invoke `ast-grep`, never `sg`: `sg` collides with the `setgroups` binary on many systems. Done when: `ast-grep` is invoked, not `sg`.

Pattern syntax: `$VAR` matches any single node; `$$$ARGS` matches zero or more nodes; `$_` matches any node (non-capturing).

Invariants: validate before searching; dry-run before applying; single-quote patterns; `--lang` is required for stdin; a pattern is code, not regex; switch to grep the moment `|`, `.*`, `\w`, or `[...]` would be needed. The helper keeps `--json` and `--update-all` as separate passes because combining them makes `--json` silently win and the write is dropped with no error.

For complex tasks, ast-grep supports YAML rule files (`sgconfig.yml`, `ast-grep new project`) with `rule`, `fix`, `inside`, `any`, and `matches` fields; invoke `ast-grep scan`/`run`/`test` directly for these.

## Failure and recovery
- Malformed pattern: `validate` exits 2 and prints the pattern debug tree with the ERROR node. No files touched. Fix the pattern and re-validate.
- Wrong blast radius: the dry-run diff or match count is not as expected. Do not `--apply`. Refine the pattern and re-run the dry-run. No files touched.
- Zero matches unexpectedly: run the 0-matches ladder in order: (1) validate the pattern; (2) check `--lang` (`tsx` is not `ts`; the wrong dialect silently matches nothing); (3) `ast-grep run -p '<pattern>' -l <L> --debug-query=pattern` and look for `ERROR`; (4) inspect the target's actual tree with `--debug-query=ast` on a known-matching snippet; (5) reproduce in the online playground. No files touched until a correct match is confirmed.
- ast-grep binary absent: `validate` skips the parse check (regex-smell only) and warns; `replace` exits 2 without running. Install ast-grep before proceeding.
- Apply pass failure: the helper reports the ast-grep error and returns non-zero. Revert the partially-written VCS-tracked targets via version control and re-run the full dry-run/apply sequence.
- Partial-result rule: a failed apply pass leaves whatever ast-grep wrote; never report done. Recover via version control and re-run from the dry-run.

## Output
- `validate`: exit 0 (valid) or 2 (malformed, with the pattern debug tree); advisory regex-smell hints on stderr.
- `replace` dry-run: a compact unified diff and an `N matches across M files` summary; no files modified.
- `replace --apply`: VCS-tracked files updated via `--update-all` plus a confirmation line.
- Direct `ast-grep` search: matched code locations.
