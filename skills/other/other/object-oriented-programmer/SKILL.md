---
name: object-oriented-programmer
description: Object-oriented design principles, patterns, and practices. Use when working with object-oriented languages (Java, C#, C++, Python, Ruby, Swift, etc.) without language-specific skills available, or when applying OOP in multi-paradigm codebases.
---

# Object-Oriented Programmer

## Purpose

This skill provides guidance on object-oriented programming principles, design patterns, and practices. Object-oriented programming organizes code around objects that combine data and behavior, using encapsulation, inheritance, and polymorphism to manage complexity. This skill serves as a foundation when working with OO languages or applying object-oriented design in multi-paradigm codebases.

## When to Use This Skill

Use this skill when:
- Working with object-oriented languages (Java, C#, C++, Python, Ruby, Swift) without language-specific skills available
- Designing systems with complex state and behavior
- Modeling domains with rich entity relationships
- Building frameworks or libraries with extension points
- Working with existing OOP codebases

**Note:** Language-specific skills (e.g., java-programmer, python-programmer) supersede this skill when available.

## Core Philosophy

### Objects as Encapsulated State and Behavior

Object-oriented programming bundles data (state) with the operations (behavior) that act on that data. An object presents a clean interface while hiding implementation details. This encapsulation creates boundaries that limit coupling and enable local reasoning.

**Quote to remember:** "Bad programmers worry about the code. Good programmers worry about data structures and their relationships." — Linus Torvalds

### Polymorphism Enables Abstraction

Polymorphism allows treating different types uniformly through shared interfaces. This enables writing code against abstractions rather than concrete types, making systems more flexible and extensible.

**Types of polymorphism:**
- **Subtype polymorphism** — Inheritance hierarchies (interfaces, abstract classes)
- **Parametric polymorphism** — Generics/templates
- **Ad-hoc polymorphism** — Method overloading

### Inheritance as Code Reuse (Use Carefully)

Inheritance enables defining types in terms of other types, inheriting both interface and implementation. However, inheritance creates tight coupling between parent and child classes.

**The inheritance trade-off:** Inheritance is easy to add (create subclass) but hard to change (affects all subclasses). Composition is harder to add (requires more boilerplate) but easier to change (localized impact).

**Modern wisdom:** "Composition over inheritance" — prefer delegating to contained objects over inheriting from parent classes.

## Fundamental Principles

### Encapsulation Hides Complexity

Encapsulation bundles related data and behavior while hiding internal implementation. Objects expose interfaces; internals are private.

**Why encapsulation matters:**
- Limits coupling (changes don't ripple through codebase)
- Enables local reasoning (understand object in isolation)
- Protects invariants (object controls its own consistency)
- Provides flexibility (change internals without affecting clients)

**Encapsulation boundaries:**
- Private state, public interface
- Package-private for internal APIs
- Protected for inheritance hierarchies (use sparingly)

### Abstraction Manages Complexity

Abstraction focuses on essential characteristics while hiding incidental details. Interfaces and abstract classes define contracts without specifying implementation.

**Why abstraction matters:**
- Program against interfaces, not implementations
- Enable substitution (Liskov Substitution Principle)
- Defer decisions (choose implementations later)
- Facilitate testing (mock interfaces easily)

**Abstraction levels:**
- Interfaces — Pure contracts (no implementation)
- Abstract classes — Partial implementation with extension points
- Concrete classes — Full implementation

### Polymorphism Enables Flexibility

Polymorphism allows uniform treatment of different types. Write code once that works with many implementations.

**Why polymorphism matters:**
- Add new implementations without changing client code
- Strategy pattern (choose behavior at runtime)
- Plugin architectures (extend without modifying core)
- Testing (inject mocks/stubs through interfaces)

**Polymorphism trade-off:** Indirection obscures flow. Reading polymorphic code requires knowing what implementations exist and which is active. Balance flexibility against clarity.

<solid_principles>
## SOLID Principles

SOLID provides guidelines for object-oriented design. These are heuristics, not laws—apply them where they improve code, not dogmatically.

<single_responsibility>
### Single Responsibility Principle

A class should have one reason to change. Each class should do one thing well.

**Good indicators:**
- Can describe class purpose in one sentence without "and"
- Changes to requirements affect only one class
- Class has cohesive set of methods

**When to violate:**
- Very small classes (splitting increases complexity)
- Clearly related concerns (don't separate prematurely)
- Performance-critical hot paths (fewer objects, fewer allocations)

**Common mistake:** Confusing "single responsibility" with "one method." Classes can have multiple methods serving one coherent purpose.
</single_responsibility>

<open_closed>
### Open-Closed Principle

Open for extension, closed for modification. Add new behavior without changing existing code.

**Implementation strategies:**
- Inheritance — Extend base classes (classic OCP)
- Composition — Inject dependencies (modern preference)
- Strategy pattern — Plug in different algorithms
- Template method — Override specific steps

**When to violate:**
- Requirements fundamentally change (refactor rather than extend)
- Abstraction is speculative (YAGNI — You Aren't Gonna Need It)
- System is small and changes are cheap

**Staff insight:** OCP assumes future requirements. Don't add extension points for hypothetical needs. Wait until you need to extend, then refactor to enable it.
</open_closed>

<liskov_substitution>
### Liskov Substitution Principle

Subtypes must be substitutable for their base types.[^1] Derived classes should strengthen (not weaken) base class contracts.

**What LSP means:**
- Preconditions cannot be strengthened (subclass can't be more restrictive)
- Postconditions cannot be weakened (subclass must do at least as much)
- Invariants must be preserved (subclass maintains base class guarantees)

**Common LSP violations:**
- Square extending Rectangle (breaks area calculation expectations)
- ReadOnlyCollection extending Collection (throws on mutating methods)
- Overriding methods to do nothing or throw exceptions

**When inheritance violates LSP, use composition instead.**

[^1]: Barbara Liskov and Jeannette Wing. 1994. A behavioral notion of subtyping. *ACM Transactions on Programming Languages and Systems* 16, 6 (Nov. 1994), 1811–1841. https://doi.org/10.1145/197320.197383
</liskov_substitution>

<interface_segregation>
### Interface Segregation Principle

Clients shouldn't depend on interfaces they don't use. Many specific interfaces beat one general interface.

**Why ISP matters:**
- Smaller surface area (easier to understand)
- Avoid implementing unnecessary methods
- Reduce coupling (changes affect fewer clients)
- Enable role-based interfaces

**When to violate:**
- Interface has few methods (splitting is overhead)
- All clients use all methods
- Language lacks interface composition (can't extend multiple interfaces)

**Staff insight:** ISP fights "fat interfaces." If clients only use subset of methods, split the interface. But don't create explosion of single-method interfaces either.
</interface_segregation>

<dependency_inversion>
### Dependency Inversion Principle

Depend on abstractions, not concretions. High-level modules shouldn't depend on low-level modules.

**Implementation:**
- Inject dependencies rather than constructing them
- Program against interfaces, not classes
- Use dependency injection frameworks (Spring, Guice) or manual constructor injection

**Why DIP matters:**
- Testability (inject mocks)
- Flexibility (swap implementations)
- Parallel development (implement against interfaces)
- Inversion of control (framework calls you)

**When to violate:**
- Value objects and data structures (no abstraction needed)
- Stable dependencies (standard library, mature frameworks)
- Performance-critical paths (virtual dispatch has cost)
</dependency_inversion>
</solid_principles>

## Design Patterns: Use With Judgment

The Gang of Four patterns are valuable but often overused. Apply patterns to solve real problems, not to demonstrate pattern knowledge.

**Quote to remember:** "Fools ignore complexity. Pragmatists suffer it. Some can avoid it. Geniuses remove it." — Alan Perlis

### Creational Patterns

**Factory Method** — Delegate object creation to subclasses
- **Use when:** Creation logic varies by subtype
- **Avoid when:** Simple construction suffices

**Abstract Factory** — Create families of related objects
- **Use when:** Multiple related object types must be consistent
- **Avoid when:** Only one object type or no consistency requirements

**Builder** — Construct complex objects step-by-step
- **Use when:** Many optional parameters or complex construction
- **Avoid when:** Simple constructors suffice

**Singleton** — Ensure single instance exists
- **Use when:** Global state is truly necessary (logging, config)
- **Avoid when:** Global state can be avoided (usually)
- **Staff insight:** Singletons are global state. Prefer dependency injection.

### Structural Patterns

**Adapter** — Convert one interface to another
- **Use when:** Integrating incompatible interfaces
- **Good for:** Wrapping third-party libraries

**Decorator** — Add behavior without subclassing
- **Use when:** Adding responsibilities dynamically
- **Good for:** Cross-cutting concerns (logging, caching)

**Facade** — Simplify complex subsystems
- **Use when:** Complex system needs simple interface
- **Good for:** API boundaries, legacy system integration

**Composite** — Treat individuals and compositions uniformly
- **Use when:** Tree structures (UI hierarchies, file systems)
- **Pattern:** Same interface for leaf and composite

### Behavioral Patterns

**Strategy** — Encapsulate interchangeable algorithms
- **Use when:** Multiple algorithms, runtime selection
- **Good for:** Different sorting, validation, pricing strategies

**Observer** — Notify dependents of state changes
- **Use when:** One-to-many dependencies, event handling
- **Watch for:** Memory leaks (observers not released)

**Template Method** — Define algorithm skeleton, defer steps to subclasses
- **Use when:** Algorithm structure is fixed, steps vary
- **Alternative:** Strategy pattern with composition

**Command** — Encapsulate requests as objects
- **Use when:** Queuing operations, undo/redo, logging
- **Good for:** Job queues, macro recording

**Visitor** — Separate algorithm from object structure
- **Use when:** Operations vary often, structure rarely changes
- **Dual to:** Functional approach (pattern matching)

### Pattern Pitfalls

**Avoid pattern-driven design:**
- Don't apply patterns because you "should"
- Don't choose patterns before understanding the problem
- Don't use patterns to demonstrate sophistication

**Watch for over-engineering:**
- Simple problems don't need complex patterns
- Patterns add indirection (cognitive cost)
- Future flexibility has present complexity cost

**Quote to remember:** "The cheapest, fastest, and most reliable components are those that aren't there." — Gordon Bell

## Staff-Level Insights

### When OOP Works Well

Object-oriented programming excels in specific contexts:

**Domain modeling with rich behavior:**
- Entities with complex state and invariants
- Business logic tied to data
- Systems modeling real-world objects

**Frameworks and extensibility:**
- Plugin architectures
- Template methods for customization
- Inversion of control containers

**UI and stateful systems:**
- GUI widgets with state and event handlers
- Game entities with behavior
- Simulations with evolving state

**Legacy codebases:**
- Established OOP systems (don't fight the paradigm)
- Team expertise in OOP patterns
- Ecosystem built around OOP (frameworks, libraries)

### When OOP Struggles

**Data transformation pipelines:**
- FP map/filter/reduce is clearer
- Immutable transformations avoid state bugs
- Composition over object hierarchies

**Highly concurrent systems:**
- Shared mutable state causes race conditions
- Message passing (Erlang/Elixir) or immutability (Clojure) may be better
- Actor model or functional approaches reduce concurrency issues

**Simple utilities and scripts:**
- Functions suffice without object structure
- Overhead of classes doesn't pay off
- Procedural or functional style is clearer

**Systems requiring frequent new operations:**
- Expression problem: OOP makes adding operations hard
- Every new operation requires touching all classes
- Functional approach (pattern matching) may be easier

### The Expression Problem Revisited

The expression problem[^3] describes a fundamental trade-off between extensibility dimensions:

**Object-oriented trade-off:**
- Easy to add new types (create new subclass)
- Hard to add new operations (modify all classes)

**When this trade-off favors OOP:**
- Domain has stable set of operations
- New types are added frequently
- Example: UI widgets (standard operations: render, handle input; many widget types)

**When this trade-off hurts OOP:**
- Operations change frequently
- Types are relatively stable
- Example: Compiler (fixed AST nodes; many new optimization passes)

**Solutions:**
- Visitor pattern (add operations to OO systems)
- Multi-methods (CLOS, Clojure)
- Type classes (Haskell)
- Accept the trade-off based on domain

[^3]: Philip Wadler. 1998. The Expression Problem. Email to the Java Genericity mailing list. http://homepages.inf.ed.ac.uk/wadler/papers/expression/expression.txt

### Inheritance vs. Composition

**When inheritance works:**
- True "is-a" relationship (not just code reuse)
- Liskov Substitution holds
- Subclass extends, not replaces, parent behavior
- Hierarchy is shallow (2-3 levels max)

**When composition is better:**
- "Has-a" or "uses-a" relationship
- Behavior can be mixed and matched
- Runtime flexibility needed
- Deep hierarchies forming

**Staff insight:** Default to composition. Only use inheritance when substitutability is genuinely needed. Most "inheritance for code reuse" is better served by composition or helper functions.

**Quote to remember:** "Favor composition over inheritance." — Gang of Four, Design Patterns

### Abstraction Costs

Abstraction has benefits but also costs:

**Benefits:**
- Flexibility (swap implementations)
- Testability (inject mocks)
- Separation of concerns

**Costs:**
- Indirection (harder to trace execution)
- Cognitive load (understand interface + implementations)
- Performance (virtual dispatch overhead)

**Guidelines:**
- Abstract when you have multiple implementations or expect future ones
- Abstract at module boundaries (not within modules)
- Don't abstract prematurely (YAGNI)
- Measure abstraction cost (some indirection is fine; seven layers is not)

### Testing Object-Oriented Code

**OOP enables testing through:**
- Dependency injection (inject mocks/stubs)
- Interface-based design (implement test doubles)
- Encapsulation (test through public API)

**OOP testing challenges:**
- Deep inheritance hierarchies (hard to set up state)
- Tight coupling (can't test in isolation)
- Hidden dependencies (static methods, singletons)

**Testing guidelines:**
- Favor composition (easier to inject test doubles)
- Minimize statics and singletons (global state)
- Test through interfaces (implementation agnostic)
- Keep setup simple (complex setup indicates design issues)

### OOP in Multi-Paradigm Languages

Many modern languages support multiple paradigms (Python, JavaScript, Ruby, Swift):

**Applying OOP selectively:**
- Use objects for stateful entities
- Use functions for transformations
- Use modules/namespaces for organization
- Mix paradigms within same codebase

**Don't force OOP everywhere:**
- Not every function needs a class
- Utility functions can stand alone
- Modules organize without inheritance
- Accept procedural or functional code where clearer

**Staff insight:** OOP is one tool. Modern software engineering embraces multi-paradigm thinking. Choose the right paradigm for each problem rather than forcing everything into objects.

<anti_patterns>
## Common Pitfalls and Anti-Patterns

<god_objects>
### God Objects

**Anti-pattern:** One class does too much, knows too much, controls too much.

**Fix:**
- Split responsibilities into focused classes
- Apply Single Responsibility Principle
- Create collaborating objects instead of one omniscient object
</god_objects>

<anemic_domain_model>
### Anemic Domain Model

**Anti-pattern:** Objects with only getters/setters, no behavior. Logic lives in separate "service" classes.[^2]

**When it's actually fine:**
- Data transfer objects (DTOs)
- Value objects
- Database entities in some architectures

**When it's a problem:**
- Domain logic is scattered across services
- Objects are just data bags with no encapsulation

**Fix:** Move behavior to objects that own the data

[^2]: Martin Fowler. 2003. AnemicDomainModel. https://martinfowler.com/bliki/AnemicDomainModel.html
</anemic_domain_model>

<deep_inheritance>
### Deep Inheritance Hierarchies

**Anti-pattern:** 5+ levels of inheritance creating brittle, hard-to-understand hierarchies.

**Fix:**
- Flatten hierarchy using composition
- Interfaces instead of abstract base classes
- Keep hierarchies shallow (2-3 levels max)
</deep_inheritance>

<primitive_obsession>
### Primitive Obsession

**Anti-pattern:** Using primitives instead of small objects (string for email, int for money).

**Fix:**
- Create value objects (Email, Money classes)
- Encapsulate validation and behavior
- Type safety through distinct types
</primitive_obsession>

<feature_envy>
### Feature Envy

**Anti-pattern:** Method in one class uses data/methods from another class more than its own.

**Fix:**
- Move method to the class it envies
- Create new class if both classes envy common data
- Apply "Tell, Don't Ask" principle
</feature_envy>

<inappropriate_intimacy>
### Inappropriate Intimacy

**Anti-pattern:** Classes know too much about each other's internals.

**Fix:**
- Increase encapsulation
- Communicate through well-defined interfaces
- Reduce coupling between classes
</inappropriate_intimacy>
</anti_patterns>

### Common Mistakes from Functional Programming Backgrounds

Programmers coming from functional languages sometimes resist OOP patterns that would actually clarify:

**Avoiding necessary state when mutation is clearer:**
- **Mistake:** Immutable everything, even for inherently stateful domains (UI widgets, game entities)
- **Fix:** Embrace encapsulated mutable state. OOP's strength is managing state safely through encapsulation

**Creating anemic domain models:**
- **Mistake:** Separating data from behavior (DTOs + service layers) because "data should be separate"
- **Fix:** Co-locate data with operations that maintain invariants. Encapsulation is about protecting invariants

**Over-using immutability when mutation is more efficient:**
- **Mistake:** Persistent data structures everywhere, even in performance-critical code
- **Fix:** Profile first. Mutable collections are often clearer and faster when properly encapsulated

**Making everything pure when side effects are acceptable:**
- **Mistake:** Forcing purity in languages/contexts where it fights idioms
- **Fix:** Accept that OOP embraces controlled side effects. Encapsulation makes them safe

**Not leveraging polymorphism through subtyping:**
- **Mistake:** Using strategy pattern everywhere instead of simple inheritance
- **Fix:** Inheritance is appropriate for true is-a relationships with substitutability

**Avoiding classes when objects would clarify:**
- **Mistake:** Module of functions + data structure when object with methods is clearer
- **Fix:** Objects make sense when behavior and data are tightly coupled and invariants matter

**Thinking in transformations when stateful objects are clearer:**
- **Mistake:** Functional pipelines for inherently stateful workflows
- **Fix:** State machines, objects with lifecycle. Not everything is a transformation

**Not using encapsulation's benefits:**
- **Mistake:** Public fields because "data should be transparent"
- **Fix:** Private state, public interface. Encapsulation protects invariants and enables change

<related_skills>
## Related Skills

- **software-engineer** — Core engineering philosophy, hexagonal architecture, system design
- **functional-programmer** — When functional approaches are clearer (transformations, concurrency)
- **test-driven-development** — Testing philosophy and TDD principles
- **java-programmer**, **python-programmer**, **swift-programmer** — Language-specific OOP idioms
</related_skills>

<safety_constraints>
## Safety Constraints

<inheritance_safety>
### Inheritance Safety
- **Never** create inheritance hierarchies deeper than 3 levels without exceptional justification
- **Never** use inheritance solely for code reuse—composition exists for this
- **Always** verify Liskov Substitution holds before creating a subclass
- **Never** override methods to do nothing or throw "not implemented" exceptions
</inheritance_safety>

<encapsulation_safety>
### Encapsulation Safety
- **Never** expose mutable collections directly—return copies or unmodifiable views
- **Never** break encapsulation "just for testing"—if you can't test through public API, design is flawed
- **Never** make fields public "for convenience"—use proper accessors
</encapsulation_safety>

<pattern_safety>
### Pattern Safety
- **Never** use Singleton for anything that could reasonably be injected
- **Never** apply Observer pattern without clear lifecycle management (subscription cleanup)
- **Never** use inheritance where composition would work—inheritance is not for code reuse
</pattern_safety>
</safety_constraints>

## Summary

Object-oriented programming emphasizes:
- **Encapsulation** — Bundle data and behavior, hide internals
- **Abstraction** — Program against interfaces, defer implementation
- **Polymorphism** — Treat different types uniformly
- **Inheritance** — Use sparingly, prefer composition

Apply OOP where it improves design: modeling domains with rich behavior, building extensible frameworks, managing complex state. Use other paradigms where they're clearer: functional for transformations, procedural for utilities. Modern software engineering is multi-paradigm—choose the right tool for each problem.
