---
name: software-design
description: Software design principles, patterns, and architecture from SOLID through distributed systems. Covers the five SOLID principles with violations and fixes, DRY/KISS/YAGNI heuristics, separation of concerns, 12 GoF design patterns organized by intent (creational, structural, behavioral), architectural patterns (MVC, MVP, MVVM, layered, hexagonal, microservices, event-driven), coupling and cohesion metrics, dependency injection, and the design decision framework for choosing between competing approaches. Use when making design decisions, reviewing architecture, refactoring code, or teaching software engineering principles.
type: skill
category: coding
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/coding/software-design/SKILL.md
superseded_by: null
---
# Software Design

Software design is the discipline of organizing code so that it is correct, understandable, and changeable. A well-designed system makes the right things easy and the wrong things hard. This skill catalogs the principles, patterns, and architectural styles that professional software engineers use to achieve this, with emphasis on when each applies and when it does not.

**Agent affinity:** dijkstra (structured programming, formal reasoning about design), kay (OOP, message-passing architecture)

**Concept IDs:** code-code-organization, code-abstraction, code-decomposition, code-peer-review

## Part 1 -- Design Principles

### The SOLID Principles

Robert C. Martin codified these five principles for object-oriented design. They apply more broadly to any modular system.

#### S -- Single Responsibility Principle (SRP)

**Statement:** A module should have one, and only one, reason to change.

**What it means.** Each class, function, or module should serve exactly one purpose. If you change the database schema, only the database layer should change. If you change the UI layout, only the UI layer should change.

**Violation signal.** A class that has methods for both parsing user input AND writing to the database. A function that both validates data AND sends an email.

**Fix.** Separate the responsibilities into distinct modules. A UserValidator validates; a UserRepository persists; an EmailService sends.

#### O -- Open/Closed Principle (OCP)

**Statement:** Software entities should be open for extension but closed for modification.

**What it means.** You should be able to add new behavior without changing existing, tested code. This is achieved through abstraction -- interfaces, abstract classes, or polymorphism.

**Violation signal.** A function with a growing chain of if/else or switch statements that must be modified every time a new case is added.

**Fix.** Define an interface that each case implements. New cases add a new implementation without touching existing code. The Strategy pattern is the canonical implementation of OCP.

#### L -- Liskov Substitution Principle (LSP)

**Statement:** Objects of a supertype should be replaceable with objects of a subtype without breaking the program.

**What it means.** Subclasses must honor the contract of their parent. If a function works with a Shape, it must work with Circle, Rectangle, and Triangle without knowing which one it has.

**The classic violation.** Square extends Rectangle. A function sets width to 5 and height to 10, then asserts area == 50. The Square overrides setWidth to also set height, so area == 100. The substitution broke the contract.

**Fix.** Do not make Square a subclass of Rectangle. Model them as siblings implementing a common Shape interface, or use composition instead of inheritance.

#### I -- Interface Segregation Principle (ISP)

**Statement:** No client should be forced to depend on methods it does not use.

**What it means.** Large interfaces should be split into smaller, more specific ones. A Printer interface with print(), scan(), fax(), and staple() forces a simple printer to implement fax() and staple() with stubs or exceptions.

**Fix.** Split into Printable, Scannable, Faxable. Clients depend only on the interfaces they use. Composition of small interfaces is more flexible than one large interface.

#### D -- Dependency Inversion Principle (DIP)

**Statement:** High-level modules should not depend on low-level modules. Both should depend on abstractions.

**What it means.** The business logic should not import the database driver directly. Instead, both the business logic and the database implementation depend on a Repository interface. This makes the database swappable without changing the business logic.

**Implementation.** Dependency injection: pass dependencies as constructor parameters or function arguments rather than creating them internally. This also enables testing -- inject a mock repository in tests, a real one in production.

### Complementary Heuristics

