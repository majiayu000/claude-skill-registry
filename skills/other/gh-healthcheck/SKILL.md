---
name: gh-healthcheck
description: Run health check on GitHub Actions workflow with root cause analysis and recommendations. Use for quick CI status overview and pattern analysis.
argument-hint: [--workflow build.yml] [--run-id <id>] [--detail low|medium|high]
context: fork
---

Analyze GitHub Actions workflow health and provide a comprehensive diagnostic report.

Arguments: $ARGUMENTS

Run the health check tool:
```bash
uv run ci/tools/gh/gh_healthcheck.py $ARGUMENTS
```

## Features

**Root Cause Analysis**: Groups errors by category (Missing Headers, Linker Errors, Platform Issues, etc.)

**Detail Levels**:
- `low`: Summary only, no log fetching (fast)
- `medium`: Fetches logs and categorizes errors (default)
- `high`: Full error details with context

## Usage Examples

- Check latest: `uv run ci/tools/gh/gh_healthcheck.py`
- Specific run: `uv run ci/tools/gh/gh_healthcheck.py --run-id 18399875461`
- High detail: `uv run ci/tools/gh/gh_healthcheck.py --detail high`

## Comparison with /gh-debug

- **gh-healthcheck**: Overview and analysis of entire workflow
- **gh-debug**: Deep dive into specific run with full error context
