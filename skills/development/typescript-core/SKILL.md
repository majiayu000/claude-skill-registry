---
name: typescript-core
description: Comprehensive TypeScript development guidance covering configuration, type safety, architectural patterns, and best practices. Use when working with TypeScript codebases for (1) TypeScript configuration and setup (tsconfig.json, strict mode), (2) Type definitions and patterns (utility types, type-safe approaches), (3) Resolving TypeScript compilation errors, (4) Applying TypeScript best practices (project structure, error handling, package selection). Automatically triggered when working in .ts/.tsx files or addressing TypeScript-specific queries.
---

# TypeScript Core

Comprehensive guidance for TypeScript development with strict type safety, functional patterns, and modern tooling.

## Core Principles

Follow these fundamental principles in all TypeScript work:

1. **TypeScript Only (Strict Mode)** - Always enable strict mode and all type-checking flags
2. **Simplicity First (KISS + YAGNI)** - Do the simplest thing that works, avoid speculative architecture
3. **Type Safety** - Use Result/Effect types instead of throwing exceptions
4. **Functional Patterns** - Prefer composition, immutability, and pure functions
5. **User Experience First** - Clear error messages, predictable behavior

See [principles.md](references/principles.md) for detailed guidance.

## Quick Start

### Setting Up a New TypeScript Project

1. **Choose the appropriate tsconfig template** based on project type:
   - Node.js backend → [assets/tsconfig-templates/strict-node.json](assets/tsconfig-templates/strict-node.json)
   - React frontend → [assets/tsconfig-templates/strict-react.json](assets/tsconfig-templates/strict-react.json)
   - Library/Package → [assets/tsconfig-templates/library.json](assets/tsconfig-templates/library.json)
   - Monorepo → [assets/tsconfig-templates/monorepo-base.json](assets/tsconfig-templates/monorepo-base.json)

2. **Install required dependencies** - Always use the latest versions with `pnpm`:
   ```bash
   pnpm add -D typescript @types/node
   pnpm add effect zod true-myth @logtape/logtape
   ```

3. **Configure strict linting** - See [strict-configuration.md](references/strict-configuration.md) for ESLint and Prettier setup

4. **Organize project structure** - Follow feature-oriented layout from [project-structure.md](references/project-structure.md)

### Resolving TypeScript Errors

When encountering TypeScript compilation errors:

1. **Read the full error message** - Includes file, line, and often helpful suggestions
2. **Check [common-errors.md](references/common-errors.md)** - Quick solutions for frequent errors
3. **Verify strict mode configuration** - Ensure all flags from [strict-configuration.md](references/strict-configuration.md) are enabled
4. **Use type utilities** - See [type-utilities.md](references/type-utilities.md) for built-in helpers

## TypeScript Configuration

All projects must use strict TypeScript configuration to catch errors early and maintain code quality.

**Key requirements:**
- Enable `strict: true` (includes all strict type-checking options)
- Enable `noUncheckedIndexedAccess: true` (not in strict by default, prevents undefined array access issues)
- Use latest TypeScript version
- Zero compiler errors or warnings before commit

See [strict-configuration.md](references/strict-configuration.md) for complete tsconfig.json and ESLint setup.

## Type Safety & Patterns

### Handling Nullable Values

Prefer True Myth's `Maybe` type over null/undefined:

```ts
import Maybe from 'true-myth/maybe';

// Instead of: User | null
function findUser(id: string): Maybe<User> {
  const user = db.findById(id);
  return Maybe.of(user);
}

// Use with chaining
const userName = findUser("123")
  .map(user => user.name)
  .unwrapOr("Unknown");
```

### Handling Errors

Use `Result` types instead of throwing exceptions:

```ts
import Result from 'true-myth/result';

// Instead of throwing
function parseConfig(data: string): Result<Config, ParseError> {
  try {
    const parsed = JSON.parse(data);
    return Result.ok(parsed);
  } catch (e) {
    return Result.err(new ParseError("Invalid JSON", e));
  }
}

// Use with pattern matching
parseConfig(data)
  .match({
    Ok: config => console.log("Config loaded:", config),
    Err: error => console.error("Parse failed:", error)
  });
```

For complex async operations, prefer Effect over raw Promises - See [error-handling.md](references/error-handling.md) for complete strategy.

### TypeScript Utility Types

Leverage built-in utility types for type transformations:

- `Partial<T>` - Make all properties optional (partial updates)
- `Required<T>` - Make all properties required
- `Pick<T, K>` - Extract specific properties (DTOs, API responses)
- `Omit<T, K>` - Exclude properties (hide sensitive fields)
- `Record<K, V>` - Type-safe dictionaries/maps
- `ReturnType<T>` - Extract function return type
- `Parameters<T>` - Extract function parameter types

See [type-utilities.md](references/type-utilities.md) for comprehensive guide with examples.

## Coding Patterns

### Composition Over Inheritance

Favor composing functionality rather than class hierarchies:

