---
name: SCHEDULING
description: Generate resident schedules respecting ACGME rules, institutional policies, and individual preferences. Orchestrates constraint propagation, optimization, and conflict resolution for medical residency program scheduling.
---

# SCHEDULING Skill

Comprehensive workflow expertise for generating ACGME-compliant medical residency schedules. This skill orchestrates the entire schedule generation process from requirements gathering through validation and deployment.

## Overview

Medical residency scheduling is a **multi-objective constraint satisfaction problem** with three tiers of requirements:

1. **Tier 1 (Absolute)**: ACGME regulatory compliance - non-negotiable
2. **Tier 2 (Institutional)**: Program-specific policies - requires approval to override
3. **Tier 3 (Optimization)**: Preferences and fairness - best-effort satisfaction

This skill guides you through the complete workflow to produce schedules that satisfy all Tier 1 constraints, maximize Tier 2 satisfaction, and optimize Tier 3 objectives.

## When to Use This Skill

Use this skill when:
- Generating a new academic year schedule
- Creating rotation schedules for a specific block period
- Regenerating schedules after major changes (new residents, policy updates)
- Resolving systemic scheduling conflicts
- Optimizing existing schedules for better coverage or fairness
- Training on the scheduling system workflow

**Do NOT use this skill for:**
- Simple swap requests (use `swap-management` skill)
- Single assignment changes (use direct API)
- ACGME validation only (use `acgme-compliance` skill)
- Emergency coverage gaps (use incident response procedures)

## Required MCP Tools (MUST USE)

**Before ANY schedule operation, you MUST run these tools:**

```
1. validate_schedule_tool - Check existing schedule for violations
2. get_defense_level_tool - Assess current resilience state
3. rag_search("scheduling context [topic]") - Query knowledge base
```

**After schedule generation:**
```
1. validate_schedule_tool - Verify new schedule is compliant
2. check_mtf_compliance_tool - Military readiness report
3. run_contingency_analysis_resilience_tool - N-1/N-2 analysis
```

These tools are NOT optional. They prevent ACGME violations and operational failures.

## Five Phases of Schedule Generation

All schedule generation follows this structured workflow:

### Phase 1: Requirements Gathering
**Purpose:** Collect all constraints, preferences, and data inputs

**Activities:**
- Identify scheduling horizon (dates, blocks)
- Gather personnel data (residents, faculty, qualifications)
- Collect absence data (leave, TDY, deployments)
- Document rotation requirements (templates, coverage levels)
- Capture preferences (shift preferences, continuity requests)
- Review institutional policies (local rules, special requirements)

**Output:** Complete `SchedulingContext` with all inputs validated

**See:** `Workflows/generate-schedule.md` - Phase 1 details

### Phase 2: Constraint Propagation
**Purpose:** Apply constraints systematically to reduce search space

**Activities:**
- Apply ACGME hard constraints (80-hour, 1-in-7, supervision)
- Enforce availability constraints (absences block assignments)
- Apply qualification constraints (only assign qualified personnel)
- Propagate temporal constraints (post-call relief, continuity)
- Identify constraint conflicts early

**Output:** Feasibility analysis, reduced solution space

**See:** `Workflows/constraint-propagation.md`

### Phase 3: Optimization
**Purpose:** Find high-quality solutions using solver algorithms

**Activities:**
- Select appropriate solver (greedy, CP-SAT, PuLP, hybrid)
- Define optimization objectives (fairness, preferences, efficiency)
- Run solver with timeout and monitoring
- Generate multiple solutions (Pareto frontier)
- Evaluate solution quality metrics

**Output:** 1-3 candidate schedules with trade-off analysis

**See:** `schedule-optimization` skill for solver details

### Phase 4: Conflict Resolution
**Purpose:** Handle unavoidable conflicts and trade-offs

**Activities:**
- Identify remaining hard conflicts
- Rank conflicts by severity and impact
- Generate trade-off proposals
- Document exceptions and rationale
- Escalate unresolvable conflicts

**Output:** Conflict resolution report, exception documentation

**See:** `Workflows/conflict-resolution.md`

### Phase 5: Validation & Deployment
**Purpose:** Verify compliance and safely deploy schedule

**Activities:**
- Run comprehensive ACGME validation
- Verify coverage requirements met
- Check resilience metrics (N-1 contingency, 80% utilization)
- Create database backup (MANDATORY)
- Deploy schedule to production
- Generate reports and notifications

**Output:** Deployed schedule, validation report, backups

**See:** `safe-schedule-generation` skill for deployment procedures

## Key Files and Components

### Backend Scheduling System

| Component | Location | Purpose |
|-----------|----------|---------|
| Scheduling Engine | `backend/app/scheduling/engine.py` | Main orchestrator |
| Solvers | `backend/app/scheduling/solvers.py` | CP-SAT, greedy, PuLP algorithms |
| Constraints | `backend/app/scheduling/constraints/` | Modular constraint system |
| ACGME Validator | `backend/app/scheduling/acgme_validator.py` | Compliance checking |
| Context Builder | `backend/app/scheduling/context.py` | Data aggregation |

### Constraint System

All constraints inherit from `BaseConstraint` and implement:
- `validate()` - Check if assignment violates constraint
- `apply()` - Apply constraint to solver model
- `penalty()` - Soft constraint penalty calculation

