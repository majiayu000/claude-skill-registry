---
name: service-blueprinting
description: Create service blueprints - frontstage/backstage visualization, touchpoints, support processes, evidence, and service design methodology.
allowed-tools: Read, Glob, Grep, Task
---

# Service Blueprinting

Design and visualize end-to-end service experiences, including customer interactions, employee actions, and supporting systems.

## When to Use This Skill

Use this skill when:

- **Service Blueprinting tasks** - Working on create service blueprints - frontstage/backstage visualization, touchpoints, support processes, evidence, and service design methodology
- **Planning or design** - Need guidance on Service Blueprinting approaches
- **Best practices** - Want to follow established patterns and standards

## MANDATORY: Skill Loading First

Before answering ANY service design question:

2. Use established service design methodology (Shostack, Nielsen Norman)
3. Base all guidance on validated service blueprinting practices

## Service Blueprint Anatomy

### The Five Lanes

```text
┌─────────────────────────────────────────────────────────────────┐
│                    PHYSICAL EVIDENCE                             │
│  (What customer sees, receives, interacts with)                  │
├─────────────────────────────────────────────────────────────────┤
│                    CUSTOMER ACTIONS                              │
│  (Steps the customer takes)                                      │
├─────────────────────────── LINE OF INTERACTION ─────────────────┤
│                    FRONTSTAGE ACTIONS                            │
│  (Employee actions visible to customer)                          │
├─────────────────────────── LINE OF VISIBILITY ──────────────────┤
│                    BACKSTAGE ACTIONS                             │
│  (Employee actions hidden from customer)                         │
├─────────────────────────── LINE OF INTERNAL INTERACTION ────────┤
│                    SUPPORT PROCESSES                             │
│  (Systems, partners, policies that enable service)               │
└─────────────────────────────────────────────────────────────────┘
```

### Additional Lanes (Extended Blueprint)

| Lane | Description |
|------|-------------|
| **Time** | Duration of each step |
| **Emotional Journey** | Customer feelings throughout |
| **Metrics** | KPIs for each touchpoint |
| **Fail Points** | Where things can go wrong |
| **Wait Points** | Where delays occur |
| **Ownership** | Who's responsible |

## Blueprint Components

### Physical Evidence

What tangible or visible elements does the customer encounter?

```csharp
public class PhysicalEvidence
{
    public required string Name { get; init; }
    public required EvidenceType Type { get; init; }
    public required string Description { get; init; }
    public string? DesignConsiderations { get; init; }
}

public enum EvidenceType
{
    Digital,        // Website, app, email
    Physical,       // Store, packaging, receipt
    Environmental,  // Signage, ambiance
    Documentation,  // Forms, contracts
    Communication   // Notifications, confirmations
}
```

### Customer Actions

What steps does the customer take?

```csharp
public class CustomerAction
{
    public int Step { get; init; }
    public required string Action { get; init; }
    public required string Intent { get; init; } // What they're trying to achieve
    public required CustomerChannel Channel { get; init; }
    public TimeSpan? ExpectedDuration { get; init; }
    public string? PainPoint { get; init; }
    public string? Opportunity { get; init; }
}

public enum CustomerChannel
{
    Web,
    Mobile,
    Phone,
    InPerson,
    Email,
    Chat,
    Social
}
```

### Frontstage Actions

Employee actions the customer sees:

```csharp
public class FrontstageAction
{
    public int Step { get; init; }
    public required string Action { get; init; }
    public required string Actor { get; init; } // Role/system
    public required InteractionType Type { get; init; }
    public bool IsAutomated { get; init; }
    public List<string> Dependencies { get; init; } = [];
}

public enum InteractionType
{
    Synchronous,    // Real-time interaction
    Asynchronous,   // Email, notification
    SelfService,    // Customer-driven with system
    Assisted        // Employee helps customer
}
```

### Backstage Actions

Hidden operations that enable the service:

```csharp
public class BackstageAction
{
    public int Step { get; init; }
    public required string Action { get; init; }
    public required string Owner { get; init; }
    public required string TriggeredBy { get; init; }
    public TimeSpan? SLA { get; init; }
    public List<string> Systems { get; init; } = [];
    public string? FailureMode { get; init; }
}
```

### Support Processes

Systems and capabilities that enable everything:

```csharp
public class SupportProcess
{
    public required string Name { get; init; }
    public required SupportType Type { get; init; }
    public required string Description { get; init; }
    public List<string> DependentActions { get; init; } = [];
}

public enum SupportType
{
    Technology,     // CRM, database, APIs
    Policy,         // Business rules, compliance
    Partner,        // Third-party services
    Training,       // Employee knowledge
    Infrastructure  // Physical or cloud resources
}
```

## Blueprint Template

````markdown
# Service Blueprint: [Service Name]

## Service Overview
- **Service:** [Name]
- **Scope:** [Start point] to [End point]
- **Primary Persona:** [Target user]
- **Service Promise:** [Value proposition]

