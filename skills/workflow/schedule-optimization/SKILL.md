---
name: schedule-optimization
description: Multi-objective schedule optimization expertise using constraint programming and Pareto optimization. Use when generating schedules, improving coverage, balancing workloads, or resolving conflicts. Integrates with OR-Tools solver and resilience framework.
model_tier: opus
parallel_hints:
  can_parallel_with: [constraint-preflight, acgme-compliance]
  must_serialize_with: [safe-schedule-generation, SCHEDULING, solver-control]
  preferred_batch_size: 1
context_hints:
  max_file_context: 100
  compression_level: 0
  requires_git_context: true
  requires_db_context: true
escalation_triggers:
  - pattern: "infeasible|no solution"
    reason: "Infeasible constraints require human review of requirements"
  - pattern: "timeout|stuck"
    reason: "Solver performance issues may need decomposition strategy"
  - keyword: ["block-assigned", "FMIT", "Night Float"]
    reason: "Block-assigned rotations have special handling requirements"
---

# Schedule Optimization Skill

Expert knowledge for generating and optimizing medical residency schedules using constraint programming and multi-objective optimization.

## Solver Status (2025-12-24, Updated 2025-12-26)

| Issue | Status | Fix Applied |
|-------|--------|-------------|
| Greedy template selection | FIXED | Selects template with fewest assignments |
| CP-SAT no template balance | FIXED | Added template_balance_penalty to objective |
| Template filtering missing | FIXED | `_get_rotation_templates()` defaults to `activity_type="outpatient"` |

**NOTE (2025-12-26):** The template filtering was initially set to `"clinic"` which was incorrect.
PR #442 was not merged because this issue was caught during evaluation. The correct filter
is `"outpatient"` because that matches the elective/selective templates that use half-day
scheduling. The `"clinic"` activity_type is specifically for FM Clinic which has its own
capacity and supervision constraint logic.

See `backend/app/scheduling/solvers.py` header for implementation details.

## Architecture: Block vs Half-Day Scheduling

**IMPORTANT:** This system has two distinct scheduling modes:

| Mode | Rotations | Assignment Unit | Solver Role |
|------|-----------|-----------------|-------------|
| **Block-Assigned** | FMIT, NF, Inpatient, NICU | Full block or half-block | Pre-assigned, NOT optimized |
| **Half-Day Optimized** | Clinic, Specialty | Half-day (AM/PM) | Solver optimizes these |

**The solvers are ONLY for outpatient half-day optimization.** Block-assigned rotations
are handled separately and should NOT be passed to the solver.

If solver assigns everyone to NF/PC/inpatient, check that templates are filtered
to `activity_type == "outpatient"` in `engine._get_rotation_templates()`.

**Activity Types Clarification:**
| Activity Type | Templates | For Solver? |
|---------------|-----------|-------------|
| `outpatient` | Neurology, ID, Palliative, PedsSub, etc. | YES - half-day electives |
| `clinic` | Family Medicine Clinic (FMC) | NO - has separate capacity constraints |
| `inpatient` | FMIT, IM, EM, L&D | NO - block-assigned |
| `night_float` | NF, NICU+NF, etc. | NO - block-assigned |
| `procedure` | Procedures Rotation | Depends on configuration |

### Night Float (NF) Half-Block Mirrored Pairing

NF has idiosyncratic half-block constraints - residents are paired in mirrored patterns:

```
Block 5 (4 weeks):
├── Half 1 (Days 1-14)     ├── Half 2 (Days 15-28)
│                          │
│ Resident A: NF           │ Resident A: NICU (or elective)
│ Resident B: NEURO        │ Resident B: NF
```

**Key rules:**
- NF is assigned per **half-block** (2 weeks), not full block
- Residents are **mirrored pairs**: one on NF half 1, partner on NF half 2
- The non-NF half is a mini 2-week rotation (NICU, NEURO, elective)
- **Post-Call (PC)** day required after NF ends (Day 15 or Day 1 of next block)
- Exactly 1 resident on NF per half-block

**Files:** See `backend/app/scheduling/constraints/night_float_post_call.py` and
`docs/development/CODEX_SYSTEM_OVERVIEW.md` for full NF/PC constraint logic.

## When This Skill Activates

- Generating new schedules
- Optimizing existing schedules
- Balancing workload distribution
- Resolving scheduling conflicts
- Improving coverage patterns
- Reducing schedule fragmentation

