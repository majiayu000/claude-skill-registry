---
name: rust-systems
description: Rust systems programming patterns and style guide for building reliable systems software. This skill should be used when writing Rust code, especially for systems programming, CLI tools, or performance-critical applications. Covers project organization with Cargo workspaces, module structure, naming conventions (RFC 430), type/trait patterns (Option, builders, associated types), and error handling with thiserror/anyhow.
---

# Rust Systems Programming Best Practices

Comprehensive Rust patterns and style conventions for systems programming, containing 52 rules across 5 categories. Designed for systems programming, CLI tools, and performance-critical applications.

## When to Apply

Reference these guidelines when:
- Writing new Rust code or modules
- Organizing Rust project structure
- Defining custom types, traits, or error handling
- Reviewing Rust code for style consistency
- Building systems tools, CLIs, or daemon processes

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Project Organization | HIGH | `org-` |
| 2 | Module Structure | HIGH | `mod-` |
| 3 | Naming Conventions | HIGH | `name-` |
| 4 | Type & Trait Patterns | HIGH | `type-` |
| 5 | Error Handling | HIGH | `err-` |

## Quick Reference

### 1. Project Organization (HIGH)

- `org-cargo-workspace` - Use Cargo Workspace for Multi-Crate Projects
- `org-directory-naming` - Use snake_case for All Directory Names
- `org-binary-library-separation` - Separate Binary and Library Crates
- `org-feature-domain-grouping` - Group Crates by Feature Domain
- `org-common-crate` - Use Dedicated Common Crate for Shared Utilities
- `org-flat-crate-structure` - Keep Crate Structure Flat

### 2. Module Structure (HIGH)

- `mod-explicit-declarations` - Use Explicit Module Declarations in lib.rs
- `mod-colocated-tests` - Co-locate Tests as test.rs Files
- `mod-submodule-organization` - Use mod.rs for Multi-File Modules
- `mod-types-errors-files` - Separate Types and Errors into Dedicated Files
- `mod-reexport-pattern` - Use pub use for Clean API Re-exports
- `mod-conditional-compilation` - Use cfg Attributes for Conditional Modules

### 3. Naming Conventions (HIGH)

- `name-function-snake-case` - Use snake_case for Functions and Methods
- `name-type-pascal-case` - Use PascalCase for Types
- `name-constant-screaming` - Use SCREAMING_SNAKE_CASE for Constants
- `name-getter-prefix` - Prefix Getter Functions with get_
- `name-boolean-predicates` - Use is_, has_, should_ for Boolean Predicates
- `name-constructor-new` - Use new for Constructors
- `name-conversion-to-from` - Use to_ and from_ for Conversions
- `name-type-suffixes` - Use Descriptive Suffixes for Type Specialization
- `name-field-unit-suffixes` - Include Unit Suffixes in Field Names
- `name-module-snake-case` - Use snake_case for Module Names
- `name-generic-parameters` - Use Descriptive or Single-Letter Generic Parameters
- `name-lifetime-parameters` - Use Single Lowercase Letters for Lifetimes
- `name-test-files` - Name Test Files as test.rs

### 4. Type & Trait Patterns (HIGH)

- `type-option-nullable-fields` - Use Option<T> for Nullable Fields
- `type-standard-derives` - Use Consistent Derive Order for Data Structs
- `type-builder-pattern` - Use Builder Pattern with Method Chaining
- `type-associated-types` - Use Associated Types for Related Type Relationships
- `type-phantom-data` - Use PhantomData for Unused Generic Parameters
- `type-newtype-pattern` - Use Newtype Pattern for Type Safety
- `type-enum-copy-simple` - Derive Copy for Simple Enums
- `type-enum-variants` - Use Enums for Type-Safe Variants
- `type-trait-impl-grouping` - Group Related Trait Implementations Together
- `type-bitflags` - Use bitflags! for Type-Safe Bit Flags
- `type-operator-overload` - Implement Operator Traits for Domain Types
- `type-public-fields` - Use Public Fields for Data Structs
- `type-async-trait` - Use async_trait for Async Trait Methods
- `type-boxed-trait-objects` - Use Box<dyn Trait> for Runtime Polymorphism
- `type-type-aliases` - Use Type Aliases for Complex Generics

### 5. Error Handling (HIGH)

- `err-thiserror-enum` - Use thiserror for Custom Error Types
- `err-result-alias` - Define Module-Local Result Type Alias
- `err-path-context` - Include Path Context in IO Errors
- `err-anyhow-context` - Use context() and with_context() for Error Messages
- `err-bail-validation` - Use bail! for Validation Failures
- `err-graceful-degradation` - Use Graceful Degradation for Non-Critical Operations
- `err-panic-unrecoverable` - Reserve panic! for Unrecoverable Situations
- `err-expect-message` - Use expect() with Descriptive Messages
- `err-source-attribute` - Use #[source] for Error Chaining
- `err-ok-or-else` - Use ok_or_else for Expensive Error Construction
- `err-two-tier-strategy` - Use Two-Tier Error Strategy

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Full Compiled Document

For the complete guide with all rules expanded: [AGENTS.md](AGENTS.md)
