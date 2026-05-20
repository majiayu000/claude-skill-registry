---
name: 'Review Pull Request'
description: 'Analyze a pull request diff and provide structured feedback on correctness, conventions, and quality.'
---

1. **Read the diff**: Run `git diff main...HEAD` to see all changes in the branch. If a PR number is provided, use `gh pr diff <number>` instead.

2. **Check for correctness**:
   - Logic errors and potential bugs
   - Proper error handling (no swallowed errors, meaningful messages)
   - Null/undefined safety given `noUncheckedIndexedAccess` is enabled
   - Correct use of Zod schemas (`.safeParse()` for untrusted input, `.parse()` for internal data)

3. **Check conventions**:
   - Module boundaries respected (processors only import from `shared`, no cross-scope imports)
   - Path aliases used (`@carrot-fndn/shared/...`) instead of relative imports across libraries
   - Conventional commit message format in PR title
   - No real data in tests (no real company names, tax IDs, plates, addresses, or PII)
   - Test stubs use `@faker-js/faker` and `zocker` helpers

4. **Check test coverage**:
   - New logic has corresponding unit tests
   - Rule processors have both `*.spec.ts` and `*.e2e.spec.ts` files
   - Test cases use `describe` blocks and `it.each` for table-driven patterns where appropriate

5. **Run quality gates**: Execute `pnpm lint:affected && pnpm ts:affected && pnpm test:affected` to verify all checks pass.

6. **Provide feedback** grouped by severity:
   - **Critical**: Bugs, logic errors, security issues, broken tests, real data in tests
   - **Suggestion**: Missing tests, naming improvements, better patterns, performance concerns
   - **Nit**: Style preferences, minor readability improvements

Focus on bugs and logic errors over style. If everything looks good, say so explicitly.
