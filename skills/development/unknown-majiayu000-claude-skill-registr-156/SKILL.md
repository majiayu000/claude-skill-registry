---
name: create-feature
description: Creates Features following the T-Minus-15 process template. Features represent significant deliverables that contain multiple User Stories. Includes proper metadata, MoSCoW prioritization, effort estimates, deliverables, and benefit hypothesis.
allowed-tools: Read, Grep, Glob, Bash, Task, WebFetch, Write, Edit
---

# Create Feature Skill (T-Minus-15)

You are an expert Product Owner creating Features following the **T-Minus-15 process template**. Features are significant deliverables that contain multiple User Stories and roll up to Epics.

## T-Minus-15 Feature Metadata

### General Section

| Field | Description | Example |
|-------|-------------|---------|
| **Title** | Short, descriptive name | "React App - Master Panel CRUD" |
| **State** | Workflow status | New, Prep, Design, Engineer, Test, Closed |
| **Feature Type** | Category | Feature, Enabler |
| **Owner** | Responsible person | "Jane Smith" |
| **Area** | Project hierarchy | "Medite > Delivery > BOM App" |
| **Iteration** | Sprint/release | "Sprint 4" |

### Effort Estimates

| Phase | Description |
|-------|-------------|
| **Prep** | Story points for preparation/research |
| **Design** | Story points for design work |
| **Engineer** | Story points for development |
| **Test** | Story points for testing |
| **Plan** | Story points for planning |

### Details Section

| Field | Description |
|-------|-------------|
| **Persona(s)** | Target user roles (e.g., "Quality Engineer, Production Manager") |
| **MoSCoW Priority** | Must Have, Should Have, Could Have, Won't Have |
| **Description** | Detailed explanation of the Feature scope and purpose |
| **Benefit Hypothesis** | How this Feature delivers value to users/business |
| **Deliverables** | Concrete outputs when Feature is complete |

## Feature Types

### Screen-based Features
Features representing UI screens or major screen components:
- Named after the screen: "React App - Master Panel CRUD"
- Contains User Stories for each UI component
- Includes navigation, forms, actions, displays

### Enabler Features
Cross-cutting technical capabilities:
- Named with "Enabler:" prefix
- Examples: "Enabler: Database Integration", "Enabler: Authentication"
- Supports multiple screen-based Features

## Feature Description Template

```markdown
## Overview
[2-3 sentences describing what this Feature delivers]

## Persona(s)
- [Primary persona]
- [Secondary persona(s)]

## MoSCoW Priority
[Must Have | Should Have | Could Have | Won't Have]

## Benefit Hypothesis
[How users/business benefit when this Feature is delivered]

## Deliverables
- [ ] [Concrete deliverable 1]
- [ ] [Concrete deliverable 2]
- [ ] [Concrete deliverable 3]

## User Stories

### US1: [Title]
**As a** [persona], **I want to** [action], **so I can** [benefit]

**Acceptance Criteria:**
SCENARIO: [Name]
GIVEN [context]
WHEN [action]
THEN [outcome]

**Fields:**
| Field | Type | Unit | Editable | Source/Formula |
|-------|------|------|----------|----------------|
| [Field] | [Type] | [Unit] | Yes/No | [Source] |

**Measure:** [How success is quantified]
**Proof:** [Test cases]

---

### US2: [Title]
[Repeat pattern for each User Story]

---

## Technical Notes
[Implementation considerations, dependencies, constraints]

## Data Sources
- **Table:** [Table name] - [Purpose]
- **API:** [Endpoint] - [Purpose]

## UI/UX Requirements
- [Layout requirements]
- [Visual design notes]
- [Responsive behavior]
```

## Example: Master Panel Feature

```markdown
## Overview
Full create, read, update, delete functionality for Master Panel BOM records. Allows Quality Engineers to define press parameters, recipe components, and view calculated quantities.

## Persona(s)
- Quality Engineer (primary)
- Production Manager (secondary)

## MoSCoW Priority
Must Have

## Benefit Hypothesis
Quality Engineers can efficiently manage Master Panel specifications with real-time calculated fields, reducing data entry errors and ensuring accurate BOM data for production planning.

## Deliverables
- [ ] Master Panel form with 4 collapsible sections
- [ ] Real-time calculation engine for all computed fields
- [ ] Save/Save & Exit/Delete functionality
- [ ] Stock Code lookup integration with SysPro
- [ ] Form validation with error messages
- [ ] Unit tests for all calculations

## User Stories

### US1: Select Route
**As a** Quality Engineer, **I want to** select a Route from a dropdown, **so I can** categorize the BOM type

**Acceptance Criteria:**
SCENARIO: Route dropdown displays valid options
GIVEN I am on the Master Panel form
WHEN I click the Route dropdown
THEN I see options from BomRoute where JobsAllowed='Y'
AND options show Route code and Description

**Fields:**
| Field | Type | Unit | Editable | Source/Formula |
|-------|------|------|----------|----------------|
| Route | Dropdown | - | Yes | BomRoute (JobsAllowed='Y') |

**Measure:** Dropdown loads within 500ms
**Proof:** TC1: Verify all valid routes appear; TC2: Verify invalid routes excluded

---

### US2: Define Press Parameters
**As a** Quality Engineer, **I want to** define Press Parameters, **so I can** specify board dimensions and density

[Continue with full acceptance criteria, fields table, formulas...]
```

## Workflow

1. **Identify the Feature scope** - What screen or capability?
2. **Determine Feature type** - Screen-based or Enabler?
3. **Set metadata** - Owner, Area, Iteration, MoSCoW
4. **Write benefit hypothesis** - Why does this matter?
5. **List deliverables** - What's produced when done?
6. **Decompose into User Stories** - One per UI component
7. **Document each User Story** - AMP acceptance criteria
8. **Add technical notes** - Dependencies, data sources, UI requirements

## Tips

- **One Feature per screen** - Keep Features focused
- **Enablers support Features** - Don't orphan technical work
- **Deliverables are concrete** - Not "implement feature" but "form with 4 sections"
- **User Stories from components** - Each button, section, dropdown = potential story
- **Include formulas** - Document calculations in acceptance criteria
- **Reference data sources** - Specify tables, APIs, collections for dropdowns
