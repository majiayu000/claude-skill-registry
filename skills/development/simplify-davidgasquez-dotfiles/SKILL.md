---
name: simplify
description: Refactor code to be simpler while maintaining identical functionality
---

# Simplify

Refactor the given code to make it **simpler, clearer, and more maintainable** without changing what it does.

## Objective

Simplify and clean the code. Implementation should be **straightforward and pragmatic**. The goal is to get the most minimal code possible.

## Principles

- **Behavior parity:** Keep interfaces and semantics identical. No new features. Preserve flags, return codes, and observable side effects.
- **KISS:** Prefer boring, obvious solutions over cleverness. Fewer moving parts > fewer lines.
- **Small pieces:** Favor small, composable functions. Design for easy deletion and iteration.
- **Prune aggressively:** Remove dead code, unused vars, redundant branches, defensive over-engineering, and needless indirection.
- **Flatten flow:** Simplify complex conditionals and deep nesting; use clear guards and early returns.
- **Standard library first:** Replace custom utilities with modern built-ins/framework primitives.
- **Fail early and often:** Don't use blanket try/catch. Skip validations.
- **Communicate with types:** Use types to express contracts and invariants. Avoid type acrobatics and generic abstractions.
- **Abstractions when earned:** Introduce/keep them only if they reduce duplication or isolate likely change.
- **Minimal deps:** Don't add dependencies unless they materially simplify and are commonly available for the target runtime.
- **No micro-optimizations** unless they remove complexity or are explicitly required.
- **Make rules explicit:** Turn hidden assumptions into defaults, parameters, or assertions.
- **Naming for intent:** Prefer clear, intention‑revealing names; one responsibility per function/module.
