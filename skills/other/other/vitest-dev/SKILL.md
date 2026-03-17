---
name: vitest-dev
metadata:
  version: 0.1.0
description: World-class Vitest QA/test engineer for TypeScript + Next.js (local + CI performance focused)
---

# vitest-dev

A Claude Code skill for producing **high-signal, low-flake, fast** Vitest suites (TypeScript + Next.js 16) and for shaping Vitest configuration for optimal **local DX** and **CI throughput**.

## Core outcomes

1. **Correctness first**: tests encode business behavior (not implementation details).
2. **Deterministic**: no network, no clocks, no global leakage, no order dependencies.
3. **Fast**:
   - fast feedback locally (watch mode + smart filtering)
   - scalable CI (parallel workers + sharding + cache + machine-readable reports)
4. **Actionable failures**: failures localize root cause quickly.

## Default operating procedure

When asked to add or improve tests:

1. **Map the unit under test**
   - Identify public API / observable behavior
   - Identify boundaries: I/O, time, randomness, network, database, filesystem, env, global state
2. **Choose the lightest test that gives confidence**
   - Pure unit test (no framework/runtime) → preferred
   - Component test in `jsdom` (React) when DOM behavior is essential
   - Integration test in Node when multiple modules must cooperate
   - Browser Mode (real browser) only when DOM fidelity matters (layout/visuals, real events)
3. **Design a minimal test matrix**
   - happy path(s)
   - boundary conditions
   - error paths
   - key invariants (idempotency, caching semantics, auth gates, etc.)
4. **Implement tests**
   - arrange/act/assert clarity
   - isolate side effects and restore mocks
   - prefer stable assertions (`toHaveTextContent`, role-based queries, etc.)
5. **Run locally and fix**
   - run smallest scope first (single file / name filtering)
6. **Harden**
   - remove flakiness vectors (timers, concurrency, random, hidden network)
   - ensure tests pass in “run mode” (CI-like)
7. **Optimize**
   - reduce expensive setup per test file
   - tune Vitest config: pool, isolate, workers, cache, deps optimization, sharding
8. **Deliver**
   - include config + scripts changes needed for local + CI
   - include README notes if non-obvious

## Naming and structure conventions

- Place tests next to code for discoverability:
  - `src/foo.ts` → `src/foo.test.ts`
  - `src/components/Button.tsx` → `src/components/Button.test.tsx`
- Use `__tests__` for framework-driven routes when colocation is awkward (Next example uses this convention).
- Prefer `describe('<unit>')` with focused `it('does X when Y')`.

## Vitest execution modes and what to target

- Local development: `vitest` (watch mode by default when TTY is detected).
- CI: `vitest run` (forces a single run and is non-interactive).

