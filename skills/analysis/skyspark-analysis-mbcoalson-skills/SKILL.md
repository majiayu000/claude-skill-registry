---
name: skyspark-analysis
description: SkySpark analytics for building automation systems including Axon queries, trend analysis, fault detection, and performance optimization using haystack tagging standards
---

# SkySpark Analysis Skill

This skill provides expertise in SkySpark analytics platform for building automation data analysis.

## Core Capabilities

### Data Query and Analysis
- Axon query development and optimization
- Haystack tag navigation and filtering
- Time series data analysis
- Historical trend evaluation

### Fault Detection
- Equipment fault identification
- Energy waste detection
- Performance degradation analysis
- Alarm correlation and root cause analysis

### Visualization and Reporting
- Custom dashboard development
- Trend chart creation and analysis
- Performance summary reports
- KPI tracking and visualization

## Available Scripts
- scripts/axon_query_builder.py: Generate common SkySpark queries
- scripts/trend_analyzer.py: Analyze time series data patterns
- scripts/fault_detector.py: Automated fault detection algorithms

## Reference Materials
- eferences/axon_syntax.md: Axon query language reference
- eferences/haystack_tags.md: Common haystack tag patterns
- eferences/fault_library.md: Common HVAC fault patterns

## Asset Templates
- ssets/dashboard_templates/: Pre-built dashboard configurations
- ssets/query_library.axon: Common SkySpark queries
- ssets/report_templates/: Analysis report formats

## Usage Examples
- "Query all AHU supply air temperature trends for last month"
- "Identify equipment with scheduling issues in SkySpark"
- "Create a dashboard for chiller plant efficiency"
- "Analyze energy consumption patterns from BAS data"

---

## Context Awareness

This skill integrates with work-command-center session tracking:

**Check Active Context:**

```bash
node .claude/skills/work-command-center/tools/session-state.js status
```

Returns: Project name, project number, duration, and deliverables context

**Log Activity Checkpoints:**

```bash
node .claude/skills/work-command-center/tools/session-state.js checkpoint \
  --activity "skyspark-analysis: Created AHU efficiency dashboard, identified 3 scheduling faults"
```

**Signal Completion (called by WCC after skill returns):**

```bash
node .claude/skills/work-command-center/tools/session-state.js skill-complete \
  --skill-name "skyspark-analysis" \
  --summary "Completed fault detection analysis. Found 3 scheduling issues and 2 setpoint deviations." \
  --outcome "success"
```

**Benefits:**

- WCC tracks time spent in this skill
- Session logs include skill work breakdown
- Context visible across skill transitions
- Deliverables auto-update from skill outcomes


## Saving Next Steps

When skyspark-analysis work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "skyspark-analysis" \
  --content "## Priority Tasks
1. Write Axon query for fault detection
2. Analyze trend data for HVAC optimization
3. Create SkySpark dashboard for building analytics"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`
