---
name: phx:mix-compression
description: Reduce mix output noise (5-15% token savings) by installing rtk filters that compress mix test/credo/dialyzer/compile output before it reaches Claude. Use when long mix output floods context.
effort: low
---

# Mix Output Compression

Mix commands (`mix test`, `mix credo`, `mix dialyzer`, `mix compile`) emit
verbose, repetitive output that consumes context fast. This skill installs
[rtk](https://github.com/rtk-ai/rtk) — a CLI proxy that filters tool output
**before it lands in the transcript**.

The filters short-circuit happy paths to a single line (`mix test: all pass`)
while preserving full failure blocks, compile errors, and stack traces. Net win:
5-15% per-session token reduction on mix-heavy workflows.

## When to use

- **Long sessions** — `/phx:work` or `/phx:full` hitting context limits from mix output
- **Debugging loops** — `/phx:investigate` retrying `mix compile`/`mix test` repeatedly
- **Dialyzer-heavy projects** — `mix dialyzer` output dominates the transcript

## Iron Laws

1. **NEVER strip critical signals** — compile errors (`** (CompileError)`,
   `== Compilation error in`), test failures (`FAILURES`, `0 failures` — preserved
   even on short-circuit), dialyzer warnings, and stack traces with `file:line` MUST
   pass through unchanged
2. **Verify after install** — run `rtk test mix-test` (or any filter name) to
   confirm the bundled test fixtures pass before declaring success
3. **Never overwrite existing `.rtk/filters.toml`** — diff and merge instead

## Workflow

### Step 1: Detect rtk

```bash
which rtk && rtk --version
```

Read `${CLAUDE_SKILL_DIR}/references/install.md` if rtk is missing — covers
homebrew install + shell hook setup.

### Step 2: Seed `.rtk/filters.toml`

Reference filters live at `${CLAUDE_SKILL_DIR}/references/rtk-filters.toml`. Six
production-tested filters covering:

- **`mix-test`** — short-circuits all-pass, preserves failure blocks + compile errors
- **`mix-credo`** — collapses clean runs, preserves violation blocks
- **`mix-dialyzer`** — drops PLT progress, keeps warnings + summary
- **`mix-deps-get`** — collapses unchanged package lists
- **`mix-ecto-migrate`** — strips compile prefix, short-circuits "already up"
- **`mix-compile`** — handles parallel worker prefixes (`N>`) and MIX_ENV

Run this if the project has no `.rtk/filters.toml` yet:

```bash
mkdir -p .rtk
cp "${CLAUDE_SKILL_DIR}/references/rtk-filters.toml" .rtk/filters.toml
```

Read both files if one already exists. Present a diff to the user. Merge only
the filters they don't already have.

### Step 3: Verify filters work

```bash
rtk test mix-test    # runs embedded [[tests.mix-test]] fixtures
rtk test mix-credo
rtk test mix-dialyzer
```

Check that all report "passed". Flag and stop if any fail — usually means the
user has a custom rtk version with regex differences.

### Step 4: Confirm shell hook

Run `rtk init zsh` (or `rtk init bash`) to install the transparent rewrite hook
that turns `mix X` into `rtk mix X`. Re-running is safe (idempotent). Skip this
step and `mix` calls run unfiltered.

## Customization

Add custom regex patterns to `strip_lines_matching` for project-specific noise
sources (e.g., third-party hex deps spamming stack traces). See the inline
example in `references/rtk-filters.toml` lines 57-59.

## What this is NOT

- **Not a hook** — Claude Code's `PostToolUse` hooks fire after the tool result
  is in the transcript and cannot shrink it. rtk works at the subprocess layer
  (the only layer where transcript-shortening is possible).
- **Not project-analysis** — the bundled filter set is universal across Phoenix
  projects. No `mix.exs` inspection needed.
- **Not telemetry** — rtk has telemetry off by default (`enabled = false` in
  `config.toml`). Filters run locally, no data leaves the machine.

## References

- `${CLAUDE_SKILL_DIR}/references/rtk-filters.toml` — bundled filter set
- `${CLAUDE_SKILL_DIR}/references/install.md` — rtk install + shell hook setup
- [rtk on GitHub](https://github.com/rtk-ai/rtk)
