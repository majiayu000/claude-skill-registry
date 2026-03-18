---
name: product-primitives
description: >-
  Break down complex products, features, or systems into fundamental primitives and building blocks
  from a software creator's perspective. Use when starting a new application, designing a large feature,
  or needing to understand a complex system's moving parts before building. Trigger phrases: "break down X",
  "decompose this", "what are the primitives", "building blocks of Z", "map the architecture",
  "what are the moving parts", "analyze this system", or any situation where you need to identify the
  atomic, reusable capabilities that compose a system. Complements product-thinker (user perspective)
  with the builder's perspective (system-level connections).
---

# Product Primitives

Break complex systems into fundamental primitives — deep, information-hiding building blocks with clear boundaries and simple interfaces. Think from the software creator's perspective: what are the atomic capabilities this system needs, how do they connect, and where should the boundaries be?

## When to Use

One-off analysis for big-picture thinking — new applications, large features, or understanding existing system architecture. While `/dev-skills:product-thinker` thinks from the user's perspective, product primitives thinks from the builder's perspective, identifying where to draw module boundaries and what each piece should encapsulate.

Use `Explore` sub-agents to research the codebase if working in an existing project. Use browser (Chrome DevTools MCP) to walk through the product if it's running.

## How to Decompose

The quality of a decomposition depends on where you draw boundaries. Use these principles to guide every boundary decision:

### Deep, not shallow
Each primitive should have a simple interface hiding significant functionality. If a primitive's interface is as complex as what it does internally, it's not a useful building block — it's just indirection. A good primitive absorbs complexity so that anything composing it stays simple.

### Information hiding
Each primitive should encapsulate a design decision — a piece of knowledge that nothing outside it needs to know. The data format, the algorithm, the storage mechanism, the external API quirks — these should live inside one primitive, not leak across boundaries. When you can change a primitive's internals without affecting anything else, the boundary is right.

### Split by knowledge, not by time
Don't decompose by execution order ("first we ingest, then we transform, then we store"). This is temporal decomposition — it leaks information because operations that happen at different times often share the same knowledge. Instead, ask: what distinct pieces of knowledge does this system need? Each piece of knowledge becomes a primitive.

### Bring together or split apart?
- **Merge** when two pieces share information, are always used together, or can't be understood independently
- **Split** when pieces are truly independent and separating them reduces the total complexity
- **Test**: will developers need to read both to understand either? If yes, they belong together

### Pull complexity downward
When complexity is unavoidable, push it into lower-level primitives so that higher-level composition stays simple. The primitives should suffer so that the system using them doesn't have to.

## What Makes a Good Primitive

- **Deep** — simple interface, powerful functionality behind it
- **Encapsulating** — hides a design decision; internals can change without rippling outward
- **Composable** — combines with other primitives through simple, obvious interfaces
- **Transferable** — useful in multiple workflows, not tied to one specific scenario

## Red Flags

- **Shallow primitive** — interface is as complex as implementation, not hiding anything useful
- **Information leakage** — same knowledge (format, protocol, business rule) appears in multiple primitives
- **Temporal decomposition** — boundaries mirror execution order instead of knowledge boundaries
- **Pass-through primitive** — does nothing but forward to another primitive with a similar interface
- **Conjoined primitives** — can't understand one without understanding the other

## Output Format

```markdown
## System: [Name]

[1-2 sentence description of what this system does]

## Primitives

### 1. [Primitive Name]
**Purpose**: What it does
**Encapsulates**: What knowledge/decisions it hides
**Interface**: What callers need to know (inputs → outputs)

### 2. [Next Primitive]
...

## How They Fit Together

[ASCII diagram showing relationships and data flow]

## Composition Examples

[Show how 2-3 user workflows are composed from these primitives]
```

## Example

**Input**: "Break down an e-commerce marketing automation system"

**Output**:

```markdown
## System: E-commerce Marketing Automation

Automate marketing campaigns for online stores — segment customers, create campaigns,
schedule sends, and measure results.

## Primitives

### 1. Audience Segmentation
**Purpose**: Group customers by behavior, demographics, or purchase history
**Encapsulates**: Segment rule evaluation logic, membership caching, refresh scheduling
**Interface**: (segment rules, customer data) → named segments with member lists

### 2. Campaign Composition
**Purpose**: Assemble a campaign from template, audience, and schedule
**Encapsulates**: Campaign state machine (draft → scheduled → sent → completed),
validation rules, duplication logic
**Interface**: (template + segment + schedule) → ready-to-send campaign

### 3. Content Rendering
**Purpose**: Produce personalized email/SMS content from templates + product data
**Encapsulates**: Template engine, personalization token resolution, product data lookup
**Interface**: (template + recipient + products) → rendered content

### 4. Send Orchestration
**Purpose**: Execute campaign delivery respecting rate limits and timing
**Encapsulates**: Channel-specific delivery (email vs SMS), rate limiting, retry logic,
bounce handling
**Interface**: (campaign + recipients + content) → delivery receipts

### 5. Performance Measurement
**Purpose**: Track opens, clicks, conversions, revenue attribution
**Encapsulates**: Event aggregation, attribution models, metric computation
**Interface**: (delivery events + interactions + orders) → campaign metrics

## How They Fit Together

┌──────────────────┐
│    Audience       │
│  Segmentation     │──────────────────────┐
└────────┬─────────┘                       │
         │ segments                        │ segment scores
         ▼                                 │
┌──────────────────┐    ┌───────────────┐  │
│    Campaign       │───▶│   Content     │  │
│   Composition     │    │  Rendering    │  │
└────────┬─────────┘    └───────┬───────┘  │
         │ campaign              │ content  │
         ▼                       ▼          │
      ┌──────────────────────────┐          │
      │    Send Orchestration    │          │
      └────────────┬─────────────┘          │
                   │ delivery events        │
                   ▼                        │
      ┌──────────────────────────┐          │
      │ Performance Measurement  │──────────┘
      └──────────────────────────┘
        (feeds back into segmentation)

## Composition Examples

**Scheduled newsletter**: Segmentation → Composition → Rendering → Orchestration → Measurement
**Triggered welcome series**: (event) → Composition → Rendering → Orchestration
**Re-engagement**: Measurement (inactive users) → Segmentation → Composition → ...

Note: each arrow represents a simple interface — the receiving primitive doesn't need to know
how the sending primitive works internally. Orchestration doesn't know how Rendering chose
which products to feature; Measurement doesn't know how Orchestration handled rate limits.
```

## Handoffs

- Pair with `/dev-skills:product-thinker` for user-perspective analysis alongside system decomposition
- Feed individual primitives into `/dev-skills:shaping-work` to shape them as work items
