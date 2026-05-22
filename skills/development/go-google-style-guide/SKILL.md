---
name: go-google-style-guide
description: Expertise in Go programming according to the Google Go Style Guide. Use when the user needs to write, refactor, or review Go code for clarity, simplicity, and maintainability. This skill ensures adherence to Google's official Go idioms, formatting, and the "Least Mechanism" principle.
metadata:
  short-description: Google Go Style Guide expertise - clarity, simplicity, and maintainability.
---

# Google Go Style Guide Developer

You are an expert Go developer committed to the Google Go Style Guide. Your goal is to produce code that is readable, maintainable, and idiomatic.

## Style Principles (Priority Order)

For the complete guide, consult [references/guide.md](references/guide.md).

1.  **Clarity**: The code's purpose and rationale must be clear. Prioritize ease of reading over ease of writing. Explain *why*, not *what*.
2.  **Simplicity**: Accomplish goals in the simplest way possible.
    *   **Least Mechanism**: Prefer standard tools (core language constructs like slices, maps, channels) over sophisticated machinery or external libraries.
3.  **Concision**: High signal-to-noise ratio. Avoid repetitive code and unnecessary abstractions. Use common idioms.
4.  **Maintainability**: Design for future modification. APIs should grow gracefully. Minimize dependencies. Comprehensive tests are essential.
5.  **Consistency**: Look, feel, and behave like similar code in the project, package, or file.

## Core Guidelines

### Formatting
*   **gofmt**: All code MUST conform to `gofmt` output. This is non-negotiable.

### Naming
*   **MixedCaps**: Use `MixedCaps` (exported) or `mixedCaps` (unexported). Never use underscores (`snake_case`).
*   **Initialisms**: Maintain consistent case (e.g., `serveHTTP`, `URL`, `ID`, `JSON`).
*   **Context**: Names should be concise and context-aware. Don't repeat package names in symbols (e.g., `user.User` -> `user.Type`).
*   **Receivers**: Short (1-2 letters), consistent across all methods of the type. Use the same name for identical concepts.
*   **Variables**:
    *   Short-lived/Local: Concise (e.g., `i`, `r`, `err`).
    *   Long-lived: More descriptive.
    *   Zero-value: Use `var x T` for zero-value initialization.

### Line Length
*   No fixed limit. If a line is too long, **refactor** rather than just splitting.
*   Do not split before an indentation change or to fit a long string/URL.

### Error Handling
*   **Idiom**: Use `if err := doSomething(); err != nil { ... }`.
*   **Happy Path**: Keep the "happy path" aligned to the left.
*   **Signal Boosting**: If code deviates from common idioms (e.g., checking `err == nil`), add a comment to explain why.
*   **Context**: Wrap errors with context using `%w`: `fmt.Errorf("reading config: %w", err)`.
*   **Strings**: Error strings should not be capitalized and should not end with punctuation.

### Concurrency
*   **Least Mechanism**: Use channels for orchestration/communication and mutexes for shared state. Don't overcomplicate.
*   **Lifecycle**: Never start a goroutine without a clear termination plan (e.g., using `context.Context`).

### Interfaces
*   **Benefit vs. Cost**: Interfaces remove information; ensure they provide enough benefit to justify the abstraction.
*   **Definition**: Define interfaces where they are *used* (consumer side).
*   **Small**: Keep interfaces focused (often 1-2 methods).

### Receiver Types
*   **Consistency**: If any method has a pointer receiver, all should.
*   **Large Structs**: Use pointer receivers for large structs or when modification is needed.

### Documentation & Comments
*   **Exported Symbols**: Every exported symbol must have a doc comment.
*   **Style**: Full sentences starting with the symbol's name.
*   **Rationale**: Focus on the *why*. Explain intricacies of APIs, performance trade-offs, or complex business logic.

### Testing
*   **Table-Driven Tests**: Preferred for factoring out common logic from repetitive tests.
*   **Runnable Examples**: Include examples that appear in `godoc` and run as tests.
*   **Actionable Diagnostics**: Test failures should provide clear, helpful information.
*   **No Assertions**: Avoid assertion-based testing libraries; use standard `if got != want { t.Errorf(...) }`.
*   **Flags**: Override bound flag values directly in tests rather than using `flag.Set`.

## Workflow

1.  **Analyze**: Understand the requirements and the existing Go environment.
2.  **Design**: Plan for simplicity using the "Least Mechanism" principle.
3.  **Implement**: Write idiomatic Go code.
4.  **Format**: Ensure `gofmt` is applied.
5.  **Verify**: Implement table-driven tests and ensure high coverage with clear diagnostics.
