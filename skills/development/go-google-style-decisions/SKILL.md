---
name: go-google-style-decisions
description: Expertise in Go programming decisions according to the Google Go Style Guide. Focuses on specific choices for naming, error handling, and language usage.
metadata:
  short-description: Google Go Style Decisions for idiomatic and consistent code.
---

# go-google-style-decisions

This skill provides expert guidance on the "Decisions" portion of the Google Go Style Guide. It focuses on the specific choices and trade-offs made to ensure consistency, readability, and maintainability across large Go codebases.

## Core Mandates

1.  **Clarity over Conciseness**: While Go favors brevity, never sacrifice clarity.
2.  **Consistency is Key**: Adhere to established patterns in the codebase.
3.  **Idiomaticity**: Follow Go-specific patterns (e.g., error handling, interface usage).
4.  **No Underscores**: Avoid underscores in names except in specifically allowed cases (tests, generated code).

## Developer Workflow

1.  **Design**: Plan APIs following the "Least Mechanism" principle.
2.  **Implement**: Write code adhering to the style decisions detailed below.
3.  **Lint**: Use `golangci-lint` or `go vet` to catch common style violations.
4.  **Test**: Include runnable examples in `_test.go` files for public APIs.
5.  **Review**: Ensure changes align with the "Core Principles" of clarity and consistency.

## Detailed Guidance

For the complete guide, consult [references/decisions.md](references/decisions.md).

### 1. Naming Conventions

*   **Underscores**: Do not use underscores in Go names (e.g., `pkg_name` or `var_name`).
    *   *Exceptions*: `_test.go` files, generated code, and low-level interop.
*   **Package Names**:
    *   Short, lowercase, single word. No `util` or `common`.
    *   Avoid common variable names (e.g., `user` as a package name if `user` is a common variable).
*   **Receiver Names**:
    *   Short (1-2 letters).
    *   Consistently used throughout the type's methods.
    *   Usually an abbreviation of the type (e.g., `c` for `Client`).
*   **Constant Names**:
    *   Use `MixedCaps` (e.g., `ExportedConst`, `internalConst`).
    *   Do NOT use `ALL_CAPS` or `kPrefix`.
*   **Initialisms**:
    *   Maintain consistent casing (e.g., `HTTPClient`, `urlPath`, `XMLParser`).
*   **Getters**:
    *   Omit `Get` prefix (e.g., use `obj.Field()` instead of `obj.GetField()`).
    *   Use `Get` only if the method is truly "getting" something that isn't a simple field (e.g., `GetURL`).
*   **Variable Names**:
    *   Length should be proportional to scope. Short names for small scopes (e.g., `i` in a loop), more descriptive names for larger scopes.
    *   Omit types from names (e.g., `users` instead of `userSlice`).

### 2. Commentary

*   **Line Length**: Aim for ~80 characters. Wrap long comments.
*   **Doc Comments**: Every top-level exported name MUST have a doc comment.
    *   Must start with the name of the object.
    *   Must be a complete sentence.
*   **Examples**: Provide `ExampleXxx` functions in test files to document public APIs.

### 3. Error Handling

*   **Error as Last Return**: Always return `error` as the final value.
*   **Returning Nil**: Return `nil` for the error value on success.
*   **Error Interfaces**: Exported functions should return the `error` interface, not a concrete type.
*   **Error Strings**:
    *   No capitalization (unless proper nouns/acronyms).
    *   No trailing punctuation.
*   **Indentation**: Handle errors early and return/continue. Keep the "happy path" at the minimal level of indentation.
*   **No In-band Errors**: Do not use special values (like `-1`) to signal errors. Use `(value, error)` or `(value, ok)`.

### 4. Language Constructs

*   **Composite Literals**: Use them for struct initialization. Always specify field names when the struct is from another package.
*   **Nil Slices**: Prefer `var s []int` (nil slice) over `s := []int{}` (empty slice).
    *   Avoid APIs that distinguish between nil and empty slices.
*   **Braces**:
    *   Closing braces should align with the opening statement.
    *   Avoid "cuddling" (e.g., `if err != nil { ... } else { ... }` is fine, but don't over-compact).
*   **Function Formatting**: Keep signatures on one line if possible. If they must wrap, indent the arguments.

### 5. Panic and Recovery

*   **Avoid Panic**: Do not use `panic` for normal error handling.
*   **Exceptional Only**: Use `panic` only for truly unrecoverable states (e.g., internal invariant failure).
*   **Program Termination**: Use `log.Exit` or `log.Fatal` (which calls `os.Exit`) only in `main` or `init` functions.
*   **MustXYZ**: Helper functions that terminate the program on failure should be prefixed with `Must` (e.g., `template.Must`).

### 6. Copying

*   **Structs with Locks**: Be extremely careful copying structs that contain `sync.Mutex` or other synchronization primitives.
*   **Pointer Receivers**: If a type has methods with pointer receivers, avoid copying values of that type.

## References

*   [Google Go Style Decisions](https://google.github.io/styleguide/go/decisions)