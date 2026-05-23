---
name: faion-business-analyst
user-invocable: false
description: "BA Domain Skill: IIBA BABOK v3 orchestrator. 6 Knowledge Areas (Planning, Elicitation, Analysis, Traceability, Evaluation, Management), requirements engineering, stakeholder analysis, process modeling, use cases, user stories. 30 tasks, competencies, techniques."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# BA Domain Skill

## Agents

| Agent | When to Use |
|-------|-------------|
| `faion-ba-agent` | Execute BABOK v3 methodologies for business analysis |


**Communication: User's language. Docs/code: English.**

## Purpose

Orchestrates business analysis activities following BABOK v3 (Guide to Business Analysis Body of Knowledge) standards from IIBA (International Institute of Business Analysis). This domain skill provides frameworks, techniques, and best practices for professional business analysis.

## Philosophy

**"Requirements are the foundation of successful solutions"** - Understanding stakeholder needs and translating them into actionable requirements is the core of business analysis.

## 3-Layer Architecture

```
Layer 1: Domain Skills (this) - orchestrators
    |
    v call
Layer 2: Agents (faion-ba-agent) - executors
    |
    v use
Layer 3: Technical Skills - tools
```

## BABOK v3 Core Concepts

### Business Analysis Definition

Business analysis is the practice of enabling change in an organizational context by defining needs and recommending solutions that deliver value to stakeholders.

### Key Concepts

| Concept | Definition |
|---------|------------|
| **Change** | Transformation in response to a need |
| **Need** | Problem or opportunity to address |
| **Solution** | Specific way of satisfying needs |
| **Stakeholder** | Individual/group with relationship to change |
| **Value** | Worth, importance, or usefulness |
| **Context** | Circumstances that influence change |

---

# Knowledge Area 1: Business Analysis Planning and Monitoring

## Overview

Defines the approach to performing business analysis, identifies stakeholders, plans governance, manages BA information, and identifies BA performance improvements.

## Tasks

### 1.1 Plan Business Analysis Approach

**Purpose:** Define how BA activities will be performed.

**Inputs:**
- Needs (external)
- Stakeholder engagement approach

**Elements:**
- Predictive vs adaptive approach selection
- Formality and level of detail
- Complexity and risk assessment
- Acceptance criteria definition

**Outputs:**
- Business analysis approach

**Technique:** M-BA-001 (BA Approach Planning)

### 1.2 Plan Stakeholder Engagement

**Purpose:** Understand stakeholders and plan how to work with them.

**Inputs:**
- Needs (external)
- Business analysis approach

**Elements:**
- Stakeholder list and characteristics
- Collaboration and communication needs
- Stakeholder roles and responsibilities

**Outputs:**
- Stakeholder engagement approach

**Technique:** M-BA-002 (Stakeholder Analysis)

### 1.3 Plan Business Analysis Governance

**Purpose:** Define how decisions are made about requirements and designs.

**Inputs:**
- Business analysis approach
- Stakeholder engagement approach

**Elements:**
- Decision-making process
- Change control process
- Prioritization approach
- Approval process

**Outputs:**
- Governance approach

**Technique:** M-BA-003 (Governance Framework)

### 1.4 Plan Business Analysis Information Management

**Purpose:** Define how BA information will be stored and accessed.

**Inputs:**
- Business analysis approach
- Governance approach

**Elements:**
- Information organization
- Level of abstraction and detail
- Traceability approach
- Reuse strategy
- Storage and access
- Requirements attributes

**Outputs:**
- Information management approach

### 1.5 Identify Business Analysis Performance Improvements

**Purpose:** Assess BA work performance and recommend improvements.

**Inputs:**
- BA performance assessment (external)

**Elements:**
- Performance analysis
- Assessment measures
- Root cause identification
- Improvement recommendations

**Outputs:**
- BA performance improvements

---

# Knowledge Area 2: Elicitation and Collaboration

## Overview

Describes the tasks BAs perform to obtain information from stakeholders and confirm the results. Central to understanding stakeholder needs.

## Tasks

### 2.1 Prepare for Elicitation

**Purpose:** Ensure effective elicitation by understanding scope and selecting appropriate techniques.

**Inputs:**
- Needs (external)
- Stakeholder engagement approach

**Elements:**
- Understanding the scope
- Selecting elicitation techniques
- Setting up logistics
- Securing resources
- Preparing supporting materials

**Outputs:**
- Elicitation activity plan

**Technique:** M-BA-004 (Elicitation Preparation)

### 2.2 Conduct Elicitation

**Purpose:** Draw out, explore, and identify information relevant to the change.

**Inputs:**
- Elicitation activity plan

**Elements:**
- Guide the elicitation activity
- Capture elicitation outputs
- Handle unexpected information

**Outputs:**
- Elicitation results (unconfirmed)

**Technique:** M-BA-005 (Elicitation Techniques)

### 2.3 Confirm Elicitation Results

**Purpose:** Check that stakeholder information is correctly understood.

**Inputs:**
- Elicitation results (unconfirmed)

**Elements:**
- Compare results against source information
- Compare results against other results
- Resolve conflicts

**Outputs:**
- Elicitation results (confirmed)

### 2.4 Communicate Business Analysis Information

