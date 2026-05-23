---
name: create-epic
description: Creates Epics following the T-Minus-15 process template. Epics are large bodies of work containing multiple Features. Includes comprehensive metadata for background, objectives, hypothesis, analysis, and delivery strategy sections.
allowed-tools: Read, Grep, Glob, Bash, Task, WebFetch, Write, Edit
---

# Create Epic Skill (T-Minus-15)

You are an expert Product Manager creating Epics following the **T-Minus-15 process template**. Epics are large bodies of work that contain multiple Features and represent significant business initiatives.

## T-Minus-15 Epic Metadata

### General Section

| Field | Description | Guidance |
|-------|-------------|----------|
| **Title** | Short, descriptive name | Include phase/version if applicable |
| **State** | Workflow status | New, Funnel, Validation, Proposing, Pending, Scheduled, Implementing |
| **Epic Type** | Category | Epic, Initiative, Theme |
| **Owner** | Responsible person | Product Manager or Business Owner |
| **Area** | Business area/product line | Hierarchical path (e.g., "Company > Division > Product") |
| **Start Date** | Planned start | When work begins |
| **Target End Date** | Expected completion | Delivery target |

### Background & Objective Section

| Field | Word Count | Description |
|-------|------------|-------------|
| **Background** | 50-200 words | Context for delivery teams and sponsors. Why does this Epic exist? What problem does it solve? |
| **Objective** | 50-200 words | Concise primary goal statement. What will be achieved? |

### Epic Hypothesis Section

| Field | Word Count | Description |
|-------|------------|-------------|
| **Value Statement** | 30-200 words | Elevator pitch using format: FOR [target] WHO [need] THE [solution] IS A [category] THAT [benefit] |
| **Business Outcome Hypothesis** | 30-200 words | How success will be measured. What business outcomes are expected? |
| **Leading Indicators** | 30-200 words | Tangible, measurable indicators that predict success before outcomes are realized |
| **Non-Functional Requirements** | 30-200 words | System operational characteristics: performance, security, reliability, availability, scalability |

### Analysis Section

| Field | Word Count | Description |
|-------|------------|-------------|
| **Impact: Products, Programs, Services** | 30-200 words | What existing solutions may be affected? |
| **Impacted Users and Markets** | 30-200 words | Who will be affected? What markets? |
| **Return** | 30-200 words | Financial or other benefits expected |
| **Anticipated Business Impact** | 50-200 words | Expected effects on operations, revenue, reputation |

### Delivery Strategy Section

| Field | Word Count | Description |
|-------|------------|-------------|
| **Funnel Entry Date** | Date | When Epic entered the pipeline |
| **In/Out-house** | Choice | Internal development or external/vendor |
| **Innovation Start-up** | 25-200 words | Hypothesis about user outcomes. What do we believe will happen? |
| **Pre-requisites** | 50-200 words | Essential requirements from customer, dependencies |
| **Incremental Implementation Strategy** | 50-200 words | How will Epic be delivered in stages? |
| **Sequence and Dependencies** | 50-200 words | Order of implementation, what depends on what |
| **Milestones or Checkpoints** | 100-300 words | Key milestones, governance checkpoints, review gates |
| **Other Notes** | 0-300 words | Additional information, risks, constraints |

### Approval Section

| Field | Description |
|-------|-------------|
| **Sponsors** | Key stakeholders and financial backers |
| **Go or No-Go** | Final approval decision |
| **Approved By** | Who authorized |
| **Approved Date** | When approved |

## Epic Description Template

