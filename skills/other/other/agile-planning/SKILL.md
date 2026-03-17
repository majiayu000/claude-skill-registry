---
name: agile-planning
description: Generate agile release plans with sprints and roadmaps using unique sprint codes. Use when creating sprint schedules, product roadmaps, release planning, or when user mentions agile planning, sprints, roadmap, or release plans.
---

# Agile Planning

Generate lean agile release plans with sprint schedules and roadmaps.

## Overview

This skill creates structured release plans for agile projects. It generates:
- Sprint schedules with unique codes (SPRINT-001, SPRINT-002, etc.)
- Tasks with ticket codes (T-001, T-002, etc.) for granular tracking
- Roadmaps showing timeline and milestones
- Dependencies and release checkpoints

Use this when planning product releases, organizing work into sprints, or communicating timelines to stakeholders.

## Instructions

### Step 1: Gather Context

Before generating a plan, collect:
- **Project scope**: What are we building?
- **Timeline**: How many weeks/months?
- **Team size**: Number of developers
- **Sprint duration**: Typically 2 weeks
- **Key milestones**: Alpha, beta, production dates
- **Priorities**: Must-have vs nice-to-have features

### Step 2: Structure Sprints

Create sprints with:
- **Unique codes**: SPRINT-001, SPRINT-002, SPRINT-003 (sequential, zero-padded)
- **Sprint theme**: Descriptive name (e.g., "Payment Integration", "UI Polish")
- **Duration**: Start and end dates
- **Goal**: One-sentence sprint objective
- **Tasks**: 3-5 concrete tasks per sprint, each with unique ticket code (T-001, T-002, etc.)
- **Dependencies**: What blocks this sprint or depends on it

**Task Numbering**:
- Use format: T-001, T-002, T-003 (zero-padded, sequential across entire release)
- Each task gets a unique code that persists throughout the project
- Never reuse task codes

**Sprint Duration Guidelines**:
- 2 weeks (most common) = 10 working days
- Plan for 80% capacity (reserve 20% for meetings, bugs, unexpected)
- Balance workload across sprints

**Sprint Themes**:
Use clear, goal-oriented themes:
- Foundation, Setup, Infrastructure
- Core Features, MVP Development
- Integration, API Development
- Testing, Bug Fixes, Optimization
- Beta Launch, Production Release

### Step 3: Build Roadmap

Group sprints into timeline view:
- **By Quarter**: Q1 2025, Q2 2025, etc.
- **By Month**: January, February, March
- **By Phase**: Foundation → Features → Launch

Include major milestones:
- Alpha release dates
- Beta release dates
- Production launch
- Key feature completions

### Step 4: Format Output

Use this structure:

```markdown
# Release Plan: [Project Name] v[Version]

**Release Goal**: [One sentence]
**Timeline**: [Start] - [End] ([X] sprints)
**Team**: [Number] developers

## Sprints

### SPRINT-001: [Theme]
**Duration**: [Start Date] - [End Date]
**Goal**: [What this sprint achieves]

**Tasks**:
- T-001: [Task description] [ ]
- T-002: [Task description] [ ]
- T-003: [Task description] [ ]

**Dependencies**: [If any]

### SPRINT-002: [Theme]
**Duration**: [Start Date] - [End Date]
**Goal**: [What this sprint achieves]

**Tasks**:
- T-004: [Task description] [ ]
- T-005: [Task description] [ ]

## Roadmap

### Q1 2025
- **SPRINT-001**: [Key achievement]
- **SPRINT-002**: [Key achievement]

### Q2 2025
- **SPRINT-003**: [Key achievement]

## Milestones
- **[Date]**: Alpha release (SPRINT-00X)
- **[Date]**: Beta release (SPRINT-00X)
- **[Date]**: Production launch (SPRINT-00X)
```

### Step 5: Validate Plan

Check:
- ✓ Sprint codes are sequential and unique (SPRINT-001, SPRINT-002, etc.)
- ✓ Task codes are sequential and unique (T-001, T-002, etc.)
- ✓ Tasks are specific and measurable
- ✓ Dependencies are identified
- ✓ Timeline is realistic
- ✓ Milestones align with sprint schedule

## Best Practices

**Sprint Planning**:
- Keep tasks specific: "T-001: Stripe SDK integration" not "T-001: work on payments"
- Limit to 3-5 tasks per sprint
- Front-load risky/complex work
- Include buffer sprint for testing

**Task Numbering**:
- Always use 3 digits: T-001, not T-1
- Sequential across entire release (T-001, T-002... T-050)
- Never reuse codes, even if task is cancelled

**Dependencies**:
- Identify early: "Requires SPRINT-001 API endpoints"
- Schedule dependent sprints sequentially
- Document external dependencies (APIs, design assets)

**Roadmap**:
- Focus on outcomes, not tasks
- Highlight major milestones
- Keep it stakeholder-friendly
- Update after each sprint

**Code Conventions**:
- Sprints: Always use 3 digits (SPRINT-001, not SPRINT-1)
- Tasks: Always use 3 digits (T-001, not T-1)
- Sequential numbering: Task codes continue across all sprints
- Never reuse codes (sprints or tasks)

## Examples

### Example 1: E-commerce Platform (6 sprints)

