---
name: github-actions-debugging
description: Debug and fix GitHub Actions CI/CD failures
version: 1.1.0
tags: [ci-cd, github-actions, debugging]
owner: devops
status: active
---

# GitHub Actions Debugging Skill

## Overview

Diagnose and fix GitHub Actions workflow failures with systematic checks.

## Usage

```
/github-actions-debugging
```

## Identity
**Role**: DevOps Engineer
**Objective**: Analyze failed workflow runs and implement fixes to get the build Green.

## Diagnostic Playbook

### Step 1: Log Retrieval
**Action**: If run locally, replicate the failure. If remote, read the `gh run view` logs.
**Keywords to Search**:
- `Process completed with exit code 1`
- `npm ERR!`
- `Module not found`
- `Permission denied`

### Step 2: Context Analysis
- **Env**: Is the Runner Ubuntu-latest? Node version mismatch?
- **Secrets**: Are secrets missing? (Logs show `***` or empty values).
- **Paths**: Is the working directory correct? (`working-directory: ./frontend`).

### Step 3: Local Reproduction
Do not code blindly. Try to run the exact command locally.
- If `npm test` failed in CI -> Run `npm test` locally.
- If it works locally but fails in CI -> Check **Node Versions** or **Missing Artifacts** (unaccounted generated files).

## Common Fixes

### 1. Dependency Caching
**Issue**: Build slow or failing on install.
**Fix**:
```yaml
- uses: actions/setup-node@v3
  with:
    cache: 'npm'
```

### 2. Flaky Tests
**Issue**: Test fails randomly.
**Fix**: Mark as flaky, improve wait logic, or increase timeout.

### 3. Missing Perms
**Issue**: `403` on Push/Release.
**Fix**: `permissions: write-all` or specific scopes in YAML.

## Workflow
**Command**: `/debug-action <run-id>`
1.  Read logs.
2.  Hypothesize root cause.
3.  Propose YAML fix or Code fix.
4.  Commit with message `ci: fix workflow failure`.

## Outputs

- CI/CD failure analysis and remediation summary.

## Related Skills

- `/deploy` - Deployment workflow checks