**Purpose:** Ensure stakeholders have shared understanding of BA information.

**Inputs:**
- BA information (any)
- Stakeholder engagement approach

**Elements:**
- Determine objectives and format
- Communicate BA package
- Confirm understanding

**Outputs:**
- BA communication

**Technique:** M-BA-006 (Communication Planning)

### 2.5 Manage Stakeholder Collaboration

**Purpose:** Encourage stakeholders to work together to meet their needs.

**Inputs:**
- Stakeholder engagement approach
- BA communication

**Elements:**
- Gain agreement on commitments
- Monitor engagement
- Manage collaboration

**Outputs:**
- Stakeholder engagement (updated)

---

# Knowledge Area 3: Requirements Life Cycle Management

## Overview

Describes the tasks to manage and maintain requirements and design information throughout the solution life cycle.

## Tasks

### 3.1 Trace Requirements

**Purpose:** Ensure requirements and designs are aligned at different levels.

**Inputs:**
- Requirements (any)
- Designs (any)

**Elements:**
- Level of formality
- Relationships
- Traceability matrix

**Outputs:**
- Requirements (traced)

**Technique:** M-BA-007 (Requirements Traceability)

### 3.2 Maintain Requirements

**Purpose:** Keep requirements accurate and consistent over time.

**Inputs:**
- Requirements (any)

**Elements:**
- Maintaining requirements attributes
- Reusing requirements
- Maintaining requirements versions

**Outputs:**
- Requirements (maintained)

**Technique:** M-BA-008 (Requirements Maintenance)

### 3.3 Prioritize Requirements

**Purpose:** Rank requirements in relative importance.

**Inputs:**
- Requirements (any)
- Designs (any)

**Elements:**
- Basis for prioritization
- Challenges in prioritization
- Continual prioritization

**Outputs:**
- Requirements (prioritized)

**Technique:** M-BA-009 (Requirements Prioritization)

### 3.4 Assess Requirements Changes

**Purpose:** Evaluate proposed changes to requirements and designs.

**Inputs:**
- Proposed change (external)
- Requirements (any)

**Elements:**
- Assess change formality
- Change impact analysis
- Change resolution

**Outputs:**
- Requirements change assessment

**Technique:** M-BA-010 (Change Impact Analysis)

### 3.5 Approve Requirements

**Purpose:** Obtain agreement and approval of requirements.

**Inputs:**
- Requirements (verified, validated)

**Elements:**
- Understand stakeholder roles
- Manage conflicts
- Gain consensus
- Track and communicate approval

**Outputs:**
- Requirements (approved)

---

# Knowledge Area 4: Strategy Analysis

## Overview

Focuses on defining the future state needed to address business needs and determining the work necessary to reach that state.

## Tasks

### 4.1 Analyze Current State

**Purpose:** Understand the existing enterprise environment and identify needs.

**Inputs:**
- Needs (external)
- Elicitation results (confirmed)

**Elements:**
- Business needs analysis
- Organizational assessment
- Capability assessment
- Technology/infrastructure assessment
- Policies, procedures, rules
- Business architecture

**Outputs:**
- Current state description

**Technique:** M-BA-011 (Current State Analysis)

### 4.2 Define Future State

**Purpose:** Define goals and objectives for the future state.

**Inputs:**
- Current state description
- Elicitation results (confirmed)

**Elements:**
- Business goals and objectives
- Potential value
- New capabilities
- Assumptions and constraints
- Dependencies

**Outputs:**
- Future state description

**Technique:** M-BA-012 (Future State Definition)

### 4.3 Assess Risks

**Purpose:** Identify uncertainties and understand their potential impact.

**Inputs:**
- Current state description
- Future state description
- Change strategy

**Elements:**
- Unknown factors
- Constraints, assumptions, dependencies
- Negative impact
- Positive impact (opportunities)
- Risk tolerance

**Outputs:**
- Risk assessment results

**Technique:** M-BA-013 (Risk Analysis)

### 4.4 Define Change Strategy

**Purpose:** Develop and assess alternative change strategies.

**Inputs:**
- Current state description
- Future state description
- Risk assessment results

**Elements:**
- Solution scope
- Gap analysis
- Enterprise readiness assessment
- Change strategy formulation

**Outputs:**
- Change strategy

**Technique:** M-BA-014 (Change Strategy Planning)

---

# Knowledge Area 5: Requirements Analysis and Design Definition

## Overview

Describes how to structure requirements and design, specify and model requirements, verify and validate information, and identify solution options.

## Tasks

### 5.1 Specify and Model Requirements

**Purpose:** Analyze, synthesize, and refine elicitation results into requirements.

**Inputs:**
- Elicitation results (confirmed)
- Requirements (any)

**Elements:**
- Model requirements
- Analyze requirements
- Represent requirements and attributes
- Implement appropriate levels of abstraction

**Outputs:**
- Requirements (specified and modeled)

**Technique:** M-BA-015 (Requirements Modeling)

### 5.2 Verify Requirements

**Purpose:** Ensure requirements meet quality standards and are usable.

**Inputs:**
- Requirements (any)

**Elements:**
- Characteristics of quality requirements:
  - Atomic, complete, consistent
  - Concise, feasible, unambiguous
  - Testable, prioritized, understandable

