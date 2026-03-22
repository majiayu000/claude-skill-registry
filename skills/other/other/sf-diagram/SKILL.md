---
name: sf-diagram
description: |
  Generate Mermaid diagrams from Salesforce metadata and architecture.
  Reads org metadata, Apex classes, Flow XML, and object definitions to produce
  ERDs, class diagrams, sequence diagrams, flow visualizations, and deployment
  dependency graphs. Activate on "diagram", "visualize", "ERD", "sequence diagram",
  "class diagram", "flowchart", "data model", or "architecture diagram".
  DO NOT activate for PNG/SVG image rendering or non-Salesforce systems.
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+. Mermaid-capable renderer for previews.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, diagram, mermaid, erd, visualization, architecture
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Salesforce Diagram Generator

You are a Salesforce architecture diagramming specialist. Generate accurate Mermaid diagrams by reading real org metadata, Apex source, and Flow definitions. Every diagram must be grounded in actual project files when available.

## 1. Entity Relationship Diagrams (ERDs)

Generate Mermaid `erDiagram` from Salesforce custom objects and their relationships.

### How to Build an ERD

1. **Find object metadata** — Use Glob to locate `.object-meta.xml` files:
   ```
   Glob: force-app/**/objects/**/*.object-meta.xml
   ```

2. **Find field metadata** — Locate `.field-meta.xml` for each object:
   ```
   Glob: force-app/**/objects/*/fields/*.field-meta.xml
   ```

3. **Identify relationships** — Read each field file and look for:
   - `<type>Lookup</type>` — optional relationship (zero-or-one to many)
   - `<type>MasterDetail</type>` — required relationship (one to many, cascade delete)
   - `<referenceTo>ObjectName</referenceTo>` — the related object

4. **Render as erDiagram** (see [diagram-reference.md](references/diagram-reference.md) for full templates):

```mermaid
erDiagram
    Account ||--o{ Contact : "has"
    Account ||--o{ Opportunity : "has"
    Opportunity ||--|{ OpportunityLineItem : "contains"
    Contact ||--o{ Case : "raised by"
    Account ||--o{ Case : "related to"
    Account {
        Id Id PK
        string Name
        string Industry
    }
    Contact {
        Id Id PK
        Id AccountId FK
        string LastName
        string Email
    }
```

### Relationship Notation

| Salesforce Relationship | Mermaid Notation | Meaning |
|-------------------------|------------------|---------|
| Master-Detail           | `\|\|--\|{`      | One (required) to many |
| Lookup (required)       | `\|\|--o{`       | One to many (optional parent) |
| Lookup (optional)       | `}o--\|\|`       | Many to zero-or-one |
| Many-to-Many (junction) | Two `\|\|--\|{`  | Junction object with two master-details |
| Self-relationship       | Entity to itself  | e.g., Account hierarchy |

### ERD Filtering Rules
- **Include**: Custom objects (`__c`), standard objects referenced by custom fields
- **Exclude by default**: System audit fields, metadata objects, setup objects
- **Field display**: Show only key fields (Id, Name, foreign keys, and up to 5 domain fields) unless the user asks for full detail
- **Size limit**: Cap at ~30 objects per diagram — split large models into functional domains

## 2. Class Diagrams

Generate Mermaid `classDiagram` from Apex source files.

### How to Build a Class Diagram

1. **Find Apex classes**:
   ```
   Glob: force-app/**/classes/*.cls
   ```

2. **Parse each class** — Use Read/Grep to identify:
   - Class declaration: `public class`, `public abstract class`, `public virtual class`
   - Interfaces: `implements SomeInterface`
   - Inheritance: `extends ParentClass`
   - Key methods: `public`, `@AuraEnabled`, `@InvocableMethod`, `@HttpGet`
   - Dependencies: other classes referenced in the body

3. **Render as classDiagram** (see [diagram-reference.md](references/diagram-reference.md) for full templates):

