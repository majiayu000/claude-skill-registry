---
name: deep-modules
description: Measures module depth, whether the interface is simple relative to the implementation behind it. Use when a module's interface has too many parameters or methods, when there are too many small classes each doing too little or when methods just forward calls to other methods. Not for evaluating whether adjacent layers provide different abstractions (use abstraction-quality) or deciding whether to merge/split specific modules (use module-boundaries).
argument-hint: "[file or module path]"
metadata:
  allowed-tools: Read, Grep
---

# Deep Modules Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file or module. Read the target code first, then apply the checks below.

Evaluate whether modules provide powerful functionality through simple interfaces.

## When to Apply

- Reviewing a new class, module, or API design
- When a module feels like it "doesn't do enough" or has too many parameters
- When you see many small classes collaborating to do one thing
- When a method signature closely mirrors what it calls
- During refactoring to decide what to merge or deepen

## Core Principles

### The Depth Principle

Every module gives functionality and costs knowledge (in the form of an interface). Deep modules give a lot and ask for very little, delivering the highest return on interface cost.

The deepest possible module can even have no interface at all. Garbage collection is the classic example: it does enormously complex work that callers never think about.

Importantly, interfaces are also bigger than they look. The visible part is the **formal** interface: signatures, types, and exceptions. The invisible part is the **informal** interface: ordering rules, side effects, performance characteristics, and thread safety assumptions. The informal interface is usually larger and more dangerous. When the invisible part goes undocumented, callers end up with dependencies they don't know exist, creating new unknown unknowns.

### The Depth Test

For each module under review:

1. How many things must a caller know to use this correctly?
2. How much work does the module do behind that interface?
3. Could a caller skip this module and do the work directly with similar effort?

If #3 is "yes," the module is shallow.

A concrete signal: if the documentation for a method would be longer than its implementation, it is shallow.

### Depth Applies at Every Scale

#### Methods Should Be Deep Too

A method with hundreds of lines is fine if it has a simple signature and does one complete thing. Splitting into shallow pieces can unnecessarily replace one interface with many, increasing the net complexity and cognitive load to understand or maintain. Get the depth right before worrying about code length. Once a method does something useful and complete, shortening it is the easy part.

This directly contradicts the rule from Robert Martin's _Clean Code_ that functions should be split by length alone. Shorter is generally easier to read, but once a function is down to a few dozen lines, further reduction is unlikely to help. The real question is whether splitting reduces the complexity of the _system_, not the function in isolation. If the pieces lose their independence and must be read together, the split made things worse.

#### When Long Methods Are Fine

A method with several sequential blocks is fine as one method if the blocks are relatively independent. If the blocks depend on each other, splitting them makes things harder, not easier. Readers now have to jump between methods to understand what was visible in one place.

### Classitis

One of the most common errors modern developers make is over-decomposing: splitting things into too many small pieces rather than too few large ones. You can often make something deeper by combining closely related things. When unified, they might simplify each other in ways that were invisible when apart.

#### Signs of Classitis:

- Many classes each doing one small thing, requiring callers to compose them
- Class names that are verbs or single operations (Reader, Writer, Parser, Validator as thin wrappers)
- Deep dependency chains where each layer adds minimal abstraction
- Needing 3+ objects to do one logical operation
- Decorator chains where each layer adds one behavior and nineteen pass-throughs

### The Defaults Principle

If nearly every user of a class needs a behavior, that behavior belongs inside the class by default, not in a separate wrapper. Merge related shallow classes into fewer, deeper ones. A class with 500 lines and 3 public methods is better than 5 classes with 100 lines and 15 total public methods. The question is never "is this class too large?" but "does this split reduce the total cognitive load on callers?"

Some modules are unavoidably shallow, like how a linked list class hides very few details behind its interface. These are still useful, but they don't provide much leverage against complexity. Don't mistake "shallow and acceptable" for "deep enough."

### Decorator Alternatives

Before creating a decorator class, consider:

1. Add the functionality directly to the underlying class (if general-purpose or used by most callers)
2. Merge the functionality with the specific use case instead of wrapping
3. Merge with an existing decorator to create one deeper decorator instead of multiple shallow ones
4. Implement as a standalone class independent of the base class

### Pass-Through Method Audit

A pass-through method adds interface cost with zero benefit. The telltale sign is a wrapper class where most public methods just forward to an inner dependency (a membrane, not a layer). If removing the wrapper changes nothing about the caller's experience, the class has no reason to exist.

#### Detection

- Signature closely resembles the method it calls
- Body is mostly a single delegation call
- Removing the method wouldn't lose any logic

#### Fixes (in Order of Preference)

1. Expose the lower-level method directly
2. Redistribute functionality so each layer has a distinct job
3. Merge the classes

#### When Legitimate

Dispatchers that route based on arguments, and multiple implementations of a shared interface and duplicate signatures with meaningfully different behavior.

### Pass-Through Variables

Data threaded through a chain of signatures just to reach one deep method. Each intermediate method must be aware of the variable without using it, and adding a new pass-through variable forces changes to every signature in the chain.

#### Fixes (in Order of Preference)

1. **Shared object**: if an object is already accessible to both the top and bottom methods, store the data there
2. **Context object**: a single object holding cross-cutting state (configuration, shared subsystems, performance counters), with references stored in instance variables via constructors so it doesn't itself become a pass-through argument
3. **Global variable**: avoids pass-through but prevents multiple instances of the system in one process. Generally avoid

Context objects are the most common solution but not ideal. Without discipline they become grab-bags of data that create non-obvious dependencies. Variables in a context should be immutable when possible.

### Interface vs Implementation

If callers see the same structure they'd see without the class, the class isn't hiding anything.

**Shallow** — `config.getString("timeout")`: callers must know the key name, parse the string to a number, and handle missing values themselves. The interface mirrors the internal key-value store.

**Deep** — `config.getTimeout()`: callers get a typed value with defaults already applied. The class absorbs parsing, validation, and key naming so callers don't have to.

### Interface Simplification Tactics

- **Defaults**: Every parameter with a sensible default is one less thing callers must specify. The common case should require no special effort from callers
- **Define errors out of existence**: Every eliminated exception is one less interface element
- **General-purpose design**: Distill to the essential operation. Special cases go in a layer above
- **Pull complexity downwards**: Handle edge cases internally rather than exposing them

## Review Process

1. **List modules**: Identify the classes, functions, or APIs under review
2. **Measure depth**: For each: count interface elements vs. implementation scope
3. **Flag shallow modules**: Any module where interface ~= implementation in complexity
4. **Check for classitis**: Are there clusters of thin classes that should be merged?
5. **Audit pass-throughs**: Are any methods just forwarding calls?
6. **Propose deepening**: For each issue, recommend: merge, absorb, or eliminate

## Relationship to Other Lenses

This skill asks "is the module deep enough?": does the interface justify what's behind it? **abstraction-quality** asks the prior question: "is the abstraction genuine?": does each layer provide a different way of thinking? A module can be deep but sit in a layer that duplicates the abstraction of its neighbor. When adjacent layers look suspiciously similar, hand off to **abstraction-quality**.

Red flag signals for module depth are cataloged in **red-flags** (Shallow Module, Pass-Through Method).
