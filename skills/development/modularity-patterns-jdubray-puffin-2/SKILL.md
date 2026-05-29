---
name: modularity-patterns
description: Recommends modularity, composition, and decoupling patterns for design challenges. Use when designing plugin architectures, reducing coupling, improving testability, or separating cross-cutting concerns.
---

# Modularity Patterns

Apply these patterns when designing or refactoring code for modularity, extensibility, and decoupling.

## Trigger Conditions

Apply this skill when:
- Designing plugin or extension architectures
- Reducing coupling between components
- Improving testability through dependency management
- Creating flexible, configurable systems
- Separating cross-cutting concerns

---

## Select the Right Pattern

| Problem | Apply These Patterns |
|---------|---------------------|
| Hard-coded dependencies | DI, IoC, Service Locator, SAM |
| Need runtime extensions | Plugin, Microkernel, Extension Points |
| Swappable algorithms | Strategy, Abstract Factory |
| Additive behavior | Decorator, Chain of Responsibility, SAM |
| Feature coupling | Package by Feature |
| Scattered concerns | AOP, Interceptors, Mixins, SAM |
| Temporal coupling | Observer, Event Bus, Event Sourcing, SAM |
| Read/write optimization | CQRS |
| Deployment flexibility | Feature Toggles, Microservices |

---

## Implementation Checklist

When applying any modularity pattern:

1. **Define clear interfaces** - Contracts before implementations
2. **Minimize surface area** - Expose only what's necessary
3. **Depend on abstractions** - Not concrete implementations
4. **Favor composition** - Over inheritance
5. **Isolate side effects** - Push to boundaries
6. **Make dependencies explicit** - Visible in signatures
7. **Design for substitution** - Any implementation satisfying contract works
8. **Consider lifecycle** - Creation, configuration, destruction
9. **Plan for versioning** - APIs evolve, maintain compatibility
10. **Test boundaries** - Verify contracts, mock implementations

---

## Pattern Reference

### Inversion Patterns

**Dependency Injection (DI)** - Provide dependencies externally rather than creating internally.
- Constructor injection (preferred, immutable)
- Setter injection (optional dependencies)
- Interface injection (framework-driven)

**Inversion of Control (IoC)** - Let framework control flow, calling your code. Use IoC containers (Spring, Guice, .NET DI) to manage object lifecycles and wiring.

**Service Locator** - Query central registry for dependencies at runtime. Achieves decoupling but hides dependencies. Prefer DI for explicitness.

---

### Plugin & Extension Architectures

**Plugin Pattern** - Load and integrate external code at runtime via defined contracts.
- Discovery: directory scanning, manifests, registries
- Lifecycle: load, initialize, unload
- Isolation: classloaders, processes, sandboxes
- Versioning: API compatibility

**Microkernel Architecture** - Build minimal core with all domain functionality in plugins. Examples: VS Code, Eclipse IDE.

**Extension Points & Registry** - Define multiple specific extension points rather than single plugin interface. Extensions declare which points they extend.

---

### Structural Composition

**Strategy Pattern** - Encapsulate interchangeable algorithms behind common interface.
```
Context → Strategy Interface → Concrete Strategies
```
Use for runtime behavioral swapping (sorting, validation, pricing).

**Decorator Pattern** - Wrap objects to add behavior without modification.
```
Component → Decorator → Decorator → Concrete Component
```
Use for composable behavior chains (logging, caching, validation).

**Composite Pattern** - Treat individuals and compositions uniformly via shared interface. Use for tree structures, UI hierarchies, file systems.

**Chain of Responsibility** - Create pipeline of handlers where each processes or forwards. Use for middleware stacks, request processing pipelines.

**Bridge Pattern** - Separate abstraction from implementation hierarchies. Use to prevent subclass explosion with multiple varying dimensions.

---

### Module Boundaries

**Module Pattern** - Encapsulate private state, expose public interface. Modern implementations: ES Modules, CommonJS, Java 9 modules.

**Facade Pattern** - Provide simplified interface to complex subsystem. Use to establish clean module boundaries.

**Package Organization**
- By Layer: Group controllers, repositories, services separately
- By Feature: Group everything for "orders" together (preferred for modularity)

---

### Event-Driven Decoupling

**Observer Pattern** - Implement publish-subscribe where subjects notify observers without knowing them.

**Event Bus / Message Broker** - Enable system-wide pub-sub with fully decoupled publishers and subscribers. Add behaviors by adding subscribers without publisher changes.

**Event Sourcing** - Store state changes as event sequence, not snapshots. Enable new projections via event replay; new behaviors react to stream.

**CQRS** - Separate read and write models.
```
Commands → Write Model (validation, rules, persistence)
Queries → Read Model (optimized for reading)
```

---

### Cross-Cutting Concerns

**Aspect-Oriented Programming (AOP)** - Modularize scattered concerns (logging, security, transactions). Define pointcuts (where) and advice (what).

**Interceptors & Middleware** - Explicitly wrap method calls or request pipelines. Less magical than AOP, more traceable.

**Mixins & Traits** - Compose behaviors from multiple sources without deep inheritance. Examples: Scala traits, Rust traits, TypeScript intersections.

---

### Configuration Patterns

**Feature Toggles** - Decouple deployment from release by shipping new code behind flags. Enables trunk-based development, A/B testing, gradual rollouts.

**Strategy Configuration** - Externalize algorithmic choices to configuration files.

**Convention over Configuration** - Reduce wiring through established defaults and naming conventions.

---

### Component Models

**Component-Based Architecture** - Build self-contained components with defined interfaces managing own state. Examples: React, Vue, server-side component frameworks.

**Entity-Component-System (ECS)** - Separate identity (entities), data (components), behavior (systems). Use for game development, highly dynamic systems.

**Service-Oriented / Microservices** - Apply component thinking at system level with process isolation boundaries.

---

### Creational Patterns

**Registry Pattern** - Maintain collection of implementations keyed by type/name, queried at runtime.

**Abstract Factory** - Create families of related objects without specifying concrete classes.

**Prototype Pattern** - Create objects by cloning prototypes, avoiding direct class instantiation.

---

### SAM Pattern (State-Action-Model)

Functional decomposition for reactive systems:

- **State:** Pure representation of current state
- **Action:** Pure functions proposing state changes
- **Model:** State acceptor enforcing business rules

Loop: View renders State → Actions propose → Model accepts/rejects → State updates.

Provides natural boundaries between representation, proposals, and validation.
