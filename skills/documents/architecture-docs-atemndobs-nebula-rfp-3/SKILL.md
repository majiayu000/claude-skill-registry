---
name: architecture-docs
description: Create and maintain architecture documentation with Mermaid diagrams. Use when writing technical documentation, system diagrams, or updating the implementation plan.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Architecture Documentation Skill

## Overview

This skill provides patterns for creating clear, maintainable architecture documentation with properly formatted Mermaid diagrams.

## When to Use

- Creating system architecture diagrams
- Documenting data flows
- Writing implementation plans
- Creating entity relationship diagrams
- Updating `docs/implementation-plan/`

---

## Mermaid Diagram Best Practices

### CRITICAL: Quote Special Characters

Mermaid will break on unquoted special characters. **ALWAYS quote node labels containing:**

| Character | Example | Wrong | Correct |
|-----------|---------|-------|---------|
| Parentheses | `(info)` | `A[Label (info)]` | `A["Label (info)"]` |
| Brackets | `[0]` | `A[Array [0]]` | `A["Array [0]"]` |
| Angle brackets | `<table>` | `A[Id<table>]` | `A["Id<table>"]` |
| Colon | `:` | `A[Key: Value]` | `A["Key: Value"]` |
| Ampersand | `&` | `A[A & B]` | `A["A & B"]` |
| Greater/Less | `>`, `<` | `A[x > 5]` | `A["x > 5"]` |
| Pipe | `\|` | `A[A \| B]` | `A["A \| B"]` |
| Question mark | `?` | `A[Is valid?]` | `A["Is valid?"]` |

### Flowchart Template

```mermaid
flowchart TD
    subgraph Input["📥 Input Layer"]
        A["SAM.gov API"]
        B["eMMA Scraper"]
        C["RFPMart API"]
    end

    subgraph Processing["⚙️ Processing"]
        D["Canonical Schema"]
        E["Deduplication"]
        F{"Eligibility Gate"}
    end

    subgraph Output["📤 Output"]
        G["ELIGIBLE"]
        H["PARTNER_REQUIRED"]
        I["REJECTED"]
    end

    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    F -->|"Pass"| G
    F -->|"Partner needed"| H
    F -->|"Fail"| I
```

### Sequence Diagram Template

```mermaid
sequenceDiagram
    participant U as "User"
    participant FE as "React Frontend"
    participant BE as "Convex Backend"
    participant AI as "Gemini AI"

    U->>FE: Click "Evaluate"
    FE->>BE: mutation("evaluations.run")
    BE->>BE: Check eligibility first
    alt Eligible
        BE->>AI: Send evaluation prompt
        AI-->>BE: Return JSON result
        BE-->>FE: Evaluation complete
    else Not Eligible
        BE-->>FE: Return rejection reason
    end
    FE-->>U: Show result
```

### Entity Relationship Diagram Template

```mermaid
erDiagram
    OPPORTUNITY ||--o{ EVALUATION : "has"
    OPPORTUNITY ||--o| PURSUIT : "may have"
    EVALUATION ||--|| ELIGIBILITY : "contains"
    EVALUATION ||--o{ DIMENSION_SCORE : "contains"
    PURSUIT ||--o{ NOTE : "has"
    PURSUIT ||--o| BRIEF : "has"
    USER ||--o{ PURSUIT : "owns"

    OPPORTUNITY {
        string id PK
        string title
        string source
        number dueDate
    }

    EVALUATION {
        string id PK
        string opportunityId FK
        string eligibilityStatus
        number totalScore
    }
```

### State Diagram Template

```mermaid
stateDiagram-v2
    [*] --> New
    New --> Triage: Review
    Triage --> Bid: Decide to pursue
    Triage --> NoBid: Decide to skip
    Bid --> Capture: Start capture
    Capture --> Draft: Begin writing
    Draft --> Review: Submit for review
    Review --> Draft: Request changes
    Review --> Submitted: Approve
    Submitted --> Won: Award received
    Submitted --> Lost: Not selected
    NoBid --> [*]
    Won --> [*]
    Lost --> [*]
```

---

## Documentation Structure

### Implementation Plan Structure

```
docs/implementation-plan/
├── README.md                    # Executive summary
│   - High-level architecture diagram
│   - Phase timeline table
│   - Success metrics
│   - Approval checklist
│
├── phase-N-[name]/README.md     # Phase details
│   - Objectives
│   - Data model changes
│   - Code examples
│   - Implementation checklist
│   - Files to create/modify
│
└── architecture/
    ├── README.md                # Multi-level architecture
    │   - Executive view (business flow)
    │   - Technical view (system components)
    │   - Implementation view (file structure)
    │
    └── DATABASE-SCHEMA.md       # Complete schema
        - Entity relationship diagram
        - Table definitions
        - Index definitions
        - Complete schema.ts code
```

### Feature Documentation Structure

```
docs/features/[feature-name]/
├── README.md           # Problem, solution, success criteria
├── ARCHITECTURE.md     # Technical design with diagrams
└── IMPLEMENTATION.md   # Step-by-step plan with checklists
```

---

## ASCII Diagrams

For inline documentation or simpler contexts, use ASCII art:

### Box Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    PROCESSING PIPELINE                   │
├─────────────────────────────────────────────────────────┤
│  INGEST → DEDUPE → ELIGIBILITY → SCORE → PIPELINE       │
└─────────────────────────────────────────────────────────┘
```

### Flow Diagram

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  INPUT   │───▶│ PROCESS  │───▶│  OUTPUT  │
└──────────┘    └──────────┘    └──────────┘
```

### Decision Tree

```
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Eligible?  │
                    └──────┬──────┘
                     Yes   │   No
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌──────────┐              ┌──────────┐
       │  SCORE   │              │  REJECT  │
       └──────────┘              └──────────┘
```

---

## Quick Reference

### Audience-Specific Diagrams

| Audience | Diagram Type | Focus |
|----------|--------------|-------|
| Executive | Flowchart | Business value flow |
| Architect | Component diagram | System boundaries |
| Developer | Sequence diagram | API interactions |
| DBA | ERD | Data relationships |

### Diagram Checklist

- [ ] All special characters are quoted
- [ ] Subgraph labels are descriptive
- [ ] Arrows have labels where helpful
- [ ] Colors/styles are consistent
- [ ] Diagram renders without errors
