---
name: shell
description: Shell scripting best practices for writing safe, portable, and maintainable bash/sh scripts (formerly shell-scripts). Use when writing, reviewing, or refactoring shell scripts. Triggers on shell scripts, bash, sh, POSIX, ShellCheck, error handling, quoting, variables.
---

# Shell Scripts Best Practices

Comprehensive best practices guide for shell scripting, designed for AI agents and LLMs. Contains 48 rules across 9 categories, prioritized by impact from critical (safety, portability) to incremental (style). Each rule includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and specific impact metrics.

## When to Apply

Reference these guidelines when:
- Writing new bash or POSIX shell scripts
- Reviewing shell scripts for security vulnerabilities
- Debugging scripts that fail silently or behave unexpectedly
- Porting scripts between Linux, macOS, and containers
- Optimizing shell script performance
- Setting up CI/CD pipelines with shell scripts

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Safety & Security | CRITICAL | `safety-` | 6 |
| 2 | Portability | CRITICAL | `port-` | 5 |
| 3 | Error Handling | HIGH | `err-` | 6 |
| 4 | Variables & Data | HIGH | `var-` | 5 |
| 5 | Quoting & Expansion | MEDIUM-HIGH | `quote-` | 6 |
| 6 | Functions & Structure | MEDIUM | `func-` | 5 |
| 7 | Testing & Conditionals | MEDIUM | `test-` | 5 |
| 8 | Performance | LOW-MEDIUM | `perf-` | 6 |
| 9 | Style & Formatting | LOW | `style-` | 4 |

## Quick Reference

### 1. Safety & Security (CRITICAL)

- [`safety-command-injection`](references/safety-command-injection.md) - Prevent command injection from user input
- [`safety-eval-avoidance`](references/safety-eval-avoidance.md) - Avoid eval for dynamic commands
- [`safety-absolute-paths`](references/safety-absolute-paths.md) - Use absolute paths for external commands
- [`safety-temp-files`](references/safety-temp-files.md) - Create secure temporary files
- [`safety-suid-forbidden`](references/safety-suid-forbidden.md) - Never use SUID/SGID on shell scripts
- [`safety-argument-injection`](references/safety-argument-injection.md) - Prevent argument injection with double dash

### 2. Portability (CRITICAL)

- [`port-shebang-selection`](references/port-shebang-selection.md) - Choose shebang based on portability needs
- [`port-avoid-bashisms`](references/port-avoid-bashisms.md) - Avoid bashisms in POSIX scripts
- [`port-printf-over-echo`](references/port-printf-over-echo.md) - Use printf instead of echo for portability
- [`port-export-syntax`](references/port-export-syntax.md) - Use portable export syntax
- [`port-test-portability`](references/port-test-portability.md) - Use portable test constructs

### 3. Error Handling (HIGH)

- [`err-strict-mode`](references/err-strict-mode.md) - Use strict mode for error detection
- [`err-exit-codes`](references/err-exit-codes.md) - Use meaningful exit codes
- [`err-trap-cleanup`](references/err-trap-cleanup.md) - Use trap for cleanup on exit
- [`err-stderr-messages`](references/err-stderr-messages.md) - Send error messages to stderr
- [`err-pipefail`](references/err-pipefail.md) - Use pipefail to catch pipeline errors
- [`err-check-commands`](references/err-check-commands.md) - Check command success explicitly

### 4. Variables & Data (HIGH)

- [`var-use-arrays`](references/var-use-arrays.md) - Use arrays for lists instead of strings
- [`var-local-scope`](references/var-local-scope.md) - Use local for function variables
- [`var-naming-conventions`](references/var-naming-conventions.md) - Follow variable naming conventions
- [`var-readonly-constants`](references/var-readonly-constants.md) - Use readonly for constants
- [`var-default-values`](references/var-default-values.md) - Use parameter expansion for defaults

### 5. Quoting & Expansion (MEDIUM-HIGH)

- [`quote-always-quote-variables`](references/quote-always-quote-variables.md) - Always quote variable expansions
- [`quote-dollar-at`](references/quote-dollar-at.md) - Use "$@" for argument passing
- [`quote-command-substitution`](references/quote-command-substitution.md) - Quote command substitutions
- [`quote-brace-expansion`](references/quote-brace-expansion.md) - Use braces for variable clarity
- [`quote-here-documents`](references/quote-here-documents.md) - Use here documents for multi-line strings
- [`quote-glob-safety`](references/quote-glob-safety.md) - Control glob expansion explicitly

### 6. Functions & Structure (MEDIUM)

- [`func-main-pattern`](references/func-main-pattern.md) - Use main() function pattern
- [`func-single-purpose`](references/func-single-purpose.md) - Write single-purpose functions
- [`func-return-values`](references/func-return-values.md) - Use return values correctly
- [`func-documentation`](references/func-documentation.md) - Document functions with header comments
- [`func-avoid-aliases`](references/func-avoid-aliases.md) - Prefer functions over aliases

### 7. Testing & Conditionals (MEDIUM)

- [`test-double-brackets`](references/test-double-brackets.md) - Use [[ ]] for tests in bash
- [`test-arithmetic`](references/test-arithmetic.md) - Use (( )) for arithmetic comparisons
- [`test-explicit-empty`](references/test-explicit-empty.md) - Use explicit empty/non-empty string tests
- [`test-file-operators`](references/test-file-operators.md) - Use correct file test operators
- [`test-case-patterns`](references/test-case-patterns.md) - Use case for pattern matching

### 8. Performance (LOW-MEDIUM)

- [`perf-builtins-over-external`](references/perf-builtins-over-external.md) - Use builtins over external commands
- [`perf-avoid-subshells`](references/perf-avoid-subshells.md) - Avoid unnecessary subshells
- [`perf-process-substitution`](references/perf-process-substitution.md) - Use process substitution for temp files
- [`perf-read-files`](references/perf-read-files.md) - Read files efficiently
- [`perf-parameter-expansion`](references/perf-parameter-expansion.md) - Use parameter expansion for string operations
- [`perf-batch-operations`](references/perf-batch-operations.md) - Batch operations instead of loops

### 9. Style & Formatting (LOW)

- [`style-indentation`](references/style-indentation.md) - Use consistent indentation
- [`style-file-structure`](references/style-file-structure.md) - Follow consistent file structure
- [`style-comments`](references/style-comments.md) - Write useful comments
- [`style-shellcheck`](references/style-shellcheck.md) - Use ShellCheck for static analysis

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |

## Key Sources

- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck](https://www.shellcheck.net/)
- [Greg's Wiki (wooledge.org)](https://mywiki.wooledge.org/)
- [POSIX Shell Specification](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
