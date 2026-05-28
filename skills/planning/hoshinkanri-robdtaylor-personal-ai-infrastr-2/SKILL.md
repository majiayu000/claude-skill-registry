---
name: Hoshinkanri
description: Strategic policy deployment system for automotive manufacturing. Cascades Group-level targets to shop floor through X-Matrix, catchball process, and bowling chart tracking.  USE WHEN user says 'hoshin', 'x-matrix', 'catchball', 'bowling chart', 'strategy deployment', 'cascade objectives', 'breakthrough objectives', 'strategic planning', 'policy deployment', or requests help with annual planning integration.  Integrates with IATF 16949 quality systems and AutomotiveManufacturing skill for work instruction cascade.
---

# Hoshin Kanri - Strategic Policy Deployment

## When to Activate This Skill

- "Create an X-Matrix for [objective]"
- "Help me cascade [Group target] to departments"
- "Set up bowling chart for [KPI]"
- "Prepare catchball documentation"
- "Monthly Hoshin review template"
- "A3 problem solving for red objective"
- "Integrate Hoshin with our quality objectives"

## Core Concepts

### The Hoshin Kanri System

```
VISION (3-5 Year)
      |
      v
BREAKTHROUGH OBJECTIVES (Annual)
      |
      v (Catchball)
ANNUAL OBJECTIVES (Departmental)
      |
      v (Catchball)
IMPROVEMENT PRIORITIES (Projects/Initiatives)
      |
      v
KEY PERFORMANCE INDICATORS (Metrics)
      |
      v
DAILY MANAGEMENT (Shop Floor Execution)
```

### X-Matrix Structure

The X-Matrix connects strategy to execution on a single page:

```
                    ANNUAL OBJECTIVES (North)
                    [What we must achieve this year]
                            |
    +-----------------------+------------------------+
    |                       |                        |
BREAKTHROUGH           CORRELATION            IMPROVEMENT
OBJECTIVES             MATRIX                 PRIORITIES
(West)                 (Center)               (East)
[3-5 year goals]       [Relationships]        [Projects/Initiatives]
    |                       |                        |
    +-----------------------+------------------------+
                            |
                    TARGETS/KPIs (South)
                    [How we measure success]
```

**Correlation Symbols:**
- Strong correlation (primary driver)
- Moderate correlation (supporting)
- Weak correlation (indirect impact)

### The Catchball Process

**Definition:** Bidirectional negotiation ensuring alignment and buy-in across levels.

**NOT:** Top-down directives presented for rubber-stamp approval.

**Process:**
1. Leadership proposes breakthrough objectives
2. Next level reviews against capabilities and constraints
3. Counter-proposals and adjustments made
4. Iterate until consensus reached
5. Document agreements and accountabilities
6. Repeat cascade to next level

**Key Questions at Each Level:**
- "Is this achievable with our current resources?"
- "What obstacles do you foresee?"
- "What support do you need?"
- "What can you commit to?"

### Bowling Chart Tracking

**Purpose:** Visual monthly tracking of Hoshin objectives

**Structure:**
```
OBJECTIVE: [Name]
OWNER: [Named Person - NOT department]
+-------+-----+-----+-----+-----+-----+-----+-----+
| Month | Jan | Feb | Mar | Apr | May | Jun | YTD |
+-------+-----+-----+-----+-----+-----+-----+-----+
| Target| X.X | X.X | X.X | X.X | X.X | X.X | X.X |
| Actual| X.X | X.X | X.X |     |     |     | X.X |
| Status| G/Y | G/Y | R/Y |     |     |     | R/Y |
+-------+-----+-----+-----+-----+-----+-----+-----+
```

**Status Colors:**
- GREEN: On or ahead of target
- YELLOW: Within acceptable variance (define %)
- RED: Behind target - requires A3

---

## Review Cadence (Aligned with Q2/Q3 Group Cycle)

| Timing | Activity | Template |
|--------|----------|----------|
| Q2-Q3 | Annual Hoshin Planning | `templates/annual-planning.md` |
| Q4 | Department Cascade | `templates/catchball-record.md` |
| Monthly | Bowling Chart Review | `templates/monthly-review.md` |
| Quarterly | Formal Hoshin Review | `templates/quarterly-review.md` |
| As Needed | A3 Problem Solving | `templates/a3-template.md` |

---

## Integration Points

### With IATF 16949

| IATF Clause | Hoshin Element |
|-------------|----------------|
| 5.1 Leadership | X-Matrix ownership |
| 6.1 Planning | Risk-based objectives |
| 6.2 Quality Objectives | Hoshin targets |
| 9.3 Management Review | Monthly/Quarterly reviews |
| 10.3 Improvement | PDCA/A3 countermeasures |

### With AutomotiveManufacturing Skill

Hoshin objectives cascade to:
- PFMEA priority updates
- Control Plan revisions
- Work Instruction updates

---

## Common Failure Modes to Avoid

1. **Too Many Objectives** - Limit to 3-5 breakthrough goals
2. **Department Ownership** - Assign to named INDIVIDUALS
3. **Skipping Catchball** - True dialogue, not rubber-stamping
4. **Ceremonial Reviews** - Problem-solve, don't just report
5. **No Daily Connection** - Link to shop floor management
6. **Leadership Drift** - Sustained executive engagement required

---

## Templates Available

| Template | Purpose | Location |
|----------|---------|----------|
| X-Matrix | Strategy visualization | `templates/x-matrix.md` |
| Catchball Record | Document negotiations | `templates/catchball-record.md` |
| Bowling Chart | Monthly tracking | `templates/bowling-chart.md` |
| Monthly Review | Meeting agenda | `templates/monthly-review.md` |
| A3 Template | Problem solving | `templates/a3-template.md` |
| Annual Planning | Year kickoff | `templates/annual-planning.md` |
| X-Matrix Excel | Spreadsheet format | `templates/x-matrix-excel.md` |
| PowerPoint Ready | Presentation content | `templates/hoshin-powerpoint.md` |

---

## Quick Reference

### Cascade Translation Example

**Group Target:** 8% BOM Cost Reduction

| Level | Objective | Owner | KPI |
|-------|-----------|-------|-----|
| Division | 8% BOM reduction | Division Lead | Total BOM variance |
| Engineering | 4 VA/VE projects | Eng. Manager | Savings per project |
| Procurement | Supplier consolidation | Proc. Manager | PPV improvement |
| Manufacturing | Scrap reduction | Prod. Manager | Scrap % |
| Shop Floor | First-pass yield | Line Lead | FPY % |

### Review Meeting Structure (30-45 min)

1. **Review bowling charts** (15 min)
   - Green: Acknowledge, move on
   - Yellow: Brief discussion, monitor
   - Red: Assign A3, set deadline

2. **A3 updates** (15 min)
   - Progress on active countermeasures
   - New issues surfaced

3. **Decisions needed** (10 min)
   - Resource requests
   - Escalations
   - Target adjustments

4. **Action items** (5 min)
   - Capture, assign, date

---

## Key Principles

1. **Vital Few** - Focus on breakthrough, not incremental
2. **Catchball** - Alignment through dialogue
3. **PDCA** - Plan-Do-Check-Act at every level
4. **Visual Management** - X-Matrix, bowling charts visible
5. **Named Owners** - Individual accountability
6. **Regular Cadence** - Monthly reviews non-negotiable
7. **A3 Discipline** - Structured problem-solving for red items

---

## Extended Context

For comprehensive methodologies and detailed guidance:
`read ~/.claude/skills/HoshinKanri/CLAUDE.md`

For templates:
`ls ~/.claude/skills/HoshinKanri/templates/`
