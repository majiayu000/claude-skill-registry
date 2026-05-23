---
name: project-schedule-template
description: Эксперт по расписаниям проектов. Используй для WBS, Gantt charts, dependency mapping и resource allocation.
---

# Project Schedule Template Expert

Expert in project scheduling, WBS, timeline management, and resource allocation.

## Work Breakdown Structure (WBS)

```yaml
wbs_principles:
  100_percent_rule: "WBS must include 100% of project scope"
  mutual_exclusivity: "No overlapping work between elements"
  appropriate_detail: "Break down until estimable (8-80 hours)"

  numbering:
    level_1: "1.0, 2.0 (Phases)"
    level_2: "1.1, 1.2 (Deliverables)"
    level_3: "1.1.1 (Work packages)"

wbs_template:
  - id: "1.0"
    name: "Initiation"
    deliverables:
      - "1.1 Project Charter"
      - "1.2 Stakeholder Analysis"

  - id: "2.0"
    name: "Planning"
    deliverables:
      - "2.1 Project Plan"
      - "2.2 Technical Design"

  - id: "3.0"
    name: "Execution"
    deliverables:
      - "3.1 Development"
      - "3.2 Testing"

  - id: "4.0"
    name: "Deployment"
    deliverables:
      - "4.1 Production Release"

  - id: "5.0"
    name: "Closure"
    deliverables:
      - "5.1 Documentation"
      - "5.2 Lessons Learned"
```

## Dependencies

```yaml
dependency_types:
  finish_to_start:
    code: "FS"
    description: "Successor starts when predecessor finishes"
    most_common: true

  start_to_start:
    code: "SS"
    description: "Both start together"

  finish_to_finish:
    code: "FF"
    description: "Both finish together"

  lag_lead:
    lag: "FS+5 = Start 5 days after"
    lead: "FS-3 = Start 3 days before finish"
```

## Duration Estimation

```yaml
three_point_estimation:
  formula: "(O + 4M + P) / 6"
  definitions:
    optimistic: "Best case (10% probability)"
    most_likely: "Most probable duration"
    pessimistic: "Worst case (10% probability)"

  example:
    optimistic: 10
    most_likely: 15
    pessimistic: 26
    result: "16 days"

risk_buffers:
  low_risk: "10-15%"
  medium_risk: "20-30%"
  high_risk: "40-50%"
```

## Resource Allocation

```yaml
resource_planning:
  max_utilization: "80% recommended"
  buffer: "20% for meetings, admin, unexpected"

  capacity_formula: "Working Days × Hours/Day × Availability %"

resource_leveling:
  techniques:
    - "Delay non-critical tasks"
    - "Split tasks"
    - "Add resources"
    - "Overtime (short-term only)"
```

## Critical Path

```yaml
critical_path:
  definition: "Longest path determining minimum duration"
  characteristics:
    - "Zero total float"
    - "Delay impacts project end date"

  calculations:
    early_start: "Max(predecessor early finishes)"
    early_finish: "Early start + Duration"
    late_finish: "Min(successor late starts)"
    late_start: "Late finish - Duration"
    total_float: "Late start - Early start"
```

## Phase Guidelines

```yaml
phase_duration:
  initiation: "5-10%"
  planning: "15-25%"
  execution: "50-70%"
  closure: "5-10%"
```

## Лучшие практики

1. **WBS first** — начинайте с полной декомпозиции работ
2. **Realistic estimates** — используйте трёхточечную оценку
3. **Buffer planning** — закладывайте буферы на риски
4. **Critical path focus** — приоритизируйте критический путь
5. **Resource leveling** — избегайте перегрузки
6. **Regular updates** — обновляйте расписание еженедельно
