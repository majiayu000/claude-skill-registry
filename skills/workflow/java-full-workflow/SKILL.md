---
name: java-full-workflow
description: Execute complete implement-test-verify workflow with coordinated agents
user-invocable: true
allowed-tools: Read, Edit, Write, Glob, Grep, Task, Skill
---

# Java Full Workflow Skill

Orchestrates complete feature implementation workflow: implement → test → fix → verify.

## PARAMETERS

- **description** (required): What to implement
- **target_class** (optional): Target class path
- **module** (optional): Target module
- **coverage_target** (optional): Coverage threshold (default: 80)

## WORKFLOW

### Step 1: Implement Feature

Launch implementation agent:

```
Task:
  subagent_type: pm-dev-java:java-implement-agent
  description: Implement feature
  prompt: |
    Implement Java feature with standards compliance.
    description={description}
    target_class={target_class if provided}
    module={module if provided}

    Return structured result with files created/modified.
```

**On failure:** Report implementation errors and stop.

### Step 2: Fix Build Errors (if needed)

If implementation produced build errors:

```
Task:
  subagent_type: pm-dev-java:java-fix-build-agent
  description: Fix compilation errors
  prompt: |
    Fix compilation errors from implementation.
    module={module if provided}
    max_iterations=3

    Return structured result.
```

### Step 3: Implement Tests

Launch test implementation agent:

```
Task:
  subagent_type: pm-dev-java:java-implement-tests-agent
  description: Implement tests
  prompt: |
    Implement unit tests for the new feature.
    target_class={target_class or implementation result}
    coverage_target={coverage_target}
    module={module if provided}

    Return structured result with coverage metrics.
```

### Step 4: Fix Test Failures (if needed)

If tests fail:

```
Task:
  subagent_type: pm-dev-java:java-fix-tests-agent
  description: Fix test failures
  prompt: |
    Fix failing unit tests.
    module={module if provided}
    max_iterations=2
    fix_production_code=false

    Return structured result.
```

### Step 5: Verify Standards Compliance

```
Task:
  subagent_type: pm-dev-java:java-verify-agent
  description: Verify compliance
  prompt: |
    Verify implementation meets all CUI standards.
    target={files from implementation}

    Return compliance report.
```

### Step 6: Final Build Verification

```
Skill: pm-dev-builder:builder-maven-rules
Workflow: Execute Maven Build
Parameters:
  goals: clean verify
  module: {module if specified}
  output_mode: errors
```

### Step 7: Generate Summary

```
╔════════════════════════════════════════════════════════════╗
║       Java Full Workflow Complete                           ║
╚════════════════════════════════════════════════════════════╝

Feature: {description}
Module: {module or "default"}

IMPLEMENTATION:
- Files created: {count}
- Files modified: {count}
- Build fixes: {fix_count}

TESTING:
- Tests generated: {test_count}
- Tests passed: {passed_count}
- Coverage: {line}% line, {branch}% branch

VERIFICATION:
- Standards compliance: {compliant}
- Checklist: {passed}/{total}

BUILD STATUS: {SUCCESS/FAILURE}

Files Changed:
{list of all files created/modified}
```

## ERROR HANDLING

- If implementation fails → Report and stop
- If build fails after 3 fix attempts → Report remaining errors
- If tests fail after 2 fix attempts → Report with recommendations
- If verification fails → Report non-compliant items

## USAGE EXAMPLES

```
# Implement new service
/java-full-workflow description="Add user authentication service"

# Implement in specific class
/java-full-workflow description="Add token validation" target_class=TokenValidator

# With module and coverage target
/java-full-workflow description="Add OAuth2 flow" module=auth-service coverage_target=90
```

## CONTINUOUS IMPROVEMENT RULE

If you discover issues or improvements during execution, record them:

1. **Activate skill**: `Skill: plan-marshall:manage-lessons`
2. **Record lesson** with:
   - Component: `{type: "command", name: "java-full-workflow", bundle: "pm-dev-java"}`
   - Category: bug | improvement | pattern | anti-pattern
   - Summary and detail of the finding
