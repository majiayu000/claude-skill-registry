---
description: Check CI build status, PR checks, and pull request build results
triggers:
  - check builds
  - check ci
  - build status
  - are builds passing
  - check build status
  - ci status
  - are tests passing
  - check pr builds
  - check pull request builds
  - pr build status
---

# Check Build Status

Check GitHub Actions CI build status for the current branch, pull requests, or recent workflow runs.

## Quick Status Check

```bash
# Check status for current branch's PR
gh pr checks

# Check specific PR
gh pr checks <PR_NUMBER>

# List recent workflow runs
gh run list --limit 5
```

## Detailed Build Information

### Current PR Status

```bash
# Full details on all checks for current branch
gh pr checks

# View specific PR with number
gh pr view <PR_NUMBER>
gh pr checks <PR_NUMBER>
```

**Output shows:**
- ✓ Passing checks (green)
- ✗ Failed checks (red)
- ○ Pending/running checks (yellow)

### Recent Workflow Runs

```bash
# List last 10 workflow runs
gh run list --limit 10

# Filter by workflow name
gh run list --workflow="Build Firmware"

# Filter by status
gh run list --status=failure
gh run list --status=success
```

### View Build Logs

```bash
# View summary of a specific run
gh run view <RUN_ID>

# View full logs
gh run view <RUN_ID> --log

# View logs for specific job
gh run view <RUN_ID> --log --job=<JOB_ID>
```

## Common Build Failure Scenarios

### Firmware Build Failures

**Typical causes:**
- Compilation errors in C code
- Missing header files
- Target-specific issues (specific board configs)
- Linker errors (flash/RAM overflow)

**How to investigate:**
```bash
# Check build logs
gh run view <RUN_ID> --log | grep -i error

# Look for specific target failures
gh run view <RUN_ID> --log | grep "FAILED"

# Reproduce locally
cd inav
./build.sh SITL  # or specific target
```

### Configurator Build Failures

**Typical causes:**
- JavaScript syntax errors
- ESM/CommonJS import issues
- Missing dependencies
- Linter/format errors

**How to investigate:**
```bash
# Check build logs
gh run view <RUN_ID> --log | grep -i error

# Reproduce locally
cd inav-configurator
npm install
NODE_ENV=development npm start
```

### Test Failures

**How to investigate:**
```bash
# Look for test failures in logs
gh run view <RUN_ID> --log | grep -i "test.*fail"

# Run tests locally
cd inav-configurator
npm test  # if test suite exists
```

## Parsing Build Failures

When a build fails, look for these patterns in logs:

### C Compilation Errors
```
error: 'variableName' undeclared
error: conflicting types for 'functionName'
error: implicit declaration of function
region 'FLASH' overflowed by XXX bytes
```

### JavaScript Errors
```
SyntaxError: Unexpected token
ReferenceError: X is not defined
TypeError: Cannot read property
Error: Cannot find module
```

### Linker Errors
```
undefined reference to 'functionName'
region 'FLASH' overflowed
multiple definition of 'symbolName'
```

## Build Status Summary

### Quick Visual Summary

```bash
# Create a simple status report
echo "=== Current Build Status ==="
gh pr checks | grep -E "✓|✗|○"
echo ""
echo "=== Recent Failures ==="
gh run list --status=failure --limit 5
```

### Monitoring Specific Workflows

For INAV projects, common workflows include:
- Firmware builds (all targets)
- SITL builds
- Configurator builds
- Linter/format checks

```bash
# Check specific workflow status
gh run list --workflow="CI" --limit 5
```

## Fixing Build Failures

### General Process

1. **Identify the failure:**
   ```bash
   gh pr checks
   gh run view <RUN_ID> --log
   ```

2. **Reproduce locally:**
   - Firmware: `cd inav && ./build.sh SITL`
   - Configurator: `cd inav-configurator && NODE_ENV=development npm start`

3. **Fix the issue:**
   - Edit code to resolve the error
   - Test locally to verify fix

4. **Commit and push:**
   ```bash
   git add <files>
   git commit -m "Fix: <describe the fix>"
   git push
   ```

5. **Verify fix:**
   ```bash
   # Wait for CI to run, then check
   gh run list --limit 1
   gh run view <NEW_RUN_ID>
   ```

## Re-running Failed Builds

Sometimes builds fail due to transient issues (network, runner problems):

```bash
# Re-run a failed workflow
gh run rerun <RUN_ID>

# Re-run only failed jobs
gh run rerun <RUN_ID> --failed
```

## Example Investigations

### Investigating PR Build Failure

```bash
# Scenario: PR #2434 has failing builds
gh pr checks 2434
gh pr view 2434

# Get the failed run ID
gh run list --limit 5

# View the failure details
gh run view <RUN_ID> --log | grep -i error

# Check what changed in the PR
gh pr diff 2434

# Reproduce locally
cd inav
./build.sh SITL
```

### Monitoring All Builds

```bash
# Quick status of everything
echo "PR Checks:"
gh pr checks
echo ""
echo "Recent Runs:"
gh run list --limit 3
echo ""
echo "Recent Failures:"
gh run list --status=failure --limit 3
```

## Resources

- **GitHub CLI docs:** `gh run --help`, `gh pr --help`
- **Build failure projects:** See `claude/projects/investigate-pr*/` for examples
- **CI configuration:** `.github/workflows/` in each repository

---

## Related Skills

- **pr-review** - Review PRs (uses check-builds to verify CI status)
- **create-pr** - Create PRs (use check-builds after PR creation)
- **git-workflow** - Git operations (often precedes build checks)
- **finish-task** - Complete tasks (verify builds pass before finishing)