## Optimization Objectives

### Primary Objectives (Hard Constraints)
These MUST be satisfied - schedule is invalid without them:

| Constraint | Description | Priority |
|------------|-------------|----------|
| ACGME Compliance | 80-hour, 1-in-7, supervision | P0 |
| Qualification Match | Only assign qualified personnel | P0 |
| No Double-Booking | One person, one place at a time | P0 |
| Minimum Coverage | Required staffing levels met | P0 |

### Secondary Objectives (Soft Constraints)
Optimize these after hard constraints satisfied:

| Objective | Description | Weight |
|-----------|-------------|--------|
| Fairness | Even workload distribution | 0.25 |
| Preferences | Honor stated preferences | 0.20 |
| Continuity | Minimize handoffs | 0.20 |
| Efficiency | Minimize gaps/fragments | 0.15 |
| Resilience | Maintain backup capacity | 0.20 |

## Solver Architecture

### Google OR-Tools CP-SAT
Primary constraint programming solver:

```python
# Located in: backend/app/scheduling/engine.py
from ortools.sat.python import cp_model

model = cp_model.CpModel()
# Define variables, constraints, objectives
solver = cp_model.CpSolver()
status = solver.Solve(model)
```

### Solver Configuration
| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_time_seconds` | 300 | Solver timeout |
| `num_workers` | 8 | Parallel threads |
| `log_search_progress` | True | Show progress |

## Optimization Strategies

### 1. Pareto Optimization
Find solutions that balance multiple objectives:

```
No single "best" solution - instead find Pareto frontier:
- Solution A: Best fairness, moderate efficiency
- Solution B: Best efficiency, moderate fairness
- Solution C: Balanced trade-off
```

**MCP Tool:**
```
Tool: generate_pareto_schedules
Input: { objectives: [...], constraints: [...] }
Output: { frontier: [solution1, solution2, ...] }
```

### 2. Iterative Improvement
Start with feasible solution, improve incrementally:

```
1. Generate any valid schedule
2. Identify worst metric
3. Local search for improvements
4. Repeat until no improvement or timeout
```

### 3. Decomposition
Break large problem into smaller sub-problems:

```
Full Year Schedule
    ├── Q1 (Jan-Mar)
    │   ├── Month 1
    │   │   ├── Week 1-2
    │   │   └── Week 3-4
    │   └── ...
    └── Q2-Q4 (similar)
```

## Coverage Optimization

### Target Coverage Levels
| Rotation | Minimum | Target | Maximum |
|----------|---------|--------|---------|
| Inpatient | 2 | 3 | 4 |
| Emergency | 3 | 4 | 5 |
| Clinic | 1 | 2 | 3 |
| Procedures | 1 | 2 | 2 |

### Coverage Gap Resolution

**Step 1: Identify Gap**
```sql
SELECT date, session, rotation, COUNT(*) as coverage
FROM assignments
WHERE date BETWEEN :start AND :end
GROUP BY date, session, rotation
HAVING COUNT(*) < minimum_coverage;
```

**Step 2: Find Candidates**
- Available personnel (not scheduled)
- Under hour limits
- Qualified for rotation
- Fair workload consideration

**Step 3: Assign and Validate**
- Make assignment
- Re-run compliance check
- Update metrics

## Workload Balancing

### Fairness Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Gini Coefficient | Distribution equality | < 0.15 |
| Std Dev Hours | σ of weekly hours | < 5 |
| Max/Min Ratio | Highest/Lowest load | < 1.3 |

### Balancing Algorithm

```python
def balance_workload(assignments):
    while gini_coefficient(assignments) > 0.15:
        overloaded = find_highest_load()
        underloaded = find_lowest_load()

        # Find swappable shift
        shift = find_transferable_shift(overloaded, underloaded)
        if shift and is_valid_transfer(shift):
            transfer(shift, from=overloaded, to=underloaded)
        else:
            break  # No valid transfers available
```

## Preference Handling

### Preference Types
| Type | Priority | Example |
|------|----------|---------|
| Hard Block | Highest | "Cannot work Dec 25" |
| Soft Preference | Medium | "Prefer AM shifts" |
| Historical Pattern | Low | Past scheduling data |

### Preference Satisfaction
Aim for:
- 100% hard blocks honored
- 80%+ soft preferences
- 70%+ historical patterns

## Resilience Integration

### 80% Utilization Rule
Never schedule above 80% capacity (queuing theory):

```
If utilization > 80%:
    - Queue delays grow exponentially
    - No buffer for emergencies
    - Burnout risk increases
