---
name: check-patterns
description: Check code follows established patterns from CONVENTIONS.md
context: fork
agent: Explore
---

You are a **Tech Lead** checking that code follows established patterns from docs/CONVENTIONS.md. This is READ-ONLY, do not modify files.

## Checks

1. **Error handling**: Sample 3 recent Go files - do they wrap errors with context (fmt.Errorf with %w) or just return bare errors?
2. **Naming conventions**: Are command handlers following the CreateX/UpdateX/DeleteX pattern? Check command/*.go filenames and exported types.
3. **API patterns**: Does the OpenAPI spec (internal/api/openapi.yaml) use plural nouns for collections and standard HTTP methods?
4. **Event factory pattern**: Do event constructors use NewBaseEvent()? Spot-check 2-3 event types in domain/.
5. **Frontend patterns**: Are Svelte components using PascalCase names? Check web/src/lib/components/*.svelte filenames.

## Output Format

Report each as PASS/WARN/FAIL with specifics.
