---
name: buff-code
description: This skill should be used when the user asks to "write code", "implement this", "build a feature", "help me code", "run /buff:code", "audit the code", "explain the code", "add a function", "refactor", or any general coding or implementation request across any language or framework. Project-aware with cross-file context, architecture enforcement, and duplication detection. Auto-activates silently during development to raise code quality; produces visible output only on explicit invocation.
version: 0.2.0
argument-hint: "[explain|audit|<feature description>]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# buff-code v2

Project-aware coding with cross-file context, duplication detection, and architecture enforcement. Loads dependency graph, architectural decisions, and past corrections before writing any code — ensuring every change fits the existing codebase structure. Silent by default; explicit subcommands (`/buff:code explain`, `/buff:code audit`) produce visible output.

## Activation modes

| Invocation | Behavior |
|---|---|
| Auto-activated by Claude | Silent — raises code quality, applies stack conventions |
| `/buff:code <feature>` | Implement the described feature using buff standards |
| `/buff:code explain` | Explain the current file or selection in plain terms |
| `/buff:code audit` | Run a visible quality audit on the current file |

## Counterfeit context loading

Before writing or editing any code, load targeted context from counterfeit memory stores. Read only what is relevant — never bulk-load.

**Project-level** (`.buff/memory/`):
- `graph.json` entry for the target file — exports, imports_from, imported_by, lines, last_modified, test_file, coverage
- `decisions.json` entries tagged with the relevant directory or module
- `learnings.json` entries related to the target file or module

**Global** (`~/.buff/memory/`):
- `corrections.json` entries for similar file types (e.g., all `.ts` corrections when editing a `.ts` file)
- `patterns.json` coding patterns the user prefers

Targeted loading tree (aim for ~200-400 tokens of context):

```
Target file: src/services/user.ts
Load context:
  ├── graph.json entry for user.ts
  ├── Import lines from files that import user.ts (Grep, not full read)
  ├── Export signatures from files user.ts imports (Grep, not full read)
  ├── decisions.json entries tagged with "services" or "user"
  └── corrections.json entries for similar file types
```

Only read full file contents when you need to understand implementation details — for dependency awareness, grep for export/import lines only.

## Stack detection

First check `.buff/memory/context.json` — if `project.stack` is already populated, use it and skip detection. Otherwise detect from project files in order:

1. `bun.lockb` → Bun runtime
2. `package.json` scripts and dependencies → framework (Next.js, Elysia, Express, etc.)
3. `tsconfig.json` → TypeScript config and strictness level
4. `pyproject.toml` / `requirements.txt` → Python stack
5. `Cargo.toml` → Rust
6. `go.mod` → Go
7. `~/.buff/memory/preferences.json` → user's global stack preference (fallback)

Store detected stack in `.buff/memory/context.json` after first detection — never re-detect the same project twice.

## Coding standards (silent enrichment)

Apply these standards on every code write or edit without announcing them:

### Universal
- Prefer explicit over implicit — clear names over terse ones
- Functions do one thing — extract when a function does two
- Error paths are first-class — handle them before the happy path
- No magic numbers or strings — name constants
- Zero dead code — remove commented-out blocks, unused imports, unreachable branches

### TypeScript / JavaScript
- Strict mode always (`"strict": true`)
- Prefer `const` and `readonly` — `let` only when mutation is necessary
- Avoid `any` — use `unknown` and narrow, or define the type
- Async/await over raw Promises — never `.then().catch()` chains in new code
- Use Zod or equivalent for runtime validation at boundaries (HTTP input, env vars, file parsing)
- Named exports over default exports (easier to grep, easier to refactor)

### Python
- Type annotations on all function signatures
- Prefer dataclasses or Pydantic models over raw dicts
- Context managers (`with`) for file and resource handling
- f-strings for formatting — never `%` or `.format()`

### Rust
- Explicit error types — `anyhow` for applications, custom errors for libraries
- Avoid `.unwrap()` in non-test code — use `?` or explicit handling
- Prefer iterator chains over imperative loops where readable

### Go
- Errors are values — check every error, never `_` an error
- Short variable names at small scope, descriptive at package scope
- Standard library first — add dependencies only when necessary

## Duplication detection

Before creating new functions, classes, or utilities, check for existing implementations:

1. **Grep for similar function names** — search for semantically similar names (e.g., `validate.*email`, `email.*valid`, `check.*email`)
2. **Check `graph.json` exports** — scan exports across all file entries for matching utility functions
3. **If match found** — import and reuse the existing function instead of duplicating

```
Existing: src/utils/validation.ts exports validateEmail()
Action: importing existing function instead of creating duplicate
```

