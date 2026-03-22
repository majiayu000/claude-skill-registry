---
name: functional-programmer
description: Functional programming principles, patterns, and practices. Use when working with functional languages (Racket, Clojure, Erlang, Haskell, Idris, Scheme, OCaml, F#, Elixir, etc.) without language-specific skills available, or when applying functional paradigms in multi-paradigm languages.
---

# Functional Programmer

## Purpose

This skill provides guidance on functional programming principles, patterns, and practices. Functional programming treats computation as the evaluation of mathematical functions, emphasizing immutability, pure functions, and declarative style. This skill serves as a foundation when working with functional languages or applying functional paradigms in multi-paradigm codebases.

## When to Use This Skill

Use this skill when:
- Working with functional languages (Racket, Clojure, Erlang, Haskell, Idris, Scheme, OCaml, F#, Elixir) without language-specific skills available
- Applying functional programming patterns in multi-paradigm languages (Java, Python, JavaScript)
- Designing systems that benefit from immutability and pure functions
- Refactoring imperative code to functional style
- Working with data transformation pipelines

**Note:** Language-specific skills (e.g., clojure-programmer, racket-programmer) supersede this skill when available.

## Core Philosophy

### Code as Mathematical Expression

Functional programming views programs as compositions of mathematical functions. A function always produces the same output for the same input, with no hidden state or side effects. This mathematical purity enables powerful reasoning about code behavior.

**Quote to remember:** "Programs must be written for people to read, and only incidentally for machines to execute." — Harold Abelson, SICP

### Data Transformation Over Mutation

Rather than modifying data in place, functional programming creates new data structures through transformation. This immutability enables:
- Safer concurrent programs (no race conditions)
- Easier reasoning about program state
- Simpler testing (functions are deterministic)
- Time-travel debugging and undo mechanisms

### Composition as Primary Abstraction

Build complex behavior by composing simple functions. Small, single-purpose functions combine to create sophisticated systems. Composition is the fundamental abstraction mechanism in functional programming.

## Fundamental Principles

### Immutability Makes Time Explicit

Data structures cannot be modified after creation. Instead, transformations produce new structures. This makes time and change explicit rather than hidden.

**Quote to remember:** "Time is a device that was invented to keep everything from happening at once." — Ray Cummings (1922), often misattributed

**Why immutability matters:**
- Eliminates entire classes of bugs (unexpected mutations, race conditions)
- Enables safe sharing without defensive copying
- Simplifies reasoning (values don't change underfoot)
- Facilitates time-travel debugging and undo

**Implementation:** Persistent data structures with structural sharing, copy-on-write, or immutable-by-convention.

### Pure Functions Enable Reasoning

Pure functions always return the same output for the same input, with no side effects. This referential transparency enables equational reasoning about code.

**Why purity matters:**
- Test without complex setup
- Compose freely (outputs match inputs)
- Parallelize safely (no shared state)
- Cache results (memoization)
- Reason algebraically (substitute equals for equals)

**Managing effects:** Push side effects to program boundaries. Separate pure core logic from effectful actions. Use effect systems when appropriate.

### Higher-Order Functions as Abstraction

Functions as values enable abstracting over patterns, not just data. This is more powerful than data abstraction alone.

**Why higher-order functions matter:**
- Express patterns once, apply everywhere (map/filter/reduce over any collection)
- Build domain-specific abstractions (custom control flow)
- Parameterize behavior, not just data
- Construct complex operations from simple parts

### Declarative Style Expresses Intent

Express *what* to compute, not *how*. Describe desired results rather than step-by-step procedures. This shifts from mechanical instructions to logical assertions about the result.

**Why declarative style matters:**
- Code reads as specification
- Implementation can optimize without changing meaning
- Easier to verify correctness (matches problem statement)
- Separates concerns (what vs. how)

<fp_decision_framework>
## When to Use Functional Programming

From the software-engineer skill, use functional approaches when:
- Transforming data through pipelines
- Ensuring correctness through immutability
- Working with concurrent systems
- Composing small, reusable operations
- Avoiding state-related bugs

**Key principles:**
- Pure functions (no side effects)
- Immutable data structures
- First-class and higher-order functions
- Composition over inheritance

<paradigm_decision_table>
### When to Choose FP vs. Other Paradigms

| Situation | FP Strength | Consider Alternative When |
|-----------|-------------|---------------------------|
| Data pipelines | Composition, immutability | Complex branching logic needed |
| Concurrent systems | No shared mutable state | Inherently stateful (games, GUIs) |
| Correctness-critical | Equational reasoning, testing | Performance-critical tight loops |
| Reusable operations | Higher-order functions | Team unfamiliar with FP |
| Domain modeling | ADTs, pattern matching | Extensible data (expression problem) |
| Parsing/transformation | Declarative specification | Complex imperative protocols |
| Mathematical computation | Pure functions match math | I/O-heavy applications |
</paradigm_decision_table>
</fp_decision_framework>

<fp_thinking_patterns>
## FP Thinking Patterns

<data_transformation>
### Data Transformation Over Control Flow

Prefer expressing operations as data transformations (map/filter/reduce) rather than control flow (loops/conditionals):

**When transformation patterns work well:**
- Processing collections uniformly
- Building pipelines of operations
- Expressing intent declaratively
- Composing reusable transformations

**When explicit control flow may be clearer:**
- Complex conditional logic with many branches
- Early termination conditions
- Performance-critical loops (profile first)
- Interleaving multiple operations
</data_transformation>

<recursion_tradeoffs>
### Recursion and Its Trade-offs

Recursion is elegant for naturally recursive structures but has costs:

**Prefer recursion for:**
- Tree and graph traversal
- Divide-and-conquer algorithms
- Processing recursive data structures
- Problems with inherently recursive definitions

**Consider alternatives when:**
- Language lacks tail call optimization (stack overflow risk)
- Simple iteration is clearer
- Performance matters (measure first)

**Tail recursion** enables constant-space recursion in languages that support it. Use trampolining to simulate TCO when unavailable.
</recursion_tradeoffs>

<composition_architecture>
### Composition as Architecture

Build complex behavior by composing simple functions. Composition is more than a pattern—it's an architectural principle.

**Composition works well when:**
- Operations form clear pipelines
- Intermediate results are meaningful
- Each step is independently useful
- Data flow is unidirectional

**Composition challenges:**
- Debugging composed pipelines (step through separately)
- Error handling across composition boundaries
- Type mismatches in composition chains
- Overly abstract compositions obscuring intent

**Partial application and currying** enable building specialized functions from general ones. Use when creating function pipelines or delaying argument provision. Don't curry everything—clarity matters more than cleverness.
</composition_architecture>

<algebraic_data_types>
### Algebraic Data Types for Correctness

Make invalid states unrepresentable through sum types (variants) and product types (tuples/records):

**Power of sum types:**
- Exhaustive pattern matching (compiler catches missing cases)
- Eliminate null checks (Option/Maybe types)
- Model business domains precisely
- Encode state machines explicitly

**When to use:**
- Modeling domains with distinct cases
- Representing success/failure (Result/Either types)
- Eliminating impossible states
- Languages with strong pattern matching support
</algebraic_data_types>

<monad_guidance>
### Monads: Use Judiciously

Monads are powerful but often unnecessary. They solve specific problems—don't reach for them reflexively.

**Good uses of monads:**
- `Maybe`/`Option` — Avoiding null checks and making absence explicit
- `Either`/`Result` — Error handling as values (when exceptions aren't idiomatic)
- `IO` — Isolating side effects in pure languages
- `State` — Threading state through pure computations
- `List` — Non-deterministic computation

**Don't use monads when:**
- Simpler patterns exist (language-specific idioms)
- Team unfamiliar with monadic patterns
- Null handling or exceptions are acceptable
- The abstraction obscures rather than clarifies

**The monad tutorial fallacy:** Monads aren't mysterious. They're patterns for chaining operations that return wrapped values. Use them when that's useful; don't force them.
</monad_guidance>
</fp_thinking_patterns>

## Staff-Level Insights

### When Not to Use Functional Programming

Functional programming is powerful but not universally optimal. Avoid forcing FP in these situations:

**Performance-critical tight loops:**
- Immutability and persistent data structures have overhead
- Mutating arrays in-place can be orders of magnitude faster
- Sometimes imperative code is clearer and more efficient

**Inherently stateful domains:**
- User interfaces with complex local state
- Game loops with entity updates
- Simulations requiring in-place updates
- Consider imperative or object-oriented approaches

**Team and ecosystem constraints:**
- Team unfamiliar with FP (training cost)
- Libraries and frameworks are imperative
- Codebase is predominantly non-functional

**Context over dogma:** Choose the right tool for the job. FP is one paradigm among many.

### Closures and Objects Are Equivalent

Closures and objects are fundamentally equivalent mechanisms for encapsulating state with behavior:

**Closures** capture environment and expose functions:
```
makeCounter() {
    let count = 0
    return {
        increment: () => ++count,
        get: () => count
    }
}
```

**Objects** store state and expose methods:
```
class Counter {
    private count = 0
    increment() { return ++this.count }
    get() { return this.count }
}
```

Both bind data to code; the difference is syntax and convention. This equivalence reveals:
- FP can represent objects using closures
- OOP can represent closures using objects with a single method
- The paradigms are dual approaches to the same problem

**Quote to remember:** "Objects are a poor man's closures" (and vice versa) — attributed to Norman Adams; the inverse attributed to Christian Queinnec. Choose based on idiom, not dogma.

<state_management>
### Managing State in Functional Systems

Pure functions can't perform I/O or maintain state. Real programs need both.

**State management strategies:**

1. **Push state to boundaries** — Keep core logic pure; handle state at program edges
2. **Explicit state threading** — Pass state through function parameters
3. **State monads** — Encapsulate state threading (in languages with monads)
4. **Atoms/Refs/Agents** — Controlled mutation (Clojure model)
5. **Persistent data structures** — Efficient immutable updates
6. **Coeffects** — Type-directed context management (see below)

<coeffects>
**Coeffects for context management:**

Coeffects (dual to effects/monads) track how programs interact with their execution context.[^1] While monads track computational *effects* (what a program does to the world), coeffects track computational *requirements* (what a program needs from its environment).

**The core problem:** How to keep functions pure while accessing external context (current time, localStorage, database, GPS sensors). Coeffects make these dependencies explicit rather than hidden side effects.

**Coeffects as dependency injection:** Coeffects are fundamentally a form of dependency injection with a type-theoretic foundation. Traditional DI passes dependencies via constructors/parameters; coeffects declare dependencies in metadata or types, and the framework injects them into a context map. Both make dependencies explicit, improve testability (inject mocks), and invert control (caller provides what callee needs).

**Examples of coeffect systems:**
- Explicit environmental dependencies (re-frame in Clojure: event handlers declare required context like `:now` or `:local-store`)
- Variable usage analysis (liveness, linearity)
- Past values in dataflow programming (accessing previous stream values)
- Platform/API versioning (cross-platform compatibility)
- Resource availability tracking (GPS sensor, database access)

**Practical use:** Coeffects work in both typed (using indexed comonads) and dynamic languages (using data injection patterns). They're valuable when you need explicit, testable environmental dependencies rather than hidden global access. However, they're an advanced pattern—apply them when environmental dependencies need to be explicit and verifiable, not as a general replacement for simpler state management.

[^1]: Tomas Petricek, Dominic Orchard, and Alan Mycroft. 2014. Coeffects: A calculus of context-dependent computation. In *Proceedings of the 19th ACM SIGPLAN International Conference on Functional Programming (ICFP '14)*. https://doi.org/10.1145/2628136.2628160
</coeffects>

**Real systems combine pure and impure code.** The goal is to maximize the pure portion while handling effects and context systematically.
</state_management>

### Performance Considerations

Functional programming patterns can have performance implications:

**Persistent data structures:**
- More memory allocation (GC pressure)
- Structural sharing amortizes cost
- Usually acceptable for most use cases
- Profile before optimizing

**Lazy evaluation:**
- Defers computation until needed
- Can prevent unnecessary work
- Can cause space leaks if not careful
- Thunks accumulate if not forced

**Recursion:**
- Elegant but risks stack overflow
- Tail call optimization essential (not all languages support it)
- Trampolining can simulate TCO
- Sometimes iteration is faster

**Trade-off:** Functional code prioritizes correctness and maintainability over raw performance. Optimize hot paths when profiling shows the need.

### Debugging Functional Code

Pure functions are easier to test but can be harder to debug:

**Debugging strategies:**
- **REPL-driven development** — Test functions interactively
- **Logging in pure code** — Use logging monads or effect systems
- **Tracing** — Instrument function calls to see execution flow
- **QuickCheck/property testing** — Generate test cases to find bugs
- **Equational reasoning** — Trace execution by substitution

**Common debugging challenges:**
- Lazy evaluation hiding errors until evaluation
- Deep recursion obscuring stack traces
- Composed functions abstracting execution flow

**Mitigation:** Write small, well-tested functions. Use types to catch errors early. Test compositions separately from components.

### Functional Programming in Non-Pure Languages

Many languages support FP without being purely functional (Java, Python, JavaScript, Swift):

**Applying FP in multi-paradigm languages:**
- Use immutable data structures when practical
- Prefer pure functions for core logic
- Use language FP features (lambdas, streams, map/filter/reduce)
- Accept side effects where idiomatic
- Don't fight the language's paradigm

**Practical FP:**
- Immutability by convention (not enforcement)
- Pure functions where beneficial
- Higher-order functions for abstraction
- Declarative style when clearer

**Don't be a zealot:** Use FP where it improves code. Accept imperative patterns where they're clearer or more efficient.

### Balancing Abstraction and Clarity

Functional programming enables powerful abstractions, but abstraction has costs:

**Abstraction benefits:**
- Eliminate duplication
- Express patterns concisely
- Build domain-specific languages

**Abstraction costs:**
- Learning curve for unfamiliar abstractions
- Indirection obscures behavior
- Harder to debug and trace

**Guidelines:**
- Abstract when patterns recur (3+ times)
- Name abstractions clearly
- Document non-obvious abstractions
- Prefer simple abstractions over clever ones
- Consider the audience (will they understand this?)

**Kernighan's Law:** "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it." — Brian Kernighan

**Quote to remember:** "Fools ignore complexity. Pragmatists suffer it. Some can avoid it. Geniuses remove it." — Alan Perlis

### The Expression Problem

The expression problem[^2]: how to add new data variants and new operations without modifying existing code?

**Object-oriented approach:** Easy to add new data types (subclasses), hard to add new operations (requires modifying all classes).

**Functional approach:** Easy to add new operations (new functions), hard to add new data variants (requires modifying all pattern matches).

**Solutions:**
- Visitor pattern (OO solution)
- Type classes / protocols (FP solution)
- Multi-methods (CLOS, Clojure)
- Accept the trade-off based on domain

**Know which dimension you'll extend:** If adding data types is common, consider OO. If adding operations is common, consider FP.

[^2]: Philip Wadler. 1998. The Expression Problem. Email to the Java Genericity mailing list. http://homepages.inf.ed.ac.uk/wadler/papers/expression/expression.txt

<common_pitfalls>
## Common Pitfalls and How to Avoid Them

<pointfree_overuse>
### Excessive Pointfree Style

**Pointfree** (tacit) style omits function parameters:
```
sum = reduce(add, 0)  # pointfree
sum = λ(xs) → reduce(add, 0, xs)  # with points
```

**Pitfall:** Pointfree code can become unreadable when overused.

**Guideline:** Use pointfree for simple compositions. Add explicit parameters when clarity improves.
</pointfree_overuse>

<recursion_overuse>
### Overusing Recursion

**Pitfall:** Recursion for every loop leads to stack overflow in languages without tail call optimization.

**Guideline:**
- Use built-in collection functions (`map`, `filter`, `reduce`) instead of explicit recursion
- Use iteration when the language doesn't optimize tail calls
- Use tail-recursive style when recursion is needed
</recursion_overuse>

<strictness_laziness>
### Ignoring Strictness vs. Laziness

**Pitfall:** Assuming all functional languages behave the same regarding evaluation order.

**Lazy languages** (Haskell): Expressions evaluate only when needed.
**Strict languages** (most others): Expressions evaluate immediately.

**Guideline:** Understand your language's evaluation model. Lazy evaluation enables infinite data structures but can cause space leaks. Strict evaluation is predictable but evaluates everything.
</strictness_laziness>

<forced_purity>
### Forcing Purity Everywhere

**Pitfall:** Trying to eliminate all side effects leads to convoluted code.

**Guideline:** Separate pure core logic from effectful boundaries. Accept that real programs perform I/O. Use language idioms for effects rather than fighting them.
</forced_purity>

<premature_abstraction>
### Premature Abstraction

**Pitfall:** Creating overly generic abstractions before understanding the problem.

**Guideline:** Follow the rule of three — abstract after seeing a pattern three times. Let abstractions emerge from concrete code rather than designing them upfront.
</premature_abstraction>

<ignoring_performance>
### Ignoring Performance

**Pitfall:** Assuming immutability and higher-order functions have no performance cost.

**Guideline:** Profile before optimizing. Most FP patterns are fast enough. When performance matters, use mutable data structures in hot paths (wrapped in pure interfaces if needed).
</ignoring_performance>
</common_pitfalls>

<common_mistakes_by_background>
### Common Mistakes from Object-Oriented and Imperative Backgrounds

Programmers coming from OOP or imperative languages often import patterns that work against functional principles:

<from_oop_background>
**From Object-Oriented Programming:**

**Creating class-like structures when simpler patterns suffice:**
- **Mistake:** Building complex closure hierarchies mimicking inheritance
- **Fix:** Use data + functions. Not everything needs object-like encapsulation
- **Remember:** Closures and objects are equivalent, but FP idiom is flat functions operating on data

**Over-engineering with manager/helper patterns:**
- **Mistake:** Creating `UserManager`, `DataHelper` classes (actually closure bundles)
- **Fix:** Compose simple functions. Managers/helpers often indicate missing abstraction or unnecessary ceremony

**Not embracing immutability:**
- **Mistake:** Defensive copying instead of persistent data structures
- **Fix:** Use language's persistent data structures (structural sharing). Don't copy, transform.

**Thinking in objects-with-methods instead of data-with-operations:**
- **Mistake:** Attaching functions to data structures like methods
- **Fix:** Separate data from operations. Data is passive, functions transform it
</from_oop_background>

<from_imperative_background>
**From Imperative Programming:**

**Writing procedural code with assignments:**
- **Mistake:** Translating imperative loops line-by-line with let-bindings that shadow
- **Fix:** Express as data transformations (map/filter/reduce) or recursion

**Forcing sequential thinking onto parallel operations:**
- **Mistake:** Sequential pipelines when operations are independent
- **Fix:** Recognize opportunities for parallelism. Pure functions enable safe parallel execution

**Using loops instead of collection operations:**
- **Mistake:** Explicit for/while loops instead of map/filter/reduce
- **Fix:** Express intent declaratively. "Find all X where P" not "loop, test, accumulate"

**Early returns and breaks:**
- **Mistake:** Trying to exit early from recursive functions
- **Fix:** Structure recursion to naturally terminate. Use predicates to express conditions

**Not thinking about referential transparency:**
- **Mistake:** Functions with side effects, hidden dependencies
- **Fix:** Make dependencies explicit (parameters). Push effects to boundaries

**Mutation creep:**
- **Mistake:** "Just one variable, for efficiency"
- **Fix:** Start pure. Optimize only after profiling shows need. Mutable state is contagious
</from_imperative_background>
</common_mistakes_by_background>

## Language-Specific Notes

When language-specific skills are available, they provide deeper expertise:

- **Clojure** — JVM interop, persistent data structures, Lisp macros, REPL workflow (clojure-programmer skill)
- **Racket** — Scheme concepts, macros, language-oriented programming (racket-programmer skill)
- **Haskell** — Type classes, lazy evaluation, monads, purely functional
- **Erlang/Elixir** — Actor model, fault tolerance, OTP framework
- **OCaml/F#** — Module system, object-functional hybrid
- **JavaScript/TypeScript** — Functional patterns in imperative language
- **Java** — Streams, lambdas, functional interfaces (java-programmer skill)
- **Python** — Comprehensions, itertools, functools (python-programmer skill)

Use language-specific skills when available for idiomatic guidance.

## Summary

Functional programming emphasizes:
- **Immutability** — Data doesn't change
- **Pure functions** — No side effects
- **Composition** — Build complex from simple
- **Declarative style** — Express what, not how

Apply FP where it improves code clarity, correctness, and maintainability. Balance functional purity with practical concerns. Use FP as one tool in your programming toolkit, not a dogmatic requirement.
