# API Usage Review Reference

## Review Instructions

1. Identify external library/framework APIs in the code. Cross-reference with project dependency files to determine library versions in use. Filter out standard library and language built-ins. Focus on third-party dependencies. If no external library usage is found, report that and stop.
2. For each identified library with non-trivial usage: resolve the library using documentation MCP tools or WebSearch, query for the specific APIs being used, and note the documented signatures, parameter types, return types, deprecation status, and version requirements.
3. Check available skills for any relevant to the libraries or frameworks identified. Run matching skills to load domain-specific best practices as additional review context.

## What to Review

- **Wrong signatures** — incorrect parameter count, order, or types
- **Deprecated APIs** — using methods/classes/functions marked as deprecated
- **Superseded APIs** — older API still works but documentation recommends a newer alternative
- **Version mismatches** — using APIs not available in the project's pinned version
- **Missing required parameters** — omitting parameters that have no default value
- **Incorrect return type assumptions** — treating the return value as a different type than documented
- **Configuration errors** — invalid option names, wrong value types, removed configuration keys
- **Breaking change patterns** — usage patterns that match known breaking changes between versions
- **Best-practice violations** — patterns that contradict guidance from loaded skills

## Determination Criteria

Flag an issue only when ALL of these hold:

1. The documentation or loaded skill clearly contradicts the usage (not ambiguous or underdocumented)
2. The issue is discrete and actionable
3. The documented behavior applies to the library version in the project's dependency file
4. The issue would cause incorrect behavior, a runtime error, a deprecation warning, or uses an API the documentation explicitly recommends superseding

## Priority Levels

- **P0** — Will cause a runtime error or crash (wrong signature, removed API)
- **P1** — Will cause incorrect behavior silently (wrong parameter type coerced, deprecated API with changed semantics)
- **P2** — Deprecated API that still works but will be removed in a future version
- **P3** — Suboptimal usage where documentation recommends a better alternative

## What to Ignore

- Standard library and language built-in usage
- APIs where documentation is ambiguous or unavailable
- Internal project APIs (only check third-party dependencies)
- Style preferences not grounded in documentation

**Extra metadata:** `**Library:** <name> <version>` and `**Docs:** <brief quote or paraphrase>`

**Verdict label:** `API Usage: <correct | issues found>`
