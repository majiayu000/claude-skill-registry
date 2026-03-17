---
name: pytest-dev
description: "World-class pytest engineer for Python: write/refactor tests, fix flakiness, design fixtures/markers, add coverage, speed up suites (collection/runtime), and optimize CI (GitHub Actions sharding, xdist parallelism, caching). Use when asked about pytest best practices, pytest 9.x features (subtests, strict mode, TOML config), pytest plugins (xdist/cov/asyncio/mock/httpx), or test performance/CI tuning."
---

# pytest-dev

Produce **high-signal, low-flake, fast** pytest suites and CI configs, with an
explicit focus on **measurable wins** (runtime, flake rate, coverage quality).

## Default workflow

1. **Classify the tests**
   - Unit: pure functions, no I/O (preferred)
   - Integration: DB/filesystem/multiprocess, slower but valuable
   - System/E2E: external services or UI, keep minimal and well-gated
2. **Identify boundaries**
   - Time/clock, randomness, network, filesystem, DB, env vars, global state
3. **Pick the lightest seam**
   - Prefer fakes/stubs over deep mocks; prefer dependency injection over
     patching internals
4. **Make it deterministic**
   - Control time, seeds, tmp dirs; avoid order dependencies
5. **Measure before optimizing**
   - Collection time vs runtime; quantify with `--durations` + a single baseline
6. **Harden for CI**
   - Enforce marker discipline, strict config, timeouts, isolation for parallel

## Quick commands

Use `python3` by default. If the project uses `uv`, prefer `uv run python`.

- Smallest repro: `python3 -m pytest path/to/test_file.py -q`
- First failure only: `python3 -m pytest -x --maxfail=1`
- Find slow tests: `python3 -m pytest --durations=20 --durations-min=0.5`
- Emit JUnit for CI: `python3 -m pytest --junitxml=reports/junit.xml`
- Parallelize on one machine (xdist): `python3 -m pytest -n auto --dist load`

## Optimization playbook (high ROI)

1. **Reduce collection scope** (`testpaths`, `norecursedirs`, avoid importing
   heavy modules at import time).
2. **Fix fixture scoping** (move expensive setup up-scope; ensure isolation).
3. **Eliminate sleeps and retries** (poll with timeouts; mock time).
4. **Parallelize safely** (xdist; isolate worker resources: tmp/db ports).
5. **Shard in CI** (split test files by historical timings; keep shards balanced).

## Use the bundled references

Read these when needed (keep SKILL.md lean):

- `references/pytest_core.md`: fixtures, markers, parametrization, strict mode,
  TOML config, subtests (pytest 9.x).
- `references/plugins.md`: plugin selection + usage patterns.
- `references/performance.md`: collection/runtime profiling and speedups.
- `references/ci_github_actions.md`: sharding, artifacts, caching, concurrency.

## Use the bundled scripts

- `scripts/junit_slowest.py`: report slowest tests/files from JUnit XML.
- `scripts/junit_split.py`: split test files into N shards using JUnit timings.
- `scripts/run_pytest_filelist.py`: run pytest for a list of test files.

## Quality gates

- Tests pass in a clean environment (no hidden dependency on local state).
- No network/time dependency without explicit control.
- Parallel-safe or explicitly marked/serialized.
- CI emits machine-readable artifacts when relevant (JUnit, coverage).
