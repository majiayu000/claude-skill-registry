---
name: faion-project-manager
user-invocable: false
description: "Project Manager role: PMBOK 7/8 (8 Performance Domains, 12 Principles), PM tools (Jira, ClickUp, Linear, GitHub Projects, Azure DevOps), risk/schedule/cost management, EVM, agile ceremonies, dashboards. 32 methodologies."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# PM Domain Skill

## References

| Reference | Content | Lines |
|-----------|---------|-------|
| [pm-tools.md](references/pm-tools.md) | Jira, ClickUp, Linear, GitHub Projects, GitLab, Azure DevOps, Notion, Trello, migrations, dashboards | ~1926 |

## Agents

| Agent | When to Use |
|-------|-------------|
| `faion-pm-agent` | Execute PMBOK 7/8 methodologies for project management |


**Communication: User's language. Docs/code: English.**

## Purpose

Orchestrates project management activities using PMBOK 7th Edition (2021) and PMBOK 8 principles. This domain skill provides professional PM methodologies for solopreneurs and teams.

## 3-Layer Architecture

```
Layer 1: Domain Skills (this) - orchestrators
    |
    v call
Layer 2: Agents - executors
    |
    v use
Layer 3: Technical Skills - tools
```

---

# PMBOK 7 Performance Domains (8)

Performance domains are interactive, interrelated, and interdependent areas of focus that work together throughout a project.

## PD-01: Stakeholder Performance Domain

**Focus:** Engaging stakeholders effectively throughout the project.

### Activities

1. **Identify stakeholders** - Who is affected by or can affect the project?
2. **Understand stakeholders** - Analyze interests, power, influence, expectations
3. **Engage stakeholders** - Develop appropriate engagement strategies
4. **Monitor engagement** - Track and adapt engagement effectiveness

### Outcomes

- Productive working relationship with stakeholders
- Stakeholder agreement on project objectives
- Stakeholders supportive of deliverables
- Stakeholders satisfied with outcomes

### Checking Results

| Indicator | What to Check |
|-----------|---------------|
| Engagement | Are stakeholders actively participating? |
| Satisfaction | Are expectations being met? |
| Conflict | Are issues resolved constructively? |
| Support | Do stakeholders advocate for the project? |

### Agent Integration

```
Call faion-pm-agent with:
  methodology: "M-PM-001" (Stakeholder Register)
  methodology: "M-PM-002" (Stakeholder Analysis Matrix)
```

---

## PD-02: Team Performance Domain

**Focus:** Building and leading high-performing teams.

### Activities

1. **Project manager leadership** - Set vision, inspire, remove obstacles
2. **Team development** - Build skills, foster collaboration
3. **Team culture** - Create psychological safety, shared values
4. **High-performing teams** - Enable autonomy, accountability

### Outcomes

- Shared ownership of project
- High-performing team
- Appropriate leadership demonstrated
- Team members grow and develop

### Team Development Stages

| Stage | Focus | Leader Action |
|-------|-------|---------------|
| Forming | Orientation | Direct, provide clarity |
| Storming | Conflict | Facilitate, resolve conflicts |
| Norming | Cohesion | Coach, enable collaboration |
| Performing | High function | Delegate, remove obstacles |
| Adjourning | Completion | Celebrate, transition |

### Agent Integration

```
Call faion-pm-agent with:
  methodology: "M-PM-003" (RACI Matrix)
  methodology: "M-PM-004" (Team Charter)
```

---

## PD-03: Development Approach and Life Cycle Performance Domain

**Focus:** Selecting and tailoring appropriate development approaches.

### Development Approaches

| Approach | When to Use | Characteristics |
|----------|-------------|-----------------|
| **Predictive** | Stable requirements, known solution | Sequential phases, upfront planning |
| **Iterative** | Unknown solution, needs refinement | Repeated cycles, prototype-based |
| **Incremental** | Needs early value delivery | Feature-based releases |
| **Agile** | High uncertainty, rapid change | Iterative + incremental, adaptive |
| **Hybrid** | Mixed needs | Combines approaches |

### Selection Factors

- Requirements stability
- Stakeholder availability
- Risk tolerance
- Regulatory constraints
- Team experience

### Life Cycle Phases

1. **Starting** - Authorization, initial scope
2. **Organizing and Preparing** - Planning, team formation
3. **Carrying Out** - Execution, monitoring
4. **Ending** - Closure, transition

### Agent Integration

```
Call faion-pm-agent with:
  methodology: "M-PM-005" (Development Approach Selection)
  methodology: "M-PM-006" (Project Life Cycle Design)
```

---

## PD-04: Planning Performance Domain

**Focus:** Organizing and elaborating how work will be done.

### Planning Components

