---
name: nestjs-vitest-setup
description: Install, migrate, or repair Vitest in NestJS backends with deterministic preflight checks, package-manager aware commands, Jest-to-Vitest conversion, and verification gates for unit, e2e, and coverage runs. Use when users ask to add Vitest, replace Jest in Nest projects, fix broken Nest tests under Vitest, standardize test scripts/config, or improve test reliability and runtime.
---

# NestJS Vitest

Use this workflow to set up, migrate, or repair NestJS tests with Vitest.

## Preflight checks (required)

1. Confirm Nest backend root by checking all required files exist:
- `package.json`
- `tsconfig.json`
- `src/main.ts`
- `src/app.module.ts`
2. Detect package manager from lockfile and keep command style consistent:
- `package-lock.json` -> `npm`
- `pnpm-lock.yaml` -> `pnpm`
- `yarn.lock` -> `yarn`
3. Confirm supported runtime:
- Prefer Node.js 20+.
4. Stop early if required files are missing and report exact missing path(s) before editing.

## Install and baseline configuration

1. Install required dev dependencies:

```bash
npm install --save-dev vitest @vitest/coverage-v8 vite-tsconfig-paths
```

2. Ensure `@nestjs/testing` and `supertest` are available for Nest unit/e2e tests.
3. Create or update `vitest.config.ts`:

```typescript
import { defineConfig } from 'vitest/config'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.spec.ts', 'test/**/*.e2e-spec.ts'],
    exclude: ['dist', 'node_modules'],
    setupFiles: ['test/vitest.setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      reportsDirectory: 'coverage',
    },
  },
})
```

4. Create or update `test/vitest.setup.ts`:

```typescript
import { afterEach, vi } from 'vitest'

afterEach(() => {
  vi.restoreAllMocks()
  vi.clearAllMocks()
})
```

5. Update `package.json` scripts:

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:cov": "vitest run --coverage",
    "test:e2e": "vitest run test/**/*.e2e-spec.ts"
  }
}
```

6. Keep `vite-tsconfig-paths` when the project uses TS path aliases. If no aliases are present, the plugin is optional.

## Migration from Jest

1. Convert Jest APIs in tests and helpers:

- `jest.fn` -> `vi.fn`
- `jest.spyOn` -> `vi.spyOn`
- `jest.mock` -> `vi.mock`
- `jest.clearAllMocks` -> `vi.clearAllMocks`
- `jest.restoreAllMocks` -> `vi.restoreAllMocks`
- `jest.useFakeTimers` -> `vi.useFakeTimers`
- `jest.useRealTimers` -> `vi.useRealTimers`
- `jest.setSystemTime` -> `vi.setSystemTime`

2. Remove Jest-only configuration once conversion is complete:
- `jest.config.*`
- `ts-jest` transforms
- scripts invoking `jest`
3. If Jest must remain temporarily (monorepo/shared tooling), document that as an intentional exception.

## NestJS test patterns

1. Unit tests for providers/services:
- Build a `TestingModule` via `Test.createTestingModule`.
- Mock dependencies with `useValue` and `vi.fn`.
- Assert behavior at the service boundary.
2. Controller tests:
- Validate delegation and response shaping.
- Stub service methods with `vi.fn` instead of real external calls.
3. e2e tests:
- Create and initialize `INestApplication` with `await app.init()`.
- Use `supertest` against `app.getHttpServer()`.
- Always run `await app.close()` in `afterAll`.

See concrete snippets in [examples.md](examples.md).

## Common pitfalls

- Path alias imports fail:
  - Add `vite-tsconfig-paths` and ensure aliases exist in `tsconfig.json`.
- Tests hang after completion:
  - Ensure `await app.close()` runs and fake timers are restored.
- Module mocks do not apply:
  - `vi.mock` is hoisted. Use patterns in [reference.md](reference.md) for factory and hoisted values.
- Decorator or reflection issues:
  - Keep `experimentalDecorators` and `emitDecoratorMetadata` consistent with the app tsconfig.

## Verification gates (required)

1. Run unit tests: `test`
2. Run e2e tests: `test:e2e`
3. Run coverage: `test:cov`
4. Confirm `coverage/` was generated.
5. Confirm Jest-only config/scripts were removed or intentionally retained with reason documented.
6. Confirm at least one unit and one e2e spec pass with Vitest.
7. If any gate fails, report exact failing command and stop before claiming success.

## Additional resources

- Advanced config and migration notes: [reference.md](reference.md)
- Nest-focused example tests: [examples.md](examples.md)
