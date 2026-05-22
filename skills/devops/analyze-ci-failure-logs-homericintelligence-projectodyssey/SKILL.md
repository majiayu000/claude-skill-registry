---
name: analyze-ci-failure-logs
description: "Parse and analyze CI failure logs to identify root causes and error patterns. Use when CI builds fail to understand what broke."
category: ci
user-invocable: false
---

# Analyze CI Failure Logs

Parse CI failure logs to identify root causes and categorize errors.

## When to Use

- CI pipeline fails and you need to understand why
- Analyzing test failure logs from GitHub Actions
- Extracting error messages from build artifacts
- Identifying patterns in recurring failures
- Determining if failure is environmental or code-related

## Quick Reference

```bash
# Download CI logs from artifact
gh run download <run-id> -D /tmp/ci-logs

# Extract from workflow run
gh run view <run-id> --log > /tmp/ci-output.log

# Grep for error patterns
grep -i "error\|failed\|panic\|exception" /tmp/ci-output.log

# Get summary of failures
tail -100 /tmp/ci-output.log | grep -A 5 "FAILED\|ERROR"
```

## Workflow

1. **Collect logs**: Download CI artifacts or view workflow run output
2. **Extract errors**: Filter for error patterns (FAILED, ERROR, PANIC, exception)
3. **Identify type**: Categorize error (compilation, test, timeout, dependency, etc.)
4. **Find root cause**: Trace back to source (line numbers, stack traces)
5. **Check context**: Compare with recent changes in PR
6. **Create summary**: Report findings with actionable next steps

## Log Analysis Patterns

**Compilation Errors**:

- Look for: `error:`, `undefined`, `type mismatch`
- Check: Mojo syntax, imports, type annotations

**Test Failures**:

- Look for: `FAILED`, `AssertionError`, `ValueError`
- Check: Test logic, expected vs actual values

**Timeout Issues**:

- Look for: `timeout`, `timed out`, `hanging`
- Check: Long-running loops, infinite recursion

**Dependency Issues**:

- Look for: `not found`, `import failed`, `version conflict`
- Check: Package versions, environment setup

**Environmental Issues**:

- Look for: `permission denied`, `out of memory`, `disk full`
- Check: Resource limits, configuration

## Output Format

Provide analysis with:

1. **Error Category** - Type of failure (compilation, test, timeout, dependency, environmental)
2. **Root Cause** - What line/code caused the failure
3. **Context** - Full error message and stack trace
4. **Related Changes** - Which PR changes might have caused it
5. **Remediation** - Recommended fix or investigation steps

## Error Handling

| Problem | Solution |
|---------|----------|
| Logs not accessible | Use `gh run view` to check permissions |
| Truncated logs | Download full artifact instead of view |
| Large log files | Use grep to extract relevant sections |
| Encoded artifacts | Unzip and decompress before analysis |

## References

- GitHub Actions documentation: workflow logs and artifacts
- CLAUDE.md: zero-warnings policy and standards
- See fix-ci-failures skill for implementing fixes
