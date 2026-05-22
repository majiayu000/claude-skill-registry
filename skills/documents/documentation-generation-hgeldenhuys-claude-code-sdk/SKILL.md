---
name: documentation-generation
description: Generate quality documentation - READMEs, API docs, inline comments. Use when creating new project documentation, updating existing docs, or ensuring documentation stays in sync with code. Covers README patterns, JSDoc, OpenAPI, and architecture docs.
version: 1.0.0
author: Claude Code SDK
tags: [documentation, readme, api-docs, comments]
---

# Documentation Generation

Generate quality documentation that stays in sync with code. From READMEs to API docs to architecture documentation.

## Quick Reference

| Doc Type | Primary File | When to Use |
|----------|--------------|-------------|
| Project README | `README.md` | New project, major updates |
| API Documentation | JSDoc/docstrings | New functions, API changes |
| OpenAPI/Swagger | `openapi.yaml` | REST API documentation |
| Architecture | `ARCHITECTURE.md` | System design, major components |
| Change Log | `CHANGELOG.md` | Each release |
| Migration Guide | `MIGRATION.md` | Breaking changes |

## Documentation Principles

### 1. Document the Why, Not Just the What

```markdown
// Bad: Documents what the code does (obvious from code)
// Increments counter by 1

// Good: Documents why
// Prevents race condition by using atomic increment
```

### 2. Keep Docs Close to Code

| Pattern | Benefit |
|---------|---------|
| JSDoc above functions | Updates when code changes |
| README.md in package | Visible in package managers |
| Inline comments | Context at point of use |

### 3. Use Examples Liberally

Every API function should have at least one working example. Examples are:
- Tested implicitly when code runs
- More useful than prose descriptions
- Easier to keep up to date

## README Structure

A good README follows this structure:

```markdown
# Project Name

One-sentence description of what this does.

## Quick Start

\`\`\`bash
npm install package-name
\`\`\`

\`\`\`typescript
import { main } from 'package-name';
main();
\`\`\`

## Features

- Feature 1 - brief description
- Feature 2 - brief description

## Installation

Detailed installation instructions.

## Usage

### Basic Usage
...

### Advanced Usage
...

## API Reference

Link to detailed API docs or inline reference.

## Configuration

Environment variables, config files.

## Contributing

How to contribute.

## License

License information.
```

### README Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Wall of text | Short paragraphs, bullet points |
| Outdated examples | Use tested code snippets |
| Missing quick start | Add minimal working example |
| No installation | Include all setup steps |

## Inline Documentation

### JSDoc for TypeScript/JavaScript

```typescript
/**
 * Calculates the total price including tax.
 *
 * @param items - Array of items with price property
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @returns Total price with tax applied
 *
 * @example
 * ```typescript
 * const items = [{ price: 10 }, { price: 20 }];
 * calculateTotal(items, 0.08); // 32.40
 * ```
 *
 * @throws {Error} If taxRate is negative
 */
function calculateTotal(items: Item[], taxRate: number): number {
  // implementation
}
```

### Python Docstrings

```python
def calculate_total(items: list[Item], tax_rate: float) -> float:
    """Calculate the total price including tax.

    Args:
        items: List of items with price attribute.
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%).

    Returns:
        Total price with tax applied.

    Raises:
        ValueError: If tax_rate is negative.

    Example:
        >>> items = [Item(price=10), Item(price=20)]
        >>> calculate_total(items, 0.08)
        32.40
    """
```

### When to Comment

| Do Comment | Don't Comment |
|------------|---------------|
| Complex algorithms | Obvious operations |
| Business rules | What the code literally does |
| Non-obvious side effects | Self-explanatory names |
| Performance optimizations | Getters/setters |
| Workarounds and hacks | Every line |

## Workflow: Document New Project

### Prerequisites
- [ ] Project structure exists
- [ ] Main functionality works
- [ ] Package.json/pyproject.toml configured

### Steps

1. **Create README.md**
   - [ ] Add project name and description
   - [ ] Write quick start with minimal example
   - [ ] Document installation steps
   - [ ] Add usage examples

