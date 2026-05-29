---
description: Real-time compliance tracking for Northcote Curio design system. Monitors
  component migration progress (Material 3 to Northcote metaphors), visual audit pass
  rates, typography distinctiveness, botanical palette adherence, and overall design
  system maturity. Feeds data from visual audits and component inventories into health
  metrics.
name: compliance-dashboard
---

# Compliance Dashboard Skill

## Overview

Transforms design system validation from **point-in-time audits** into **continuous visibility**. Tracks Northcote Curio adoption across your component library, reveals trends (improving or diverging?), and identifies high-priority refinement targets.

A brief is only successful if the system reflects it. A dashboard makes that visible.

## When to Use This Skill

Use this skill when you need to:

- **Track design system health** over time (quarterly reviews, maturity assessment)
- **Monitor component migration** progress (Material 3 → Northcote naming/aesthetics)
- **Identify compliance trends** (is your system becoming more Northcote-aligned?)
- **Spot components needing refresh** (which ones diverge most from standards?)
- **Measure brief effectiveness** (how well is your brief guiding work?)
- **Communicate progress** to stakeholders (visual evidence of maturation)
- **Make prioritization decisions** (where should team focus next?)
- **Celebrate milestones** (we've hit 80% Northcote compliance!)

## How It Works

The skill aggregates data from multiple sources:

1. **Visual Audit Results** (from northcote-visual-audit skill)
   - Component pass/fail/needs-refinement status
   - Specific assessment per dimension (typography, color, layout, botanical)
   - Timestamp and iteration tracking

2. **Component Inventory** (from codebase-orchestrator skill)
   - Total components in system
   - Material 3 vs. Northcote naming count
   - Component categorization

3. **Historical Trends** (accumulated over time)
   - Compliance score progression
   - Migration percentage over quarters
   - Average audit pass rate

4. **Manual Input** (optional human verification)
   - Justifications for components that "fail" but are acceptable
   - Context for edge cases
   - Team notes on strategic decisions

## The Compliance Metrics

### Core Metrics

| Metric | What It Measures | Green | Yellow | Red |
|---|---|---|---|---|
| **Overall Compliance** | % of components passing audit | 80%+ | 60-79% | <60% |
| **Typography Distinctiveness** | % using Northcote fonts, not defaults | 90%+ | 70-89% | <70% |
| **Color Palette Adherence** | % using Australian botanical colors | 85%+ | 65-84% | <65% |
| **Layout Intentionality** | % with organic spacing, not mechanical | 80%+ | 60-79% | <60% |
| **Botanical Integration** | % with meaningful (not decorative) motifs | 70%+ | 50-69% | <50% |
| **Component Migration** | % using Northcote names (Pebble, Stone, etc.) | 100% | 80-99% | <80% |

### Trend Metrics

| Metric | Meaning | Good Trend | Bad Trend |
|---|---|---|---|
| **Compliance Trajectory** | Is system getting more or less Northcote? | Upward | Downward |
| **Audit Consistency** | Are results becoming more predictable? | Stabilizing | Diverging |
| **Refinement Rate** | How many components improve per quarter? | High | Low |

### Strategic Metrics

| Metric | What It Reveals |
|---|---|
| **Brief Effectiveness** | Do audit results match brief guidance? (Consistency = brief is working) |
| **Component Maturity** | Average number of audit iterations before pass |
| **Priority Gap** | Which dimensions most commonly fail (where to focus)? |

## Dashboard Views

### View 1: Health Overview (30-second snapshot)

```
NORTHCOTE CURIO DESIGN SYSTEM HEALTH
Last Updated: 2026-01-28

Overall Compliance:     78% ▲ (was 72% last quarter)
Typography:             85% ✓
Color Palette:          82% ✓
Layout Intentionality:  74% ▼ (was 78%)
Botanical Integration:  68% ▲ (was 65%)
Component Migration:    92% ✓

Trend: Improving overall, slight layout regression
Status: Approaching 80% threshold (production ready)
```

### View 2: Component Breakdown

List of every component with status:

```
Component Name      | Type   | Status | Last Audit | Iterations
Pebble (Button)     | Input  | PASS   | 2026-01-27 | 2
Stone (Card)        | Layout | PASS   | 2026-01-25 | 3
Sediment (List)     | Layout | NEEDS  | 2026-01-24 | 4
Leaf (Badge)        | Input  | FAIL   | 2026-01-20 | 1
...                 | ...    | ...    | ...        | ...
```

Click each to see detailed audit findings.

### View 3: Migration Progress

Visual representation of Material 3 → Northcote journey:

```
Component Naming Migration
████████░░ 92% complete

Material 3 Legacy Names:    3 components (M3Button, M3Card, M3List)
Northcote Metaphor Names:   47 components (Pebble, Stone, Sediment, etc.)

Remaining Migration Work:
- M3Button → Pebble (high priority, input heavy)
- M3Card → Stone (medium priority, legacy code)
- M3List → Sediment (low priority, being refactored)
```

### View 4: Quarterly Trends

```
Compliance Score Progression

Q4 2025: ████░░░░░░ 45%
Q1 2026: ████████░░ 78%

Trend: Strong improvement (33 point gain)
Trajectory: On pace for 90% by Q2 2026
Milestone: Production-ready (80%) achieved Jan 2026
```

### View 5: Dimension Deep-Dive

Which dimensions need focus?

```
Dimension Performance (Latest Audit Round)

Typography:              ████████░░ 85% STRONG
Color:                  ████████░░ 82% STRONG
Layout:                 ███████░░░ 74% GOOD
Botanical:              ██████░░░░ 68% NEEDS WORK
Overall Coherence:      ███████░░░ 76% GOOD

Priority for Next Sprint: Improve botanical integration
Expected Effort: Medium
Impact on Overall: +3-5% compliance
```

## Integration with Other Skills

### With Northcote-Visual-Audit
Each visual audit automatically feeds results into the dashboard. Monthly automated audits create historical baseline.

### With Codebase-Orchestrator
Component inventory data feeds dashboard to track migration completion percentage.

### With Brand-Brief-Optimizer
If brief clarity score is high but component compliance is low, the brief isn't guiding work effectively (signals need for training/alignment).

### With Northcote-Typography-Strategy
Typography audit results feed directly into compliance metrics, showing which components have distinctive fonts vs. generic defaults.

## Handover Integration

Compliance dashboard automatically integrates with orchestrator handover mode to prioritize migration tasks:

**Priority Calculation:**
Dashboard calculates handover task sequence based on:
1. **Compliance Score**: Components with lowest scores prioritized (highest impact)
2. **Blocking Dependencies**: Components blocking other migrations moved up
3. **Usage Frequency**: Most-used components prioritized (highest user impact)

**Handover Contribution:**
Dashboard feeds orchestrator with:
- Component visual audit status (pass/fail/needs-refinement)
- Compliance dimensions needing focus (typography, color, layout, botanical)
- Historical trend data (improving or regressing?)
- Dimension-specific gaps (where to focus effort)

**Output Example:**
```json
{
  "compliance_metrics": {...},
  "handover_priorities": [
    {
      "component": "Lens",
      "priority": 1,
      "compliance_score": 42,
      "blocking": "form adoption",
      "dimensions_failing": ["typography", "color"],
      "usage_frequency": "high"
    },
    {
      "component": "Mark",
      "priority": 2,
      "compliance_score": 38,
      "blocking": "bulk actions",
      "dimensions_failing": ["layout", "botanical"],
      "usage_frequency": "medium"
    }
  ]
}
```

**Workflow:**
1. Orchestrator identifies components needing migration
2. Dashboard scores compliance and identifies gaps
3. Dashboard calculates priority (impact + blocking + frequency)
4. Orchestrator packages as handover tasks in priority order
5. Gemini executes highest-impact migrations first
6. Post-migration, dashboard visual audit validates improvements

## Workflow: Continuous Monitoring

### Monthly (Automated)
1. Screenshot deployed components
2. Run visual audits
3. Update compliance metrics
4. Generate dashboard report
5. Identify new issues

### Quarterly (Manual Review)
1. Analyze trends
2. Discuss compliance trajectory with team
3. Identify strategic focus areas
4. Set next quarter priorities
5. Celebrate milestones

### Annually (Comprehensive)
1. Review full year of compliance data
2. Assess design system maturity
3. Update brief based on learnings
4. Plan next year's migration/improvement work

## Key Insights the Dashboard Reveals

### Insight 1: Brief Effectiveness
If visual audits are consistently passing, your brief is clear and guiding work.  
If audits are inconsistent, brief language needs clarification.

### Insight 2: Component Maturity
If components need many audit iterations to pass, your standards are complex or brief isn't clear.  
If most pass on first audit, team understands brief well.

### Insight 3: Strategic Gaps
Which dimension fails most often? That's where to invest in brief clarity and training.

### Insight 4: Timeline to Excellence
Current trajectory projected forward shows when you'll hit 90% compliance (production excellence).

## Example Scenarios

### Scenario 1: Strong Compliance, Downward Trend
**Problem**: Something changed (new team member, brief misunderstanding, pressure to ship fast)  
**Response**: Identify what changed, re-align team, potentially update brief if standards evolved

### Scenario 2: Weak Compliance, Upward Trend
**Good news**: You're moving in right direction  
**Response**: Accelerate effort, add resources, celebrate progress

### Scenario 3: Strong Typography, Weak Botanical
**Insight**: Typography strategy is clear and guiding decisions  
Botanical guidance needs clarification or examples

### Scenario 4: Stalled Progress
**Problem**: Compliance stuck at 70% for two quarters  
**Response**: Analyze why, could be unclear standards, resource constraints, or competing priorities

## Creating a Culture of Excellence Through Visibility

The dashboard's real power is psychological. When your team sees:

- "We've gone from 45% to 78% in one quarter"
- "Typography distinctiveness is at 85%"
- "We're on pace for production-ready design system by Q2"

They understand: **This matters. We're succeeding. Keep going.**

That visibility transforms design system work from thankless compliance to **visible progress toward excellence**.

## Limitations

This skill:

✅ Tracks compliance trends over time  
✅ Aggregates data from multiple audit sources  
✅ Reveals strategic gaps in brief or execution  
✅ Provides visible progress indicators  

❌ Cannot guarantee consistency across auditors (human judgment involved)  
❌ Doesn't fix components (only reveals what needs fixing)  
❌ Requires regular audit data (skipped months create gaps)  
❌ Metrics are relative to your standards, not industry benchmarks

## Success Criteria

Dashboard is valuable when it:

1. **Shows clear trend** (system is measurably improving)
2. **Identifies priority work** (next focus area is obvious)
3. **Tracks milestone achievement** (80% compliance celebrated)
4. **Reveals brief effectiveness** (consistent results validate brief clarity)
5. **Motivates team** (visible progress sustains momentum)

## Key Principle

You can't improve what you don't measure. A compliance dashboard makes design system maturity **visible, trackable, and achievable**.

It transforms the question from "Are we Northcote?" to "How Northcote are we becoming?"

That shift from binary to directional thinking enables continuous improvement.

---

*A great design system is measured in its ability to guide consistent, excellent work. The dashboard shows whether you're achieving that.*
