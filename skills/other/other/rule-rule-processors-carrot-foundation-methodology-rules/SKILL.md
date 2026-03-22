---
name: rule-rule-processors
description: 'Rule mapping for rule-processors'
---

# Rule rule-processors

Apply this rule whenever work touches:
- `libs/methodologies/**/*.ts`

Rule processors are the core units of methodology evaluation. Each processor validates a specific aspect of a document against Bold methodology requirements.

### Directory structure

Every rule processor must contain the following files:

```
{rule-name}/
├── {rule-name}.processor.ts       # Core logic
├── {rule-name}.lambda.ts          # Lambda handler (thin wrapper)
├── {rule-name}.processor.spec.ts  # Unit tests
├── {rule-name}.lambda.e2e.spec.ts # E2E tests
├── {rule-name}.test-cases.ts      # Shared test data
├── index.ts                       # Public exports
├── project.json                   # Nx project config
└── jest.config.ts                 # Jest config
```

### Scaffolding

Always use the CLI tool to create new rules:

```bash
# Create a new rule
pnpm create-rule vehicle-validation mass-id "Validates vehicle data"

# Apply the rule to a methodology
pnpm apply-methodology-rule carbon-organic geolocation-precision mass-id
```

### Processor implementation

Processors extend `ParentDocumentRuleProcessor<RuleSubject>` and implement `evaluateResult()`:

```ts
import { ParentDocumentRuleProcessor } from '@carrot-fndn/shared/rule';
import type { RuleSubject } from '@carrot-fndn/shared/rule';

export class VehicleValidationProcessor extends ParentDocumentRuleProcessor<RuleSubject> {
  protected override evaluateResult(subject: RuleSubject): RuleOutput {
    // Business logic here
  }
}
```

### Test organization

Define reusable test data in `{rule-name}.test-cases.ts`:

```ts
import { stubRuleInput } from '@carrot-fndn/shared/testing';

export const validInput = stubRuleInput({
  // override only what this rule cares about
});

export const invalidInput = stubRuleInput({
  // data that should cause the rule to fail
});
```

Both `*.spec.ts` and `*.e2e.spec.ts` files should import from the test-cases file to keep assertions consistent.
