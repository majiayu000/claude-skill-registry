---
name: process-modeling
description: Process modeling using BPMN notation and flowchart patterns. Creates process diagrams with activities, gateways, events, swimlanes, and decision points for workflow documentation.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Process Modeling

## When to Use This Skill

Use this skill when:

- **Process Modeling tasks** - Working on process modeling using bpmn notation and flowchart patterns. creates process diagrams with activities, gateways, events, swimlanes, and decision points for workflow documentation
- **Planning or design** - Need guidance on Process Modeling approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Create and document business processes using BPMN (Business Process Model and Notation) and flowchart notation. Visualize activities, decisions, events, and participant interactions for process understanding and improvement.

## What is Process Modeling?

**Process modeling** creates visual representations of how work flows through an organization. It documents:

- **Activities**: What work is performed
- **Sequence**: Order of activities
- **Decisions**: Choice points and conditions
- **Participants**: Who performs each step
- **Events**: What triggers and ends the process

## BPMN Core Elements

### Activities (Rectangles)

| Type | Symbol | Description |
|------|--------|-------------|
| **Task** | Rectangle | Atomic work unit |
| **Sub-Process** | Rectangle with + | Contains child process |
| **Call Activity** | Rectangle with thick border | Invokes reusable process |

**Task Types:**

| Type | Description |
|------|-------------|
| User Task | Human interaction required |
| Service Task | Automated system action |
| Script Task | Script/code execution |
| Business Rule Task | Decision table evaluation |
| Send Task | Message sent |
| Receive Task | Message received |
| Manual Task | Physical work without system |

### Events (Circles)

| Position | Symbol | Description |
|----------|--------|-------------|
| **Start** | Thin circle | Process trigger |
| **Intermediate** | Double circle | Mid-process event |
| **End** | Thick circle | Process termination |

**Event Types:**

| Type | Trigger |
|------|---------|
| None | Unspecified start/end |
| Message | Message received/sent |
| Timer | Time-based trigger |
| Error | Error condition |
| Signal | Broadcast signal |
| Terminate | Process termination |

### Gateways (Diamonds)

| Type | Symbol | Description |
|------|--------|-------------|
| **Exclusive (XOR)** | Diamond with X | One path based on condition |
| **Parallel (AND)** | Diamond with + | All paths execute |
| **Inclusive (OR)** | Diamond with O | One or more paths |
| **Event-Based** | Diamond with circle | Wait for events |

### Connectors

| Type | Symbol | Description |
|------|--------|-------------|
| **Sequence Flow** | Solid arrow | Order of activities |
| **Message Flow** | Dashed arrow | Messages between pools |
| **Association** | Dotted line | Artifacts to elements |

### Swimlanes

| Type | Description |
|------|-------------|
| **Pool** | Represents a participant (organization/system) |
| **Lane** | Subdivisions within a pool (roles/departments) |

## Workflow

### Phase 1: Define Scope

#### Step 1: Identify Process Boundaries

```markdown
## Process Definition

**Process Name:** [Name]
**Purpose:** [Why this process exists]
**Scope:**
  - **Starts When:** [Trigger event]
  - **Ends When:** [Completion criteria]
  - **Includes:** [In-scope activities]
  - **Excludes:** [Out-of-scope activities]

**Participants:**
| Pool | Lanes (Roles) |
|------|---------------|
| [Org/System] | [Role 1], [Role 2] |
```

#### Step 2: Choose Model Type

| Type | When to Use |
|------|-------------|
| **As-Is** | Documenting current state |
| **To-Be** | Designing future state |
| **High-Level** | Overview, communication |
| **Detailed** | Implementation, automation |

### Phase 2: Model the Process

#### Step 1: Identify Main Path (Happy Path)

1. Start event (trigger)
2. Main sequence of activities
3. End event (completion)

#### Step 2: Add Decision Points

For each decision:

- Type of gateway (XOR/AND/OR)
- Conditions for each path
- Reconvergence point

#### Step 3: Add Exception Paths

- Error handling
- Timeout scenarios
- Escalation paths

#### Step 4: Add Participants

- Assign activities to lanes
- Model inter-participant communication
- Add message flows between pools

### Phase 3: Validate and Document

#### Step 1: Validate Completeness

| Check | Question |
|-------|----------|
| All paths connected | Do all activities have incoming and outgoing flows? |
| No dead ends | Do all paths reach an end event? |
| Gateways balanced | Are split gateways matched with joins? |
| Roles assigned | Is every activity in a lane? |
| Triggers defined | Does every start event have a clear trigger? |

#### Step 2: Add Documentation

```markdown
## Process: [Name]

### Overview

[Brief description of process purpose and flow]

### Triggers

| Event | Description | Frequency |
|-------|-------------|-----------|
| [Trigger] | [What causes it] | [How often] |

### Activities

| # | Activity | Role | System | Duration |
|---|----------|------|--------|----------|
| 1 | [Activity name] | [Role] | [System] | [Time] |

### Decision Points

| # | Decision | Conditions | Paths |
|---|----------|------------|-------|
| 1 | [Decision] | [Criteria] | [Path A], [Path B] |

### Exceptions

| Exception | Handling |
|-----------|----------|
| [Error] | [How handled] |
```

## Output Formats

### Mermaid Flowchart (BPMN-Style)

```mermaid
flowchart TD
    Start((Start))
    Task1[Receive Order]
    Gateway1{Valid Order?}
    Task2[Process Payment]
    Task3[Reject Order]
    Task4[Ship Product]
    End1((Complete))
    End2((Rejected))

    Start --> Task1
    Task1 --> Gateway1
    Gateway1 -->|Yes| Task2
    Gateway1 -->|No| Task3
    Task2 --> Task4
    Task4 --> End1
    Task3 --> End2
```

