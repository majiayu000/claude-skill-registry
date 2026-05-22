---
name: nestjs-vitest-coverage
description: Upgrade, repair, and enforce Vitest coverage in NestJS backends with deterministic provider alignment, coverage config hardening, script normalization, threshold enforcement, and test-gap remediation. Use when users ask to fix failing coverage, migrate or change coverage provider (v8/istanbul), configure coverage reporters/thresholds, raise CI coverage, or stop coverage drift after framework/test upgrades.
---

# NestJS Vitest Coverage

Use this workflow to keep NestJS coverage reliable, enforceable in CI, and aligned with current Vitest behavior.

## 1. Preflight and baseline audit

1. Detect package manager from lockfiles and use matching commands (`npm`, `pnpm`, or `yarn`) for all install and script operations.
2. Verify runtime and toolchain:
- `node -v`
- package manager version
3. Verify current versions and coverage package alignment:

```bash
npm ls vitest @vitest/coverage-v8 @vitest/coverage-istanbul
```

4. Confirm where test config lives:
- `vitest.config.ts`, or
- `vite.config.ts` with a `test` block.

5. Check whether `package.json` has `test:cov` and whether coverage output is cleaned.
6. Run baseline coverage once and capture current failures before editing:
- `npm run test:cov` (or package-manager equivalent).

## 2. Upgrade packages

Prefer `v8` coverage unless the project explicitly requires Istanbul compatibility.

`v8` provider:

```bash
npm install -D vitest@latest @vitest/coverage-v8@latest
```

`istanbul` provider:

```bash
npm install -D vitest@latest @vitest/coverage-istanbul@latest
```

Rules:
- Keep `vitest` and selected coverage package on the same major version.
- Install exactly one provider package unless the project intentionally keeps both.
- If both providers are installed unintentionally, remove the unused one.

## 3. Configure coverage

Add or update the `coverage` block in the active Vitest config:

```typescript
coverage: {
  provider: 'v8',
  reporter: ['text', 'html', 'lcov'],
  reportsDirectory: 'coverage',
  include: ['src/**/*.ts'],
  exclude: [
    'node_modules',
    'dist',
    '**/*.spec.ts',
    '**/*.test.ts',
    'src/main.ts',
    '**/*.module.ts',
    'test/**',
  ],
  thresholds: {
    lines: 85,
    functions: 85,
    branches: 80,
    statements: 85,
  },
},
```

Guidelines:
- Set `provider` to match the installed package.
- Keep `text` for terminal feedback and `html` for local inspection.
- Add `lcov` for CI tools such as Sonar and Codecov.
- Use `include` to measure real source files instead of only executed files.
- Exclude only entrypoints, modules, test files, generated code, and tooling.
- Keep or increase existing thresholds; do not reduce thresholds unless user explicitly requests it.

## 4. Ensure scripts are correct

Update `package.json` scripts:

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:cov": "vitest run --coverage",
    "test:cov:watch": "vitest --coverage --watch"
  }
}
```

If a cleanup script exists, ensure coverage output is removed (for example `rimraf dist coverage .cache`).

## 5. Run and inspect coverage

1. Run:

```bash
npm run test:cov
```

2. Inspect:
- Terminal summary for low files and uncovered lines.
- `coverage/index.html` for branch-level gaps.

3. Confirm thresholds are enforced and fail below target.
4. If CI runs coverage, confirm command parity between local and CI scripts/workflows.

## 6. Raise coverage by improving tests

Preferred approach: add or improve tests for uncovered project code.

For NestJS:
- Use `Test.createTestingModule` and mock dependencies with `vi.fn`.
- Add branch tests for success, failure, and edge paths.
- Cover guards, pipes, interceptors, and service error handling.
- In e2e suites, always close the app in `afterAll`.
- Prefer deterministic mocks/spies and avoid flaky time/network coupling.

Do not make coverage pass by excluding maintained source files.

## 7. Apply exclusions responsibly

Allowed exclusions:
- Generated clients (for example Prisma generated output)
- Framework entrypoints (`src/main.ts`)
- Thin wiring modules (`**/*.module.ts`)
- Test/setup files

Avoid excluding controllers, services, handlers, domain logic, and shared libraries.

## 8. Validate completion

- [ ] Coverage command passes locally with enforced thresholds
- [ ] Coverage directory includes expected reporters (`text`, `html`, `lcov`)
- [ ] Provider package matches config (`v8` or `istanbul`)
- [ ] CI coverage command is aligned with local script behavior
- [ ] Coverage gains came from test additions or fixes, not broad source exclusions

## Additional resources

- [reference.md](reference.md) - quick config and troubleshooting reference
- [../nestjs-vitest-setup/SKILL.md](../nestjs-vitest-setup/SKILL.md) - full NestJS Vitest setup and migration
- Vitest coverage docs: https://vitest.dev/guide/coverage.html
