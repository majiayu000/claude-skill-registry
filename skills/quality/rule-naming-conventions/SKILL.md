---
name: rule-naming-conventions
description: 'Rule mapping for naming-conventions'
---

# Rule naming-conventions

Apply this rule whenever work touches:
- `*.ts`
- `*.tsx`

Consistent naming reduces cognitive load and makes the codebase searchable. Every identifier and file in this repository must follow the patterns below.

### Identifier casing

| Kind | Casing | Example |
|---|---|---|
| Variable, function, parameter | camelCase | `vehicleWeight`, `computeScore` |
| Type, interface, enum, class | PascalCase | `RuleOutput`, `DocumentStatus` |
| Module-level constant | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `DEFAULT_PRECISION` |
| Enum member | UPPER_SNAKE_CASE | `DocumentStatus.APPROVED` |

### File naming

All files and directories use kebab-case:

```text
vehicle-validation.processor.ts
vehicle-validation.processor.spec.ts
vehicle-validation.lambda.ts
vehicle-validation.lambda.e2e.spec.ts
vehicle-validation.test-cases.ts
```

### Rule processor structure

Each rule processor follows a predictable naming pattern tied to the rule name:

| File | Pattern |
|---|---|
| Processor | `{rule-name}.processor.ts` |
| Lambda handler | `{rule-name}.lambda.ts` |
| Unit tests | `{rule-name}.processor.spec.ts` |
| E2E tests | `{rule-name}.lambda.e2e.spec.ts` |
| Test data | `{rule-name}.test-cases.ts` |

### Meaningful identifiers

Names must be descriptive enough to understand at the call site without jumping to the definition:

```ts
// Clear
const carbonCreditScore = computeCarbonCreditScore(massBalance);

// Unclear
const s = calc(mb);
```

Avoid generic names like `data`, `info`, or `result` unless qualified with domain context (e.g. `documentData`, `validationResult`).

### Booleans

Boolean variables and functions should read as questions:

```ts
const isExpired = checkExpiration(document);
const hasValidSignature = verifySignature(certificate);
const canRetry = retryCount < MAX_RETRY_COUNT;
```
