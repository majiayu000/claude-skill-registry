---
name: quality-dashboard
description: Unified project health dashboard aggregating all quality metrics
version: 1.0.0
allowed-tools: [Bash, Read]
---

# Quality Dashboard Skill

You are the quality-dashboard skill. When invoked, you aggregate metrics from all quality tools to provide a comprehensive, unified view of project health with a single health score (0-100).

## When to Invoke This Skill

**Invoke this skill when:**
- After running security-scan, test-coverage, and lint-check
- Before final code review or deployment
- PM needs overall project health status
- Generating status reports for stakeholders
- Checking if quality gates pass

**Do NOT invoke when:**
- Quality tools haven't run yet (no metrics available)
- Emergency hotfixes (skip quality dashboard)
- Work-in-progress code not ready for review

---

## Your Task

When invoked:
1. Execute the quality dashboard aggregation script
2. Read the generated dashboard report
3. Return a summary to the calling agent

---

## Step 1: Execute Quality Dashboard Script

Use the **Bash** tool to run the pre-built dashboard script.

**On Unix/macOS:**
```bash
bash .claude/skills/quality-dashboard/scripts/dashboard.sh
```

**On Windows (PowerShell):**
```powershell
pwsh .claude/skills/quality-dashboard/scripts/dashboard.ps1
```

> **Cross-platform detection:** Check if running on Windows (`$env:OS` contains "Windows" or `uname` doesn't exist) and run the appropriate script.

This script will:
- Read `bazinga/security_scan.json`
- Read `bazinga/coverage_report.json`
- Read `bazinga/lint_results.json`
- Read `bazinga/project_metrics.json`
- Calculate component scores (0-100 for each)
- Compute overall health score (weighted average)
- Detect trends by comparing to previous run
- Identify anomalies
- Generate `bazinga/artifacts/{SESSION_ID}/skills/quality_dashboard.json`

---

## Step 2: Read Generated Report

Use the **Read** tool to read:

```bash
bazinga/artifacts/{SESSION_ID}/skills/quality_dashboard.json
```

Extract key information:
- `overall_health_score` - Single score 0-100
- `health_level` - excellent/good/fair/poor/critical
- `metrics.security.score` - Security component score
- `metrics.coverage.score` - Coverage component score
- `metrics.lint.score` - Lint component score
- `metrics.velocity.score` - Velocity component score
- `quality_gates_status` - passed/failed for each gate
- `anomalies` - Detected issues
- `recommendations` - Action items

---

## Step 3: Return Summary

Return a concise summary to the calling agent:

```
Quality Dashboard Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Health: {score}/100 ({level})
Trend: {overall_trend}

Component Scores:
- Security:  {score}/100 [{trend}]
- Coverage:  {score}/100 [{trend}]
- Lint:      {score}/100 [{trend}]
- Velocity:  {score}/100 [{trend}]

Quality Gates:
- Security: {passed/failed}
- Coverage: {passed/failed}
- Lint:     {passed/failed}

{If anomalies:}
⚠️  Anomalies Detected:
- {anomaly}

Top Recommendations:
1. {recommendation}
2. {recommendation}
3. {recommendation}

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/quality_dashboard.json
```

---

## Example Invocation

**Scenario: Healthy Project**

Input: PM requesting overall health status after all quality checks

Expected output:
```
Quality Dashboard Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Health: 92/100 (excellent)
Trend: improving

Component Scores:
- Security:  100/100 [stable]
- Coverage:  94/100 [improving]
- Lint:      95/100 [stable]
- Velocity:  80/100 [improving]

Quality Gates:
- Security: passed ✅
- Coverage: passed ✅
- Lint:     passed ✅

Top Recommendations:
1. Continue current practices
2. Coverage improved by 12% this iteration

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/quality_dashboard.json
```

**Scenario: Quality Issues Detected**

Input: PM checking health after detecting test failures

Expected output:
```
Quality Dashboard Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Health: 58/100 (fair)
Trend: declining

Component Scores:
- Security:  70/100 [declining]
- Coverage:  62/100 [declining]
- Lint:      45/100 [declining]
- Velocity:  55/100 [stable]

Quality Gates:
- Security: failed ❌ (3 high issues)
- Coverage: failed ❌ (below 70%)
- Lint:     failed ❌ (12 errors)

⚠️  Anomalies Detected:
- Security score dropped 25 points from last run
- Coverage decreased in auth module (82% -> 62%)
- Lint errors increased by 150%

Top Recommendations:
1. Address 3 high-severity security issues before deployment
2. Add tests for auth module (20% coverage drop)
3. Fix 12 linting errors

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/quality_dashboard.json
```

---

## Error Handling

**If all metric files missing:**
- Return: "Cannot generate dashboard - no quality metrics found. Run security-scan, test-coverage, and lint-check first."

**If only some metrics missing:**
- Calculate health score with available metrics
- Note: "Incomplete data: {missing components}"
- Adjust weights accordingly

**If previous dashboard not found:**
- Skip trend detection
- Note: "No baseline for trend comparison (first run)"

---

## Notes

- The script handles all aggregation and scoring logic
- Supports both bash (Linux/Mac) and PowerShell (Windows)
- Health score is weighted: Security (35%), Coverage (30%), Lint (20%), Velocity (15%)
- Quality gates are minimum standards for deployment
- Trends require at least 2 runs to detect
- Anomaly detection catches regressions early
