---
name: typescript-import-style
description: Merge-friendly import formatting (one-per-line, alphabetical). Auto-loads when writing TypeScript/JavaScript imports to minimize merge conflicts in parallel development. Enforces consistent grouping and sorting.
user-invocable: false
---

# TypeScript Import Style Guidelines (Merge Conflict Reduction)

Import formatting and ordering rules to minimize merge conflicts when multiple developers or parallel agents modify the same file.

## CRITICAL: One Import Per Line

When importing multiple items from a module, put EACH import on its own line:

```typescript
// CORRECT - merge-friendly (each on separate line)
import {
  alpha,
  beta,
  gamma,
} from 'some-module';

// WRONG - causes merge conflicts
import { alpha, beta, gamma } from 'some-module';
```

This is enforced by Prettier with `printWidth: 80`. With one-per-line, Git can merge imports from parallel changes without conflicts.

## Import Order (Top to Bottom)

1. **Node.js built-ins** (e.g., `import fs from 'fs'`, `import path from 'path'`)
2. **External packages** (e.g., `import React from 'react'`, `import express from 'express'`)
3. **Internal aliases** (e.g., `import { util } from '@/utils'`)
4. **Parent directory imports** (e.g., `import { Parent } from '../Parent'`)
5. **Sibling imports** (e.g., `import { Sibling } from './Sibling'`)
6. **Index imports** (e.g., `import { thing } from './index'`)
7. **Type-only imports** (e.g., `import type { MyType } from './types'`)

## Within Each Group

- Sort imports alphabetically by module path (case-insensitive)
- Sort named imports alphabetically within braces
- Sort export statements alphabetically

## Spacing

- Add one blank line between import groups
- No blank lines within a group

## Complete Example

```typescript
// Node.js built-ins
import fs from 'fs';
import path from 'path';

// External packages
import express from 'express';
import React from 'react';

// Internal aliases
import { config } from '@/config';
import { logger } from '@/utils';

// Parent imports
import { BaseService } from '../BaseService';

// Sibling imports (one per line when multiple)
import {
  helperA,
  helperB,
  helperC,
} from './helpers';
import { utils } from './utils';

// Type imports (one per line when multiple)
import type { Config } from '@/types';
import type {
  Request,
  Response,
} from 'express';
```

## Named Exports

Sort named exports alphabetically, one per line when multiple:

```typescript
// CORRECT
export {
  alpha,
  beta,
  gamma,
};

// WRONG
export { gamma, alpha, beta };
```

## Why This Matters

Sorted, one-per-line imports reduce merge conflicts because:

- New imports are inserted at predictable positions (alphabetically)
- Parallel tasks adding imports to the same file won't conflict
- Git can auto-merge changes on different lines
- Consistent structure makes diffs cleaner and reviews easier

## Tooling (Auto-enforced)

These rules are enforced by:

- **eslint-plugin-simple-import-sort**: Sorts imports/exports alphabetically
- **Prettier with `printWidth: 80`**: Forces line wrapping for multiple imports

Run `eslint --fix && prettier --write` before committing.

## ESLint Configuration

```javascript
// .eslintrc.js or eslint.config.js
module.exports = {
  plugins: ['simple-import-sort'],
  rules: {
    'simple-import-sort/imports': 'error',
    'simple-import-sort/exports': 'error',
  },
};
```

## Prettier Configuration

```json
{
  "printWidth": 80,
  "singleQuote": true,
  "trailingComma": "all"
}
```

## Re-export Patterns

When re-exporting from index files, follow the same one-per-line rule:

```typescript
// CORRECT
export {
  ComponentA,
  ComponentB,
  ComponentC,
} from './components';

export type {
  TypeA,
  TypeB,
} from './types';

// WRONG
export { ComponentA, ComponentB, ComponentC } from './components';
```

## Dynamic Imports

Dynamic imports follow the same alphabetical ordering when multiple exist:

```typescript
// Alphabetical order by module path
const moduleA = await import('./moduleA');
const moduleB = await import('./moduleB');
const utils = await import('./utils');
```