```

### N-1 Contingency
Schedule must remain valid if any one person unavailable:

```
Tool: run_contingency_analysis_resilience_tool
Check: Remove each person, verify coverage holds
```

### Static Fallbacks
Pre-compute backup schedules for common failure scenarios:

```
Tool: get_static_fallbacks_tool
Returns: { scenario: backup_schedule, ... }
```

## Optimization Workflow

### New Schedule Generation

**Step 1: Gather Inputs**
```yaml
inputs:
  - personnel: All available faculty/residents
  - rotations: Required rotation coverage
  - preferences: Submitted preferences
  - constraints: ACGME + program rules
  - horizon: Date range to schedule
```

**Step 2: Initialize Solver**
```python
engine = SchedulingEngine(
    solver="or-tools",
    objectives=["compliance", "fairness", "preferences"],
    timeout=300
)
```

**Step 3: Generate Solutions**
```python
solutions = engine.solve(inputs)
# Returns Pareto frontier of valid schedules
```

**Step 4: Present Options**
Show decision-makers 3-5 options with trade-offs:
- Option A: Maximizes fairness
- Option B: Maximizes preferences
- Option C: Balanced approach

**Step 5: Select and Finalize**
- Human selects preferred option
- System validates one more time
- Publish to calendar system

### Existing Schedule Optimization

**Step 1: Analyze Current State**
```
Tool: analyze_schedule_health
Returns: {
  compliance_score,
  fairness_score,
  coverage_gaps,
  improvement_opportunities
}
```

**Step 2: Identify Improvements**
Rank opportunities by impact/effort:
- Quick wins: Single swap fixes issue
- Medium effort: Multi-swap optimization
- Major restructure: Requires re-solve

**Step 3: Apply Changes**
- Execute as atomic transaction
- Validate after each change
- Rollback if validation fails

## Common Scenarios

### Scenario: New Block Schedule
**Input:** Need 13-week rotation schedule
**Process:**
1. Load rotation templates
2. Apply qualification constraints
3. Balance across 13 weeks
4. Optimize for preferences
5. Validate ACGME compliance
6. Generate 3 options for review

### Scenario: Coverage Emergency
**Input:** 3 faculty out sick tomorrow
**Process:**
1. Identify critical gaps
2. Query backup pool
3. Optimize minimal disruption
4. Execute emergency swaps
5. Document and rebalance later

### Scenario: Fairness Complaint
**Input:** Resident claims unfair workload
**Process:**
1. Run fairness analysis
2. Compare to cohort
3. If valid, identify rebalancing swaps
4. Execute approved changes
5. Monitor going forward

## Performance Metrics

### Solver Performance
| Metric | Target | Action if Missed |
|--------|--------|------------------|
| Solve Time | < 5 min | Increase timeout or decompose |
| Solution Quality | > 90% optimal | Tune weights |
| Constraint Satisfaction | 100% hard | Debug constraints |

### Schedule Quality
| Metric | Target | Measurement |
|--------|--------|-------------|
| ACGME Compliance | 100% | Zero violations |
| Coverage | 100% | All slots filled |
| Fairness (Gini) | < 0.15 | Weekly calculation |
| Preference Match | > 80% | Survey feedback |

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `generate_schedule` | Create new schedule |
| `optimize_schedule` | Improve existing schedule |
| `analyze_schedule_health` | Quality metrics |
| `generate_pareto_schedules` | Multi-objective options |
| `validate_schedule` | Compliance check |
| `run_contingency_analysis_resilience_tool` | N-1/N-2 analysis |

## REQUIRED: Documentation After Each Step

**Every scheduling task MUST include documentation updates.** This prevents knowledge loss
between sessions and ensures issues are tracked properly.

### Documentation Checkpoint Protocol

After EACH significant step, document:

1. **What was attempted** - The specific action or fix tried
2. **What happened** - Actual results (success, failure, unexpected behavior)
3. **What was learned** - New understanding of the system
4. **What needs to happen next** - Remaining work or blockers

### Where to Document

| Finding Type | Location | Example |
|--------------|----------|---------|
| Bug/Known Issue | `solvers.py` header | Template selection bug |
| Architecture insight | This skill file | Block vs half-day modes |
| Workaround | Code comments + skill | Manual adjustment needed |
| Fix needed | TODO in code + HUMAN_TODO.md | Template filtering |

### Planning Template

When starting a scheduling task, create a plan that includes documentation:

```markdown
## Task: [Description]

