---
name: doc-generator
description: Generate documentation for code including JSDoc, docstrings, README, and API docs. Use when documenting code, creating README files, or generating API documentation.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Doc Generator

**Version**: 1.0.0
**Purpose**: Generate comprehensive documentation

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Document | "document this", "ドキュメント生成", "add docs" |
| README | "create README", "README作成" |
| API docs | "generate API docs", "API文書" |
| JSDoc | "add JSDoc", "コメント追加" |

---

## Documentation Types

### 1. JSDoc/TSDoc

```typescript
/**
 * Calculates the total price including tax.
 *
 * @param items - Array of items with price property
 * @param taxRate - Tax rate as decimal (e.g., 0.1 for 10%)
 * @returns Total price including tax
 *
 * @example
 * ```ts
 * const total = calculateTotal([{ price: 100 }], 0.1);
 * // Returns: 110
 * ```
 *
 * @throws {Error} If items array is empty
 * @see {@link Item} for item structure
 */
function calculateTotal(items: Item[], taxRate: number): number {
  // implementation
}
```

### 2. Interface Documentation

```typescript
/**
 * Represents a user in the system.
 *
 * @interface User
 * @property {string} id - Unique identifier
 * @property {string} email - User's email address
 * @property {Date} createdAt - Account creation timestamp
 */
interface User {
  id: string;
  email: string;
  createdAt: Date;
}
```

### 3. README Structure

```markdown
# Project Name

> One-line description

[![npm](https://img.shields.io/npm/v/package-name)](https://npmjs.com/package/package-name)
[![License](https://img.shields.io/npm/l/package-name)](LICENSE)

## Features

- Feature 1
- Feature 2

## Installation

\`\`\`bash
npm install package-name
\`\`\`

## Quick Start

\`\`\`typescript
import { something } from 'package-name';

const result = something();
\`\`\`

## API Reference

### `functionName(param)`

Description of function.

**Parameters:**
- `param` (Type) - Description

**Returns:** Type - Description

**Example:**
\`\`\`typescript
const result = functionName('value');
\`\`\`

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| option1 | string | 'default' | Description |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

### 4. CHANGELOG

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-01-15

### Added
- New feature X (#123)

### Changed
- Updated dependency Y

### Fixed
- Bug in Z (#124)

### Deprecated
- Old API method

### Removed
- Legacy code

### Security
- Fixed vulnerability
```

---

## Workflow

### Step 1: Analyze Code

```bash
# Find undocumented functions
grep -r "^export function" src/ | grep -v "/\*\*"
```

### Step 2: Generate Docs

For each function/class:
1. Read implementation
2. Understand purpose
3. Write description
4. Add parameters
5. Add return type
6. Add examples

### Step 3: Verify

```bash
# TypeScript doc check
npx typedoc --validation

# Lint docs
npx eslint --rule 'jsdoc/*' src/
```

---

## Best Practices

### Do

```typescript
/**
 * Validates email format.
 *
 * @param email - Email address to validate
 * @returns True if email is valid
 */
function isValidEmail(email: string): boolean { }
```

### Don't

```typescript
/**
 * This function validates emails.
 * It takes an email parameter.
 * It returns a boolean.
 */
function isValidEmail(email: string): boolean { }
```

---

## Templates

### Function Doc

```typescript
/**
 * [Brief description in imperative mood]
 *
 * [Longer description if needed]
 *
 * @param paramName - [Description]
 * @returns [Description]
 *
 * @example
 * \`\`\`ts
 * [Usage example]
 * \`\`\`
 *
 * @throws {ErrorType} [When this error occurs]
 * @since [version]
 * @deprecated [Use X instead]
 */
```

### Class Doc

```typescript
/**
 * [Brief description]
 *
 * [Longer description]
 *
 * @example
 * \`\`\`ts
 * const instance = new ClassName(options);
 * instance.method();
 * \`\`\`
 */
class ClassName { }
```

---

## Checklist

- [ ] All public APIs documented
- [ ] Examples included
- [ ] Parameters described
- [ ] Return values described
- [ ] Errors documented
- [ ] README is current
- [ ] CHANGELOG updated