```ts
// Prefer this
const withLogging = <T extends (...args: any[]) => any>(fn: T) => {
  return ((...args: Parameters<T>) => {
    logger.info("Calling function", { args });
    return fn(...args);
  }) as T;
};

// Over this
class LoggableService extends BaseService {
  // ...
}
```

### Railway-Oriented Error Flow

Chain operations with Effect or Result types to handle errors gracefully:

```ts
import { pipe } from 'effect';
import Result from 'true-myth/result';

const result = pipe(
  validateInput(data),
  Result.andThen(processData),
  Result.andThen(saveToDatabase),
  Result.mapErr(err => new ApplicationError("Process failed", err))
);
```

See [patterns.md](references/patterns.md) for complete pattern library including immutability, pattern matching, and concurrency patterns.

## Project Organization

Structure projects by feature, not by technical type:

```
src/
├── features/
│   └── users/
│       ├── components/
│       ├── services/
│       ├── hooks/
│       └── types.ts
├── lib/
│   ├── api/
│   └── utils/
└── state/
```

See [project-structure.md](references/project-structure.md) for complete layouts for web apps, backends, CLIs, and monorepos.

## Package Ecosystem

### Always Use (Standard Toolkit)

These packages are included by default in new projects:

- **Effect** - Functional effect system for async/concurrent operations
- **Zod** - Schema validation at boundaries (API inputs, env vars)
- **True Myth** - `Maybe`/`Result` types for null safety and error handling
- **LogTape** - Structured logging with redaction and integrations
- **Oclif** - CLI framework (for CLI projects)

See [packages-always-use.md](references/packages-always-use.md) for detailed rationale and usage.

### Utility Libraries

Context-specific packages for common needs:

- Date handling, string manipulation, async utilities, etc.
- See [packages-utilities.md](references/packages-utilities.md)

### CLI Tools

For command-line applications:

- Ink (rich TUI), Inquirer (prompts), Ora (spinners), cli-progress
- See [packages-cli.md](references/packages-cli.md)

## Testing

Use Vitest with Testing Library for all tests:

```ts
import { describe, it, expect } from 'vitest';

describe('UserService', () => {
  it('should create user with valid input', () => {
    const result = createUser({ name: "Alice", email: "alice@example.com" });
    expect(result.isOk()).toBe(true);
  });
});
```

See [testing.md](references/testing.md) for complete testing strategy including React component testing, Effect testing, and MSW for API mocking.

## Code Review Standards

Before submitting code:

1. **Zero errors** - `tsc --noEmit` passes with no errors
2. **Zero warnings** - ESLint and Prettier checks pass
3. **Tests pass** - All tests green
4. **Follows patterns** - Uses Result/Maybe, Effect for async, proper error handling
5. **Proper naming** - See [naming.md](references/naming.md) for conventions

See [code-review.md](references/code-review.md) for complete checklist.

## Dependency Management

- **Always use latest versions** - Update dependencies regularly
- **Use pnpm** - Required package manager for all projects
- **Audit security** - Run `pnpm audit` before releases
- **Lock file committed** - `pnpm-lock.yaml` always in version control

See [dependencies.md](references/dependencies.md) for update strategies and security practices.

## Reference Files

**Configuration & Setup:**
- [strict-configuration.md](references/strict-configuration.md) - Complete TypeScript and ESLint configuration
- [project-structure.md](references/project-structure.md) - Directory layouts for different project types
- [dependencies.md](references/dependencies.md) - Dependency management and updates

**Patterns & Practices:**
- [principles.md](references/principles.md) - Core development principles (KISS, YAGNI, UX-first)
- [patterns.md](references/patterns.md) - Code patterns (composition, immutability, railway-oriented)
- [error-handling.md](references/error-handling.md) - Complete error handling strategy
- [naming.md](references/naming.md) - Naming conventions for files, functions, and variables
- [testing.md](references/testing.md) - Testing approaches and best practices
- [code-review.md](references/code-review.md) - Code review standards and checklist

**TypeScript-Specific:**
- [common-errors.md](references/common-errors.md) - Quick solutions for TypeScript compilation errors
- [type-utilities.md](references/type-utilities.md) - Built-in utility types reference

**Packages:**
- [packages-always-use.md](references/packages-always-use.md) - Standard toolkit (Effect, Zod, LogTape, etc.)
- [packages-utilities.md](references/packages-utilities.md) - Utility libraries for specific needs
- [packages-cli.md](references/packages-cli.md) - CLI-specific tooling

## Templates

Pre-configured tsconfig.json files for quick project setup:

- [strict-node.json](assets/tsconfig-templates/strict-node.json) - Node.js backend with strict mode
- [strict-react.json](assets/tsconfig-templates/strict-react.json) - React application with strict mode
- [library.json](assets/tsconfig-templates/library.json) - Library/package configuration
- [monorepo-base.json](assets/tsconfig-templates/monorepo-base.json) - Monorepo base configuration
