---
name: Agile Scrum
description: Comprehensive guide to Agile Scrum methodology including roles, ceremonies, artifacts, sprint planning, and best practices for iterative software development
---

# Agile Scrum

## What is Scrum?

**Scrum:** Agile framework for managing complex projects through iterative development in short cycles (sprints).

### Core Principles
```
Iterative: Work in short cycles (1-4 weeks)
Incremental: Deliver working software each sprint
Collaborative: Cross-functional teams
Adaptive: Respond to change quickly
Transparent: Visible progress and blockers
```

### Scrum vs Waterfall
```
Waterfall:
Requirements → Design → Development → Testing → Deployment
(6-12 months, all at once)

Scrum:
Sprint 1 → Sprint 2 → Sprint 3 → ...
(2 weeks each, continuous delivery)
```

---

## Scrum Roles

### Product Owner (PO)
**Responsibilities:**
- Define product vision
- Manage product backlog
- Prioritize features
- Accept/reject work
- Stakeholder communication

**Key Activities:**
```
- Write user stories
- Prioritize backlog
- Attend sprint planning
- Review sprint demos
- Make business decisions
```

### Scrum Master (SM)
**Responsibilities:**
- Facilitate Scrum ceremonies
- Remove impediments
- Coach team on Scrum
- Protect team from distractions
- Foster continuous improvement

**Key Activities:**
```
- Run daily standups
- Facilitate retrospectives
- Remove blockers
- Shield team from interruptions
- Promote Scrum values
```

**Not a Manager:**
```
❌ Assign tasks
❌ Manage performance
❌ Make technical decisions

✓ Facilitate
✓ Coach
✓ Remove obstacles
```

### Development Team
**Responsibilities:**
- Deliver working software
- Self-organize
- Estimate work
- Commit to sprint goals
- Continuously improve

**Characteristics:**
```
Cross-functional: All skills needed (dev, test, design)
Self-organizing: Decide how to do work
3-9 members: Small enough to be agile
Dedicated: Full-time on one team
```

---

## Scrum Artifacts

### Product Backlog
**Definition:** Prioritized list of all desired features and improvements

**Format:**
```
Priority | User Story                                    | Points | Status
---------|-----------------------------------------------|--------|--------
1        | As a user, I want to login with email         | 5      | Ready
2        | As a user, I want to reset my password        | 3      | Ready
3        | As a user, I want to update my profile        | 8      | Draft
4        | As an admin, I want to view user analytics    | 13     | Draft
```

**Characteristics:**
```
Dynamic: Constantly evolving
Prioritized: Most valuable items at top
Estimated: Story points assigned
Refined: Regularly groomed
```

### Sprint Backlog
**Definition:** Subset of product backlog committed to for current sprint

**Example:**
```
Sprint 15 (Jan 15 - Jan 28)
Goal: Complete user authentication

Stories:
☐ User login with email (5 points)
☐ Password reset (3 points)
☐ Email verification (5 points)
☐ Remember me functionality (3 points)

Total: 16 points
Team velocity: 15-20 points
```

### Increment
**Definition:** Sum of all completed product backlog items at end of sprint

**Criteria:**
```
Done: Meets Definition of Done
Working: Fully functional
Tested: All tests passing
Deployable: Could ship to production
```

---

## Scrum Ceremonies

### Sprint Planning
**When:** First day of sprint
**Duration:** 2-4 hours (for 2-week sprint)
**Attendees:** Entire Scrum team

**Agenda:**
```
Part 1: What will we deliver?
- Review product backlog
- Select stories for sprint
- Define sprint goal

Part 2: How will we do it?
- Break stories into tasks
- Estimate tasks
- Commit to sprint backlog
```

**Output:**
```
✓ Sprint goal
✓ Sprint backlog
✓ Team commitment
```

### Daily Standup
**When:** Every day, same time
**Duration:** 15 minutes (max)
**Attendees:** Development team (+ SM, PO optional)

**Format:**
```
Each team member answers:
1. What did I do yesterday?
2. What will I do today?
3. Any blockers?
```

**Example:**
```
John: "Yesterday I finished the login API. Today I'll work on 
       password reset. No blockers."

Jane: "Yesterday I worked on the UI. Today I'll continue. 
       Blocked on API documentation."

SM: "I'll get you that documentation after standup."
```

**Rules:**
```
✓ Stand up (keeps it short)
✓ Same time, same place
✓ Focus on progress and blockers
✓ Parking lot for detailed discussions

❌ Problem-solving (take offline)
❌ Status reports to manager
❌ Longer than 15 minutes
```

### Sprint Review (Demo)
**When:** Last day of sprint
**Duration:** 1-2 hours
**Attendees:** Scrum team + stakeholders

**Agenda:**
```
1. Review sprint goal
2. Demo completed work
3. Discuss what's done vs not done
4. Review updated product backlog
5. Discuss next steps
```

**Example:**
```
PO: "Our goal was to complete user authentication. Let me show you 
     what we built..."

[Demo of login, password reset, email verification]

Stakeholder: "Great! Can we add social login next sprint?"
PO: "I'll add it to the backlog and prioritize."
```

