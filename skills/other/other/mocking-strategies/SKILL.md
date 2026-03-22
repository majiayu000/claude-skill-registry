---
name: mocking-strategies
description: >
  Mocks vs stubs vs spies, dependency injection for testing, jest.mock/unittest.mock/gomock,
  and when NOT to mock. Use when the user needs to isolate dependencies in tests, asks about
  mocking external services, or has tests tightly coupled to implementation details.
---

# Mocking Strategies

Mocking isolates the code under test from its dependencies. Done right, mocks make tests fast and focused. Done wrong, they create brittle tests coupled to implementation details.

## When to Use
- User needs to test code that calls external APIs or databases
- User asks about mocks, stubs, spies, or fakes
- Tests are slow because they hit real services
- User wants to test error paths that are hard to trigger naturally
- Tests are brittle and break on internal refactors

## Core Patterns

### Mocks vs Stubs vs Spies

| Type | Purpose | Verifies Calls? | Returns Data? |
|------|---------|----------------|---------------|
| Stub | Replace with canned response | No | Yes |
| Spy | Observe calls without replacing | Yes | Original |
| Mock | Replace + verify calls + canned response | Yes | Yes |

```typescript
// STUB: Replace function, return fixed data
const getUser = vi.fn().mockResolvedValue({ id: 1, name: 'Alice' })

// SPY: Watch real function, keep original behavior
const spy = vi.spyOn(userService, 'getUser')
// Real getUser still runs, but calls are recorded

// MOCK: Replace function, return fixed data, verify calls
const sendEmail = vi.fn().mockResolvedValue({ sent: true })
await notifyUser(1)
expect(sendEmail).toHaveBeenCalledWith('alice@example.com', expect.any(String))
```

### Vitest / Jest Mocking

**Module mock:**

```typescript
import { describe, it, expect, vi } from 'vitest'
import { processOrder } from './orders'

// Mock the entire payment module
vi.mock('./payment', () => ({
  chargeCard: vi.fn().mockResolvedValue({ success: true, txId: 'tx-123' }),
}))

import { chargeCard } from './payment'

describe('processOrder', () => {
  it('charges the card and returns order confirmation', async () => {
    const order = await processOrder({ userId: 1, amount: 99 })

    expect(chargeCard).toHaveBeenCalledWith({ userId: 1, amount: 99 })
    expect(order.status).toBe('confirmed')
    expect(order.transactionId).toBe('tx-123')
  })

  it('handles payment failure', async () => {
    vi.mocked(chargeCard).mockRejectedValueOnce(new Error('Card declined'))

    await expect(processOrder({ userId: 1, amount: 99 }))
      .rejects.toThrow('Card declined')
  })
})
```

**Spy on object method:**

```typescript
const spy = vi.spyOn(console, 'error').mockImplementation(() => {})

await riskyOperation()

expect(spy).toHaveBeenCalledWith('Operation failed:', expect.any(Error))
spy.mockRestore()
```

### Python unittest.mock

**Patching with context manager:**

```python
from unittest.mock import patch, MagicMock

def test_send_notification():
    with patch('myapp.services.email.send') as mock_send:
        mock_send.return_value = {"sent": True}

        result = notify_user(user_id=1, message="Hello")

        mock_send.assert_called_once_with(
            to="alice@example.com",
            body="Hello"
        )
        assert result["sent"] is True
```

**Patching with decorator:**

```python
@patch('myapp.services.payment.charge_card')
def test_process_order(mock_charge):
    mock_charge.return_value = {"success": True, "tx_id": "tx-123"}

    order = process_order(user_id=1, amount=99)

    mock_charge.assert_called_once_with(user_id=1, amount=99)
    assert order["status"] == "confirmed"
```

**Mock side effects for error testing:**

```python
@patch('myapp.services.payment.charge_card')
def test_payment_failure(mock_charge):
    mock_charge.side_effect = PaymentError("Card declined")

    with pytest.raises(PaymentError, match="Card declined"):
        process_order(user_id=1, amount=99)
```

### Dependency Injection for Testability

Design code to accept dependencies, making them mockable:

```typescript
// HARD TO TEST: Direct import
import { db } from './database'

export async function getUser(id: string) {
  return db.query('SELECT * FROM users WHERE id = $1', [id])
}

// EASY TO TEST: Dependency injection
export function createUserService(db: Database) {
  return {
    async getUser(id: string) {
      return db.query('SELECT * FROM users WHERE id = $1', [id])
    },
  }
}

// In tests:
const mockDb = { query: vi.fn().mockResolvedValue({ id: '1', name: 'Alice' }) }
const service = createUserService(mockDb)
const user = await service.getUser('1')
```

### When NOT to Mock

Do not mock these — use the real thing:

```
1. Pure functions (no side effects, deterministic)
   createSlug('Hello World') -> test with real input/output

2. Value objects and data transformations
   formatDate(date) -> test with real dates

3. Your own code under test
   Do not mock the function you are testing

4. Standard library / language built-ins
   Do not mock Array.map, string methods, Math.random (seed instead)

5. Simple internal utilities
   If formatCurrency() is fast and pure, call it for real
```

Mock only at system boundaries:
- External HTTP APIs
- Database queries
- File system operations
- Email/SMS services
- Payment processors
- Clock/time (use fake timers instead)

### Fake Timers

For time-dependent code, use fake timers instead of mocking Date:

```typescript
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest'

describe('session expiry', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('expires session after 30 minutes', () => {
    const session = createSession()
    expect(session.isValid()).toBe(true)

    vi.advanceTimersByTime(30 * 60 * 1000) // 30 minutes

    expect(session.isValid()).toBe(false)
  })
})
```

## Anti-Patterns

- **Mocking everything**: If you mock all dependencies, you are testing the mocking framework, not your code. Mock at boundaries; let internal code run for real.
- **Testing mock behavior**: `expect(mock).toHaveBeenCalled()` without asserting the result tests that you called a mock, not that your code works. Always assert on output or observable behavior.
- **Mocking what you do not own without integration tests**: Mocking a third-party API is fine for unit tests, but you also need integration tests that call the real API to catch contract changes.
- **Implementation-coupled mocks**: If a refactor (same behavior, different internal calls) breaks your tests, the mocks are too specific. Mock at a higher level.
- **Not restoring mocks**: Forgetting `mockRestore()` or `afterEach(() => vi.restoreAllMocks())` leaks mock state between tests, causing flaky failures.
- **Mocking pure functions**: If a function has no side effects and is fast, call it for real. Mocking it adds complexity without value.

## Quick Reference

| Scenario | Strategy |
|----------|----------|
| External API call | Mock the HTTP client |
| Database query | Mock the repository/query function |
| Time-dependent logic | Fake timers (`vi.useFakeTimers()`) |
| Error paths | `mockRejectedValue` / `side_effect` |
| Pure functions | Do NOT mock — test with real input |
| Internal utilities | Do NOT mock — call for real |
| File I/O | Mock the fs calls or use temp directory |

**Mock at boundaries**: External services, databases, filesystem, network.
**Do not mock**: Pure functions, value objects, the code under test itself.
**Always restore**: `vi.restoreAllMocks()` in afterEach or use `mockRestore()`.
**DI for testability**: Accept dependencies as parameters, not hard imports.
