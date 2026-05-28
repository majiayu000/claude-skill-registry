---
name: unix-cli
description: UNIX command-line interface guidelines for building tools that follow POSIX conventions, proper exit codes, stream handling, and the UNIX philosophy. This skill should be used when writing, reviewing, or designing CLI tools to ensure they integrate properly with the UNIX tool chain. Triggers on tasks involving CLI tools, command-line arguments, exit codes, stdout/stderr, signals, or shell scripts.
---

# UNIX/POSIX Standards CLI Best Practices

Comprehensive guidelines for building command-line tools that follow UNIX conventions, designed for AI agents and LLMs. Contains 44 rules across 8 categories, prioritized by impact from critical (argument handling, exit codes, output streams) to incremental (configuration and environment).

## When to Apply

Reference these guidelines when:
- Writing new CLI tools in any language
- Parsing command-line arguments and flags
- Deciding what goes to stdout vs stderr
- Choosing appropriate exit codes
- Handling signals like SIGINT and SIGTERM

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Argument & Flag Design | CRITICAL | `args-` |
| 2 | Exit Codes | CRITICAL | `exit-` |
| 3 | Output Streams | CRITICAL | `output-` |
| 4 | Error Handling | HIGH | `error-` |
| 5 | I/O & Composition | HIGH | `io-` |
| 6 | Help & Documentation | MEDIUM-HIGH | `help-` |
| 7 | Signals & Robustness | MEDIUM | `signal-` |
| 8 | Configuration & Environment | MEDIUM | `config-` |

## Quick Reference

### 1. Argument & Flag Design (CRITICAL)

- [`args-use-getopt`](references/args-use-getopt.md) - Use standard argument parsing libraries
- [`args-provide-long-options`](references/args-provide-long-options.md) - Provide long options for all short options
- [`args-support-double-dash`](references/args-support-double-dash.md) - Support double-dash to terminate options
- [`args-require-help-version`](references/args-require-help-version.md) - Implement --help and --version options
- [`args-prefer-flags-over-positional`](references/args-prefer-flags-over-positional.md) - Prefer flags over positional arguments
- [`args-use-standard-flag-names`](references/args-use-standard-flag-names.md) - Use standard flag names
- [`args-never-read-secrets-from-flags`](references/args-never-read-secrets-from-flags.md) - Never read secrets from command-line flags
- [`args-support-option-bundling`](references/args-support-option-bundling.md) - Support option bundling

### 2. Exit Codes (CRITICAL)

- [`exit-zero-for-success`](references/exit-zero-for-success.md) - Return zero for success only
- [`exit-use-standard-codes`](references/exit-use-standard-codes.md) - Use standard exit codes
- [`exit-signal-codes`](references/exit-signal-codes.md) - Use 128+N for signal termination
- [`exit-partial-success`](references/exit-partial-success.md) - Handle partial success consistently
- [`exit-distinguish-error-types`](references/exit-distinguish-error-types.md) - Distinguish error types with different exit codes

### 3. Output Streams (CRITICAL)

- [`output-stdout-for-data`](references/output-stdout-for-data.md) - Write data to stdout only
- [`output-stderr-for-errors`](references/output-stderr-for-errors.md) - Write errors and diagnostics to stderr
- [`output-detect-tty`](references/output-detect-tty.md) - Detect TTY for human-oriented output
- [`output-provide-machine-format`](references/output-provide-machine-format.md) - Provide machine-readable output format
- [`output-line-based-text`](references/output-line-based-text.md) - Use line-based output for text streams
- [`output-respect-no-color`](references/output-respect-no-color.md) - Respect NO_COLOR environment variable

### 4. Error Handling (HIGH)

- [`error-include-program-name`](references/error-include-program-name.md) - Include program name in error messages
- [`error-actionable-messages`](references/error-actionable-messages.md) - Make error messages actionable
- [`error-use-strerror`](references/error-use-strerror.md) - Use strerror for system errors
- [`error-avoid-stack-traces`](references/error-avoid-stack-traces.md) - Avoid stack traces in user-facing errors
- [`error-validate-early`](references/error-validate-early.md) - Validate input early and fail fast

### 5. I/O & Composition (HIGH)

- [`io-support-stdin`](references/io-support-stdin.md) - Support reading from stdin
- [`io-write-to-stdout`](references/io-write-to-stdout.md) - Write output to stdout by default
- [`io-be-stateless`](references/io-be-stateless.md) - Design stateless operations
- [`io-handle-binary-safely`](references/io-handle-binary-safely.md) - Handle binary data safely
- [`io-atomic-writes`](references/io-atomic-writes.md) - Use atomic file writes
- [`io-handle-multiple-files`](references/io-handle-multiple-files.md) - Handle multiple input files consistently

### 6. Help & Documentation (MEDIUM-HIGH)

- [`help-show-usage-on-error`](references/help-show-usage-on-error.md) - Show brief usage on argument errors
- [`help-structure-help-output`](references/help-structure-help-output.md) - Structure help output consistently
- [`help-show-defaults`](references/help-show-defaults.md) - Show default values in help
- [`help-include-examples`](references/help-include-examples.md) - Include practical examples in help
- [`help-version-format`](references/help-version-format.md) - Format version output correctly

### 7. Signals & Robustness (MEDIUM)

- [`signal-handle-sigint`](references/signal-handle-sigint.md) - Handle SIGINT gracefully
- [`signal-handle-sigterm`](references/signal-handle-sigterm.md) - Handle SIGTERM for clean shutdown
- [`signal-handle-sigpipe`](references/signal-handle-sigpipe.md) - Handle SIGPIPE for broken pipes
- [`signal-cleanup-on-second-interrupt`](references/signal-cleanup-on-second-interrupt.md) - Skip cleanup on second interrupt

### 8. Configuration & Environment (MEDIUM)

- [`config-follow-xdg`](references/config-follow-xdg.md) - Follow XDG Base Directory Specification
- [`config-precedence-order`](references/config-precedence-order.md) - Apply configuration in correct precedence order
- [`config-env-naming`](references/config-env-naming.md) - Use consistent environment variable naming
- [`config-never-store-secrets`](references/config-never-store-secrets.md) - Never store secrets in config files or environment
- [`config-respect-standard-vars`](references/config-respect-standard-vars.md) - Respect standard environment variables

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
