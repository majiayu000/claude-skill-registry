---
name: unit-test-philosophy
description: Risk-based unit testing and Allure-readable behavioral spec style for open-agreements. Use when adding/updating tests, expanding coverage, or reviewing test quality across src, integration-tests, and workspace packages.
metadata:
  short-description: Open Agreements testing philosophy
---

# Unit Test Philosophy (Open Agreements)

## Use this skill when
- A request asks to add tests, improve coverage, or harden regressions.
- A change touches `src/`, `integration-tests/`, `packages/contracts-workspace`, or `packages/contracts-workspace-mcp`.
- You need readable Allure behavior specs and OpenSpec traceability.

## Core philosophy
1. Test highest-risk behavior first.
   Focus first on mutating flows, parser/validator boundaries, and policy/safety checks.
2. Optimize for regression prevention, not just line coverage.
   Prioritize branches where failures could produce wrong legal output or unsafe automation behavior.
3. Treat Allure as test style, not test type.
   Use normal unit/integration tests with Allure labels, steps, and attachments in the same files.
4. Keep spec and test effectively coextensive.
   If behavior is important enough to test, map it to canonical OpenSpec scenarios or active change-package scenarios.
5. Keep assertions behavior-oriented.
   Verify user-observable outputs, diagnostics, and mutation outcomes before internals.
6. Make failures easy to debug.
   Attach structured context for inputs, normalized outputs, and error payloads.

## Repo standards

### Test structure
- Use Given/When/Then/And wording in Allure step titles.
- Keep scenario steps as top-level test steps; avoid wrapping the full test body in synthetic container steps like `Execute test body`.
- Prefer one assertion per step where practical.
- Multiple assertions in one step are acceptable when they validate one cohesive invariant.
- Keep tests deterministic (fixed fixtures, explicit env flags, no timing assumptions).

### Allure API
- Prefer repo helpers over direct raw Allure calls:
  - `integration-tests/helpers/allure-test.ts`
  - Common helpers: `itAllure`, `testAllure`, `allureStep`, `allureJsonAttachment`, `allurePrettyJsonAttachment`, `allureWordLikeTextAttachment`, `allureParameter`, `allureSeverity`
- Do not import from `allure-vitest` in tests.
- Keep helper usage consistent across `src/**/*.test.ts` and `integration-tests/**/*.test.ts`.
- For complex fixtures/stateful flows, attach:
  - a pretty JSON artifact for request/result payloads
  - a human-readable “Word-like” artifact for document/checklist state before and after mutation when relevant
- Rendering note: HTML preview attachments rely on the report post-process sanitizer allowlist patch (`scripts/patch_allure_html_sanitizer.mjs`, invoked by `npm run report:allure`). Do not bypass this pipeline when generating reports for review.

### File naming and placement
- Use collocated test files like `src/<module>.test.ts`.
- Add Allure style inside these tests; do not split by "allure-only" test types by default.
- Keep one test file focused on one module or capability.
- Migration policy: gradually rename legacy `*.allure.test.ts` files to `*.test.ts`; do not introduce new `*.allure.test.ts` files.

### OpenSpec traceability
- Use `.openspec('OA-###')` whenever a matching scenario ID exists for the behavior.
- Scenario IDs may come from either canonical specs (`openspec/specs/open-agreements/spec.md`) or active change-package specs (`openspec/changes/<change-id>/specs/open-agreements/spec.md`).
- Pre-canonical IDs from active change packages are valid during implementation and should remain stable when promoted into canonical specs.
- For new important behavior, add scenario IDs in the active change package first, map tests immediately, then promote those IDs into canonical specs when archiving.

## Coverage expansion workflow
1. Read coverage summaries and identify branch-heavy modules in `src/core/**` and integration flows.
2. Rank by blast radius and mutation risk.
3. Add tests in this order:
   - Validation and error branches
   - Strict vs permissive behavior
   - No-partial-mutation / transactional guarantees
   - Invariants (deterministic outputs, schema safety, idempotency)
4. Run targeted tests first, then full suite and coverage.

## Severity recommendation rubric
- `critical`: mutation correctness, legal-output integrity, data-loss risk, security/policy guardrails.
- `normal`: standard behavior and compatibility scenarios.
- `minor`: narrow edge cases with low production impact.
- Apply severity based on failure impact, not module ownership.

## Command checklist
```bash
npm run test:run
npm run test:coverage
npm run check:spec-coverage
npm run check:allure-labels
```

## Minimal test template (TypeScript)
```ts
import { describe, expect } from 'vitest';
import { itAllure as it, allureStep, allureJsonAttachment } from '../../../integration-tests/helpers/allure-test.js';

describe('checklist patch behavior', () => {
  it('applies replacement deterministically', async () => {
    let result: { ok: boolean };

    await allureStep('Given a valid patch payload', async () => {
      await allureJsonAttachment('patch-input.json', {
        patch_id: 'patch_001',
        operations: [{ op: 'replace', path: '/issues/0/status', value: 'CLOSED' }],
      });
    });

    await allureStep('When patch validation runs', async () => {
      result = { ok: true };
    });

    await allureStep('Then validation succeeds', async () => {
      expect(result!.ok).toBe(true);
    });
  });
});
```

## Extended reference
- See `references/allure-test-spec-writing-guide.md` for full Allure step-writing guidance.
