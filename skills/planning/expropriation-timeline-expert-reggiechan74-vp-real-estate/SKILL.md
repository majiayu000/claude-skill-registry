---
name: expropriation-timeline-expert
description: Expert in calculating critical path project timelines using PERT/CPM methodology with statutory deadline integration for expropriation projects. Use when managing complex project schedules, tracking OEA statutory deadlines (3-month registration, Form 2/7 service), identifying timeline risks, or optimizing resource allocation. Key terms include critical path, PERT analysis, CPM scheduling, statutory deadlines, float analysis, resource leveling
tags: [critical-path, pert-cpm, project-management, statutory-deadlines, timeline-analysis, resource-planning]
capability: Provides comprehensive project timeline analysis including critical path method (CPM), PERT time estimates (optimistic/most_likely/pessimistic), statutory deadline tracking (OEA s.9, s.11), risk assessment (deadline compliance, zero float), resource requirements calculation, dependency analysis, and Gantt visualization
proactive: true
---

You are an expert in calculating critical path project timelines using PERT/CPM (Program Evaluation and Review Technique / Critical Path Method) methodology with integration of statutory deadlines for expropriation projects.

## Granular Focus

Project timeline calculation and critical path analysis (complementary to deadline tracking). This skill provides quantitative schedule analysis - NOT operational deadline monitoring.

## When to Use This Skill

Use this skill when you need to:

1. **Calculate project duration** using critical path method (CPM)
2. **Identify critical path tasks** (zero float tasks that drive project duration)
3. **Perform PERT analysis** (optimistic/most_likely/pessimistic time estimates)
4. **Assess timeline risks** (statutory deadline compliance, float analysis)
5. **Calculate resource requirements** (staff, consultants, budget by phase)
6. **Optimize project schedule** (identify bottlenecks, dependency chains)
7. **Generate Gantt charts** for visualization and communication

## Critical Path Method (CPM) Fundamentals

### What is Critical Path?

**Critical path**: Longest sequence of dependent tasks that determines minimum project duration.

**Critical tasks**: Tasks with zero total float (any delay directly extends project completion).

**Total float**: Amount of time a task can be delayed without extending project duration.
- **Critical path tasks**: Total float = 0 days
- **Non-critical tasks**: Total float > 0 days (schedule flexibility)

**Free float**: Amount of time a task can be delayed without delaying any successor.

### Forward Pass & Backward Pass

**Forward pass**: Calculate earliest start/finish times
1. Start with day 0
2. Early start = max(predecessor early finishes)
3. Early finish = early start + duration

**Backward pass**: Calculate latest start/finish times
1. Start with project end date
2. Late finish = min(successor late starts)
3. Late start = late finish - duration

**Float calculation**:
- Total float = late start - early start (or late finish - early finish)
- Free float = min(successor early starts) - early finish

### Example Calculation

**Tasks**:
- A: Duration 10 days (no predecessors)
- B: Duration 20 days (after A)
- C: Duration 15 days (after A)
- D: Duration 5 days (after B and C)

**Forward pass**:
- A: ES=0, EF=10
- B: ES=10, EF=30
- C: ES=10, EF=25
- D: ES=30 (max of B and C), EF=35

**Backward pass**:
- D: LS=30, LF=35
- B: LS=10, LF=30
- C: LS=15, LF=30
- A: LS=0, LF=10

**Float**:
- A: 0 (critical)
- B: 0 (critical)
- C: 5 days (LS 15 - ES 10)
- D: 0 (critical)

**Critical path**: A → B → D (35 days)

## PERT Analysis

### Three-Point Estimates

**PERT uses three time estimates** to account for uncertainty:

1. **Optimistic (O)**: Best-case scenario (everything goes perfectly)
2. **Most Likely (M)**: Realistic scenario (normal conditions)
3. **Pessimistic (P)**: Worst-case scenario (significant problems)

### PERT Formulas

**Expected time (weighted average)**:
```
TE = (O + 4M + P) / 6
```

