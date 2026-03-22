---
name: rule-module-boundaries
description: 'Rule mapping for module-boundaries'
---

# Rule module-boundaries

Apply this rule whenever work touches:
- `libs/**/*.ts`

Nx enforces strict module boundaries to keep the dependency graph clean and prevent coupling between unrelated parts of the codebase.

### Dependency rules

The architecture enforces a layered dependency model:

```
apps/methodologies/*  -->  libs/methodologies/bold/rule-processors/*
                                      |
                                      v
                           libs/shared/*  (helpers, lambda, rule, testing, etc.)
```

Key constraints:

- **Processors depend on shared only.** A rule processor under `libs/methodologies/bold/rule-processors/mass-id/` can import from `libs/shared/*` but never from `libs/methodologies/bold/rule-processors/credit-order/`.
- **Shared libraries are independent.** Shared libraries should not depend on processors or apps.
- **No circular references.** If library A imports from library B, then B must not import from A.

### Path aliases

Always use the configured path aliases for cross-library imports:

```ts
// Correct
import { getDocumentField } from '@carrot-fndn/shared/methodologies/bold/helpers';
import { stubDocument } from '@carrot-fndn/shared/testing';

// Wrong
import { getDocumentField } from '../../../shared/methodologies/bold/helpers/src';
```

### Verifying boundaries

Use the Nx dependency graph to check for violations:

```bash
pnpm nx graph
pnpm nx lint <project-name>  # includes module boundary checks
```

The `@nx/enforce-module-boundaries` ESLint rule will flag any import that violates the configured constraints.
