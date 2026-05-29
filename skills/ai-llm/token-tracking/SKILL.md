---
name: token-tracking
description: Token usage monitoring and cost tracking with configurable thresholds. Reference this skill to understand pricing and limits.
---

// Project Autopilot - Token Usage Monitoring
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Token Tracking Skill

Monitor token usage and costs with configurable thresholds for warnings, alerts, and hard stops. Thresholds can be set globally via `/autopilot:config` and persist across sessions.

---

## Model Pricing (as of 2024)

### Claude Models (4.5 Generation)

| Model | Input (per 1M) | Output (per 1M) |
|-------|----------------|-----------------|
| Opus | $5.00 | $25.00 |
| Sonnet | $3.00 | $15.00 |
| Haiku | $1.00 | $5.00 |

### Quick Reference

| Model | 1K Input | 1K Output | Typical Task |
|-------|----------|-----------|--------------|
| Opus | $0.005 | $0.025 | ~$0.05-0.20 |
| Sonnet | $0.003 | $0.015 | ~$0.02-0.10 |
| Haiku | $0.00025 | $0.00125 | ~$0.002-0.01 |

---

## Threshold Types

### Warning (Yellow) ⚠️
- Log warning to progress.md
- Display alert to user
- **Continue execution**

### Alert (Orange) 🟠
- Log alert to progress.md
- Display prominent alert
- **Pause and ask for confirmation**
- Resume only with explicit approval

### Stop (Red) 🛑
- Log stop reason to progress.md
- Save checkpoint immediately
- **Halt all execution**
- Require manual restart with increased limit

---

## Configuration Options

### By Dollar Amount

```bash
# Warning at $5, alert at $10, stop at $20
/autopilot:takeoff --warn-cost=5 --alert-cost=10 --max-cost=20

# Just a hard stop at $50
/autopilot:takeoff --max-cost=50

# Warning only
/autopilot:takeoff --warn-cost=10
```

### By Token Count

```bash
# Warning at 100K, alert at 500K, stop at 1M tokens
/autopilot:takeoff --warn-tokens=100000 --alert-tokens=500000 --max-tokens=1000000

# Using K/M suffixes
/autopilot:takeoff --warn-tokens=100K --alert-tokens=500K --max-tokens=1M
```

### Combined

```bash
# Stop at either $20 OR 1M tokens (whichever first)
/autopilot:takeoff --max-cost=20 --max-tokens=1M
```

---

## Tracking Data

### Token Log Format

Store in `.autopilot/token-usage.md`:

```markdown
# Token Usage Log

## Session Summary
**Started:** [Timestamp]
**Current:** [Timestamp]

### Totals
| Metric | Value |
|--------|-------|
| Input Tokens | 245,382 |
| Output Tokens | 89,421 |
| Estimated Cost | $4.23 |

### Thresholds
| Type | Limit | Current | Status |
|------|-------|---------|--------|
| Warning | $5.00 | $4.23 | 85% ⚠️ |
| Alert | $10.00 | $4.23 | 42% |
| Stop | $20.00 | $4.23 | 21% |

---

## Usage by Phase

| Phase | Input | Output | Cost |
|-------|-------|--------|------|
| 001 | 15,234 | 8,421 | $0.18 |
| 002 | 45,891 | 22,103 | $0.52 |
| 003 | 89,234 | 31,892 | $0.98 |

## Usage by Agent

| Agent | Model | Input | Output | Cost |
|-------|-------|-------|--------|------|
| planner | Sonnet | 12,345 | 5,678 | $0.12 |
| backend | Sonnet | 78,901 | 34,567 | $0.76 |
| architect | Opus | 23,456 | 12,345 | $1.28 |

---

## Event Log

### [Timestamp]
**Type:** Task Complete
**Task:** 003.2
**Tokens:** +5,234 input, +2,891 output
**Cost:** +$0.08
**Running Total:** $4.23

### [Timestamp]
**Type:** ⚠️ WARNING
**Threshold:** 85% of $5.00 warning limit
**Action:** Logged, continuing execution
```

---

## Threshold Checks

### When to Check

1. **After every tool call**
2. **After every agent response**
3. **Before starting new task**
4. **Before spawning sub-agent**

### Check Logic

