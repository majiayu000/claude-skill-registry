---
name: initiative
description: Initiative planning, status reporting, and KPI-based performance reports with trend analysis
user-invocable: true
help:
  purpose: |-
    Initiative planning, status reporting, and KPI-based performance reports with trend analysis.
  use_cases:
    - "Plan a new initiative for [topic]"
    - "What's the status of [initiative]?"
    - "Generate a performance report"
  scope: initiatives,planning,status,kpis,performance
---

# Initiative skill: planning, status, and performance

Comprehensive initiative management with three distinct modes: planning new initiatives, tracking status, and generating performance reports with KPI analysis.

---

## Explicitly excludes

This does NOT provide: hour estimates, sprint planning, developer task breakdowns, ticket creation, complexity points.

---

## Planning mode

Scope new initiatives, build business cases, and assess project feasibility from a product management perspective.

### 1. Skill sets required

Identify competencies needed:

| Category | Examples |
|----------|----------|
| **Technical** | Data Science, ML Engineering, Backend, Frontend |
| **Domain** | Industry expertise, Compliance, Data Governance, UX Research |
| **Operational** | Project Management, Vendor Relations |

For each skill note:
- Proficiency level (Basic / Intermediate / Expert)
- Coverage (Covered / Gap / Partial)

### 2. Milestone breakdown

Outcome-oriented milestones, not tasks:

| Phase | Example |
|-------|---------|
| **Discovery** | "User research complete with pain points validated" |
| **Design** | "Technical architecture approved" |
| **Build** | "MVP deployed to staging" |
| **Launch** | "Soft launch with beta customers" |
| **Scale** | "GA release with target adoption" |

### 3. Dependencies, risks, assumptions

- **Dependencies:** Internal teams, external vendors, data sources
- **Risks:** Technical, resource, timeline, market
- **Assumptions:** What must be true for success?

### 4. Complexity and effort (qualitative)

| Dimension | Low | Medium | High |
|-----------|-----|--------|------|
| **Technical** | Known patterns | Some unknowns | Novel |
| **Coordination** | Single team | 2-3 teams | Org-wide |
| **Timeline** | Flexible | Target date | Hard deadline |

**Effort profile:** Light / Medium / Heavy / Major
**Door type:** One-Way (irreversible) / Two-Way (reversible)

---

## Status mode

When invoked for initiative status (not planning):

1. Read initiative from `memory/initiatives/{name}.md`
2. Query project tracker for current sprint status:
   - Open items with initiative label
   - Blocked items
   - Completion metrics
3. Query recent journal entries for meeting notes mentioning the initiative
4. Compile health report:
   - **Status:** On Track / At Risk / Blocked
   - **Progress:** Stories done vs total
   - **Blockers:** Open blocked items
   - **Recent decisions:** From memory/decisions/
   - **Upcoming milestones:** From initiative memory file
   - **Recommendations:** Based on data

---

## Performance mode

Generate KPI-based performance reports with trend analysis, separate from initiative-status (which gives holistic project health). This mode focuses on operational metrics and trends.

### Step 1: Read KPI definitions

Read `reference/kpis.md` to determine:
- Which teams/initiatives to report on
- Which metrics to pull
- Data sources for each metric

### Step 2: Query data sources

#### Project tracker

Common query patterns per metric:

| Metric | Query intent |
|--------|-------------|
| Velocity | Completed items in recent sprints |
| Cycle time | Average time from start to done |
| Bug count | Open bugs by severity |
| Blocked items | Items in blocked status |
| Sprint completion | Open sprint progress |
| Deployment frequency | Releases in recent period |

#### Time tracking (when configured)
- Time and utilization data
- Billable hours by team member

#### Monitoring (when configured)
- Pipeline reliability, uptime
- Infrastructure cost trends

### Step 3: Calculate trends

