# sdlc-reports

Generate comprehensive SDLC reports including iteration status, metrics dashboards, and executive summaries.

## Triggers

- "iteration report"
- "sprint summary"
- "project report"
- "sdlc metrics"
- "status report"
- "executive summary"
- "phase report"

## Purpose

This skill generates SDLC reporting across all phases by:
- Aggregating metrics from multiple sources
- Tracking progress against milestones
- Generating stakeholder-appropriate reports
- Visualizing trends and health indicators
- Providing actionable insights

## Behavior

When triggered, this skill:

1. **Determines report type**:
   - Iteration/sprint report
   - Phase status report
   - Executive summary
   - Metrics dashboard
   - Custom report

2. **Aggregates data**:
   - Pull from project artifacts
   - Calculate derived metrics
   - Compare to baselines/targets

3. **Analyzes status**:
   - Progress vs plan
   - Risk status
   - Quality indicators
   - Team velocity

4. **Generates report**:
   - Format for audience
   - Include visualizations
   - Highlight key insights
   - Provide recommendations

## Report Types

### Iteration Report

```yaml
iteration_report:
  audience: development_team, scrum_master
  frequency: end_of_iteration
  length: 5 minutes read

  sections:
    - iteration_summary
    - completed_work
    - incomplete_work
    - metrics
    - blockers
    - retrospective_items
    - next_iteration_preview
```

### Phase Report

```yaml
phase_report:
  audience: project_manager, stakeholders
  frequency: phase_gate
  length: 10 minutes read

  sections:
    - phase_summary
    - milestone_progress
    - deliverables_status
    - risk_status
    - quality_metrics
    - resource_utilization
    - gate_readiness
```

### Executive Summary

```yaml
executive_summary:
  audience: executives, sponsors
  frequency: monthly_or_on_demand
  length: 3 minutes read

  sections:
    - headline_status
    - key_achievements
    - risks_and_issues
    - budget_status
    - timeline_status
    - decisions_needed
```

### Metrics Dashboard

```yaml
metrics_dashboard:
  audience: all_stakeholders
  frequency: real_time
  format: visual_dashboard

  metrics:
    - velocity
    - burndown
    - defect_rate
    - coverage
    - risk_score
    - schedule_variance
```

## Iteration Report Template

```markdown
# Iteration Report

**Iteration**: Sprint 15
**Period**: Dec 2-15, 2025
**Team**: Platform Team

---

## Summary

| Metric | Planned | Actual | Status |
|--------|---------|--------|--------|
| Story Points | 42 | 38 | ⚠️ 90% |
| Stories Completed | 8 | 7 | ⚠️ 88% |
| Bugs Fixed | 5 | 7 | ✅ 140% |
| Tech Debt | 10pts | 8pts | ⚠️ 80% |

**Overall**: Slightly behind on features, ahead on bugs.

---

## Velocity Trend

```
Sprint 12: ████████████████████████████████████ 36
Sprint 13: ██████████████████████████████████████████ 42
Sprint 14: ████████████████████████████████████████ 40
Sprint 15: ██████████████████████████████████████ 38
           Average: 39 pts
