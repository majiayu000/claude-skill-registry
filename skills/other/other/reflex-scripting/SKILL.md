---
name: reflex-scripting
description: Use this skill for Reflex library commands and scripting — direct one-off commands (reflex xlsx, reflex rest, reflex csv, ...), inline Lua/Python scripts, and saved reusable scripts.
---

# Reflex Scripting & Library Skill

## Purpose

Use this skill when you need to use **Reflex libraries** — whether through direct CLI commands, inline scripts, or saved script files. This covers:

- **Direct library commands**: `reflex xlsx open data.xlsx sheet Sheet1 get-cell 1 1` — one-liner operations without writing any script
- **Inline scripts**: `reflex lua exec "..."` — complex one-off logic without creating a file
- **Saved scripts**: `reflex lua run <file>` — reusable automation the user can run again

Default language: **Lua**. Use Python only when the user explicitly asks for Python or there is a clear reason not to use Lua.

## When To Use This Skill

- User asks to manipulate files (xlsx, csv, json) without a browser
- User asks to call a REST API
- User asks for data transformation or batch processing
- User asks for a reusable Lua or Python script
- User wants to export data collected via browser to a file
- User asks for any non-browser library operation

## When NOT To Use This Skill

- User asks to interact with a website or browser → use `reflex-browser` first
- Pure browser automation without scripting → use `reflex-browser`

## Starting Point Decision

### Does the task involve a website?

Start with the `reflex-browser` skill first. Use `reflex browser ...` to inspect the site, validate selectors, and prove the flow. Come back here when:

- The browser flow is validated and needs to be turned into a script
- You need loops, branching, retries, or composition beyond single browser commands
- You need to export collected browser data to a file

Carry forward all discovered selectors, refs, URLs, and page transitions — do not restart discovery.

### Is the task non-browser?

Start directly here. Choose the simplest approach that solves the task:

1. **Direct command** if it can be done in one chained call
2. **Inline script** (`reflex lua exec "..."`) if it needs loops, conditions, or multiple library calls
3. **Saved script** (`reflex lua run <file>`) only if the user wants something reusable

## Three Ways To Use Libraries

### 1. Direct Library Commands

Run library methods directly from the command line. The CLI compiles the chain into a script and executes it — no script file needed.

Syntax: `reflex <library> <method> [args] [method] [args] ...`

```bash
# Read a cell from an Excel file
reflex xlsx open data.xlsx sheet Sheet1 get-cell 1 1

# Make a GET request
reflex rest get https://api.example.com/data

# Chain multiple operations
reflex xlsx open report.xlsx sheet Summary get-cell 1 2
```

Each chained method call operates on the return value of the previous one. For example, `xlsx open ... sheet ... get-cell ...` chains: `Xlsx.open(path)` → `.sheet(name)` → `.getCell(col, row)`.

Use direct commands when the task is a single operation or a short chain. If you need loops or conditions, escalate to inline script.

### 2. Inline Scripts (`reflex lua exec`)

For complex one-off logic that does not need a saved file:

```bash
reflex lua exec "
local wb = Xlsx.open('data.xlsx')
local sheet = wb.sheet('Sheet1')
local value = sheet.getCell(1, 1)
wb.close()
Xlsx.close()
return value
"
```

Use inline scripts when the task needs loops, branching, retries, multiple library calls, or composition — but the user did not ask for a saved file.

### 3. Saved Scripts (`reflex lua run`)

For reusable automation the user wants to run again:

```bash
reflex lua run scripts/export-data.lua
```

Only create a saved script file when the user explicitly asks for a reusable script or the task clearly benefits from reuse.

## Library Discovery

Find available libraries and their methods:

```bash
# List all libraries available for Lua
reflex lua libs

# List all libraries available for Python
reflex python libs

# Get help for a specific library (shows methods, arguments, chaining, examples)
reflex help <library>
reflex lua help <library>
```

Check library help once when you need exact method signatures. Do not run broad capability audits before you have a concrete task.

## Core Rules

1. Use `reflex help <library>` as the syntax source of truth for library methods.
2. Prefer direct library commands for one-off operations — they are first-class CLI features, not workarounds.
3. Keep non-browser library usage stateless inside one script execution.
4. Pass native Lua/Python data structures in scripts; pass JSON only for direct CLI commands.
5. Reuse selectors, refs, URLs, and page assumptions discovered in browser CLI exactly, including prefixes such as `css=` and `xpath=`.
6. Check output library constraints once up front; do not wander into alternate stacks just because a library has a constraint.
7. If the user asks to create a file such as Excel output but does not ask for a script, prefer the direct command or `reflex lua exec ...` first.

## Browser-Backed Script Rules

When a script automates a browser flow discovered via the `reflex-browser` skill:

1. The script continues a known browser flow — it is not a new discovery phase.
2. Use the exact selectors and URLs validated during browser discovery; do not strip prefixes like `css=`.
3. Prefer targeted browser reads/actions over `browser.source()` or whole-page regex parsing.
4. Use `reflex browser lua` only after the browser flow is already stable; treat its output as a trace to refactor, not the final script.
5. Do not restart with broad research once the browser flow is already validated.

## Output Planning

1. Verify the output library's constraints once before writing export logic.
2. `Csv` is the simplest path for tabular output; use it when the user does not specifically require `.xlsx`.
3. If the user explicitly wants `.xlsx`, check whether `Xlsx` requires a template and decide the template path early.
4. `Fl.write(path, content)` handles JSON, Markdown, or plain text output.
5. Do not jump to Python packages, external tools, or alternative approaches just to avoid a library constraint unless the user explicitly asks for that route.
6. Output planning should support the task, not derail it.

## Authoring Workflow

1. Identify which library you need:
   - `reflex help <library>` for the one concrete library you need next
   - use `reflex lua libs` only when the correct library is genuinely unknown
2. For browser-backed tasks, do browser discovery first (see `reflex-browser` skill).
3. For non-browser tasks, start with the direct command if possible.
4. Escalate to `reflex lua exec "..."` when you need loops, branching, or multiple calls.
5. Write a saved script file only after the flow is understood and the user actually wants a reusable file.
6. If the user explicitly asks for Python, switch the same workflow to `reflex python ...`.

## Anti-Patterns (Forbidden)

1. Jumping to a saved script file when a direct command or `reflex lua exec` would suffice.
2. Starting with broad capability audits (`reflex lua libs`, repeated `help` calls) before trying the task.
3. Writing a browser automation script without first validating the flow with `reflex browser ...`.
4. Restarting discovery from scratch when moving from browser to script — carry forward the validated flow.
5. Treating browser, direct commands, and scripting as competing options instead of layers of the same tool.
6. Stripping selector prefixes (`css=`, `xpath=`) when moving discovered selectors into scripts.

## Worked Examples

- Browser page → one-off export (browser + direct chaining, no saved script):
  - `skills/reflex-browser/examples/page-to-export-one-off.md`
- Careers page → Excel output → reusable Lua script:
  - `skills/reflex-browser/examples/careers-to-xlsx-lua.md`
