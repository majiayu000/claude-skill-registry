---
name: java-analyze-all
description: Run parallel analysis agents for quality, coverage, and standards compliance
user-invocable: true
allowed-tools: Read, Glob, Task, Skill
---

# Java Analyze All Skill

Orchestrates parallel analysis using multiple specialized agents for comprehensive code assessment.

## PARAMETERS

- **target** (required): Directory or file to analyze
- **module** (optional): Module scope

## WORKFLOW

### Step 1: Validate Target

Verify target exists:
```
Glob: pattern="{target}**/*.java"
```

If no files found → Report error and stop.

### Step 2: Launch Parallel Analysis Agents

Use Task tool to spawn agents in parallel:

```
Task:
  subagent_type: pm-dev-java:java-quality-agent
  description: Analyze code quality
  prompt: |
    Analyze code quality and standards compliance.
    target={target}
    module={module if specified}
    Return structured report.

Task:
  subagent_type: pm-dev-java:java-coverage-agent
  description: Analyze test coverage
  prompt: |
    Analyze test coverage and identify gaps.
    module={module if specified}
    threshold=80
    Return structured report.

Task:
  subagent_type: pm-dev-java:java-verify-agent
  description: Verify standards compliance
  prompt: |
    Verify standards compliance for target files.
    target={target}
    Return compliance report.
```

### Step 3: Aggregate Results

Collect results from all three agents:
- Quality report
- Coverage report
- Compliance report

### Step 4: Generate Summary

```
╔════════════════════════════════════════════════════════════╗
║       Java Analysis Summary                                 ║
╚════════════════════════════════════════════════════════════╝

Target: {target}
Module: {module or "all"}

QUALITY ANALYSIS:
- Compliance rate: {compliance_rate}%
- Violations: {violation_count}
- Standards checked: {standards_count}

COVERAGE ANALYSIS:
- Line coverage: {line}%
- Branch coverage: {branch}%
- Status: {meets_threshold | below_threshold}

STANDARDS VERIFICATION:
- Compliant: {compliant}
- Checklist: {passed}/{total} checks passed

RECOMMENDATIONS:
{aggregated recommendations from all agents}
```

## ERROR HANDLING

- If any agent fails → Include failure in summary, report partial results
- If all agents fail → Report aggregate failure
- This is a read-only command → Never modifies files

## USAGE EXAMPLES

```
# Analyze specific directory
/java-analyze-all target=src/main/java/auth/

# Analyze specific module
/java-analyze-all target=src/main/java/ module=auth-service

# Analyze entire project
/java-analyze-all target=src/main/java/
```

## CONTINUOUS IMPROVEMENT RULE

If you discover issues or improvements during execution, record them:

1. **Activate skill**: `Skill: plan-marshall:manage-lessons`
2. **Record lesson** with:
   - Component: `{type: "command", name: "java-analyze-all", bundle: "pm-dev-java"}`
   - Category: bug | improvement | pattern | anti-pattern
   - Summary and detail of the finding
