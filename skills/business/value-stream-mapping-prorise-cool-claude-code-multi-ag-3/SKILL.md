---
name: value-stream-mapping
description: Lean value stream mapping for identifying waste and optimization opportunities. Creates current/future state maps with cycle time analysis and improvement recommendations.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Value Stream Mapping

Create Lean value stream maps to visualize flow, identify waste, and design improvement opportunities. Based on Lean manufacturing principles adapted for knowledge work.

## What is a Value Stream?

A **value stream** is the sequence of activities required to deliver value to a customer, from request to delivery. Value stream mapping (VSM) visualizes this flow to identify:

- **Value-adding activities** - Steps that directly create customer value
- **Waste (Muda)** - Steps that consume resources without adding value
- **Flow problems** - Bottlenecks, delays, and inefficiencies

## The 8 Wastes (TIMWOODS)

| Waste | Description | Examples in Knowledge Work |
|-------|-------------|---------------------------|
| **T**ransportation | Moving work between locations | Handoffs between teams, tool switching |
| **I**nventory | Unfinished work waiting | Backlog, WIP, queued requests |
| **M**otion | Unnecessary movement | Context switching, searching for info |
| **W**aiting | Idle time | Approvals, blocked work, dependencies |
| **O**verproduction | Making more than needed | Unused features, premature optimization |
| **O**verprocessing | Doing more than required | Gold plating, excessive documentation |
| **D**efects | Errors requiring rework | Bugs, miscommunication, rework |
| **S**kills | Underutilized talent | Manual work that could be automated |

## Workflow

### Phase 1: Define Scope

#### Step 1: Identify the Value Stream

| Question | Answer |
|----------|--------|
| What value are we delivering? | [Customer outcome] |
| Who is the customer? | [Internal/External customer] |
| Where does the stream start? | [Trigger/Request] |
| Where does it end? | [Value delivered] |

#### Step 2: Set Boundaries

```markdown
## Value Stream Definition

**Name:** Customer Order Fulfillment
**Trigger:** Customer places order
**End State:** Customer receives product
**Scope:** Order entry → Shipping (excludes manufacturing)
**Customer:** External retail customer
```

### Phase 2: Current State Map

#### Step 1: Walk the Process

Observe actual work (gemba walk):

- Follow a real work item through the process
- Document what actually happens, not what should happen
- Note handoffs, delays, and workarounds

#### Step 2: Document Process Steps

For each step, capture:

| Metric | Definition | How to Measure |
|--------|------------|----------------|
| **Process Time (PT)** | Active work time | Time actually working |
| **Lead Time (LT)** | Total elapsed time | Clock time start to finish |
| **Wait Time (WT)** | Time waiting | LT - PT |
| **% Complete & Accurate (%C&A)** | First-time quality | % not requiring rework |

#### Step 3: Create Current State Map

```markdown
## Current State Value Stream

| Step | Owner | PT | LT | %C&A | Inventory | Notes |
|------|-------|-----|-----|------|-----------|-------|
| Order Entry | Sales | 15m | 2h | 85% | 50 orders | Manual entry |
| Credit Check | Finance | 10m | 8h | 95% | 30 orders | Batch processing |
| Inventory Alloc | Warehouse | 5m | 4h | 90% | 20 orders | System lookup |
| Pick & Pack | Warehouse | 30m | 6h | 92% | 40 orders | Manual process |
| Ship | Logistics | 10m | 24h | 98% | 100 orders | Carrier pickup |

**Total Process Time:** 70 minutes
**Total Lead Time:** 44 hours
**Flow Efficiency:** 2.7% (PT / LT)
```

### Phase 3: Analyze Waste

#### Step 1: Calculate Flow Efficiency

```text
Flow Efficiency = Process Time / Lead Time × 100%

Example: 70 min / 2640 min = 2.7%
```

**Interpretation:**

- < 5%: Significant waste (typical for unoptimized processes)
- 5-15%: Moderate efficiency
- 15-25%: Good efficiency
- > 25%: Excellent (rare for knowledge work)

#### Step 2: Identify Waste by Type

