---
name: velocity-tracker
description: Track development velocity, cycle times, and identify trends for PM decision-making
version: 1.0.0
allowed-tools: [Bash, Read]
---

# Velocity Tracker Skill

You are the velocity-tracker skill. When invoked, you analyze historical project data to provide quantitative metrics for PM decision-making.

## When to Invoke This Skill

**Invoke this skill when:**
- After completing each task group (to track cycle time)
- Before spawning new developers (to check velocity capacity)
- When a task appears stuck (to detect 99% rule violations)
- Before sending BAZINGA (to record final metrics for learning)
- Planning next iteration (to use historical data)

**Do NOT invoke when:**
- First run with no completed tasks yet
- Emergency bug fixes (skip metrics to save time)
- User explicitly requests fast mode
- No PM state file exists yet

---

## Your Task

When invoked:
1. Execute the velocity tracking script
2. Read the generated metrics report
3. Return a summary to the calling agent

---

## Step 1: Execute Velocity Tracking Script

Use the **Bash** tool to run the pre-built tracking script.

**On Unix/macOS:**
```bash
bash .claude/skills/velocity-tracker/scripts/track.sh
```

**On Windows (PowerShell):**
```powershell
pwsh .claude/skills/velocity-tracker/scripts/track.ps1
```

> **Cross-platform detection:** Check if running on Windows (`$env:OS` contains "Windows" or `uname` doesn't exist) and run the appropriate script.

This script will:
- Read PM state from database (`bazinga/bazinga.db`)
- Calculate current velocity and cycle times
- Compare against historical metrics
- Detect trends (improving/stable/declining)
- Identify 99% rule violations
- Generate `bazinga/artifacts/{SESSION_ID}/skills/project_metrics.json`
- Update `bazinga/artifacts/{SESSION_ID}/skills/historical_metrics.json`

---

## Step 2: Read Generated Report

Use the **Read** tool to read the generated report:

```bash
bazinga/artifacts/{SESSION_ID}/skills/project_metrics.json
```

Extract key information:
- `current_run.velocity` - Story points completed
- `current_run.percent_complete` - Progress percentage
- `trends.velocity` - Velocity trend
- `warnings` - Any 99% rule violations
- `recommendations` - Action items

---

## Step 3: Return Summary

Return a concise summary to the calling agent:

```
Velocity Metrics:
- Current velocity: {velocity} story points (historical avg: {historical_avg})
- Trend: {improving/stable/declining}
- Cycle time: {avg_minutes} minutes average
- Completion: {percent}%

{If warnings exist:}
⚠️  Warnings:
- {warning 1}
- {warning 2}

Top Recommendations:
1. {recommendation 1}
2. {recommendation 2}
3. {recommendation 3}

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/project_metrics.json
```

---

## Example Invocation

**Scenario 1: Normal Progress Check**

Input: PM agent requests velocity check after completing task group G002

Expected output:
```
Velocity Metrics:
- Current velocity: 12 story points (historical avg: 10.5)
- Trend: improving
- Cycle time: 45 minutes average
- Completion: 40%

Top Recommendations:
1. Current velocity exceeds historical average - good progress
2. Estimated remaining time: 3.5 hours

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/project_metrics.json
```

**Scenario 2: 99% Rule Violation Detected**

Input: PM agent checks why task G003 is taking too long

Expected output:
```
Velocity Metrics:
- Current velocity: 8 story points (historical avg: 10.5)
- Trend: declining
- Cycle time: 125 minutes average
- Completion: 30%

⚠️  Warnings:
- 99% Rule Violation: Task G003 taking 3x longer than expected (135 min vs 45 min estimate)

Top Recommendations:
1. Escalate G003 to Tech Lead for investigation
2. Velocity below average - may need task breakdown
3. Database tasks pattern: taking 2.5x estimate

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/project_metrics.json
```

---

## Error Handling

**If script fails:**
- Check the script output for error messages
- Verify database `bazinga/bazinga.db` exists and contains PM state
- Return error message to calling agent

**If no completed groups:**
- Return: "No completed groups yet. Run velocity tracker after completing at least one task group."

**If historical data missing:**
- Script will create initial baseline
- Note: "First run - no historical comparison available"

---

## Notes

- The script handles all calculation logic (260+ lines)
- Supports both bash (Linux/Mac) and PowerShell (Windows)
- Gracefully degrades if historical data is missing
- Automatically updates historical metrics for future runs
