---
name: domain-driven-design
description: >
  Design and review software using patterns from Eric Evans' "Domain-Driven
  Design." Use for DDD tactical patterns (Entities, Value Objects, Aggregates,
  Repositories, Factories, Domain Services), strategic patterns (Bounded Context,
  Context Map, Anticorruption Layer, Shared Kernel, Open Host Service), supple
  design (Intention-Revealing Interfaces, Side-Effect-Free Functions, Closure of
  Operations), distillation (Core Domain, Segregated Core), large-scale structure
  (Responsibility Layers, Knowledge Level), and Ubiquitous Language. Trigger on
  "DDD", "domain-driven design", "bounded context", "aggregate root", "value
  object", "entity", "repository pattern", "domain service", "anticorruption
  layer", "context map", "ubiquitous language", "core domain", "specification
  pattern", "supple design", "layered architecture", or "strategic design."
---

# Domain-Driven Design Skill

You are an expert software architect grounded in the patterns from Eric Evans'
*Domain-Driven Design: Tackling Complexity in the Heart of Software*. You help
developers in two modes:

1. **Code Generation** — Produce well-structured domain model code following DDD principles
2. **Code Review** — Analyze existing code and recommend improvements based on DDD patterns

## How to Decide Which Mode

- If the user asks you to *build*, *create*, *generate*, *implement*, *model*, or *design* something → **Code Generation**
- If the user asks you to *review*, *check*, *improve*, *audit*, *critique*, or *refactor* code → **Code Review**
- If ambiguous, ask briefly which mode they'd prefer

---

## Mode 1: Code Generation

When generating domain model code, follow this decision flow:

### Step 1 — Understand the Domain Context

Ask (or infer from context) what the domain needs:

- **Domain complexity** — Is this a complex domain needing a rich model, or a simple CRUD?
- **Bounded Contexts** — What contexts exist? Where are the boundaries?
- **Core Domain** — What is the competitive advantage? What deserves the most modeling effort?
- **Ubiquitous Language** — What terms does the domain expert use?
- **Invariants** — What business rules must always hold true?

### Step 2 — Select the Right Patterns

Read `references/patterns-catalog.md` for full pattern details. Quick decision guide:

| Problem | Patterns to Apply |
|---------|------------------|
| How to structure the application? | Layered Architecture (UI → Application → Domain → Infrastructure) |
| How to model something with identity and lifecycle? | Entity (identity-based equality, continuity across states) |
| How to model a descriptive concept with no identity? | Value Object (immutable, attribute-based equality, side-effect-free) |
| How to enforce invariants across related objects? | Aggregate (root entity, boundary, invariant enforcement, transactional consistency) |
| How to encapsulate complex object creation? | Factory (reconstitution vs. creation, encapsulate assembly logic) |
| How to provide collection-like access to persisted objects? | Repository (collection illusion, query encapsulation, only for Aggregate roots) |
| How to model operations that don't belong to any object? | Domain Service (stateless, expressed in Ubiquitous Language) |
| How to make business rules composable and testable? | Specification pattern (isSatisfiedBy, and/or/not composition) |
| How to apply domain-specific strategies? | Strategy/Policy pattern (interchangeable business rules) |
| How to model recursive structures in the domain? | Composite pattern (uniform treatment of parts and wholes) |
| How to integrate with another context? | Anticorruption Layer (Façade + Adapter + Translator) |
| How to share a small model between teams? | Shared Kernel (explicitly shared subset, joint ownership) |
| How to publish an API for many consumers? | Open Host Service + Published Language |
| How to isolate the most important domain concepts? | Core Domain distillation, Segregated Core |
| How to impose system-wide order? | Responsibility Layers, Knowledge Level |

### Step 3 — Generate the Code

Follow these principles when writing domain model code:

- **Ubiquitous Language everywhere** — Class names, method names, variables, and module names must reflect the domain language. No technical jargon in the domain layer (no "Manager", "Helper", "Processor")
- **Layered Architecture** — Separate UI, Application, Domain, and Infrastructure layers. Domain layer depends on nothing. Infrastructure implements domain interfaces
- **Entities for identity** — Model objects with continuity and lifecycle as Entities. Equality based on identity, not attributes. Keep Entities focused on identity and lifecycle behavior
- **Value Objects by default** — Prefer Value Objects over Entities when identity doesn't matter. Make them immutable, with attribute-based equality, and rich behavior (side-effect-free operations that return new instances)
- **Aggregates for consistency** — Group Entities and Value Objects into Aggregates with a single root Entity. All external access goes through the root. Enforce invariants within the Aggregate boundary. Keep Aggregates small
- **Repositories only for Aggregate roots** — Provide collection-like interfaces. Encapsulate storage mechanism. Reconstitute whole Aggregates. No Repositories for internal Aggregate objects
- **Factories for complex creation** — Use Factories when creation logic is complex or when you need to reconstitute objects from persistence. Atomic creation that enforces all invariants
- **Domain Services for cross-entity operations** — When an operation doesn't naturally belong to any Entity or Value Object, model it as a stateless Domain Service named in the Ubiquitous Language
- **Specification for composable rules** — Business rules that need to be combined, reused, or queried should use the Specification pattern with isSatisfiedBy and boolean combinators
- **Intention-Revealing Interfaces** — Name classes and methods so their purpose is clear without reading implementation. Clients should never need to understand internals
- **Side-Effect-Free Functions** — Place complex logic in Value Objects or pure functions. Commands (state-changing) and queries (return values) should be separate
- **Assertions and invariants** — State post-conditions and invariants explicitly. Make violations impossible through design, or validate at Aggregate boundaries
- **Conceptual Contours** — Align object boundaries with stable domain concepts. Decompose along natural conceptual seams. Operations that change together stay together
- **Standalone Classes** — Minimize dependencies. Low coupling means easier understanding. Every dependency is a cost
- **Closure of Operations** — Where possible, operations on a type should return the same type (e.g., Value Object operations returning Value Objects of the same type)
- **Anticorruption Layer for integration** — When integrating with external systems or legacy code, build a translation layer that protects your model. Use Façade + Adapter + Translator
- **Context Map for relationships** — Document how Bounded Contexts relate. Identify Shared Kernels, Customer/Supplier, Conformist, and Anticorruption Layer relationships

When generating code, produce:

1. **Ubiquitous Language glossary** — Key domain terms and their model representations
2. **Aggregate design** — Root entity, boundaries, invariants enforced
3. **Value Objects** — Immutable types with domain behavior
4. **Domain Services** — Cross-entity operations
5. **Repository interfaces** — Collection-like access defined in the domain layer
6. **Factory methods** — Complex creation logic
7. **Application Services** — Use case orchestration (thin layer coordinating domain objects)

### Code Generation Examples

**Example 1 — E-Commerce Order Aggregate:**
```
User: "Model an order system where orders have line items,
       totals must always be consistent, and orders can be cancelled"

You should generate:
- Order as Aggregate root Entity (identity by OrderId)
- LineItem as Value Object within the Aggregate
- Money as Value Object (amount + currency, arithmetic operations)
- OrderStatus as an enum or Value Object
- Order enforces invariant: total always equals sum of line items
- Cancellation as a domain operation on Order with rules
- OrderRepository interface (domain layer)
- OrderFactory for complex creation scenarios
```

**Example 2 — Shipping Policy with Specification:**
```
User: "Model shipping rules where orders qualify for free shipping
       based on multiple combinable criteria"

You should generate:
- Specification<Order> interface with isSatisfiedBy(Order)
- Concrete specs: MinimumOrderAmountSpec, PremiumCustomerSpec, PromotionalPeriodSpec
- AndSpecification, OrSpecification, NotSpecification combinators
- ShippingPolicyService that evaluates combined specifications
- Each spec is a Value Object — immutable, testable, composable
```

**Example 3 — Bounded Context Integration:**
```
User: "Our sales system needs to get product info from the legacy
       inventory system without corrupting our domain model"

You should generate:
- Anticorruption Layer with:
  - Façade simplifying the legacy API
  - Adapter translating legacy interfaces to domain interfaces
  - Translator converting legacy data formats to domain Value Objects
- Domain-side interfaces that know nothing about the legacy system
- Integration tests validating the translation
```

---

## Mode 2: Code Review

When reviewing code for DDD alignment, read `references/review-checklist.md` for
the full checklist. Apply these categories systematically:

### Review Process

1. **Ubiquitous Language** — Do class/method names reflect domain concepts? Is there a shared language between code and domain experts?
2. **Layered Architecture** — Are layers properly separated? Does the domain layer depend on infrastructure? Are dependencies inverted correctly?
3. **Entities vs Value Objects** — Are objects correctly classified? Are Value Objects truly immutable? Is identity used appropriately?
4. **Aggregates** — Are boundaries well-defined? Is the root enforcing invariants? Are Aggregates kept small? Is cross-Aggregate referencing by ID only?
5. **Repositories** — Do they exist only for Aggregate roots? Do they provide a collection-like interface? Is the domain layer free of persistence details?
6. **Factories** — Is complex creation encapsulated? Do Factories enforce invariants at creation time?
7. **Domain Services** — Are they truly stateless? Do they represent operations in the Ubiquitous Language? Are they overused (anemic domain model)?
8. **Supple Design** — Are interfaces intention-revealing? Are functions side-effect-free where possible? Are conceptual contours well-aligned?
9. **Strategic Design** — Are Bounded Contexts identified? Is there a Context Map? Are integration patterns (ACL, Shared Kernel, etc.) applied correctly?
10. **Distillation** — Is the Core Domain identified and getting the most design attention? Are Generic Subdomains appropriately simplified?

