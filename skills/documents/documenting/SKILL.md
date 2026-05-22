---
name: 'documenting'
description: 'Creates clear, maintainable documentation for code and APIs. Use when writing README files, API docs, code comments, or when asked to document code.'
---

# Documenting

## Documentation Types

| Type      | Audience     | Content                           |
| --------- | ------------ | --------------------------------- |
| README    | New users    | Quick start, installation, usage  |
| API docs  | Developers   | Endpoints, parameters, responses  |
| Code docs | Contributors | Architecture, patterns, decisions |
| Comments  | Code readers | Why, not what                     |

## README Structure

```markdown
# Project Name

Brief description (1-2 sentences).

## Quick Start

\`\`\`bash
npm install project-name
\`\`\`

## Usage

\`\`\`typescript
import { feature } from 'project-name';
// Minimal working example
\`\`\`

## API Reference

Link to detailed docs or brief overview.

## Contributing

How to contribute, run tests, submit PRs.

## License

License type and link.
```

## Code Comments

```typescript
// Good - explains WHY
// Cache invalidated after 5 minutes to balance freshness vs API rate limits
const CACHE_TTL = 300_000;

// Bad - explains WHAT (obvious from code)
// Set cache TTL to 300000
const CACHE_TTL = 300_000;
```

## JSDoc Format

```typescript
/**
 * Calculates the total price including tax.
 *
 * @param items - Cart items to calculate
 * @param region - Tax region (affects rate)
 * @returns Total price in cents
 * @throws {ValidationError} If items array is empty
 *
 * @example
 * const total = calculateTotal([{ price: 1000 }], 'EU');
 * // Returns: 1210 (with 21% VAT)
 */
function calculateTotal(items: Item[], region: Region): number {
```

## Principles

1. **Audience-first**: Write for the reader, not yourself
2. **Examples over explanation**: Show, don't just tell
3. **Keep current**: Outdated docs are worse than none
4. **DRY**: Link to existing docs, don't duplicate
5. **Scannable**: Use headings, lists, tables