```markdown
# Release Plan: E-commerce Platform v2.0

**Release Goal**: Launch new checkout system with multiple payment options
**Timeline**: Jan 1 - Mar 15, 2025 (6 sprints)
**Team**: 3 developers

## Sprints

### SPRINT-001: Payment Foundation
**Duration**: Jan 1 - Jan 14
**Goal**: Setup payment infrastructure and API integrations

**Tasks**:
- T-001: Stripe SDK integration [ ]
- T-002: Payment database schema design [ ]
- T-003: Payment API endpoints [ ]
- T-004: Shipping cost calculator [ ]

**Dependencies**: None

---

### SPRINT-002: Checkout UI
**Duration**: Jan 15 - Jan 28
**Goal**: Build responsive checkout flow

**Tasks**:
- T-005: Guest checkout form [ ]
- T-006: Address autosave feature [ ]
- T-007: Mobile responsive layout [ ]
- T-008: Form validation logic [ ]

**Dependencies**: Requires SPRINT-001 payment API (T-003)

---

### SPRINT-003: PayPal Integration
**Duration**: Jan 29 - Feb 11
**Goal**: Add PayPal as payment option

**Tasks**:
- T-009: PayPal SDK setup [ ]
- T-010: Payment method selector UI [ ]
- T-011: Order confirmation emails [ ]
- T-012: Transaction logging system [ ]

**Dependencies**: Requires SPRINT-001 infrastructure (T-002, T-003)

---

### SPRINT-004: Testing & Polish
**Duration**: Feb 12 - Feb 25
**Goal**: Ensure production readiness

**Tasks**:
- T-013: End-to-end testing suite [ ]
- T-014: Bug fixes from QA [ ]
- T-015: Performance optimization [ ]
- T-016: Security review and fixes [ ]

**Dependencies**: All features complete (T-001 through T-012)

---

### SPRINT-005: Beta Launch
**Duration**: Feb 26 - Mar 11
**Goal**: Soft launch to beta users

**Tasks**:
- T-017: Beta deployment to staging [ ]
- T-018: User feedback collection system [ ]
- T-019: Analytics and tracking setup [ ]
- T-020: Critical bug fixes [ ]

**Dependencies**: SPRINT-004 testing complete (T-013)

---

### SPRINT-006: Production Release
**Duration**: Mar 12 - Mar 15
**Goal**: Full production rollout

**Tasks**:
- T-021: Production deployment [ ]
- T-022: Monitoring and alerting setup [ ]
- T-023: User documentation [ ]
- T-024: Team handoff and training [ ]

**Dependencies**: Beta success metrics met (T-017, T-018)

## Roadmap

### Q1 2025
- **SPRINT-001**: Payment infrastructure complete
- **SPRINT-002**: Checkout UI launched
- **SPRINT-003**: PayPal support added
- **SPRINT-004**: Testing complete, production-ready
- **SPRINT-005**: Beta launch successful
- **SPRINT-006**: Full production release

## Milestones
- **Feb 25**: Alpha release (internal testing)
- **Feb 26**: Beta release (limited users)
- **Mar 12**: Production launch (all users)
```

### Example 2: Mobile App MVP (4 sprints)

```markdown
# Release Plan: Fitness Tracker App v1.0

**Release Goal**: Launch MVP with core tracking features
**Timeline**: 8 weeks (4 sprints)
**Team**: 2 developers

## Sprints

### SPRINT-001: User Foundation
**Duration**: Week 1-2
**Goal**: User accounts and authentication

**Tasks**:
- T-001: Firebase authentication setup [ ]
- T-002: User profile creation flow [ ]
- T-003: Profile editing functionality [ ]
- T-004: Avatar upload feature [ ]

### SPRINT-002: Activity Tracking
**Duration**: Week 3-4
**Goal**: Core fitness tracking features

**Tasks**:
- T-005: Step counter integration [ ]
- T-006: Manual activity logging interface [ ]
- T-007: Activity history view [ ]
- T-008: Basic statistics dashboard [ ]

### SPRINT-003: Data Visualization
**Duration**: Week 5-6
**Goal**: Charts and progress tracking

**Tasks**:
- T-009: Daily activity charts [ ]
- T-010: Weekly summary view [ ]
- T-011: Goal progress indicators [ ]
- T-012: Achievement badges system [ ]

### SPRINT-004: Launch Prep
**Duration**: Week 7-8
**Goal**: Polish and release

**Tasks**:
- T-013: App store assets creation [ ]
- T-014: Beta testing coordination [ ]
- T-015: Critical bug fixes [ ]
- T-016: Production deployment [ ]

## Roadmap

### Month 1
- SPRINT-001: User system live
- SPRINT-002: Activity tracking functional

### Month 2
- SPRINT-003: Data visualization complete
- SPRINT-004: MVP launched to app stores

## Milestones
- **Week 6**: Beta testing begins
- **Week 8**: App store submission
- **Week 9**: Public launch
```

## Reference Files

For more detailed guidance:
- **Sprint planning**: See [references/sprint-guide.md](references/sprint-guide.md)
- **Template**: See [references/template.md](references/template.md)

## When to Use

Use this skill when:
- Starting a new product release
- Planning quarterly roadmaps
- Breaking down large projects into sprints
- Communicating timelines to stakeholders
- Organizing backlog into time-boxed iterations
- Creating sprint schedules for agile teams
