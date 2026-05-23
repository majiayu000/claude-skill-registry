---
name: 'Execute Task'
description: 'Autonomously implement a task following project conventions with iterative verification.'
---

1. **Understand the task**: Read the task description or plan carefully. Identify what needs to change, which projects are affected, and any constraints.

2. **Identify affected files**: Use search tools to find relevant files. Understand the existing code structure before making changes. Check module boundaries — processors can only import from `shared` libraries.

3. **Implement changes**:
   - Follow existing patterns in the codebase (look at similar files for reference)
   - Use path aliases (`@carrot-fndn/shared/...`) for cross-library imports
   - Use Zod schemas for runtime validation, derive types with `z.infer`
   - Use `@faker-js/faker` and `zocker` for test data, never real data
   - For rule processors, follow the standard structure: `.processor.ts`, `.lambda.ts`, `.processor.spec.ts`, `.lambda.e2e.spec.ts`, `.test-cases.ts`

4. **Verify after each significant change**: Run quality checks incrementally to catch issues early.
   ```bash
   pnpm lint:affected
   pnpm ts:affected
   pnpm test:affected
   ```

5. **Debug and fix**: If tests or checks fail, read the error output carefully, identify the root cause, and fix it. Do not blindly retry — understand why it failed.

6. **Summarize**: When finished, provide a concise summary of:
   - What was changed and why
   - Any design decisions made
   - Any open questions or follow-up items
