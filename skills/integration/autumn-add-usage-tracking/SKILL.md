---
name: autumn-add-usage-tracking
description: Skill for adding feature gating and usage tracking using Autumn.
---

# Autumn Usage Tracking

**Always consult [docs.useautumn.com](https://docs.useautumn.com) for code examples and latest API.**

Autumn tracks feature usage and enforces limits. Backend checks required for security.

---

## Quick Reference

### Core Pattern
```
check → work → track
```

### Check Response

| Field | Description |
|-------|-------------|
| `allowed` | Can customer proceed |
| `balance` | Units remaining |
| `included_usage` | Total usage included in plan |
| `unlimited` | No limit enforced |

### Feature Types

| Type | Behavior |
|------|----------|
| `boolean` | Access granted or denied |
| `metered` | Usage tracked against limit |
| `credit_system` | Pool for multiple features |

---

## Security Model

| Layer | Purpose | Trust |
|-------|---------|-------|
| Frontend | UX (show/hide UI) | Untrusted |
| Backend | Enforcement | Required |

---

## Backend Implementation

```typescript
import { Autumn } from "autumn-js";

const autumn = new Autumn({ secretKey: process.env.AUTUMN_SECRET_KEY });

// 1. Check
const { data } = await autumn.check({ customer_id, feature_id: "api_calls" });
if (!data.allowed) return { error: "Limit reached" };

// 2. Work
const result = await doWork();

// 3. Track
await autumn.track({ customer_id, feature_id: "api_calls", value: 1 });
return result;
```

```python
from autumn import Autumn

autumn = Autumn('am_sk_test_xxx')

response = await autumn.check(customer_id="user_123", feature_id="api_calls")
if not response.allowed:
    raise HTTPException(403, "Limit reached")

result = await do_work()
await autumn.track(customer_id="user_123", feature_id="api_calls", value=1)
```

---

## React Implementation

```tsx
import { useCustomer } from "autumn-js/react";

const { check, refetch } = useCustomer();

const handleAction = async () => {
  const { data } = await check({ featureId: "messages" });
  if (!data?.allowed) {
    showUpgradePrompt();
    return;
  }
  
  await performAction();
  await refetch();
};
```

---

## Displaying Usage

```tsx
const { customer } = useCustomer();
const feature = customer?.features?.api_calls;

<p>{feature?.balance} / {feature?.included_usage}</p>
```

---

## Credit Systems

Track the underlying metered feature, not the credit system:

```typescript
// Config: credits → api_calls (1), image_gen (10)

// Wrong
await autumn.track({ customer_id, feature_id: "credits", value: 10 });

// Right - Autumn deducts 10 credits automatically
await autumn.track({ customer_id, feature_id: "image_gen", value: 1 });
```

---

## Common Gotchas

1. **Track after success** - Only track if work completes successfully
2. **Backend required** - Frontend checks can be bypassed
3. **Credit systems** - Track metered features, not the credit pool
4. **Idempotency** - Use `idempotency_key` to prevent double-counting
5. **Batch tracking** - Pass higher `value` for bulk operations

---

## Resources

- [Check Docs](https://docs.useautumn.com/api-reference/core/check)
- [Track Docs](https://docs.useautumn.com/api-reference/core/track)
- [Credit Systems](https://docs.useautumn.com/documentation/pricing/credits)
- [LLMs.txt](https://docs.useautumn.com/llms.txt)