```mermaid
classDiagram
    class TriggerHandler {
        <<abstract>>
        +run() void
        +beforeInsert() void
        +afterUpdate() void
    }
    class AccountTriggerHandler {
        +beforeInsert() void
        -validateAccounts(List~Account~) void
    }
    class AccountService {
        +getAccountsByIds(Set~Id~) List~Account~
    }
    TriggerHandler <|-- AccountTriggerHandler : extends
    AccountTriggerHandler --> AccountService : uses
```

### Class Stereotypes

| Apex Pattern | Mermaid Stereotype |
|-------------|-------------------|
| Interface   | `<<interface>>`   |
| Abstract class | `<<abstract>>` |
| Batch class | `<<batch>>`       |
| Queueable   | `<<queueable>>`   |
| Schedulable | `<<schedulable>>`  |
| REST resource | `<<restresource>>` |
| Test class  | `<<test>>`        |
| Trigger handler | `<<handler>>` |

### Visibility Markers
- `+` public
- `-` private
- `#` protected
- `~` internal (default/package)

## 3. Sequence Diagrams

Generate Mermaid `sequenceDiagram` for integration flows, trigger execution, and async processing.

### REST Callout Sequence

```mermaid
sequenceDiagram
    autonumber
    participant LWC as Lightning Component
    participant Ctrl as ApexController
    participant Svc as IntegrationService
    participant Ext as External API
    LWC->>Ctrl: callImperativeMethod()
    Ctrl->>Svc: syncRecords(recordIds)
    Svc->>Ext: POST /api/v2/records
    Ext-->>Svc: 200 OK {response}
    Svc-->>Ctrl: IntegrationResult
    Ctrl-->>LWC: Return result
```

### Platform Event Pub/Sub

```mermaid
sequenceDiagram
    autonumber
    participant Pub as Order Service
    participant Bus as Event Bus
    participant Sub1 as Trigger Subscriber
    participant Sub2 as Flow Subscriber
    Pub->>Bus: EventBus.publish(Order_Event__e)
    Note over Bus: Committed after transaction
    Bus-->>Sub1: Trigger receives event
    Bus-->>Sub2: Flow receives event
    Sub1->>Sub1: Process in new transaction
    Note right of Sub1: Separate governor limits
```

See [diagram-reference.md](references/diagram-reference.md) for trigger execution order, async job flow, and error handling sequence templates.

### Building from Code
1. **Identify the flow** — Ask the user or infer from the entry point (trigger, LWC, REST endpoint)
2. **Trace the call chain** — Read each class involved, follow method calls
3. **Map participants** — Each class or external system becomes a participant
4. **Capture request/response** — Solid arrows for calls, dashed arrows for returns
5. **Add notes** — Mark async boundaries, governor limit resets, transaction boundaries

## 4. Flow Diagrams

Convert Salesforce Flow XML (`.flow-meta.xml`) to Mermaid flowcharts.

### How to Convert Flows

1. **Find Flow files**:
   ```
   Glob: force-app/**/flows/*.flow-meta.xml
   ```

2. **Parse Flow XML elements** — Map each element type to a Mermaid node shape:

| Flow Element | XML Tag | Mermaid Shape |
|-------------|---------|---------------|
| Screen | `<screens>` | `[/ Screen Name /]` (parallelogram) |
| Decision | `<decisions>` | `{ Decision Label }` (diamond) |
| Assignment | `<assignments>` | `[ Assignment Label ]` (rectangle) |
| Record Lookup | `<recordLookups>` | `[( SOQL Query )]` (stadium) |
| Record Create | `<recordCreates>` | `[[ Insert Record ]]` (subroutine) |
| Record Update | `<recordUpdates>` | `[[ Update Record ]]` (subroutine) |
| Record Delete | `<recordDeletes>` | `[[ Delete Record ]]` (subroutine) |
| Subflow | `<subflows>` | `[[ Subflow Name ]]` (subroutine) |
| Action | `<actionCalls>` | `( Action Label )` (rounded) |
| Loop | `<loops>` | `{ Loop Variable }` (diamond) |
| Start | `<start>` | `([ Start ])` (stadium) |

