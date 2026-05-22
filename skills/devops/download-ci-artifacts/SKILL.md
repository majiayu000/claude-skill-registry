---
name: download-ci-artifacts
description: Download test results, screenshots, and logs from GitHub Actions
allowed-tools:
  - Bash
  - Read
  - Write
context: manual
---

# Download CI Artifacts Skill

Download test artifacts from GitHub Actions CI runs for analysis.

## When to Use

- After a CI run completes (pass or fail)
- To analyze test failures
- To review UI screenshots
- Before running `/analyze-test-results`

## Prerequisites

- GitHub CLI (`gh`) must be authenticated
- Must be in the repository directory

## Quick Run

```bash
# List recent workflow runs
gh run list --workflow=tests.yml --limit=5

# Download artifacts from most recent run
gh run download --name=test-report --dir=./ci-artifacts/
gh run download --name=ui-screenshots --dir=./ci-artifacts/screenshots/
gh run download --name=slicer-test-results --dir=./ci-artifacts/slicer/
gh run download --name=unit-test-results-py3.11 --dir=./ci-artifacts/unit/
```

## Download Specific Run

```bash
# Get run ID from list
RUN_ID=<run-id>

# Download all artifacts from that run
gh run download $RUN_ID --dir=./ci-artifacts/

# Or download specific artifact
gh run download $RUN_ID --name=ui-screenshots --dir=./ci-artifacts/screenshots/
```

## Artifact Contents

### test-report/
- `test-report.md` - Summary of all test results

### ui-screenshots/
- `*.png` - UI screenshots captured during tests
- `manifest.json` - Descriptions of each screenshot

### slicer-test-results/
- `slicer-output.log` - Full Slicer test output
- `screenshots/` - Screenshots from Slicer tests

### unit-test-results-py*/
- `unit-tests.xml` - JUnit XML test results

## After Download

Run these skills to analyze:

1. `/analyze-test-results` - Parse failures, suggest fixes
2. `/review-ui-screenshots` - Analyze UI for issues

## Example Workflow

```bash
# 1. Check latest run status
gh run list --workflow=tests.yml --limit=1

# 2. If failed, download artifacts
gh run download --dir=./ci-artifacts/

# 3. View test report
cat ci-artifacts/test-report/test-report.md

# 4. View screenshot manifest
cat ci-artifacts/ui-screenshots/manifest.json

# 5. Run analysis
# (Use /analyze-test-results skill)
```

## Cleanup

After analysis, remove artifacts:

```bash
rm -rf ./ci-artifacts/
```

## Troubleshooting

### "no artifacts found"
- Run may still be in progress
- Artifacts expire after 30 days
- Check run ID is correct

### Auth issues
```bash
gh auth status
gh auth login
```
