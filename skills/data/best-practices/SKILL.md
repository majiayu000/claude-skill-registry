---
name: best-practices
description: Provides language-specific best practices, code quality standards, and framework detection for refactoring workflows
user-invocable: false
version: 1.3.0
---

# Best Practices

## Language References

Based on file extension, load the appropriate reference:

- `.ts`, `.js` → `references/typescript.md`
- `.tsx`, `.jsx` → `references/typescript.md` + `references/react/react.md`
- `.py` → `references/python.md` + `references/python/INDEX.md`
- `.go` → `references/go.md`
- `.swift` → `references/swift.md`

Universal principles: `references/universal.md`

## Next.js/React References

For Next.js projects, use `references/react/` directory:

1. `references/react/rules/INDEX.md` - pattern index by impact level
2. `references/react/rules/_sections.md` - priorities and categories
3. Specific rule files matching observed patterns

## Rule Application

- Auto-detect frameworks; only apply Next.js rules if Next.js is detected
- Prefer **CRITICAL** rules first (waterfalls, bundle size, hydration)
- Preserve behavior and public interfaces

## Code Quality Standards

- **Comments**: Only for complex business logic; remove code-restating comments
- **Error Handling**: Try-catch only where recoverable; no defensive checks in trusted paths
- **Type Safety**: No `any`; use proper types or `unknown` with guards
- **Style**: Match existing code style; check CLAUDE.md
- **Cleanup**: Remove all unused imports, variables, functions, types
- **No compat hacks**: Delete unused `_vars`, re-exports of deleted code
- **Renaming**: Use descriptive names instead of marking unused
- **Dead code**: Delete completely, never comment out

## Workflow

1. **Identify** target scope
2. **Detect** frameworks and languages
3. **Load** language + framework references
4. **Filter** rules for detected frameworks only
5. **Analyze** complexity, redundancy, violations
6. **Execute** behavior-preserving refinements
7. **Validate** tests pass