**Constraint Categories:**
| Category | Files | Examples |
|----------|-------|----------|
| ACGME | `acgme.py` | 80-hour, 1-in-7, supervision |
| Availability | `temporal.py` | Absences, blackout dates |
| Coverage | `capacity.py`, `inpatient.py` | Minimum staffing levels |
| Equity | `equity.py`, `call_equity.py` | Fair workload distribution |
| Resilience | `resilience.py` | 80% utilization, N-1 |
| Specialty | `fmit.py`, `night_float_post_call.py` | Rotation-specific rules |

**See:** `Reference/constraint-index.md` for complete constraint catalog

### MCP Tools for Scheduling

| Tool | Phase | Purpose |
|------|-------|---------|
| `generate_schedule` | 3 | Generate new schedule |
| `validate_acgme_compliance` | 5 | Check ACGME rules |
| `detect_conflicts` | 4 | Find scheduling conflicts |
| `analyze_swap_candidates` | 4 | Find conflict resolutions |
| `get_schedule_health` | 5 | Quality metrics |
| `run_contingency_analysis_resilience_tool` | 5 | N-1/N-2 validation |

## Output Format

### Schedule Generation Request
```json
{
  "start_date": "2026-07-01",
  "end_date": "2027-06-30",
  "algorithm": "cp_sat",
  "timeout_seconds": 300,
  "objectives": {
    "acgme_compliance": 1.0,
    "fairness": 0.25,
    "preferences": 0.20,
    "efficiency": 0.15
  }
}
```

### Schedule Generation Response
```json
{
  "schedule_id": "2026-2027-academic-year",
  "status": "success",
  "assignments_created": 4380,
  "validation": {
    "acgme_compliant": true,
    "violations": [],
    "warnings": [
      "Resident PGY1-03 approaching 75 hours in week 12"
    ]
  },
  "metrics": {
    "coverage_rate": 0.97,
    "fairness_gini": 0.12,
    "preference_satisfaction": 0.84,
    "n1_compliant": true
  },
  "alternatives": [
    {
      "id": "alt-1",
      "description": "Maximizes fairness (Gini=0.08)",
      "trade_offs": "Lower preference satisfaction (0.78)"
    }
  ]
}
```

## Error Handling

### Common Errors and Resolutions

| Error | Cause | Resolution |
|-------|-------|------------|
| `NO_FEASIBLE_SOLUTION` | Over-constrained problem | Relax Tier 3 constraints, check absences |
| `ACGME_VIOLATION` | Invalid configuration | Review resident hours, supervision ratios |
| `INSUFFICIENT_COVERAGE` | Not enough personnel | Reduce coverage requirements or add personnel |
| `TIMEOUT` | Problem too complex | Use decomposition, increase timeout, or hybrid solver |
| `DATABASE_ERROR` | Connection/backup issue | Verify backend health, check backup status |

### Escalation Triggers

**Escalate to Program Director when:**
- Multiple Tier 1 violations cannot be resolved
- Systemic policy conflict (e.g., ACGME vs. institutional)
- Resource insufficiency (not enough residents/faculty)
- Solver repeatedly fails to find solutions

**Escalate to Technical Team when:**
- Solver crashes or hangs repeatedly
- Database corruption or backup failure
- Performance degradation (>10 minute solve times)
- New constraint type needed

## Success Criteria

A successfully generated schedule must meet:

| Criterion | Target | Validation Method |
|-----------|--------|-------------------|
| **ACGME Compliance** | 100% (zero violations) | `validate_acgme_compliance` |
| **Coverage** | >95% blocks assigned | Count assignments vs. required |
| **Fairness** | Gini coefficient <0.15 | Workload distribution analysis |
| **Resilience** | N-1 compliant | `run_contingency_analysis` |
| **Preference Match** | >80% soft preferences | User satisfaction survey |

## Integration with Other Skills

- **acgme-compliance**: Phase 2 and Phase 5 validation
- **schedule-optimization**: Phase 3 solver execution
- **safe-schedule-generation**: Phase 5 deployment procedures
- **swap-management**: Post-deployment adjustments
- **schedule-verification**: Human review checklist
- **constraint-preflight**: Adding new constraints

## See Also

### Workflow Documents
- `Workflows/generate-schedule.md` - Detailed step-by-step workflow
- `Workflows/constraint-propagation.md` - Constraint handling strategies
- `Workflows/conflict-resolution.md` - Trade-off negotiation

### Reference Documents
- `Reference/acgme-rules.md` - ACGME compliance requirements
- `Reference/institutional-rules.md` - Tripler-specific policies
- `Reference/constraint-index.md` - All constraints with priorities

### Architecture Documentation
- `docs/architecture/SOLVER_ALGORITHM.md` - Technical algorithm details
- `docs/architecture/cross-disciplinary-resilience.md` - Resilience framework
- `docs/development/CODEX_SYSTEM_OVERVIEW.md` - System architecture

### Related Skills
- `schedule-optimization` - Solver algorithms and optimization
- `safe-schedule-generation` - Backup and deployment safety
- `acgme-compliance` - Regulatory compliance validation
- `swap-management` - Post-deployment schedule adjustments
- `schedule-verification` - Human review procedures
