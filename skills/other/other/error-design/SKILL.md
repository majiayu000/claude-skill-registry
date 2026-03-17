---
name: error-design
description: Reviews error handling strategy and exception design. Use when the user asks to review error handling, when a module throws too many exceptions, or when callers must handle errors they shouldn't need to know about. Applies the "define errors out of existence" principle with a decision tree for exception strategies.
argument-hint: "[file or module path]"
metadata:
  allowed-tools: Read, Grep
---

# Error Design Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file or module. Read the target code first, then apply the checks below.

**Each exception a module throws is an interface element.** The best way to deal with exceptions is to not have them.

> "Exception handling code rarely executes. Bugs can go undetected for a long time, and when the exception handling code is finally needed, there's a good chance that it won't work." — John Ousterhout, _A Philosophy of Software Design_

## The "Too Many Exceptions" Anti-Pattern

Programmers are taught that "the more errors detected, the better," but this leads to an over-defensive style that throws exceptions for anything suspicious. Throwing exceptions is easy. Handling them is hard.

> "Classes with lots of exceptions have complex interfaces, and they are shallower than classes with fewer exceptions." — John Ousterhout, _A Philosophy of Software Design_

## When to Apply

- Reviewing error handling code or exception hierarchies
- When a function has many error cases or throws many exception types
- When callers are burdened with handling errors that rarely occur
- When error handling code is longer than the happy path

## Core Principles

### The Decision Tree

_The four techniques below have no canonical ordering. This tree sequences them by preference for practical use._

For every error condition:

#### 1. Can the error be defined out of existence?

Change the interface so the condition isn't an error. If yes: do this. Always the best option.

#### 2. Can the error be masked?

Handle internally without propagating. If yes: mask if handling is safe and complete.

#### 3. Can the error be aggregated?

Replace many specific exceptions with one general mechanism. If yes: aggregate to reduce interface surface.

#### 4. Must the caller handle it?

Propagate only if the caller genuinely must decide. If the caller can't do anything meaningful: crash.

### Define Errors Out of Existence

**Error conditions follow from how an operation is specified. Change the specification, and the error disappears.**

The general move: instead of "do X" (fails if preconditions aren't met), write "ensure state S" (trivially satisfied if state already holds).

- **Unset variable?** "Delete this variable" (fails if absent) → "ensure this variable no longer exists" (always succeeds)
- **File not found on delete?** Unix `unlink` doesn't "delete a file." It removes a directory entry. Returns success even if processes have the file open.
- **Substring not found?** Python slicing clamps out-of-range indices (no exception, no defensive code). Java's `substring` throws `IndexOutOfBoundsException`, forcing bounds-clamping around a one-line call.

Defining errors out of existence is like a spice: a small amount improves the result but too much ruins the dish. The technique only works when the exception information is genuinely not needed outside the module. A networking module that masked all network exceptions left callers with no way to detect lost messages or failed peers. Those errors needed to be exposed because callers depended on them to build reliable applications.

### Exception Masking

Handle internally without exposing to callers. Valid when:

- The module can recover completely
- Recovery doesn't lose important information
- The masking behavior is part of the module's specification

TCP masks packet loss this way. Before masking, ask whether a developer debugging the system would want to know it happened. If yes, log it. If the loss is irreversible and important, don't mask. Propagate.

### Exception Aggregation

Replace many specific exceptions with fewer general ones handled in one place. Masking absorbs errors low and aggregation catches errors high. Together they produce an hourglass where middle layers have no exception handling at all.

#### Web Server Pattern

Let all `NoSuchParameter` exceptions propagate to the top-level dispatcher where a single handler generates the error response. New handlers automatically work with the system. The same applies to any request-processing loop: catch in one place near the top, abort the current request, clean up and continue.

### Aggregation Through Promotion

Rather than building separate recovery for each failure type, promote smaller failures into a single crash-recovery mechanism. Fewer code paths, more frequently exercised (which surfaces bugs in recovery sooner). Trade-off: promotion increases recovery cost per incident, so it only makes sense when the promoted errors are rare.

### Just Crash

When an error is difficult or impossible to handle and occurs infrequently, the simplest response is to print diagnostic information and abort. Out-of-memory errors fit this pattern because there's not much an application can do and the handler itself may need to allocate memory. The same principle applies anywhere: wrap the operation so it aborts on failure, eliminating exception handling at every call site.

#### Appropriate When

The error is infrequent, recovery is impractical, and the caller can't do anything meaningful.

#### Not Appropriate When

The system's value depends on handling that failure (e.g., a replicated storage system must handle I/O errors, not crash on them).

## Review Process

1. **Inventory exceptions**: List every error case, exception throw, and error return.
2. **Apply the decision tree**: Can each one be defined out? Masked? Aggregated?
3. **Check depth impact**: How many exception types are in the module's interface?
4. **Audit catch blocks**: Are callers doing meaningful work, or just logging and re-throwing?
5. **Evaluate safety**: For any proposed masking, verify nothing important is lost.
6. **Recommend simplification**: Propose specific reductions in error surface.

Red flag signals for error design are cataloged in **red-flags** (Catch-and-Ignore, Overexposure, Shallow Module).
