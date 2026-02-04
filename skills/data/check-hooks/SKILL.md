---
name: check-hooks
description: Comprehensive health check for hooks - detects import errors, runtime failures, performance issues, and provides auto-fix suggestions
---

# Check Hook Health

**Command**: `/sw:check-hooks`

Runs comprehensive health check on all hooks in the project.
Detects import errors, runtime failures, performance issues, and provides auto-fix suggestions.

## Usage

```bash
# Check all hooks
/sw:check-hooks

# Check and auto-fix issues
/sw:check-hooks --fix

# Check only critical hooks
/sw:check-hooks --critical

# Verbose output with details
/sw:check-hooks --verbose

# Check specific hook
/sw:check-hooks update-ac-status

# Generate markdown report
/sw:check-hooks --format markdown --output report.md

# Check reflect hook health (self-improving AI)
/sw:check-hooks --reflect

# Check reflect with verbose details
/sw:check-hooks --reflect --verbose
```

## Options

- `--fix` - Automatically repair fixable issues (missing .js extensions, etc.)
- `--critical` - Check only critical hooks (post-task-completion, user-prompt-submit)
- `--verbose` - Show detailed error messages and stack traces
- `--format <format>` - Output format: console (default), markdown, json, junit
- `--output <file>` - Write report to file
- `--timeout <ms>` - Hook execution timeout (default: 5000ms)
- `--fail-on-warnings` - Exit with error code if warnings detected
- `--reflect` - Check reflect hook health (stop-reflect.sh, jq, memory dirs)
- `--include-cache` - Also check plugin cache health

## What It Checks

### Import Errors (ERR_MODULE_NOT_FOUND)
- Missing .js extensions in ES module imports
- Incorrect import paths
- Missing dependencies

### Runtime Errors
- Static vs instance method mismatches
- Syntax errors
- JSON parse errors

### Performance Issues
- Hooks exceeding expected execution time
- Slow file I/O operations

### Best Practices
- Deprecated API usage
- Security vulnerabilities

## Auto-Fix Capabilities

The `--fix` flag can automatically repair:

1. **Missing .js Extensions**
   ```typescript
   // Before:
   import { ACStatusManager } from '../../../../src/core/increment/ac-status-manager';

   // After:
   import { ACStatusManager } from '../../../../src/core/increment/ac-status-manager.js';
   ```

2. **Import Path Corrections** (high confidence only)

## Output Formats

### Console (Default)
Colorized output for terminal viewing:

```
🏥 Hook Health Check
═══════════════════════════════════════════════════════════

✅ All hooks healthy (8/8 passed)

Hooks Checked:
  ✅ update-ac-status (42ms)
  ✅ auto-transition (38ms)
  ✅ sync-living-docs (156ms)
  ...

Summary:
  Total Hooks: 8
  ✅ Passed: 8
  ⏱️  Total Time: 625ms
```

### Markdown
Detailed report for documentation:

```markdown
# 🏥 Hook Health Check Report

**Generated**: 2025-11-16 14:00:00
**Overall Health**: 🟢 HEALTHY

## Summary
- **Total Hooks**: 8
- **Passed**: ✅ 8
- **Failed**: ❌ 0
```

### JSON
Machine-readable format for CI/CD:

```json
{
  "timestamp": "2025-11-16T14:00:00Z",
  "totalHooks": 8,
  "passedHooks": 8,
  "failedHooks": 0,
  "overallHealth": "healthy"
}
```

### JUnit XML
For CI/CD test reporting:

```xml
<testsuite name="Hook Health Check" tests="8" failures="0">
  <testcase name="update-ac-status" classname="specweave" time="0.042"/>
</testsuite>
```

## Exit Codes

- `0` - All hooks healthy
- `1` - Hook failures detected
- `2` - Critical hook failures (blocks workflow)

## Examples

### Pre-Build Health Check
```bash
npm run check:hooks
```

### CI/CD Integration
```yaml
# .github/workflows/test.yml
- name: Check Hook Health
  run: npm run check:hooks -- --format junit --output junit.xml

- name: Publish Test Results
  uses: EnricoMi/publish-unit-test-result-action@v2
  with:
    files: junit.xml
```

### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

npm run check:hooks --critical
if [ $? -ne 0 ]; then
  echo "❌ Critical hooks failing - commit blocked"
  exit 1
fi
```

## Troubleshooting

### "Hook execution timeout"
Increase timeout: `/sw:check-hooks --timeout 10000`

### "Cannot find module"
Run with auto-fix: `/sw:check-hooks --fix`

### "Permission denied"
Check hook file permissions: `chmod +x plugins/*/hooks/*.sh`

## Quick Health Dashboard

For a quick visual dashboard of hook health, run:

```bash
bash plugins/specweave/scripts/hook-health.sh
```

Or use specific views:
```bash
bash plugins/specweave/scripts/hook-health.sh --status   # Quick status
bash plugins/specweave/scripts/hook-health.sh --metrics  # Detailed metrics
bash plugins/specweave/scripts/hook-health.sh --reset    # Reset circuit breakers
bash plugins/specweave/scripts/hook-health.sh --clean    # Clean stale state
```

## Concurrency System

The hook system uses proper concurrency primitives:

### Semaphore
- Limits concurrent hook execution (default: 15)
- Graceful degradation when slots unavailable
- Automatic cleanup of stale locks

### Circuit Breaker
- Per-hook circuit breakers with 3 states:
  - CLOSED: Normal operation
  - OPEN: Too many failures, fail fast
  - HALF_OPEN: Testing recovery

### Metrics
- Success/failure/timeout tracking
- Latency percentiles (p50, p95, p99)
- Health score calculation

### Configuration
Environment variables:
- `HOOK_MAX_CONCURRENT` - Max concurrent hooks (default: 15)
- `HOOK_TIMEOUT` - Hook execution timeout in seconds (default: 5)
- `HOOK_DEBUG` - Enable debug logging (1 = enabled)

## See Also

- Hook Health Check Architecture: `.specweave/increments/0037-project-specific-tasks/architecture/HOOK-HEALTH-CHECK-ARCHITECTURE.md`
- Hook Development Guide: `.specweave/docs/public/guides/hook-development.md`
- Concurrency Libraries: `plugins/specweave/hooks/lib/`
