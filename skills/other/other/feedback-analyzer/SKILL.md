---
name: feedback-analyzer
description: Analyze skill effectiveness through usage feedback, metrics analysis, and outcome assessment. Task-based operations for feedback collection, effectiveness measurement, trend analysis, and insight extraction. Use when analyzing skill effectiveness, measuring ROI, understanding usage patterns, or evaluating toolkit impact based on real usage data.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Feedback Analyzer

## Overview

feedback-analyzer evaluates skill effectiveness through analysis of usage data, feedback, metrics, and outcomes.

**Purpose**: Data-driven understanding of what works and what doesn't

**The 4 Analysis Operations**:
1. **Collect Usage Data** - Gather metrics on skill usage and effectiveness
2. **Measure Effectiveness** - Quantify impact and ROI of skills
3. **Analyze Trends** - Identify patterns in usage and effectiveness
4. **Extract Insights** - Generate actionable insights from data

## When to Use

- After skills have been used (have usage data)
- Measuring toolkit ROI and impact
- Understanding which skills provide most value
- Identifying underutilized skills
- Data-driven improvement decisions

## Operations

### Operation 1: Collect Usage Data

**Purpose**: Gather data on how skills are used

**Data Sources**:
- Build times (how long to build skills?)
- Usage frequency (which skills used most?)
- Effectiveness metrics (do skills achieve purposes?)
- Quality scores (from reviews)
- User feedback (satisfaction, issues)

**Process**:
1. Identify data sources
2. Collect available metrics
3. Document usage patterns
4. Organize data for analysis

**Output**: Usage data collection

**Time**: 30-60 minutes

---

### Operation 2: Measure Effectiveness

**Purpose**: Quantify skill impact and ROI

**Metrics**:
- Time savings (vs without tool)
- Quality improvements (before/after)
- Efficiency gains (percentage faster)
- Usage rate (frequency of use)
- Satisfaction (user ratings)

**Process**:
1. Define effectiveness criteria
2. Calculate metrics
3. Compare to baseline or targets
4. Assess ROI

**Output**: Effectiveness measurements with evidence

**Time**: 45-90 minutes

---

### Operation 3: Analyze Trends

**Purpose**: Identify patterns in effectiveness over time

**Process**:
1. Plot metrics over time
2. Identify trends (improving/degrading/stable)
3. Find correlations
4. Detect anomalies

**Output**: Trend analysis with insights

**Time**: 45-90 minutes

---

### Operation 4: Extract Insights

**Purpose**: Generate actionable insights from data

**Process**:
1. Synthesize findings
2. Identify high-impact insights
3. Make recommendations
4. Prioritize actions

**Output**: Data-driven insights and recommendations

**Time**: 30-60 minutes

---

## Example Analysis

```
Effectiveness Analysis: Development Toolkit
===========================================

Usage Data (Skills 1-23):
- Build times: 2h - 20h (mean: 6.8h)
- Efficiency: 35% - 97% faster than baseline (mean: 85%)
- Quality: 100% pass rate (5/5 structure)

Effectiveness Metrics:
- Time Saved: 392 hours total (85% reduction)
- Quality: Maintained (100% Grade A)
- Completion: 100% (all 23 finished)
- ROI: 392h saved / 68h invested = 576% ROI

Trends:
✅ Improving: Efficiency compounds (72% → 97%)
✅ Stable: Quality consistent (all 5/5)
⚠️ Plateau: Efficiency plateaus ~85-90% for simple skills

Insights:
1. Toolkit highly effective (576% ROI, 85% efficiency)
2. Quality maintained despite speed (100% pass rate)
3. Efficiency plateaus at 85-90% (cannot exceed certain minimum times)
4. Complex skills still benefit (35-50% faster)

Recommendations:
1. Continue using toolkit (proven effective)
2. Expect 85-90% efficiency for simple/medium skills
3. Adjust estimates for complex skills (30-50% faster, not 85%)
4. Focus on quality maintenance (already excellent)
```

---

## Quick Reference

| Operation | Focus | Time | Output |
|-----------|-------|------|--------|
| Collect Usage Data | Gather metrics | 30-60m | Data collection |
| Measure Effectiveness | Quantify impact, ROI | 45-90m | Effectiveness metrics |
| Analyze Trends | Patterns over time | 45-90m | Trend analysis |
| Extract Insights | Actionable insights | 30-60m | Recommendations |

**Integration**: Uses data from skill-evolution-tracker, analysis skill

---

**feedback-analyzer provides data-driven understanding of toolkit effectiveness for evidence-based improvement decisions.**
