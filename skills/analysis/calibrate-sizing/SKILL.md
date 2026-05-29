---
name: calibrate-sizing
description: Use to improve story sizing accuracy by analyzing historical estimation data. Identifies patterns, updates size definitions, and refines PROBE proxy selections.
version: 1.0.0
---
<!-- Powered by PRISMâ„¢ Core -->

# Calibrate Sizing Task

## Purpose

Continuously improve story sizing accuracy using PSP measurement data:
- Analyze actual vs estimated times
- Update size category definitions
- Refine PROBE proxy selections
- Identify estimation patterns
- Improve future sizing precision

## Reference Materials

For detailed YAML examples of all structures below, see [./reference/probe-methodology.md](./reference/probe-methodology.md).

## SEQUENTIAL Task Execution

### 1. Gather Historical Data

Load completed stories from last 10-20 completions. Collect size distribution data including count, estimated average, actual average, and variance for each size category (VS, S, M, L, VL). Flag Very Large stories for potential breakdown.

### 2. Identify Patterns

**Analyze Systematic Biases:**

Identify overestimation patterns (e.g., Backend CRUD), underestimation patterns (e.g., third-party integrations), and accurate patterns. Document technology factors (new vs familiar tech multipliers) and complexity factors (high integration vs standalone).

### 3. Update Size Definitions

Based on actual data, compare old ranges to actual averages and propose new ranges. Update the story point mapping (1, 2, 3, 5, 8 points) accordingly. Flag 8-point stories as requiring split.

### 4. Refine PROBE Proxies

**Update Proxy Story Library:**

- Retire outdated proxies that no longer represent current patterns
- Add new proxies from recent well-estimated stories
- Organize proxies into categories: ui_simple, ui_with_api, backend_crud, integration
- Calculate average duration for each category

### 5. Create Regression Model

If sufficient data (>30 stories), build a regression model with:
- Base overhead (intercept)
- Factors per: acceptance criteria, API endpoints, UI components, database tables, integration points
- Formula combining all factors
- Model accuracy metrics (R-squared, mean error, confidence level)

### 6. Generate Recommendations

**Specific Improvements:**

Generate three categories of recommendations:
- **Immediate actions**: Size definition updates, buffer adjustments, estimate calibrations
- **Process improvements**: Flags for large stories, checklists for integrations
- **Training needs**: Team-specific guidance based on identified patterns

### 7. Update Estimation History

Record calibration details: date, stories analyzed, adjustments made (size ranges, proxy changes, patterns identified), accuracy improvement metrics, and next calibration trigger.

### 8. Generate Calibration Report

Generate a markdown report including:
- Executive Summary (stories analyzed, overall accuracy, key finding, primary action)
- Size Category Performance table
- Pattern Analysis (overestimation and underestimation patterns with actions)
- Updated Sizing Guide with new ranges
- Recommendations
- Next Steps

See [./reference/probe-methodology.md](./reference/probe-methodology.md) for the full report template.

## Success Criteria

- [ ] Minimum 10 stories analyzed
- [ ] Patterns identified and documented
- [ ] Size definitions updated if needed
- [ ] Proxy library refreshed
- [ ] Recommendations actionable
- [ ] Team notified of changes
- [ ] History file updated

## Output

- Calibration report (markdown)
- Updated estimation-history.yaml
- Modified PROBE proxy library
- New size range definitions
- Team communication of changes