| Component | Purpose | Key Activities |
|-----------|---------|----------------|
| **Scope** | What to deliver | WBS, requirements |
| **Schedule** | When to deliver | Sequencing, estimation |
| **Cost** | How much it costs | Budgeting, reserves |
| **Resources** | Who/what does work | Team, equipment, materials |
| **Quality** | How good enough | Standards, metrics |
| **Risk** | What could go wrong | Identification, response |
| **Communications** | How to share info | Channels, frequency |
| **Procurement** | What to buy | Contracts, vendors |
| **Stakeholder** | How to engage | Strategies, monitoring |

### Planning Progression

```
Progressive elaboration:
High-level --> Detailed --> Rolling wave

Uncertainty decreases as project progresses
```

### Estimation Techniques

| Technique | Accuracy | When to Use |
|-----------|----------|-------------|
| Analogous | Low | Early stages |
| Parametric | Medium | Historical data available |
| Bottom-up | High | Detailed scope defined |
| Three-point | Variable | Risk-aware estimation |

### Agent Integration

```
Call faion-pm-agent with:
  methodology: "M-PM-007" (WBS Creation)
  methodology: "M-PM-008" (Schedule Development)
  methodology: "M-PM-009" (Cost Estimation)
```

---

## PD-05: Project Work Performance Domain

**Focus:** Executing project activities to deliver outcomes.

### Activities

1. **Manage physical resources** - Equipment, materials, facilities
2. **Manage procurements** - Vendor relationships, contracts
3. **Monitor changes** - Track scope, schedule, cost variances
4. **Enable learning** - Capture and share knowledge
5. **Manage communications** - Information flow to stakeholders

### Project Work Processes

```
Plan -> Execute -> Monitor -> Adjust -> Repeat
        |                        ^
        +------------------------+
```

### Communication Matrix

| Stakeholder | What | When | How | Who |
|-------------|------|------|-----|-----|
| Sponsor | Status summary | Weekly | Email | PM |
| Team | Daily progress | Daily | Standup | PM |
| Customer | Milestone report | Monthly | Meeting | PM |

### Agent Integration

```
Call faion-pm-agent with:
  methodology: "M-PM-010" (Communication Management Plan)
  methodology: "M-PM-011" (Change Management Process)
```

---

## PD-06: Delivery Performance Domain

**Focus:** Delivering value and outcomes throughout the project.

### Value Delivery

| Concept | Description |
|---------|-------------|
| **Deliverables** | Outputs produced by project work |
| **Outcomes** | End results from using deliverables |
| **Benefits** | Gains realized from outcomes |
| **Value** | Worth to stakeholders |

### Delivery Approaches

| Approach | Delivery Timing | Examples |
|----------|-----------------|----------|
| Single delivery | End of project | Construction, one-time event |
| Multiple deliveries | Throughout project | Software releases, phases |
| Continuous delivery | Ongoing | SaaS features, content |

### Quality Management

```
Plan Quality -> Manage Quality -> Control Quality
     |               |                 |
     v               v                 v
  Standards     Prevention        Inspection
```

### Agent Integration

```
Call faion-pm-agent with:
  methodology: "M-PM-012" (Quality Management Plan)
  methodology: "M-PM-013" (Acceptance Criteria Definition)
```

---

## PD-07: Measurement Performance Domain

**Focus:** Tracking progress and performance.

### Key Metrics

| Category | Metrics |
|----------|---------|
| **Schedule** | SPI, variance, on-time % |
| **Cost** | CPI, variance, budget remaining |
| **Scope** | Requirements completed, defects |
| **Quality** | Defect rate, rework % |
| **Resources** | Utilization, productivity |
| **Stakeholder** | Satisfaction, engagement |

### Earned Value Management (EVM)

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **PV** | Planned Value | Budget for scheduled work |
| **EV** | Earned Value | Budget for completed work |
| **AC** | Actual Cost | Actual spend |
| **SV** | EV - PV | Schedule variance |
| **CV** | EV - AC | Cost variance |
| **SPI** | EV / PV | Schedule performance (>1 good) |
| **CPI** | EV / AC | Cost performance (>1 good) |
| **EAC** | BAC / CPI | Estimate at completion |

### Dashboard Elements

- Overall health indicator (RAG)
- Key performance metrics
- Trend analysis
- Risk status
- Milestone status

### Agent Integration

```
Call faion-pm-agent with:
  methodology: "M-PM-014" (Earned Value Management)
  methodology: "M-PM-015" (Project Dashboard Design)
```

---

## PD-08: Uncertainty Performance Domain

**Focus:** Navigating risks, ambiguity, and complexity.

### Types of Uncertainty

| Type | Description | Response |
|------|-------------|----------|
| **Risk** | Known unknowns, can estimate probability | Risk management |
| **Ambiguity** | Unclear understanding | Clarification, prototypes |
| **Complexity** | Interconnected systems | Systems thinking |
| **Volatility** | Rapid change | Flexibility, reserves |

