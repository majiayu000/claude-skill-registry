---
name: meta-library-dev
description: Develop reusable library code across languages. Use when designing public APIs, organizing modules, managing versioning, or creating utility libraries. Provides foundational patterns that language-specific *-lib-* skills extend.
---

# Library Development Patterns

Foundational patterns for developing reusable library code across programming languages. This meta-skill provides guidance that language-specific library skills (e.g., `rust-lib-dev`, `python-lib-dev`) extend.

## When to Use This Skill

- Designing library public APIs
- Organizing modules and package structure
- Managing semantic versioning and compatibility
- Creating utility libraries, frameworks, or toolkits
- Establishing documentation and testing standards for libraries
- Publishing and distributing packages

## This Skill Does NOT Cover

- SDK development (wrapping APIs/services) - see `meta-sdk-patterns-eng`
- Application architecture - see `architecture-patterns`
- Language-specific implementation details - see `*-lib-*` skills
- CLI tool development - see `*-cli-*` skills

---

## Library vs SDK: Key Distinctions

| Aspect | Library | SDK |
|--------|---------|-----|
| **Purpose** | Reusable functionality | API/service wrapper |
| **Dependencies** | Minimal, self-contained | Tied to external service |
| **Versioning** | Independent semver | Often tracks API version |
| **Examples** | lodash, requests, serde | AWS SDK, Stripe SDK |
| **Testing** | Unit/integration tests | Mocks external service |

---

## Public API Design

### Principle: Minimal Surface Area

Expose only what users need. Everything public becomes a maintenance commitment.

```
Good: 3-5 primary exports that compose
Bad: 50 exports that users must navigate
```

### Export Patterns

**Layered Exports:**
```
library/
├── mod.rs (or index.ts, __init__.py)  # Primary public API
├── types.rs                            # Public types/interfaces
├── errors.rs                           # Error types
└── internal/                           # Private implementation
    └── ...
```

**Explicit vs Glob Exports:**
```python
# Preferred: Explicit exports
from .core import parse, validate, transform
__all__ = ["parse", "validate", "transform"]

# Avoid: Glob re-exports (hides what's public)
from .core import *
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| **Functions** | Verb-first, descriptive | `parse_json`, `validateInput` |
| **Types/Classes** | Noun, singular | `Parser`, `ValidationResult` |
| **Constants** | SCREAMING_SNAKE | `DEFAULT_TIMEOUT`, `MAX_RETRIES` |
| **Modules** | Lowercase, descriptive | `parser`, `validators` |

### Function Signatures

**Prefer Specific Over Generic:**
```rust
// Good: Clear intent
fn parse_config(path: &Path) -> Result<Config, ParseError>

// Avoid: Too generic, unclear
fn parse(input: &str) -> Result<Value, Error>
```

**Parameter Guidelines:**
- 0-3 parameters: Use positional
- 4+ parameters: Use options object/struct
- Required first, optional last
- Sensible defaults for optional parameters

```typescript
// Good: Options object for many parameters
interface ParseOptions {
  encoding?: string;
  strict?: boolean;
  maxDepth?: number;
}
function parse(input: string, options?: ParseOptions): Result

// Avoid: Too many positional parameters
function parse(input: string, encoding: string, strict: boolean, maxDepth: number): Result
```

---

## Module Organization

### Standard Structure

```
library/
├── src/
│   ├── lib.rs           # Rust: Library root
│   ├── index.ts         # TS: Package entry
│   ├── __init__.py      # Python: Package init
│   │
│   ├── core/            # Core functionality
│   │   ├── mod.rs
│   │   ├── parser.rs
│   │   └── validator.rs
│   │
│   ├── types/           # Type definitions
│   │   ├── mod.rs
│   │   └── config.rs
│   │
│   ├── errors/          # Error types
│   │   ├── mod.rs
│   │   └── parse_error.rs
│   │
│   └── utils/           # Internal utilities
│       └── ...
│
├── tests/               # Integration tests
├── examples/            # Usage examples
├── benches/             # Benchmarks (if applicable)
└── docs/                # Additional documentation
```

### Module Cohesion Principles

**High Cohesion:**
- Modules should do one thing well
- Related functionality stays together
- Clear boundaries between modules

**Low Coupling:**
- Modules should be independently testable
- Minimize cross-module dependencies
- Use dependency injection for flexibility

### Re-export Patterns

**Facade Pattern for Complex Libraries:**
```rust
// lib.rs - Clean public interface
pub use crate::core::{parse, validate};
pub use crate::types::{Config, Result};
pub use crate::errors::ParseError;

// Internal modules hidden
mod core;
mod types;
mod errors;
mod utils;  // Not re-exported
```

---

## Versioning Strategy

### Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)
```

### What Constitutes Breaking Changes?

