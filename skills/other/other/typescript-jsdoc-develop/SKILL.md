---
name: typescript-jsdoc-develop
description: Create, repair, or standardize JSDoc in .js, .ts, and .tsx files with deterministic non-behavior-changing edits. Use when users ask to add missing docs, refresh stale comments after signature changes, enforce tag quality (@param/@returns/@throws/@example), or document functions, classes, types, and React components.
---

# JSDoc Create/Update

Use this workflow to add or repair JSDoc without changing runtime behavior.

## Inputs to collect

- Confirm target files or symbols.
- Confirm coverage level: exported/public only (default) or full/internal.
- Confirm strictness: baseline tags only (`@param`, `@returns`) or full tags (`@throws`, `@example`, optional `@deprecated`/`@see`/`@remarks`).
- Confirm whether comment style must match existing repository conventions.

## Scope defaults

Document by default:
- Exported functions, public methods, and classes.
- Public interfaces/types when brief intent text adds value.
- React components and major props behavior.

Skip by default unless requested:
- Trivial one-liners, obvious getters/setters, and private implementation details.

## Preflight checks

1. Inspect target files for existing lint/doc rules that constrain JSDoc format.
2. Identify declarations changed since last documentation update (if stale docs are suspected).
3. Confirm no runtime edits are needed; this skill edits comments only.

## Workflow

1. Inspect declarations and current JSDoc blocks in target files.
2. Keep useful existing docs; update stale text to match current signatures and behavior.
3. Add missing JSDoc blocks only where scope rules require coverage.
4. Place each JSDoc block directly above its declaration with no blank line.
5. Write a short first sentence, then tags in this order when relevant:
   - `@param`
   - `@returns`
   - `@throws`
   - `@example`
   - optional tags like `@deprecated`, `@see`, `@remarks`
6. Verify accuracy:
   - Parameter names match exactly, including destructured properties.
   - Optional/default parameters are documented correctly.
   - Return and thrown behavior matches actual code.
   - No behavior changes were introduced while editing.
7. Run repository checks for touched files (for example lint/typecheck/test targets) when available.

## Language rules

### JavaScript (.js)

- Use JSDoc types (`{Type}`) for parameters/returns because types are not in the signature.
- Use `@typedef` and `@property` when the type exists only in JSDoc.

### TypeScript and TSX (.ts/.tsx)

- Prefer types in code; use JSDoc mainly for behavior and intent.
- Omit `{Type}` when the signature is already clear; include it only when it clarifies unions or generics.
- For overloaded functions, document behavior on the implementation block.
- For React components, document purpose and key props, or reference the props interface when clear.

## Edit constraints

- Do not rename symbols, reorder logic, or refactor implementations while documenting.
- Do not invent thrown errors, return values, or side effects that are not present in code.
- Preserve valid existing terminology unless it is clearly incorrect.

## Quality bar

- Do not add boilerplate text that repeats the signature.
- Keep comments concise and useful for IDE hovers and TypeDoc output.
- Preserve existing terminology and style unless it is clearly wrong.
- Ensure each edited block is internally consistent (summary sentence and tags describe the same behavior).

## Additional resources

- Tag details and edge cases: [reference.md](reference.md)
- Before/after patterns: [examples.md](examples.md)