4. **If existing doesn't quite fit** — extend the existing function to cover the new case. First check callers via `graph.json` `imported_by` to ensure the extension won't break them.
5. **If extension would break callers** — create the new function but flag it for future consolidation:

```
New: src/utils/string-helpers.ts exports normalizeEmail()
Note: similar to validateEmail() in validation.ts — consolidate in future simplify pass
```

## Architecture enforcement

Before implementation, read `.buff/plan.md` and `.buff/memory/decisions.json`. Validate that the change conforms:

- **File placement** — the file matches a planned component or follows the established directory structure
- **Import direction** — imports follow architectural layers (e.g., routes → services → repositories → db, never reversed)
- **Export patterns** — new exports follow the conventions established by existing files in the same directory
- **Error handling** — follows the decided error handling pattern (Result type, exceptions, error codes, etc.)

On architecture drift, show a warning and fix silently:

```
⚠ Architecture drift: src/routes/users.ts imports directly from src/db/queries.ts
  Plan says: routes → services → repositories → db
  Fix: route through UserService instead of direct DB access
  Proceeding with fix applied.
```

Log all drift events to `.buff/memory/learnings.json` so the pattern is not repeated.

## Feature implementation workflow

When implementing a feature (`/buff:code <feature>`):

1. **Counterfeit context load** — read graph.json, decisions.json, corrections.json, and patterns.json for relevant entries
2. **Read `.buff/plan.md`** if it exists — implement within the planned architecture
3. **Read relevant existing files** — understand patterns already in use (grep for signatures, not full reads where possible)
4. **Duplication check** — grep for similar function names, check graph.json exports for existing utilities
5. **Implement code** using buff coding standards
6. **Architecture validation** — check that imports follow decided layers, file placement matches plan
7. **Update `graph.json`** for touched files — re-read exports, imports_from, line count, last_modified
8. **Stage for git commit** at logical completion (coordinate with git hook)

Never invent architecture that contradicts `.buff/plan.md`. If the plan is wrong, flag it explicitly: "Plan says X, but I recommend Y because [reason]. Shall I update the plan?"

## Writes to counterfeit

After coding, write back to counterfeit memory stores:

- **New file entries** → `.buff/memory/graph.json` — add full entry with exports, imports_from, imported_by (update referencing files too), lines, last_modified
- **Dependency links** → `.buff/memory/graph.json` — update imported_by arrays on files that the new/modified file imports from
- **Drift events** → `.buff/memory/learnings.json` — record what drifted and how it was fixed
- **Novel patterns** → `~/.buff/memory/patterns.json` — if the user introduces a pattern not yet recorded, add it

## Correction detection

Watch for the user correcting code output (rejection, replacement, redirect). Follow the correction capture mechanism defined in `counterfeit` SKILL.md — detect signals, record to `learnings.json` + `corrections.json`, promote to `patterns.json` at 2+ occurrences. Use `skill: "code"` when writing correction entries. Apply the correction immediately without arguing.

## Graph update (post-skill)

After writing or editing files, update `.buff/memory/graph.json` entries for every file touched:

- Re-read the file's export statements → update `exports` array
- Re-read import statements → update `imports_from` array
- Count lines → update `lines`
- Set `last_modified` to current timestamp
- Update `imported_by` on any newly imported files

This is the "lazy update" trigger defined in counterfeit v2 — the graph stays current without expensive full-project scans.

## `/buff:code explain` output format

```
## [Filename] explanation

**What it does**: [1-2 sentences]

**Key functions**:
- `functionName(params)` — [one line]
- `functionName(params)` — [one line]

**Data flow**: [1-3 sentences tracing input → output]

**Notable patterns**: [anything non-obvious]
```

## `/buff:code audit` output format

```
## Code audit — [filename]

| Issue | Line | Severity | Fix |
|---|---|---|---|
| [description] | L42 | high/med/low | [specific fix] |

**Summary**: N issues found (H high, M medium, L low)
```

Severity guide:
- **High**: Bug, security issue, data loss risk, type unsafety at boundary
- **Med**: Performance problem, unclear intent, missing error handling
- **Low**: Style inconsistency, minor naming issue, optional improvement

## Counterfeit integration

See the Skill Integration Map in `counterfeit` SKILL.md for the full read/write contract. Key reads: `preferences.json` (`code_style.naming`, `code_style.imports`, `code_style.error_handling`), `patterns.json`, `corrections.json`, `graph.json`, `decisions.json`, `learnings.json`. Key writes: `graph.json` (file entries), `learnings.json` (drift events), `patterns.json` (novel patterns), `corrections.json` (cross-project corrections).

## Additional Resources

- **`references/patterns.md`** — Language-specific patterns, idioms, anti-patterns, and cross-file patterns by stack