**Standard deviation**:
```
σ = (P - O) / 6
```

**Variance**:
```
σ² = ((P - O) / 6)²
```

**Project variance** (sum of critical path task variances):
```
Project σ² = Σ(critical path task variances)
```

**Project standard deviation**:
```
Project σ = √(Project σ²)
```

### Confidence Intervals

**90% confidence interval** (Z = 1.645):
```
Lower bound = Expected duration - 1.645 × Project σ
Upper bound = Expected duration + 1.645 × Project σ
```

**95% confidence interval** (Z = 1.960):
```
Lower bound = Expected duration - 1.960 × Project σ
Upper bound = Expected duration + 1.960 × Project σ
```

### Example PERT Calculation

**Task**: Prepare expropriation plan
- Optimistic: 14 days
- Most Likely: 21 days
- Pessimistic: 35 days

**Expected time**:
```
TE = (14 + 4×21 + 35) / 6 = (14 + 84 + 35) / 6 = 133 / 6 = 22.2 days
```

**Standard deviation**:
```
σ = (35 - 14) / 6 = 21 / 6 = 3.5 days
```

**Variance**:
```
σ² = 3.5² = 12.25
```

**Interpretation**: Task will take approximately 22 days, with ±3.5 days variability.

## Integration with OEA Statutory Deadlines

### Statutory Deadline Constraints

**3-Month Registration Deadline (OEA s.9(2))**:
- Expropriation plan must be registered within 90 days of approval
- Deadline is **absolute** (approval expires if missed)
- Critical path must complete plan registration by day 85 (5-day buffer)

**Form 2 Service (Best Practice)**:
- Serve Notice of Application 30 days before registration
- Not statutory, but reduces procedural challenges

**Form 7 Service (OEA s.11)**:
- Serve Notice of Expropriation at least 30 days before possession
- Statutory minimum (can give more time)

### Deadline Risk Assessment

**Buffer analysis**:
```
Buffer = Statutory deadline - Task late finish
```

**Risk levels**:
- **CRITICAL**: Buffer < 0 (task finishes AFTER deadline)
- **HIGH**: Buffer 0-5 days (insufficient buffer)
- **MEDIUM**: Buffer 5-10 days (below minimum buffer)
- **LOW**: Buffer > 10 days (adequate buffer)

**Example**:
- Statutory deadline: Day 90 (registration)
- Task late finish: Day 91 (plan registration)
- Buffer: 90 - 91 = **-1 day** (CRITICAL risk - misses deadline)

## Calculator Usage

### Input Format

**JSON input structure**:
```json
{
  "project_name": "Transit Station Property Acquisition",
  "approval_date": "2025-03-15",
  "tasks": [
    {
      "id": "A",
      "name": "Obtain approval",
      "duration": 30,
      "optimistic": 20,
      "most_likely": 30,
      "pessimistic": 45,
      "resources": {
        "staff": 2,
        "consultants": {"legal": 1},
        "budget": 15000
      }
    }
  ],
  "dependencies": [
    ["A", "B"]
  ],
  "statutory_deadlines": {
    "G": 90
  },
  "buffer_days": 10
}
```

### Command Line Usage

**Basic calculation**:
```bash
python project_timeline_calculator.py sample_1_simple_acquisition.json
```

**Specify output location**:
```bash
python project_timeline_calculator.py input.json -o Reports/timeline_analysis.md
```

**JSON output format**:
```bash
python project_timeline_calculator.py input.json -f json -o results.json
```

**Verbose output**:
```bash
python project_timeline_calculator.py input.json -v
```

### Output Report

**Markdown report includes**:
1. **Executive Summary**: Project duration, critical path percentage, risk summary
2. **Critical Path Analysis**: Sequence of critical tasks with schedule
3. **Statutory Deadlines**: OEA milestone dates and compliance status
4. **Risk Assessment**: Timeline risks by severity (critical/high/medium/low)
5. **Task Details Table**: All tasks with early/late dates, float, criticality
6. **Gantt Chart**: Text-based visualization of timeline
7. **Resource Requirements**: Total and peak resource needs
8. **Dependency Analysis**: Complexity metrics and bottleneck identification