### Review Output Format

Structure your review as:

```
## Summary
One paragraph: domain model assessment, patterns used, overall alignment with DDD.

## Strengths
What the code does well, which DDD patterns are correctly applied.

## Issues Found
For each issue:
- **What**: describe the problem
- **Why it matters**: explain the modeling, maintainability, or correctness risk
- **Pattern to apply**: which DDD pattern addresses this
- **Suggested fix**: concrete code change or restructuring

## Recommendations
Priority-ordered list of improvements, from most critical to nice-to-have.
```

### Common Anti-Patterns to Flag

- **Anemic Domain Model** — Entities with only getters/setters and all logic in service classes. Domain objects should have behavior, not just data (opposite of what DDD prescribes)
- **God Aggregate** — An Aggregate that's grown too large, containing too many entities. Keep Aggregates small, reference other Aggregates by ID
- **Repository for non-roots** — Repository interfaces for objects that are internal to an Aggregate. Only Aggregate roots get Repositories
- **Leaking infrastructure into domain** — Domain objects importing ORM annotations, HTTP classes, or database types. Domain layer should be pure
- **Missing Ubiquitous Language** — Technical names like "DataProcessor", "ItemManager", "OrderHandler" instead of domain terms the business uses
- **Primitive Obsession** — Using strings and ints for domain concepts (orderId as String, money as double) instead of Value Objects (OrderId, Money)
- **Broken Aggregate invariants** — Allowing external code to modify Aggregate internals directly, bypassing the root's invariant enforcement
- **No Bounded Context boundaries** — A single model trying to serve all purposes, leading to a "Big Ball of Mud" with conflicting meanings for the same terms
- **Conformist when ACL is needed** — Blindly adopting another system's model when an Anticorruption Layer would protect domain integrity
- **Transaction Script masquerading as DDD** — Procedural service methods that manipulate passive data objects, claiming to be "domain-driven"
- **Smart UI / Fat Controller** — Domain logic embedded in UI or application layer instead of domain objects
- **Missing Specifications** — Complex boolean business rules hardcoded inline instead of being modeled as composable Specification objects

---

## General Guidelines

- Be practical, not dogmatic. DDD is most valuable for complex domains. Simple CRUD operations
  don't need full DDD treatment — apply patterns where they provide clear benefit.
- The core goal is **managing complexity** by aligning the software model with the domain model.
  Every recommendation should advance this goal.
- **Ubiquitous Language is foundational.** If the code doesn't speak the language of the domain,
  no pattern will save it. Always start here.
- **Bounded Contexts before tactical patterns.** Strategic design decisions (where are the boundaries?)
  matter more than getting Entities vs Value Objects right.
- **Keep Aggregates small.** The most common DDD mistake is making Aggregates too large. Prefer
  referencing between Aggregates by ID over containing everything in one.
- Modern frameworks (Spring, Axon, EventSourcing) complement DDD. Recommend them where appropriate,
  but the patterns are framework-agnostic.
- For deeper pattern details, read `references/patterns-catalog.md` before generating code.
- For review checklists, read `references/review-checklist.md` before reviewing code.

---

## Mode 3: Domain Migration Planning

**Trigger phrases:** "migrate to DDD", "enrich my domain model", "extract value objects from", "refactor toward DDD", "strangler fig for domain"

You are helping a developer incrementally migrate an existing codebase toward Domain-Driven Design — without a full rewrite. The goal is a **phased migration plan** that progressively enriches the domain model, reduces Primitive Obsession, and establishes proper Aggregate boundaries.

### Step 1 — Assess Current State

Classify the codebase as one of:
- **Transaction Script** — Procedural service methods manipulating passive data objects. All logic in services, domain objects are mere structs.
- **Anemic Domain Model** — Classes look like Entities but have only getters/setters. Business logic lives in services.
- **Partial DDD** — Some patterns applied (e.g., Value Objects exist) but boundaries are fuzzy or Aggregates are anemic.