### Phase 1: Investigation
- [ ] Explore current state
- [ ] Document findings in [location]

### Phase 2: Implementation
- [ ] Make changes
- [ ] Document what changed in commit message

### Phase 3: Verification
- [ ] Test the changes
- [ ] Document results (success/failure)

### Phase 4: Documentation Update
- [ ] Update skill if new knowledge gained
- [ ] Update code comments if behavior clarified
- [ ] Update HUMAN_TODO.md if manual work needed
```

### Anti-Pattern: Silent Failures

**DO NOT:**
- Discover an issue and only mention it in chat
- Switch to a "workaround" without documenting why
- Assume the next session will remember context

**DO:**
- Add issues to code headers immediately
- Update skill files with architectural insights
- Create explicit TODOs for unfixed problems

## Concrete Usage Example

### End-to-End: Generating Block 10 Schedule

**Scenario:** Generate a 13-week schedule for Block 10 (Jan-Apr 2025) with 6 residents, ensuring ACGME compliance and fair call distribution.

**Step 1: Gather Requirements**
```bash
cd /home/user/Autonomous-Assignment-Program-Manager/backend

# Check available residents
python -c "
from app.db.session import SessionLocal
from app.models import Person
from sqlalchemy import select

with SessionLocal() as db:
    residents = db.execute(select(Person).where(Person.role == 'RESIDENT')).scalars().all()
    print(f'Found {len(residents)} residents')
    for r in residents:
        print(f'  - {r.id}: {r.first_name} {r.last_name} (PGY-{r.pgy_level})')
"

# Check rotation templates
python -c "
from app.db.session import SessionLocal
from app.models import RotationTemplate
from sqlalchemy import select

with SessionLocal() as db:
    templates = db.execute(select(RotationTemplate)).scalars().all()
    print(f'Found {len(templates)} rotation templates')
    for t in templates[:10]:
        print(f'  - {t.name} ({t.activity_type})')
"
```

**Expected Output:**
```
Found 6 residents
  - res-001: Alice Smith (PGY-1)
  - res-002: Bob Jones (PGY-2)
  ...

Found 25 rotation templates
  - Family Medicine Clinic (clinic)
  - Neurology (outpatient)
  - Palliative Care (outpatient)
  ...
```

**Step 2: Initialize Solver**
```python
# In backend/app/scheduling/engine.py or interactive shell
from datetime import date
from app.scheduling.engine import SchedulingEngine
from app.scheduling.constraints.manager import ConstraintManager
from app.db.session import SessionLocal

db = SessionLocal()

# Create engine with Block 10 constraints
engine = SchedulingEngine(
    db=db,
    block_number=10,
    start_date=date(2025, 1, 6),  # Block 10 start
    end_date=date(2025, 4, 6),     # Block 10 end (13 weeks)
    solver_type="or-tools",
    timeout_seconds=300
)

# Load constraints
constraint_manager = ConstraintManager.create_default()
print(f"Loaded {len(constraint_manager.constraints)} constraints")
```

**Step 3: Run Solver**
```python
# Generate schedule
result = engine.solve()

if result.status == "OPTIMAL" or result.status == "FEASIBLE":
    print(f"✅ Solution found! Status: {result.status}")
    print(f"   Objective value: {result.objective_value}")
    print(f"   Assignments: {len(result.assignments)}")
else:
    print(f"❌ No solution: {result.status}")
    print(f"   Reason: {result.error_message}")
```

**Expected Output (Success):**
```
✅ Solution found! Status: OPTIMAL
   Objective value: 245.3
   Assignments: 156 (6 residents × 13 weeks × 2 sessions)
```

**Step 4: Validate Solution**
```python
from app.scheduling.acgme_validator import ACGMEValidator

validator = ACGMEValidator()
compliance_result = validator.validate_schedule(
    assignments=result.assignments,
    start_date=date(2025, 1, 6),
    end_date=date(2025, 4, 6)
)

if compliance_result.is_compliant:
    print("✅ ACGME compliance: PASS")
