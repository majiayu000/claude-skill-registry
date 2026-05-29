---
name: nixtla-usage-optimizer
description: "Analyze Nixtla usage and optimize cost-effective forecast routing strategies. Use when auditing API usage or reducing costs. Trigger with 'optimize nixtla costs' or 'audit API usage'."
allowed-tools: "Read,Glob,Grep"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla Usage Optimizer

Audit Nixtla library usage and recommend cost-effective routing strategies.

## Overview

This skill analyzes and optimizes Nixtla usage:

- **Usage scanning**: Find all TimeGPT and baseline usage
- **Cost analysis**: Identify optimization opportunities
- **Routing recommendations**: Smart model selection
- **ROI assessment**: Cost vs accuracy trade-offs

## Prerequisites

**Required**:
- Python 3.8+
- Existing Nixtla codebase to audit

**No Additional Packages**: Uses only Read, Glob, Grep tools

## Instructions

### Step 1: Scan Repository

Find all Nixtla library usage:
```bash
grep -r "NixtlaClient" --include="*.py" .
grep -r "StatsForecast" --include="*.py" .
grep -r "MLForecast" --include="*.py" .
```

### Step 2: Analyze Patterns

Categorize usage by:
- Location (experiments, pipelines, notebooks)
- Frequency (how often called)
- Data characteristics (simple vs complex patterns)

### Step 3: Generate Report

Create `000-docs/nixtla_usage_report.md` with:
- Executive summary
- Usage analysis
- Recommendations
- ROI assessment

### Step 4: Implement Routing

Apply recommendations:
- Replace TimeGPT with baselines for simple patterns
- Add TimeGPT for high-value forecasts
- Implement fallback chains

## Output

- **000-docs/nixtla_usage_report.md**: Comprehensive usage report
- **routing_rules.json**: Machine-readable routing logic (optional)

## Error Handling

1. **Error**: `No Nixtla usage found`
   **Solution**: Repository may not use Nixtla - recommend adoption

2. **Error**: `Cannot determine cost impact`
   **Solution**: Add usage metrics or API call logging

3. **Error**: `Mixed usage patterns`
   **Solution**: Report both opportunities, prioritize high-impact

4. **Error**: `No baseline models found`
   **Solution**: Recommend adding StatsForecast for fallback

## Examples

### Example 1: Audit Existing Project

**Scan results**:
```
Found Nixtla usage:
  - TimeGPT: 12 locations
  - StatsForecast: 5 locations
  - MLForecast: 2 locations
```

**Recommendations**:
```
1. Replace TimeGPT in 4 low-impact areas (save ~40%)
2. Add fallback to StatsForecast baselines
3. Keep TimeGPT for high-value forecasts
```

### Example 2: No TimeGPT Yet

**Scan results**:
```
Found Nixtla usage:
  - StatsForecast: 8 locations
  - TimeGPT: 0 locations
```

**Recommendations**:
```
1. Add TimeGPT for 2 high-value forecasts
2. Keep baselines for simple patterns
3. Implement tiered routing
```

## Resources

- Routing Framework: See Error Handling section
- TimeGPT Pricing: https://nixtla.io/pricing
- StatsForecast Docs: https://nixtla.github.io/statsforecast/

**Related Skills**:
- `nixtla-experiment-architect`: Validate routing decisions
- `nixtla-timegpt-finetune-lab`: Evaluate fine-tuning ROI
- `nixtla-prod-pipeline-generator`: Implement routing in production
