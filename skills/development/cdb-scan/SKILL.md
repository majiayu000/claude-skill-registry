---
name: cdb-scan
description: Survey this codebase once and store a profile of it in project memory — stack, layout, conventions, workflows. Re-run any time to refresh it in place. Use when memory is newly installed on an existing project, or when the project has changed enough that the stored profile is stale.
---

# Survey this project into memory

Everything else in claude-db's memory is testimony: it records what happened,
turn by turn, as it happened. A fresh install knows none of that, and stays
useless for weeks while it fills up.

This fills the gap from the one source available on day one — the code itself.
What you write here is **your reading of the codebase, not a record of events**,
so it is tagged `inferred` and must never be phrased as history.

## How to run it

Work through the sections below in order. For each one, look at the actual
files, then call the `remember` MCP tool once with the given `key`.

`key` is what makes this re-runnable: writing the same key again replaces that
note rather than adding a second copy. Use these exact keys, and always pass
`tags: ["inferred"]` and `kind: "context"`.

Before you start, call `search` for `profile` in this project. If notes already
exist, read them first and update what changed rather than restating it — a
second run should be an edit, not a rewrite.

### 1. `profile:stack`

Languages, runtime and version floors, frameworks, package manager, database,
test runner, build tool. Read the manifest (`package.json`, `pyproject.toml`,
`go.mod`, `Cargo.toml`) and the lockfile rather than guessing. Name versions
where a version constrains what can be written.

### 2. `profile:layout`

The directory map, one line each, and what lives where. Include the entry
points: the binary, the server, the main export. Skip anything generated.

### 3. `profile:conventions`

How this codebase is written, taken from the code and not from a style guide:
module system, import style, error handling, naming, comment density, how
tests are structured. Note where the project deviates from the language default,
since that is what someone would otherwise get wrong.

### 4. `profile:workflows`

The commands that matter — install, build, test, lint, run, release — and
anything non-obvious about running them: a required service, an environment
variable, a step that must come first. Take them from the manifest scripts and
CI config, not from the README's aspirations.

### 5. `profile:architecture`

Only the parts a newcomer could not infer from the layout: the main
abstractions and how a request or a command actually flows through them. Two
paragraphs at most. If the codebase is small enough that the layout says it
all, skip this section rather than padding it.

## Rules

- **One `remember` call per section.** Five notes, five stable keys.
- **Write claims, not headings.** "Storage is one `MemoryStore` interface with
  three adapters, selected by URI scheme" — not "Storage architecture".
- **Say what you verified.** If something was not read, leave it out. An
  inferred profile that is confidently wrong is worse than a short one.
- **Never restate `CLAUDE.md`.** That file is already in the system prompt on
  every turn. Memory is for what is not.
- **Do not record secrets, credentials or personal data**, even if the code
  contains them.