From the Vitest CLI guide, Vitest defaults to watch mode when `process.stdout.isTTY` is true and falls back to run mode otherwise, while `vitest run` always runs once. (See: https://vitest.dev/guide/cli)

## Configuration baseline

### Recommended “default” config goals

- Use TypeScript path aliases (monorepos and Next apps frequently need this).
- Choose an environment per project:
  - `node` for backend/unit tests
  - `jsdom` (or `happy-dom`) for React component tests
- Keep setup lightweight.

### Pool choice (speed vs compatibility)

Vitest runs test files using a **pool** (`forks`, `threads`, `vmThreads`, `vmForks`). By default (Vitest v4 docs) it uses **`forks`**. `threads` can be faster but may break libraries that use native bindings; `forks` uses `child_process` and supports process APIs like `process.chdir()`. (See: https://vitest.dev/config/pool)

**Rule of thumb**:
- Prefer `threads` for “pure JS/TS” unit tests.
- Use `forks` if you use:
  - native addons (e.g. Prisma, bcrypt, canvas)
  - `process.*` APIs that are not available in threads
- Avoid VM pools unless you have measured wins and understand the tradeoffs.

### Isolation (speed vs global leakage)

`test.isolate` defaults to `true`. Disabling can improve performance when tests don’t rely on side effects (often true for Node-only units). (See: https://vitest.dev/config/isolate)

**Rule of thumb**:
- Keep `isolate: true` for frontend/component tests (`jsdom`) and any suite that touches global state.
- Consider `isolate: false` for Node-only pure units *after* you have strong isolation discipline.

### File-level and test-level parallelism

- `test.fileParallelism` default is `true`. Setting it to `false` forces single-worker execution by overriding `maxWorkers` to 1. (See: https://vitest.dev/config/fileparallelism)
- `test.maxWorkers` defaults to:
  - all available parallelism when watch is disabled
  - half when watch is enabled
  It also accepts a percentage string like `"50%"`. (See: https://vitest.dev/config/maxworkers)
- `test.maxConcurrency` controls how many `test.concurrent` tests can run simultaneously, default `5`. (See: https://vitest.dev/config/maxconcurrency)

### Cache (CI win)

Vitest caching is enabled by default and uses `node_modules/.vite/vitest`. (See: https://vitest.dev/config/cache)

For CI, persist this directory between runs (per branch key) for significant speedups.

## Next.js 16 integration defaults

Use Next’s recommended baseline:
- Install (TypeScript): `vitest`, `@vitejs/plugin-react`, `jsdom`, `@testing-library/react`, `@testing-library/dom`, `vite-tsconfig-paths`.
- Configure `test.environment = 'jsdom'` with the React + tsconfigPaths plugins.

(See: https://nextjs.org/docs/app/guides/testing/vitest)

**Important limitation noted by Next.js**: Vitest currently does not support `async` Server Components; for `async` components, use E2E tests instead. (See the same Next.js guide above.)

## Mocking & test doubles discipline

### Preferred hierarchy (from most realistic to most isolated)

1. **Real pure functions** (no mocking)
2. **In-memory fakes** (e.g., fake repo with a Map)
3. **Contract-driven stubs** (minimal, stable)
4. **Spies** (`vi.spyOn`) for verifying interactions
5. **Module mocks** (`vi.mock`) only when necessary

### Mock reset policy

- Default: clean up per test file:
  - `afterEach(() => vi.restoreAllMocks())`
- If you use global stubs (env/globals), clean them up in `afterEach` too.

### Timers

Use fake timers to avoid slow sleeps. Vitest’s docs show using `vi.useFakeTimers()` with `vi.runAllTimers()` / `vi.advanceTimersByTime()` to speed time-based code. (See: https://vitest.dev/guide/mocking/timers)

Advanced note: if you configure `fakeTimers.toFake` to include `nextTick`, it is **not supported** with `--pool=forks` because Node’s `child_process` uses `process.nextTick` internally and can hang; it is supported with `--pool=threads`. (See: https://vitest.dev/config/faketimers)

## CI reporting and sharding

### Reporters

- Use `junit` to export JUnit XML (for most CI systems). (See: https://vitest.dev/guide/reporters)
- In GitHub Actions, Vitest automatically adds `github-actions` reporter when `GITHUB_ACTIONS === 'true'` if default reporters are used; if you override reporters, add it explicitly. (See: https://vitest.dev/guide/reporters)

### Sharding (multi-machine parallel CI)

Use `--shard` with the `blob` reporter and merge at the end. Vitest recommends the blob reporter for sharded runs and provides `--merge-reports`. (See: https://vitest.dev/guide/reporters)

## Using test projects for multi-environment suites

Use `test.projects` to run multiple configurations in one process (monorepos or mixed environments). Vitest notes the older “workspace” name is deprecated in favor of `projects`. (See: https://vitest.dev/guide/projects)

Patterns:
- project A: `environment: 'node'`, `pool: 'threads'`, `isolate: false`
- project B: `environment: 'jsdom'`, `isolate: true`

## Deliverables this skill produces

When invoked, this skill can generate or update:

- Vitest config(s): `vitest.config.ts`, multi-project configs, CI overrides
- Test setup: `setupTests.ts`, test utils, mocks
- Tests: unit, integration, React component tests, type tests
- CI scripts: sharding + merging reports, coverage, flake detection
- Performance tuning recommendations with measurable steps

## Output quality gates

Before finalizing, ensure:

- No test uses real timers (`setTimeout` waits), real network, or real clock time without explicit control.
- All mocks/stubs are restored.
- Tests pass with:
  - `vitest`
  - `vitest run`
- On CI, tests emit machine-readable artifacts (JUnit, JSON, blob merge) if requested.
- Coverage settings match team goals and don’t create “coverage theater”.

## Where to look for authoritative details (official docs)

- Config reference: https://vitest.dev/config
- CLI: https://vitest.dev/guide/cli
- Improving performance: https://vitest.dev/guide/improving-performance
- Profiling performance: https://vitest.dev/guide/profiling-test-performance
- Parallelism: https://vitest.dev/guide/parallelism
- Mocking: https://vitest.dev/guide/mocking
- Reporters: https://vitest.dev/guide/reporters
- Coverage: https://vitest.dev/guide/coverage
- Next.js 16 + Vitest: https://nextjs.org/docs/app/guides/testing/vitest
