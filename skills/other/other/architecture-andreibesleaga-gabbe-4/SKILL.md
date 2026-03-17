---
name: domain-model
description: Create or review a domain model for a system — identifying bounded contexts, entities, value objects, aggregates, domain events, and context relationships. Technology-agnostic. Works from requirements or from existing system descriptions.
triggers: [domain model, bounded context, ubiquitous language, context map, domain design, domain analysis, domain events, aggregate, entities, DDD analysis]
context_cost: medium
---

# Domain Model Skill

## Goal

Produce a clear domain model that captures the business concepts and their relationships.
This model is the shared language between stakeholders and developers — it drives naming,
component boundaries, and data design. Technology-agnostic: no database tables, no
class syntax, no framework artifacts.

---

## When to Use

- **Scenario 1 (New product)**: Before designing architecture. "What are the core business concepts?"
- **Scenario 2 (Existing system review)**: "Does the current system model correctly reflect the domain?"
- **Before splitting a monolith**: Identify bounded context boundaries.
- **When teams disagree on terminology**: Model the language explicitly.

---

## Step 1 — Discover Ubiquitous Language

```
Ubiquitous language = the vocabulary shared between all stakeholders and code.
The same term must mean the same thing everywhere.

Discovery process:
  1. Extract all nouns from requirements documents
     (These are candidate domain concepts: entities, value objects)
  2. Extract all verbs and verb phrases
     (These are candidate domain events and domain operations)
  3. Interview or analyze stakeholder language
     (What terms do domain experts use naturally?)

Build a Glossary:
  | Term | Definition | Context (if term varies by subdomain) |
  |------|-----------|---------------------------------------|
  | Order | A confirmed request to purchase items | Order Management context |
  | Order | The ranked sequence in search results | Search context |
  (Same word, different meaning = CONTEXT BOUNDARY SIGNAL)

Glossary rules:
  - One term = one meaning within a context
  - Ambiguous terms signal bounded context boundaries
  - Technical terms forbidden in ubiquitous language
  - Business domain terms only
```

---

## Step 2 — Identify Bounded Contexts

```
Bounded context = a section of the domain where a model (ubiquitous language) is consistent.
Within a bounded context, all terms have unambiguous meaning.

Signals of a bounded context boundary:
  - The same word means different things (see glossary step)
  - A team owns this area independently
  - Different data lifecycle (orders have a lifecycle independent of catalog)
  - Different change rate (product catalog changes slower than order status)
  - Legal/compliance boundary

Context identification method:
  1. Group related concepts from the glossary
  2. Find where the same word changes meaning → draw a boundary
  3. Name each context using domain language (not technical names)

Examples:
  Identity & Access Context:   User, Credential, Session, Permission, Role
  Order Management Context:    Order, OrderItem, OrderStatus, ShippingAddress
  Product Catalog Context:     Product, Category, Attribute, Price, Stock
  Payment Context:             Payment, Invoice, Refund, PaymentMethod
  Notification Context:        Notification, NotificationChannel, Template

Each context gets its own ubiquitous language — models are isolated.
```

---

## Step 3 — Classify Domain Objects

```
Within each bounded context, classify concepts:

ENTITY: Has a unique identity that persists over time.
  - Identity: identified by ID, not by attributes
  - Mutable: attributes may change, identity does not
  - Lifecycle: has a state machine (created, active, cancelled, etc.)
  Examples: Order, Customer, Invoice, Product

VALUE OBJECT: Defined by its attributes, no persistent identity.
  - No identity: two VOs with same attributes are equal
  - Immutable: replace, never modify
  - Descriptive: describes an attribute of an entity
  Examples: Address, Money, DateRange, EmailAddress, PhoneNumber, Color

AGGREGATE: Cluster of entities and VOs treated as one unit.
  - One AGGREGATE ROOT: the entity that guards all others
  - Access rule: only the root can be referenced externally
  - Transactional boundary: changes are atomic within one aggregate
  - Keep small: an aggregate that's too large causes contention
  Examples:
    Order aggregate root: Order (root), OrderItems[], ShippingAddress (VO)
    Product aggregate root: Product (root), Variants[], Price (VO)

DOMAIN SERVICE: Business logic that doesn't belong to one entity.
  - Stateless
  - Named after an action ("PricingCalculator", "TaxService")
  - Only when logic operates on multiple aggregates

DOMAIN EVENT: Something significant that happened in the domain.
  - Past tense: "OrderPlaced", "PaymentFailed", "InventoryDepleted"
  - Immutable fact: events don't change after they happen
  - Used for: decoupling contexts, audit trail, event sourcing
```

---

## Step 4 — Design Aggregates