```

---

## Completed Work

### Features
| ID | Title | Points | Owner |
|----|-------|--------|-------|
| US-145 | User dashboard | 8 | Sarah |
| US-146 | Export to CSV | 5 | David |
| US-147 | Filter improvements | 3 | Elena |
| US-148 | Bulk actions | 5 | David |
| US-149 | Search enhancement | 5 | Sarah |

### Bugs Fixed
| ID | Title | Severity | Owner |
|----|-------|----------|-------|
| BUG-234 | Login timeout | High | Elena |
| BUG-235 | Export crash | High | David |
| BUG-236 | UI alignment | Low | Sarah |
| ... | ... | ... | ... |

### Tech Debt
| ID | Title | Points | Impact |
|----|-------|--------|--------|
| TD-45 | Upgrade React | 5 | Perf +15% |
| TD-46 | Add logging | 3 | Debug time -30% |

---

## Incomplete Work

### Carried to Next Sprint
| ID | Title | Points | Reason | New Target |
|----|-------|--------|--------|------------|
| US-150 | API v2 migration | 8 | Blocked by vendor | Sprint 16 |

**Impact**: API v2 delay affects integration timeline

---

## Metrics

### Quality
- Code coverage: 82% (target: 80%) ✅
- Critical bugs: 0 (target: 0) ✅
- Technical debt ratio: 12% (target: <15%) ✅

### Process
- PR review time: 4.2 hours (target: <8h) ✅
- Build time: 8 min (target: <10 min) ✅
- Deploy frequency: 12 deploys (target: >10) ✅

### Performance
- API p99 latency: 180ms (target: <200ms) ✅
- Error rate: 0.02% (target: <0.1%) ✅

---

## Blockers & Risks

### Active Blockers
| ID | Issue | Impact | Owner | Status |
|----|-------|--------|-------|--------|
| BLK-15 | Vendor API down | US-150 blocked | David | Waiting |

### Emerging Risks
- **Holiday availability**: Reduced capacity Dec 23-Jan 2
- **Scope creep**: 2 new requests this sprint

---

## Retrospective Highlights

### What Went Well
- Pair programming on complex features
- Quick bug triage process

### What to Improve
- Better vendor communication
- Earlier blocker escalation

### Actions
- [ ] Schedule vendor sync meeting (Owner: David)
- [ ] Update blocker escalation process (Owner: Sarah)

---

## Next Iteration Preview

**Sprint 16**: Dec 16-29, 2025

### Planned Work
| Priority | ID | Title | Points |
|----------|-----|-------|--------|
| High | US-150 | API v2 migration | 8 |
| High | US-151 | Performance optimization | 5 |
| Medium | US-152 | New user onboarding | 5 |
| Medium | US-153 | Analytics integration | 5 |

**Capacity**: 35 pts (reduced due to holidays)

---

## Team Notes

- Sarah OOO Dec 23-27
- New team member starting Jan 2
```

## Executive Summary Template

```markdown
# Executive Summary

**Project**: Customer Portal Modernization
**Period**: December 2025
**Status**: 🟡 On Track with Risks

---

## At a Glance

| Dimension | Status | Trend |
|-----------|--------|-------|
| Schedule | 🟡 -1 week | → |
| Budget | 🟢 92% spent | ↓ |
| Scope | 🟢 100% | → |
| Quality | 🟢 All metrics green | ↑ |
| Risk | 🟡 1 high risk | → |

---

## Key Achievements This Month

1. **Phase Gate Passed**: Elaboration complete, entering Construction
2. **Architecture Baseline**: SAD and ADRs approved
3. **Team Scaled**: 2 new developers onboarded
4. **Risk Retired**: Database migration approach validated via PoC

---

## Risks & Issues

### Top Risk
**Database Scalability** (High)
- Mitigation 60% complete
- On track for Feb resolution
- No immediate project impact

### Active Issue
**Vendor API Delay**
- 1 week schedule impact
- Workaround identified
- Escalated to vendor management

---

## Budget Status

| Category | Budget | Actual | Remaining |
|----------|--------|--------|-----------|
| Personnel | $400K | $380K | $20K |
| Infrastructure | $50K | $42K | $8K |
| Licenses | $30K | $28K | $2K |
| **Total** | **$480K** | **$450K** | **$30K** |

**Forecast**: On budget, $30K contingency available

---

## Timeline Status

```
Inception   [████████████████████] Complete
Elaboration [████████████████████] Complete  ← Current
Construction [░░░░░░░░░░░░░░░░░░░░] Starting
Transition  [░░░░░░░░░░░░░░░░░░░░] Planned

Target: March 15, 2026
Current Forecast: March 22, 2026 (+1 week)
```

---

## Decisions Needed

1. **Budget Reallocation**: Move $10K from licenses to infrastructure for scaling?
   - Recommendation: Approve
   - Deadline: Dec 15

2. **Scope Change Request**: Add mobile app to v1.0?
   - Recommendation: Defer to v1.1
   - Impact if included: +6 weeks, +$80K

---

## Next Month Preview

- Begin Construction phase
- First feature delivery (Dec 30)
- Midpoint security review
- Holiday capacity planning
```

## Metrics Dashboard