### Risk Response Strategies

**For Threats:**
- **Avoid** - Eliminate the threat
- **Mitigate** - Reduce probability or impact
- **Transfer** - Shift to third party
- **Accept** - Acknowledge without action

**For Opportunities:**
- **Exploit** - Ensure realization
- **Enhance** - Increase probability or impact
- **Share** - Transfer to best positioned party
- **Accept** - Take advantage if occurs

### Risk Register

| ID | Risk | Probability | Impact | Score | Response | Owner |
|----|------|-------------|--------|-------|----------|-------|
| R1 | ... | H/M/L | H/M/L | P x I | Strategy | Name |

### Agent Integration

```
Call faion-pm-agent with:
  methodology: "M-PM-016" (Risk Register)
  methodology: "M-PM-017" (Risk Response Planning)
```

---

# PMBOK 7 Principles (12)

Principles guide behavior and decision-making throughout project work.

## P-01: Stewardship

**Statement:** Be a diligent, respectful, and caring steward.

**Application:**
- Act with integrity and ethics
- Consider broad impact of decisions
- Be accountable for resources
- Respect others and their perspectives

**Indicators:**
- Trust from stakeholders
- Ethical decision-making
- Resource efficiency
- Long-term thinking

---

## P-02: Team

**Statement:** Build a culture of accountability and respect.

**Application:**
- Foster collaborative environment
- Enable diverse perspectives
- Support individual and team growth
- Create psychological safety

**Team Health Check:**
- [ ] Members feel safe to speak up
- [ ] Conflicts resolved constructively
- [ ] Contributions recognized
- [ ] Learning encouraged

---

## P-03: Stakeholders

**Statement:** Engage stakeholders proactively.

**Application:**
- Identify all affected parties
- Understand expectations and influence
- Communicate appropriately
- Build and maintain relationships

**Engagement Levels:**
| Level | Description |
|-------|-------------|
| Unaware | Not aware of project |
| Resistant | Aware but opposed |
| Neutral | Aware, neither supportive nor resistant |
| Supportive | Aware and supportive |
| Leading | Actively engaged and championing |

---

## P-04: Value

**Statement:** Focus on value.

**Application:**
- Align project with business objectives
- Prioritize work that delivers value
- Measure outcomes, not just outputs
- Continuously reassess value

**Value Questions:**
- What problem are we solving?
- Who benefits and how?
- How do we measure success?
- What is the cost of not doing this?

---

## P-05: Systems Thinking

**Statement:** Recognize, evaluate, and respond to system dynamics.

**Application:**
- See the whole, not just parts
- Understand interdependencies
- Consider unintended consequences
- Optimize the system, not components

**Systems View:**
```
Internal: Project <-> Portfolio <-> Organization
External: Regulatory <-> Market <-> Technology <-> Society
```

---

## P-06: Leadership

**Statement:** Demonstrate leadership behaviors.

**Application:**
- Inspire and motivate
- Adapt style to situation
- Enable others to lead
- Model desired behaviors

**Leadership Styles:**
| Style | When to Use |
|-------|-------------|
| Directing | Low skill, high will |
| Coaching | Low skill, low will |
| Supporting | High skill, low will |
| Delegating | High skill, high will |

---

## P-07: Tailoring

**Statement:** Tailor based on context.

**Application:**
- Adapt processes to project needs
- Consider constraints and environment
- Balance rigor with agility
- Document tailoring decisions

**Tailoring Factors:**
- Project size and complexity
- Team experience
- Organizational culture
- Regulatory requirements
- Risk tolerance

---

## P-08: Quality

**Statement:** Build quality into processes and deliverables.

**Application:**
- Define quality standards upfront
- Prevent defects, don't just detect
- Integrate quality activities
- Continuously improve

**Quality Dimensions:**
- Performance (does it work?)
- Conformance (meets requirements?)
- Reliability (consistent?)
- Durability (long-lasting?)
- Serviceability (maintainable?)

---

## P-09: Complexity

**Statement:** Navigate complexity.

**Application:**
- Recognize complexity sources
- Use appropriate strategies
- Avoid oversimplification
- Embrace emergence when needed

**Complexity Sources:**
| Source | Example |
|--------|---------|
| Human behavior | Stakeholder politics |
| System behavior | Integration issues |
| Ambiguity | Unclear requirements |
| Technological | New or unproven tech |

---

## P-10: Risk

**Statement:** Optimize risk responses.

**Application:**
- Balance risk with reward
- Consider risk tolerance
- Address both threats and opportunities
- Maintain risk awareness

