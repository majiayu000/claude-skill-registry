---
name: de-dupe
description: Remove duplicated code and tech debt by keeping code DRY. Use when asked to de-duplicate logic, extract shared utilities, or refactor repeated patterns ("keep code DRY", "remove duplicated code", "extract common functions", "reduce tech debt"). Include checks for uncommitted changes before refactors.
---

# De-dupe and DRY Refactor

Follow a safe, repeatable workflow to find duplicated code, extract shared helpers, and reduce maintenance burden while preserving behavior.

## Workflow

1. Check for uncommitted changes before refactor.
   - Run `git status -sb` and note touched files.
   - If the tree is dirty, prefer working incrementally and avoid mixing unrelated changes.

2. Identify duplication targets.
   - Scan for obvious repeats in the touched files.
   - Use `rg` to find similar blocks or repeated strings.
     - Example: `rg -n "functionName|error message|regex literal" src/`
     - Example: `rg -n "(\w+\([^)]*\))" src/` then narrow to common blocks.

3. Decide if extraction is warranted.
   - Extract when logic is repeated 2+ times and the abstraction is stable.
   - Do not extract when it makes call sites harder to read or behavior diverges.

4. Extract shared utilities.
   - Create a small function with a focused signature.
   - Place in an existing shared module or create a new `utils`/`shared` file.
   - Keep side effects explicit and minimize hidden dependencies.

5. Replace duplicates.
   - Update call sites to use the new helper.
   - Remove redundant code and keep names consistent.

6. Verify behavior.
   - Update or add tests when behavior is non-trivial.
   - Run relevant tests or linters if available.

## Heuristics

- Prefer simple helpers over deep class refactors.
- Keep params explicit; avoid passing large context objects without need.
- Extract constants for repeated literals (strings, regexes, numbers).
- If duplication is across layers, consider moving logic to the lowest shared layer.

## Guardrails

- Avoid introducing new dependencies for small refactors.
- Do not change public APIs unless explicitly requested.
- Preserve performance characteristics; avoid extra allocations in hot paths.

## Notes for Codex

- Use `rg` for fast discovery and validate with context before editing.
- Keep the diff small and focused; do not mix refactors with unrelated changes.
