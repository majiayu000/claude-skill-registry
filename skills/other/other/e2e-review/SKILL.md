---
name: e2e-review
description: "Reviews spec implementation with E2E visual browser validation via Playwright. Triggers on keywords: e2e review, visual review, spec review, browser validation"
project-agnostic: true
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# E2E Spec Review Command

Validate implementation against spec requirements using browser-based visual proof.

**Spec File:** $1
**Base URL:** $2 (default: `http://localhost:${DEFAULT_PORT:-5173}/`)

## Pre-Flight Checks

1. **Verify Spec File Exists**
   - Read spec file from `$1`
   - If not found: STOP with "Spec file not found: $1"

2. **Verify playwright-cli Installed**
   - Run: `playwright-cli --help`
   - If not available: STOP with "playwright-cli not installed. Run: npm install -g @playwright/cli@latest"

3. **Parse Spec Requirements**
   - Extract MLOs (Mid-Level Objectives) from Human Section
   - Extract acceptance criteria from Details section
   - Create validation checklist

## Execution

1. **Initialize Review Session**
   - Create output directory: `{PROJECT_ROOT}/outputs/review/<spec-id>/`
   - Record review start timestamp

2. **Open Application**
   - Navigate to base URL: `playwright-cli open <base_url>`
   - Take initial screenshot: `playwright-cli screenshot --output {PROJECT_ROOT}/outputs/review/<spec-id>/01_initial.png`
   - Verify application loads successfully

3. **Validate Each MLO**
   - For each Mid-Level Objective:
     a. Navigate to relevant UI section
     b. Take screenshot of current state
     c. Verify visual elements match expected
     d. Test interactions if applicable
     e. Document pass/fail with evidence

4. **Capture Visual Proof**
   - Screenshot key states during validation
   - Name format: `<NN>_<mlo>_<state>.png`
   - Example: `02_mlo1_button_visible.png`

5. **Generate Review Summary**

## Output Format

Generate markdown review summary:

```markdown
# Review: <spec-title>

**Spec:** $1
**Date:** <ISO date>
**Status:** PASSED | FAILED | PARTIAL

## MLO Validation

### MLO-1: <title>
- Status: PASSED/FAILED
- Evidence: ![screenshot]({PROJECT_ROOT}/outputs/review/<spec-id>/02_mlo1.png)
- Notes: <observations>

### MLO-2: <title>
...

## Screenshots

| # | Description | Path |
|---|-------------|------|
| 1 | Initial load | {PROJECT_ROOT}/outputs/review/<spec-id>/01_initial.png |
| 2 | MLO-1 validation | {PROJECT_ROOT}/outputs/review/<spec-id>/02_mlo1.png |

## Video Recording

Full session: {PROJECT_ROOT}/outputs/e2e/<timestamp>-review-<spec-id>.webm

## Summary

<brief summary of findings>
```

## Error Handling

- On navigation failure: capture error state, continue with next MLO
- On element not found: document as failure with screenshot
- On timeout: retry once, then mark as failed
- Always generate summary even if partial failure
