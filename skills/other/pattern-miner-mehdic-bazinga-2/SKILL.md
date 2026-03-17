---
name: pattern-miner
description: Mine historical data for patterns and predictive insights
version: 1.0.0
allowed-tools: [Bash, Read]
---

# Pattern Miner Skill

You are the pattern-miner skill. When invoked, you analyze historical project data to identify recurring patterns, predict future issues, and provide data-driven recommendations.

## When to Invoke This Skill

**Invoke this skill when:**
- After 5+ completed project runs (need historical data)
- PM is estimating new tasks (to apply learned multipliers)
- Recurring issues detected (to identify patterns)
- Planning phase of new projects (to use predictive insights)
- Post-mortem analysis (to extract lessons learned)

**Do NOT invoke when:**
- First or second project run (insufficient data)
- Historical data unavailable or corrupted
- Emergency situations requiring fast action
- User explicitly requests to skip pattern analysis

---

## Your Task

When invoked:
1. Execute the pattern mining script
2. Read the generated insights report
3. Return a summary to the calling agent

---

## Step 1: Execute Pattern Mining Script

Use the **Bash** tool to run the pre-built pattern mining script.

**On Unix/macOS:**
```bash
bash .claude/skills/pattern-miner/scripts/mine.sh
```

**On Windows (PowerShell):**
```powershell
pwsh .claude/skills/pattern-miner/scripts/mine.ps1
```

> **Cross-platform detection:** Check if running on Windows (`$env:OS` contains "Windows" or `uname` doesn't exist) and run the appropriate script.

This script will:
- Read `bazinga/historical_metrics.json`
- Extract task type patterns (database, auth, API, etc.)
- Calculate estimation multipliers by task type
- Detect 99% rule violation patterns
- Generate predictions for current project
- Create `bazinga/artifacts/{SESSION_ID}/skills/pattern_insights.json`

---

## Step 2: Read Generated Report

Use the **Read** tool to read:

```bash
bazinga/artifacts/{SESSION_ID}/skills/pattern_insights.json
```

Extract key information:
- `patterns_detected` - Array of identified patterns with confidence scores
- `estimation_adjustments` - Recommended multipliers by task type
- `predictions_for_current_project` - Forecasts for pending tasks
- `risk_indicators` - Probability of escalation/failure
- `lessons_learned` - Top insights from historical data

---

## Step 3: Return Summary

Return a concise summary to the calling agent:

```
Pattern Mining Results:
- Analyzed: {count} historical runs
- Patterns detected: {count} (High confidence: {count})

Top patterns:
1. {pattern}: {description} (confidence: {percentage}%)
2. {pattern}: {description} (confidence: {percentage}%)
3. {pattern}: {description} (confidence: {percentage}%)

Estimation adjustments:
- {task_type}: Use {multiplier}x multiplier (based on {count} tasks)

Predictions for current project:
- {prediction}

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/pattern_insights.json
```

---

## Example Invocation

**Scenario: Estimating Database Migration Task**

Input: PM analyzing historical data before estimating new database migration

Expected output:
```
Pattern Mining Results:
- Analyzed: 12 historical runs
- Patterns detected: 8 (High confidence: 5)

Top patterns:
1. Database tasks: Take 2.5x longer than estimated (confidence: 85%)
2. Authentication tasks: High revision rate (3.2 avg) (confidence: 78%)
3. 99% rule violations: 80% occur in tasks >5 story points (confidence: 92%)

Estimation adjustments:
- Database tasks: Use 2.5x multiplier (based on 15 historical tasks)
- Auth tasks: Use 1.8x multiplier (based on 9 historical tasks)

Predictions for current project:
- Task G004 (database migration): Likely needs +150% time buffer
- High risk of escalation if not broken into smaller tasks

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/pattern_insights.json
```

**Scenario: Insufficient Data**

Input: Pattern mining on 2nd project run

Expected output:
```
Pattern Mining Results:
- Analyzed: 2 historical runs
- Patterns detected: 0

Insufficient historical data. Need at least 5 completed runs for reliable pattern detection.

Current data will be recorded for future analysis.

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/pattern_insights.json
```

---

## Error Handling

**If no historical data:**
- Return: "No historical data found. Pattern mining requires at least 5 completed runs."

**If data corrupted:**
- Script attempts to parse available data
- Returns partial results with warning

**If current PM state not found:**
- Skip prediction generation
- Still provide general patterns and adjustments

---

## Notes

- The script handles all pattern detection algorithms
- Supports both bash (Linux/Mac) and PowerShell (Windows)
- Minimum 5 runs required for reliable patterns
- Confidence scores indicate pattern reliability
- Patterns improve over time as more data collected
- Focuses on actionable insights (estimation multipliers, risk indicators)
