---
name: test-environment
description: Run all tests (unit, integration, E2E) in isolated containers separate from dev environment. Handles build, container startup, health checks, test execution, and cleanup. SINGLE SOURCE OF TRUTH for running tests in isolated containers.
---

# test-environment Skill

**Purpose**: Run all tests in isolated containers separate from dev environment

**When to Use**:
- Before running any test suite (E2E, unit, integration)
- When dev containers are busy with other agents
- To prevent test interference with development work
- For complete test isolation

**Single Source**: This skill is the ONLY way to run tests in isolated containers.

## Features

✅ **Complete Isolation**
- Separate test database (`witchcityrope_test`)
- Separate API and Web containers
- No interference with dev environment

✅ **Fresh Environment**
- Builds from current codebase
- Fresh database each run
- Clean state for every test

✅ **All Test Types**
- Unit tests (.NET)
- Integration tests (.NET)
- E2E tests (Playwright)
- Failed-only reruns

✅ **Automatic Cleanup**
- Removes containers after tests
- Removes images (prevents orphans)
- Prunes dangling images
- Optional keep flags for debugging

## Quick Start

```bash
# Run E2E tests (default)
bash .claude/skills/test-environment/execute.sh

# Run specific E2E test file
bash .claude/skills/test-environment/execute.sh --mode e2e --filter "admin-events-dashboard"

# Run all tests
bash .claude/skills/test-environment/execute.sh --mode all

# Keep containers for debugging
bash .claude/skills/test-environment/execute.sh --mode e2e --keep-containers
```

## Options

| Option | Description |
|--------|-------------|
| `--mode MODE` | Test mode: all, unit, integration, e2e, failed-only |
| `--filter PATTERN` | Filter E2E tests by filename pattern |
| `--coverage` | Generate coverage reports (not yet implemented) |
| `--keep-images` | Keep built images for faster reruns |
| `--keep-containers` | Keep containers running for debugging |
| `--skip-confirm` | Skip confirmation prompts (for automation) |

## Test Modes

### `--mode e2e` (default)
Runs Playwright E2E tests against test containers.

### `--mode all`
Runs all test types: unit + integration + e2e

### `--mode unit`
Runs .NET unit tests only

### `--mode integration`
Runs .NET integration tests only

### `--mode failed-only`
Reruns previously failed tests (not yet implemented)

## Integration with Agents

### test-executor
```markdown
BEFORE running ANY tests:
1. Use test-environment skill to start isolated containers
2. Skill handles build, start, health checks automatically
3. Run tests in isolation
```

### test-developer
```markdown
When writing/debugging tests:
1. Use test-environment skill with --keep-containers
2. Inspect running containers for debugging
3. Containers remain running until manual cleanup
```

## How It Works

1. **Build** - Creates fresh images from current codebase
2. **Start** - Launches test containers (API, Web, DB)
3. **Health Check** - Verifies compilation and database seeded
4. **Test** - Executes requested tests
5. **Results** - Saves to /test-results/
6. **Cleanup** - Removes containers/images (unless --keep-* flags)

## Files

```
.claude/skills/test-environment/
├── SKILL.md                     # This file
├── execute.sh                   # Main entry point
├── lib/
│   ├── build-containers.sh     # Build test images
│   ├── start-containers.sh     # Start test containers
│   ├── run-tests.sh            # Execute tests
│   ├── health-checks.sh        # Verify environment
│   ├── cleanup.sh              # Remove containers/images
│   └── failed-tests-tracker.sh # Track failures (TODO)
└── config/
    └── test-modes.json         # Test mode configurations
```

## Troubleshooting

**Build fails**: Check for compilation errors in source code

**Health check fails**: Review container logs with `docker logs`

**Tests fail**: Results saved to `/test-results/`

**Orphaned images**: Skill automatically prunes on cleanup

## Future Enhancements

- [ ] Failed test tracking and reruns
- [ ] Coverage report generation
- [ ] Performance baseline tracking
- [ ] Parallel test execution optimization

---

**Last Updated**: 2025-12-02
**Maintained by**: Test Team
**Related**: test-executor-lessons-learned.md, test-developer-lessons-learned.md