### Swimlane Diagram

```mermaid
flowchart TD
    subgraph Customer
        A[Place Order]
        G[Receive Product]
    end

    subgraph Sales
        B[Review Order]
        C{Approved?}
    end

    subgraph Warehouse
        D[Pick Items]
        E[Pack Order]
        F[Ship Order]
    end

    A --> B
    B --> C
    C -->|Yes| D
    C -->|No| A
    D --> E
    E --> F
    F --> G
```

### Narrative Summary

```markdown
## Process: Order Fulfillment

**Version:** 1.0
**Date:** [ISO Date]
**Owner:** [Name]

### Summary

This process handles customer orders from receipt to delivery.

### Flow Description

1. **Start**: Customer places order (online or phone)
2. **Review Order**: Sales validates order details
3. **Decision**: Is order valid?
   - Yes: Proceed to fulfillment
   - No: Return to customer for correction
4. **Pick Items**: Warehouse locates products
5. **Pack Order**: Items packaged for shipping
6. **Ship Order**: Handed to carrier
7. **End**: Customer receives product

### Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Cycle Time | 3 days | 2 days |
| Error Rate | 5% | 1% |
| Automation | 40% | 70% |

### Improvement Opportunities

1. Automate order validation
2. Parallel picking for multi-item orders
3. Real-time tracking integration
```

### Structured Data (YAML)

```yaml
process_model:
  name: "Order Fulfillment"
  version: "1.0"
  date: "2025-01-15"
  type: "as_is"  # or "to_be"
  owner: "Operations"

  boundaries:
    trigger: "Customer places order"
    end_state: "Customer receives product"
    scope:
      includes:
        - "Order receipt"
        - "Payment processing"
        - "Fulfillment"
        - "Shipping"
      excludes:
        - "Returns"
        - "Customer support"

  participants:
    - pool: "Company"
      lanes:
        - name: "Sales"
          activities: ["Review Order"]
        - name: "Warehouse"
          activities: ["Pick Items", "Pack Order", "Ship Order"]
    - pool: "Customer"
      lanes:
        - name: "Buyer"
          activities: ["Place Order", "Receive Product"]

  elements:
    events:
      - id: "start_1"
        type: "start"
        name: "Order Received"
        trigger: "message"

      - id: "end_1"
        type: "end"
        name: "Order Complete"

    activities:
      - id: "task_1"
        type: "user_task"
        name: "Review Order"
        lane: "Sales"
        duration: "15 minutes"

      - id: "task_2"
        type: "service_task"
        name: "Process Payment"
        lane: "Sales"
        system: "Payment Gateway"

    gateways:
      - id: "gw_1"
        type: "exclusive"
        name: "Order Valid?"
        conditions:
          - path: "task_2"
            condition: "Order validated"
          - path: "task_reject"
            condition: "Validation failed"

  sequence_flows:
    - from: "start_1"
      to: "task_1"
    - from: "task_1"
      to: "gw_1"
    - from: "gw_1"
      to: "task_2"
      condition: "valid"

  metrics:
    cycle_time:
      current: "3 days"
      target: "2 days"
    automation_rate:
      current: 40
      target: 70
```

## Common Process Patterns

### Sequential Process

Activities in strict order, one after another.

```mermaid
flowchart LR
    A[Step 1] --> B[Step 2] --> C[Step 3] --> D[Step 4]
```

### Parallel Split and Join

Activities that can occur simultaneously.

```mermaid
flowchart TD
    A[Start] --> B{Parallel Split}
    B --> C[Task A]
    B --> D[Task B]
    B --> E[Task C]
    C --> F{Join}
    D --> F
    E --> F
    F --> G[End]
```

### Exclusive Decision

Only one path taken based on condition.

```mermaid
flowchart TD
    A[Review] --> B{Decision}
    B -->|Approve| C[Process]
    B -->|Reject| D[Notify]
    C --> E[End]
    D --> E
```

### Loop/Iteration

Repeat activities until condition met.

```mermaid
flowchart TD
    A[Start] --> B[Process]
    B --> C{Complete?}
    C -->|No| B
    C -->|Yes| D[End]
```

### Exception Handling

Handle errors and exceptions.

```mermaid
flowchart TD
    A[Process] --> B{Success?}
    B -->|Yes| C[Continue]
    B -->|Error| D[Handle Error]
    D --> E{Recoverable?}
    E -->|Yes| A
    E -->|No| F[Escalate]
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Start simple | Begin with happy path, add complexity |
| One start, one end | Per pool, ideally |
| Name activities | Use verb-noun format (e.g., "Review Order") |
| Label gateways | Show the decision question |
| Label conditions | Describe each outgoing path |
| Balance gateways | Split and join with matching types |
| Avoid crossing lines | Rearrange for clarity |
| Document exceptions | Show error handling paths |

## Integration

### Upstream

- **stakeholder-analysis** - Process participants
- **domain-storytelling** - Current process discovery
- **capability-mapping** - Capability context

### Downstream

- **value-stream-mapping** - Value flow analysis
- **Requirements** - Process requirements
- **System design** - Automation opportunities

## Related Skills

- `value-stream-mapping` - Lean perspective on process flow
- `data-modeling` - Data entities in processes
- `journey-mapping` - Customer experience perspective
- `capability-mapping` - Process-capability alignment

## Version History

- **v1.0.0** (2025-12-26): Initial release