---

## Blueprint

### Stage 1: [Stage Name]

| Element | Details |
|---------|---------|
| **Physical Evidence** | [What customer sees] |
| **Customer Action** | [What customer does] |
| **Frontstage** | [Visible employee/system action] |
| **Backstage** | [Hidden operations] |
| **Support** | [Enabling systems/processes] |
| **Duration** | [Time] |
| **Emotion** | [Customer feeling] |
| **Fail Point** | [What could go wrong] |

### Stage 2: [Stage Name]
[Continue pattern...]

---

## Visual Blueprint

```text

Time →     [5 min]        [2 min]         [24 hrs]       [5 min]
           ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
Evidence   │ Website │    │ Form    │    │ Email   │    │ Product │
           └─────────┘    └─────────┘    └─────────┘    └─────────┘

           ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
Customer   │ Browse  │───►│ Submit  │───►│ Receive │───►│ Unbox   │
           │ catalog │    │ order   │    │ confirm │    │ product │
           └─────────┘    └─────────┘    └─────────┘    └─────────┘
           ═══════════════════════════════════════════════════════════
           Line of Interaction
           ═══════════════════════════════════════════════════════════
           ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
Frontstage │ Display │    │ Confirm │    │ Send    │    │ Deliver │
           │ products│    │ payment │    │ updates │    │ package │
           └─────────┘    └─────────┘    └─────────┘    └─────────┘
           ═══════════════════════════════════════════════════════════
           Line of Visibility
           ═══════════════════════════════════════════════════════════
           ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
Backstage  │ Catalog │    │ Process │    │ Pick &  │    │ Shipping│
           │ mgmt    │    │ payment │    │ pack    │    │ handoff │
           └─────────┘    └─────────┘    └─────────┘    └─────────┘
           ═══════════════════════════════════════════════════════════
           Line of Internal Interaction
           ═══════════════════════════════════════════════════════════
           ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
Support    │ Product │    │ Payment │    │ WMS     │    │ Carrier │
           │ database│    │ gateway │    │         │    │ API     │
           └─────────┘    └─────────┘    └─────────┘    └─────────┘

Emotion    😊 Curious    😟 Anxious     😌 Relieved   🎉 Excited
           ─────────────────────────────────────────────────────────
                        ▼ Fail Point: Payment decline

```

---

## Pain Points & Opportunities

### Identified Pain Points

| Stage | Pain Point | Impact | Root Cause |
|-------|------------|--------|------------|
| [Stage] | [Issue] | [H/M/L] | [Why it happens] |

### Improvement Opportunities

| Stage | Opportunity | Expected Impact | Effort |
|-------|-------------|-----------------|--------|
| [Stage] | [Idea] | [Benefit] | [H/M/L] |

---

## Metrics

| Touchpoint | Metric | Current | Target |
|------------|--------|---------|--------|
| [Stage] | [Measure] | [Value] | [Goal] |

---

## Dependencies & Risks

### System Dependencies

| System | Used By | Risk Level | Mitigation |
|--------|---------|------------|------------|
| [System] | [Stages] | [H/M/L] | [Plan] |

### Fail Points

| Stage | Failure Mode | Probability | Impact | Recovery |
|-------|--------------|-------------|--------|----------|
| [Stage] | [What fails] | [H/M/L] | [Effect] | [How to recover] |

````

## Service Moments

### Moment Types

| Moment Type | Definition | Example |
|-------------|------------|---------|
| **Moment of Truth** | Critical interaction that shapes perception | First contact, payment, delivery |
| **Moment of Waiting** | Customer experiences delay | Processing, shipping |
| **Moment of Failure** | Something goes wrong | Error, stockout |
| **Moment of Delight** | Exceeds expectations | Surprise upgrade |

### Moment Analysis

```csharp
public class ServiceMoment
{
    public int Stage { get; init; }
    public required string Name { get; init; }
    public required MomentType Type { get; init; }
    public required int ImportanceScore { get; init; } // 1-10
    public required int CurrentPerformance { get; init; } // 1-10
    public decimal GapScore => ImportanceScore - CurrentPerformance;
    public string? Opportunity { get; init; }
}

public enum MomentType
{
    Truth,
    Waiting,
    Failure,
    Delight,
    Routine
}

// Prioritization: Focus on high importance + low performance
public static IEnumerable<ServiceMoment> PrioritizeImprovements(
    IEnumerable<ServiceMoment> moments) =>
    moments
        .Where(m => m.ImportanceScore >= 7)
        .OrderByDescending(m => m.GapScore)
        .ThenByDescending(m => m.ImportanceScore);
```

## Cross-Channel Blueprint

For omnichannel services, map the journey across channels:

