---
name: general-vs-special
description: Evaluates whether interfaces are appropriately general-purpose. Use when the user asks to check interface generality, when a module has if-branches or parameters serving only one caller, when getters/setters expose internal representation, or when an interface is over-specialized. Checks general-purpose design, special-general mixture, and defaults.
argument-hint: "[file or module path]"
metadata:
  allowed-tools: Read, Grep
---

# General vs. Special-Purpose Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file or module. Read the target code first, then apply the checks below.

> "What particularly surprised me is that general-purpose interfaces are simpler and deeper than special-purpose ones." — John Ousterhout, _A Philosophy of Software Design_

General-purpose modules are simpler, deeper and actually less work to build, even when used in only one context. They also produce better information hiding. A general-purpose interface doesn't need to know about specific callers, so knowledge stays where it belongs.

## When to Apply

- Designing a new module, API, or utility
- When a module has use-case-specific logic embedded in it
- When a module's interface is cluttered with rarely-used parameters
- When deciding between a flexible API and a specific one

## Core Principles

### The Generality Test

> "What is the simplest interface that will cover all my current needs?" — John Ousterhout, _A Philosophy of Software Design_

Not "the most general interface possible." The target is **somewhat general-purpose**.

- **Functionality**: Scoped to current needs. Doesn't build features you don't need.
- **Interface**: General enough to support multiple uses. Doesn't tie it only to today's caller.

**A general-purpose interface is usually simpler than a special-purpose one**. Fewer methods means lower cognitive load. Fewer methods per capability is the signal of increasing generality.

Two companion questions:

- **In how many situations will this method be used?** If exactly one, it's over-specialized.
- **Is this API easy to use for my current needs?** If callers must write loops or compose many calls for basic tasks, the abstraction level is wrong.

### Special-General Mixture

Special-purpose code mixed into a general-purpose module makes it shallower. Two forms:

#### At the Interface

Methods or parameters that only serve specific callers. The interface widens, and policy decisions from a higher layer get encoded in a lower one.

#### Inside Method Bodies

Special cases show up as `if` branches in method bodies. The fix is to choose a representation that makes edge cases disappear. A search function that returns null on no match forces every caller to null-check before looping. Return an empty array instead and the `for` loop handles it: zero iterations, zero `if` branches.

> "The best way to do this is by designing the normal case in a way that automatically handles the edge conditions without any extra code." — John Ousterhout, _A Philosophy of Software Design_

### Getters/Setters as Representation Leakage

**Declaring a field `private` then providing `getFoo`/`setFoo` does not constitute information hiding.** The variable's existence, type, and name are fully visible. Callers depend on the representation.

Before writing a getter or setter: should callers know about this property at all? A `rename()` method absorbs related logic and hides the representation. The goal is for the module to do work, not expose data.

### Defaults as a Depth Tool

**Every sensible default is one less decision pushed to callers.** If nearly every user of a class needs a behavior, it belongs inside the class by default.

Gatekeeping question: "Will callers be able to determine a better value than we can determine here?" The answer is usually no.

### The Default Position

When unsure, err on the side of slightly more general. A slightly-too-general interface has unused capabilities (low cost). A slightly-too-special interface requires a rewrite when the second use case arrives (high cost).

But "slightly more general" means one step, not three. Generality should come from simplifying the interface, not from adding parameters.

## Review Process

1. **Identify the general mechanism**: What is the core operation?
2. **Separate special from general**: Is caller-specific logic in the core? Special-case `if` branches that could be eliminated?
3. **Apply the generality test**: Simplest interface that covers all current needs?
4. **Audit getters/setters**: Exposing representation or abstraction?
5. **Review defaults**: Could required parameters become optional?
6. **Recommend**: Push specialization to edges. Deepen with defaults.

Red flag signals for generality are cataloged in **red-flags** (Special-General Mixture, Overexposure).