## Resource Requirements Analysis

### Resource Calculation

**For each task**, specify:
- **Staff**: Number of staff required (concurrent)
- **Consultants**: Number by type (legal, surveyor, appraiser, etc.)
- **Budget**: Cost allocated to task

**Calculator computes**:
- **Total staff-days**: Σ(staff × duration)
- **Total consultant-days**: Σ(consultants × duration) by type
- **Total budget**: Σ(task budgets)
- **Peak resources**: Maximum concurrent staff/consultants at any point

### Resource Leveling

**Identify resource bottlenecks**:
1. Tasks with peak resource requirements (> 5 concurrent staff)
2. Critical path tasks with high resource needs (no flexibility)
3. Resource conflicts (multiple tasks requiring same consultant)

**Mitigation strategies**:
- Delay non-critical tasks (use available float)
- Increase resources during peak periods
- Outsource specialist work (appraisals, surveys)

## Dependency Analysis

### Dependency Complexity Metrics

**Total dependencies**: Number of predecessor-successor relationships

**Average dependencies per task**: Total dependencies ÷ Total tasks
- **Simple project**: < 1.5 dependencies/task
- **Moderate complexity**: 1.5 - 2.5 dependencies/task
- **High complexity**: > 2.5 dependencies/task

**Dependency density**: Total dependencies ÷ (Total tasks)²
- Measures interconnectedness
- Higher density = more complex, rigid schedule

**Bottleneck tasks**: Tasks with 3+ dependencies (predecessors or successors)
- High risk: Any delay cascades through project
- Monitor closely, allocate extra resources

### Dependency Types

**Finish-to-Start (FS)**: Successor starts after predecessor finishes
- **Example**: "Prepare plan" → "Review plan"
- Most common dependency type

**Start-to-Start (SS)**: Tasks start together
- **Example**: "Negotiation" starts when "Appraisal" starts
- Used for parallel work streams

**Finish-to-Finish (FF)**: Tasks finish together
- **Example**: "Legal review" finishes when "Plan preparation" finishes
- Used for coordinated completions

**Start-to-Finish (SF)**: Rare, successor finishes when predecessor starts
- Uncommon in expropriation projects

**Note**: Current calculator supports Finish-to-Start only. For other types, model as multiple FS dependencies.

## Risk Assessment

### Timeline Risk Categories

**1. Statutory Deadline Risk**:
- Task late finish exceeds statutory deadline
- **Severity**: CRITICAL (approval expires)
- **Mitigation**: Crash critical path, expedite reviews, obtain second approval

**2. Critical Path No-Float Risk**:
- Critical path task with zero schedule flexibility
- **Severity**: MEDIUM
- **Mitigation**: Add buffer time, parallel work streams, increase resources

**3. Long Duration Risk**:
- Task duration > 60 days (potential for unforeseen delays)
- **Severity**: LOW
- **Mitigation**: Break into sub-tasks, weekly monitoring

**4. Dependency Bottleneck Risk**:
- Task with 3+ dependencies (delays cascade)
- **Severity**: MEDIUM
- **Mitigation**: Early coordination, dedicated resources

### Risk Mitigation Strategies

**Crashing the schedule** (reduce critical path duration):
1. Add resources to critical path tasks
2. Work overtime / weekends
3. Outsource work to expedite
4. Fast-track (overlap dependent tasks if possible)

**Fast-tracking**:
- Start successor before predecessor 100% complete
- **Risk**: Rework if predecessor output changes
- **Example**: Start plan review while plan preparation 80% complete

**Buffering**:
- Add contingency time to critical path
- **Project buffer**: 10-15% of critical path duration
- **Feeding buffers**: Protect critical path from non-critical delays

## Worked Example

### Sample Input

**Project**: Transit station property acquisition (see `samples/sample_1_simple_acquisition.json`)

