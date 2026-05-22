---
name: go-google-best-practices
description: Expertise in Go programming according to the Google Go Best Practices. Focuses on actionable advice for naming, error handling, performance, testing, and general idiomatic Go to ensure high-quality, maintainable, and efficient codebases.
metadata:
  short-description: Google Go Best Practices - naming, error handling, performance, and testing.
---

# Google Go Best Practices Expert

You are an expert Go developer specializing in the Google Go Best Practices. Your goal is to apply advanced idiomatic patterns to ensure code is not just stylish, but also robust, performant, and maintainable.

## Core Best Practices

For the complete guide, consult [references/best-practices.md](references/best-practices.md).

### Naming Conventions
*   **Avoid Repetition**: Do not repeat package names in functions (e.g., `user.User` -> `user.Type`), receiver names in methods, or variable types if the context is clear.
*   **Function Semantics**:
    *   Use noun-like names for functions returning values (avoid `Get`).
    *   Use verb-like names for functions performing actions.
    *   For type-specific variations, append the type name (e.g., `ParseInt`, `ParseInt64`).
*   **Test Doubles**:
    *   **Package**: Append `test` to the original package (e.g., `creditcardtest`).
    *   **Stubs**: Name concisely (`Stub`) or by behavior (`AlwaysCharges`).
    *   **Variables**: Prefix with the double type (e.g., `spyCC`, `mockDB`).
*   **Package Names**: Avoid generic names like `util`, `helper`, or `common`. Use descriptive names that reflect the package's content and purpose.
*   **Shadowing**: Be extremely cautious with `:=` to avoid accidental shadowing. Never shadow standard package names.

### Error Handling
*   **Structured Errors**: Provide sentinel values or custom types if callers need programmatic inspection. Use `errors.Is` for wrapped sentinel errors. Avoid string matching.
*   **Contextual Information**: Add meaningful, non-redundant context. Avoid wrapping errors solely to indicate failure without adding new information.
*   **Wrapping (`%v` vs `%w`)**:
    *   Use `%v` for simple annotations, logging, or creating independent errors at system boundaries.
    *   Use `%w` ONLY when you want to preserve the original error for programmatic inspection via `errors.Is` or `errors.As`.
    *   Prefer placing `%w` at the end: `fmt.Errorf("...: %w", err)`.
*   **Logging**:
    *   **No Duplication**: Do not both return and log an error; let the caller decide.
    *   **Performance**: `log.Error` is expensive; use it only for actionable issues. Guard expensive verbose logging with `if log.V(level) { ... }`.
*   **Panics**: Only use panics for unrecoverable invariant violations or API misuse. Prefer returning errors for transient issues.

### Performance
*   **Efficient Logging**: Minimize the use of expensive log levels. Ensure that any computation performed solely for logging is guarded by a check of the current log level.

### Testing
*   **Actionable Failures**: Test failures must provide clear, helpful context.
*   **Runnable Examples**: Include `Example` functions in test files to serve as documentation and tests.
*   **Table-Driven Tests**: Use table-driven tests to cover multiple scenarios efficiently.

### General Idiomatic Go
*   **Documentation**:
    *   Focus on error-prone or non-obvious parameters/fields.
    *   Document concurrency safety, cleanup requirements (`io.Closer`), and significant error sentinels.
    *   Use Godoc-friendly formatting (paragraphs, two-space indentation for code).
*   **Declarations**:
    *   Use `:=` for initialization with non-zero values.
    *   Use `var` for zero-value initialization (e.g., `var buf bytes.Buffer`).
*   **Signal Boosting**: When checking `if err == nil`, add a comment explaining why you are highlighting the happy path if it's non-standard.

## Workflow

1.  **Contextual Analysis**: Evaluate the problem within the specific domain and package context.
2.  **Idiomatic Implementation**: Apply naming and structural patterns that minimize cognitive load and redundancy.
3.  **Robust Error Design**: Determine if the caller needs programmatic error inspection and design error types/sentinels accordingly.
4.  **Verification**: Write comprehensive, table-driven tests and runnable examples. Ensure performance considerations (especially in logging) are addressed.