```markdown
## Waste Analysis

### Waiting (45% of lead time)
- Credit check batch processing: 8 hours → could be real-time
- Carrier pickup schedule: 24 hours → could be on-demand

### Inventory (150 orders WIP)
- Orders queue at each step
- No pull system in place

### Defects (15% rework at order entry)
- Manual data entry errors
- Missing required fields

### Overprocessing
- Full credit check for returning customers
- Duplicate data entry across systems
```

#### Step 3: Identify Bottlenecks

The constraint (bottleneck) limits the entire system:

```markdown
## Bottleneck Analysis

**Primary Bottleneck:** Credit Check
- Highest queue (30 orders)
- Batch processing creates 8-hour wait
- Blocks downstream flow

**Secondary Bottleneck:** Pick & Pack
- Manual process
- Variable cycle time
```

### Phase 4: Future State Design

#### Step 1: Apply Lean Principles

| Principle | Current Problem | Future State Solution |
|-----------|----------------|----------------------|
| **Flow** | Batch processing | Continuous flow, single-piece |
| **Pull** | Push based on forecast | Pull based on demand |
| **Perfection** | Accept defects, fix later | Build quality in |

#### Step 2: Design Improvements

```markdown
## Future State Design

### Eliminate Waiting
- Real-time credit API vs. batch
- On-demand carrier pickup

### Reduce Inventory
- WIP limits at each step
- Pull signals between steps

### Improve Quality
- Validation at order entry
- Auto-populate from CRM

### Automate Motion Waste
- Single system vs. multiple tools
- API integrations
```

#### Step 3: Create Future State Map

```markdown
## Future State Value Stream

| Step | Owner | PT | LT | %C&A | Inventory | Changes |
|------|-------|-----|-----|------|-----------|---------|
| Order Entry | Sales | 10m | 30m | 98% | 10 orders | Validation, auto-fill |
| Credit Check | System | 1m | 5m | 99% | 0 | Real-time API |
| Inventory Alloc | System | 1m | 5m | 99% | 0 | Automated |
| Pick & Pack | Warehouse | 25m | 2h | 96% | 15 orders | Better tooling |
| Ship | Logistics | 10m | 4h | 99% | 20 orders | On-demand pickup |

**Target Process Time:** 47 minutes (33% reduction)
**Target Lead Time:** 6.7 hours (85% reduction)
**Target Flow Efficiency:** 11.7% (4x improvement)
```

### Phase 5: Implementation Roadmap

#### Step 1: Prioritize Improvements

| Improvement | Impact | Effort | Priority |
|-------------|--------|--------|----------|
| Real-time credit API | High (8h → 5m) | Medium | 1 |
| Order entry validation | Medium (15% → 2% errors) | Low | 2 |
| On-demand carrier | High (24h → 4h) | High | 3 |
| Automated inventory | Medium | Medium | 4 |

#### Step 2: Define Kaizen Events

Focused improvement workshops:

```markdown
## Kaizen Event: Credit Check Automation

**Scope:** Eliminate credit check batch processing
**Target:** 8 hours → 5 minutes lead time
**Team:** Finance, IT, Process Owner
**Duration:** 1 week intensive
**Deliverables:**
- API integration specification
- Process redesign
- Training materials
```

## Output Formats

### Narrative Summary

```markdown
## Value Stream Analysis Summary

**Value Stream:** [Name]
**Date:** [ISO date]
**Analyst:** value-stream-analyst

### Current State Metrics
- **Process Time:** X minutes
- **Lead Time:** Y hours
- **Flow Efficiency:** Z%
- **Primary Bottleneck:** [Step]

### Top Waste Categories
1. **Waiting (X% of LT):** [Description]
2. **Inventory (X orders WIP):** [Description]
3. **[Other waste]:** [Description]

### Future State Targets
- **Lead Time Reduction:** X%
- **Flow Efficiency Target:** Y%
- **Quality Target:** Z% first-time right

### Recommended Actions
1. [High priority improvement]
2. [Medium priority improvement]
3. [Lower priority improvement]
```

### Structured Data (YAML)

