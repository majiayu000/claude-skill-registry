---
name: rule-lambda
description: 'Rule mapping for lambda'
---

# Rule lambda

Apply this rule whenever work touches:
- `**/*.lambda.ts`

Lambda handlers are the entry points for AWS Lambda invocations. They must remain thin wrappers that connect the Lambda runtime to the processor.

### Handler structure

A typical Lambda handler file:

```ts
import { wrapHandler } from '@carrot-fndn/shared/lambda';
import { VehicleValidationProcessor } from './vehicle-validation.processor';

const processor = new VehicleValidationProcessor();

export const handler = wrapHandler(processor);
```

The handler should contain no business logic. All evaluation, validation, and transformation happens in the processor.

### Error handling

Let errors propagate naturally to the Lambda runtime:

```ts
// Correct - errors propagate for retry
export const handler = wrapHandler(processor);

// Wrong - swallowing errors prevents retries
export const handler = async (event: unknown) => {
  try {
    return await processor.execute(event);
  } catch {
    return { statusCode: 500, body: 'Error' };
  }
};
```

AWS Lambda has built-in retry mechanisms for asynchronous invocations. Swallowing errors defeats this reliability mechanism.

### E2E testing

E2E tests exercise the full handler path including event deserialization:

```ts
import { handler } from './vehicle-validation.lambda';
import { validInput, invalidInput } from './vehicle-validation.test-cases';

describe('VehicleValidation Lambda E2E', () => {
  it('should return approved for valid input', async () => {
    const result = await handler(validInput);
    expect(result.resultStatus).toBe('APPROVED');
  });
});
```

These tests complement the processor unit tests by verifying the integration between the handler and processor layers.
