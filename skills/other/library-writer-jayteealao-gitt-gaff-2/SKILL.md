---
name: library-writer
description: This skill should be used when writing software libraries, packages, or modules following battle-tested patterns for clean, minimal, production-ready code. It applies when creating new libraries, refactoring existing ones, designing library APIs, or when clean, dependency-minimal library code is needed. Triggers on requests like "create a library", "write a package", "design a module API", or mentions of professional library development.
---

# Library Writer

Write software libraries following battle-tested patterns from the most successful open-source maintainers. These patterns have been proven across hundreds of libraries with billions of downloads.

## Core Philosophy

**Simplicity over cleverness.** Zero or minimal dependencies. Explicit code over metaprogramming. Framework integration without framework coupling. Every pattern serves production use cases.

**The best library is the one you don't have to think about.** It should:
- Install easily
- Configure simply
- Work as expected
- Not break on upgrades
- Have obvious documentation

## Entry Point Structure

Every library follows this pattern:

```
1. Dependencies (stdlib preferred)
2. Internal modules (relative imports)
3. Conditional framework loading (never require frameworks directly)
4. Module with config and errors
```

### Why This Order?

1. **Dependencies first** - Fail fast if deps are missing
2. **Internal modules** - Load library components
3. **Conditional framework** - Don't force framework on non-framework users
4. **Config and errors** - Ready for use immediately

### Conditional Framework Loading

Never require frameworks directly. Check if they exist first:

```
# Only load framework integration if framework is present
if framework_is_loaded:
  load framework_integration

# This allows the library to work:
# - In framework apps (with integration)
# - In plain apps (without framework overhead)
# - In test environments (isolated)
```

See [framework-integration.md](./references/framework-integration.md) for detailed patterns.

## Configuration Pattern

Use simple accessors, not Configuration objects:

```
Good:
  MyLib.api_key = "..."
  MyLib.timeout = 30
  MyLib.logger = custom_logger

Bad:
  MyLib.configure do |config|
    config.api_key = "..."
    config.timeout = 30
    config.logger = custom_logger
  end
```

### Why Simple Accessors?

- Easier to understand (just assignment)
- Can be set from anywhere
- No DSL to learn
- Works with environment variables naturally
- Testable (just set the value)

### Configuration Defaults

Set sensible defaults immediately:

```
Module MyLib:
  timeout = 10           # Reasonable default
  logger = null          # Optional
  api_key = ENV["KEY"]   # From environment
```

See [api-design.md](./references/api-design.md) for API patterns.

## Error Handling

Simple hierarchy with informative messages:

```
Module MyLib:
  class Error (base error)
  class ConfigError (configuration problems)
  class ValidationError (invalid input)
  class ConnectionError (network issues)
```

### Error Design Principles

1. **Inherit from standard error class** - Works with existing error handling
2. **Few error types** - Don't create an error for every situation
3. **Informative messages** - Include what went wrong and how to fix it
4. **Validate early** - Raise ArgumentError on bad input immediately

```
Good error message:
  "API key must be 32 characters, got 16. Set MyLib.api_key or MYLIB_API_KEY environment variable."

Bad error message:
  "Invalid key"
```

## API Design Principles

### Class Macro Pattern

The signature pattern for libraries that enhance classes:

```
Usage:
  class Product:
    searchable(fields: ["name", "description"])

Implementation:
  def searchable(**options):
    validate_options(options)
    store_options(options)
    add_methods()
```

### Single Configuration Method

One method call should configure everything:

```
Good:
  class User:
    authenticatable()  # Adds all auth methods

Bad:
  class User:
    add_password_field()
    add_session_methods()
    add_remember_token()
    configure_encryption()
```

See [api-design.md](./references/api-design.md) for detailed patterns.

## Dependency Management

### Zero Runtime Dependencies (When Possible)

```
Good:
  # Use stdlib for common operations
  # Vendor small utilities if needed
  # No runtime dependencies in manifest

Bad:
  # Dependencies for things stdlib handles
  # Dependencies for "convenience"
  # Dependencies that pull in more dependencies
```

### Development Dependencies

Keep development dependencies separate:

```
Development only:
  - Test framework
  - Linting tools
  - Documentation generators
  - Debug utilities

Never in production:
  - These don't ship with the library
  - Users don't install them
```

### Lock Files

**Never commit lock files in libraries.** Lock files:
- Lock to specific versions you tested with
- Prevent users from getting compatible updates
- Cause conflicts with user's other dependencies

See [module-organization.md](./references/module-organization.md) for structure patterns.

## Testing Philosophy

### Use Standard Test Framework

Every language has a standard test framework. Use it.

```
Python: pytest or unittest
JavaScript: Jest or Vitest
Go: testing stdlib
Rust: built-in test
Ruby: Minitest
```

### What to Test

```
1. Public API - Every public method
2. Edge cases - Empty input, null, large data
3. Error conditions - Invalid input, network failures
4. Configuration - Different config combinations
5. Integration - With frameworks (if applicable)
```

### Test Structure

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Tests with external systems
└── fixtures/       # Test data
```

See [testing-patterns.md](./references/testing-patterns.md) for detailed patterns.

## Anti-Patterns to Avoid

| Pattern | Problem | Alternative |
|---------|---------|-------------|
| Dynamic method generation | Hard to understand, debug | Define methods explicitly |
| Configuration objects | Unnecessary complexity | Simple accessors |
| Tight framework coupling | Limits library usage | Conditional loading |
| Many runtime dependencies | Bloat, conflicts, security | Use stdlib, vendor |
| Heavy DSLs | Learning curve, magic | Explicit method calls |
| Metaprogramming magic | Debugging nightmare | Clear, explicit code |
| Committing lock files | Version conflicts | Let users manage deps |

## Directory Structure

```
my-library/
├── lib/                    # Source code (or src/)
│   ├── my_library.ext      # Entry point
│   ├── my_library/         # Internal modules
│   │   ├── client.ext
│   │   ├── config.ext
│   │   └── errors.ext
│   └── my_library/integrations/  # Framework integrations
│       └── framework.ext
├── tests/                  # Test files
├── README.md               # Documentation
├── LICENSE                 # License file
└── [package manifest]      # package.json, setup.py, etc.
```

See [module-organization.md](./references/module-organization.md) for detailed structure.

## Reference Files

For deeper patterns, see:

| File | Topics |
|------|--------|
| [module-organization.md](./references/module-organization.md) | Directory layouts, file structure, require/import patterns |
| [framework-integration.md](./references/framework-integration.md) | Conditional loading, hooks, lazy initialization |
| [testing-patterns.md](./references/testing-patterns.md) | Multi-version testing, CI setup, fixture patterns |
| [api-design.md](./references/api-design.md) | Public interface design, class macros, configuration |

## Success Criteria

A well-designed library:
- Installs with one command
- Configures with simple assignment
- Works without framework (if applicable)
- Has zero or minimal dependencies
- Uses explicit, readable code
- Tests pass across supported versions
- Documents the public API clearly
- Handles errors informatively
- Doesn't break on upgrades