else:
    print("❌ ACGME violations:")
    for violation in compliance_result.violations:
        print(f"   - {violation}")
```

**Step 5: Analyze Fairness**
```python
# Check call distribution
from collections import Counter

call_assignments = [a for a in result.assignments if a.is_call]
call_counts = Counter(a.person_id for a in call_assignments)

print("Call distribution:")
for person_id, count in call_counts.items():
    print(f"  {person_id}: {count} call shifts")

# Calculate Gini coefficient
from app.analytics.fairness import calculate_gini_coefficient

gini = calculate_gini_coefficient([count for count in call_counts.values()])
print(f"Gini coefficient: {gini:.3f} (target < 0.15)")
```

**Expected Output:**
```
Call distribution:
  res-001: 13 call shifts
  res-002: 12 call shifts
  res-003: 13 call shifts
  res-004: 12 call shifts
  res-005: 13 call shifts
  res-006: 12 call shifts

Gini coefficient: 0.021 (target < 0.15) ✅
```

**Step 6: Handle Common Issues**

**Issue: Solver times out without solution**
```python
# Try decomposition approach
from app.scheduling.decomposition import decompose_by_month

monthly_solutions = []
for month_start, month_end in decompose_by_month(date(2025, 1, 6), date(2025, 4, 6)):
    month_engine = SchedulingEngine(
        db=db,
        start_date=month_start,
        end_date=month_end,
        solver_type="or-tools",
        timeout_seconds=60  # Shorter timeout for smaller problem
    )
    month_result = month_engine.solve()
    monthly_solutions.append(month_result)

# Combine monthly solutions
combined_solution = combine_solutions(monthly_solutions)
```

**Issue: Infeasible constraints**
```python
# Run pre-solver validation to detect issues early
from app.scheduling.validation import validate_constraints_feasibility

feasibility_check = validate_constraints_feasibility(
    residents=residents,
    rotations=rotations,
    date_range=(date(2025, 1, 6), date(2025, 4, 6))
)

if not feasibility_check.is_feasible:
    print("❌ Constraints are infeasible!")
    for issue in feasibility_check.issues:
        print(f"   - {issue.description}")
        print(f"     Suggestion: {issue.suggestion}")
```

**Step 7: Save Solution**
```python
from app.services.schedule_service import save_schedule

# Save to database
schedule_id = await save_schedule(
    db=db,
    assignments=result.assignments,
    block_number=10,
    generated_by="solver",
    notes="Block 10 schedule generated with OR-Tools CP-SAT solver"
)

print(f"✅ Schedule saved with ID: {schedule_id}")
```

**Total Time:** ~10-15 minutes for successful generation

## Common Failure Modes

### Failure Mode 1: Solver Assigns Everyone to Same Rotation
**Symptom:** All residents assigned to NF, FMIT, or other block-assigned rotation

**Cause:** Template filtering not restricting to half-day rotations

**Detection:**
```python
# Check assigned templates
assigned_templates = set(a.rotation_template_name for a in result.assignments)
print(f"Templates used: {assigned_templates}")
# Output: {'Night Float', 'FMIT'} ← WRONG! Should be outpatient electives
```

**Fix:**
```python
# In engine.py, _get_rotation_templates()
def _get_rotation_templates(self, activity_type: str = "outpatient"):
    """Get rotation templates for solver.

    Args:
        activity_type: Filter to this activity type (default: "outpatient")
                      Use "outpatient" for elective/selective half-day scheduling
                      NOT "clinic" (that's for FM Clinic capacity constraints)
    """
    templates = db.execute(
        select(RotationTemplate).where(RotationTemplate.activity_type == activity_type)
    ).scalars().all()
    return templates
```

### Failure Mode 2: Solver Times Out
**Symptom:** Solver runs for 5+ minutes without finding solution

**Cause:** Problem too large, conflicting constraints, or poor initial solution

**Detection:**
```python
# Check solver progress
if result.status == "TIMEOUT":
    print(f"Solver timed out after {result.solve_time_seconds}s")
    print(f"Best objective found: {result.best_objective}")
