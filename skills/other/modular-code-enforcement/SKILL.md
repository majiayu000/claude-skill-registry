---
name: modular-code-enforcement
description: "Enforces strict modular code architecture: SRP, no monolithic index files, no catch-all utils, 200 LOC hard limit. This rule is NON-NEGOTIABLE. Violations BLOCK all further work until resolved."
---

# Modular Code Architecture — Zero Tolerance Policy

This rule is NON-NEGOTIABLE. Violations BLOCK all further work until resolved.

## Rule 1: index files are ENTRY POINTS, NOT dumping grounds

`index` files (`index.ts`, `__init__.py`, `index.js`, etc.) MUST ONLY contain:
- Re-exports (`export { ... } from "./module"`)
- Factory function calls that compose modules
- Top-level wiring/registration (hook registration, plugin setup)

`index` files MUST NEVER contain:
- Business logic implementation
- Helper/utility functions
- Type definitions beyond simple re-exports
- Multiple unrelated responsibilities mixed together

**If you find mixed logic in an index file**: Extract each responsibility into its own dedicated file BEFORE making any other changes. This is not optional.

## Rule 2: No Catch-All Files — utils/helpers/service are CODE SMELLS

A single `utils`, `helpers`, `service`, or `common` file is a **gravity well** — every unrelated function gets tossed in, and it grows into an untestable, unreviewable blob.

**These file names are BANNED as top-level catch-alls.** Instead:

| Anti-Pattern | Refactor To |
|--------------|-------------|
| `utils` with `formatDate()`, `slugify()`, `retry()` | `date-formatter`, `slugify`, `retry` |
| `service` handling auth + billing + notifications | `auth-service`, `billing-service`, `notification-service` |
| `helpers` with 15 unrelated exports | One file per logical domain |

**Design for reusability from the start.** Each module should be:
- **Independently importable** — no consumer should need to pull in unrelated code
- **Self-contained** — its dependencies are explicit, not buried in a shared grab-bag
- **Nameable by purpose** — the filename alone tells you what it does

If you catch yourself typing `utils` or `service`, STOP and name the file after what it actually does.

## Rule 3: Single Responsibility Principle — ABSOLUTE

Every source file MUST have exactly ONE clear, nameable responsibility.

**Self-test**: If you cannot describe the file's purpose in ONE short phrase (e.g., "parses YAML frontmatter", "matches rules against file paths"), the file does too much. Split it.

| Signal | Action |
|--------|--------|
| File has 2+ unrelated exported functions | **SPLIT NOW** — each into its own module |
| File mixes I/O with pure logic | **SPLIT NOW** — separate side effects from computation |
| File has both types and implementation | **SPLIT NOW** — types file + implementation file |
| You need to scroll to understand the file | **SPLIT NOW** — it's too large |

## Rule 4: 200 LOC Hard Limit — CODE SMELL DETECTOR

Any source file exceeding **200 lines of code** (excluding prompt strings, template literals containing prompts, and markdown content) is an **immediate code smell**.

**When you detect a file > 200 LOC**:
1. **STOP** current work
2. **Identify** the multiple responsibilities hiding in the file
3. **Extract** each responsibility into a focused module
4. **Verify** each resulting file is < 200 LOC and has a single purpose
5. **Resume** original work

Prompt-heavy files (agent definitions, skill definitions) where the bulk of content is template literal prompt text are EXEMPT from the LOC count — but their non-prompt logic must still be < 200 LOC.

### How to Count LOC

**Count these** (= actual logic):
- Import statements
- Variable/constant declarations
- Function/class/interface/type definitions
- Control flow (`if`, `for`, `while`, `switch`, `try/catch`)
- Expressions, assignments, return statements
- Closing braces `}` that belong to logic blocks

**Exclude these** (= not logic):
- Blank lines
- Comment-only lines (`//`, `/* */`, `/** */`)
- Lines inside template literals that are prompt/instruction text
- Lines inside multi-line strings used as documentation/prompt content

**Quick method**: Read the file → subtract blank lines, comment-only lines, and prompt string content → remaining count = LOC.

**Example**:
```typescript
// 1  import { foo } from "./foo";          ← COUNT
// 2                                         ← SKIP (blank)
// 3  // Helper for bar                      ← SKIP (comment)
// 4  export function bar(x: number) {       ← COUNT
// 5    const prompt = `                     ← COUNT (declaration)
// 6      You are an assistant.              ← SKIP (prompt text)
// 7      Follow these rules:                ← SKIP (prompt text)
// 8    `;                                   ← COUNT (closing)
// 9    return process(prompt, x);           ← COUNT
// 10 }                                      ← COUNT
```
→ LOC = **5** (lines 1, 4, 5, 9, 10). Not 10.

When in doubt, **round up** — err on the side of splitting.

## How to Apply

When reading, writing, or editing ANY source file:

1. **Check the file you're touching** — does it violate any rule above?
2. **If YES** — refactor FIRST, then proceed with your task
3. **If creating a new file** — ensure it has exactly one responsibility and stays under 200 LOC
4. **If adding code to an existing file** — verify the addition doesn't push the file past 200 LOC or add a second responsibility. If it does, extract into a new module.

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) modular-code-enforcement rule