```
For each aggregate:

1. Identify the root: "Who owns this cluster of objects?"
2. Define the boundary: "What objects MUST change together?"
3. Check invariants: "What business rules must always hold?"
4. Minimize the aggregate: "Can this be split?"

Aggregate design rules:
  □ Reference other aggregates by ID only (no object reference across boundaries)
  □ One transaction = one aggregate (if multiple aggregates, use domain events)
  □ Load whole aggregate or don't load it
  □ Keep aggregates small — large aggregates are a smell

Invariant identification:
  An invariant is a business rule that must always be true.
  Example: "An Order must always have at least one OrderItem"
            "Order total must equal sum of OrderItem prices"
  The aggregate root enforces ALL invariants within its boundary.

Document each aggregate:
  Aggregate: [Name]
  Root: [Entity name]
  Members: [List of entities and VOs]
  Invariants: [Business rules that must always hold]
  Lifecycle States: [State machine: Created → Confirmed → Shipped → Delivered → Cancelled]
  Domain Events: [Events emitted on state transitions]
```

---

## Step 5 — Context Map

```
Context map = the relationships between bounded contexts.

Relationship patterns (DDD):
  Partnership:
    Two contexts cooperate equally — changes to one require the other to change.
    Use when: both teams can coordinate easily.

  Shared Kernel:
    Two contexts share a small model (common entities/VOs).
    Use when: sharing is genuinely valuable and teams coordinate well.
    Caution: creates coupling — avoid where possible.

  Customer/Supplier (Upstream/Downstream):
    Supplier (upstream) provides an API. Customer (downstream) conforms to it.
    Upstream doesn't know about downstream.
    Use when: one context serves another; clear ownership.

  Conformist:
    Downstream conforms completely to upstream's model (no translation).
    Use when: upstream cannot be influenced; not worth translating.

  Anti-Corruption Layer (ACL):
    Downstream translates upstream's model into its own language.
    Use when: upstream model is messy or conflicting with your domain.
    Cost: translation code to maintain.

  Open Host Service (OHS):
    Context provides a well-defined API for many consumers.
    Use when: many contexts depend on this one.

  Published Language (PL):
    Formal, shared language (schema, API spec) for communication.
    Often combined with OHS.

  Separate Ways:
    Contexts have no integration — solve independently.
    Use when: integration is more expensive than duplication.

Draw the context map showing:
  - All bounded contexts as boxes
  - All integration relationships as labeled arrows with pattern name
  - U (upstream) / D (downstream) labels on Customer/Supplier relationships

Fill: templates/architecture/CONTEXT_MAP_TEMPLATE.md
```

---

## Step 6 — Domain Event Catalog

```
For each significant state transition in each aggregate, define a domain event:

Domain Event Format:
  Name:     [PastTenseVerb][Noun] (e.g., "OrderPlaced", "PaymentFailed")
  Context:  [which bounded context emits this]
  Trigger:  [what causes this event]
  Payload:  [what data is carried — domain language, no tech types]
  Consumers:[which other contexts care about this event]
  Invariant:[any business rule that must hold when this event fires]

Event catalog use:
  - Integration events: events crossing context boundaries
  - Internal events: events within one context (optional)
  - Events drive the context map (who listens to whom)

Event Storming (optional):
  If modeling a complex domain, use Event Storming notation:
  Orange  = Domain Event
  Blue    = Command (what causes the event)
  Yellow  = Actor (who issues the command)
  Green   = External System
  Purple  = Policy/Process (automated command in response to event)
  Red     = Problem/Hot Spot
```

---

## Output Format

Produce `docs/domain/DOMAIN_MODEL.md` from `templates/architecture/DOMAIN_MODEL_TEMPLATE.md`:

```markdown
# Domain Model — [System Name]

## Ubiquitous Language Glossary
| Term | Definition | Context |

## Bounded Contexts
[List with description of each]

## Context Map
[Mermaid diagram showing relationships]
[Relationship explanations]

## Aggregate Definitions
For each aggregate:
  ### [Aggregate Name]
  Root | Members | Invariants | Lifecycle | Events

## Domain Event Catalog
| Event Name | Context | Trigger | Payload | Consumers |

## Domain Diagram (Mermaid)
[Class-style diagram showing entities, VOs, and relationships]
```

---

## Constraints

- Domain model must use business language only — no technical terms
- Every bounded context boundary must be justified (ambiguous term OR team/lifecycle boundary)
- Aggregates must be minimal — if an aggregate is complex, split it
- Context map relationships must be explicit — no implicit coupling between contexts
- Domain events must have clear, specific payload — "all order data" is not acceptable
- Model is validated against requirements: every use case must be traceable to domain objects