**Risk Appetite Levels:**
| Level | Characteristic |
|-------|----------------|
| Risk-averse | Prefer certainty, avoid threats |
| Risk-neutral | Balanced approach |
| Risk-seeking | Accept higher risk for higher reward |

---

## P-11: Adaptability and Resilience

**Statement:** Embrace adaptability and resilience.

**Application:**
- Build flexibility into plans
- Learn from experience
- Recover from setbacks
- Anticipate change

**Resilience Practices:**
- Short feedback cycles
- Reserve capacity
- Alternative strategies
- Continuous learning

---

## P-12: Change

**Statement:** Enable change to achieve the envisioned future state.

**Application:**
- Prepare stakeholders for change
- Address resistance constructively
- Sustain change through reinforcement
- Measure change adoption

**Change Readiness:**
- [ ] Clear vision communicated
- [ ] Stakeholders prepared
- [ ] Support systems in place
- [ ] Quick wins planned

---

# Methodologies (20)

## M-PM-001: Stakeholder Register

### Problem

Need to identify and track all project stakeholders with their characteristics and engagement approach.

### Framework

1. **Identify stakeholders**
   - Brainstorm with team
   - Review organization charts
   - Analyze contracts and agreements

2. **Analyze stakeholders**
   - Power/Interest grid
   - Influence/Impact matrix
   - Salience model (Power, Legitimacy, Urgency)

3. **Document in register**
   - Contact information
   - Role and relationship
   - Expectations and influence
   - Engagement strategy

### Template

| ID | Name | Role | Power | Interest | Current | Desired | Strategy |
|----|------|------|-------|----------|---------|---------|----------|
| S1 | ... | ... | H/M/L | H/M/L | Level | Level | Approach |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-002: Stakeholder Analysis Matrix

### Problem

Need to visualize stakeholder positioning for engagement planning.

### Framework

**Power/Interest Grid:**

```
         High Power
              |
    Keep      |    Manage
   Satisfied  |    Closely
              |
   -----------+----------- High Interest
              |
    Monitor   |    Keep
   (Minimum)  |   Informed
              |
         Low Power
```

### Template

| Quadrant | Stakeholders | Strategy |
|----------|--------------|----------|
| Manage Closely | High power, high interest | Active engagement |
| Keep Satisfied | High power, low interest | Periodic updates |
| Keep Informed | Low power, high interest | Regular communication |
| Monitor | Low power, low interest | Minimal effort |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-003: RACI Matrix

### Problem

Need to clarify roles and responsibilities for project activities.

### Framework

| Role | Meaning | Rules |
|------|---------|-------|
| **R** Responsible | Does the work | At least one per activity |
| **A** Accountable | Final authority | Exactly one per activity |
| **C** Consulted | Input before decision | Can be multiple |
| **I** Informed | Notified of outcome | Can be multiple |

### Template

| Activity | Role A | Role B | Role C | Role D |
|----------|--------|--------|--------|--------|
| Task 1 | A | R | C | I |
| Task 2 | A | R | - | I |
| Task 3 | A | C | R | I |

### Validation

- Each row has exactly one A
- Each row has at least one R
- A and R can be same person
- No role overload (too many Rs)

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-004: Team Charter

### Problem

Need to establish team agreements, norms, and working arrangements.

### Framework

1. **Team Purpose** - Why we exist
2. **Team Values** - What we stand for
3. **Working Agreements** - How we work
4. **Communication Norms** - How we communicate
5. **Decision Making** - How we decide
6. **Conflict Resolution** - How we resolve issues

### Template

```markdown
# Team Charter: [Project Name]

## Purpose
[One sentence describing team's mission]

## Values
- [Value 1]: [Description]
- [Value 2]: [Description]

## Working Agreements
- [ ] Core hours: [time range]
- [ ] Response time: [expectation]
- [ ] Meeting etiquette: [norms]

## Communication
| Type | Channel | Response Time |
|------|---------|---------------|
| Urgent | [channel] | [time] |
| Normal | [channel] | [time] |
| FYI | [channel] | [time] |

## Decision Making
[Process for making team decisions]

## Conflict Resolution
[Steps for resolving disagreements]

## Signatures
[Team member acknowledgments]
```

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-005: Development Approach Selection

### Problem

Need to choose the right development approach for the project context.

### Framework

**Assessment Questions:**

| Factor | Predictive | Agile |
|--------|-----------|-------|
| Requirements | Stable, well-defined | Evolving, emergent |
| Technology | Proven, familiar | New, experimental |
| Stakeholder availability | Limited | High |
| Team experience | Traditional PM | Agile methods |
| Risk tolerance | Low | High |
| Delivery frequency | Single | Continuous |

**Scoring:**
- Count factors favoring each approach
- Consider organizational constraints
- Hybrid if mixed results

### Template

