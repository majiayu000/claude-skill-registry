---
name: workflow-fixer
description: CI/CD workflow failure diagnosis and automated repair skills
icon: 🔧
category: automation
tools:
  - git
  - gh
  - nix
  - github-actions
  - github-mcp
---

# Workflow Fixer Skills

## Overview

This skill provides expertise in diagnosing CI/CD workflow failures and implementing automated fixes. It combines log analysis, pattern recognition, and targeted repairs to quickly resolve pipeline issues.

## Activation Triggers

The workflow-fixer skill activates when:
- User mentions workflow/CI/build failures
- A GitHub Actions run has failed status
- Error patterns are detected in discussion
- Keywords match: `failed`, `broken`, `ci`, `workflow`, `pipeline`, `fix`

## Log Analysis

### Fetching Logs

```bash
# Via GitHub CLI
gh run list --status failure --limit 5
gh run view <run-id> --log-failed

# Via MCP Tools (preferred when available)
# Use github-mcp-server-actions_list with method: "list_workflow_runs"
# Use github-mcp-server-get_job_logs with run_id and failed_only: true
```

### Error Pattern Matching

| Pattern | Category | Common Fix |
|---------|----------|------------|
| `npm ERR! ERESOLVE` | Dependency | Update lockfile, use `--legacy-peer-deps` |
| `pip: No matching distribution` | Dependency | Pin version, check Python version |
| `nix: error: path .* does not exist` | Build | Check flake inputs, rebuild |
| `colcon build returned nonzero` | Build | Fix ROS2 package CMakeLists/setup.py |
| `FAILED.*test_` | Test | Fix test logic or mark as flaky |
| `Error: Process completed with exit code 137` | Resource | OOM - optimize or increase memory |
| `Error: The operation was canceled` | Resource | Timeout - increase `timeout-minutes` |
| `Error: Resource not accessible` | Permission | Check GITHUB_TOKEN permissions |

### Log Parsing Commands

```bash
# Extract error lines
grep -E "error|ERROR|Error|failed|FAILED|Failed" logs.txt | head -20

# Find stack traces
grep -A 10 "Traceback\|at .*\.ts:\|at .*\.js:" logs.txt

# Nix-specific errors
grep -E "error: |builder for .* failed" logs.txt
```

## Fix Strategies

### Dependency Issues

```bash
# NPM
rm -rf node_modules package-lock.json
npm install

# Pip/Python
pip install --upgrade pip
pip install -r requirements.txt --upgrade

# Nix
nix flake update
nix flake check --no-build

# Pixi
rm -f pixi.lock
pixi install
```

### Build Failures

```bash
# Clean rebuild
rm -rf build install log
colcon build --symlink-install

# Nix rebuild
nix develop --command echo "rebuilt"

# Check for missing dependencies
nix flake show
```

### Test Failures

```bash
# Run specific test with verbose output
pytest -xvs path/to/test.py::test_name

# Run with coverage to find issues
coverage run -m pytest path/to/test.py
coverage report -m

# Mark flaky test (last resort)
@pytest.mark.flaky(reruns=3)
def test_sometimes_fails():
    ...
```

### Environment Issues

```yaml
# Add missing environment variable
env:
  MY_VAR: ${{ secrets.MY_SECRET }}

# Fix permission issues
permissions:
  contents: read
  packages: write

# Add required setup step
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
```

## Workflow Debugging

### Step-by-step Investigation

1. **Identify the failed run**
   ```bash
   gh run list --status failure --limit 1
   ```

2. **Get failed job details**
   ```bash
   gh run view <run-id> --json jobs --jq '.jobs[] | select(.conclusion=="failure")'
   ```

3. **Extract relevant logs**
   ```bash
   gh run view <run-id> --log-failed 2>&1 | tail -100
   ```

4. **Identify error pattern**
   - Look for `Error:`, `error:`, `FAILED`, `Exception`
   - Check exit codes (137 = OOM, 143 = SIGTERM)

5. **Trace to source**
   - Find file and line number from error
   - Check recent commits that touched that file

6. **Implement minimal fix**
   - Change only what's necessary
   - Test locally if possible

7. **Verify fix**
   - Push and monitor new run
   - Check related jobs don't break

## Common Workflow Patterns

### Nix + Pixi (This Repository)

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: DeterminateSystems/nix-installer-action@v21
  - uses: DeterminateSystems/magic-nix-cache-action@v13
  - run: nix develop .#default --command pixi install
  - run: nix develop .#default --command pixi run <command>
```

### Common Fixes for This Repository

| Issue | Fix |
|-------|-----|
| `pixi.lock` mismatch | Remove `pixi.lock`, run `pixi install` |
| Flake evaluation error | Check `flake.nix`, run `nix flake check` |
| ROS2 build failure | Check `package.xml`, CMakeLists.txt |
| macOS CUDA error | Ensure CUDA shell only on Linux |
| Disk space | Add cleanup step before build |

## Integration with MCP

When GitHub MCP tools are available, use them for structured data:

```python
# List failed workflow runs
actions_list(
    method="list_workflow_runs",
    owner="FlexNetOS",
    repo="ripple-env",
    workflow_runs_filter={"status": "failure"}
)

# Get failed job logs
get_job_logs(
    owner="FlexNetOS",
    repo="ripple-env",
    run_id=12345,
    failed_only=True,
    return_content=True
)
```

## Related Skills

- [DevOps](../devops/SKILL.md) - CI/CD pipeline management
- [Nix Environment](../nix-environment/SKILL.md) - Nix-specific debugging
- [ROS2 Development](../ros2-development/SKILL.md) - ROS2 build issues

## Best Practices

1. **Always read logs first** - Don't guess at the problem
2. **Look for the first error** - Later errors are often cascading failures
3. **Check recent changes** - Most failures come from recent commits
4. **Test fixes locally** - When possible, verify before pushing
5. **Document non-obvious fixes** - Add comments explaining why
6. **Don't mask errors** - Fix root causes, not symptoms
7. **Consider flakiness** - Some failures are intermittent
