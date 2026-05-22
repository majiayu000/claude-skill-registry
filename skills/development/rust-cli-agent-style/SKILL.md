---
name: rust-cli-agent-style
description: Coding patterns extracted from OpenAI Codex Rust codebase - a production CLI/agent system with strict error handling, async patterns, and workspace organization
---

# OpenAI Codex Rust CLI Agent Best Practices

This skill teaches you to write Rust code in the style of the OpenAI Codex codebase - a production CLI/agent system with 50 crates and 787 Rust files.

## Key Characteristics

- **Edition 2024** with strict Clippy configuration
- **Zero unwrap/expect** in non-test code (enforced at workspace level)
- **Tokio async runtime** with proper Send + Sync bounds
- **thiserror** for library errors, **anyhow** for application code
- **Flat workspace** structure with centralized dependencies

## When to Apply

Apply this skill when:
- Building CLI tools or agent systems in Rust
- Writing async Rust with Tokio
- Designing Rust workspace organization
- Implementing error handling patterns
- Working on production Rust codebases

## Quick Reference

### Critical Rules (Must Follow)

| Rule | Description |
|------|-------------|
| [err-no-unwrap](references/err-no-unwrap.md) | Never use `unwrap()` in non-test code |
| [err-no-expect](references/err-no-expect.md) | Avoid `expect()` in library code |
| [err-thiserror-domain](references/err-thiserror-domain.md) | Use thiserror for domain errors |
| [err-context-chain](references/err-context-chain.md) | Add context to errors with `.context()` |

### Error Handling

| Rule | Description |
|------|-------------|
| [err-anyhow-application](references/err-anyhow-application.md) | Use anyhow::Result for entry points |
| [err-from-derive](references/err-from-derive.md) | Use #[from] for error conversion |
| [err-transparent](references/err-transparent.md) | Use #[error(transparent)] for wrapped errors |
| [err-structured-variants](references/err-structured-variants.md) | Include relevant data in error variants |
| [err-io-result](references/err-io-result.md) | Use std::io::Result for I/O functions |
| [err-map-err-conversion](references/err-map-err-conversion.md) | Use map_err for error conversion |
| [err-doc-errors](references/err-doc-errors.md) | Document error conditions |

### Organization

| Rule | Description |
|------|-------------|
| [org-workspace-flat](references/org-workspace-flat.md) | Flat workspace with utils subdirectory |
| [org-crate-naming](references/org-crate-naming.md) | kebab-case directories, project prefix |
| [org-module-visibility](references/org-module-visibility.md) | Use pub(crate) for internal APIs |
| [org-test-common-crate](references/org-test-common-crate.md) | Shared test utilities crate |
| [org-integration-tests-suite](references/org-integration-tests-suite.md) | Tests in suite directory |
| [org-feature-modules](references/org-feature-modules.md) | Feature-based module organization |
| [org-handlers-subdir](references/org-handlers-subdir.md) | Handlers in dedicated subdirectory |
| [org-errors-file](references/org-errors-file.md) | Errors in dedicated file |

### Component Patterns

| Rule | Description |
|------|-------------|
| [mod-derive-order](references/mod-derive-order.md) | Consistent derive macro ordering |
| [mod-async-trait-macro](references/mod-async-trait-macro.md) | Use #[async_trait] for async traits |
| [mod-trait-bounds](references/mod-trait-bounds.md) | Send + Sync + 'static for concurrent traits |
| [mod-extension-trait-suffix](references/mod-extension-trait-suffix.md) | Ext suffix for extension traits |
| [mod-builder-pattern](references/mod-builder-pattern.md) | Builder pattern for complex config |
| [mod-type-alias-complex](references/mod-type-alias-complex.md) | Type aliases for complex generics |
| [mod-impl-block-order](references/mod-impl-block-order.md) | Consistent impl block ordering |
| [mod-generic-constraints](references/mod-generic-constraints.md) | Where clauses for complex bounds |
| [mod-newtype-pattern](references/mod-newtype-pattern.md) | Newtypes for type safety |
| [mod-struct-visibility](references/mod-struct-visibility.md) | Private fields with public constructor |
| [mod-serde-rename](references/mod-serde-rename.md) | Serde rename for wire format |
| [mod-jsonschema-derive](references/mod-jsonschema-derive.md) | JsonSchema for API types |

### Naming Conventions

| Rule | Description |
|------|-------------|
| [name-async-no-suffix](references/name-async-no-suffix.md) | No _async suffix for async functions |
| [name-try-prefix-fallible](references/name-try-prefix-fallible.md) | try_ prefix for fallible constructors |
| [name-with-prefix-builder](references/name-with-prefix-builder.md) | with_ prefix for builder methods |
| [name-handler-suffix](references/name-handler-suffix.md) | Handler suffix for handlers |
| [name-error-suffix](references/name-error-suffix.md) | Error suffix for error types |
| [name-result-type-alias](references/name-result-type-alias.md) | Crate-specific Result alias |
| [name-const-env-var](references/name-const-env-var.md) | _ENV_VAR suffix for env constants |
| [name-request-response](references/name-request-response.md) | Request/Response type pairing |
| [name-options-suffix](references/name-options-suffix.md) | Options suffix for config bundles |
| [name-info-suffix](references/name-info-suffix.md) | Info suffix for read-only data |
| [name-provider-suffix](references/name-provider-suffix.md) | Provider suffix for services |
| [name-client-suffix](references/name-client-suffix.md) | Client suffix for API clients |
| [name-manager-suffix](references/name-manager-suffix.md) | Manager suffix for lifecycle mgmt |
| [name-bool-is-prefix](references/name-bool-is-prefix.md) | is_/has_/should_ for booleans |
| [name-plural-collections](references/name-plural-collections.md) | Plural names for collections |

### Style

| Rule | Description |
|------|-------------|
| [style-import-granularity](references/style-import-granularity.md) | One item per use statement |
| [style-deny-stdout](references/style-deny-stdout.md) | Deny stdout/stderr in libraries |
| [style-inline-format-args](references/style-inline-format-args.md) | Inline format arguments |
| [style-module-docs](references/style-module-docs.md) | Module-level documentation |
| [style-expect-reason](references/style-expect-reason.md) | #[expect] with reason for lints |
| [style-cfg-test-module](references/style-cfg-test-module.md) | Unit tests in mod tests |

### Cross-Crate

| Rule | Description |
|------|-------------|
| [cross-workspace-lints](references/cross-workspace-lints.md) | Workspace-level lint config |
| [cross-workspace-deps](references/cross-workspace-deps.md) | Centralized dependency versions |

## Example: Proper Error Handling

```rust
use thiserror::Error;
use anyhow::Context;

// Domain error with thiserror
#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("failed to read config file: {path}")]
    ReadFailed {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },

    #[error(transparent)]
    Parse(#[from] toml::de::Error),
}

// Library function returns domain error
pub fn load_config(path: &Path) -> Result<Config, ConfigError> {
    let content = fs::read_to_string(path)
        .map_err(|source| ConfigError::ReadFailed {
            path: path.to_owned(),
            source,
        })?;
    toml::from_str(&content).map_err(Into::into)
}

// Application code uses anyhow with context
fn main() -> anyhow::Result<()> {
    let config = load_config(Path::new("config.toml"))
        .context("failed to load configuration")?;
    run(config).await
}
```

## Source

Patterns extracted from [OpenAI Codex](https://github.com/openai/codex) (`codex-rs/` subdirectory) - a production Rust codebase with 50 crates and 787 Rust files.