| Factor | Score (1-5) | Favors |
|--------|-------------|--------|
| Requirements stability | | |
| Technology novelty | | |
| Stakeholder availability | | |
| Team agile experience | | |
| Regulatory constraints | | |
| Need for early delivery | | |
| **Total** | | **Recommendation** |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-006: Project Life Cycle Design

### Problem

Need to structure the project into phases with appropriate gates.

### Framework

**Phase Components:**
- Entry criteria
- Key activities
- Deliverables
- Exit criteria (gate)

**Common Patterns:**

| Pattern | Phases | Use Case |
|---------|--------|----------|
| Waterfall | Requirements -> Design -> Build -> Test -> Deploy | Stable requirements |
| Iterative | Concept -> [Elaborate -> Build -> Review]* -> Transition | Solution discovery |
| Incremental | [Plan -> Develop -> Release]* | Phased delivery |
| Agile | [Sprint]* | Continuous adaptation |

### Template

```markdown
# Project Life Cycle: [Project Name]

## Phase 1: [Name]
- Entry: [Criteria]
- Activities: [List]
- Deliverables: [List]
- Gate: [Decision criteria]

## Phase 2: [Name]
...
```

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-007: WBS Creation

### Problem

Need to decompose project scope into manageable work packages.

### Framework

**Decomposition Rules:**
1. 100% rule - WBS contains all work
2. Mutually exclusive - No overlap
3. Deliverable-oriented - Focus on outcomes
4. 8/80 rule - Work packages 8-80 hours

**Levels:**
1. Project
2. Deliverables / Phases
3. Sub-deliverables
4. Work Packages

### Template

```
1.0 Project Name
    1.1 Deliverable 1
        1.1.1 Sub-deliverable 1.1
            1.1.1.1 Work Package
            1.1.1.2 Work Package
        1.1.2 Sub-deliverable 1.2
    1.2 Deliverable 2
    1.3 Project Management
```

### Validation Checklist

- [ ] All scope included (100% rule)
- [ ] No overlapping work
- [ ] Consistent decomposition level
- [ ] Work packages are 8-80 hours
- [ ] Deliverable-oriented (nouns)

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-008: Schedule Development

### Problem

Need to create a realistic project schedule with dependencies.

### Framework

**Steps:**
1. Define activities (from WBS)
2. Sequence activities (dependencies)
3. Estimate durations
4. Develop schedule
5. Identify critical path

**Dependency Types:**
| Type | Meaning | Example |
|------|---------|---------|
| FS | Finish-to-Start | Code before test |
| FF | Finish-to-Finish | Parallel completion |
| SS | Start-to-Start | Parallel start |
| SF | Start-to-Finish | Rare, relief coverage |

**Estimation Methods:**
- Expert judgment
- Analogous (similar projects)
- Parametric (formula-based)
- Three-point (O + 4M + P) / 6

### Template

| ID | Activity | Duration | Predecessors | Start | End |
|----|----------|----------|--------------|-------|-----|
| A1 | ... | 5d | - | | |
| A2 | ... | 3d | A1 | | |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-009: Cost Estimation

### Problem

Need to estimate project costs accurately for budgeting.

### Framework

**Cost Categories:**
- Labor (internal, external)
- Materials and supplies
- Equipment (purchase, rental)
- Facilities
- Travel
- Reserves (contingency, management)

**Estimation Techniques:**

| Technique | Accuracy | Phase |
|-----------|----------|-------|
| Rough Order of Magnitude | -50% to +100% | Initiation |
| Budget Estimate | -10% to +25% | Planning |
| Definitive Estimate | -5% to +10% | Execution |

### Template

| WBS ID | Description | Labor | Materials | Other | Total |
|--------|-------------|-------|-----------|-------|-------|
| 1.1.1 | ... | $ | $ | $ | $ |
| | **Subtotal** | $ | $ | $ | $ |
| | **Contingency (%)** | | | | $ |
| | **Total Budget** | | | | $ |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-010: Communication Management Plan

### Problem

Need to ensure effective information flow to all stakeholders.

### Framework

**5 W's of Communication:**
- Who needs information?
- What information is needed?
- When is it needed?
- Where/how to deliver?
- Who is responsible?

### Template

| Stakeholder | Information | Frequency | Channel | Owner | Notes |
|-------------|-------------|-----------|---------|-------|-------|
| Sponsor | Status report | Weekly | Email | PM | |
| Team | Task updates | Daily | Standup | PM | |
| Customer | Milestone review | Monthly | Meeting | PM | |

### Communication Channels Formula

```
Channels = n(n-1) / 2
Where n = number of people

Example: 10 people = 45 channels
```

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-011: Change Management Process

### Problem

Need to control scope, schedule, and cost changes formally.

### Framework

