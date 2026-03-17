---
name: build-run-local
description: "Run local builds with proper environment setup. Use when building code locally to verify changes before pushing."
category: ci
mcp_fallback: none
user-invocable: false
---

# Build and Run Local

Execute local builds with environment setup matching CI pipeline.

## When to Use

- Building code locally before pushing
- Testing individual components locally
- Verifying changes work before creating PR
- Running tests in local environment
- Debugging build issues in isolation

## Quick Reference

```bash
# Activate environment
eval "$(pixi shell-hook)"
pixi run mojo --version

# Build project
pixi run mojo build -I . shared/core/extensor.mojo

# Run tests
pixi run mojo test -I . tests/shared/core/

# Run specific test
pixi run mojo test -I . tests/shared/core/test_extensor.mojo

# Format code
pixi run mojo format .
```

## Workflow

1. **Activate environment**: Use pixi to setup environment
2. **Verify environment**: Check mojo version and dependencies
3. **Build locally**: Run mojo build with proper flags
4. **Run tests**: Execute test suite locally
5. **Check warnings**: Verify zero-warnings policy compliance
6. **Run pre-commit**: Validate formatting and linting
7. **Commit changes**: Only after local verification passes

## Build Configuration

**Environment Setup**:

- `pixi shell-hook` activates the pixi environment
- Sets MOJO_PATH and compiler flags
- Matches CI environment configuration

**Build Flags**:

- `-I .` includes current directory in path
- `-O` enables optimizations for release builds
- `--no-warn-unused` suppresses specific warnings (use sparingly)

**Test Flags**:

- `-I .` for module resolution
- `-v` for verbose output
- `-k "pattern"` to run specific tests

## Output Format

Report build results with:

1. **Status** - Success or failure
2. **Warnings** - Any compiler warnings found (must be zero)
3. **Test Results** - Passed/failed counts
4. **Build Time** - Performance metrics
5. **Issues** - Any errors encountered

## Error Handling

| Problem | Solution |
|---------|----------|
| Environment not found | Run `pixi shell-hook` to activate |
| Module not found | Verify `-I .` flag and correct paths |
| Permission denied | Check file permissions and ownership |
| Out of memory | Reduce parallel jobs or simplify test |
| Timeout | Check for infinite loops or long operations |

## References

- See pixi.toml for available tasks and configuration
- See CLAUDE.md for zero-warnings policy
- See mojo-test-runner skill for advanced testing