```yaml
value_stream:
  name: "Customer Order Fulfillment"
  version: "1.0"
  date: "{ISO-8601-date}"
  analyst: "value-stream-analyst"

  boundaries:
    trigger: "Customer places order"
    end_state: "Customer receives product"
    customer: "External retail customer"

  current_state:
    total_process_time_minutes: 70
    total_lead_time_hours: 44
    flow_efficiency_percent: 2.7
    wip_total: 240

    steps:
      - name: "Order Entry"
        owner: "Sales"
        process_time_minutes: 15
        lead_time_hours: 2
        complete_accurate_percent: 85
        inventory: 50
        waste_types:
          - type: defects
            description: "Manual entry errors"
          - type: motion
            description: "Multiple system entry"

      - name: "Credit Check"
        owner: "Finance"
        process_time_minutes: 10
        lead_time_hours: 8
        complete_accurate_percent: 95
        inventory: 30
        is_bottleneck: true
        waste_types:
          - type: waiting
            description: "Batch processing"

  waste_analysis:
    - type: waiting
      percent_of_lead_time: 45
      root_causes:
        - "Batch processing"
        - "Scheduled pickups"

    - type: inventory
      total_wip: 240
      root_causes:
        - "No WIP limits"
        - "Push system"

  future_state:
    target_process_time_minutes: 47
    target_lead_time_hours: 6.7
    target_flow_efficiency_percent: 11.7

    improvements:
      - name: "Real-time credit API"
        waste_eliminated: waiting
        impact: high
        effort: medium
        lead_time_reduction_hours: 7.9

  roadmap:
    - phase: 1
      improvements: ["Real-time credit API", "Order validation"]
      duration_weeks: 4

    - phase: 2
      improvements: ["On-demand carrier", "Inventory automation"]
      duration_weeks: 8
```

### Mermaid Diagrams

**Current State Flow:**

```mermaid
flowchart LR
    subgraph Current State
        A[Order Entry<br/>PT: 15m | LT: 2h<br/>WIP: 50] --> B[Credit Check<br/>PT: 10m | LT: 8h<br/>WIP: 30]
        B --> C[Inventory<br/>PT: 5m | LT: 4h<br/>WIP: 20]
        C --> D[Pick & Pack<br/>PT: 30m | LT: 6h<br/>WIP: 40]
        D --> E[Ship<br/>PT: 10m | LT: 24h<br/>WIP: 100]
    end

    style B fill:#ff9999
```

**Future State Flow:**

```mermaid
flowchart LR
    subgraph Future State
        A[Order Entry<br/>PT: 10m | LT: 30m<br/>WIP: 10] --> B[Credit<br/>API: 1m<br/>WIP: 0]
        B --> C[Inventory<br/>Auto: 1m<br/>WIP: 0]
        C --> D[Pick & Pack<br/>PT: 25m | LT: 2h<br/>WIP: 15]
        D --> E[Ship<br/>PT: 10m | LT: 4h<br/>WIP: 20]
    end

    style B fill:#99ff99
    style C fill:#99ff99
```

## When to Use

| Scenario | Use Value Stream Mapping? |
|----------|--------------------------|
| Process improvement | Yes - identify waste |
| New system design | Yes - design for flow |
| Cost reduction | Yes - find inefficiencies |
| Lead time complaints | Yes - find bottlenecks |
| Quality problems | Partial - with root cause analysis |
| Greenfield project | Maybe - limited current state |

## Integration

### Upstream (Discovery)

- **process-modeling** - Understand current process
- **capability-mapping** - Link to business capabilities
- **stakeholder-analysis** - Identify process owners

### Downstream

- **Requirements** - Improvement requirements
- **Systems design** - Automation opportunities
- **Project planning** - Kaizen event planning

## Related Skills

- `journey-mapping` - Customer experience perspective
- `capability-mapping` - Capability view of value delivery
- `root-cause-analysis` - Investigate bottleneck causes
- `prioritization` - Prioritize improvement initiatives
- `process-modeling` - Detailed BPMN process diagrams
- `estimation` - Estimate improvement effort
- `benchmarking` - Current vs target comparison

## Version History

- **v1.0.0** (2025-12-26): Initial release
