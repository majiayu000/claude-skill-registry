---
name: domain-storytelling
description: Collaborative domain modeling through pictographic stories. Use when gathering requirements, understanding business workflows, onboarding team members, or preparing for event storming. Follows Stefan Hofer & Henning Schwentner's methodology with actors, work objects, and activities.
allowed-tools: Read, Write, Glob, Grep, Skill, Task
---

# Domain Storytelling Skill

## Overview

Domain Storytelling is a collaborative modeling technique that captures business processes through pictographic stories. This skill guides AI-assisted domain storytelling sessions that can feed into event storming and bounded context discovery.

**Key Principle:** Stories are told from the perspective of domain experts, using their language and understanding.

## When to Use This Skill

**Keywords:** domain storytelling, pictographic, actors, work objects, activities, AS-IS, TO-BE, business workflow, domain modeling, story collection, bounded context discovery, requirements gathering

**Use this skill when:**

- Gathering requirements from domain experts
- Understanding existing business workflows (AS-IS)
- Designing future state processes (TO-BE)
- Onboarding team members to a domain
- Preparing for event storming sessions
- Identifying bounded context candidates
- Building a ubiquitous language glossary

## Story Types

### AS-IS Stories

Document how things work **today**:

- Current state processes
- Existing pain points
- Workarounds and exceptions
- Real behavior (not idealized)

**When to use:** Understanding current state, identifying problems, baseline before changes.

### TO-BE Stories

Document how things **should work**:

- Desired future state
- Improved processes
- New capabilities
- Idealized flow (but achievable)

**When to use:** Requirements gathering, designing solutions, communicating vision.

## Pictographic Language

Domain Storytelling uses simple pictographic elements:

| Element | Symbol | Description |
| --- | --- | --- |
| **Actor** | 🧑 (stick figure) | Person or system that performs activities |
| **Work Object** | 📄 (document) | Data, documents, or physical items exchanged |
| **Activity** | ➡️ (arrow with verb) | Action performed by an actor |
| **Sequence** | ① ② ③ | Numbered order of activities |
| **Annotation** | 💬 (note) | Additional context or explanation |

**Detailed notation guide:** See `references/pictographic-notation.md`

## AI-Assisted Story Collection Protocol

### Phase 1: Story Collection

**Goal:** Gather the narrative from the user in their own words.

**Prompts:**

- "Tell me about a typical [process] from start to finish"
- "Walk me through what happens when [trigger event]"
- "Who is involved and what do they do?"

**Capture:**

- Who does what (actors and activities)
- What they work with (work objects)
- In what order (sequence)
- Any variations or exceptions

### Phase 2: Story Refinement

**Goal:** Explore edge cases and variations.

**Prompts:**

- "What happens if [X] fails or is unavailable?"
- "Are there any special cases or exceptions?"
- "What's the most common path vs rare paths?"
- "What frustrates you about this process?"

**Capture:**

- Alternative flows
- Error handling
- Pain points
- Implicit knowledge

### Phase 3: Actor Identification

**Goal:** Map all participants in the story.

**Prompts:**

- "Who else is involved that we haven't mentioned?"
- "Are there any systems or external parties?"
- "Who approves, reviews, or audits?"

**Capture:**

- Human actors (by role, not name)
- System actors (internal and external)
- Actor responsibilities

### Phase 4: Work Object Cataloging

**Goal:** Identify all data and documents exchanged.

**Prompts:**

- "What information is passed between actors?"
- "What documents or forms are used?"
- "What data is created, updated, or referenced?"

**Capture:**

- Documents and forms
- Data entities
- Physical items (if applicable)
- Work object lifecycle

### Phase 5: Boundary Discovery

**Goal:** Find bounded context candidates.

**Analysis:**

- Where does terminology change?
- Which actors work together closely?
- What work objects belong together?
- Where are the natural handoff points?

**Output:** Potential bounded context candidates for event storming.

**Detailed boundary discovery:** See `references/boundary-discovery.md`

## Story Output Format

### Text Representation

