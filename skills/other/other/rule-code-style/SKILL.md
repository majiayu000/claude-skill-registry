---
name: rule-code-style
description: 'Rule mapping for code-style'
---

# Rule code-style

Apply this rule whenever work touches:
- `*.ts`
- `*.tsx`

Code in this repository should be immediately readable by any team member without requiring extra context or tribal knowledge.

### Naming clarity

Choose names that convey meaning at the point of use:

```ts
// Clear
const documentExpirationDate = computeExpirationDate(document);

// Unclear
const d = calc(doc);
```

Functions should read as actions: `validateVehiclePlate`, `fetchCreditOrder`, `buildRuleOutput`. Variables should read as things: `ruleResult`, `parsedDocument`, `vehicleWeight`.

### Guard clauses and early returns

Flatten control flow by returning early for edge cases:

```ts
function evaluateResult(subject: RuleSubject): RuleOutput {
  if (!subject.document) {
    return { status: 'REJECTED', reason: 'Missing document' };
  }

  if (!subject.document.isValid) {
    return { status: 'REJECTED', reason: 'Invalid document' };
  }

  // Main logic at top indentation level
  return computeApproval(subject.document);
}
```

### Single responsibility

Each file and function should do one thing well. If a function needs a comment to separate "sections," it is likely doing too much. Extract helper functions with descriptive names.

### Formatting and linting

The project uses ESLint and Prettier via Nx. After changing code, verify it passes:

```bash
pnpm nx lint <project-name>
```

Every file must end with a single trailing newline (no trailing blank lines, no missing final newline).

### Imports

Use path aliases for anything outside the current library:

```ts
import { BoldHelpers } from '@carrot-fndn/shared/methodologies/bold/helpers';
```

Within the same library, use relative paths. Avoid deep relative paths that cross Nx project boundaries.
