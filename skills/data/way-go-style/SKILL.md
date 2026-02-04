---
name: way-go-style
description: Guide for writing idiomatic, effective, and standard Go code. Use this skill when writing, refactoring, or reviewing Go code to ensure adherence to established conventions and best practices.
---

# Way Go Style

## Project Setup (AGENTS.md)

Go projects MUST include this skill's **Way Specific Conventions** in their `AGENTS.md` file to ensure compliance.

1.  **Reference this skill**: Under "Local Skills".
2.  **Copy Conventions**: Copy the **Way Specific Conventions** section below into `AGENTS.md` under "Key Conventions".

## Way Specific Conventions

- **Testing**: Use standard `testing` and `github.com/google/go-cmp/cmp` **only**. No frameworks (Testify, Ginkgo, etc.).
- **Linting**: Run `GolangCI-Lint` v2. Configure via project-specific `.golangci.yml`.
- **Build**: Use `way-magefile` skill.
- **Encore**: Use `encore-go-*` skills. Encore conventions (e.g., globals) take precedence.

## Overview

This skill provides a condensed reference for writing high-quality Go code, synthesizing advice from "Effective Go", Google's "Code Review Comments", and other authoritative sources. It focuses on idiomatic usage, correctness, and maintainability.

## Effective Go Idioms

Critical idioms from [Effective Go](references/effective_go.html).

### Control Flow & Error Handling
- **Defer Evaluation:** Arguments to deferred functions are evaluated **immediately** at the call site (not at execution).
- **Init Scope:** Use `if err := f(); err != nil` to restrict variable scope.
- **Switch:** Use tagless `switch { case condition: ... }` instead of long `if-else` chains.
- **Internal Panic/Recover:** Use `panic` to simplify deep error handling in complex internal code (e.g., parsers), but **always** `recover` at the package boundary to return a standard `error`.

### Types & Interfaces
- **Functional Adapters:** Define methods on function types (e.g., `type MyFunc func()`) to satisfy interfaces. See `http.HandlerFunc`.
- **Interface Verification:** Use a global blank assignment to ensure a type satisfies an interface at compile time: `var _ Interface = (*Type)(nil)`.

## Google Style Decisions & Best Practices

Key decisions from the [Google Go Style Guide](references/google/index.md) and [Code Review Comments](references/CodeReviewComments.md).

### Core Principles
- **Clarity:** "Clear to the reader" is priority #1. Explain *why*, not just *what*.
- **Simplicity:** "Least Mechanism". Prefer core constructs (slices, maps) over complex abstractions.
- **Concision:** High signal-to-noise ratio. Avoid boilerplate.

### Naming & Structure
- **Packages:** Single-word, lowercase (e.g., `task`, not `task_manager`). **Avoid** `util`, `common`.
- **Receivers:** 1-2 letter abbreviations (e.g., `c` for `Client`). **NEVER** use `me`, `this`, `self`.
- **Constants:** Always `MixedCaps` (e.g., `MaxLength`), even if exported. **NEVER** `MAX_LENGTH`.
- **Getters:** `Owner()` (not `GetOwner`).
- **Interfaces:** One-method interfaces -> `Method` + `-er` (e.g., `Reader`). Define in the **consumer** package. Keep them small.

### Functions & Methods
- **Receiver Type:**
  - **Pointer (`*T`):** If mutating, contains `sync.Mutex`, or large struct.
  - **Value (`T`):** Maps, channels, functions, small immutable structs.
  - **Consistency:** Prefer all pointers or all values for a type's methods.
- **Pass Values:** Don't pass pointers to small types (`*string`, `*int`) just to save memory.
- **Synchronous:** Prefer synchronous APIs. Let the caller decide to use goroutines.
- **Must Functions:** `MustXYZ` panic on failure. Use **only** for package-level init or test helpers.

### Error Handling
- **Flow:** Handle errors immediately (`if err != nil { return err }`). Keep "happy path" unindented. Avoid `else`.
- **Structure:** Use `%w` with `fmt.Errorf` to wrap errors for programmatic inspection (`errors.Is`).
- **Panics:** **Never** panic in libraries. Return errors. `log.Fatal` is okay in `main`.
- **Strings:** Lowercase, no punctuation (e.g., `fmt.Errorf("something bad")`) for easy embedding.

### Concurrency
- **Lifetimes:** Never start a goroutine without knowing how it stops.
- **Context:** Always first arg `ctx context.Context`. **Never** store in structs.
- **Copying:** **Do not copy** structs with `sync.Mutex` or `bytes.Buffer`.

### Testing
- **Framework:** Use `testing` package. No assertion libraries (use `cmp` for diffs).
- **Helpers:** Mark setup/teardown functions with `t.Helper()`.
- **Failure Messages:** `YourFunc(%v) = %v, want %v`. (Got before Want).
- **Table-Driven:** Use field names in struct literals for clarity.
- **Subtests:** Use `t.Run()` for clear scope and filtering. Avoid slashes in names.

### Global State & Init
- **Avoid Globals:** Libraries should not rely on package-level vars. Allow clients to instantiate (`New()`).
- **Initialization:** Use `:=` for non-zero values. Use `var t []T` (nil) for empty slices.
- **Imports:** Group order: Stdlib, Project/Vendor, Side-effects (`_`). No `.` imports.

## Practical Go Cheat Sheet

Best practices for maintainable Go from **Dave Cheney's** [Practical Go](references/dave-cheney-practical-go.md).

### Guiding Principles
- **Simplicity, Readability, Productivity:** The core values. Clarity > Brevity.
- **Identifiers:** Choose for clarity. Length proportional to scope/lifespan. Don't include type in name (e.g., `usersMap` -> `users`).

### Design & Structure
- **Package Names:** Name for what it *provides* (e.g., `http`), not what it contains. Avoid `util`, `common`.
- **Project Structure:** Prefer fewer, larger packages. Arrange files by import dependency.
- **API Design:** Hard to misuse. Avoid multiple params of same type. Avoid `nil` params.
- **Interfaces:** Let functions define behavior they require (e.g., take `io.Writer` not `*os.File`).
- **Zero Value:** Make structs useful without explicit initialization (e.g., `sync.Mutex`, `bytes.Buffer`).

### Concurrency & Errors
- **Concurrency:** Leave it to the caller. Never start a goroutine without knowing when/how it stops.
- **Errors:** Eliminate error handling by eliminating errors (e.g., `bufio.Scanner`). Handle errors once (don't log AND return).
- **Return Early:** Use guard clauses. Keep the "happy path" left-aligned.

## Available References

Detailed documentation available in the `references/` directory:

- **[Effective Go](references/effective_go.html):** (HTML) The foundational guide to idiomatic Go.
- **[Code Review Comments](references/CodeReviewComments.md):** Common comments made during Go code reviews at Google.
- **[Google Style Guide](references/google/index.md):** Complete set of Google's Go style documents.
  - [Guide](references/google/guide.md): Core guidelines.
  - [Decisions](references/google/decisions.md): Normative style decisions.
  - [Best Practices](references/google/best-practices.md): Evolving guidance.
- **[Practical Go](references/dave-cheney-practical-go.md):** **Dave Cheney's** advice on writing maintainable Go programs.