| Change Type | Breaking? | Version Bump |
|-------------|-----------|--------------|
| Remove public function | Yes | MAJOR |
| Change function signature | Yes | MAJOR |
| Add required parameter | Yes | MAJOR |
| Add optional parameter | No | MINOR |
| Add new function | No | MINOR |
| Fix bug in existing behavior | No | PATCH |
| Performance improvement | No | PATCH |

### Pre-release Versions

```
0.x.y  - Initial development (breaking changes allowed in minor)
1.0.0-alpha.1 - Alpha release
1.0.0-beta.1  - Beta release
1.0.0-rc.1    - Release candidate
1.0.0         - Stable release
```

### Deprecation Process

1. **Announce deprecation** with `@deprecated` annotation
2. **Document migration path** in deprecation notice
3. **Maintain deprecated API** for at least one minor version
4. **Remove in next major version**

```python
import warnings

def old_function():
    """
    .. deprecated:: 2.0.0
       Use :func:`new_function` instead.
    """
    warnings.warn(
        "old_function is deprecated, use new_function instead",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function()
```

---

## Error Handling

### Error Type Design

**Hierarchical Error Types:**
```rust
#[derive(Debug, thiserror::Error)]
pub enum LibraryError {
    #[error("Parse error: {0}")]
    Parse(#[from] ParseError),

    #[error("Validation error: {0}")]
    Validation(#[from] ValidationError),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

#[derive(Debug, thiserror::Error)]
pub enum ParseError {
    #[error("Invalid syntax at line {line}: {message}")]
    InvalidSyntax { line: usize, message: String },

    #[error("Unexpected token: {0}")]
    UnexpectedToken(String),
}
```

### Error Messages

**Good Error Messages Include:**
- What happened
- Where it happened (context)
- How to fix it (when possible)

```
# Good
ParseError: Invalid JSON at line 42: expected ',' or '}' after object property

# Bad
Error: Parse failed
```

### Result Types

**Prefer Result Types Over Exceptions (where language supports):**
```rust
// Rust: Result type
pub fn parse(input: &str) -> Result<Document, ParseError>

// TypeScript: Discriminated union
type ParseResult =
  | { success: true; data: Document }
  | { success: false; error: ParseError };
```

---

## Configuration Patterns

### Configuration Hierarchy

```
1. Defaults (in code)
2. Config file
3. Environment variables
4. Explicit parameters
```

### Builder Pattern for Configuration

```rust
let config = ConfigBuilder::new()
    .timeout(Duration::from_secs(30))
    .max_retries(3)
    .strict_mode(true)
    .build()?;
```

### Validation at Construction

```python
@dataclass
class Config:
    timeout: int
    max_retries: int

    def __post_init__(self):
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative")
```

---

## Testing Strategies

### Test Pyramid for Libraries

```
         /\
        /  \     E2E (examples work)
       /----\
      /      \   Integration (modules work together)
     /--------\
    /          \ Unit (individual functions work)
   --------------
```

### Testing Patterns

**Property-Based Testing:**
```rust
#[quickcheck]
fn parse_roundtrip(input: ValidJson) -> bool {
    let parsed = parse(&input.0)?;
    let serialized = serialize(&parsed);
    input.0 == serialized
}
```

**Snapshot Testing:**
```javascript
test('parser output', () => {
  const result = parse(complexInput);
  expect(result).toMatchSnapshot();
});
```

**Fuzz Testing:**
```rust
#[fuzz]
fn fuzz_parser(data: &[u8]) {
    // Should not panic on any input
    let _ = parse(data);
}
```

### Example-Driven Testing

```python
def parse_date(s: str) -> date:
    """Parse a date string.

    Examples:
        >>> parse_date("2024-01-15")
        date(2024, 1, 15)

        >>> parse_date("invalid")
        Traceback (most recent call last):
            ...
        ValueError: Invalid date format
    """
```

---

## Documentation Standards

### Documentation Hierarchy

```
README.md          # Quick start, installation
docs/
├── guide/         # Tutorials, how-tos
├── reference/     # API documentation
└── examples/      # Runnable examples
```

### API Documentation Requirements

Every public item needs:
1. **Summary** - One-line description
2. **Description** - Detailed explanation (if needed)
3. **Parameters** - Each parameter documented
4. **Returns** - Return value documented
5. **Errors** - Possible errors documented
6. **Examples** - At least one usage example

```rust
/// Parses a configuration file into a Config struct.
///
/// Reads the file at the given path and parses it as TOML format.
/// The file must exist and be valid UTF-8.
///
/// # Arguments
///
/// * `path` - Path to the configuration file
///
/// # Returns
///
/// A `Config` struct containing the parsed configuration.
///
/// # Errors
///
/// Returns `ParseError::Io` if the file cannot be read.
/// Returns `ParseError::InvalidSyntax` if the TOML is malformed.
///
/// # Examples
///
/// ```
/// let config = parse_config("config.toml")?;
/// assert_eq!(config.timeout, 30);
/// ```
pub fn parse_config(path: &Path) -> Result<Config, ParseError> {
    // ...
}
```

### README Template

```markdown
# Library Name

