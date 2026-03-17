---
name: midnight-dapp:error-handling
description: Use when implementing error handling in Midnight DApps, displaying errors to users, handling proof generation failures, managing transaction rejections, or dealing with network disconnections.
---

# Error Handling

Handle errors gracefully in Midnight DApps with user-friendly messaging, proper error classification, and recovery strategies.

## When to Use

- Displaying errors to users in a helpful way
- Implementing error boundaries for React components
- Handling proof generation failures
- Managing transaction rejections and contract errors
- Dealing with network disconnections (indexer, proof server)
- Creating consistent error messaging across your DApp

## Key Concepts

### Error Taxonomy

Midnight DApps encounter several categories of errors:

| Category | Source | Examples |
|----------|--------|----------|
| **Proof Errors** | ZK proof generation | Timeout, constraint violations, witness failures |
| **Transaction Errors** | Contract execution | Insufficient balance, state conflicts, rejections |
| **Network Errors** | Infrastructure | Indexer down, proof server unavailable, WebSocket disconnect |
| **Wallet Errors** | User interaction | Not installed, rejected, wrong network |

### User-Friendly Messaging

Technical errors should be translated to actionable messages:

```typescript
// Technical error
"Circuit constraint failed at gate 1042: input > max_value"

// User-friendly message
"The amount exceeds the maximum allowed. Please enter a smaller value."
```

### Recovery Patterns

Different errors require different recovery strategies:

- **Retryable**: Timeouts, temporary network issues - offer retry button
- **User Action Required**: Wrong network, insufficient balance - guide user
- **Fatal**: Contract bugs, invalid state - show support contact

## References

| Document | Description |
|----------|-------------|
| [proof-errors.md](references/proof-errors.md) | ZK proof failures and diagnosis |
| [transaction-errors.md](references/transaction-errors.md) | Contract execution errors |
| [network-errors.md](references/network-errors.md) | Connection and timeout handling |
| [user-messaging.md](references/user-messaging.md) | UX guidelines for error display |

## Examples

| Example | Description |
|---------|-------------|
| [error-boundary/](examples/error-boundary/) | React error boundary for Midnight |
| [error-toast/](examples/error-toast/) | Toast notification component |
| [typed-errors/](examples/typed-errors/) | Custom error classes and catalog |

## Quick Start

### 1. Create Typed Errors

```typescript
import { MidnightError, ErrorCode } from './MidnightErrors';

// Throw typed errors in your code
throw new MidnightError(
  ErrorCode.PROOF_TIMEOUT,
  'Proof generation timed out',
  { timeoutMs: 60000, operation: 'transfer' }
);
```

### 2. Classify Unknown Errors

```typescript
import { classifyError } from './errorUtils';

try {
  await contract.callTx.transfer(recipient, amount, witnesses);
} catch (error) {
  const classified = classifyError(error);
  // { code, message, userMessage, suggestion, retryable, category }
}
```

### 3. Display to Users

```typescript
import { useErrorToast } from './useErrorToast';

function TransferButton() {
  const { showError } = useErrorToast();

  const handleTransfer = async () => {
    try {
      await performTransfer();
    } catch (error) {
      showError(error); // Shows user-friendly toast
    }
  };
}
```

### 4. Wrap Components

```tsx
import { MidnightErrorBoundary } from './MidnightErrorBoundary';

function App() {
  return (
    <MidnightErrorBoundary
      onReset={() => window.location.reload()}
      fallback={<ErrorPage />}
    >
      <MyDApp />
    </MidnightErrorBoundary>
  );
}
```

## Common Patterns

### Error Classification Utility

```typescript
interface ClassifiedError {
  code: string;
  message: string;
  userMessage: string;
  suggestion: string;
  retryable: boolean;
  category: 'proof' | 'transaction' | 'network' | 'wallet' | 'unknown';
}

function classifyError(error: unknown): ClassifiedError {
  if (error instanceof MidnightError) {
    return {
      code: error.code,
      message: error.message,
      userMessage: ERROR_CATALOG[error.code].userMessage,
      suggestion: ERROR_CATALOG[error.code].suggestion,
      retryable: ERROR_CATALOG[error.code].retryable,
      category: ERROR_CATALOG[error.code].category,
    };
  }

  // Classify by error message patterns
  const message = error instanceof Error ? error.message : String(error);
  return classifyByMessage(message);
}
```

### Retry with Backoff

```typescript
async function withRetry<T>(
  operation: () => Promise<T>,
  options: {
    maxRetries: number;
    baseDelayMs: number;
    shouldRetry: (error: unknown) => boolean;
  }
): Promise<T> {
  let lastError: unknown;

  for (let attempt = 1; attempt <= options.maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;

      if (!options.shouldRetry(error) || attempt === options.maxRetries) {
        throw error;
      }

      const delay = options.baseDelayMs * Math.pow(2, attempt - 1);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError;
}
```

### Error Context Provider

```typescript
const ErrorContext = createContext<ErrorContextValue | null>(null);

function ErrorProvider({ children }: { children: ReactNode }) {
  const [errors, setErrors] = useState<ClassifiedError[]>([]);

  const addError = useCallback((error: unknown) => {
    const classified = classifyError(error);
    setErrors(prev => [...prev, classified]);

    // Auto-dismiss non-critical errors
    if (classified.category !== 'wallet') {
      setTimeout(() => dismissError(classified.code), 5000);
    }
  }, []);

  const dismissError = useCallback((code: string) => {
    setErrors(prev => prev.filter(e => e.code !== code));
  }, []);

  return (
    <ErrorContext.Provider value={{ errors, addError, dismissError }}>
      {children}
    </ErrorContext.Provider>
  );
}
```

## Error Handling Best Practices

1. **Never swallow errors silently** - Always log or display
2. **Provide actionable messages** - Tell users what they can do
3. **Log technical details** - Keep full error info for debugging
4. **Use error boundaries** - Prevent cascading failures in UI
5. **Categorize appropriately** - Different errors need different handling
6. **Test error paths** - Verify error UI works correctly
7. **Consider accessibility** - Error messages should work with screen readers

## Related Skills

- `wallet-integration` - Wallet-specific error handling
- `proof-handling` - Proof generation error patterns
- `transaction-flows` - Transaction error recovery
- `state-management` - State read error handling

## Related Commands

- `/dapp-check` - Validates error handling patterns
- `/dapp-debug errors` - Diagnose error handling issues