```yaml
dashboard_sections:
  velocity:
    chart: line_graph
    metrics:
      - story_points_completed
      - story_points_planned
    period: last_6_iterations

  burndown:
    chart: burndown_chart
    metrics:
      - remaining_work
      - ideal_burndown
    period: current_iteration

  quality:
    chart: gauge_cluster
    metrics:
      - code_coverage
      - defect_rate
      - technical_debt_ratio

  schedule:
    chart: gantt
    data:
      - planned_milestones
      - actual_progress
      - forecast

  risk_heatmap:
    chart: heatmap
    axes:
      - probability
      - impact
    data: active_risks
```

## Usage Examples

### Iteration Report

```
User: "Generate sprint 15 report"

Skill executes:
1. Pull iteration data
2. Calculate metrics
3. Aggregate completed/incomplete
4. Generate report

Output:
"Sprint 15 Report Generated

Summary:
- Velocity: 38/42 pts (90%)
- Stories: 7/8 completed
- Bugs: 7/5 fixed (ahead!)

Key Highlights:
✅ User dashboard feature complete
✅ Critical bugs resolved
⚠️ API migration blocked (vendor)

Recommendations:
1. Escalate vendor blocker
2. Reduce Sprint 16 capacity (holidays)

Report: .aiwg/reports/iteration/sprint-15.md"
```

### Executive Summary

```
User: "Executive summary for steering committee"

Skill generates:
1. Aggregate project status
2. Highlight key points
3. Format for executives

Output:
"Executive Summary Generated

Status: 🟡 On Track with Risks

Headlines:
- Phase gate passed (Elaboration → Construction)
- Schedule: -1 week (vendor delay)
- Budget: On track ($30K contingency)

Decisions Needed:
1. Budget reallocation approval
2. Scope change decision

Report: .aiwg/reports/executive/dec-2025.md"
```

### Metrics Dashboard

```
User: "Show project metrics"

Skill generates:
"Project Metrics Dashboard

Velocity (Last 6 Sprints):
S10: ████████████████ 32
S11: ████████████████████ 38
S12: ████████████████████ 36
S13: ██████████████████████ 42
S14: ████████████████████ 40
S15: ██████████████████ 38
     Avg: 37.7 pts/sprint

Quality Metrics:
Coverage:  ████████████████░░ 82% ✅
Defects:   ██░░░░░░░░░░░░░░░░ 3 open ✅
Tech Debt: ████████████░░░░░░ 12% ✅

Schedule:
Progress:  ████████████░░░░░░ 65%
Target:    ████████████████░░ 70%
Variance:  -5% (1 week behind)"
```

## Integration

This skill uses:
- `project-awareness`: Current project context
- `artifact-metadata`: Artifact status tracking
- `traceability-check`: Requirements coverage data
- `test-coverage`: Quality metrics
- `risk-cycle`: Risk status

## Agent Orchestration

```yaml
agents:
  metrics:
    agent: metrics-analyst
    focus: Data aggregation and calculation

  analysis:
    agent: project-manager
    focus: Status interpretation

  writing:
    agent: technical-writer
    focus: Report formatting
```

## Configuration

### Report Templates

```yaml
templates:
  iteration: templates/management/iteration-report.md
  phase: templates/management/phase-report.md
  executive: templates/management/executive-summary.md
  dashboard: templates/management/metrics-dashboard.md
```

### Metric Sources

```yaml
metric_sources:
  velocity:
    source: .aiwg/planning/iterations/
    calculation: sum(completed_points)

  quality:
    sources:
      - coverage: .aiwg/testing/coverage/
      - defects: .aiwg/quality/defects/
      - debt: .aiwg/quality/tech-debt/

  schedule:
    source: .aiwg/planning/phase-plan.md
    comparison: actual_vs_planned
```

## Output Locations

- Iteration reports: `.aiwg/reports/iteration/`
- Phase reports: `.aiwg/reports/phase/`
- Executive summaries: `.aiwg/reports/executive/`
- Dashboards: `.aiwg/reports/dashboards/`

## References

- Report templates: templates/management/
- Metrics catalog: docs/metrics-catalog.md
- Dashboard guide: docs/dashboard-configuration.md
