---
name: haskell
description: Expert Haskell development assistance. Use when working with Haskell code, .hs files, Cabal, ghcid, or when user mentions Haskell, functional programming, or type-level programming.
---

# Haskell Development

Expert assistance for Haskell programming.

## Guidelines

**CRITICAL - Error Handling in Code**: NEVER write code that silently ignores errors:
- Do NOT use `undefined` or `error` as placeholders
- Do NOT skip handling error cases in pattern matches
- Do NOT ignore `Maybe`/`Either` failure cases
- Handle all possible cases explicitly
- Use types to make impossible states unrepresentable

Every error case in generated code must be handled properly.

**CRITICAL - Compile Status**:
- The code MUST compile without errors.
- You MUST check `ghcid.txt` after every change and fix any errors reported there.
- Do NOT proceed to verification or linting until `ghcid.txt` is clean.

**CRITICAL - HLint Compliance**:
- You MUST check for `.hlint.yaml` in the project root.
- If it exists, you MUST run `hlint` on any file you modify.
- You MUST fix ALL hlint warnings before considering the task complete.
- Do NOT ignore hlint warnings unless explicitly instructed by the user.

**Code Quality**:
- Write type signatures for all top-level definitions
- Write total functions (avoid `head`, `tail`)
- Prefer pure functions over IO when possible
- Use explicit exports in modules
- Leverage type system for safety
- Favor composition over complex functions
- Write Haddock documentation for public APIs

**Idiomatic Patterns**:
- Prefer `Text` over `String`
- Use `newtype` wrappers for domain types
- Apply smart constructors for validation
- Records:
    - Use RecordDotSyntax & OverloadedRecordDot (add pragma to modules that use the syntax)
    - Use DisambiguateRecordFields and DuplicateRecordFields for simple field names (add pragma to modules that use the syntax)
- Use lenses for record manipulation when appropriate
- Use `Applicative` and `Monad` appropriately
- Avoid trivial `let` bindings when inlining keeps code simple and readable

**Working with Aeson**:
- NEVER construct aeson objects by hand
- Instead create a type and use `encode` and `decode` on it
- These types should generally use generic deriving of aeson (no hand deriving)


## Relude Best Practices

When using `relude`, refer to [RELUDE.md](RELUDE.md) for best practices and idioms.

## Testing

- Use QuickCheck for property-based testing
- Use HUnit or Hspec for unit tests
- Provide good examples in documentation

## Build instructions

As you make code changes, start a subagent in parallel to resolve any compile errors in `ghcid.txt`.

**IMPORTANT**: Do not run build commands yourself. The human runs ghcid in the terminal, which then updates `ghcid.txt` with any compile error or warning (if this file does not exist, or if ghcid has stopped, remind the human to address it). You should read `ghcid.txt` (in _entirety_) after making code changes; this file updates near-instantly.

**Adding/Deleting modules**: When a new `.hs` file is added or deleted, the `.cabal` file must be updated accordingly. However, if `package.yaml` exists in the project, run `hpack` instead to regenerate the `.cabal` file with the updated module list. This will trigger `ghcid` to restart automatically.

**HLint warnings**: MANDATORY. After `ghcid.txt` shows success, if `.hlint.yaml` exists, run `hlint` on the modified files. You are NOT done until `hlint` reports no issues.
