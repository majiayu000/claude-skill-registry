---
name: rust-clap
description: Rust Clap CLI argument parsing best practices. This skill should be used when writing, reviewing, or refactoring Rust CLI applications using clap. Triggers on tasks involving argument parsing, CLI design, subcommands, and command-line interfaces in Rust.
---

# Rust Clap Best Practices

Comprehensive best practices guide for building CLI applications in Rust using clap. Contains 42 rules across 8 categories, prioritized by impact to guide CLI design, argument parsing, and testing.

## When to Apply

Reference these guidelines when:
- Designing new Rust CLI applications
- Adding arguments or subcommands to existing CLIs
- Validating and parsing command-line input
- Writing integration tests for CLI tools
- Improving help text and user experience

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Type-Driven Design | CRITICAL | `type-` |
| 2 | Derive API Patterns | CRITICAL | `derive-` |
| 3 | Argument Configuration | HIGH | `arg-` |
| 4 | Validation & Parsing | HIGH | `valid-` |
| 5 | Subcommand Architecture | MEDIUM-HIGH | `subcmd-` |
| 6 | Help & Documentation | MEDIUM | `help-` |
| 7 | Error Handling | MEDIUM | `error-` |
| 8 | Testing Patterns | LOW-MEDIUM | `test-` |

## Quick Reference

### 1. Type-Driven Design (CRITICAL)

- [`type-valueenum-enums`](references/type-valueenum-enums.md) - Use ValueEnum for enumerated arguments
- [`type-option-optional`](references/type-option-optional.md) - Use Option for truly optional arguments
- [`type-pathbuf-files`](references/type-pathbuf-files.md) - Use PathBuf for file system arguments
- [`type-vec-multiple`](references/type-vec-multiple.md) - Use Vec for multiple value arguments
- [`type-newtype-semantic`](references/type-newtype-semantic.md) - Use newtypes for semantic distinction
- [`type-bool-flags`](references/type-bool-flags.md) - Use bool for simple flags

### 2. Derive API Patterns (CRITICAL)

- [`derive-parser-entry`](references/derive-parser-entry.md) - Derive Parser for CLI entry point
- [`derive-command-metadata`](references/derive-command-metadata.md) - Use Command attribute for metadata
- [`derive-subcommand-enum`](references/derive-subcommand-enum.md) - Use Subcommand derive for command hierarchies
- [`derive-args-reusable`](references/derive-args-reusable.md) - Derive Args for reusable argument groups
- [`derive-doc-comments`](references/derive-doc-comments.md) - Use doc comments for help text
- [`derive-global-options`](references/derive-global-options.md) - Use Global for cross-subcommand options
- [`derive-propagate-version`](references/derive-propagate-version.md) - Propagate version to subcommands

### 3. Argument Configuration (HIGH)

- [`arg-default-value`](references/arg-default-value.md) - Use default_value for sensible defaults
- [`arg-env-fallback`](references/arg-env-fallback.md) - Use env for environment variable fallback
- [`arg-short-long`](references/arg-short-long.md) - Provide both short and long option names
- [`arg-conflicts-with`](references/arg-conflicts-with.md) - Use conflicts_with for mutually exclusive options
- [`arg-requires`](references/arg-requires.md) - Use requires for dependent arguments
- [`arg-value-name`](references/arg-value-name.md) - Use value_name for descriptive placeholders

### 4. Validation & Parsing (HIGH)

- [`valid-value-parser`](references/valid-value-parser.md) - Use value_parser for custom validation
- [`valid-possible-values`](references/valid-possible-values.md) - Use PossibleValuesParser for string constraints
- [`valid-fromstr-types`](references/valid-fromstr-types.md) - Implement FromStr for domain types
- [`valid-try-parse`](references/valid-try-parse.md) - Use try_parse for graceful error handling
- [`valid-num-args`](references/valid-num-args.md) - Use num_args for value count constraints

### 5. Subcommand Architecture (MEDIUM-HIGH)

- [`subcmd-nested-hierarchy`](references/subcmd-nested-hierarchy.md) - Use nested subcommands for complex CLIs
- [`subcmd-args-struct`](references/subcmd-args-struct.md) - Use struct for subcommand arguments
- [`subcmd-required-help`](references/subcmd-required-help.md) - Require subcommand or show help
- [`subcmd-arg-groups`](references/subcmd-arg-groups.md) - Use ArgGroup for one-of-many requirements
- [`subcmd-external`](references/subcmd-external.md) - Use external subcommands for plugin systems

### 6. Help & Documentation (MEDIUM)

- [`help-shell-completions`](references/help-shell-completions.md) - Generate shell completions with clap_complete
- [`help-next-heading`](references/help-next-heading.md) - Use next_help_heading for organized help
- [`help-after-help`](references/help-after-help.md) - Use after_help for examples and context
- [`help-hide-options`](references/help-hide-options.md) - Hide advanced options from default help

### 7. Error Handling (MEDIUM)

- [`error-exit-codes`](references/error-exit-codes.md) - Use appropriate exit codes
- [`error-context`](references/error-context.md) - Add context to error messages
- [`error-suggestions`](references/error-suggestions.md) - Enable suggestions for typos
- [`error-color-styles`](references/error-color-styles.md) - Use colored output for error visibility

### 8. Testing Patterns (LOW-MEDIUM)

- [`test-assert-cmd`](references/test-assert-cmd.md) - Use assert_cmd for integration testing
- [`test-predicates`](references/test-predicates.md) - Use predicates for flexible assertions
- [`test-temp-files`](references/test-temp-files.md) - Use assert_fs for temporary test files
- [`test-parse-from`](references/test-parse-from.md) - Use parse_from for unit testing parsers
- [`test-trycmd-snapshots`](references/test-trycmd-snapshots.md) - Use trycmd for snapshot testing

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
