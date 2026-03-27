---
name: phx:investigate
description: Investigate a bug or error in Elixir/Phoenix code. Use whenever the user reports a bug, error, crash, exception, or unexpected behavior. Also use when seeing stack traces, compile errors, or test failures that need root-cause analysis. Uses Ralph Wiggum approach — checks obvious things first, reads errors literally. Add --parallel for 4-track deep investigation.
effort: high
argument-hint: <bug description> [--parallel]
disable-model-invocation: true
---

# Investigate Bug

Investigate bugs using the Ralph Wiggum approach: check the
obvious, read errors literally.

## Usage

```
/phx:investigate Users can't log in after password reset
/phx:investigate FunctionClauseError in UserController.show
/phx:investigate Complex auth bug --parallel
```

## Arguments

`$ARGUMENTS` = Bug description or error message. Add `--parallel`
for deep 4-track investigation.

## Mode Selection

Use **parallel mode** (spawn `deep-bug-investigator`) when:
bug mentions 3+ modules, spans multiple contexts, is intermittent
or involves concurrency, or user says `--parallel`/`deep`.

**Otherwise**: Run the sequential workflow below.

**Avoid confirmatory subagents**: Do NOT spawn parallel subagents
to "verify" findings you already identified in the main context.
If Step 3-4 already identified the root cause with high confidence,
present it directly — don't spend ~80K tokens on 4 subagents to
confirm what's already obvious (confirmed waste: session c135330a).

## Iron Laws

1. **Read the error message literally first** — Most bugs tell you exactly what's wrong; resist the urge to theorize before reading what the system is saying
2. **Check the obvious before going deep** — Compile errors, missing migrations, atom/string mismatches explain 80% of bugs; exhausting the Ralph Wiggum checklist saves hours
3. **Check changeset errors before UI debugging** — Silent form saves are almost always `{:error, changeset}` with validation failures, not viewport or JS issues
4. **Consult compound docs before investigating fresh** — A previously solved problem saves the entire investigation cycle; always search `.claude/solutions/` first

## Investigation Workflow

### Step 0: Consult Compound Docs

```bash
grep -rl "KEYWORD" .claude/solutions/ 2>/dev/null
```

If matching solution exists, present it and ask: "Apply this
fix, or investigate fresh?"

### Step 0a: Runtime Auto-Capture (Tidewave -- PRIMARY when available)

If Tidewave MCP is detected, **start here instead of asking
the user to paste errors**. Auto-capture runtime context:

1. `mcp__tidewave__get_logs level: :error` -- capture recent errors
2. Parse stacktraces, correlate with source via
   `mcp__tidewave__get_source_location`
3. For data bugs: `mcp__tidewave__execute_sql_query` to inspect state
4. For logic bugs: `mcp__tidewave__project_eval` to test hypotheses
5. For UI bugs: `mcp__tidewave__get_source_location` with component name

Present pre-populated context to the user:

> **Auto-captured from runtime:**
>
> - Error: {parsed error from logs}
> - Location: {file:line from get_source_location}
>
> Investigating this. Correct if wrong.

This eliminates copy-pasting errors between app and agent.
**If Tidewave NOT available**: Fall through to Step 1.

### Step 1: Sanity Checks

```bash
mix compile --warnings-as-errors 2>&1 | head -50
mix ecto.migrate
```

### Step 2: Reproduce

```bash
mix test test/path_test.exs --trace
tail -200 log/dev.log | grep -A 5 -i "error\|exception"
```

### Step 3: Read Error LITERALLY

Parse the error message — check `${CLAUDE_SKILL_DIR}/references/error-patterns.md`.

### Step 4: Check the Obvious (Ralph Wiggum Checklist)

File saved? Atom vs string? Data preloaded? Pattern match
correct? Nil? Return value? Server restarted?

**LiveView form saves silently failing?** Check changeset errors
FIRST — not viewport, click mechanics, or JS. A missing
`hidden_input` for a required embedded field causes `{:error,
changeset}` with no visible UI feedback.

### Step 5: IO.inspect / Tidewave project_eval

### Step 6: Identify Root Cause

What's actually happening vs what should happen.

## Autonomous Iteration

For autonomous debugging, use `/ralph-loop:ralph-loop` with
clear completion criteria and `--max-iterations`.

## References

- `${CLAUDE_SKILL_DIR}/references/error-patterns.md` — Common errors and checklist
- `${CLAUDE_SKILL_DIR}/references/investigation-template.md` — Output format
- `${CLAUDE_SKILL_DIR}/references/debug-commands.md` — Debug commands and common fixes
