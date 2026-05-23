---
name: project-planner
description: "Universal project planning for non-technical projects. Domains: business, personal, creative, academic, organizational, events. Capabilities: goal setting, milestone planning, resource allocation, timeline creation, risk assessment, progress tracking. Actions: create, plan, structure, breakdown, track projects. Keywords: project plan, roadmap, strategy, goal setting, milestones, timeline, action plan, project management, business plan, personal goals, creative project, academic planning, event planning, organizational change, OKRs, SMART goals, Gantt chart. Use when: creating project plans, setting goals/milestones, planning business initiatives, organizing events, structuring academic work, developing strategies/roadmaps."
auto_invoke: true
tags: [planning, project-management, strategy, goal-setting, action-plans, generic-planning]
---

# Project Planner Skill

Universal planning methodology for creating structured, actionable plans for any project type. Works for business initiatives, personal goals, creative projects, academic work, event planning, and organizational change.

## When to Use This Skill

Activate this skill when planning:
- **Business Projects**: Product launches, marketing campaigns, process improvements
- **Personal Goals**: Career development, learning objectives, lifestyle changes
- **Creative Projects**: Writing projects, art installations, content creation
- **Academic Work**: Research projects, thesis planning, study programs
- **Event Planning**: Conferences, weddings, community events
- **Organizational Change**: Restructuring, culture initiatives, policy changes

**NOT for software development** - Use `implementation-planner` skill instead

## Pre-Planning Protocol

**ALWAYS execute before creating new plan:**

1. **Check for active plan**:
   ```bash
   test -f docs/plan.md && cat docs/plan.md
   ```

2. **If active plan exists**:
   - Ask user: "Active plan found: [PLAN-ID]. Continue this plan or create new one?"
   - If continue: Load active plan and continue from current phase
   - If new: Mark current plan as paused/completed and create new

3. **If no active plan**:
   - Proceed with new plan creation

## Plan Format Standards

### Naming Convention
- **Format**: `PLAN-YYYYMMDD-HHMM-{project-slug}.md`
- **Example**: `PLAN-20251118-1430-product-launch.md`
- **Location**: `docs/plans/`

### Required Frontmatter
```yaml
---
plan_id: PLAN-YYYYMMDD-HHMM-{slug}
title: [Project Name]
created: YYYY-MM-DD HH:MM
status: draft | active | completed | on_hold | cancelled
category: business | personal | creative | academic | event | organizational
phase: planning | execution | monitoring | complete
priority: critical | high | medium | low
---
```

### Required Sections
1. **Vision & Objectives** - What and why
2. **Scope & Deliverables** - Specific outcomes
3. **Action Steps** - Sequenced tasks with owners
4. **Resources Required** - People, budget, materials, time
5. **Timeline & Milestones** - Deadlines and checkpoints
6. **Risks & Contingencies** - What could go wrong
7. **Success Metrics** - Measurable outcomes

## Master Plan Tracker (docs/plan.md)

Same structure as implementation-planner, tracks all project plans.

### Update Workflow

**When creating new plan:**
1. Generate plan file in `docs/plans/`
2. Update `docs/plan.md`:
   - Set `active_plan` to new plan ID
   - Add to appropriate category section
   - Update `last_updated` timestamp

**When completing plan:**
1. Update plan file `status: completed`
2. Update `docs/plan.md`:
   - Move to "Completed" with ✅
   - Update statistics

**When pausing plan:**
1. Update plan file `status: on_hold`
2. Update `docs/plan.md`:
   - Move to "On Hold" section
   - Clear `active_plan` if it was active

## Core Planning Principles

1. **Clarity over complexity** - Simple, understandable plans
2. **Action-oriented** - Every section leads to concrete actions
3. **Flexibility** - Plans adapt to changing circumstances
4. **Accountability** - Clear ownership and deadlines
5. **Measurable** - Success criteria are objective

## Planning Methodology

### Step 1: Vision & Objectives (< 5 minutes)

**Purpose**: Define what you want to achieve and why

**Questions to answer:**
- What is the desired end state?
- Why is this project important?
- Who benefits from this project?
- What problem does this solve?

