---
name: test-features
description: Test a feature or flow and report findings; use when asked to validate UI or runtime behavior, optionally with a URL.
---

# Test Features

## Overview

Use this skill to validate feature behavior, review logs, and summarize issues.

## Inputs

- Feature description
- Optional URL to test

## Workflow

1. Identify the relevant test or runtime entry point.
2. Run unit or integration tests for the feature when available.
3. If a URL is provided and browser automation is available, exercise the flow and capture console output.
4. Check app logs for errors or warnings.
5. Capture evidence (errors, failing tests, screenshots if available).

## Output

- Findings grouped by severity with suggested fixes.
