---
name: analyze-cc-feature
description: >
  Reverse engineer and analyze a specific feature in Claude Code's source.
  Use when the user wants to understand how a Claude Code feature works
  internally, or when asked to analyze Claude Code internals.
argument-hint: [feature-keyword]
---

# Analyze Claude Code Feature

Reverse engineer a specific feature in Claude Code's source code.

**Terminology note**: Claude Code's `cli.js` is **minified** (whitespace removed, identifiers shortened for size), NOT **obfuscated** (intentionally made hard to read with control flow flattening, string encryption, etc.). webcrack's `--no-deobfuscate` flag is used because there is no obfuscation to reverse. The output file is called `deobfuscated.js` by webcrack convention, but it is more accurately "unminified" source.

**IMPORTANT**: Use the task list (TaskCreate/TaskUpdate) to track progress through the pipeline. Create all tasks upfront, then work through them sequentially, marking each in_progress when starting and completed when done.

## Pipeline

Create these tasks at the start:

1. **Acquire source** — Download and extract cli.js from npm
2. **Unminify** — Run webcrack + prettier to produce readable source
3. **Locate the feature** — Search for anchor strings to find the code
4. **Extract & annotate** — Pull out the feature's code, rename identifiers inline
5. **Analyze** — Document what the feature does step by step
6. **Write report** — Produce a markdown report with evidence
7. **Self-reflect** — Evaluate whether the skill itself should be updated

If the user says to skip steps (e.g., "unminified source already exists at X, skip steps 1-2"), create those tasks as completed immediately.

---

### Step 1: Acquire source

Run `scripts/extract-cli.sh` to download and extract `cli.js` from the npm package. The script caches by version.

```bash
bash ~/.claude/skills/analyze-cc-feature/scripts/extract-cli.sh
```

This produces `/tmp/claude-code-npm/package/cli.js`.

### Step 2: Unminify

Run `scripts/unminify.sh` to produce readable source. The script caches the output.

```bash
bash ~/.claude/skills/analyze-cc-feature/scripts/unminify.sh
```

This produces a `webcrack-output/deobfuscated.js` file (700K+ lines, well-formatted). Despite the filename, this is unminified code — see terminology note above.

### Step 3: Locate the feature

Search the unminified source for the feature keyword the user specified. Use multiple anchor strings:

- The command/feature name as a string literal (e.g., `"insights"`, `"compact"`)
- Any known prompts or descriptions associated with the feature
- `querySource:` values that tag API calls
- Known field names, labels, or HTML content
- Telemetry event names (e.g., `"tengu_compact"`, `"tengu_input_command"`)

Use Grep to find all occurrences and identify the line range where the feature's code is concentrated. Search for at least 3-4 different anchor strings to triangulate.

### Step 4: Extract & annotate

Read the identified line range from the unminified file. Read in large chunks (500+ lines) to see full boundaries. Also search for any helper functions called from within the range that are defined elsewhere (API call wrappers, model selectors, data loaders, prompt builders).

Save an annotated file as `{feature}-annotated.js` (or `{feature}-raw.js` + `{feature}-clean.js` if producing both raw and renamed versions) that contains:
- The extracted code with mangled identifiers **renamed inline** to meaningful names
- Comments explaining non-obvious logic
- Line references back to `deobfuscated.js` (e.g., `// deobfuscated.js:554320`)

**Renaming technique:**

- Function names: infer from string literals in return values, object properties, error messages
- Parameters: infer from how they're used (e.g., parameter passed to `.filter()` is likely an item)
- Variables: infer from what they hold (e.g., variable set to `new Map()` and used with `.get()/.set()` with session IDs is a session map)