### Sprint Retrospective
**When:** After sprint review
**Duration:** 1-1.5 hours
**Attendees:** Scrum team only

**Format:**
```
1. What went well?
2. What didn't go well?
3. What will we improve?
```

**Example:**
```
Went Well:
+ Good collaboration between dev and design
+ All stories completed
+ No major blockers

Didn't Go Well:
- Too many meetings interrupted flow
- Unclear requirements on one story
- CI/CD pipeline was slow

Action Items:
→ Block focus time (no meetings 9-12am)
→ Refine stories better in backlog grooming
→ Optimize CI/CD pipeline (assign to John)
```

**Techniques:**
```
- Start/Stop/Continue
- Mad/Sad/Glad
- 4Ls (Liked, Learned, Lacked, Longed for)
- Sailboat (wind/anchor)
```

### Backlog Refinement (Grooming)
**When:** Mid-sprint
**Duration:** 1-2 hours
**Attendees:** Scrum team

**Activities:**
```
- Review upcoming stories
- Add details and acceptance criteria
- Estimate story points
- Split large stories
- Remove obsolete items
```

---

## User Stories

### Format
```
As a [role]
I want [feature]
So that [benefit]
```

### Examples
```
As a user
I want to reset my password
So that I can regain access if I forget it

As an admin
I want to view user analytics
So that I can understand user behavior
```

### Acceptance Criteria
```
User Story: Password reset

Acceptance Criteria:
✓ User can request reset via email
✓ Reset link expires after 24 hours
✓ User can set new password (min 8 chars)
✓ User receives confirmation email
✓ Old password no longer works
```

### INVEST Criteria
```
Independent: Can be developed separately
Negotiable: Details can be discussed
Valuable: Provides value to users
Estimable: Can be estimated
Small: Fits in one sprint
Testable: Can be verified
```

---

## Story Points and Estimation

### Story Points
**Definition:** Relative measure of effort, complexity, and uncertainty

**Not:**
```
❌ Hours or days
❌ Absolute measure
```

**Fibonacci Scale:**
```
1, 2, 3, 5, 8, 13, 21

1 = Trivial (change button text)
3 = Small (add form field)
5 = Medium (new API endpoint)
8 = Large (authentication system)
13 = Very large (payment integration)
21+ = Too large (split into smaller stories)
```

### Planning Poker
**Process:**
```
1. PO reads user story
2. Team discusses and asks questions
3. Each member selects estimate card (secretly)
4. All reveal cards simultaneously
5. Discuss differences (highest and lowest explain)
6. Re-estimate until consensus
```

**Example:**
```
Story: "Add password reset"

Estimates revealed: 3, 5, 5, 8

Discussion:
- Why 3? "Seems straightforward, we've done similar"
- Why 8? "Need to integrate with email service, handle edge cases"

Re-estimate: 5, 5, 5, 5 → Consensus: 5 points
```

---

## Velocity

### Definition
**Velocity:** Average story points completed per sprint

### Calculation
```
Sprint 1: 15 points
Sprint 2: 18 points
Sprint 3: 16 points

Average velocity: (15 + 18 + 16) / 3 = 16.3 points/sprint
```

### Usage
```
Use velocity to:
- Plan sprint capacity
- Forecast release dates
- Track team performance trends

Don't:
❌ Compare teams (different scales)
❌ Use as performance metric
❌ Pressure team to increase velocity
```

---

## Definition of Done (DoD)

### Purpose
**Shared understanding of what "done" means**

### Example DoD
```
A story is done when:
✓ Code written and reviewed
✓ Unit tests written and passing
✓ Integration tests passing
✓ Code merged to main branch
✓ Deployed to staging
✓ Acceptance criteria met
✓ Documentation updated
✓ Product Owner accepted
```

### Levels
```
Story Done: Meets story DoD
Sprint Done: All stories done + sprint goal met
Release Done: All sprints done + production ready
```

---

## Sprint Workflow

### Sprint Cycle (2 weeks)
```
Day 1: Sprint Planning (4 hours)
       - Select stories
       - Define sprint goal
       - Break into tasks

Day 2-9: Development
         - Daily standup (15 min)
         - Work on tasks
         - Update board

Day 5: Backlog Refinement (2 hours)
       - Groom upcoming stories

Day 10: Sprint Review (2 hours)
        - Demo completed work
        
        Sprint Retrospective (1.5 hours)
        - Discuss improvements

Day 11: Start next sprint
```

---

## Scrum Board

### Columns
```
To Do | In Progress | In Review | Done
------|-------------|-----------|-----
Story | Story       | Story     | Story
Story | Task        | Task      | Story
Task  |             |           | Task
```

### Example
```
To Do          | In Progress      | In Review        | Done
---------------|------------------|------------------|-------------
Password reset | Login UI         | Login API        | User signup
Email verify   | Password API     | Email templates  | Database setup
Profile update |                  |                  |
```