```
FUNCTION checkThresholds(currentUsage):
    
    # Check STOP threshold (highest priority)
    IF currentUsage >= stopThreshold:
        LOG "🛑 STOP: Threshold reached"
        SAVE checkpoint immediately
        HALT execution
        RETURN "STOP"
    
    # Check ALERT threshold
    IF currentUsage >= alertThreshold:
        IF not alreadyAlerted:
            LOG "🟠 ALERT: Threshold reached"
            PAUSE execution
            ASK "Cost alert: ${current}/${limit}. Continue? (yes/no)"
            IF response != "yes":
                SAVE checkpoint
                HALT execution
                RETURN "STOP"
            SET alreadyAlerted = true
        RETURN "CONTINUE"
    
    # Check WARNING threshold
    IF currentUsage >= warnThreshold:
        IF not alreadyWarned:
            LOG "⚠️ WARNING: Approaching limit"
            DISPLAY warning banner
            SET alreadyWarned = true
        RETURN "CONTINUE"
    
    RETURN "CONTINUE"
```

---

## Cost Estimation

### Per-Task Estimates

| Task Type | Typical Tokens | Est. Cost (Sonnet) |
|-----------|----------------|-------------------|
| Read file | 500-2000 | $0.002-0.008 |
| Write file | 1000-5000 | $0.005-0.025 |
| Code generation | 2000-10000 | $0.01-0.05 |
| Code review | 3000-8000 | $0.015-0.04 |
| Test generation | 2000-6000 | $0.01-0.03 |
| Documentation | 1000-4000 | $0.005-0.02 |

### Per-Phase Estimates

| Phase | Tasks | Est. Tokens | Est. Cost |
|-------|-------|-------------|-----------|
| Setup | 5 | 20K | $0.10 |
| Database | 4 | 30K | $0.15 |
| Auth | 6 | 50K | $0.25 |
| API | 8 | 80K | $0.40 |
| Business | 10 | 100K | $0.50 |
| Frontend | 12 | 120K | $0.60 |
| Testing | 8 | 60K | $0.30 |

**Typical Full Project:** 500K-2M tokens, $2.50-$10.00 (Sonnet)

---

## Default Thresholds

### Threshold Priority (highest to lowest)

1. **CLI Arguments** - `--max-cost=N` etc.
2. **Checkpoint** - From previous session (in resume)
3. **Global Config** - From `~/.claude/autopilot/config.json`
4. **Built-in Defaults** - Fallback values

### Built-in Defaults

If no global config and no arguments:

| Type | Default |
|------|---------|
| Warning | $10.00 or 500K tokens |
| Alert | $25.00 or 1M tokens |
| Stop | $50.00 or 2M tokens |

### Setting Global Defaults

Configure once, apply to all projects:

```bash
# Set your preferred defaults
/autopilot:config --set max-cost=100
/autopilot:config --set warn-cost=20
/autopilot:config --set alert-cost=50

# View current config
/autopilot:config
```

These persist in `~/.claude/autopilot/config.json` and apply to all future builds unless overridden by CLI arguments.

### Reading Global Defaults

```
FUNCTION getEffectiveThresholds(cliArgs, checkpoint):

    # Load global config
    globalConfig = readJSON("~/.claude/autopilot/config.json")

    RETURN {
        maxCost: cliArgs.maxCost OR checkpoint?.maxCost OR globalConfig?.defaults.maxCost OR 50,
        warnCost: cliArgs.warnCost OR checkpoint?.warnCost OR globalConfig?.defaults.warnCost OR 10,
        alertCost: cliArgs.alertCost OR checkpoint?.alertCost OR globalConfig?.defaults.alertCost OR 25,
        maxTokens: cliArgs.maxTokens OR checkpoint?.maxTokens OR globalConfig?.defaults.maxTokens OR 2000000,
        warnTokens: cliArgs.warnTokens OR checkpoint?.warnTokens OR globalConfig?.defaults.warnTokens OR 500000,
        alertTokens: cliArgs.alertTokens OR checkpoint?.alertTokens OR globalConfig?.defaults.alertTokens OR 1000000
    }
```

To disable: `--no-cost-limit`

---

## Progress Display

Include in status output:

```
💰 Cost: $4.23 / $20.00 (21%)
📊 Tokens: 334K / 1M (33%)
████████░░░░░░░░░░░░ 21%
```

When approaching limits:

```
⚠️ Cost: $4.50 / $5.00 (90%) - WARNING
📊 Tokens: 450K / 500K (90%) - WARNING
██████████████████░░ 90%
```