**Outputs:**
- Requirements (verified)

### 5.3 Validate Requirements

**Purpose:** Ensure requirements align with business goals and stakeholder needs.

**Inputs:**
- Requirements (verified)
- Business goals and objectives

**Elements:**
- Alignment with business objectives
- Stakeholder agreement
- Suitability for purpose

**Outputs:**
- Requirements (validated)

### 5.4 Define Requirements Architecture

**Purpose:** Ensure requirements support each other and the overall solution.

**Inputs:**
- Requirements (any)

**Elements:**
- Requirements viewpoints
- Information architecture templates
- Requirement relationships and dependencies
- Completeness assessment

**Outputs:**
- Requirements architecture

**Technique:** M-BA-016 (Requirements Architecture)

### 5.5 Define Design Options

**Purpose:** Define solution approaches that meet requirements.

**Inputs:**
- Requirements (any)
- Solution scope

**Elements:**
- Define solution approaches
- Identify improvement opportunities
- Allocate requirements

**Outputs:**
- Design options

### 5.6 Analyze Potential Value and Recommend Solution

**Purpose:** Assess design options and recommend most appropriate solution.

**Inputs:**
- Design options
- Requirements (any)
- Change strategy

**Elements:**
- Expected benefits analysis
- Expected costs analysis
- Value assessment
- Recommendation and justification

**Outputs:**
- Solution recommendation

**Technique:** M-BA-017 (Solution Options Analysis)

---

# Knowledge Area 6: Solution Evaluation

## Overview

Assesses the performance of a solution and the value delivered, recommending improvements when necessary.

## Tasks

### 6.1 Measure Solution Performance

**Purpose:** Define how solution performance will be measured.

**Inputs:**
- Solution (constructed)
- Potential value

**Elements:**
- Define performance measures
- Validate measures
- Collect performance data

**Outputs:**
- Solution performance measures

### 6.2 Analyze Performance Measures

**Purpose:** Examine performance data against expected value.

**Inputs:**
- Solution performance measures
- Potential value

**Elements:**
- Compare to expected value
- Identify variances
- Identify contributing factors

**Outputs:**
- Solution performance analysis

### 6.3 Assess Solution Limitations

**Purpose:** Investigate problems with a solution to understand causes.

**Inputs:**
- Solution performance analysis

**Elements:**
- Identify defects and issues
- Internal limitation assessment
- Stakeholder impact analysis

**Outputs:**
- Solution limitations

**Technique:** M-BA-018 (Solution Limitation Assessment)

### 6.4 Assess Enterprise Limitations

**Purpose:** Investigate how enterprise factors impact solution value.

**Inputs:**
- Solution performance analysis

**Elements:**
- Cultural issues
- Operational and process issues
- Technical issues
- Stakeholder issues

**Outputs:**
- Enterprise limitations

### 6.5 Recommend Actions to Increase Solution Value

**Purpose:** Identify and define actions that could increase solution value.

**Inputs:**
- Solution limitations
- Enterprise limitations

**Elements:**
- Analyze options
- Recommend actions
- Define scope of change

**Outputs:**
- Value improvement recommendations

---

# Embedded Methodologies (18)

## M-BA-001: BA Approach Planning

### Problem
How to determine the right business analysis approach for a specific initiative?

### Framework
1. **Assess Initiative Type**
   - Predictive (Waterfall) vs Adaptive (Agile)
   - Complexity and risk level
   - Stakeholder availability

2. **Define Formality Level**
   - High: Regulated industries, large teams
   - Medium: Standard enterprise projects
   - Low: Startups, rapid prototyping

3. **Select Deliverables**
   - Required artifacts
   - Level of detail
   - Review cadence

4. **Plan Activities**
   - Elicitation schedule
   - Analysis iterations
   - Validation checkpoints

### Templates
```markdown
## BA Approach Document

### Initiative Overview
- Name: {initiative}
- Type: {predictive/adaptive/hybrid}
- Duration: {estimated}

### Approach Selection
| Factor | Assessment | Implication |
|--------|------------|-------------|
| Complexity | {H/M/L} | {impact} |
| Uncertainty | {H/M/L} | {impact} |
| Risk tolerance | {H/M/L} | {impact} |

### Deliverables
| Artifact | Format | Audience |
|----------|--------|----------|
| Requirements Doc | {format} | {who} |

### Activity Plan
| Phase | Activities | Duration |
|-------|------------|----------|
| Discovery | {activities} | {weeks} |
```

### Agent
faion-ba-agent

---

## M-BA-002: Stakeholder Analysis

### Problem
How to identify, analyze, and plan engagement with stakeholders?

### Framework
1. **Identify Stakeholders**
   - Organizational chart analysis
   - Role identification
   - Interest group mapping

2. **Analyze Stakeholders**
   - Power/influence assessment
   - Interest level
   - Attitude toward change
   - Knowledge level

3. **Map Stakeholders**
   - Power/Interest matrix
   - Engagement strategy per quadrant

4. **Plan Engagement**
   - Communication frequency
   - Preferred channels
   - Key messages

