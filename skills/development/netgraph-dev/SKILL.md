---
name: netgraph-dev
description: >
  NetGraph contributor development workflow. Use when: setting up dev environment,
  running tests or lint, fixing CI failures, running performance benchmarks,
  troubleshooting venv issues, or asking about make targets.
  For running scenarios and interpreting results, use netgraph-dsl instead.
---

# NetGraph Development Workflow

For NetGraph contributors. For writing and running scenarios, see the `netgraph-dsl` skill.

## Development Setup

```bash
make dev  # Creates venv, installs deps, sets up pre-commit
```

Requires Python 3.11+.

## Code Iteration

| Command | Purpose |
|---------|---------|
| `make qt` | Quick tests (no coverage, excludes slow/benchmark) |
| `make check` | Full validation: auto-fix, schema, tests, lint, type check |
| `make test` | Full tests with coverage (includes slow/benchmark) |
| `make lint` | Verify formatting + lint + type check (no fixes) |
| `make format` | Auto-format only |
| `make validate` | Schema validation only |
| `make docs` | Regenerate API docs |

### Workflow

1. Make changes
2. `make qt` - fast feedback during development
3. `make check` - complete validation before commit
4. If API changed: `make docs` to regenerate API reference

## Performance Benchmarking

For algorithm complexity analysis and regression testing:

```bash
make perf  # Run all benchmark profiles with analysis and plots
```

Output in `dev/perf_results/` (JSON) and `dev/perf_plots/` (graphs).

### Perf CLI

```bash
# List available benchmark profiles
./venv/bin/python -m dev.perf.main show profile

# Show profile details
./venv/bin/python -m dev.perf.main show profile spf_complexity_clos2tier

# Run specific profile
./venv/bin/python -m dev.perf.main run --profile spf_complexity_grid2d

# List topology types
./venv/bin/python -m dev.perf.main show topology
```

Available profiles: `spf_complexity_*`, `max_flow_complexity_*` (Clos and Grid2D topologies).

## Running Commands

Use direct venv paths (avoids shell state issues):

```bash
./venv/bin/python -m pytest tests/dsl/
./venv/bin/ngraph inspect scenario.yaml
```

## Dev Tools

| Tool | Purpose |
|------|---------|
| `dev/perf/` | Performance benchmarking framework |
| `dev/generate_api_docs.py` | API doc generator (used by `make docs`) |
| `dev/run-checks.sh` | Quality checks (used by `make check`) |
| `dev/dev.md` | Quick development reference |

## Code Standards

### Python Practices
- Use modern type hints on public APIs; avoid `Any` where practical
- Provide clear docstrings for public APIs (arguments, return values, important errors)
- Use the project's logging facilities instead of `print()` in library code
- Prefer algorithmic improvements over micro-optimizations

### Testing
- Add or update tests for new behavior or bug fixes
- Keep tests readable and focused; use fixtures to avoid duplication
- When tests fail, fix the code rather than weakening tests (unless test is incorrect)

### Completion Checklist
A change is complete only after:
1. `make check` passes (auto-fixes, schema, lint, type check, tests)
2. Relevant tests cover the new behavior

## Pre-commit and CI

Pre-commit hooks run automatically on commit. To run manually:

```bash
make check  # Runs format, lint, type checks, tests
```

CI runs the same checks. If CI fails:
1. Pull latest changes
2. Run `make check` locally
3. Fix any failures
4. Push again

## Troubleshooting

### Venv Missing

```bash
make dev  # Recreates if missing
```

### Import Errors After Pull

```bash
./venv/bin/pip install -e '.[dev]'
```

### Pre-commit Failures

```bash
make format  # Auto-fix formatting
make check   # Verify all checks pass
```
