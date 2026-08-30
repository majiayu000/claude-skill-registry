---
name: phx-investigate
description: Investigate Elixir/Phoenix bugs root-cause first. Reproduce failures,
  cite evidence, and use optional native DeepSeek Harness subagents only when useful.
---
# Investigate Bug

Investigate Elixir/Phoenix bugs root-cause first. Reproduce or establish the
failing behavior before recommending a fix, and cite concrete paths and lines.

## Usage

```text
/phx-investigate Users can't log in after password reset
/phx-investigate FunctionClauseError in UserController.show
/phx-investigate Complex auth bug --parallel
```

Treat the text after the skill name as the bug description. `--parallel` asks
for independent investigation tracks when native DeepSeek Harness subagent tooling is
available; it is an optimization, never a requirement.

## Iron Laws

1. **Read the error literally first** — extract the exception, message, failing
   assertion, and first relevant application frame before theorizing.
2. **Check the obvious before going deep** — compile errors, missing migrations,
   atom/string mismatches, nil values, stale servers, and changeset errors explain
   many failures.
3. **Reproduce before proposing a fix** — run the smallest relevant test or
   controlled command and record its output. If reproduction is impossible,
   state exactly what evidence establishes the failure instead.
4. **Confirm the root cause with evidence** — distinguish the observed failure,
   the causal code path, and the proposed correction.
5. **Do not edit while investigating unless the user asks for a fix** — the
   investigation result is evidence and a recommendation, not an implicit patch.

## Workflow

### 1. Consult Existing Evidence

Search `.claude/solutions/`, recent diffs, tests, logs, and the literal error.
Do not block if `.claude/solutions/` does not exist.

### 2. Capture Runtime Context When Available

Tidewave is optional. If its tools are configured, use them for logs, source
locations, safe queries, or hypothesis checks. Otherwise use repository files,
`mix` commands, and local logs. Never fail or ask the user to install Tidewave
merely to continue an investigation.

### 3. Run Sanity Checks

Choose focused checks that fit the report, such as:

```bash
mix compile --warnings-as-errors
mix test test/path_test.exs --trace
```

Do not run migrations or other state-changing commands unless they are necessary,
safe for the fixture, and authorized by the user.

### 4. Reproduce Before Fixing

Capture the exact command, failure, and relevant output. Read
`references/error-patterns.md`, then inspect only the code needed to trace the
failure from entry point to cause.

### 5. Check the Obvious

Check saved files, atom/string keys, preload state, pattern matches, nil values,
return values, server restarts, and changeset errors. For silent LiveView form
failures, inspect `{:error, changeset}` and rendered validation errors before JS.

### 6. Trace and Test the Hypothesis

Use targeted searches, source reads, tests, or non-mutating diagnostics. Only add
temporary source diagnostics if the user explicitly authorizes edits, and remove
them before reporting. Cite `path:line` evidence for both the failing behavior
and the causal code.

If native DeepSeek Harness subagents are available and the bug genuinely spans independent
areas, delegate read-only tracks by concern. Otherwise perform the same tracks
sequentially in this session. Do not require named custom agents.

### 7. Report

Use `references/investigation-template.md`. Include:

- reproduction or evidence establishing the failure;
- root cause, not merely the symptom;
- relevant paths and lines;
- confidence and any unverified assumptions;
- the smallest safe fix or next diagnostic step.

Route follow-up work with `/phx-quick`, `/phx-plan`, or `/phx-compound` when
appropriate. Do not invoke another skill unless the user asks you to continue.

## References

- `references/error-patterns.md` — common errors and checklist
- `references/investigation-template.md` — output format
- `references/debug-commands.md` — debug commands and common fixes