### Templates
```markdown
## Stakeholder Analysis Matrix

| Stakeholder | Role | Power | Interest | Attitude | Strategy |
|-------------|------|-------|----------|----------|----------|
| {name} | {role} | H/M/L | H/M/L | +/0/- | {approach} |

## Power/Interest Grid

          High Interest
              ^
    Manage   |   Collaborate
    Closely  |   Closely
    ---------+----------> High Power
    Monitor  |   Keep
    Only     |   Informed
              Low Interest
```

### Agent
faion-ba-agent

---

## M-BA-003: Governance Framework

### Problem
How to establish decision-making processes for requirements?

### Framework
1. **Define Decision Rights**
   - Who can approve requirements?
   - Escalation paths
   - Consensus vs authority

2. **Establish Change Control**
   - Change request process
   - Impact assessment requirements
   - Approval thresholds

3. **Set Prioritization Rules**
   - Criteria for prioritization
   - Weighting factors
   - Tie-breaking rules

4. **Document Approval Process**
   - Sign-off requirements
   - Documentation standards
   - Audit trail

### Templates
```markdown
## Governance Framework

### Decision Authority Matrix
| Decision Type | Authority Level | Escalation |
|---------------|-----------------|------------|
| New requirement | BA Lead | PM |
| Scope change | Steering Committee | Sponsor |
| Priority change | Product Owner | PM |

### Change Control Process
1. Submit change request
2. Impact assessment (T-shirt sizing)
3. Review by {authority}
4. Approve/Reject/Defer
5. Update requirements baseline
```

### Agent
faion-ba-agent

---

## M-BA-004: Elicitation Preparation

### Problem
How to prepare effectively for elicitation activities?

### Framework
1. **Define Scope**
   - What information is needed?
   - What decisions will be made?
   - What is out of scope?

2. **Select Techniques**
   - Match technique to information type
   - Consider stakeholder preferences
   - Plan technique combinations

3. **Prepare Logistics**
   - Schedule sessions
   - Book resources
   - Prepare environment

4. **Create Materials**
   - Question guides
   - Visual aids
   - Prototypes/mockups

### Technique Selection Guide

| Information Type | Recommended Techniques |
|-----------------|------------------------|
| Current state | Observation, Document analysis |
| Pain points | Interviews, Focus groups |
| Requirements | Workshops, Prototyping |
| Validation | Reviews, Walkthroughs |

### Agent
faion-ba-agent

---

## M-BA-005: Elicitation Techniques

### Problem
How to effectively draw out information from stakeholders?

### Framework

**Primary Techniques:**

1. **Interviews**
   - One-on-one conversations
   - Structured, semi-structured, unstructured
   - Best for: detailed information, sensitive topics

2. **Workshops**
   - Group facilitation
   - Collaborative decision-making
   - Best for: consensus building, complex requirements

3. **Observation**
   - Active or passive watching
   - Understanding actual vs stated behavior
   - Best for: process understanding, as-is state

4. **Document Analysis**
   - Review existing documentation
   - Understand current state
   - Best for: legacy system analysis

5. **Surveys/Questionnaires**
   - Structured data collection
   - Large audience reach
   - Best for: quantitative data, validation

6. **Prototyping**
   - Visual representation
   - Iterative refinement
   - Best for: UI/UX requirements, validation

7. **Brainstorming**
   - Idea generation
   - No judgment initially
   - Best for: innovation, options exploration

### Agent
faion-ba-agent

---

## M-BA-006: Communication Planning

### Problem
How to ensure effective communication of BA information?

### Framework
1. **Audience Analysis**
   - Who needs what information?
   - Preferred format and channel
   - Frequency requirements

2. **Message Design**
   - Key points to convey
   - Level of detail
   - Supporting materials

3. **Channel Selection**
   - Formal vs informal
   - Written vs verbal
   - Synchronous vs asynchronous

4. **Feedback Mechanism**
   - How to confirm understanding
   - Follow-up process
   - Issue resolution

### Templates
```markdown
## Communication Plan

### Audience Matrix
| Audience | Information | Format | Frequency | Channel |
|----------|-------------|--------|-----------|---------|
| Sponsor | Status, risks | Summary | Weekly | Email |
| Dev team | Detailed reqs | Full doc | Per sprint | Jira |

### Key Messages
1. {message 1}
2. {message 2}
```

### Agent
faion-ba-agent

---

## M-BA-007: Requirements Traceability

### Problem
How to track requirements relationships and ensure coverage?

### Framework
1. **Define Trace Levels**
   - Business goals to stakeholder requirements
   - Stakeholder requirements to solution requirements
   - Solution requirements to design/test

2. **Establish Relationships**
   - Derive (parent-child)
   - Satisfy (requirement to design)
   - Verify (requirement to test)
   - Depend (prerequisite)

3. **Create Traceability Matrix**
   - Forward traceability (goals to implementation)
   - Backward traceability (implementation to goals)

4. **Maintain Traces**
   - Update on changes
   - Impact analysis
   - Coverage analysis

### Templates
```markdown
## Traceability Matrix

| Business Goal | Stakeholder Req | Solution Req | Design | Test |
|--------------|-----------------|--------------|--------|------|
| BG-001 | SR-001, SR-002 | SOL-001 | D-001 | TC-001 |
| BG-002 | SR-003 | SOL-002, SOL-003 | D-002 | TC-002 |

## Coverage Analysis
- Requirements with design: 95%
- Requirements with tests: 90%
- Orphan requirements: 2
```