2. **Add API Documentation**
   - [ ] Add JSDoc/docstrings to public functions
   - [ ] Include @example for each function
   - [ ] Document parameters and return types
   - [ ] Note any thrown exceptions

3. **Create Architecture Doc (if needed)**
   - [ ] Diagram main components
   - [ ] Explain data flow
   - [ ] Document key decisions

4. **Initialize Changelog**
   - [ ] Create CHANGELOG.md
   - [ ] Add initial version entry

### Validation
- [ ] README has working quick start
- [ ] All public APIs documented
- [ ] Examples are runnable
- [ ] No broken links

## Workflow: Update Existing Documentation

### Steps

1. **Identify Stale Docs**
   - [ ] Check README against current behavior
   - [ ] Verify API docs match signatures
   - [ ] Test example code snippets

2. **Update Documentation**
   - [ ] Fix outdated examples
   - [ ] Update API references
   - [ ] Add missing sections

3. **Validate**
   - [ ] Run example code
   - [ ] Check all links work
   - [ ] Review for consistency

## Workflow: Generate API Docs

### For TypeScript (TypeDoc)

```bash
# Install
bun add -d typedoc

# Generate
bunx typedoc --out docs src/index.ts
```

### For Python (Sphinx)

```bash
# Install
pip install sphinx sphinx-autodoc-typehints

# Generate
sphinx-apidoc -o docs/api src/
sphinx-build -b html docs docs/_build
```

### For OpenAPI

See [API-DOCS.md](./API-DOCS.md) for detailed OpenAPI generation patterns.

## Keeping Docs in Sync

### Automated Approaches

| Approach | Tool | Use Case |
|----------|------|----------|
| TypeDoc | TypeScript | Generate from JSDoc |
| Sphinx | Python | Generate from docstrings |
| OpenAPI Generator | REST | Generate from spec |
| Storybook | React | Component documentation |

### Manual Checklist

Add to PR template:

```markdown
## Documentation
- [ ] README updated (if public API changed)
- [ ] JSDoc/docstrings added for new functions
- [ ] CHANGELOG updated
- [ ] Migration guide updated (if breaking change)
```

### Documentation Tests

```typescript
// In test file
import { exampleCode } from '../docs/examples';

test('documentation examples work', async () => {
  // Run the example code from docs
  const result = await exampleCode();
  expect(result).toBeDefined();
});
```

## Common Documentation Tasks

### Add JSDoc to Existing Code

```typescript
// Before
function processData(data, options) {
  // ...
}

// After
/**
 * Processes raw data according to specified options.
 *
 * @param data - Raw data to process
 * @param options - Processing configuration
 * @param options.validate - Whether to validate input (default: true)
 * @param options.transform - Transform function to apply
 * @returns Processed data object
 *
 * @example
 * ```typescript
 * const result = processData(rawData, { validate: true });
 * ```
 */
function processData(data: RawData, options: ProcessOptions): ProcessedData {
  // ...
}
```

### Generate README from Template

For a TypeScript library:

```markdown
# {package-name}

{one-line-description}

[![npm version](https://badge.fury.io/js/{package-name}.svg)](https://www.npmjs.com/package/{package-name})

## Installation

\`\`\`bash
npm install {package-name}
# or
bun add {package-name}
\`\`\`

## Quick Start

\`\`\`typescript
import { main } from '{package-name}';

const result = main();
console.log(result);
\`\`\`

## API

### `main(options?)`

Main entry point.

**Parameters:**
- `options.debug` (boolean): Enable debug mode

**Returns:** Result object

## License

MIT
```

## Debugging Documentation Issues

| Issue | Solution |
|-------|----------|
| Outdated examples | Set up doc tests |
| Broken links | Use relative links, add link checker |
| Missing docs | Add to PR checklist |
| Inconsistent style | Use doc linter (markdownlint) |

## Reference Files

| File | Contents |
|------|----------|
| [README-PATTERNS.md](./README-PATTERNS.md) | README generation, project documentation patterns |
| [API-DOCS.md](./API-DOCS.md) | API documentation, JSDoc, docstrings, OpenAPI |
| [MAINTENANCE.md](./MAINTENANCE.md) | Keeping docs up to date, validation strategies |