**Key tasks**:
- A: Obtain approval (30 days)
- B: Prepare plan (21 days) - after A
- C: Plan review (7 days) - after B
- D: Corrections (10 days) - after C
- E: Solicitor approval (7 days) - after D
- F: Registry scheduling (15 days) - after E
- G: Plan registration (1 day) - after F
- H: Appraisal (30 days) - after A, parallel to B-G
- I: Prepare Form 2 (5 days) - after A
- J: Serve Form 2 (1 day) - after I

**Statutory deadline**: Task G (registration) must complete by day 90.

### Critical Path Analysis

**Critical path**: A → B → C → D → E → F → G

**Project duration**: 30 + 21 + 7 + 10 + 7 + 15 + 1 = **91 days**

**Problem**: Critical path (91 days) exceeds statutory deadline (90 days) by 1 day!

**Buffer**: 90 - 91 = **-1 day** (CRITICAL risk)

### PERT Analysis

**Task B (Prepare plan)**:
- Optimistic: 14 days
- Most Likely: 21 days
- Pessimistic: 35 days

**Expected time**: (14 + 4×21 + 35) / 6 = 22.2 days (vs. 21 deterministic)

**Standard deviation**: (35 - 14) / 6 = 3.5 days

**Project with PERT estimates**: ~92 days (expected)
- **90% confidence interval**: 86 - 98 days
- **Probability of meeting 90-day deadline**: ~30% (not acceptable)

### Risk Mitigation

**Option 1: Crash critical path**
- Reduce Task B (plan preparation) from 21 → 18 days (add surveyor)
- Reduce Task C (plan review) from 7 → 5 days (priority review)
- **New duration**: 88 days (2-day buffer)

**Option 2: Fast-track**
- Start Task C (review) when Task B is 90% complete (overlap 2 days)
- Start Task F (registry scheduling) during Task E (parallel booking)
- **New duration**: 87 days (3-day buffer)

**Option 3: Parallel work streams**
- Split plan preparation into multiple parcels
- Register parcels as ready (rolling registration)
- **Risk**: Complex coordination, higher legal costs

**Recommended**: Combination of Options 1 and 2 to achieve 85-day completion (5-day buffer).

## Integration with Other Skills

**Complementary skills**:

1. **expropriation-statutory-deadline-tracking**:
   - Operational deadline monitoring (weekly checks, escalation)
   - This skill: Quantitative schedule calculation

2. **expropriation-compensation-entitlement-analysis**:
   - Legal entitlement to compensation components
   - This skill: Timeline for compensation calculation tasks

3. **land-assembly-expert**:
   - Multi-property acquisition strategy
   - This skill: Timeline for land assembly projects

## Automated Workflow

**Calculator follows PDF → JSON → Python → Report pattern**:

1. **Input**: User creates JSON file with tasks, dependencies, deadlines
2. **Validation**: Schema validation ensures data integrity
3. **Calculation**: PERT/CPM analysis computes critical path
4. **Risk Assessment**: Identifies deadline compliance and timeline risks
5. **Output**: Markdown report with Gantt chart, JSON data export

**No manual intervention required** - fully automated from input to report.

## Limitations

**Current implementation**:
- Supports Finish-to-Start (FS) dependencies only
- Assumes deterministic resource availability
- Does not optimize resource allocation (requires manual leveling)
- Weekends/holidays not modeled (calendar days only)

**For advanced features**:
- Use project management software (Microsoft Project, Primavera P6)
- Resource optimization algorithms
- Monte Carlo simulation (10,000+ scenarios)
- Earned value analysis (budget vs. actual tracking)

---

**This skill activates when you**:
- Calculate project critical path and duration
- Perform PERT analysis with three-point estimates
- Identify timeline risks and statutory deadline compliance
- Calculate resource requirements by phase
- Generate Gantt charts for visualization
- Analyze dependency complexity and bottlenecks
- Optimize project schedule through crashing or fast-tracking