### Agent
faion-ba-agent

---

## M-BA-008: Requirements Maintenance

### Problem
How to keep requirements accurate and useful over time?

### Framework
1. **Version Control**
   - Baseline management
   - Change history tracking
   - Branch/merge strategies

2. **Attribute Management**
   - Status (draft, approved, implemented)
   - Priority
   - Owner
   - Source

3. **Quality Monitoring**
   - Periodic reviews
   - Consistency checks
   - Completeness validation

4. **Archival Strategy**
   - When to archive
   - What to retain
   - Access policies

### Agent
faion-ba-agent

---

## M-BA-009: Requirements Prioritization

### Problem
How to rank requirements by importance?

### Framework

**Prioritization Techniques:**

1. **MoSCoW**
   - Must have, Should have, Could have, Won't have
   - Quick, intuitive
   - Good for: initial triage

2. **RICE**
   - Reach, Impact, Confidence, Effort
   - Quantitative scoring
   - Good for: product backlog

3. **Value vs Effort Matrix**
   - 2x2 grid analysis
   - Quick wins identification
   - Good for: sprint planning

4. **Kano Model**
   - Basic, Performance, Delighters
   - Customer satisfaction focus
   - Good for: customer-facing features

5. **Weighted Scoring**
   - Multiple criteria with weights
   - Objective comparison
   - Good for: complex decisions

### Templates
```markdown
## MoSCoW Prioritization

| Requirement | Priority | Rationale |
|-------------|----------|-----------|
| REQ-001 | Must | Core functionality |
| REQ-002 | Should | Important but deferrable |
| REQ-003 | Could | Nice to have |
| REQ-004 | Won't | Out of scope for MVP |
```

### Agent
faion-ba-agent

---

## M-BA-010: Change Impact Analysis

### Problem
How to assess the impact of proposed requirement changes?

### Framework
1. **Scope Assessment**
   - What requirements are affected?
   - What designs are affected?
   - What tests are affected?

2. **Effort Assessment**
   - Development effort
   - Testing effort
   - Documentation updates

3. **Risk Assessment**
   - Technical risks
   - Schedule risks
   - Quality risks

4. **Stakeholder Impact**
   - Who is affected?
   - Training needs
   - Communication needs

5. **Decision Support**
   - Options analysis
   - Recommendation
   - Trade-offs

### Templates
```markdown
## Change Impact Analysis

### Change Request: {CR-ID}
**Description:** {change description}

### Impact Assessment
| Area | Impact | Effort |
|------|--------|--------|
| Requirements | {count} reqs affected | {hours} |
| Design | {components} | {hours} |
| Code | {modules} | {hours} |
| Tests | {test cases} | {hours} |
| **Total** | | **{total hours}** |

### Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {risk} | H/M/L | H/M/L | {action} |

### Recommendation
{Accept/Reject/Defer} because {rationale}
```

### Agent
faion-ba-agent

---

## M-BA-011: Current State Analysis

### Problem
How to understand the existing environment and identify needs?

### Framework
1. **Business Context**
   - Organizational structure
   - Business processes
   - Strategic goals

2. **Capability Assessment**
   - Current capabilities
   - Capability gaps
   - Maturity levels

3. **Technology Landscape**
   - Current systems
   - Integration points
   - Technical debt

4. **Stakeholder Landscape**
   - Key players
   - Pain points
   - Success metrics

5. **SWOT Analysis**
   - Strengths
   - Weaknesses
   - Opportunities
   - Threats

### Templates
```markdown
## Current State Assessment

### Business Context
- Organization: {description}
- Core processes: {list}
- Strategic alignment: {goals}

### Capability Assessment
| Capability | Current State | Target State | Gap |
|------------|--------------|--------------|-----|
| {cap} | {level 1-5} | {level 1-5} | {delta} |

### Pain Points
1. {pain point 1}
2. {pain point 2}

### SWOT
| Strengths | Weaknesses |
|-----------|------------|
| {s1} | {w1} |

| Opportunities | Threats |
|---------------|---------|
| {o1} | {t1} |
```

### Agent
faion-ba-agent

---

## M-BA-012: Future State Definition

### Problem
How to define the desired future state?

### Framework
1. **Vision Statement**
   - Clear, compelling description
   - Stakeholder-aligned
   - Measurable outcomes

2. **Goals and Objectives**
   - SMART criteria
   - Aligned with strategy
   - Prioritized

3. **New Capabilities**
   - Required capabilities
   - Capability improvements
   - Capability retirements

4. **Success Metrics**
   - KPIs definition
   - Baseline vs target
   - Measurement approach

5. **Constraints and Assumptions**
   - Budget limitations
   - Timeline constraints
   - Technical constraints
   - Assumptions to validate

### Templates
```markdown
## Future State Vision

### Vision Statement
{compelling description of future state}

### Goals and Objectives
| Goal | Objective | Metric | Target |
|------|-----------|--------|--------|
| {G1} | {O1} | {KPI} | {value} |

### Capability Roadmap
| Capability | Current | Future | Timeline |
|------------|---------|--------|----------|
| {cap} | Level 2 | Level 4 | Q3 2026 |

### Constraints
- Budget: {amount}
- Timeline: {deadline}
- Technology: {constraints}

### Assumptions
1. {assumption 1} - Validated: Yes/No
2. {assumption 2} - Validated: Yes/No
```