**Output format:**
```markdown
## Vision & Objectives

### Vision Statement
[One paragraph describing the ideal outcome]

### Primary Objective
[Main goal - SMART format: Specific, Measurable, Achievable, Relevant, Time-bound]

### Secondary Objectives
- Objective 1: [SMART format]
- Objective 2: [SMART format]

### Alignment
- **Strategic Fit**: [How this aligns with broader goals]
- **Stakeholders**: [Who cares about this and why]
- **Value Proposition**: [Why now, why this approach]
```

### Step 2: Scope & Deliverables (< 5 minutes)

**Purpose**: Define boundaries and specific outputs

**Questions to answer:**
- What's included in this project?
- What's explicitly excluded?
- What tangible deliverables will we produce?
- What are the acceptance criteria?

**Output format:**
```markdown
## Scope & Deliverables

### In Scope
- [Specific activity/outcome 1]
- [Specific activity/outcome 2]

### Out of Scope
- [What we're NOT doing 1]
- [What we're NOT doing 2]

### Deliverables
1. **Deliverable 1**: [Description]
   - Acceptance Criteria: [How we know it's done]
   - Format: [Document, event, product, etc.]

2. **Deliverable 2**: [Description]
   - Acceptance Criteria: [How we know it's done]
   - Format: [Format]

### Constraints
- **Budget**: [Budget limitation]
- **Time**: [Time constraint]
- **Resources**: [Resource constraints]
- **Quality**: [Non-negotiable quality standards]
```

### Step 3: Action Steps (< 10 minutes)

**Purpose**: Break down work into executable tasks

**Sequencing principles:**
1. Dependencies first - Complete prerequisites before dependent tasks
2. Quick wins early - Build momentum with achievable tasks
3. Parallel work - Identify tasks that can happen simultaneously
4. Critical path - Highlight tasks that determine overall timeline

**Output format:**
```markdown
## Action Steps

### Phase 1: [Phase Name] (Weeks 1-2)

#### Step 1.1: [Action Verb] [What]
- **Description**: [What needs to be done]
- **Owner**: [Who is responsible]
- **Duration**: [Estimated time]
- **Dependencies**: [What must be done first]
- **Output**: [What this produces]
- **Verification**: [How to confirm completion]

#### Step 1.2: [Action Verb] [What]
[Same structure]

### Phase 2: [Phase Name] (Weeks 3-4)
[Continue with steps]

### Critical Path
Tasks that determine overall timeline:
1. Step X.X → Step Y.Y → Step Z.Z
```

### Step 4: Resources Required (< 5 minutes)

**Purpose**: Identify what's needed to execute

**Categories:**
- People: Skills, roles, time commitment
- Budget: Money for materials, services, licenses
- Materials: Physical items, equipment, supplies
- Time: Duration, deadlines, availability
- Knowledge: Training, expertise, information
- Tools: Software, platforms, systems

**Output format:**
```markdown
## Resources Required

### People
- **Role 1**: [Skills needed], [Time commitment], [Availability]
- **Role 2**: [Skills], [Time], [Availability]

### Budget
| Category | Item | Estimated Cost | Status |
|----------|------|----------------|--------|
| Materials | [Item] | $X,XXX | Approved/Pending |
| Services | [Service] | $X,XXX | Approved/Pending |

**Total Budget**: $X,XXX

### Materials & Equipment
- [Item 1]: [Quantity], [Specifications], [Source]
- [Item 2]: [Quantity], [Specifications], [Source]

### Knowledge & Training
- [Skill/Knowledge 1]: [Who needs it], [How to acquire]
- [Skill/Knowledge 2]: [Who needs it], [How to acquire]

### Tools & Systems
- [Tool 1]: [Purpose], [License/Access], [Cost]
- [Tool 2]: [Purpose], [License/Access], [Cost]
```

### Step 5: Timeline & Milestones (< 5 minutes)

**Purpose**: Set deadlines and create accountability

**Milestone criteria:**
- Significant progress point
- Measurable completion
- Enables next phase
- Stakeholder visibility