For each metric:
- **Current period**: Last 2 weeks (or current sprint)
- **Previous period**: Prior 2 weeks (or previous sprint)
- **Trend**: Improving / Declining / Stable
  - Improving: current is better than previous by >10%
  - Declining: current is worse than previous by >10%
  - Stable: within 10% variance

### Step 4: Flag issues

Flag metrics that:
- Crossed a negative threshold (e.g., defect rate >15%)
- Show declining trend for 2+ consecutive periods
- Have items blocked >5 days
- Are missing data (MCP query failed or connector not configured)

### Step 5: Generate report

```markdown
# Performance report: YYYY-MM-DD

## [Team/Initiative Name]

| KPI | Current | Previous | Trend |
|-----|---------|----------|-------|
| [Metric] | [Value] | [Value] | [Improving/Declining/Stable] |

### Flagged issues
- [Issue description with specific data]

### Recommended actions
- [Data-driven recommendation]
```

Repeat for each team/initiative in `reference/kpis.md`.

### Step 6: Save to journal

Save to `journal/YYYY-MM/YYYY-MM-DD-performance-report.md`

```yaml
---
date: YYYY-MM-DD
title: Performance Report
type: performance
teams: [Team names]
initiatives: [Initiative names]
---
```

---

## Output format (planning mode)

```markdown
## Initiative: [Name]

### Executive summary
[2-3 sentences]

### Skill sets required
| Skill | Level | Coverage |
|-------|-------|----------|

### Milestones
1. **[Phase]:** [Outcome] -- Timeline range

### Dependencies
- Internal: [[Team/Person]]
- External: [[Vendor]]

### Risks and assumptions
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|

### Effort profile
- Technical complexity: [L/M/H]
- Coordination: [L/M/H]
- Overall: [Light/Medium/Heavy/Major]
- Door type: [One-Way / Two-Way]
```

---

## Output format (status mode)

```markdown
## Initiative status: [Name]

**Overall health:** [On Track / At Risk / Blocked]

### Progress
| Metric | Value |
|--------|-------|
| Stories completed | X / Y |
| Blocked items | N |
| Sprint velocity | Z pts |

### Blockers
- [Blocker description with owner]

### Recent decisions
- [Decision from memory/decisions/]

### Upcoming milestones
- [Milestone with target date]

### Recommendations
- [Data-driven recommendation]
```

---

## Output format (performance mode)

```markdown
## Performance report: YYYY-MM-DD

### [Team/Initiative Name]

| KPI | Current | Previous | Trend | Status |
|-----|---------|----------|-------|--------|
| [Metric] | [Value] | [Value] | [Improving/Declining/Stable] | [OK/Warning/Critical] |

### Flagged issues
- [Issue description with specific data and timeline]

### Recommended actions
- [Data-driven recommendation with priority]

### Data source notes
- [Any limitations or gaps in metric collection]
```

---

## Context budget

**Planning mode:**
- Memory: Read initiative file + up to 3 related files
- Project tracker: Up to 3 queries
- Journal: Current month `_index.md` + up to 2 relevant entries

**Status mode:**
- Memory: Read initiative file + up to 3 related files
- Project tracker: Up to 3 queries
- Journal: Current month `_index.md` + up to 2 relevant entries

**Performance mode:**
- Reference: `reference/kpis.md` (mandatory)
- Project tracker: Up to 3 queries per team/initiative
- Memory: Read initiative files for context (up to 3)
- Time tracking: Limited to configured integration
- Monitoring: Limited to configured integration

---

## Absolute constraints

**Planning mode:**
- NEVER provide hour or sprint estimates
- NEVER create tickets (report only)
- NEVER skip dependency analysis in planning mode

**Status mode:**
- NEVER skip project tracker query in status mode (fall back to memory-only if not configured)

**Performance mode:**
- NEVER fabricate metric data (if query fails, report the gap)
- NEVER skip trend calculation
- NEVER output without the flagged issues section (even if empty)
- ALWAYS save to journal
- ALWAYS note data source limitations in the report