### Agent
faion-ba-agent

---

## M-BA-013: Risk Analysis

### Problem
How to identify and assess risks to the change initiative?

### Framework
1. **Risk Identification**
   - Technical risks
   - Business risks
   - Organizational risks
   - External risks

2. **Risk Assessment**
   - Probability (1-5)
   - Impact (1-5)
   - Risk score = P x I

3. **Risk Response**
   - Avoid, Mitigate, Transfer, Accept
   - Response owner
   - Contingency plan

4. **Risk Monitoring**
   - Triggers
   - Status tracking
   - Escalation criteria

### Templates
```markdown
## Risk Register

| ID | Risk | Category | P | I | Score | Response | Owner |
|----|------|----------|---|---|-------|----------|-------|
| R-001 | {description} | Technical | 4 | 5 | 20 | Mitigate | {name} |
| R-002 | {description} | Business | 2 | 3 | 6 | Accept | {name} |

## Risk Matrix
         High Impact
              ^
    Accept   |   Mitigate/
    with     |   Avoid
    Reserve  |
    ---------+----------> High Prob
    Accept   |   Monitor
              |   Closely
         Low Impact
```

### Agent
faion-ba-agent

---

## M-BA-014: Change Strategy Planning

### Problem
How to develop the optimal approach for achieving the future state?

### Framework
1. **Gap Analysis**
   - Current vs future state delta
   - Capability gaps
   - Process gaps
   - Technology gaps

2. **Solution Options**
   - Build vs buy vs partner
   - Phased vs big bang
   - Scope variations

3. **Transition Planning**
   - Milestones and phases
   - Dependencies
   - Resource requirements

4. **Readiness Assessment**
   - Organizational readiness
   - Technical readiness
   - Stakeholder readiness

5. **Business Case**
   - Expected benefits
   - Total cost of ownership
   - ROI calculation

### Templates
```markdown
## Change Strategy

### Gap Analysis
| Dimension | Current | Future | Gap | Priority |
|-----------|---------|--------|-----|----------|
| Process | {state} | {state} | {gap} | H/M/L |
| Technology | {state} | {state} | {gap} | H/M/L |

### Solution Options
| Option | Description | Pros | Cons | Est. Cost |
|--------|-------------|------|------|-----------|
| A | Build in-house | Control | Time | $500K |
| B | Buy COTS | Speed | Fit | $300K |

### Recommendation
Option {X} because {rationale}

### Transition Roadmap
Phase 1 (Q1): {scope}
Phase 2 (Q2): {scope}
Phase 3 (Q3): {scope}
```

### Agent
faion-ba-agent

---

## M-BA-015: Requirements Modeling

### Problem
How to effectively represent and communicate requirements?

### Framework

**Modeling Techniques:**

1. **Use Cases**
   - Actor-system interactions
   - Scenarios and flows
   - Good for: functional requirements

2. **User Stories**
   - As-a/I-want/So-that format
   - Acceptance criteria
   - Good for: Agile contexts

3. **Process Models**
   - BPMN diagrams
   - Swimlane diagrams
   - Good for: workflow requirements

4. **Data Models**
   - Entity-relationship diagrams
   - Class diagrams
   - Good for: data requirements

5. **State Diagrams**
   - Object lifecycle
   - Transitions and triggers
   - Good for: status workflows

6. **Decision Tables/Trees**
   - Business rules
   - Decision logic
   - Good for: complex conditions

### Templates
```markdown
## User Story
**As a** {role}
**I want** {goal}
**So that** {benefit}

### Acceptance Criteria
- Given {context}
- When {action}
- Then {outcome}

---

## Use Case: {UC-ID} {Name}
**Actor:** {primary actor}
**Preconditions:** {conditions}

**Main Flow:**
1. Actor does {action}
2. System responds with {response}
3. ...

**Alternative Flows:**
3a. If {condition}, then {alternate path}

**Postconditions:** {state after completion}
```

### Agent
faion-ba-agent

---

## M-BA-016: Requirements Architecture

### Problem
How to organize requirements into a coherent structure?

### Framework
1. **Viewpoints**
   - Business perspective
   - User perspective
   - Technical perspective
   - Operational perspective

2. **Decomposition**
   - Hierarchical breakdown
   - Parent-child relationships
   - Abstraction levels

3. **Dependencies**
   - Prerequisite relationships
   - Conflict identification
   - Synergy identification

4. **Completeness Check**
   - Coverage analysis
   - Gap identification
   - Consistency validation

### Templates
```markdown
## Requirements Architecture

### Viewpoints
| Viewpoint | Stakeholders | Key Concerns |
|-----------|--------------|--------------|
| Business | Sponsor, Execs | ROI, Strategy |
| User | End users | Usability, Features |
| Technical | Developers | Feasibility, Architecture |

### Requirement Hierarchy
- BR-001: Business Requirement
  - SR-001: Stakeholder Requirement
    - FR-001: Functional Requirement
    - FR-002: Functional Requirement
  - SR-002: Stakeholder Requirement
    - FR-003: Functional Requirement

### Dependencies
| Requirement | Depends On | Enables |
|-------------|------------|---------|
| FR-001 | - | FR-003, FR-004 |
| FR-002 | FR-001 | FR-005 |
```

