---
name: php-patterns
description: Apply PHP design patterns — Repository, Factory, Strategy, Decorator, Observer, Singleton, Builder, and Dependency Injection patterns in PHP. Use when architecting PHP applications or understanding patterns used in Magento and other frameworks.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# PHP Design Patterns

## Before writing code

**Fetch live docs**: Web-search `php design patterns examples` for current community patterns and best practices. For Magento-specific patterns, web-search `site:developer.adobe.com commerce php development components`.

## Creational Patterns

### Factory

Creates objects without exposing instantiation logic. In Magento, auto-generated Factory classes (`SomeModelFactory`) create non-injectable objects via `$factory->create()`.

**When to use**: When you need new instances (entities, models) rather than shared singletons. When the caller shouldn't know the concrete class.

### Builder

Constructs complex objects step by step. Magento's `SearchCriteriaBuilder`, `FilterBuilder`, `SortOrderBuilder` follow this pattern.

**When to use**: When object construction requires many optional parameters or multi-step assembly.

### Singleton (Shared Instance)

Single instance shared across the application. Magento's Object Manager shares instances by default. Explicit singleton is generally an anti-pattern — prefer DI container sharing.

**When to use**: Rarely — let the DI container manage instance sharing.

## Structural Patterns

### Proxy

Delays instantiation of resource-intensive dependencies. Magento auto-generates Proxy classes (`SomeClass\Proxy`) that create the real object only when a method is called.

**When to use**: When a class injects a heavy dependency it doesn't always use.

### Decorator

Wraps an object to add behavior without modifying the original. Used in Magento composite components and cache decorators.

**When to use**: When you need to add behavior to an object dynamically without subclassing.

### Composite

Treats individual objects and compositions uniformly. Magento's UI component tree and layout container system follow this pattern.

**When to use**: When you have tree-structured data or components.

## Behavioral Patterns

### Strategy

Defines a family of algorithms, encapsulates each one, makes them interchangeable. Magento shipping carriers and payment methods are strategy implementations.

**When to use**: When you have multiple algorithms for the same task and want runtime selection.

### Observer

Defines a one-to-many dependency. When one object changes state, all dependents are notified. Magento's event/observer system is a direct implementation.

**When to use**: When changes in one object should trigger actions in others without tight coupling.

### Repository

Mediates between domain and data mapping layers. Magento's repository interfaces (`ProductRepositoryInterface`) centralize all data access through a clean API.

**When to use**: Always — for any data access beyond simple reads. It's the standard Magento pattern.

### Command

Encapsulates a request as an object. Magento's Payment Gateway Command pattern uses this — authorize, capture, refund are separate command objects.

**When to use**: When you need to parameterize, queue, or log requests.

## Architectural Patterns

### Dependency Injection

Objects receive their dependencies through constructors rather than creating them. Magento's DI container (Object Manager + di.xml) is the foundation of the entire framework.

**When to use**: Always — it's the core pattern. Inject interfaces, not concrete classes.

### Service Layer

Defines an application's boundary with a layer of services that encapsulates business logic. Magento's Service Contracts (interfaces in `Api/`) form this layer.

**When to use**: Always — expose module functionality through service interfaces.

### Data Transfer Object (DTO)

Simple objects that carry data between processes. Magento's Data Interfaces (`Api/Data/`) are DTOs — they have getters/setters but no business logic.

**When to use**: When passing data across architectural boundaries (API, service layer).

## Anti-Patterns to Avoid

- **God Object** — classes that do too much (split into focused services)
- **Service Locator** — calling Object Manager directly (use constructor injection)
- **Anemic Domain Model** — models with only getters/setters (add behavior where appropriate)
- **Tight Coupling** — depending on concrete classes (depend on interfaces)
- **Hard-coded Dependencies** — instantiating with `new` (use factories or DI)

## Best Practices

- Program to interfaces, not implementations
- Favor composition over inheritance
- Keep classes focused (Single Responsibility)
- Use DI container for dependency management
- Use factories for creating non-shared instances
- Use proxies for lazy-loading expensive dependencies
- Use the strategy pattern for swappable algorithms
- Document which pattern a class implements

Fetch current framework documentation for exact interface signatures and implementation patterns before applying.
