---
name: pop-assessment-performance
description: "Evaluates PopKit efficiency using concrete metrics for context usage, token consumption, and lazy loading validation"
context: fork
triggers:
  - assess performance
  - performance test
  - efficiency audit
version: 1.0.0
---

# Performance Assessment Skill

## Purpose

Provides concrete, reproducible performance assessment for PopKit plugins using:

- Measurable efficiency metrics
- Automated context analysis
- Token consumption estimation
- Lazy loading validation

## How to Use

### Step 1: Run Automated Metrics Collection

```bash
python skills/pop-assessment-performance/scripts/measure_context.py packages/plugin/
python skills/pop-assessment-performance/scripts/analyze_loading.py packages/plugin/
python skills/pop-assessment-performance/scripts/calculate_efficiency.py packages/plugin/
```

### Step 2: Apply Performance Checklists

Read and apply checklists in order:

1. `checklists/context-efficiency.json` - Context window usage
2. `checklists/startup-performance.json` - Plugin initialization
3. `checklists/file-access-patterns.json` - Read/write efficiency

### Step 3: Generate Report

Combine automated metrics with checklist results for final performance report.

## Standards Reference

| Standard            | File                               | Key Checks            |
| ------------------- | ---------------------------------- | --------------------- |
| Context Efficiency  | `standards/context-efficiency.md`  | CE-001 through CE-008 |
| Startup Performance | `standards/startup-performance.md` | SP-001 through SP-006 |
| File Access         | `standards/file-access.md`         | FA-001 through FA-008 |
| Token Consumption   | `standards/token-consumption.md`   | TC-001 through TC-006 |

## Performance Targets

| Metric               | Target       | Warning   | Critical |
| -------------------- | ------------ | --------- | -------- |
| Skill Prompt Size    | <2000 tokens | 2000-4000 | >4000    |
| Agent Prompt Size    | <5000 tokens | 5000-8000 | >8000    |
| Tier-1 Agent Count   | <=15         | 16-20     | >20      |
| File Reads/Operation | <5           | 5-10      | >10      |
| Startup Files        | <10          | 10-20     | >20      |

## Output

Returns JSON with:

- `efficiency_score`: 0-100 (higher = better)
- `metrics`: Collected performance measurements
- `bottlenecks`: Identified performance issues
- `optimizations`: Recommended improvements