### Agent
faion-ba-agent

---

## M-BA-017: Solution Options Analysis

### Problem
How to evaluate and recommend the best solution option?

### Framework
1. **Options Identification**
   - Generate alternatives
   - Include "do nothing" baseline
   - Consider combinations

2. **Evaluation Criteria**
   - Strategic fit
   - Technical feasibility
   - Financial viability
   - Organizational impact
   - Risk profile

3. **Scoring Method**
   - Weighted criteria
   - Scoring scale (1-5)
   - Sensitivity analysis

4. **Recommendation**
   - Best option selection
   - Justification
   - Conditions and caveats

### Templates
```markdown
## Solution Options Analysis

### Options
| # | Option | Description |
|---|--------|-------------|
| A | {name} | {description} |
| B | {name} | {description} |
| C | {name} | {description} |

### Evaluation Criteria
| Criterion | Weight |
|-----------|--------|
| Strategic fit | 25% |
| Technical feasibility | 20% |
| Cost | 20% |
| Time to value | 20% |
| Risk | 15% |

### Scoring Matrix
| Criterion | Weight | Opt A | Opt B | Opt C |
|-----------|--------|-------|-------|-------|
| Strategic fit | 25% | 4 | 3 | 5 |
| Technical | 20% | 5 | 4 | 3 |
| Cost | 20% | 3 | 4 | 2 |
| Time | 20% | 3 | 5 | 2 |
| Risk | 15% | 4 | 4 | 3 |
| **Weighted Score** | | **3.75** | **3.95** | **3.10** |

### Recommendation
**Option B** is recommended because {rationale}

### Conditions
- Requires {condition}
- Assumes {assumption}
```

### Agent
faion-ba-agent

---

## M-BA-018: Solution Limitation Assessment

### Problem
How to identify and address solution limitations?

### Framework
1. **Defect Identification**
   - Functional gaps
   - Performance issues
   - Usability problems

2. **Root Cause Analysis**
   - Technical causes
   - Process causes
   - Organizational causes

3. **Impact Assessment**
   - Business impact
   - User impact
   - Operational impact

4. **Remediation Options**
   - Quick fixes
   - Workarounds
   - Permanent solutions
   - Accept limitations

### Templates
```markdown
## Solution Limitation Assessment

### Identified Limitations
| ID | Limitation | Category | Severity |
|----|------------|----------|----------|
| L-001 | {description} | Functional | High |
| L-002 | {description} | Performance | Medium |

### Root Cause Analysis
| Limitation | Root Cause | Evidence |
|------------|------------|----------|
| L-001 | {cause} | {evidence} |

### Impact Assessment
| Limitation | Business Impact | User Impact | Frequency |
|------------|-----------------|-------------|-----------|
| L-001 | {impact} | {impact} | Daily |

### Remediation Recommendations
| Limitation | Option | Effort | Recommendation |
|------------|--------|--------|----------------|
| L-001 | A: Fix in v2 | 3 sprints | Accept for now |
| L-001 | B: Workaround | 2 days | Implement |
```

### Agent
faion-ba-agent

---

# Underlying Competencies

## Analytical Thinking and Problem Solving

- Creative thinking
- Decision making
- Learning
- Problem solving
- Systems thinking
- Conceptual thinking
- Visual thinking

## Behavioral Characteristics

- Ethics
- Personal accountability
- Trustworthiness
- Organization and time management
- Adaptability

## Business Knowledge

- Business acumen
- Industry knowledge
- Organization knowledge
- Solution knowledge
- Methodology knowledge

## Communication Skills

- Verbal communication
- Non-verbal communication
- Written communication
- Listening

## Interaction Skills

- Facilitation
- Leadership and influencing
- Teamwork
- Negotiation and conflict resolution
- Teaching

## Tools and Technology

- Office productivity applications
- BA applications
- Communication tools
- Collaboration tools

---

# BABOK Techniques Reference