**Change Control Process:**
1. Request submitted
2. Impact analyzed
3. Decision made (approve/reject/defer)
4. Update baseline if approved
5. Communicate decision

### Template

```markdown
# Change Request: [CR-XXX]

## Request Information
- Requested by: [Name]
- Date: [Date]
- Priority: High/Medium/Low

## Description
[What change is being requested]

## Justification
[Why the change is needed]

## Impact Analysis
- Scope: [Impact]
- Schedule: [+/- days]
- Cost: [+/- amount]
- Quality: [Impact]
- Risk: [New risks]

## Recommendation
[Approve/Reject/Defer]

## Decision
- Decision: [Approved/Rejected/Deferred]
- Decision maker: [Name]
- Date: [Date]
- Conditions: [If any]
```

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-012: Quality Management Plan

### Problem

Need to define quality standards and how to achieve them.

### Framework

**Quality Components:**
1. Quality Planning - Define standards
2. Quality Assurance - Process audits
3. Quality Control - Deliverable inspection

**Cost of Quality:**
| Type | Examples |
|------|----------|
| Prevention | Training, documentation, reviews |
| Appraisal | Testing, inspections, audits |
| Internal Failure | Rework, scrap, retesting |
| External Failure | Warranty, returns, reputation |

### Template

| Deliverable | Quality Standard | Metric | Target | Method |
|-------------|------------------|--------|--------|--------|
| Code | Code review passed | Review score | 4/5 | Peer review |
| Design | UX guidelines | Heuristic eval | 85% | Expert review |
| Docs | Style guide | Compliance % | 100% | Checklist |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-013: Acceptance Criteria Definition

### Problem

Need clear, testable criteria for deliverable acceptance.

### Framework

**SMART Criteria:**
- **S**pecific - Clear and unambiguous
- **M**easurable - Quantifiable
- **A**chievable - Realistic
- **R**elevant - Aligned with objectives
- **T**ime-bound - When to verify

### Template

| Requirement ID | Acceptance Criterion | Test Method | Pass/Fail |
|----------------|---------------------|-------------|-----------|
| REQ-001 | Response time < 200ms | Load test | |
| REQ-002 | 95% test coverage | CI report | |
| REQ-003 | Zero critical bugs | QA sign-off | |

### Acceptance Levels

| Level | Performed By | Purpose |
|-------|--------------|---------|
| Unit | Developer | Component works |
| Integration | QA | Components work together |
| System | QA | Full system works |
| User | Customer | Meets business needs |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-014: Earned Value Management

### Problem

Need integrated measurement of scope, schedule, and cost performance.

### Framework

**Core Metrics:**

| Metric | Formula | Meaning |
|--------|---------|---------|
| PV | Planned Value | Budgeted cost of scheduled work |
| EV | Earned Value | Budgeted cost of completed work |
| AC | Actual Cost | Actual cost of completed work |
| SV | EV - PV | Schedule variance |
| CV | EV - AC | Cost variance |
| SPI | EV / PV | Schedule Performance Index |
| CPI | EV / AC | Cost Performance Index |

**Forecasting:**

| Metric | Formula | Meaning |
|--------|---------|---------|
| EAC | BAC / CPI | Estimate at Completion |
| ETC | EAC - AC | Estimate to Complete |
| VAC | BAC - EAC | Variance at Completion |
| TCPI | (BAC-EV)/(BAC-AC) | To-Complete Performance Index |

**Interpretation:**

| Index | > 1 | = 1 | < 1 |
|-------|-----|-----|-----|
| SPI | Ahead | On track | Behind |
| CPI | Under budget | On budget | Over budget |

### Template

| Period | PV | EV | AC | SV | CV | SPI | CPI |
|--------|----|----|----|----|----|----|-----|
| Week 1 | | | | | | | |
| Week 2 | | | | | | | |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-015: Project Dashboard Design

### Problem

Need at-a-glance project health visualization for stakeholders.

### Framework

**Dashboard Sections:**
1. Overall Health (RAG status)
2. Key Metrics (schedule, cost, scope)
3. Milestone Status
4. Risk Summary
5. Action Items

**RAG Status:**
| Color | Status | Action |
|-------|--------|--------|
| Green | On track | Continue monitoring |
| Amber | At risk | Corrective action needed |
| Red | Off track | Escalation required |

### Template

```
+------------------+------------------+
|  OVERALL: GREEN  |  BUDGET: $XXX    |
+------------------+------------------+
|  Schedule: GREEN |  Cost: AMBER     |
|  Scope: GREEN    |  Quality: GREEN  |
+------------------+------------------+
|  MILESTONES                         |
|  [x] M1: Done    [ ] M2: In progress|
+------------------+------------------+
|  TOP RISKS                          |
|  R1: [desc] - AMBER                 |
+------------------+------------------+
|  ACTIONS                            |
|  A1: [action] - Due [date]          |
+-------------------------------------+
```

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-016: Risk Register