### Digital Tools
```
- Jira
- Trello
- Azure DevOps
- Linear
- Asana
```

---

## Common Metrics

### Burndown Chart
```
Story Points Remaining

40 |●
   |  ●
30 |    ●
   |      ●
20 |        ●
   |          ●
10 |            ●
   |              ●
0  |________________●
   Day 1  ...     Day 10

Ideal: Straight line from start to zero
Actual: May vary but should trend down
```

### Velocity Chart
```
Story Points

20 |     ■     ■     ■
   |   ■   ■       ■
15 | ■           ■
   |
10 |
   |_________________________
    S1  S2  S3  S4  S5  S6

Track: Average velocity over time
Goal: Stable, predictable velocity
```

### Cumulative Flow Diagram
```
Stories

40 |           Done
   |         In Review
30 |       In Progress
   |     To Do
20 |
   |
10 |
   |_________________________
    Week 1  Week 2  Week 3

Shows: Work distribution across states
Goal: Smooth flow, no bottlenecks
```

---

## Scaling Scrum

### Multiple Teams
```
Scrum of Scrums:
- Representatives from each team meet
- Discuss dependencies
- Coordinate work
- Remove cross-team blockers
```

### SAFe (Scaled Agile Framework)
```
Team Level: Scrum teams
Program Level: Agile Release Train (ART)
Portfolio Level: Strategic themes
```

### LeSS (Large-Scale Scrum)
```
One product backlog
One Product Owner
Multiple teams
Coordinated sprints
```

---

## Best Practices

### 1. Keep Sprints Consistent
```
✓ Same duration (2 weeks recommended)
✓ Same day of week
✓ Predictable rhythm
```

### 2. Protect the Sprint
```
✓ No scope changes mid-sprint
✓ PO shields team from distractions
✓ Focus on sprint goal
```

### 3. Maintain Sustainable Pace
```
✓ Don't overcommit
✓ Leave buffer for unknowns
✓ Avoid burnout
```

### 4. Embrace Change
```
✓ Adapt based on feedback
✓ Continuously improve
✓ Inspect and adapt
```

### 5. Focus on Value
```
✓ Prioritize high-value features
✓ Deliver working software
✓ Get user feedback early
```

---

## Common Pitfalls

### ❌ Scrum Theater
```
Going through motions without embracing values
- Standups become status reports
- Retrospectives don't lead to change
- Sprint planning is just task assignment
```

### ❌ Scope Creep
```
Adding work mid-sprint
- Breaks sprint commitment
- Reduces predictability
- Frustrates team
```

### ❌ Skipping Ceremonies
```
"We're too busy to do retrospectives"
- Misses improvement opportunities
- Repeats same mistakes
```

### ❌ Treating Scrum Master as Project Manager
```
SM assigns tasks and tracks hours
- Undermines self-organization
- Creates dependency
```

### ❌ Ignoring Definition of Done
```
"It's done except for tests"
- Accumulates technical debt
- Reduces quality
```

---

## Transitioning to Scrum

### Step 1: Training
```
- Scrum fundamentals for all
- Role-specific training
- Certified Scrum Master (CSM)
```

### Step 2: Form Teams
```
- Cross-functional teams
- Assign roles (PO, SM, Dev)
- Co-locate if possible
```

### Step 3: Create Backlog
```
- Gather requirements
- Write user stories
- Prioritize
- Estimate
```

### Step 4: Run First Sprint
```
- Keep it simple
- Focus on learning
- Expect mistakes
```

### Step 5: Inspect and Adapt
```
- Honest retrospectives
- Implement improvements
- Iterate on process
```

---

## Tools and Resources

### Project Management
```
- Jira (most popular)
- Azure DevOps
- Linear
- Trello
- Asana
```

### Estimation
```
- Planning Poker (app or cards)
- Scrum Poker Online
- PlanITpoker
```

### Retrospectives
```
- Retrium
- FunRetro
- Miro
- Metro Retro
```

### Learning
```
- Scrum Guide (official)
- Scrum Alliance
- Scrum.org
- Mountain Goat Software (Mike Cohn)
```

---

## Summary

**Scrum:** Agile framework for iterative development

**Roles:**
- Product Owner (what to build)
- Scrum Master (how to work)
- Development Team (build it)

**Artifacts:**
- Product Backlog (all work)
- Sprint Backlog (sprint work)
- Increment (done work)

**Ceremonies:**
- Sprint Planning (plan sprint)
- Daily Standup (sync daily)
- Sprint Review (demo work)
- Sprint Retrospective (improve)
- Backlog Refinement (prepare backlog)

**Key Concepts:**
- User stories (requirements)
- Story points (estimation)
- Velocity (capacity)
- Definition of Done (quality)
- Sprint (time-box)

**Benefits:**
- Faster time to market
- Higher quality
- Better adaptability
- Improved collaboration
- Continuous improvement

**Success Factors:**
- Committed team
- Empowered Product Owner
- Servant-leader Scrum Master
- Stakeholder support
- Continuous learning