Rules:
- Only rename what is unambiguous
- Flag uncertain renames with `/* uncertain */` comments
- Never rename inside string literals, template literals, or regex patterns
- Multi-character identifiers (function names, module vars) are safe for global replace
- Single-character identifiers must be renamed within function scope only
- Avoid renaming `$` or `_` in functions with template literals (conflicts with `${...}`)
- Use the **Mangled identifier reference** table in [REFERENCE.md](REFERENCE.md#mangled-identifier-reference) to recognize known infrastructure functions

**Scoping strategy**: Find the `v(() => { ... })` lazy initializer that sets up the feature's module. All functions between this initializer and the next one belong to the same module. For `local-jsx` commands, also trace the `load:` → module → `call` export chain to find the entry-point component, then include all components it renders.

### Step 5: Analyze

Read the annotated code and document:
- What the feature does, step by step
- What LLM calls it makes (model, prompts, token limits)
- What data it reads and writes
- Any caching or privacy mechanisms
- Cross-reference against actual output if available (run the feature first)

### Step 6: Report

Produce a markdown report with:
- Model and cost metadata at the top (model used, estimated API cost, date, source)
- Architecture overview (Mermaid diagram if helpful)
- Pipeline stages with code excerpts from the annotated file
- Tables for any taxonomies, enums, or mappings
- Findings about behavior, edge cases, interesting details
- All claims backed by specific code evidence (cite as `deobfuscated.js:NNNNN`)

### Step 7: Self-reflect

After completing the analysis, evaluate the **skill itself** (this file + REFERENCE.md):

1. **Were there patterns or infrastructure functions discovered during this analysis that should be added to the Common Patterns table or REFERENCE.md?** For example, new helper functions, new command types, new telemetry patterns.
2. **Did the pipeline steps feel right, or was anything wasteful/missing?** For example, if a step was skipped because it didn't add value, or if a missing step would have helped.
3. **Was the scoping strategy effective?** Did the lazy-init boundary approach correctly identify the module boundaries?

If improvements are warranted, **propose specific edits** to this SKILL.md or REFERENCE.md and ask the user if they'd like to apply them. Not every analysis will produce skill updates — only suggest changes when they'd concretely help future analyses.

---

## Command types

Commands have different `type` values that affect how to analyze them:

- **`type: "prompt"`** — Injects a prompt into the conversation. Look for `getPromptForCommand`. These are pipeline-style features (like `/insights`) with procedural logic.
- **`type: "local"`** — Runs code locally without sending a prompt to the LLM. The module exports `{ call: entryFunction }` which is invoked directly. The return value determines what happens (e.g., `type: "compact"` replaces the entire conversation). Examples: `/compact`, `/clear`, `/copy`.
- **`type: "local-jsx"`** — Renders a React/Ink UI component. Look for `load:` which returns a module with a `call` export. These are UI-heavy features (like `/usage`) built as component trees.

For `local-jsx` commands, the extraction strategy differs — see the React/Ink section below.

### How commands are dispatched

The dispatch function (`NGY`) matches on `command.type`:
- `"local"` — Calls `(await command.load()).call(args, toolUseContext)` and handles the return type (`"compact"`, `"skip"`, `"microcompact"`, or plain value)
- `"local-jsx"` — Same load pattern, but the result is rendered as JSX
- `"prompt"` — Calls `command.getPromptForCommand(args, context)` and injects the result as messages

## React/Ink components

Many features render UI using React (via Ink for terminal). Key patterns:

- **`q1(N)` + `Symbol.for("react.memo_cache_sentinel")`** — React Compiler memoization boilerplate. This is verbose but mechanical: it caches JSX elements to avoid re-renders. When reading, mentally skip the cache check/set pattern and focus on what's being created (`createElement` calls, props, children).
- **Component boundaries** — A module's components are grouped between consecutive `v(() => { ... })` lazy initializers. All functions between two initializers typically belong to the same module.
- **Read larger chunks** — React components with memoization are verbose but low-density. Read 500+ lines at a time instead of 80–200 to see full component boundaries efficiently.
- **`createElement(f, { dimColor: true }, ...)`** — `f` is Ink's `<Text>` component. `I` is Ink's `<Box>` (layout container).

## Common patterns

See the **Mangled identifier reference** table in [REFERENCE.md](REFERENCE.md#mangled-identifier-reference) for the full list of known infrastructure functions (telemetry, settings, token counting, hooks, etc.) with their call signatures and stable evidence patterns for re-identification across versions.

## Important notes

- **String literals survive minification perfectly.** They are the primary evidence for understanding what code does. Prompts, error messages, event names, field names — all intact.
- The `querySource` field in API call options tags which feature is making the call.
- The `v(() => { ... })` pattern is a lazy initializer — code inside runs once on first access.
- Look for command definitions: objects with `type: "prompt"`, `name`, `description`, `getPromptForCommand`, or `type: "local-jsx"` / `type: "local"` with `load:`.
- For `local-jsx` commands, trace the `load:` function to find the module, then find its `call` export to locate the entry point.
- **Cite line numbers** in all analysis artifacts as `deobfuscated.js:NNNNN` for traceability.