### Problem

Need to identify, assess, and track project risks systematically.

### Framework

**Risk Identification:**
- Brainstorming
- Checklists
- Interviews
- SWOT analysis
- Assumption analysis

**Risk Assessment:**

| Probability | Score |
|-------------|-------|
| Very High | 5 |
| High | 4 |
| Medium | 3 |
| Low | 2 |
| Very Low | 1 |

| Impact | Score |
|--------|-------|
| Catastrophic | 5 |
| Major | 4 |
| Moderate | 3 |
| Minor | 2 |
| Negligible | 1 |

**Risk Score = Probability x Impact**

### Template

| ID | Risk Description | Category | P | I | Score | Response | Owner | Status |
|----|------------------|----------|---|---|-------|----------|-------|--------|
| R1 | ... | Technical | 3 | 4 | 12 | Mitigate | Name | Open |
| R2 | ... | External | 2 | 5 | 10 | Transfer | Name | Open |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-017: Risk Response Planning

### Problem

Need to develop strategies and actions for identified risks.

### Framework

**Threat Responses:**

| Strategy | Action | When to Use |
|----------|--------|-------------|
| Avoid | Eliminate threat | High priority risks |
| Mitigate | Reduce P or I | Can influence factors |
| Transfer | Shift to third party | Insurance, contracts |
| Accept | Acknowledge | Low priority or unavoidable |

**Opportunity Responses:**

| Strategy | Action | When to Use |
|----------|--------|-------------|
| Exploit | Ensure realization | High value opportunities |
| Enhance | Increase P or I | Can influence factors |
| Share | Partner | Need capability/resources |
| Accept | Take if occurs | Low effort opportunities |

### Template

| Risk ID | Strategy | Response Actions | Trigger | Owner | Budget |
|---------|----------|------------------|---------|-------|--------|
| R1 | Mitigate | Train team on new tech | Start of project | PM | $5,000 |
| R2 | Transfer | Purchase insurance | Contract signing | Legal | $2,000 |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-018: Lessons Learned

### Problem

Need to capture and apply knowledge from project experience.

### Framework

**Collection Points:**
- End of each phase/sprint
- After significant events
- Project closure

**Categories:**
- What went well (continue)
- What went poorly (change)
- Recommendations (improve)

### Template

```markdown
# Lessons Learned: [Project/Phase]
Date: [Date]
Facilitator: [Name]

## What Went Well
| Item | Details | Recommendation |
|------|---------|----------------|
| | | Keep doing |

## What Went Poorly
| Item | Details | Root Cause | Recommendation |
|------|---------|------------|----------------|
| | | | Change process |

## Recommendations for Future Projects
| # | Recommendation | Priority | Owner |
|---|----------------|----------|-------|
| 1 | | High/Med/Low | |

## Attendees
[List of participants]
```

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-019: Project Closure Checklist

### Problem

Need to ensure proper project completion and transition.

### Framework

**Closure Activities:**
1. Verify deliverables accepted
2. Complete financial closure
3. Release resources
4. Archive documentation
5. Conduct lessons learned
6. Celebrate success
7. Administrative closure

### Template

| Activity | Status | Owner | Notes |
|----------|--------|-------|-------|
| All deliverables accepted | [ ] | PM | |
| Final payments processed | [ ] | Finance | |
| Team released | [ ] | PM | |
| Documentation archived | [ ] | PM | |
| Lessons learned captured | [ ] | PM | |
| Stakeholder communication | [ ] | PM | |
| Contracts closed | [ ] | Procurement | |
| Celebration held | [ ] | PM | |

### Agent

Execute with: `faion-pm-agent`

---

## M-PM-020: Project Status Report

### Problem

Need standardized format for communicating project status.

### Framework

**Report Sections:**
1. Executive Summary (RAG + key message)
2. Progress (completed, in progress, planned)
3. Schedule Status (milestone view)
4. Budget Status (actual vs planned)
5. Risks and Issues
6. Decisions Needed

### Template

```markdown
# Project Status Report
Project: [Name]
Period: [Start - End Date]
Author: [PM Name]

## Executive Summary
**Overall Status:** [GREEN/AMBER/RED]

[2-3 sentence summary of current state]

## Progress This Period
### Completed
- [Item 1]
- [Item 2]

### In Progress
- [Item 1] - [% complete]

### Planned Next Period
- [Item 1]

## Schedule
| Milestone | Planned | Forecast | Status |
|-----------|---------|----------|--------|
| M1 | [Date] | [Date] | GREEN |

## Budget
| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|
| Total | $X | $Y | $Z |

## Risks and Issues
| ID | Description | Status | Action |
|----|-------------|--------|--------|

## Decisions Needed
| # | Decision | By Whom | By When |
|---|----------|---------|---------|
```

