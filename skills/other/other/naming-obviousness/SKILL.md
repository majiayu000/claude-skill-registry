---
name: naming-obviousness
description: Reviews naming quality and code obviousness. Use when the user asks to check naming, when names feel vague or imprecise, when something is hard to name (a design signal, not a vocabulary problem), or when code behavior isn't obvious on first read. Applies the isolation test, scope-length principle, and consistency audit.
argument-hint: "[file or module path]"
metadata:
  allowed-tools: Read, Grep
---

# Naming & Obviousness Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file or module. Read the target code first, then apply the checks below.

Names are arguably the most important form of abstraction because a name claims what matters most about an entity. Because names appear at extreme frequency, mediocre names produce systemic complexity that no single example would suggest.

## When to Apply

- Reviewing any code for readability and clarity
- When a variable, method, or class name feels wrong
- When code requires reading the implementation to understand the interface

## Core Principles

### The Isolation Test

Read a name without surrounding context. Does it convey what the entity is?

- **Pass:** `byteCount`, `retryDelayMs`, `userAuthToken`
- **Fail:** `data`, `x`, `process`, `handle`, `item`
- **Context-dependent:** `result` is acceptable for a method's return value but problematic at wider scope

### Precision: The Most Common Failure

Generic names create false mental models because the reader's first assumption goes wrong and the name protects that wrong assumption from being questioned.

| Bad                           | Better                     | Why                                  |
| ----------------------------- | -------------------------- | ------------------------------------ |
| `x` / `y` (pixel coordinates) | `columnIndex` / `rowIndex` | Name what they index, not their axis |
| `connectStatus` (boolean)     | `isConnected`              | Booleans should be predicates        |
| `NULL_ACCOUNT_ID`             | `ACCOUNT_NOT_CREATED`      | Say what it means, not what it is    |

Too specific is also wrong. A parameter named `filename` on a method that accepts any path encodes a false constraint.

Too similar is also wrong. Related entities with near-identical names (`config` vs `configuration`, `authKey` vs `authToken`) force readers to memorize which is which. Names for related things should clarify the relationship, not obscure it.

### Avoid Extra Words

Every word in a name should provide useful information.

| Pattern        | Bad             | Better      | Why                                        |
| -------------- | --------------- | ----------- | ------------------------------------------ |
| Redundant noun | `httpResponse`  | `response`  | Context is already HTTP                    |
| Type-in-name   | `strName`       | `name`      | IDEs make Hungarian notation unnecessary   |
| Class echo     | `User.userName` | `User.name` | Don't repeat the class name in its members |

### Hard-to-Name Diagnostic

When you struggle to find a precise name, the problem is design, not vocabulary.

| Symptom                          | Fix                   |
| -------------------------------- | --------------------- |
| The entity is doing two things   | Split it              |
| The abstraction isn't worked out | Clarify before naming |
| Two concepts have been conflated | Separate them         |

### Scope-Length Principle

Name length should scale with scope distance. `i` in a 3-line loop is clear. `data` at module scope is a defect.

A short name can be precise and still fail at long range because it carries no information when stripped of context. Verbosity doesn't compensate for vagueness. A name needs to be precise enough to create an accurate mental image that survives traveling to the use site.

### Consistency Audit: Three Requirements

1. Always use the common name for the given purpose
2. Never use the common name for anything else
3. Make the purpose narrow enough that all variables with the name have the same behavior

The third requirement is **critical**. One name, two behaviors: the name looks consistent while concealing a semantic split. Short names are especially prone to this: `pk` for a primary key, a public key, or a private key, `e` for error, event, or element. Ambiguous short names across a codebase compound into real confusion.

### Obviousness Check

> "Software should be designed for ease of reading, not ease of writing." — John Ousterhout, _A Philosophy of Software Design_

Code is obvious when a first-time reader's guesses about behavior are correct.

The writer is the worst judge. When a reviewer says something isn't obvious, that's data.

Four recurring patterns that break obviousness:

1. **Event-driven programming**: control flow looks sequential but handlers are invoked indirectly
2. **Generic containers**: `Record<string, unknown>` forces callers to cast and guess what keys exist. A named type would be self-documenting
3. **Mismatched declaration and allocation types**: `Readable` hiding a `Transform` stream with different backpressure behavior
4. **Violated reader expectations**: a `connect()` method that silently starts a background health-check thread

#### Three Strategies (in order)

Reduce information needed (deep modules, information hiding), leverage what readers already know (good names, conventions), present information explicitly (comments).

## Review Process

1. **Scan names**: Read each in isolation. Precise enough?
2. **Check scope-length fit**: Wide-scope names precise? Narrow-scope names brief?
3. **Run consistency audit**: Same concept = same name? Same name = same concept?
4. **Apply hard-to-name diagnostic**: Hard to choose? Investigate the design.
5. **Assess obviousness**: Can a newcomer understand each function without reading its implementation?
6. **Recommend**: Specific renames tied to the isolation test

Red flag signals for naming and obviousness are cataloged in **red-flags** (Vague Name, Hard to Pick Name, Non-obvious Code).
