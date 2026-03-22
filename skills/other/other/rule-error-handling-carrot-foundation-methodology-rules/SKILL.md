---
name: rule-error-handling
description: 'Rule mapping for error-handling'
---

# Rule error-handling

Apply this rule whenever work touches:
- `*.ts`

Proper error handling ensures that failures are visible, diagnosable, and recoverable. In a Lambda-based architecture, error propagation also controls retry behavior and dead-letter queue routing.

### Input validation at boundaries

Validate external data where it enters the system. Use Zod schemas:

```ts
const parseResult = RuleInputSchema.safeParse(event);

if (!parseResult.success) {
  logger.error({ errors: parseResult.error.issues }, 'Invalid rule input');
  throw new ValidationError('Rule input failed schema validation', {
    cause: parseResult.error,
  });
}

const ruleInput = parseResult.data;
```

Internal function-to-function calls within a trusted boundary do not need redundant validation; rely on TypeScript's type system there.

### Error enrichment

When catching an error to add context, preserve the original error as the `cause`:

```ts
try {
  await fetchDocument(documentId);
} catch (error) {
  throw new DocumentFetchError(
    `Failed to fetch document ${documentId} during credit evaluation`,
    { cause: error },
  );
}
```

This preserves the full error chain for debugging while adding the business context needed to understand what was happening.

### Lambda error propagation

Lambda handlers must not swallow errors for operations that should be retried. Let the error propagate to the Lambda runtime:

```ts
// Correct - error reaches Lambda runtime, triggers retry
export const handler = async (event: SQSEvent): Promise<void> => {
  const input = parseAndValidate(event);
  await processRule(input);
};

// Wrong - error is caught and swallowed, message is lost
export const handler = async (event: SQSEvent): Promise<void> => {
  try {
    const input = parseAndValidate(event);
    await processRule(input);
  } catch {
    console.log('Something went wrong');
  }
};
```

### Structured logging

Use pino for all logging. Include structured fields that aid debugging:

```ts
logger.error(
  {
    documentId,
    ruleId,
    operation: 'evaluateResult',
    err: error,
  },
  'Rule evaluation failed',
);
```

Never include credentials, tokens, full request/response bodies with PII, or other sensitive data in log output.

### Result patterns for expected failures

For failure modes that callers are expected to handle (e.g., a document that legitimately fails validation), consider using a Result-like return type instead of throwing:

```ts
type EvaluationResult =
  | { success: true; output: RuleOutput }
  | { success: false; reason: string };
```

Reserve thrown errors for unexpected failures (infrastructure errors, programming bugs, corrupted data).