```text
           Web          Mobile        Phone         Store
           ┌────────────────────────────────────────────────┐
Stage 1    │ Research   │ Research   │     -       │   -    │
           ├────────────────────────────────────────────────┤
Stage 2    │ Compare    │ Compare    │     -       │ Browse │
           ├────────────────────────────────────────────────┤
Stage 3    │ Order      │ Order      │     -       │ Order  │
           ├────────────────────────────────────────────────┤
Stage 4    │     -      │ Track      │ Support     │ Pickup │
           ├────────────────────────────────────────────────┤
Stage 5    │ Review     │ Review     │     -       │   -    │
           └────────────────────────────────────────────────┘

Channel Transitions:
- Web → Mobile: Save cart sync
- Mobile → Store: Store availability check
- Phone ↔ Any: Case continuity
```

## .NET Service Blueprint Model

```csharp
public class ServiceBlueprint
{
    public Guid Id { get; init; }
    public required string ServiceName { get; init; }
    public required string Scope { get; init; }
    public required Persona PrimaryPersona { get; init; }
    public required List<BlueprintStage> Stages { get; init; }

    public IEnumerable<FailPoint> GetFailPoints() =>
        Stages.SelectMany(s => s.FailPoints);

    public IEnumerable<BlueprintStage> GetCriticalMoments() =>
        Stages.Where(s => s.IsMomentOfTruth);

    public TimeSpan TotalDuration =>
        TimeSpan.FromTicks(Stages.Sum(s => s.Duration?.Ticks ?? 0));
}

public class BlueprintStage
{
    public int Order { get; init; }
    public required string Name { get; init; }

    // The five lanes
    public List<PhysicalEvidence> Evidence { get; init; } = [];
    public required CustomerAction CustomerAction { get; init; }
    public required FrontstageAction FrontstageAction { get; init; }
    public List<BackstageAction> BackstageActions { get; init; } = [];
    public List<SupportProcess> SupportProcesses { get; init; } = [];

    // Extended lanes
    public TimeSpan? Duration { get; init; }
    public EmotionalState? CustomerEmotion { get; init; }
    public List<FailPoint> FailPoints { get; init; } = [];
    public List<string> Metrics { get; init; } = [];
    public bool IsMomentOfTruth { get; init; }
    public string? Owner { get; init; }
}

public class FailPoint
{
    public required string Description { get; init; }
    public required FailureProbability Probability { get; init; }
    public required FailureImpact Impact { get; init; }
    public required string RecoveryProcedure { get; init; }
    public string? PreventionMeasure { get; init; }
}

public enum FailureProbability { Rare, Occasional, Frequent }
public enum FailureImpact { Low, Medium, High, Critical }

public enum EmotionalState
{
    Frustrated,
    Anxious,
    Neutral,
    Satisfied,
    Delighted
}
```

## Blueprinting Workshop

### Workshop Agenda

```markdown
## Service Blueprinting Workshop

**Duration:** 3-4 hours
**Participants:** Cross-functional team (design, product, ops, support)

### Before Workshop
- [ ] Define service scope
- [ ] Identify key personas
- [ ] Gather existing journey maps
- [ ] Prepare materials (sticky notes, markers, template)

### Workshop Flow

**Part 1: Set Context (30 min)**
1. Review service scope and persona
2. Share existing research/data
3. Align on goals

**Part 2: Customer Journey (45 min)**
1. Map customer actions (sticky notes)
2. Sequence and refine
3. Identify channels at each step

**Part 3: Lines of Interaction (30 min)**
1. Add frontstage actions
2. Draw line of visibility
3. Add backstage actions

**Part 4: Support Systems (30 min)**
1. Identify technology dependencies
2. Map policies and partners
3. Note training needs

**Part 5: Analysis (45 min)**
1. Mark fail points
2. Identify pain points
3. Spot opportunities
4. Add emotional journey
5. Note metrics

**Part 6: Prioritize (30 min)**
1. Vote on priority improvements
2. Assign ownership
3. Define next steps

### Outputs
- [ ] Completed service blueprint
- [ ] Prioritized improvement backlog
- [ ] Action items with owners
```

## Checklist: Service Blueprint

### Preparation

- [ ] Service scope defined
- [ ] Primary persona identified
- [ ] Stakeholders aligned
- [ ] Existing data gathered

### Blueprint Elements

- [ ] All customer actions mapped
- [ ] Physical evidence identified
- [ ] Frontstage actions documented
- [ ] Backstage actions documented
- [ ] Support processes identified
- [ ] Time estimates added
- [ ] Emotional journey mapped

### Analysis

- [ ] Fail points identified
- [ ] Wait points noted
- [ ] Pain points documented
- [ ] Opportunities surfaced
- [ ] Metrics defined

### Validation

- [ ] Cross-functional review
- [ ] Reality check with operations
- [ ] Customer validation (if possible)

## Related Skills

- `journey-mapping` (business-analysis) - Customer journey focus
- `user-research-planning` - Research for blueprinting
- `prototype-strategy` - Prototyping service touchpoints
- `process-modeling` (business-analysis) - BPMN process flows
