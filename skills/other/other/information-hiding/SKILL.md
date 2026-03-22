---
name: information-hiding
description: Checks for information leakage across module boundaries. Use when the user asks to check information hiding, when modules seem to change together, when implementation details leak across boundaries, or when structure follows execution order rather than knowledge ownership. Detects temporal decomposition and false encapsulation.
argument-hint: "[file or module path]"
metadata:
  allowed-tools: Read, Grep
---

# Information Hiding Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file or module. Read the target code first, then apply the checks below.

Evaluate whether modules encapsulate design decisions effectively.

## When to Apply

- Reviewing module boundaries or class decomposition decisions
- When multiple modules change together for single-decision changes
- When private fields have matching getters and setters
- When modules are organized around execution steps (read/process/write)
- When a format, protocol, or representation appears in multiple places

## Core Principles

### Knowledge Ownership Test

For every design decision in the code (data format, algorithm choice, protocol, storage representation):

1. Which module owns this decision?
2. Is that ownership exclusive, and no other module knows this?
3. If this decision changes, does only one module need editing?

If #3 is "no," there is information leakage.

### Two Kinds of Leakage

#### Interface Leakage

The decision appears in parameters, return types, or exceptions. Bad, but at least visible and discoverable.

#### Back-Door Leakage

Two or more modules encode the decision in their implementations with nothing in the code surface making the dependency visible. This maps directly to unknown unknowns: a developer modifying one module has no signal the other must change. More pernicious than interface leakage for exactly this reason.

Signs of back-door leakage:

- Changing an internal data structure breaks a seemingly unrelated module
- Two modules must be updated in lockstep but have no direct API dependency
- Shared assumptions about file formats, message ordering, or naming conventions that exist only in developers' heads
- Tests that break in module B when module A's internals change

Not all dependencies are eliminable. Transforming a hidden dependency into an obvious one is often more valuable than trying to remove it. At least then the next developer knows to look.

### The Temporal Decomposition Trap

The most common cause of information leakage is temporal decomposition. When code gets split into a "read the file" step and a "parse the file" step, both modules have to agree on the file format. It's important to draw boundaries around knowledge domains, not execution phases. A module that reads AND writes a format should own the definition of that format exclusively. Merging the two steps actually produces one module with a simpler interface and no shared assumptions. A slightly larger class that hides (i.e. abstracts) more is almost always worth the extra length.

This fails at larger scales too. Microservices split along workflow stages scatter shared protocol knowledge across service boundaries.

### Private Is Not Hiding

Marking a field `private` and providing getters/setters does not actually hide it. Other code still knows the field exists, what it's called, and what type it holds. That is as much exposure as if the field were public.

**Test**: Does the caller need this information to use the module correctly? If no, it should be genuinely invisible, not just access-controlled.

### Partial Hiding Has Value

Information hiding is not all-or-nothing. If a feature is only needed by a few users and accessed through separate methods not visible in common use cases, it is mostly hidden, creating fewer dependencies than information visible to every user. Design for the common case to be simple. Rare cases can require extra methods.

### Hiding Within a Class

Information hiding applies inside a class too, not just at its boundary. Design private methods so each encapsulates some capability hidden from the rest of the class. Minimize the number of places where each instance variable is used. Fewer internal access points means fewer internal dependencies.

### Don't Hide What Callers Need

Information hiding only makes sense when the hidden information isn't needed outside the module. If callers genuinely need something (performance-tuning parameters, configuration that varies by use case), it must be exposed. The goal is to minimize the _amount_ of information needed outside, not to hide everything unconditionally.

### Leakage Through Over-Specialization

When a general-purpose module is given knowledge of specific higher-level operations, information leaks upward. When a general-purpose data layer defines methods like `archiveExpiredItems`, it encodes business-rule knowledge. Any change to the expiration policy forces a data-layer change. This is the special-general mixture red flag.

## Review Process

1. **Inventory design decisions**: List formats, algorithms, protocols, data structures, representation choices
2. **Map ownership**: For each, identify which module(s) know about it
3. **Flag leakage**: Any decision known by more than one module is leaking
4. **Check for temporal decomposition**: Are boundaries drawn around steps or knowledge?
5. **Audit getters/setters**: Are any "private" fields effectively public through accessors?
6. **Propose consolidation**: Merge the knowing modules, or extract shared knowledge into a single owner with a genuinely abstract interface

Red flag signals for information hiding are cataloged in **red-flags** (Information Leakage, Temporal Decomposition, Overexposure).

## References

For deeper coverage, load these on demand:

- [Back-door leakage](references/back-door-leakage.md): Detection patterns for invisible cross-module dependencies