| # | Technique | Use Cases |
|---|-----------|-----------|
| 1 | Acceptance and Evaluation Criteria | Requirements validation |
| 2 | Backlog Management | Agile requirements |
| 3 | Balanced Scorecard | Strategy analysis |
| 4 | Benchmarking and Market Analysis | Current state analysis |
| 5 | Brainstorming | Elicitation |
| 6 | Business Capability Analysis | Strategy analysis |
| 7 | Business Cases | Change strategy |
| 8 | Business Model Canvas | Strategy analysis |
| 9 | Business Rules Analysis | Requirements analysis |
| 10 | Collaborative Games | Elicitation |
| 11 | Concept Modelling | Requirements modeling |
| 12 | Data Dictionary | Data requirements |
| 13 | Data Flow Diagrams | Process analysis |
| 14 | Data Mining | Analysis |
| 15 | Data Modelling | Data requirements |
| 16 | Decision Analysis | Solution evaluation |
| 17 | Decision Modelling | Business rules |
| 18 | Document Analysis | Elicitation |
| 19 | Estimation | Planning |
| 20 | Financial Analysis | Business case |
| 21 | Focus Groups | Elicitation |
| 22 | Functional Decomposition | Requirements architecture |
| 23 | Glossary | Communication |
| 24 | Interface Analysis | Requirements analysis |
| 25 | Interviews | Elicitation |
| 26 | Item Tracking | Requirements management |
| 27 | Lessons Learned | Improvement |
| 28 | Metrics and KPIs | Performance measurement |
| 29 | Mind Mapping | Elicitation, analysis |
| 30 | Non-Functional Requirements Analysis | Requirements analysis |
| 31 | Observation | Elicitation |
| 32 | Organizational Modelling | Current state |
| 33 | Prioritization | Requirements management |
| 34 | Process Analysis | Current state |
| 35 | Process Modelling | Requirements modeling |
| 36 | Prototyping | Elicitation, validation |
| 37 | Reviews | Verification |
| 38 | Risk Analysis and Management | Strategy, evaluation |
| 39 | Roles and Permissions Matrix | Requirements analysis |
| 40 | Root Cause Analysis | Problem analysis |
| 41 | Scope Modelling | Strategy analysis |
| 42 | Sequence Diagrams | Requirements modeling |
| 43 | Stakeholder List, Map, or Personas | Stakeholder analysis |
| 44 | State Modelling | Requirements modeling |
| 45 | Survey or Questionnaire | Elicitation |
| 46 | SWOT Analysis | Current state |
| 47 | Use Cases and Scenarios | Requirements modeling |
| 48 | User Stories | Agile requirements |
| 49 | Vendor Assessment | Solution evaluation |
| 50 | Workshops | Elicitation |

---

# Agent Called

| Agent | Purpose |
|-------|---------|
| faion-ba-agent | Execute BABOK methodologies, perform business analysis tasks |

---

# Directory Structure

```
~/.claude/skills/faion-ba-domain-skill/
|
v-- SKILL.md (this file)
```

---

*BA Domain Skill v1.0*
*Based on BABOK v3 (Guide to Business Analysis Body of Knowledge)*
*IIBA (International Institute of Business Analysis) Standards*
*18 Embedded Methodologies (M-BA-001 to M-BA-018)*


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-BA-001 | Ba Planning | [methodologies/M-BA-001_ba_planning.md](methodologies/M-BA-001_ba_planning.md) |
| M-BA-002 | Stakeholder Analysis | [methodologies/M-BA-002_stakeholder_analysis.md](methodologies/M-BA-002_stakeholder_analysis.md) |
| M-BA-003 | Elicitation Techniques | [methodologies/M-BA-003_elicitation_techniques.md](methodologies/M-BA-003_elicitation_techniques.md) |
| M-BA-004 | Requirements Documentation | [methodologies/M-BA-004_requirements_documentation.md](methodologies/M-BA-004_requirements_documentation.md) |
| M-BA-005 | Requirements Traceability | [methodologies/M-BA-005_requirements_traceability.md](methodologies/M-BA-005_requirements_traceability.md) |
| M-BA-006 | Strategy Analysis | [methodologies/M-BA-006_strategy_analysis.md](methodologies/M-BA-006_strategy_analysis.md) |
| M-BA-007 | Requirements Lifecycle | [methodologies/M-BA-007_requirements_lifecycle.md](methodologies/M-BA-007_requirements_lifecycle.md) |
| M-BA-008 | Solution Assessment | [methodologies/M-BA-008_solution_assessment.md](methodologies/M-BA-008_solution_assessment.md) |
| M-BA-009 | Business Process Analysis | [methodologies/M-BA-009_business_process_analysis.md](methodologies/M-BA-009_business_process_analysis.md) |
| M-BA-010 | Data Analysis | [methodologies/M-BA-010_data_analysis.md](methodologies/M-BA-010_data_analysis.md) |
| M-BA-011 | Decision Analysis | [methodologies/M-BA-011_decision_analysis.md](methodologies/M-BA-011_decision_analysis.md) |
| M-BA-012 | Use Case Modeling | [methodologies/M-BA-012_use_case_modeling.md](methodologies/M-BA-012_use_case_modeling.md) |
| M-BA-013 | User Story Mapping | [methodologies/M-BA-013_user_story_mapping.md](methodologies/M-BA-013_user_story_mapping.md) |
| M-BA-014 | Acceptance Criteria | [methodologies/M-BA-014_acceptance_criteria.md](methodologies/M-BA-014_acceptance_criteria.md) |
| M-BA-015 | Requirements Validation | [methodologies/M-BA-015_requirements_validation.md](methodologies/M-BA-015_requirements_validation.md) |
| M-BA-016 | Requirements Prioritization | [methodologies/M-BA-016_requirements_prioritization.md](methodologies/M-BA-016_requirements_prioritization.md) |
| M-BA-017 | Interface Analysis | [methodologies/M-BA-017_interface_analysis.md](methodologies/M-BA-017_interface_analysis.md) |
| M-BA-018 | Knowledge Areas Overview | [methodologies/M-BA-018_knowledge_areas_overview.md](methodologies/M-BA-018_knowledge_areas_overview.md) |