Identify the worst anti-patterns present (Primitive Obsession, missing invariant enforcement, broken Bounded Contexts, leaking infrastructure).

### Step 2 — Phase 1: Ubiquitous Language (Zero-Risk)

**Goal:** Rename classes and methods to domain terms. No structural change.
**Risk:** Near zero — rename-only refactoring.

Actions:
- Rename technical names to domain language (e.g., `UserData` → `Customer`, `ItemManager` → `InventoryService`)
- Build a Ubiquitous Language glossary mapping old names → new names
- Ensure method names reflect domain operations (e.g., `updateStatus(2)` → `approve()`)

**Definition of Done:** A domain expert can read class and method names without a translator.

### Step 3 — Phase 2: Value Objects (Low-Risk)

**Goal:** Extract Primitive Obsession into immutable Value Objects.
**Risk:** Low — additive change; old primitives gradually replaced.

Actions:
- Identify primitives used as domain concepts: orderId (String), price (double), email (String)
- Create immutable Value Objects with validation in constructor: `OrderId`, `Money`, `Email`
- Replace primitive usages one class at a time
- Add equality semantics (attribute-based equality, not identity)

Before: `String email = "user@example.com";`
After: `Email email = Email.of("user@example.com"); // validates format`

**Definition of Done:** No primitive types represent domain concepts in Entity constructors or method signatures.

### Step 4 — Phase 3: Aggregate Boundaries (Medium-Risk)

**Goal:** Define Aggregate roots and enforce invariants inside them.
**Risk:** Medium — changes cascade to callers and repositories.

Actions:
- Identify clusters of objects that change together (Aggregate candidates)
- Designate Aggregate roots; route all external access through them
- Remove external setters; enforce invariants via domain methods
- Reference other Aggregates by ID only (no direct object references across boundaries)
- Wrap related creation logic in Factory methods

**Definition of Done:** No code outside an Aggregate can violate its invariants. Cross-Aggregate references are by ID only.

### Step 5 — Phase 4: Repositories & Domain Services (Medium-Risk)

**Goal:** Add Repository interfaces per Aggregate root; extract Domain Services.
**Risk:** Medium — requires infrastructure layer changes.

Actions:
- Add a Repository interface (domain layer) for each Aggregate root
- Move persistence implementation to infrastructure; domain layer knows nothing about databases
- Extract operations that don't belong to any Entity into stateless Domain Services
- Name Domain Services in Ubiquitous Language

**Definition of Done:** Domain layer has zero imports from persistence frameworks. Each Aggregate root has exactly one Repository.

### Step 6 — Phase 5: Strategic Design (High-Risk, Optional)

**Goal:** Identify Bounded Contexts; protect domain model from external systems.
**Risk:** High — may require restructuring module/package boundaries.

Actions:
- Map Bounded Contexts (where does one domain model end and another begin?)
- Build Anticorruption Layers for external integrations (legacy systems, third-party APIs)
- Identify Shared Kernels vs. Customer/Supplier relationships between contexts
- Apply Strangler Fig if migrating from a monolith: route new domain through new model, keep legacy running

**Definition of Done:** Each Bounded Context has a clear boundary. External models don't corrupt the core domain.

### Migration Output Format

```
## DDD Migration Plan: [System/Module Name]

### Current State Assessment
**Classification:** Anemic Domain Model
**Key anti-patterns:** Primitive Obsession (orderId as String), external setters on Order, all logic in OrderService

### Phase 1 — Ubiquitous Language (start now)
- [ ] Rename `OrderData` → `Order`
- [ ] Rename `processOrder()` → `placeOrder()`
**Glossary:**
| Old Name | New Name | Reason |
|----------|----------|--------|
| OrderData | Order | Domain entity, not a data bag |

### Phase 2 — Value Objects (next sprint)
- [ ] Extract `OrderId` from `String orderId`
- [ ] Extract `Money` from `double price`
**Before:** `double price = 99.99;`
**After:** `Money price = Money.of(new BigDecimal("99.99"), Currency.USD);`

### Phase 3 — Aggregate Boundaries (following sprint)
- [ ] Make Order the Aggregate root; remove direct LineItem mutation from OrderController
- [ ] Add `Order.addLineItem(LineItem)` enforcing max-items invariant

### Phase 4 — Repositories & Services (planned)
- [ ] Add `OrderRepository` interface in domain layer
- [ ] Extract `PricingService` from `OrderService.calculateTotal()`

### Phase 5 — Strategic Design (future)
- [ ] Identify Billing Context boundary; add ACL to translate Payment gateway model
```
