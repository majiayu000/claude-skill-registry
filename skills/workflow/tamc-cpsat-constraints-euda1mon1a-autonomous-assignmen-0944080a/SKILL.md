---
name: tamc-cpsat-constraints
description: "CP-SAT constraint model for TAMC Family Medicine scheduling optimization. Use when building or debugging the OR-Tools solver for faculty/resident scheduling. Documents hard constraints, soft constraints, decision variables, and objective functions."
audience: coworker
version: "1.2"
last_updated: "2026-01-14"
---

# TAMC Scheduling CP-SAT Constraint Model

Reference for the Google OR-Tools CP-SAT solver implementation for faculty and call scheduling.

## Architecture Note

**Excel is the communication layer; CP-SAT is the engine.** Excel provides the configuration (who's available, what rotations, constraints), and the solver optimizes within those constraints. The code has "more nitty gritty" logic than what Excel shows.

## Build Order

The solver should process in this order:
1. **Preload phase** - Lock FMIT, leave, conferences, holidays
2. **Call assignment** - Distribute with equity tracking
3. **Resident schedules** - Apply rotation patterns
4. **Faculty C/AT** - Fill remaining slots
5. **Admin time** - GME/DFM for remaining faculty slots

## Architecture Overview

```
1. PRELOAD phase: Lock non-negotiable assignments
2. SOLVE phase: CP-SAT optimizes remaining slots
3. VALIDATE phase: Verify all constraints satisfied
```

## Decision Variables

### Faculty Schedule Variables
```python
# For each faculty f, day d, slot s (AM/PM):
faculty_assigned[f, d, s] = model.NewBoolVar(f'fac_{f}_{d}_{s}')

# Assignment type (mutually exclusive)
is_clinic[f, d, s] = model.NewBoolVar(f'clinic_{f}_{d}_{s}')
is_admin[f, d, s] = model.NewBoolVar(f'admin_{f}_{d}_{s}')  # GME or DFM
is_sm[f, d, s] = model.NewBoolVar(f'sm_{f}_{d}_{s}')  # Tagawa only
```

### Call Variables
```python
# For each faculty f, night n:
on_call[f, n] = model.NewBoolVar(f'call_{f}_{n}')

# Post-call blocking
post_call_am[f, d] = model.NewBoolVar(f'pcat_{f}_{d}')
post_call_pm[f, d] = model.NewBoolVar(f'do_{f}_{d}')
```

### Auxiliary Variables
```python
# Weekly clinic counts (for cap enforcement)
weekly_clinic_count[f, w] = model.NewIntVar(0, MAX_CLINIC, f'wk_clinic_{f}_{w}')

# Sunday call counts (for equity)
sunday_call_count[f] = model.NewIntVar(0, 4, f'sun_call_{f}')
weekday_call_count[f] = model.NewIntVar(0, 20, f'wd_call_{f}')
```

---

## Hard Constraints

### 0. ACGME Supervision Ratios (HIGHEST PRIORITY - CANNOT VIOLATE)

**This constraint takes precedence over ALL others. ACGME minimum supervision.**

```python
# AT demand per resident type
AT_DEMAND = {
    'PGY1': 0.5,   # Interns need more supervision
    'PGY2': 0.25,
    'PGY3': 0.25,
    'PROC': 1.0,   # Procedures = dedicated AT
    'VAS': 1.0,    # Vascular = dedicated AT
}

# Codes that count as AT coverage
AT_COVERAGE_CODES = {'C', 'PCAT', 'CV'}  # Clinic, Post-Call Admin, Virtual

for day in DAYS:
    for slot in [AM, PM]:
        # Calculate demand
        demand = 0
        for resident in RESIDENTS:
            if resident_in_clinic(resident, day, slot):
                demand += AT_DEMAND[resident.pgy_level]
            if resident_in_proc(resident, day, slot):
                demand += AT_DEMAND['PROC']

        # Round up - can't have half a faculty
        demand_rounded = math.ceil(demand)

        # Count coverage
        coverage = sum(
            1 for f in FACULTY
            if faculty_assignment[f, day, slot] in AT_COVERAGE_CODES
        )

        # HARD CONSTRAINT: coverage >= demand
        model.Add(coverage >= demand_rounded)
```

**This constraint is NON-NEGOTIABLE. If it cannot be satisfied, the schedule is INVALID.**

#### Balancing AT: Two-Way Optimization

AT compliance is an equation: `Coverage >= Demand`

The solver can satisfy this by:
1. **Increasing coverage** - Assign more faculty C/PCAT
2. **Decreasing demand** - Reduce resident clinic load

```python
# Resident clinic assignment is a DECISION VARIABLE, not fixed
resident_in_clinic[r, day, slot] = model.NewBoolVar(...)

# Can move residents C -> ADM to reduce demand
# PROC -> C reduces demand by 0.75 (1.0 -> 0.25)

# Soft constraint: prefer residents in clinic (educational value)
# But AT compliance is HARD - will pull residents if needed
model.Minimize(
    ... +
    10 * sum(not_in_clinic_penalty[r, d, s] for r, d, s in ...)
)
```

**Priority order:**
1. ACGME AT compliance (HARD - cannot violate)
2. Faculty weekly caps (soft - can exceed if needed)
3. Resident clinic time (soft - educational preference)
4. GME/admin preferences (soft - fill remaining)

### 1. Weekly Clinic Caps (C only, NOT AT)
```python
# IMPORTANT: Caps apply to C (Clinic), NOT AT (Attending)
# C = Faculty seeing OWN patients → has MIN and MAX
# AT = Faculty supervising residents → NO cap (unlimited)

for faculty in FACULTY:
    for week in WEEKS:
        c_count = sum(is_clinic[faculty, d, s]
                      for d in week_days(week)
                      for s in [AM, PM])

        # MAX constraint (hard)
        model.Add(c_count <= faculty.max_clinic_per_week)

        # MIN constraint (hard - WARN if cannot meet)
        model.Add(c_count >= faculty.min_clinic_per_week)
```

**Faculty C caps (MIN and MAX per week):**
| Faculty | MIN C/week | MAX C/week | AT? |
|---------|------------|------------|-----|
| Kinkennon | 2 | 4 | Unlimited |
| LaBounty | 2 | 4 | Unlimited |
| McRae | 2 | 4 | Unlimited |
| Montgomery | 2 | 2 | Unlimited |
| Lamoureux | 2 | 2 | Unlimited |
| McGuire | 1 | 1 | Unlimited |
| Tagawa | 0 (SM only) | 0 | Can do AT when not on SM |
| Bevis, Dahl, Chu, Napierala, Van Brunt, Colgan | 0 | 0 | N/A |

**If MIN cannot be met:** WARN - flag for PD review (conflicts with other constraints)

### 2. FMIT Blocking
```python
for faculty in FACULTY:
    for day in faculty.fmit_days:
        # Cannot take clinic during FMIT
        model.Add(is_clinic[faculty, day, AM] == 0)
        model.Add(is_clinic[faculty, day, PM] == 0)

        # Cannot take Sun-Thu call during FMIT week
        if day.is_weekday or day.is_sunday:
            model.Add(on_call[faculty, day] == 0)
```

### 3. Post-Call PCAT/DO
```python
for faculty in FACULTY:
    for night in NIGHTS:
        if not is_fmit_call(faculty, night):
            next_day = night + 1
            # If on call, next day must be PCAT/DO
            model.Add(post_call_am[faculty, next_day] >= on_call[faculty, night])
            model.Add(post_call_pm[faculty, next_day] >= on_call[faculty, night])

            # PCAT/DO blocks clinic
            model.Add(is_clinic[faculty, next_day, AM] + post_call_am[faculty, next_day] <= 1)
            model.Add(is_clinic[faculty, next_day, PM] + post_call_pm[faculty, next_day] <= 1)
```

### 4. FMIT Call Coverage
```python
# FMIT week structure: Friday (start) -> Thursday (end)
# FMIT faculty covers Friday and Saturday call (first 2 nights of FMIT)
# PC = Friday after FMIT ends (day off)

for faculty in FACULTY:
    for fmit_start in faculty.fmit_fridays:  # Friday is FMIT start day
        # FMIT faculty must cover Fri/Sat call
        model.Add(on_call[faculty, fmit_start] == 1)  # Friday
        model.Add(on_call[faculty, fmit_start + 1] == 1)  # Saturday

        # Cannot be on call Sun-Thu during FMIT (on inpatient service)
        for day_offset in range(2, 7):  # Sun=+2, Mon=+3, ..., Thu=+6
            model.Add(on_call[faculty, fmit_start + day_offset] == 0)

        # PC on Friday after (day 7 from FMIT start)
        pc_friday = fmit_start + 7
        model.Add(assignment[faculty, pc_friday, AM] == 'PC')
        model.Add(assignment[faculty, pc_friday, PM] == 'PC')

        # Cannot be on call Saturday after FMIT (recovery, day 8)
        model.Add(on_call[faculty, fmit_start + 8] == 0)
```

### 5. No Back-to-Back Call (HARD CONSTRAINT)
```python
# Faculty cannot have call on consecutive days - need gap days
# Example: Call on Mar 15 AND Mar 17 (1 day gap) = INVALID
# Example: Call on Mar 15 AND Mar 19 (3 day gap) = VALID

for faculty in FACULTY:
    for night in NIGHTS[:-1]:
        # No consecutive nights
        model.Add(on_call[faculty, night] + on_call[faculty, night + 1] <= 1)

    # Extended gap rule: prefer at least 2 days between calls
    for night in NIGHTS[:-2]:
        # Soft constraint: penalize 1-day gaps
        one_day_gap = model.NewBoolVar(f'gap1_{faculty}_{night}')
        model.Add(on_call[faculty, night] + on_call[faculty, night + 2] <= 1 + one_day_gap)
        # Add penalty to objective
```

### 6. One Faculty Per Call Night
```python
for night in NIGHTS:
    model.Add(sum(on_call[f, night] for f in CALL_ELIGIBLE) == 1)
```

### 7. SM Requires Tagawa
```python
TAGAWA = get_faculty('Tagawa')
for day in DAYS:
    for slot in [AM, PM]:
        # If any resident has SM, Tagawa must have SM
        resident_sm = sum(resident_is_sm[r, day, slot] for r in SM_RESIDENTS)
        model.Add(is_sm[TAGAWA, day, slot] >= resident_sm)

        # If Tagawa blocked, no resident can have SM
        if tagawa_blocked(day, slot):
            for r in SM_RESIDENTS:
                model.Add(resident_is_sm[r, day, slot] == 0)
```

### 8. Physical Clinic Capacity (Max 6 Clinical Workers)
```python
# Staffing constraint: max 6 people doing clinical work per half-day
# AT (supervision) does NOT count - they precept, don't generate patients

CLINICAL_CODES = {'C', 'CV', 'PR', 'VAS'}  # Codes that generate patient load

for day in DAYS:
    for slot in [AM, PM]:
        # Count residents doing clinical work
        resident_clinical = sum(
            1 for r in RESIDENTS
            if resident_assignment[r, day, slot] in CLINICAL_CODES
        )

        # Count faculty doing clinic (not AT supervision)
        faculty_clinical = sum(
            is_clinic[f, day, slot] for f in FACULTY
        )

        # HARD CONSTRAINT: total clinical workers <= 6
        model.Add(resident_clinical + faculty_clinical <= 6)
```

**Note:** This constraint is due to staffing limitations (MAs, check-in, etc.). More than 6 providers generating patients overwhelms support staff.

### 9. Intern Continuity Clinic (Wednesday AM)
```python
# HARD CONSTRAINT: PGY-1 interns have Continuity Clinic on Wednesday mornings
# This is protected time for panel patients - cannot be moved

WED_AM_COLS = [18, 32, 46, 60]  # Wednesday AM columns in Block Template2

for intern in PGY1_RESIDENTS:
    for wed_am_col in WED_AM_COLS:
        rotation = get_rotation(intern, wed_am_col)

        # Exceptions - these rotations don't have Wed AM clinic
        if rotation in ['NF', 'Peds NF', 'Hilo', 'Kapiolani L and D', 'OB', 'Transitional']:
            continue  # Use rotation-specific code

        # All other PGY-1 rotations → Continuity Clinic
        model.Add(resident_assignment[intern, wed_am_col] == CLINIC_CODE)
```

**Intern clinic codes by experience level:**
| Block Range | Code | Appointment Length |
|-------------|------|-------------------|
| Block 1-6 | C60 | 60 minutes (new intern) |
| Block 7-13 | C40 | 40 minutes (experienced) |
| ER rotation | C30 | 30 minutes |

**Senior residents (PGY-2/3) do NOT have this constraint** - their Wed AM varies by rotation.

### 10. Night Float Timing
```python
# Night Float Structure:
# - Starts: Thursday
# - Ends: Wednesday (following week)
# - Post-call: Thursday after (inter-block day)
# - C-N code: Thursday PM for oncoming NF (preserves continuity)

for resident in NF_RESIDENTS:
    nf_start_day = resident.nf_start_date  # Must be Thursday
    assert nf_start_day.weekday() == THURSDAY

    # Thursday PM: C-N (oncoming clinic)
    model.Add(resident_assignment[resident, nf_start_day, PM] == 'C-N')

    # Friday through Wednesday: NF pattern (OFF AM, NF PM)
    for day_offset in range(1, 7):  # Fri=1, Sat=2, ..., Wed=6
        day = nf_start_day + day_offset
        model.Add(resident_assignment[resident, day, AM] == 'OFF')
        model.Add(resident_assignment[resident, day, PM] == 'NF')

    # Thursday after: POST-CALL (inter-block)
    post_call_day = nf_start_day + 7
    model.Add(resident_assignment[resident, post_call_day, AM] == 'OFF')
    model.Add(resident_assignment[resident, post_call_day, PM] == 'OFF')
```

### 11. Last Wednesday of Block
```python
# Final Wednesday has special rules - NO morning clinic
# AM: Lecture (LEC)
# PM: Advising (ADV)

LAST_WED_COL = 60  # Apr 8 AM in Block 10

for resident in RESIDENTS:
    # AM = LEC (protected)
    model.Add(resident_assignment[resident, LAST_WED_COL] == 'LEC')
    # PM = ADV
    model.Add(resident_assignment[resident, LAST_WED_COL + 1] == 'ADV')
```

### 12. IM Rotation Last Wednesday Exception
```python
# IM residents get Tuesday PM clinic instead of final Wednesday
# Preserves 4 weeks of continuity (otherwise only 3)

for resident in IM_RESIDENTS:
    last_tue_pm = get_last_tuesday_pm(resident.rotation_end)

    # Move clinic from Wed to Tue PM
    model.Add(resident_assignment[resident, last_tue_pm] == 'C')

    # Last Wed follows standard Last Wednesday rules (LEC/ADV)
```

### 13. Resident Clinic Caps
```python
# Clinic caps by PGY level (per week)
CLINIC_CAPS = {
    'PGY1': (1, 2),   # min=1, max=2 (ideally 1)
    'PGY2': (2, 3),   # min=2, max=3
    'PGY3': (3, 4),   # min=3, max=4
}

# R2 on Sports Med: max 3 (hard cap)
for resident in R2_ON_SM:
    for week in WEEKS:
        clinic_count = sum(
            resident_in_clinic[resident, d, s]
            for d in week_days(week)
            for s in [AM, PM]
        )
        model.Add(clinic_count <= 3)

# Flex time requirements
FLEX_REQUIRED = {
    'PGY1': 2,  # 2 half-days FLX
    'PGY2': 1,  # 1 half-day FLX
    'PGY3': 1,  # At least 1 half-day FLX (FMC)
}
```

### 14. Kapiolani L&D Schedule (Intern)
```python
# Kapiolani is off-site L&D for interns
# Special schedule: Mon PM-Tue OFF, Wed AM clinic, Thu-Sun KAP

for intern in KAP_INTERNS:
    for week in WEEKS:
        mon = get_monday(week)

        # Mon PM through Tue: OFF (travel/recovery)
        model.Add(resident_assignment[intern, mon, PM] == 'OFF')
        model.Add(resident_assignment[intern, mon + 1, AM] == 'OFF')  # Tue AM
        model.Add(resident_assignment[intern, mon + 1, PM] == 'OFF')  # Tue PM

        # Wed AM: Continuity clinic (NOT KAP)
        model.Add(resident_assignment[intern, mon + 2, AM] == 'C')

        # Thu-Sun: KAP (4 shifts)
        for day_offset in range(3, 7):  # Thu=3, Fri=4, Sat=5, Sun=6
            day = mon + day_offset
            model.Add(resident_assignment[intern, day, AM] == 'KAP')
            model.Add(resident_assignment[intern, day, PM] == 'KAP')
```

### 15. L&D Night Float (R2)
```python
# R2 L&D nights have FRIDAY morning clinic (not Wednesday!)

for r2 in LDNF_RESIDENTS:
    for week in WEEKS:
        fri = get_friday(week)

        # Friday AM: Clinic
        model.Add(resident_assignment[r2, fri, AM] == 'C')
        # Friday PM: OFF
        model.Add(resident_assignment[r2, fri, PM] == 'OFF')

        # Mon-Thu: OFF AM, LDNF PM
        for day in [get_monday(week), get_tuesday(week), get_wednesday(week), get_thursday(week)]:
            model.Add(resident_assignment[r2, day, AM] == 'OFF')
            model.Add(resident_assignment[r2, day, PM] == 'LDNF')
```

### 16. Houseless Clinic (HLC) and CLC
```python
# HLC: Monday PM for R2/R3 only
# One resident per slot, every Monday

MONDAY_PM_COLS = [15, 29, 43, 57]  # Monday PM columns

for mon_pm in MONDAY_PM_COLS:
    # Exactly one R2/R3 assigned HLC
    hlc_assigned = [
        resident_assignment[r, mon_pm] == 'HLC'
        for r in R2_R3_RESIDENTS
    ]
    model.Add(sum(hlc_assigned) == 1)

# CLC: Thursday PM, weeks 2 and 4 (NOT back-to-back)
# 2nd Thursday PM and 4th Thursday PM
WEEK2_THU_PM = 21  # Mar 19 PM
WEEK4_THU_PM = 49  # Apr 2 PM

for thu_pm in [WEEK2_THU_PM, WEEK4_THU_PM]:
    # Residents scheduled for CLC
    for r in CLC_ELIGIBLE_RESIDENTS:
        model.Add(resident_assignment[r, thu_pm] == 'CLC')
```

### 17. Faculty Weekly Target Distribution
```python
# Target: 10 half-days/week per faculty
# 3 C + 2-3 GME + 3-4 AT + 1 PCAT/DO (if call)

WEEKLY_TARGETS = {
    'C': (2, 4),      # MIN 2, MAX 4 (faculty-specific caps override)
    'GME': (2, 3),    # Admin time
    'AT': (3, 4),     # Supervision (soft target, no cap)
    'PCAT_DO': (0, 1) # Only if took call
}

# Soft constraint: prefer full-day C (AM+PM same day)
for faculty in FACULTY:
    for day in WEEKDAYS:
        am_clinic = is_clinic[faculty, day, AM]
        pm_clinic = is_clinic[faculty, day, PM]

        # Penalize split days (only one half has C)
        split_penalty = model.NewBoolVar(f'split_{faculty}_{day}')
        # XOR detection: exactly one is true
        model.Add(am_clinic + pm_clinic == 1).OnlyEnforceIf(split_penalty)

# Add to objective with small weight
model.Minimize(... + 1 * sum(split_penalties))
```

### 18. Preloaded Slots Locked
```python
for (faculty, day, slot, code) in PRELOADED:
    if code == 'FMIT':
        model.Add(is_fmit[faculty, day, slot] == 1)
    elif code == 'LV':
        model.Add(is_leave[faculty, day, slot] == 1)
    elif code == 'PC':
        model.Add(is_post_fmit[faculty, day, slot] == 1)
    # ... etc
```

---

## Soft Constraints / Objectives

### 1. Call Equity (Primary)
```python
# Minimize variance in call counts
max_call = model.NewIntVar(0, 30, 'max_call')
min_call = model.NewIntVar(0, 30, 'min_call')

for faculty in CALL_ELIGIBLE:
    total_call = sum(on_call[faculty, n] for n in NIGHTS)
    model.Add(max_call >= total_call)
    model.Add(min_call <= total_call)

# Objective: minimize spread
model.Minimize(max_call - min_call)
```

### 2. Sunday Equity (Secondary)
```python
# Track Sunday calls separately
max_sunday = model.NewIntVar(0, 4, 'max_sun')
min_sunday = model.NewIntVar(0, 4, 'min_sun')

for faculty in CALL_ELIGIBLE:
    sun_calls = sum(on_call[faculty, n] for n in SUNDAY_NIGHTS)
    model.Add(max_sunday >= sun_calls)
    model.Add(min_sunday <= sun_calls)

# Add to objective with weight
model.Minimize(
    10 * (max_call - min_call) +  # Weekday equity
    5 * (max_sunday - min_sunday)  # Sunday equity
)
```

### 3. Tagawa SM Target (3-4/week)
```python
TAGAWA = get_faculty('Tagawa')
for week in WEEKS:
    sm_count = sum(is_sm[TAGAWA, d, AM] for d in week_days(week))

    # Soft constraint: penalize deviation from 3-4
    under_target = model.NewIntVar(0, 3, f'sm_under_{week}')
    over_target = model.NewIntVar(0, 4, f'sm_over_{week}')

    model.Add(sm_count + under_target >= 3)
    model.Add(sm_count - over_target <= 4)

# Add penalty to objective
model.Minimize(
    ... +
    2 * sum(under_target[w] + over_target[w] for w in WEEKS)
)
```

### 4. AT Coverage Balance
```python
# Aim for consistent clinic coverage across days
for day in WEEKDAYS:
    clinic_count = sum(is_clinic[f, day, s] for f in FACULTY for s in [AM, PM])

    # Penalize deviation from target
    target = AT_DEMAND[day]
    deviation = model.NewIntVar(0, 10, f'at_dev_{day}')
    model.Add(clinic_count - target <= deviation)
    model.Add(target - clinic_count <= deviation)

model.Minimize(... + sum(deviation[d] for d in WEEKDAYS))
```

### 5. Full-Day Clinic Preference
```python
# Faculty prefer full-day clinic (C AM + C PM) over split days
# This also increases chances of getting full-day GME

for faculty in FACULTY:
    for day in WEEKDAYS:
        # Penalty for having clinic in only one half
        has_am_clinic = is_clinic[faculty, day, AM]
        has_pm_clinic = is_clinic[faculty, day, PM]

        # XOR: penalty when exactly one is true
        split_day = model.NewBoolVar(f'split_{faculty}_{day}')
        model.Add(has_am_clinic + has_pm_clinic - 2 * split_day <= 1)
        model.Add(has_am_clinic + has_pm_clinic - 2 * split_day >= 0)

# Add to objective with small weight (soft preference)
model.Minimize(
    ... +
    1 * sum(split_day[f, d] for f in FACULTY for d in WEEKDAYS)
)
```

---

## Special Faculty Rules (Encoded as Constraints)

### Chu (Week-on/Week-off FMIT)
```python
CHU = get_faculty('Chu')
for week in CHU.off_weeks:
    # No Sun-Thu call during off weeks
    for night in week_nights(week):
        if night.day_of_week in [SUN, MON, TUE, WED, THU]:
            model.Add(on_call[CHU, night] == 0)

# Not immediately available after FMIT
for fmit_end in CHU.fmit_end_dates:
    for day in range(fmit_end + 1, fmit_end + 3):  # Skip 2 days
        model.Add(on_call[CHU, day] == 0)
```

### Bevis (Post-FMIT Availability)
```python
BEVIS = get_faculty('Bevis')
# Available starting next week after FMIT
fmit_end_week = get_week(BEVIS.fmit_end_date)
for night in NIGHTS:
    if get_week(night) <= fmit_end_week:
        model.Add(on_call[BEVIS, night] == 0)
```

### LaBounty (Pre-FMIT Restriction)
```python
LABOUNTY = get_faculty('LaBounty')
fmit_start_week = get_week(LABOUNTY.fmit_start_date)
# No call in week immediately before FMIT
for night in NIGHTS:
    if get_week(night) == fmit_start_week - 1:
        model.Add(on_call[LABOUNTY, night] == 0)
```

---

## Preload Phase

Before solving, lock these codes:
```python
PRELOAD_CODES = {
    'FMIT',   # FM Inpatient Team
    'LV',     # Leave
    'W',      # Weekend (in schedule, not call)
    'PC',     # Post-FMIT Friday
    'LEC',    # Lecture (Wed PM)
    'SIM',    # Simulation
    'HAFP',   # Hawaii AFP conference
    'USAFP',  # USAFP conference
    'BLS',    # BLS training
    'DEP',    # Deployed
    'PI',     # Process Improvement
    'MM',     # M&M conference
    'HOL',    # Holiday
    'TDY',    # Temporary Duty (residents)
}
```

---

## Solver Configuration

```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# Time limit
solver.parameters.max_time_in_seconds = 60.0

# Parallelism
solver.parameters.num_search_workers = 8

# Solution callback for progress
class SolutionCallback(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self):
        print(f'Solution {self.solution_count}: obj={self.ObjectiveValue()}')

status = solver.Solve(model, SolutionCallback())

if status == cp_model.OPTIMAL:
    print('Optimal solution found')
elif status == cp_model.FEASIBLE:
    print('Feasible solution found (may not be optimal)')
else:
    print('No solution found')
```

---

## Validation Checklist

After solving, verify:
- [ ] **ACGME supervision ratios satisfied (HIGHEST PRIORITY)**
- [ ] No faculty exceeds weekly clinic cap (MIN and MAX)
- [ ] All call nights have exactly one faculty assigned
- [ ] PCAT/DO applied for all non-FMIT call
- [ ] No back-to-back call for any faculty (need gap days)
- [ ] SM slots have both Tagawa and resident
- [ ] FMIT faculty not on Sun-Thu call
- [ ] Sunday call distributed (max 1-2 per faculty)
- [ ] **Physical clinic capacity ≤6 per slot**
- [ ] **PGY-1 interns have Continuity Clinic on Wednesday AM**
- [ ] Preloaded codes not overwritten
- [ ] **Night float: starts Thursday, ends Wednesday, C-N on oncoming day**
- [ ] **Last Wednesday: AM=LEC, PM=ADV (no morning clinic)**
- [ ] **IM rotation: Tuesday PM clinic instead of final Wednesday**
- [ ] **R2 clinic caps: max 3 per week**
- [ ] **HLC assigned Monday PM (one R2/R3)**
- [ ] **CLC on 2nd and 4th Thursday PM**
- [ ] **Flex time requirements met by PGY level**
- [ ] **Kapiolani interns: Wed AM clinic, Mon PM-Tue OFF, Thu-Sun KAP**
- [ ] **L&D NF (R2): Friday AM clinic (not Wednesday!)**
- [ ] **Faculty full-day C preferred (AM+PM same day)**

---

## Integration with Excel

```python
from openpyxl import load_workbook

def apply_solution_to_excel(solver, variables, workbook_path):
    wb = load_workbook(workbook_path)
    sheet = wb['Block Template2']

    for (faculty, day, slot), var in variables.items():
        if solver.Value(var):
            row = FACULTY_ROWS[faculty]
            col = day_slot_to_col(day, slot)

            if solver.Value(is_clinic[faculty, day, slot]):
                sheet.cell(row=row, column=col).value = 'C'
            elif solver.Value(is_sm[faculty, day, slot]):
                sheet.cell(row=row, column=col).value = 'SM'
            # ... etc

    # Apply call assignments
    for (faculty, night), var in on_call.items():
        if solver.Value(var):
            col = night_to_col(night)
            sheet.cell(row=4, column=col).value = faculty.upper()

    wb.save(workbook_path)
```