**Output format:**
```markdown
## Timeline & Milestones

### Overall Timeline
**Start Date**: YYYY-MM-DD
**End Date**: YYYY-MM-DD
**Total Duration**: [X weeks/months]

### Milestones

#### Milestone 1: [Name] - [Date]
- **Criteria**: [What must be complete]
- **Deliverables**: [What to show]
- **Checkpoint**: [Review meeting/decision point]

#### Milestone 2: [Name] - [Date]
[Same structure]

### Gantt Chart (Text-based)

```
Week 1  : [█████████░░░] Phase 1 (Step 1.1-1.3)
Week 2  : [░░░░█████████] Phase 1 (Step 1.4-1.6)
Week 3  : [█████████░░░] Phase 2 (Step 2.1-2.3)
Week 4  : [░░░░█████████] Phase 2 Complete
```

### Key Dates
- [YYYY-MM-DD]: [Event/Deadline]
- [YYYY-MM-DD]: [Event/Deadline]
```

### Step 6: Risks & Contingencies (< 5 minutes)

**Purpose**: Anticipate problems and plan responses

**Risk categories:**
- External: Market changes, regulations, competition
- Resource: Budget cuts, people unavailable, materials
- Technical: Complexity, dependencies, unknowns
- Stakeholder: Resistance, competing priorities, misalignment
- Timeline: Delays, scope creep, optimism bias

**Output format:**
```markdown
## Risks & Contingencies

### Risk 1: [Description]
**Category**: [External/Resource/Technical/Stakeholder/Timeline]
**Probability**: [High/Medium/Low]
**Impact**: [High/Medium/Low]
**Risk Score**: [Probability × Impact = Score]

**Mitigation**: [How to prevent]
**Contingency**: [What to do if it happens]
**Early Warning Signs**: [Indicators this is occurring]
**Owner**: [Who monitors this]

### Risk 2: [Description]
[Same structure]

### Risk Matrix

```
Impact
High   │ R3 │ R1 │ R1 │
Medium │ R5 │ R2 │ R1 │
Low    │ R7 │ R5 │ R2 │
       └────┴────┴────┘
         L   M   H
       Probability
```
```

### Step 7: Success Metrics (< 3 minutes)

**Purpose**: Define measurable outcomes

**SMART criteria:**
- Specific: Exact metric
- Measurable: Quantifiable
- Achievable: Realistic
- Relevant: Aligned with objectives
- Time-bound: By when

**Output format:**
```markdown
## Success Metrics

### Primary Metrics
- **Metric 1**: [Name]
  - **Target**: [Specific number/outcome]
  - **Measurement**: [How to measure]
  - **Frequency**: [How often to check]
  - **Baseline**: [Current state]

- **Metric 2**: [Name]
  [Same structure]

### Secondary Metrics
- [Metric 3]: [Target]
- [Metric 4]: [Target]

### Completion Criteria
- [ ] All deliverables accepted by stakeholders
- [ ] Primary metrics meet/exceed targets
- [ ] Budget within ±10% of estimate
- [ ] Timeline within ±10% of estimate
- [ ] Stakeholder satisfaction ≥ 8/10
- [ ] No critical issues remaining

### Post-Project Review
- **Review Date**: [2-4 weeks after completion]
- **Participants**: [Who attends]
- **Topics**: Lessons learned, metrics achieved, improvements
```

## Complete Plan Template

```markdown
---
plan_id: PLAN-YYYYMMDD-HHMM-{slug}
title: [Project Name]
created: YYYY-MM-DD HH:MM
status: draft
category: [business|personal|creative|academic|event|organizational]
phase: planning
priority: [critical|high|medium|low]
---

# 🎯 Project Plan: [Project Name]

## Vision & Objectives
[Vision statement and SMART objectives]

## Scope & Deliverables
[What's included, excluded, and delivered]

## Action Steps
[Phased, sequenced tasks with owners]

## Resources Required
[People, budget, materials, time, knowledge, tools]

## Timeline & Milestones
[Dates, milestones, Gantt chart]

## Risks & Contingencies
[Identified risks with mitigation strategies]

## Success Metrics
[Measurable outcomes and completion criteria]

## Notes & Considerations
[Additional context, assumptions, dependencies]
```