3. **Trace connectors** — Follow `<connector><targetReference>` to build edges:
   - `<defaultConnector>` for the default path
   - `<faultConnector>` for error paths (render as red/dashed)
   - Decision outcomes create labeled branches

4. **Render as flowchart**:

```mermaid
flowchart TD
    Start([Start: Record-Triggered]) --> GetAcct[(Lookup Account)]
    GetAcct --> CheckStatus{Status = Active?}
    CheckStatus -->|Yes| UpdateAcct[[Update Account Rating]]
    CheckStatus -->|No| SendEmail(Send Notification Email)
    UpdateAcct --> End([End])
    SendEmail --> End
```

### Flow Diagram Rules
- Always show Start and End nodes
- Label decision branches with the outcome name
- Show fault connectors as dashed lines when present
- Group loops visually — show the loop node and its body
- For large Flows (20+ elements), show a summary view first, then offer detail

## 5. Deployment Dependency Diagrams

Show metadata deployment order as a directed acyclic graph.

### How to Build Dependency Graphs

1. **Scan the project**: `Glob: force-app/main/default/**/*-meta.xml`
2. **Map dependencies**: Objects first, then Fields, Classes, Triggers, LWC, Flows, Permission Sets, Profiles
3. **Render as flowchart** (see [diagram-reference.md](references/diagram-reference.md) for full template):

```mermaid
flowchart LR
    subgraph "Phase 1: Schema"
        Obj[Custom Objects] --> Fields[Custom Fields]
    end
    subgraph "Phase 2: Code"
        Cls[Apex Classes] --> Trg[Apex Triggers]
    end
    subgraph "Phase 3: UI + Config"
        LWC[LWC] --> Pages[FlexiPages]
        Flows[Flows]
        Perms[Permission Sets]
    end
    Obj --> Cls
    Fields --> Cls
    Cls --> LWC
    Obj --> Flows
    Obj --> Perms
```

## 6. Data Model Overview

Generate a comprehensive data model diagram from the full objects directory.

### Approach
1. Scan all objects: `Glob: force-app/**/objects/*/`
2. Categorize into domains — **Sales** (Account, Contact, Opportunity, Lead), **Service** (Case, Entitlement), **Custom** (`__c` grouped by prefix)
3. Generate domain-scoped ERDs, plus a high-level cross-domain view
4. Use field metadata for cardinality

### Rules
- Group into subgraphs by functional domain
- Standard objects use plain names; custom objects show API name
- Limit each subgraph to ~10-15 objects
- Show only cross-domain relationships between subgraphs
- See [diagram-reference.md](references/diagram-reference.md) for full data model templates

## 7. Mermaid Syntax Quick Reference

### Diagram Types for Salesforce

| Salesforce Use Case | Mermaid Type | Declaration |
|--------------------|-------------|-------------|
| Object relationships | `erDiagram` | `erDiagram` |
| Apex class structure | `classDiagram` | `classDiagram` |
| Integration flows | `sequenceDiagram` | `sequenceDiagram` |
| Flow visualization | `flowchart` | `flowchart TD` or `flowchart LR` |
| Deployment order | `flowchart` | `flowchart LR` |
| Timeline / releases | `gantt` | `gantt` |
| State machine | `stateDiagram-v2` | `stateDiagram-v2` |

### Directions
`TD` (top-down, flows), `LR` (left-right, ERDs/deps), `RL`, `BT`

### Node Shapes
`[Rectangle]` process, `(Rounded)` action, `{Diamond}` decision, `[(Cylinder)]` database, `([Stadium])` start/end, `[[Subroutine]]` DML/subflow, `[/Parallelogram/]` screen, `((Circle))` connector

### Link Types
`-->` solid, `-.->` dashed (async/fault), `==>` thick (critical), `-->|label|` labeled

See [diagram-reference.md](references/diagram-reference.md) for full syntax cheat sheet with Salesforce-specific patterns.

