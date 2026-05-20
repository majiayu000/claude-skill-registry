---
context: fork
---

# /architecture

Create an Architecture note documenting high-level design (HLD), low-level design (LLD), C4 diagrams, or solution architecture with systems, integrations, and design decisions.

## Usage

```
/architecture <title>
/architecture <title> --type hld
/architecture "SAP to DataPlatform Integration Design" --type hld --project MyDataIntegration
/architecture "DataPlatform Data Pipeline" --type c4-context
```

## Instructions

### Phase 1: Parse Input & Gather Scope

1. Extract architecture title
2. Ask for architecture type:
   ```
   Architecture Type:
   - high-level-design (HLD) - System-level overview
   - low-level-design (LLD) - Component details
   - c4-context - C4 context diagram (highest level)
   - c4-container - Container diagram (system internals)
   - aws-architecture - Cloud infrastructure
   Default: high-level-design
   ```

3. Ask what project/scope:
   ```
   Is this for a specific project?
   Search: [[Project - {{name}}]]
   Or: Enterprise-wide / Domain-wide
   Default: Project-scoped
   ```

### Phase 2: Systems & Components

```
Which systems are involved?
(Multi-select - search and add each)

Add System:
> SAP S/4HANA
Found: [[System - SAP S/4HANA]] ✓

Add System:
> DataPlatform
Found: [[System - DataPlatform]] ✓

Add System:
> Snowflake
Found: [[System - Snowflake]] ✓

Done adding systems? (Y/n)
> n

Systems involved: 3
```

### Phase 3: Design Details

```
1️⃣ Design Pattern(s):
   - microservices
   - event-driven
   - api-gateway
   - data-lake
   - monolith
   - serverless
   Default: null
   User input: [select applicable]

2️⃣ Key Design Decision(s):
   Why was this architecture chosen?
   > "Use event-driven for real-time data flows"
   > "Kafka enables loose coupling"
   > "Cloud for scalability and cost"
   Default: null
```

### Phase 4: Non-Functional Requirements

Ask: "Add NFR details? (Y/n)"

If YES:
```
- Availability Target (%): 99.95
- Latency (p99): < 100ms
- Throughput: 1000 req/sec
- Scalability: auto-scaling 2x-10x
- Security: end-to-end encryption
- Compliance: GDPR, SOC2, ISO27001
```

### Phase 5: Design Alternatives

Ask: "Document considered alternatives? (Y/n)"

If YES:
```
What alternative approaches were considered?
1. Option A: Vendor X (cost: high, complexity: low)
2. Option B: AWS native (cost: medium, complexity: high)
3. Chose: Option A due to...
```

### Phase 6: Generate Frontmatter

```yaml
type: Architecture
title: "{{title}}"

architectureType: {{type}}
c4Level: {{c4_level|null}}
designStatus: proposed

scope: {{scope}}
project: "[[Project - {{project}}]]"

systemsInvolved:
  - "[[System - SAP S/4HANA]]"
  - "[[System - DataPlatform]]"
  - "[[System - Snowflake]]"

designPattern: [{{patterns}}]

nfr-availability: "99.95"
nfr-latency-p99: "< 100ms"
nfr-throughput: "1000 req/sec"

designDecisions: [{{decisions}}]
consideredAlternatives: [{{alternatives}}]

reviewedBy: []
approvedBy: []
approvalDate: null

confidence: medium
freshness: current
verified: false

created: 2026-01-14
tags: [type/architecture, {{type|lower}}, {{project|lower}}]
```

### Phase 7: Generate Body Content

1. **Overview**: What this architecture solves
2. **Executive Summary**: For business stakeholders
3. **Architecture Diagram**: Mermaid diagram showing systems and flows
4. **C4 Context Diagram**: If applicable
5. **C4 Container Diagram**: If applicable
6. **Architecture Details by Layer**: Presentation, application, integration, data, infrastructure
7. **Non-Functional Requirements**: Availability, latency, scalability targets
8. **Design Decisions**: Why this approach
9. **Implementation Plan**: Phases and timeline
10. **Monitoring & Operations**: How to operate this

### Phase 8: Link to Related Items

Ask: "Link to related items? (Y/n)"

```
Related ADRs:
> [[ADR - Event-Driven Architecture]]
> [[ADR - SAP Integration Patterns]]

Related Projects:
> [[Project - MyDataIntegration]]
```

### Phase 9: Create File

**Filename**: `Architecture - {{title}}.md`

**Location**: Vault root

**Output**:
```
✅ Created: Architecture - {{title}}.md

Systems included:
- [[System - SAP S/4HANA]]
- [[System - DataPlatform]]
- [[System - Snowflake]]

Linked to:
- [[Project - {{project}}]]
- [[ADR - ...]]

Next steps:
1. Generate C4 diagram: /c4-diagram [[Architecture - {{title}}]]
2. Generate data flow: /dataflow-diagram [[Project - MyDataIntegration]]
3. Create scenario: /scenario "Future State" --architecture [[Architecture - {{title}}]]
```

## Example Interaction

```
User: /architecture "SAP to DataPlatform Integration" --project MyDataIntegration

Architecture Type (default: HLD):
> high-level-design

Systems involved:
> SAP S/4HANA
> DataPlatform
> Snowflake

Design Pattern:
- event-driven ✓
- api-gateway ✓

Key decisions:
> Event-driven for real-time data
> Kafka for loose coupling
> Snowflake for analytics

Availability SLA:
> 99.95

Latency target (p99):
> < 100ms

Throughput:
> 5000 records/second

✅ Created: Architecture - SAP to DataPlatform Integration.md

Next: /c4-diagram [[Architecture - SAP to DataPlatform Integration]]
```
