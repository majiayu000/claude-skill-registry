---
name: product-planning
description: |
  Product Owner / Business Analyst toolkit for product planning tasks.
  Use when the user wants to:
  - Write or refine user stories, epics, or acceptance criteria
  - Create or review PRDs (Product Requirement Documents)
  - Prioritize backlog items (RICE scoring, MoSCoW, etc.)
  - Plan sprints or releases
  - Create or update product roadmaps
  - Conduct competitive analysis or user research
  - Write release notes or stakeholder updates

  MANDATORY TRIGGERS: user story, epic, PRD, backlog, sprint planning, roadmap, acceptance criteria, product requirements, prioritize, story points, PO, BA, product owner, business analyst
---

# Product Planning Skill

Help with Product Owner and Business Analyst tasks using the product planning artifacts in this project.

## Context Files

Before responding to product planning requests, read the relevant context files in `product-planning/`:

| File | When to Read |
|------|--------------|
| `PRODUCT_VISION.md` | Always read first - provides product context |
| `personas/PERSONAS.md` | When writing user stories or considering user needs |
| `backlog/BACKLOG.md` | When prioritizing, planning sprints, or checking existing work |
| `roadmap/ROADMAP.md` | When discussing timelines or release planning |

## Templates

Use templates from `product-planning/templates/` when creating new artifacts:

- `USER_STORY_TEMPLATE.md` - For new user stories
- `EPIC_TEMPLATE.md` - For new epics
- `PRD_TEMPLATE.md` - For product requirement documents
- `SPRINT_PLANNING_TEMPLATE.md` - For sprint planning

## Common Tasks

### Writing User Stories

1. Read `PRODUCT_VISION.md` and `personas/PERSONAS.md`
2. Use the user story format: "As a [persona], I want [goal], so that [benefit]"
3. Include 3-5 acceptance criteria in Given/When/Then format
4. Reference which persona benefits most
5. Suggest story points (1, 2, 3, 5, 8, 13)

### Prioritizing Backlog

1. Read `backlog/BACKLOG.md` to see current items
2. Apply RICE scoring:
   - **R**each: How many users impacted?
   - **I**mpact: How much value? (3=massive, 2=high, 1=medium, 0.5=low)
   - **C**onfidence: How certain? (100%, 80%, 50%)
   - **E**ffort: Person-weeks of work
3. Score = (Reach × Impact × Confidence) / Effort
4. Provide reasoning for priority order

### Sprint Planning

1. Review backlog and identify ready items
2. Consider team capacity (story points)
3. Identify dependencies between items
4. Create a cohesive sprint goal
5. Balance feature work with tech debt

### Creating PRDs

1. Read product vision for alignment
2. Use `PRD_TEMPLATE.md` structure
3. Include measurable success metrics
4. Document edge cases and error handling
5. List dependencies and risks

## Best Practices

- Always reference personas by name (e.g., "Casual Carl", "Serious Sarah")
- Use INVEST criteria for stories: Independent, Negotiable, Valuable, Estimable, Small, Testable
- Keep acceptance criteria specific and testable
- Consider offline/PWA requirements for this app
- Reference accessibility requirements

## Updating Artifacts

When creating new stories, epics, or other artifacts:
1. Add them to the appropriate file in `product-planning/`
2. Update `backlog/BACKLOG.md` with new items
3. Maintain consistent ID numbering (US-XXX, E-XXX)