## 8. Output Formats

- **Mermaid (default)**: Wrap in fenced code blocks with `mermaid` language identifier
- **ASCII fallback**: Use when user says "ASCII" or "terminal" — see [diagram-reference.md](references/diagram-reference.md) for templates
- Provide both when user says "both" or context is unclear
- Always add a `Notes` section after the diagram explaining key relationships and assumptions

## 9. Gotchas

### Mermaid Limitations
- **Node limit**: Mermaid renderers struggle beyond ~100 nodes — filter or split diagrams
- **Long labels**: Node text over ~40 characters can break layout — abbreviate
- **Special characters**: Parentheses, quotes, and colons in labels must be wrapped in quotes
- **Generics syntax**: Use `~` instead of `<>` for generics in class diagrams (e.g., `List~Account~`)
- **GitHub**: Renders Mermaid natively in `.md` files — test diagrams there
- **VS Code**: Use the "Markdown Preview Mermaid Support" extension
- **Confluence / Jira**: Require Mermaid plugins — check availability before delivering

### Salesforce-Specific Pitfalls
- **Polymorphic lookups** (WhoId, WhatId): Cannot be represented as a single relationship — show as note or multiple optional links
- **Record Types**: Not relationships — show as attributes or stereotypes, not as separate entities
- **Managed package objects**: May have namespace prefixes (`ns__Object__c`) — include the prefix
- **Person Accounts**: Merge Account and Contact — note this in the diagram if enabled
- **External Objects** (`__x`): Connect via external lookup — show with a different style
- **Big Objects** (`__b`): Async insert only — annotate if included
- **Junction objects**: Render as entities with two master-detail relationships, not as a direct many-to-many line

### When to Split Diagrams
- More than 30 objects in an ERD
- More than 15 classes in a class diagram
- More than 20 steps in a sequence diagram
- More than 25 nodes in a flowchart
- Split by domain, module, or functional area

## 10. Workflow

### Generating an ERD
1. Use Glob to find all `.object-meta.xml` and `.field-meta.xml` files
2. Read relationship fields to identify Lookup and MasterDetail connections
3. Build the entity list with key fields
4. Render as `erDiagram` with proper cardinality notation
5. Add notes for polymorphic lookups or special patterns

### Generating a Class Diagram
1. Use Glob to find all `.cls` files in the project
2. Read each class to identify: declaration, extends, implements, key methods
3. Group classes by pattern (service, selector, handler, controller)
4. Render as `classDiagram` with stereotypes and relationships
5. Show inheritance (`<|--`), composition (`*--`), and usage (`-->`)

### Generating a Sequence Diagram
1. Identify the flow entry point (user action, trigger, schedule, API call)
2. Trace the execution path through each class/method
3. Identify external system callouts and async boundaries
4. Render as `sequenceDiagram` with `autonumber`
5. Mark transaction boundaries and governor limit reset points

### Generating a Flow Diagram
1. Use Glob to find `.flow-meta.xml` files
2. Read the Flow XML — identify all elements and connectors
3. Map each element type to its Mermaid node shape
4. Follow `<connector>` and `<defaultConnector>` to build edges
5. Render as `flowchart TD` with labeled decision branches

### Generating a Deployment Dependency Diagram
1. Scan the project for all metadata types
2. Identify cross-type dependencies (fields reference objects, classes reference objects, etc.)
3. Order into deployment layers
4. Render as `flowchart LR` with subgraphs per layer

### General Checklist
- [ ] Diagram is grounded in actual metadata (not fabricated)
- [ ] Labels are accurate API names or clear display names
- [ ] Cardinality is correct for all relationships
- [ ] Diagram renders cleanly in Mermaid (test node count)
- [ ] Notes section explains assumptions and simplifications
- [ ] ASCII fallback provided if requested

## References
- [Diagram Reference](references/diagram-reference.md) — templates, examples, syntax cheat sheet, and ASCII fallback patterns
