---
name: pr-doctor
description: Diagnose and fix PR issues (build, reviews, Sonar)
user-invocable: true
allowed-tools: Skill, Read, Edit, Glob, Grep, Bash, Task
---

# PR Doctor Skill

Diagnose and fix pull request issues with parameterized checks.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `pr` | optional | Pull request number/URL (auto-detects current if not provided) |
| `checks` | optional | build\|reviews\|sonar\|all (default: all) |
| `auto-fix` | optional | Auto-apply fixes without prompting (default: false) |
| `wait` | optional | Wait for CI/Sonar to complete (default: true) |
| `handoff` | optional | Handoff structure from previous phase (JSON) |

## Prerequisites

Load required skills:
```
Skill: pm-workflow:workflow-integration-ci
Skill: pm-workflow:workflow-integration-sonar
```

## Workflow

### Step 0: Process Handoff Input

If `handoff` parameter provided: Parse JSON, extract artifacts/decisions/constraints.

### Step 1: Get PR Information

Auto-detect if not provided:
```bash
gh pr view --json number,title,state
```

Validate: PR must be numeric or valid GitHub URL.

### Step 2: Wait for Checks (If Requested)

If wait=true:
```bash
gh pr checks {pr} --json name,status,conclusion
```

Poll every 30 seconds. Timeout after 30 minutes with prompt: "[C]ontinue / [S]kip / [A]bort"

### Step 3: Diagnose Issues

Based on `checks` parameter:

**Build**: `gh pr checks` → BUILD_FAILURE if failed

**Reviews**: workflow-integration-ci (Fetch Comments) → REVIEW_COMMENTS ({count})

**Sonar**: workflow-integration-sonar (Fetch Issues) → SONAR_QUALITY ({count}/{severity})

### Step 4: Generate Diagnostic Report

```
═══════════════════════════════════════════════
PR Diagnostic Report: #{pr}
═══════════════════════════════════════════════

Build Status: {PASS|FAIL}
Review Comments: {count} unresolved
Sonar Issues: {count} ({severity breakdown})

Issues Found:
{per-category breakdown}

Recommended Actions:
{action list}
```

### Step 5: Fix Issues

Based on checks parameter:

**BUILD_FAILURE**: Run build fix workflow

**REVIEW_COMMENTS**: Use workflow-integration-ci (Handle Review). For each: triage → fix/explain/acknowledge.

**SONAR_QUALITY**: Use workflow-integration-sonar (Fix Issues). For each: triage → fix/suppress (with approval if not auto-fix).

### Step 6: Verify and Commit

After fixes: Verify build, commit via git workflow, push to PR branch.

### Step 7: Generate Summary

Display: `✓ {fixed} fixed, ⚠ {remaining} remaining, → {next_action}`

---

## Usage Examples

**Fix all PR issues:**
```
/pr-doctor pr=123
```

**Fix only Sonar issues:**
```
/pr-doctor pr=456 checks=sonar
```

**Auto-fix without prompts:**
```
/pr-doctor checks=all auto-fix
```

**Skip CI wait, fix current PR:**
```
/pr-doctor wait=false
```

## Architecture

Delegates to skills:
```
/pr-doctor (orchestrator)
  ├─> workflow-integration-ci skill (Fetch Comments, Handle Review)
  ├─> workflow-integration-sonar skill (Fetch Issues, Fix Issues)
  └─> workflow-integration-git skill (Commit workflow)
```

## Continuous Improvement

If you discover issues or improvements during execution, record them:

1. **Activate skill**: `Skill: plan-marshall:manage-lessons`
2. **Record lesson** with component: `{type: "skill", name: "pr-doctor", bundle: "pm-workflow"}`

## Related

| Skill | Purpose |
|-------|---------|
| `pm-workflow:workflow-integration-ci` | PR review comment handling |
| `pm-workflow:workflow-integration-sonar` | Sonar quality issue handling |
| `pm-workflow:workflow-integration-git` | Git commit workflow |
| `pm-workflow:task-implement` | Implement tasks before PR |
