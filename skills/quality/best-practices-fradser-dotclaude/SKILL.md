---
name: best-practices
description: This skill should be used when the user asks to "refactor", "refactor the whole project", "simplify code", "clean up code", "apply best practices", "improve readability", "reduce duplication", "standardize patterns", "improve performance", "optimize Next.js performance", "make code more maintainable", "follow coding standards", "optimize code quality", or requests behavior-preserving refactoring with best-practice guidance.
user-invocable: false
version: 1.2.0
---

# Best Practices

## Scope

Support both:

- **Targeted refactoring**: recently modified code in the current session, or specific files/directories provided by the user
- **Project-wide refactoring**: entire repository when explicitly requested

## Agent Invocation

Launch the `code-simplifier` agent for execution. Pass the target scope and any constraints. If already running inside `code-simplifier`, skip launching and proceed with the workflow.

## Language References

Based on file extension, load the appropriate reference:

- `.ts`, `.tsx`, `.js`, `.jsx` → See `references/typescript.md`
- `.py` → See `references/python.md`
- `.go` → See `references/go.md`
- `.swift` → See `references/swift.md`

For universal principles applicable to all languages, see `references/universal.md`.

## Next.js Best Practices References

Use the Next.js reference set when the target includes Next.js code (typically `.tsx`, `.jsx`, Next.js app/pages routes, Server Components, Client Components).

Reference directory:

- `references/nextjs/`

Recommended entry points:

1. Read `references/nextjs/INDEX.md` for complete pattern index organized by impact level and category.
2. Read `references/nextjs/_sections.md` to understand priorities and categories.
3. Read the specific rule file(s) that match the pattern observed (for example, `async-defer-await.md`, `bundle-dynamic-imports.md`).

## Rule Application Guidance

- Prefer **CRITICAL** rules first when there is evidence of user-facing impact (waterfalls, bundle size, hydration issues).
- Keep changes minimal and targeted; optimize only when the pattern is present in the code.
- Preserve behavior and public interfaces; do not change externally visible semantics during a refactor.

## Framework and Language Detection

Before applying refactoring rules, detect the project's frameworks and languages:

1. **Framework Detection**:
   - Check for Next.js: Look for `next.config.js`, `next.config.ts`, or `"next"` in package.json dependencies
   - Check for React: Look for `"react"` in package.json dependencies
   - Check for Vite: Look for `vite.config.js`, `vite.config.ts`
   - Check for other frameworks as needed

2. **Language Detection**:
   - Scan file extensions: `.ts`, `.tsx` (TypeScript), `.js`, `.jsx` (JavaScript)
   - `.py` (Python), `.go` (Go), `.swift` (Swift)

3. **Rule Category Selection**:
   - Based on detected frameworks and user configuration, determine which rule categories to apply:
     - **Next.js projects only**: async, bundle, server, client, rerender, rendering, js, advanced
     - **React (non-Next.js) projects**: client, rerender, rendering, js
     - **All projects**: Universal principles, language-specific rules

**IMPORTANT**: Only apply Next.js-specific rules if Next.js is actually detected. For Tauri + React + Vite projects or other React setups without Next.js, only apply React-specific and universal rules.

## Rule Application Strategy

Apply rules based on framework detection and project characteristics:

- **Next.js-specific rules**: Only applied if Next.js is detected
- **Language-specific rules**: Applied based on detected file types
- **Universal rules**: Applied to all projects

Framework detection determines which rule categories are applicable.

## Code Quality Standards

Apply these standards during all refactoring operations:

- **Comments**: Only add comments explaining complex business logic or non-obvious decisions; remove comments that restate code or conflict with file style
- **Error Handling**: Add try-catch only where errors can be handled/recovered; remove defensive checks in trusted internal paths (validate only at boundaries: user input, external APIs)
- **Type Safety**: Never use `any` to bypass type issues; use proper types, `unknown` with type guards, or refactor the root cause
- **Style Consistency**: Match existing code style in file and project; check CLAUDE.md for conventions
- **Aggressive cleanup**: Remove unused imports, variables, functions, and type definitions completely
- **No backwards-compatibility hacks**: Delete unused `_vars`, remove re-exports of deleted code, remove `// removed` comments
- **Proper renaming**: Rename poorly named variables/functions to descriptive names instead of marking them unused
- **Delete dead code**: If code is unreachable or unused, delete it completely rather than commenting it out

## Workflow

1. **Identify**: Determine target scope (specified files/directories, session modifications, or entire project)
2. **Detect**: Identify frameworks (Next.js, React, Vite, etc.) and languages in the codebase
3. **Load References**: Load language references for the target files, plus framework-specific references when applicable
4. **Filter Rules**: Only apply rules for detected frameworks (e.g., skip Next.js rules if Next.js not present)
5. **Analyze**: Review code for complexity, redundancy, and best-practice violations that matter for the target scope
6. **Execute**: Apply behavior-preserving refinements following the loaded references and Code Quality Standards
7. **Validate**: Ensure tests pass (or suggest the most relevant tests to run) and the code is cleaner
