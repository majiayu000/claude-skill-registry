---
name: delivery.dashboard_brief
phase: delivery
roles:
  - Data Analyst
  - Product Designer
description: Align analysts and designers on the goals, requirements, and storytelling approach for a new or updated dashboard.
variables:
  required:
    - name: audience
      description: Primary audience for the dashboard.
    - name: decisions
      description: Decisions or actions the dashboard should enable.
  optional:
    - name: data_sources
      description: Key data sources feeding the dashboard.
    - name: design_language
      description: Design system or visualization guidelines.
outputs:
  - Dashboard goals and narrative structure.
  - Data requirements, transformations, and quality checks.
  - Wireframe outline with recommended visualizations and interactions.
---

# Purpose
Ensure analytics and design have a shared blueprint before building dashboards, reducing iteration and aligning on data storytelling.

# Pre-run Checklist
- ✅ Gather stakeholder requirements and success metrics.
- ✅ Review existing dashboards or reports serving similar needs.
- ✅ Confirm data availability and latency expectations.

# Invocation Guidance
```bash
codex run --skill delivery.dashboard_brief \
  --vars "audience={{audience}}" \
         "decisions={{decisions}}" \
         "data_sources={{data_sources}}" \
         "design_language={{design_language}}"
```

# Recommended Input Attachments
- Sample dashboards or inspiration references.
- Data dictionary or metric catalog extracts.
- UX research on stakeholder workflows.

# Claude Workflow Outline
1. Summarize audience, decisions, and context.
2. Define dashboard objectives, success metrics, and narrative flow.
3. Detail data sources, transformations, and quality considerations.
4. Recommend visualization choices mapped to user questions.
5. Outline collaboration plan, milestones, and review cadence.

# Output Template
```
## Dashboard Brief
### Audience & Decisions
- Audience:
- Key Decisions:

### Narrative Flow
1. Context
2. Explore
3. Act

### Data Requirements
| Source | Metric | Transformation | Quality Checks | Owner |
| --- | --- | --- | --- | --- |

### Visualization Outline
| Section | Visual Type | Purpose | Notes |
| --- | --- | --- | --- |

### Collaboration Plan
- Milestones:
- Feedback Rituals:
- Open Questions:
```

# Follow-up Actions
- Create build tasks for analytics engineering and design.
- Validate data quality before stakeholder preview.
- Schedule enablement session to walk through the dashboard story.