```

**Fix Options:**
1. **Increase timeout:**
   ```python
   engine = SchedulingEngine(..., timeout_seconds=600)  # 10 minutes
   ```

2. **Decompose problem:**
   ```python
   # Break 13 weeks into 4 smaller problems (3-4 weeks each)
   ```

3. **Relax soft constraints:**
   ```python
   # Reduce weight of less important constraints
   constraint_manager.get("TuesdayCallPreference").weight = 1.0  # Lower priority
   ```

### Failure Mode 3: No Template Balance
**Symptom:** Some residents get 10 assignments, others get 2

**Cause:** Greedy selection or missing template_balance_penalty in objective

**Detection:**
```python
from collections import Counter

assignments_per_person = Counter(a.person_id for a in result.assignments)
print(f"Min assignments: {min(assignments_per_person.values())}")
print(f"Max assignments: {max(assignments_per_person.values())}")
print(f"Ratio: {max(assignments_per_person.values()) / min(assignments_per_person.values()):.2f}")
# If ratio > 1.3, balance is poor
```

**Fix:**
```python
# In solver, add template balance penalty to objective
template_counts = {}  # person_id -> template_name -> count

for person, template, block in assignment_vars:
    if person not in template_counts:
        template_counts[person] = {}
    if template not in template_counts[person]:
        template_counts[person][template] = 0

    template_counts[person][template] += assignment_vars[(person, template, block)]

# Penalize imbalance
for person in template_counts:
    counts = list(template_counts[person].values())
    max_count = model.NewIntVar(0, 100, f"max_count_{person}")
    min_count = model.NewIntVar(0, 100, f"min_count_{person}")

    model.AddMaxEquality(max_count, counts)
    model.AddMinEquality(min_count, counts)

    balance_penalty = max_count - min_count
    objective_terms.append(-5 * balance_penalty)  # Penalize imbalance
```

### Failure Mode 4: ACGME Violations Post-Solve
**Symptom:** Solver completes but validation finds 80-hour violations

**Cause:** ACGME constraint not properly added to solver or validation using different logic

**Detection:**
```python
validator = ACGMEValidator()
result = validator.validate_schedule(assignments)

if not result.is_compliant:
    for violation in result.violations:
        if "80-hour" in violation.rule_name:
            print(f"Person {violation.person_id}: {violation.hours} hours in week {violation.week}")
```

**Fix:**
```python
# Ensure 80-hour constraint is in solver
# In constraints/acgme.py
class EightyHourRule(HardConstraint):
    def add_to_cpsat(self, model, variables, context):
        for person in context.persons:
            for week_start in context.weeks:
                week_assignments = [
                    var for var, (p, d, s) in variables.items()
                    if p == person.id and week_start <= d < week_start + timedelta(days=7)
                ]

                # Each assignment is ~10-12 hours, enforce max 80
                model.Add(sum(week_assignments) * 10 <= 80)
```

### Failure Mode 5: Forgetting to Document
**Symptom:** Next session repeats same debugging, loses context

**Cause:** Not following documentation checkpoint protocol

**Prevention:**
After each solver run:
1. Update `backend/app/scheduling/solvers.py` header with findings
2. Update this skill file with new architectural insights
3. Create HUMAN_TODO.md entry if manual intervention needed

## Integration with Other Skills

### With `constraint-preflight`
**When:** Adding new constraints that affect schedule generation
**Workflow:**
1. Create and register constraint using constraint-preflight
2. Test impact with schedule-optimization
3. Tune weight based on solver performance
4. Document in both skill files

### With `acgme-compliance`
**When:** Ensuring generated schedules meet regulatory requirements
**Workflow:**
1. Generate schedule with schedule-optimization
2. Invoke acgme-compliance for validation
3. If violations found, adjust constraints and re-solve
4. Repeat until compliant

### With `swap-management`
**When:** Optimizing existing schedule after swaps
**Workflow:**
1. Swaps executed via swap-management
2. Check if swaps degraded fairness metrics
3. If yes, invoke schedule-optimization to rebalance
4. Generate minimal-disruption adjustments

### With `resilience-dashboard`
**When:** Ensuring schedule maintains backup capacity
**Workflow:**
1. Generate schedule with schedule-optimization
2. Invoke resilience-dashboard to check N-1 contingency
3. If resilience inadequate, adjust constraints (lower utilization target)
4. Re-solve with resilience-aware constraints

### With `systematic-debugger`
**When:** Solver producing unexpected results
**Workflow:**
1. Notice issue (e.g., all residents on same rotation)
2. Invoke systematic-debugger to explore
3. Identify root cause (e.g., template filtering)
4. Fix and document in both skill files
5. Re-test with schedule-optimization