## Quality Standards

### Completeness
- All 7 sections present and filled
- Each action step has owner and deadline
- Resources are realistic and available
- Risks have mitigation plans
- Success metrics are SMART

### Clarity
- Anyone can understand the plan
- No jargon without explanation
- Concrete examples provided
- Ambiguity eliminated

### Actionability
- Next steps are clear
- Owners know what to do
- Timeline is realistic
- Resources are secured

## Common Project Types

### Business Project Example Triggers
- Product launch, marketing campaign, sales initiative
- Process improvement, efficiency project
- Market expansion, partnership development

### Personal Project Example Triggers
- Career transition, skill development
- Health/fitness goal, lifestyle change
- Financial goal, savings plan

### Creative Project Example Triggers
- Book/article writing, content creation
- Art project, exhibition planning
- Music production, album release

### Academic Project Example Triggers
- Research project, thesis planning
- Study program, exam preparation
- Conference presentation, paper publication

### Event Planning Example Triggers
- Conference/workshop organization
- Wedding/celebration planning
- Community event, fundraiser

### Organizational Change Example Triggers
- Team restructuring, role changes
- Culture initiative, value implementation
- Policy change, process adoption

## Continue Planning Workflow

**When user says "continue plan":**

1. **Load active plan** from `docs/plan.md`
2. **Check phase**:
   - Planning: Add details, refine sections
   - Execution: Update progress, mark steps complete
   - Monitoring: Review metrics, adjust timeline
3. **Update status** as work progresses

## Format Validation

**Before finalizing:**
- [ ] Frontmatter complete (plan_id, title, status, category, phase, priority)
- [ ] All 7 sections present
- [ ] Vision is inspiring and clear
- [ ] Objectives are SMART
- [ ] Action steps have owners and deadlines
- [ ] Resources identified and available
- [ ] Timeline is realistic
- [ ] Risks have contingencies
- [ ] Success metrics are measurable
- [ ] Master tracker updated

## Example Usage

**Scenario: Product Launch Plan**

User: "Create a plan for launching our new mobile app"

Claude:
1. Checks `docs/plan.md` - no active plan
2. Asks clarifying questions:
   - Who is the target audience?
   - What's the launch date goal?
   - What's the budget?
3. Creates `PLAN-20251118-1430-mobile-app-launch.md`:
   - Vision: Achieve 10K downloads in first month
   - Objectives: SMART goals for downloads, revenue, engagement
   - Scope: Features in v1.0, marketing channels, launch events
   - Action Steps: Development, testing, marketing, launch
   - Resources: Team roles, budget, tools
   - Timeline: 12-week timeline with milestones
   - Risks: Technical delays, market reception, competition
   - Metrics: Downloads, DAU, revenue, ratings
4. Updates `docs/plan.md` with active plan

**Scenario: Personal Learning Goal**

User: "Help me plan learning Python for data science"

Claude:
1. Checks for active plan
2. Creates structured learning plan:
   - Vision: Become job-ready data scientist in 6 months
   - Objectives: Complete courses, build portfolio projects
   - Scope: Topics to cover, projects to build
   - Action Steps: Weekly study schedule, hands-on practice
   - Resources: Courses, books, datasets, tools
   - Timeline: Month-by-month progression
   - Risks: Time management, motivation, difficulty
   - Metrics: Courses completed, projects finished, job applications

## Integration with Implementation Planner

**When planning involves software development:**

1. Use this skill for **overall project planning**:
   - Business objectives
   - Stakeholder management
   - Resource allocation
   - Timeline

2. Use `implementation-planner` for **technical implementation**:
   - Code architecture
   - File changes
   - Testing strategy
   - Deployment

3. **Cross-reference** plans:
   - Implementation plan referenced in technical deliverables
   - Project plan tracks implementation as one action step

---

**This skill creates actionable, complete plans for any project type while maintaining consistent format and tracking.**
