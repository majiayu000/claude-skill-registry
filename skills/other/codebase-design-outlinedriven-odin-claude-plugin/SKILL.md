---
name: codebase-design
description: 'Shared vocabulary for designing deep modules: module, interface, implementation, depth, seam, adapter, leverage, locality. Use when designing or improving a module interface, deciding where a seam goes, making code more testable, or when another skill needs the deep-module terms.'
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Use this language and these principles wherever code is being designed or restructured. The aim is leverage for callers, locality for maintainers, and testability for everyone.

Shared vocabulary for every suggestion this skill makes. Use these terms exactly — do not substitute "component," "service," "API," or "boundary." Consistent language is the whole point.

## Terms

**Module**
Anything with an interface and an implementation. Deliberately scale-agnostic — applies equally to a function, class, package, crate, module, or tier-spanning slice.
_Avoid_: unit, component, service.

**Interface**
Everything a caller must know to use the module correctly. Includes the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics.
_Avoid_: API, signature (too narrow — those refer only to the type-level surface).

**Implementation**
What sits inside a module — its body of code. Distinct from **Adapter**: a single thing can be a small adapter with a large implementation (e.g. a Postgres repository in Rust or a JPA repository in Java) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth**
Leverage at the interface — the amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface. A module is **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(from Michael Feathers)_
A place where behaviour can be altered without editing in that place. The *location* at which a module's interface lives. Choosing where to put the seam is its own design decision, separate from its implementation.
_Avoid_: boundary (overloaded with DDD's bounded context).

**Adapter**
A concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what is inside).

**Leverage**
What callers get from depth. More capability per unit of interface they have to learn. One implementation pays back across N call sites and M tests.

**Locality**
What maintainers get from depth. Change, bugs, knowledge, and verification concentrate at one place rather than spreading across callers. Fix once, fixed everywhere.

## Deep vs shallow

**Deep module** = a small interface with lots of implementation behind it.

**Shallow module** = a large interface with little implementation. Avoid.

The deep form hides complex behaviour behind a narrow surface. The shallow form exposes nearly as much interface as implementation, so callers carry the complexity. Prefer depth when it gives callers more leverage and maintainers more locality.

When designing an interface, ask:

- Can the number of methods be reduced?
- Can the parameters be simplified?
- Can more complexity be hidden inside?

Depth matters more than line count: a single method that handles a hard problem well is deeper than ten methods that each forward to another layer.

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts — they just are not part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, the module was not hiding anything (it was a pass-through). If complexity reappears across N callers, the module was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If a contributor wants to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Do not introduce a seam unless something actually varies across it.

## Designing for testability

Good interfaces make testing natural:

1. **Accept dependencies instead of constructing them.**

   **Python**

   ```python
   # Testable — gateway is injected
   def process_order(order: Order, gateway: PaymentGateway) -> Receipt: ...

   # Hard to test — gateway is constructed internally
   def process_order(order: Order) -> Receipt:
       gateway = StripeGateway()
       ...
   ```

   **Rust**

   ```rust
   // Testable
   fn process_order(order: &Order, gateway: &dyn PaymentGateway) -> Receipt { ... }

   // Hard to test
   fn process_order(order: &Order) -> Receipt {
       let gateway = StripeGateway::new();
       ...
   }
   ```

2. **Return results instead of mutating.**

   **Python**

   ```python
   # Testable — pure return value
   def calculate_discount(cart: Cart) -> Discount: ...

   # Hard to test — hidden side effect
   def apply_discount(cart: Cart) -> None:
       cart.total -= discount
   ```

   **Rust**

   ```rust
   // Testable
   fn calculate_discount(cart: &Cart) -> Discount { ... }

   // Hard to test
   fn apply_discount(cart: &mut Cart) {
       cart.total -= discount;
   }
   ```

3. **Keep the surface small.** Fewer methods → fewer tests needed. Fewer parameters → simpler test setup. A narrow surface is easier to keep stable across refactors.

## Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Cross-language anchors

- **Rust** — `Module` typically maps to a crate or module path; `Interface` includes trait bounds, lifetime constraints, error enums, and `#[must_use]` annotations; `Seam` is most often a trait object boundary or a generic parameter; `Adapter` is the concrete `impl Trait for Type`.
- **Go** — `Module` maps to a package; `Interface` includes the named `interface` type, the package-level error sentinels, and any context-cancellation contract; `Seam` is the interface declaration site; `Adapter` is the concrete struct with method receivers.
- **OCaml** — `Module` maps to a `.ml`/`.mli` pair; `Interface` is the `.mli` plus invariants encoded by the abstract type `t`; `Seam` is the signature `S` consumed by a functor; `Adapter` is the argument module passed to that functor.
- **Java / Kotlin** — `Module` maps to a package or Gradle module; `Interface` is the language `interface`/`sealed interface` plus checked exceptions and JavaDoc invariants; `Seam` is the interface; `Adapter` is the concrete implementation injected via the DI container.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. Use depth-as-leverage instead.
- **"Interface" as the language-level keyword (TypeScript `interface`, Java `interface`, Go `interface{}`) or a class's public methods**: too narrow — interface here includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.