### Agent

Execute with: `faion-pm-agent`

---

# Agents Called

| Agent | Purpose |
|-------|---------|
| faion-pm-agent | Executes PMBOK methodologies (M-PM-001 to M-PM-020) |

---

# Integration with Other Domain Skills

| Domain Skill | Integration Point |
|--------------|-------------------|
| faion-sdd-domain-skill | Task planning uses PMBOK scheduling |
| faion-ba-domain-skill | Requirements feed into PMBOK scope |
| faion-product-domain-skill | Product roadmap aligns with project schedule |
| faion-marketing-domain-skill | Campaign planning uses PMBOK methods |

---

*PM Domain Skill v2.0 - 2026-01-18*
*Based on PMBOK 7th Edition (2021) and PMBOK 8 updates*
*8 Performance Domains | 12 Principles | 32 Methodologies (M-PM + M-PMT)*
*Consolidated from: faion-pm-tools*


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-PM-001 | Stakeholder Engagement | [methodologies/M-PM-001_stakeholder_engagement.md](methodologies/M-PM-001_stakeholder_engagement.md) |
| M-PM-001 | Stakeholder Register | [methodologies/M-PM-001_stakeholder_register.md](methodologies/M-PM-001_stakeholder_register.md) |
| M-PM-002 | Raci Matrix | [methodologies/M-PM-002_raci_matrix.md](methodologies/M-PM-002_raci_matrix.md) |
| M-PM-003 | Wbs Creation | [methodologies/M-PM-003_wbs_creation.md](methodologies/M-PM-003_wbs_creation.md) |
| M-PM-003 | Work Breakdown Structure | [methodologies/M-PM-003_work_breakdown_structure.md](methodologies/M-PM-003_work_breakdown_structure.md) |
| M-PM-004 | Schedule Development | [methodologies/M-PM-004_schedule_development.md](methodologies/M-PM-004_schedule_development.md) |
| M-PM-005 | Cost Estimation | [methodologies/M-PM-005_cost_estimation.md](methodologies/M-PM-005_cost_estimation.md) |
| M-PM-006 | Risk Management | [methodologies/M-PM-006_risk_management.md](methodologies/M-PM-006_risk_management.md) |
| M-PM-006 | Risk Register | [methodologies/M-PM-006_risk_register.md](methodologies/M-PM-006_risk_register.md) |
| M-PM-007 | Earned Value Management | [methodologies/M-PM-007_earned_value_management.md](methodologies/M-PM-007_earned_value_management.md) |
| M-PM-008 | Change Control | [methodologies/M-PM-008_change_control.md](methodologies/M-PM-008_change_control.md) |
| M-PM-009 | Quality Management | [methodologies/M-PM-009_quality_management.md](methodologies/M-PM-009_quality_management.md) |
| M-PM-010 | Communications Management | [methodologies/M-PM-010_communications_management.md](methodologies/M-PM-010_communications_management.md) |
| M-PM-010 | Team Development | [methodologies/M-PM-010_team_development.md](methodologies/M-PM-010_team_development.md) |
| M-PM-011 | Project Integration | [methodologies/M-PM-011_project_integration.md](methodologies/M-PM-011_project_integration.md) |
| M-PM-012 | Agile Hybrid Approaches | [methodologies/M-PM-012_agile_hybrid_approaches.md](methodologies/M-PM-012_agile_hybrid_approaches.md) |
| M-PM-013 | Resource Management | [methodologies/M-PM-013_resource_management.md](methodologies/M-PM-013_resource_management.md) |
| M-PM-014 | Procurement Management | [methodologies/M-PM-014_procurement_management.md](methodologies/M-PM-014_procurement_management.md) |
| M-PM-015 | Lessons Learned | [methodologies/M-PM-015_lessons_learned.md](methodologies/M-PM-015_lessons_learned.md) |
| M-PM-016 | Benefits Realization | [methodologies/M-PM-016_benefits_realization.md](methodologies/M-PM-016_benefits_realization.md) |
| M-PM-017 | Project Closure | [methodologies/M-PM-017_project_closure.md](methodologies/M-PM-017_project_closure.md) |
| M-PM-018 | Stakeholder Engagement | [methodologies/M-PM-018_stakeholder_engagement.md](methodologies/M-PM-018_stakeholder_engagement.md) |
| M-PM-019 | Scope Management | [methodologies/M-PM-019_scope_management.md](methodologies/M-PM-019_scope_management.md) |
| M-PM-020 | Performance Domains Overview | [methodologies/M-PM-020_performance_domains_overview.md](methodologies/M-PM-020_performance_domains_overview.md) |