Brief description of what the library does.

## Installation

\`\`\`bash
# Package manager command
\`\`\`

## Quick Start

\`\`\`language
// Minimal working example
\`\`\`

## Features

- Feature 1
- Feature 2
- Feature 3

## Documentation

- [Guide](docs/guide/)
- [API Reference](docs/reference/)
- [Examples](examples/)

## License

[License type]
```

---

## Compatibility Considerations

### Minimum Supported Version

**Document and test against minimum versions:**
```toml
# Cargo.toml
rust-version = "1.70"

# pyproject.toml
requires-python = ">=3.9"

# package.json
"engines": {
  "node": ">=18.0.0"
}
```

### Feature Flags

**Use feature flags for optional functionality:**
```toml
# Cargo.toml
[features]
default = ["json"]
json = ["serde_json"]
yaml = ["serde_yaml"]
async = ["tokio"]
```

### Backward Compatibility Strategies

1. **Additive changes only** in minor versions
2. **Feature flags** for optional new features
3. **Type aliases** to rename types without breaking
4. **Default parameters** instead of signature changes

---

## Publishing and Distribution

### Pre-publish Checklist

- [ ] Version bumped appropriately
- [ ] CHANGELOG updated
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Examples work with new version
- [ ] No accidental breaking changes
- [ ] License file present
- [ ] README accurate

### Registry-Specific Guidelines

| Registry | Key Requirements |
|----------|------------------|
| **crates.io** | Cargo.toml metadata complete, license |
| **npm** | package.json fields, TypeScript types |
| **PyPI** | pyproject.toml, classifiers, requires-python |
| **Maven** | pom.xml, GPG signing, Javadoc |

### Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

## [Unreleased]

## [2.1.0] - 2024-01-15

### Added
- New `parse_strict` function for strict parsing

### Changed
- Improved error messages for parse failures

### Deprecated
- `parse_loose` is deprecated, use `parse` with `strict: false`

## [2.0.0] - 2024-01-01

### Changed
- **BREAKING**: Renamed `Config` to `Settings`
- **BREAKING**: `parse` now returns `Result` instead of panicking
```

---

## Performance Considerations

### Avoid Premature Optimization

1. **Correctness first** - Make it work
2. **Clarity second** - Make it readable
3. **Performance third** - Make it fast (if needed)

### Common Performance Patterns

**Zero-Copy Where Possible:**
```rust
// Good: Borrow instead of clone
fn process(data: &str) -> Result<&str, Error>

// Avoid: Unnecessary allocation
fn process(data: &str) -> Result<String, Error>
```

**Lazy Evaluation:**
```rust
// Good: Iterator (lazy)
fn items(&self) -> impl Iterator<Item = &Item>

// Avoid: Collect everything (eager)
fn items(&self) -> Vec<Item>
```

**Benchmark Before Optimizing:**
```rust
#[bench]
fn bench_parse(b: &mut Bencher) {
    let input = include_str!("../fixtures/large.json");
    b.iter(|| parse(input));
}
```

---

## Extension Points

### Plugin Architecture

```rust
pub trait Plugin {
    fn name(&self) -> &str;
    fn process(&self, input: &Document) -> Result<Document, Error>;
}

pub struct Library {
    plugins: Vec<Box<dyn Plugin>>,
}

impl Library {
    pub fn register_plugin(&mut self, plugin: impl Plugin + 'static) {
        self.plugins.push(Box::new(plugin));
    }
}
```

### Callback Hooks

```typescript
interface Hooks {
  beforeParse?: (input: string) => string;
  afterParse?: (result: Document) => Document;
  onError?: (error: Error) => void;
}

function parse(input: string, hooks?: Hooks): Document {
  const processed = hooks?.beforeParse?.(input) ?? input;
  // ...
}
```

---

## Anti-Patterns to Avoid

### 1. God Module
**Problem:** Single module with too many responsibilities
**Solution:** Split by domain/functionality

### 2. Leaky Abstractions
**Problem:** Internal implementation details exposed in public API
**Solution:** Clear public/private boundaries

### 3. Unstable Dependencies
**Problem:** Depending on unstable/pre-1.0 libraries in public API
**Solution:** Wrap or re-export with stable types

### 4. Breaking Changes in Patches
**Problem:** Changing behavior in patch releases
**Solution:** Strict semver adherence

### 5. Missing Error Context
**Problem:** Generic errors that don't help debugging
**Solution:** Rich error types with context

### 6. Documentation Drift
**Problem:** Docs out of sync with code
**Solution:** Doc tests, examples in tests

---

## References

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [The Little Manual of API Design](https://people.mpi-inf.mpg.de/~jblanche/api-design.pdf)
- Language-specific: `*-lib-*` skills
- SDK development: `meta-sdk-patterns-eng`