```markdown
# Domain Story: [Story Name]

**Type:** AS-IS | TO-BE
**Domain:** [Domain Name]
**Date:** YYYY-MM-DD

## Narrative Summary

[2-3 sentence plain language summary]

## Story Sequence

① **Customer** submits **Order Form** to **Sales Rep**
② **Sales Rep** validates **Order Form** using **Product Catalog**
③ **Sales Rep** creates **Order** in **Order System**
④ **Order System** notifies **Warehouse** with **Pick List**
⑤ **Warehouse Staff** picks items using **Pick List**
...

## Actors

| Actor | Type | Responsibilities |
| --- | --- | --- |
| Customer | Human (External) | Initiates orders |
| Sales Rep | Human (Internal) | Validates and enters orders |
| Order System | System (Internal) | Order management |
| Warehouse | System (Internal) | Inventory and fulfillment |

## Work Objects

| Work Object | Type | Used By | Description |
| --- | --- | --- | --- |
| Order Form | Document | Customer, Sales Rep | Customer order request |
| Product Catalog | Reference | Sales Rep | Available products |
| Order | Data | Order System | Validated order record |
| Pick List | Document | Warehouse Staff | Items to pick |

## Annotations

- [Note 1]: Exception handling for out-of-stock items
- [Note 2]: Peak season requires additional staff
```

### Mermaid Diagram (Optional)

```text
sequenceDiagram
    participant C as Customer
    participant SR as Sales Rep
    participant OS as Order System
    participant W as Warehouse

    C->>SR: ① submits Order Form
    SR->>SR: ② validates using Product Catalog
    SR->>OS: ③ creates Order
    OS->>W: ④ notifies with Pick List
    W->>W: ⑤ picks items
```

**Story templates:** See `references/story-templates.md`

## Integration with Event Storming

Domain stories naturally feed into event storming:

| Story Element | Event Storming Element |
| --- | --- |
| Activity | Command or Event |
| Actor | Actor (yellow sticky) |
| Work Object | Aggregate or Read Model |
| Sequence | Timeline ordering |
| Boundary | Bounded context candidate |

**Workflow:**

```text
Domain Storytelling (understand "what happens")
    ↓
Event Storming (design "how it happens")
    ↓
Bounded Contexts → Modular Architecture
```

**To proceed to event storming:** Invoke the `enterprise-architecture:event-storming` skill with collected stories as input.

## Facilitation Modes

### Interactive Mode (Recommended)

The skill guides an interactive conversation with the user:

1. Ask open-ended questions
2. Capture responses as story elements
3. Reflect back for validation
4. Iterate until story is complete

### Quick Mode

Rapid story capture from user-provided narrative:

1. User provides full narrative
2. Skill extracts actors, work objects, activities
3. Skill structures into story format
4. User validates and refines

### Document Mode

Extract stories from existing documentation:

1. Read existing process documents
2. Extract story elements
3. Structure into story format
4. Validate with user

## Glossary Building

As stories are collected, build a domain glossary:

| Term | Definition | Context | Aliases |
| --- | --- | --- | --- |
| Order | A validated customer request for products | Sales | Purchase Order, PO |
| Pick List | List of items to retrieve from warehouse | Warehouse | Picking Ticket |

**Glossary purpose:**

- Establishes ubiquitous language
- Identifies term collisions (same word, different meanings)
- Documents domain knowledge
- Supports bounded context discovery

## Best Practices

### DO

- Use domain expert's language, not technical jargon
- Capture stories at the right granularity (not too detailed)
- Include exceptions and variations
- Number activities sequentially
- Document annotations for implicit knowledge
- Build glossary as you go

### DON'T

- Impose technical terminology
- Skip edge cases and exceptions
- Assume you understand without asking
- Mix AS-IS and TO-BE in same story
- Forget to validate with domain expert

## References

- `references/pictographic-notation.md` - Detailed notation guide with examples
- `references/story-templates.md` - YAML headers, output formats
- `references/boundary-discovery.md` - Finding bounded contexts from stories

## Related Skills

- `event-storming` - Design "how it happens" after understanding "what happens"
- `modular-architecture` - Implement bounded contexts discovered from stories
- `adr-management` - Document significant decisions discovered during storytelling

---

**Last Updated:** 2025-12-22

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
