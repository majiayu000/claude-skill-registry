---
name: time-crystal-scheduling
description: Time crystal-inspired schedule stability analysis. Use when analyzing schedule churn, detecting natural periodicities, or optimizing for minimal disruption.
---

# Time Crystal Scheduling Skill

Use this skill when working with schedule stability, churn analysis, or periodicity detection.

## When to Use

- Analyzing schedule changes between regenerations
- Detecting natural cycles (weekly, biweekly, ACGME 4-week)
- Optimizing schedules for minimal disruption
- Checking stroboscopic checkpoint status
- Troubleshooting schedule instability

## Key Concepts

### Time Crystal Objective Function

```
score = (1-α-β)·constraint_score + α·rigidity_score + β·fairness_score
```

**Weight Guidelines:**
- α = 0.0: Pure constraint optimization (may cause large reshuffles)
- α = 0.3: Balanced - satisfy constraints with minimal disruption (RECOMMENDED)
- α = 0.5: Conservative - prefer stability over minor improvements
- α = 1.0: Pure stability (no changes even if suboptimal)

### Rigidity Score

Measures schedule stability (0.0-1.0):
- ≥0.95: Minimal changes (safe to publish)
- 0.85-0.94: Low churn (review recommended)
- 0.70-0.84: Moderate churn (review carefully)
- <0.50: Critical churn (investigate root cause)

### Subharmonic Periods

Natural cycles detected via autocorrelation:
- 7 days: Weekly structure
- 14 days: Alternating weekends
- 28 days: ACGME 4-week averaging window
- 84 days: Quarterly rotation

## Module Location

```
backend/app/scheduling/periodicity/
├── __init__.py              # Module exports
├── anti_churn.py            # Rigidity scoring, time crystal objective
├── subharmonic_detector.py  # Cycle detection via autocorrelation
└── stroboscopic_manager.py  # Checkpoint-based state management
```

## Key Functions

### Anti-Churn Analysis

```python
from app.scheduling.periodicity import (
    calculate_schedule_rigidity,
    time_crystal_objective,
    estimate_churn_impact,
    hamming_distance,
)

# Compare two schedules
rigidity = calculate_schedule_rigidity(new_schedule, current_schedule)
# Returns 0.0-1.0 (1.0 = identical)

# Get detailed impact
impact = estimate_churn_impact(current, proposed)
# Returns: total_changes, affected_people, severity, recommendation
```

### Periodicity Detection

```python
from app.scheduling.periodicity import (
    detect_subharmonics,
    analyze_periodicity,
)

# Find natural cycles
cycles = detect_subharmonics(assignments, base_period=7)
# Returns: [7, 14, 28] - detected cycle lengths in days

# Full analysis
report = analyze_periodicity(assignments)
# Returns: PeriodicityReport with strength, patterns, recommendations
```

### Stroboscopic State Management

```python
from app.scheduling.periodicity import (
    StroboscopicScheduleManager,
    CheckpointBoundary,
)

manager = StroboscopicScheduleManager()

# Propose draft changes
await manager.propose_draft(new_assignments)

# Advance checkpoint (makes draft authoritative)
await manager.advance_checkpoint(CheckpointBoundary.WEEK_START)

# Get stable state (what observers see)
state = await manager.get_observable_state()
```

## MCP Tools

5 MCP tools available:

1. **`analyze_schedule_rigidity_tool`** - Compare schedule stability
2. **`analyze_schedule_periodicity_tool`** - Detect natural cycles
3. **`calculate_time_crystal_objective_tool`** - Combined optimization score
4. **`get_checkpoint_status_tool`** - Stroboscopic state info
5. **`get_time_crystal_health_tool`** - Component health monitoring

## Common Tasks

### Check if Schedule Regeneration is Safe

```python
from app.scheduling.periodicity import estimate_churn_impact, ScheduleSnapshot

current = ScheduleSnapshot.from_assignments(current_assignments)
proposed = ScheduleSnapshot.from_assignments(proposed_assignments)

impact = estimate_churn_impact(current, proposed)

if impact["severity"] in ["high", "critical"]:
    print(f"WARNING: {impact['affected_people']} people affected")
    print(f"Recommendation: {impact['recommendation']}")
else:
    print("Safe to publish")
```

### Preserve Natural Patterns

```python
from app.scheduling.periodicity import analyze_periodicity

report = analyze_periodicity(assignments)

# Configure optimizer to preserve detected patterns
optimizer_config = {
    "preserve_cycles": report.subharmonic_periods,
    "rigidity_weight": 0.3 if report.periodicity_strength > 0.7 else 0.5,
}
```

## Documentation

- Architecture: `docs/architecture/TIME_CRYSTAL_ANTI_CHURN.md`
- Research: `docs/SYNERGY_ANALYSIS.md` Section 11
- Integration Guide: `backend/app/scheduling/periodicity/INTEGRATION_GUIDE.md`

## References

- Shleyfman et al. (2025). Planning with Minimal Disruption. arXiv:2508.15358
- Time Crystal Physics: Discrete time crystals (Wilczek 2012)
- docs/explorations/boolean-algebra-parallels.md
