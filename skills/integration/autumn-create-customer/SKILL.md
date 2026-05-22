---
name: autumn-create-customer
description: Skill for setting up Autumn billing integration and creating customers.
---

# Autumn Customer Setup

**Always consult [docs.useautumn.com](https://docs.useautumn.com) for code examples and latest API.**

---

## Quick Reference

### Environment Variables
- `AUTUMN_SECRET_KEY` - Required. Get one at [app.useautumn.com](https://app.useautumn.com/dev?tab=api_keys)

### Installation
```bash
npm install autumn-js    # Node.js
pip install autumn-py    # Python
```

---

## Integration Paths

| Stack | Path |
|-------|------|
| React + Node.js | Mount handler + AutumnProvider |
| Backend only | Initialize client + call API |

---

## Path A: React + Node.js

### Handler Setup

| Framework | File | Import |
|-----------|------|--------|
| Next.js App Router | `app/api/autumn/[...all]/route.ts` | `autumn-js/next` |
| React Router | `app/routes/api.autumn.tsx` | `autumn-js/react-router` |
| Hono | Any file | `autumn-js/hono` |
| Express | Any file | `autumn-js/express` |
| Fastify | Any file | `autumn-js/fastify` |

```typescript
import { autumnHandler } from "autumn-js/next";

export const { GET, POST } = autumnHandler({
  identify: async (request) => {
    const session = await getSession(request);
    return {
      customerId: session.user.id,  // or session.org.id for B2B
      customerData: { name: session.user.name, email: session.user.email },
    };
  },
});
```

### Client Setup

```tsx
import { AutumnProvider } from "autumn-js/react";

<AutumnProvider>{children}</AutumnProvider>

// Different backend URL:
<AutumnProvider backendUrl={process.env.NEXT_PUBLIC_API_URL} />
```

### Verify

```tsx
import { useCustomer } from "autumn-js/react";

const { customer } = useCustomer();
console.log("Autumn customer:", customer);
```

---

## Path B: Backend Only

### Initialize

```typescript
import { Autumn } from "autumn-js";

const autumn = new Autumn({ secretKey: process.env.AUTUMN_SECRET_KEY });
```

```python
from autumn import Autumn

autumn = Autumn('am_sk_test_xxx')
```

### Create Customer

```typescript
const { data } = await autumn.customers.create({
  id: "user_id_from_auth",
  name: "Test User",
  email: "test@example.com",
});
```

---

## Common Gotchas

1. **B2C vs B2B** - Decide if `customerId` is user ID or org ID before integrating
2. **Idempotent** - `customers.create` returns existing customer if ID exists
3. **Backend URL** - Pass `backendUrl` to provider if API is on different domain
4. **Secret key** - Keep `AUTUMN_SECRET_KEY` server-side only

---

## Resources

- [Setup Docs](https://docs.useautumn.com/documentation/getting-started/setup/sdk)
- [React Setup](https://docs.useautumn.com/documentation/getting-started/setup/react)
- [LLMs.txt](https://docs.useautumn.com/llms.txt)
