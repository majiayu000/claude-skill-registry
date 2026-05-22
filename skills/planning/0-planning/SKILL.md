---
name: planning
description: "Universal planning for technical and non-technical projects. Domains: software implementation, business, personal, creative, academic, events. Capabilities: feature planning, system architecture, goal setting, milestone planning, requirement breakdown, trade-off analysis, resource allocation, risk assessment. Actions: plan, architect, design, evaluate, breakdown, structure projects. Keywords: implementation plan, technical design, architecture, roadmap, project plan, strategy, goal setting, milestones, timeline, action plan, SMART goals, sprint planning, task breakdown, OKRs. Use when: planning features, designing architecture, creating roadmaps, setting goals, organizing projects, breaking down requirements."
---

# Planning

Universal planning methodology for technical implementation and general project planning.

## Mode Selection

| Project Type | Mode | Key Focus |
|--------------|------|-----------|
| **Software/Technical** | Implementation | Codebase analysis, architecture, code changes |
| **Business/Personal/Creative** | Project | Goals, milestones, resources, timeline |

---

## Technical Implementation Planning

**Use when:** Planning software features, system architecture, technical solutions

### Core Principles

Always honor **YAGNI**, **KISS**, and **DRY** principles.
**Be honest, be brutal, straight to the point, and be concise.**

### Workflow

1. **Research & Analysis** → `references/research-phase.md`
   - Skip if: Provided with researcher reports

2. **Codebase Understanding** → `references/codebase-understanding.md`
   - Skip if: Provided with scout reports

3. **Solution Design** → `references/solution-design.md`

4. **Plan Organization** → `references/plan-organization.md`

5. **Task Breakdown** → `references/output-standards.md`

### Output Structure

```
plans/
└── YYYYMMDD-HHmm-plan-name/
    ├── research/
    ├── reports/
    ├── scout/
    ├── plan.md
    └── phase-XX-*.md
```

### Requirements

- DO NOT implement code - only create plans
- Self-contained with necessary context
- Include code snippets/pseudocode when clarifying
- Provide options with trade-offs
- Detailed enough for junior developers

---

## Project Planning (Non-Technical)

**Use when:** Business, personal, creative, academic, event planning

### Domains

- **Business**: Product launches, marketing, process improvements
- **Personal**: Career development, learning, lifestyle changes
- **Creative**: Writing, art, content creation
- **Academic**: Research, thesis, study programs
- **Events**: Conferences, weddings, community events

### Plan Format

**Location:** `docs/plans/PLAN-YYYYMMDD-HHMM-{slug}.md`

**Frontmatter:**
```yaml
---
plan_id: PLAN-YYYYMMDD-HHMM-{slug}
title: [Project Name]
created: YYYY-MM-DD HH:MM
status: draft | active | completed | on_hold
category: business | personal | creative | academic | event
phase: planning | execution | monitoring | complete
priority: critical | high | medium | low
---
```

### Required Sections

1. **Vision & Objectives** - SMART goals, alignment
2. **Scope & Deliverables** - In/out of scope, acceptance criteria
3. **Action Steps** - Phased tasks with owners, durations
4. **Resources Required** - People, budget, materials, tools
5. **Timeline & Milestones** - Dates, checkpoints, Gantt
6. **Risks & Contingencies** - Mitigation, early warnings
7. **Success Metrics** - Measurable outcomes, completion criteria

### Quick Templates

- `references/business-plan-template.md`
- `references/personal-goal-template.md`
- `references/generic-plan-template.md`

---

## Pre-Planning Protocol

**ALWAYS execute before creating new plan:**

1. Check for active plan: `test -f docs/plan.md && cat docs/plan.md`
2. If exists: Ask user to continue or create new
3. If none: Proceed with new plan creation

---

## Quality Standards

### Technical Plans
- Consider long-term maintainability
- Address security and performance
- Validate against codebase patterns
- Research thoroughly when uncertain

### Project Plans
- All 7 sections present
- Each step has owner and deadline
- Resources are realistic
- Risks have contingencies
- Metrics are SMART

### Both Types
- Be thorough and specific
- Simple, understandable structure
- Action-oriented
- Clear next steps

---

## References

### Technical Implementation
- `references/research-phase.md` - Research methodology
- `references/codebase-understanding.md` - Codebase analysis
- `references/solution-design.md` - Architecture patterns
- `references/plan-organization.md` - Plan structure
- `references/output-standards.md` - Task breakdown standards

### Project Templates
- `references/business-plan-template.md`
- `references/personal-goal-template.md`
- `references/generic-plan-template.md`

---

**Plan quality determines implementation success. Be comprehensive.**