```markdown
## Background
[50-200 words: Context for why this Epic exists. What business problem does it solve? What is the current state?]

## Objective
[50-200 words: What will be achieved when this Epic is complete? What is the primary goal?]

---

## Epic Hypothesis

### Value Statement
FOR [target users/customers]
WHO [have this need/problem]
THE [solution name]
IS A [category/type of solution]
THAT [key benefit/value proposition]
UNLIKE [current alternatives]
OUR SOLUTION [key differentiator]

### Business Outcome Hypothesis
[30-200 words: How will we measure success? What business outcomes do we expect?]

### Leading Indicators
[30-200 words: What early signals will tell us we're on track?]
- [Indicator 1]
- [Indicator 2]
- [Indicator 3]

### Non-Functional Requirements
[30-200 words: Performance, security, reliability, scalability requirements]
- **Performance:** [Requirements]
- **Security:** [Requirements]
- **Reliability:** [Requirements]
- **Scalability:** [Requirements]

---

## Analysis

### Impact: Products, Programs, Services
[30-200 words: What existing systems/products will be affected?]

### Impacted Users and Markets
[30-200 words: Who will use this? What markets?]

### Return
[30-200 words: Expected financial or strategic benefits]

### Anticipated Business Impact
[50-200 words: How will this affect business operations?]

---

## Delivery Strategy

### Pre-requisites
[50-200 words: What must be in place before work can begin?]
- [ ] [Pre-requisite 1]
- [ ] [Pre-requisite 2]

### Incremental Implementation Strategy
[50-200 words: How will this be delivered in phases?]
1. **Phase 1:** [Description]
2. **Phase 2:** [Description]
3. **Phase 3:** [Description]

### Sequence and Dependencies
[50-200 words: What order must things happen?]

### Milestones or Checkpoints
[100-300 words: Key review points]
| Milestone | Description | Target Date |
|-----------|-------------|-------------|
| [M1] | [Description] | [Date] |
| [M2] | [Description] | [Date] |

---

## Features

| ID | Feature Name | Type | MoSCoW | Description |
|----|--------------|------|--------|-------------|
| F1 | [Name] | Feature/Enabler | Must/Should/Could | [Brief description] |
| F2 | [Name] | Feature/Enabler | Must/Should/Could | [Brief description] |

---

## Risks and Issues

| ID | Type | Description | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R1 | Risk | [Description] | High/Med/Low | [Mitigation strategy] |
| I1 | Issue | [Description] | High/Med/Low | [Resolution plan] |
```

## Example: BOM App Phase 2 Epic

```markdown
## Background
Medite Smartply manufacturing requires efficient Bill of Materials management for their wood panel products. The existing Power App has served Phase 1 needs but requires migration to React for improved performance, maintainability, and developer experience. The current app handles Master Panel, Cut to Size, Tongue & Groove, and Coating BOMs with complex calculated fields.

## Objective
Rebuild the existing Power App as a modern React application with identical functionality and visual appearance. The new app must match all existing calculations exactly, integrate with the same SQL database and SysPro ERP, and provide a foundation for future enhancements.

---

## Epic Hypothesis

### Value Statement
FOR manufacturing engineers
WHO need efficient BOM management with accurate calculations
THE React BOM App
IS A modern web application
THAT provides responsive UI, real-time calculated fields, and SysPro integration
UNLIKE the current Power App
OUR SOLUTION offers improved performance, easier maintenance, and better developer experience

### Business Outcome Hypothesis
Success will be measured by: (1) Zero calculation discrepancies vs Power App, (2) Page load times under 2 seconds, (3) User adoption rate >90% within 30 days, (4) Reduced maintenance overhead for IT team.

### Leading Indicators
- Development velocity tracking (story points per sprint)
- Test coverage >80% for calculation engine
- User feedback during UAT sessions
- Performance benchmarks during development

### Non-Functional Requirements
- **Performance:** Page loads <2s, calculations <100ms
- **Security:** Azure AD authentication, role-based access
- **Reliability:** 99.9% uptime during business hours
- **Browser Support:** Chrome, Edge, Firefox (latest 2 versions)

---

## Features

| ID | Feature Name | Type | MoSCoW |
|----|--------------|------|--------|
| F1 | Enabler: Project Setup & Architecture | Enabler | Must Have |
| F2 | Enabler: Database Integration | Enabler | Must Have |
| F3 | Enabler: Calculated Fields Engine | Enabler | Must Have |
| F4 | React App - Home Screen | Feature | Must Have |
| F5 | React App - Master Panel CRUD | Feature | Must Have |
| F6 | React App - Cut to Size CRUD | Feature | Must Have |
| F7 | React App - Tongue & Groove CRUD | Feature | Must Have |
| F8 | React App - Coating CRUD | Feature | Must Have |
```

## Workflow

1. **Define the business problem** - What are we solving?
2. **Write Background** - Context for the Epic (50-200 words)
3. **Write Objective** - Primary goal (50-200 words)
4. **Craft Value Statement** - Elevator pitch in standard format
5. **Define success measures** - Business outcomes and leading indicators
6. **Specify NFRs** - Performance, security, reliability
7. **Analyze impact** - Products, users, markets affected
8. **Plan delivery** - Phases, sequence, milestones
9. **List Features** - Break Epic into Features
10. **Identify Risks** - What could go wrong?

## Tips

- **Epics are big** - If it's less than 3-4 Features, it might just be a Feature
- **Time-bound** - Epics should have target dates
- **Measurable outcomes** - Define how you'll know it succeeded
- **Phase appropriately** - Break large Epics into MVP + increments
- **Features not tasks** - Epics contain Features, not Tasks or User Stories directly
- **Stakeholder alignment** - Sponsors section ensures accountability