**DRY (Don't Repeat Yourself).** Every piece of knowledge should have a single, unambiguous, authoritative representation. Duplication is a maintenance liability. But premature de-duplication (abstracting too early) can be worse than duplication -- wait until you see the pattern three times (the Rule of Three).

**KISS (Keep It Simple, Stupid).** The simplest solution that works is the best solution. Complexity is a cost, not a feature. Every abstraction layer, design pattern, and framework adds complexity that must be justified by the problems it solves.

**YAGNI (You Aren't Gonna Need It).** Do not build features, abstractions, or flexibility for hypothetical future requirements. Build what you need now. When the future requirement arrives, you will understand it better and build a more appropriate solution.

**Separation of Concerns.** Each module addresses a separate concern. The UI does not contain business logic. The business logic does not contain database queries. The database layer does not format HTTP responses. This is the meta-principle behind SOLID, MVC, and layered architecture.

### Coupling and Cohesion

**Coupling** measures how much modules depend on each other. Low coupling means modules can be changed independently. High coupling means a change in one module cascades through many others.

**Cohesion** measures how closely related the elements within a module are. High cohesion means a module does one thing well. Low cohesion means a module is a grab-bag of unrelated functionality.

**The goal:** high cohesion within modules, low coupling between modules. This is the quantitative formulation of good design.

## Part 2 -- Design Patterns

Design patterns are reusable solutions to common design problems. They are not code templates -- they are conceptual tools for structuring interactions between objects and modules. The Gang of Four (GoF) cataloged 23 patterns in 1994; the 12 most practically important are covered here.

### Creational Patterns

#### Factory Method

**Problem:** Client code needs to create objects but should not know the concrete class.

**Solution:** Define a method that returns an instance of an interface. Subclasses or configuration determine the concrete class.

**When to use.** When the creation logic is complex, when the concrete class depends on runtime conditions, or when you want to decouple client code from implementation classes.

#### Builder

**Problem:** Constructing complex objects with many optional parameters leads to telescoping constructors or error-prone parameter ordering.

**Solution:** Separate the construction of a complex object from its representation. The builder accumulates configuration and produces the final object in a build() call.

**When to use.** Objects with more than 3-4 optional parameters. Immutable objects that require all fields at construction time. Configuration objects.

#### Singleton

**Problem:** Ensure a class has exactly one instance and provide a global access point.

**Solution:** Private constructor, static instance method.

**When to use.** Almost never. Singleton is the most overused pattern. It creates hidden global state, makes testing difficult, and couples all consumers to the singleton. Prefer dependency injection. Use singleton only for truly global, stateless services (logging, metrics) and even then consider alternatives.

### Structural Patterns

#### Adapter

**Problem:** Two interfaces are incompatible but need to work together.

**Solution:** Create a wrapper that translates calls from one interface to the other.

**When to use.** Integrating third-party libraries, wrapping legacy APIs, bridging between different data formats.

#### Decorator

**Problem:** Add behavior to an object dynamically without modifying its class.

**Solution:** Wrap the object in a decorator that implements the same interface and adds behavior before or after delegating to the wrapped object.

**When to use.** Middleware chains (logging, authentication, caching), stream transformations, adding features to sealed classes.

#### Facade

**Problem:** A complex subsystem has many interacting classes that clients should not need to understand.

**Solution:** Provide a simplified interface that hides the complexity behind a single entry point.

**When to use.** Wrapping complex libraries, providing a simplified API for common use cases, reducing the learning curve for new developers.

### Behavioral Patterns

#### Strategy

**Problem:** An algorithm needs to be selected at runtime from a family of alternatives.

**Solution:** Define an interface for the algorithm. Each variant implements the interface. The context holds a reference to the current strategy and delegates to it.

**When to use.** Sorting strategies, payment processing methods, validation rules, rendering backends. This is the canonical implementation of the Open/Closed Principle.

#### Observer

**Problem:** One object changes state and multiple other objects need to be notified without tight coupling.

**Solution:** Define a subscription mechanism. Observers register interest in a subject. When the subject's state changes, it notifies all registered observers.

**When to use.** Event systems, UI data binding, pub/sub messaging, reactive programming.

#### Iterator

**Problem:** Traverse a collection without exposing its internal structure.

**Solution:** Define a standard interface (hasNext/next or the language's iterator protocol) that produces elements one at a time.

**When to use.** Any collection traversal. Most modern languages have built-in iterator support (Python's for/in, JavaScript's Symbol.iterator, Rust's Iterator trait).

#### Command

**Problem:** Encapsulate a request as an object so it can be parameterized, queued, logged, or undone.

**Solution:** Create a command object with an execute() method (and optionally undo()). The invoker holds commands and executes them without knowing what they do.

**When to use.** Undo/redo systems, task queues, macro recording, transaction logs.

#### State

**Problem:** An object's behavior changes based on its internal state, leading to complex conditionals.

**Solution:** Encapsulate each state as a separate class implementing a common interface. The context delegates to the current state object.

**When to use.** State machines (UI components, protocol handlers, game entities), workflow engines.

#### Template Method

**Problem:** Multiple algorithms share a common structure but differ in specific steps.

**Solution:** Define the skeleton in a base class method, with abstract methods for the varying steps. Subclasses implement the abstract methods.

**When to use.** Framework hooks (test setup/teardown, request processing pipelines), algorithms with fixed structure and variable details.

## Part 3 -- Architectural Patterns

### MVC (Model-View-Controller)

**Model:** Data and business logic. Notifies observers when state changes.
**View:** UI presentation. Reads from the model, renders output.
**Controller:** Handles user input, updates the model.

**When to use.** Web applications (Rails, Django, Spring MVC), desktop applications. The most widely known architectural pattern.

**Variants.** MVP (Model-View-Presenter) -- the presenter mediates all communication between view and model, making the view passive and testable. MVVM (Model-View-ViewModel) -- the view model exposes observable properties that the view binds to declaratively (WPF, SwiftUI, Vue.js).

### Layered Architecture

**Layers (top to bottom):** Presentation -> Business Logic -> Data Access -> Database.

Each layer depends only on the layer directly below it. This enforces separation of concerns and makes layers independently replaceable. The strict boundary rule in this project (src/ never imports desktop/) is a layered architecture constraint.

### Hexagonal Architecture (Ports and Adapters)

**Core:** Business logic with no external dependencies.
**Ports:** Interfaces that the core defines for its needs (input ports for use cases, output ports for persistence).
**Adapters:** Implementations of ports for specific technologies (REST adapter, PostgreSQL adapter, CLI adapter).

**Why it matters.** The business logic is testable in isolation. Technology decisions (which database, which framework) are pushed to the edges and can be changed without touching the core.

### Microservices

**Principle:** Decompose a system into small, independently deployable services, each owning its data and communicating via well-defined APIs.

**When to use.** Large teams where independent deployment matters, systems with genuinely different scaling requirements per component, polyglot environments.

**When NOT to use.** Small teams, early-stage products, systems where the domain boundaries are unclear. The distributed systems overhead (network latency, partial failure, eventual consistency, observability) is substantial. Start with a modular monolith.

### Event-Driven Architecture

**Principle:** Components communicate by producing and consuming events rather than making direct calls. Decouples producers from consumers.

**When to use.** Systems with many independent reactions to the same event, audit/logging requirements, eventual consistency is acceptable.

**Key patterns.** Event sourcing (store events, not state), CQRS (separate read and write models), saga pattern (coordinate distributed transactions via events).

## Design Decision Framework

When choosing between competing approaches, evaluate along these dimensions:

| Dimension | Question |
|---|---|
| Simplicity | Which approach has fewer moving parts? |
| Testability | Which is easier to test in isolation? |
| Changeability | Which requires fewer changes when requirements evolve? |
| Understandability | Which can a new developer understand fastest? |
| Performance | Does it matter? Measure, don't guess. |
| Team capability | Does the team have experience with this approach? |

**The first dimension wins ties.** When two approaches are equally good on other dimensions, choose the simpler one. Complexity is a liability that compounds over time.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Premature abstraction | Abstracts before the pattern is clear | Wait for three instances (Rule of Three) |
| Pattern worship | Forces patterns where they add complexity without value | Patterns are tools, not goals |
| God class | One class does everything | Split along responsibility boundaries (SRP) |
| Leaky abstraction | Implementation details leak through the interface | Review interface contracts, hide internals |
| Inheritance for code reuse | Tight coupling, fragile base class problem | Prefer composition over inheritance |
| Distributed monolith | Microservices that must be deployed together | Either make them independent or merge them |
| Premature microservices | Distributed complexity without the benefits | Start with a modular monolith |

## Cross-References

- **dijkstra agent:** Structured programming, formal reasoning about program correctness, "Go To considered harmful."
- **kay agent:** Object-oriented design, message passing, late binding, Smalltalk philosophy.
- **knuth agent:** Algorithm-level design decisions, literate programming as a design discipline.
- **lovelace agent:** Architectural vision, seeing computation as more than calculation.
- **programming-fundamentals skill:** The building blocks that design principles organize.
- **debugging-testing skill:** Testing strategies that validate design decisions.

## References

- Martin, R. C. (2017). *Clean Architecture*. Prentice Hall.
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
- Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley.
- Dijkstra, E. W. (1968). "Go To Statement Considered Harmful." *Communications of the ACM*, 11(3), 147-148.
- Kay, A. (1993). "The Early History of Smalltalk." *ACM SIGPLAN Notices*, 28(3), 69-95.
- Cockburn, A. (2005). "Hexagonal Architecture." alistair.cockburn.us.
- Newman, S. (2021). *Building Microservices*. 2nd edition. O'Reilly.
