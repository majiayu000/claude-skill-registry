---
name: abstraction-quality
description: Evaluates whether abstractions genuinely provide a fundamentally different way of thinking or are structurally shallow. Use when adjacent layers feel redundant, when decorator/wrapper patterns add boilerplate without depth or when an abstraction feels leaky. Not for measuring a single module's interface-to-implementation ratio (use deep-modules) or checking for information leakage across boundaries (use information-hiding).
argument-hint: "[file or module path]"
metadata:
  allowed-tools: Read, Grep
---

# Abstraction Quality Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file or module. Read the target code first, then apply the checks below.

Evaluate whether abstractions are genuine (hiding complexity) or false (adding layers without reducing what callers must know).

## When to Apply

- Reviewing class hierarchies or layered architectures
- When an abstraction feels like it adds complexity rather than reducing it
- When decorator or wrapper patterns are used
- When two layers seem to operate at the same level of abstraction

## Core Principles

### Genuine vs. False Abstraction Test

**Can callers forget what's underneath?** If yes, it's genuine. If callers must peek through to use it correctly, it's false.

#### Two Ways Abstractions Fail

- **Including unimportant details**: The interface leaks implementation concerns. Shows up as wide interfaces, excessive parameters. More common, at least visible.
- **Omitting important details**: The interface hides something callers need. **More dangerous because it signals nothing.** The abstraction appears clean, inviting trust it doesn't deserve.

A file system can safely hide which disk blocks store data. It cannot hide flush rules for durable storage. Databases depend on that guarantee.

### Different Layer, Different Abstraction

**Each layer should provide a fundamentally different way of thinking about the problem.** If two adjacent layers have similar methods, similar parameters, similar concepts, the layering adds cost without value.

Check: compare the interface of each layer. Are they at different conceptual levels? Or is one just a thin rephrasing of the other?

### Decorator Pattern Trap

**Decorators are structurally committed to shallowness.** A decorator that adds one behavior to a class with twenty methods has nineteen pass-throughs and one meaningful method.

Four alternatives before creating a decorator:

1. Add the functionality directly to the underlying class
2. Merge with the use case
3. Merge with an existing decorator
4. Implement as a standalone class

Ask whether the new functionality really needs to wrap the existing functionality. If not, implement it independently.

### Resolving False Abstractions

When a false abstraction is detected:

1. **Redistribute**: Move functionality between layers so each has a distinct, coherent responsibility
2. **Merge**: Combine adjacent layers into one deeper layer
3. **Expose**: Remove the abstraction. Let callers use the underlying layer directly

## Review Process

1. **Map layers**: Identify the abstraction layers under review
2. **Compare adjacent layers**: Do they provide different mental models?
3. **Test each abstraction**: Can callers forget what's underneath?
4. **Audit decorators/wrappers**: Adding depth or just adding a layer?
5. **Check pass-throughs**: Any methods or variables that just forward without contributing? (See **deep-modules** for pass-through audits, interface-vs-implementation checks, and when signature duplication is legitimate.)
6. **Resolve**: Redistribute, merge, or expose

## Relationship to Other Lenses

This skill asks "is the abstraction genuine?": does each layer provide a different way of thinking? **deep-modules** asks the follow-up: "is the module deep enough?": does the interface justify what's behind it? A layer can provide a genuinely different abstraction and still be shallow. Use this skill first to evaluate layer structure, then **deep-modules** to evaluate depth within each layer.
