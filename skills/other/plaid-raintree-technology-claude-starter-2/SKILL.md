---
name: plaid
description: Plaid banking API expert for financial data integration. Covers Plaid Link, Auth (account/routing numbers), Transactions, Identity verification, Balance checking, and webhooks. Build fintech apps with bank connections, ACH transfers, and transaction history. Triggers on Plaid, banking API, Plaid Link, bank connection, ACH, financial data, transaction history.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
license: MIT
metadata:
  author: raintree
  version: "1.0"
---

# Plaid Banking API Expert

Plaid connects applications to users' bank accounts for financial data access, payments, and identity verification.

## When to Use

- Connecting bank accounts in fintech apps
- Implementing Plaid Link flow
- Retrieving transactions, balances, or account info
- Setting up ACH transfers
- Identity/income verification
- Handling Plaid webhooks

## Core Products

| Product | Purpose |
|---------|---------|
| **Auth** | Bank account/routing numbers for ACH |
| **Transactions** | Transaction history (up to 24 months) |
| **Identity** | Verify user via bank account ownership |
| **Balance** | Real-time account balances |
| **Investments** | Holdings from investment accounts |
| **Liabilities** | Loan and credit card data |

## Quick Start

### 1. Install SDK

```bash
npm install plaid react-plaid-link
```

### 2. Create Plaid Client

```typescript
import { Configuration, PlaidApi, PlaidEnvironments } from "plaid";

const client = new PlaidApi(
  new Configuration({
    basePath: PlaidEnvironments.sandbox,
    baseOptions: {
      headers: {
        "PLAID-CLIENT-ID": process.env.PLAID_CLIENT_ID,
        "PLAID-SECRET": process.env.PLAID_SECRET,
      },
    },
  })
);
```

### 3. Create Link Token (Server)

```typescript
// POST /api/plaid/create-link-token
export async function POST(req: Request) {
  const response = await client.linkTokenCreate({
    user: { client_user_id: userId },
    client_name: "Your App",
    products: ["auth", "transactions"],
    country_codes: ["US"],
    language: "en",
  });

  return Response.json({ link_token: response.data.link_token });
}
```

### 4. Plaid Link (Client)

```tsx
import { usePlaidLink } from "react-plaid-link";

function ConnectBank({ linkToken }) {
  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: async (public_token, metadata) => {
      // Exchange for access_token on server
      await fetch("/api/plaid/exchange-token", {
        method: "POST",
        body: JSON.stringify({ public_token }),
      });
    },
  });

  return (
    <button onClick={() => open()} disabled={!ready}>
      Connect Bank Account
    </button>
  );
}
```

### 5. Exchange Token (Server)

```typescript
// POST /api/plaid/exchange-token
export async function POST(req: Request) {
  const { public_token } = await req.json();

  const response = await client.itemPublicTokenExchange({
    public_token,
  });

  // Store access_token securely (encrypted in database)
  await db.users.update(userId, {
    plaid_access_token: response.data.access_token,
    plaid_item_id: response.data.item_id,
  });

  return Response.json({ success: true });
}
```

## Data Retrieval

### Get Auth (Account/Routing Numbers)

```typescript
const response = await client.authGet({ access_token });

const ach = response.data.numbers.ach[0];
console.log("Account:", ach.account);
console.log("Routing:", ach.routing);
```

### Get Transactions

```typescript
const response = await client.transactionsGet({
  access_token,
  start_date: "2024-01-01",
  end_date: "2024-12-31",
});

let transactions = response.data.transactions;

// Handle pagination
while (transactions.length < response.data.total_transactions) {
  const more = await client.transactionsGet({
    access_token,
    start_date: "2024-01-01",
    end_date: "2024-12-31",
    offset: transactions.length,
  });
  transactions = transactions.concat(more.data.transactions);
}
```

**Transaction object:**
```typescript
{
  transaction_id: "abc123",
  amount: 12.34,           // Positive = outflow
  date: "2024-11-16",
  name: "Starbucks",
  merchant_name: "Starbucks",
  category: ["Food and Drink", "Coffee Shop"],
  pending: false,
}
```

### Get Balance

```typescript
const response = await client.accountsBalanceGet({ access_token });

response.data.accounts.forEach((account) => {
  console.log(`${account.name}: $${account.balances.current}`);
});
```

### Get Identity

```typescript
const response = await client.identityGet({ access_token });

const owner = response.data.accounts[0].owners[0];
console.log("Name:", owner.names[0]);
console.log("Email:", owner.emails[0].data);
console.log("Phone:", owner.phone_numbers[0].data);
```

## Webhooks

### Setup Endpoint

```typescript
// POST /api/plaid/webhook
export async function POST(req: Request) {
  const { webhook_type, webhook_code, item_id } = await req.json();

  switch (webhook_type) {
    case "TRANSACTIONS":
      if (webhook_code === "DEFAULT_UPDATE") {
        // New transactions available - fetch them
        await syncTransactions(item_id);
      }
      break;

    case "ITEM":
      if (webhook_code === "ERROR") {
        // Connection issue - prompt user to re-authenticate
        await notifyUserReauth(item_id);
      }
      break;
  }

  return Response.json({ received: true });
}
```

**Key webhook events:**
| Event | Meaning |
|-------|---------|
| `TRANSACTIONS: INITIAL_UPDATE` | First batch ready |
| `TRANSACTIONS: DEFAULT_UPDATE` | New transactions |
| `ITEM: ERROR` | Connection issue |
| `ITEM: PENDING_EXPIRATION` | Credentials expiring |

## Environments

| Environment | Use Case | Base Path |
|-------------|----------|-----------|
| **Sandbox** | Testing | `PlaidEnvironments.sandbox` |
| **Development** | Limited live (100 connections) | `PlaidEnvironments.development` |
| **Production** | Live | `PlaidEnvironments.production` |

### Sandbox Test Credentials

- Username: `user_good`
- Password: `pass_good`
- MFA: `1234`

## Error Handling

### Re-authentication (Update Mode)

When credentials expire:

```typescript
// Create link token for update mode
const response = await client.linkTokenCreate({
  user: { client_user_id: userId },
  client_name: "Your App",
  access_token: existingAccessToken, // Triggers update mode
  country_codes: ["US"],
  language: "en",
});
```

### Common Errors

| Error | Solution |
|-------|----------|
| `ITEM_LOGIN_REQUIRED` | Re-authenticate via Link update mode |
| `RATE_LIMIT_EXCEEDED` | Implement exponential backoff |
| `PRODUCT_NOT_READY` | Wait for webhook or retry |

## Security Best Practices

**DO:**
- Store access tokens encrypted in database
- Use environment variables for credentials
- Verify webhook signatures
- Use HTTPS for all endpoints

**DON'T:**
- Expose secret keys client-side
- Log access tokens
- Store credentials in code

## Next.js App Router Example

```typescript
// app/api/plaid/create-link-token/route.ts
import { NextResponse } from "next/server";
import { Configuration, PlaidApi, PlaidEnvironments } from "plaid";

const client = new PlaidApi(
  new Configuration({
    basePath: PlaidEnvironments.sandbox,
    baseOptions: {
      headers: {
        "PLAID-CLIENT-ID": process.env.PLAID_CLIENT_ID!,
        "PLAID-SECRET": process.env.PLAID_SECRET!,
      },
    },
  })
);

export async function POST(req: Request) {
  const session = await getSession();

  const response = await client.linkTokenCreate({
    user: { client_user_id: session.user.id },
    client_name: "Your App",
    products: ["auth", "transactions"],
    country_codes: ["US"],
    language: "en",
    webhook: `${process.env.NEXT_PUBLIC_URL}/api/plaid/webhook`,
  });

  return NextResponse.json({ link_token: response.data.link_token });
}
```

## Implementation Checklist

- [ ] Sign up for Plaid account
- [ ] Get client ID and secret
- [ ] Install `plaid` and `react-plaid-link`
- [ ] Set environment variables
- [ ] Create link token endpoint
- [ ] Implement token exchange endpoint
- [ ] Integrate Plaid Link on frontend
- [ ] Store access tokens securely
- [ ] Set up webhook endpoint
- [ ] Handle re-authentication errors
- [ ] Test with sandbox credentials

## Resources

- **Docs:** https://plaid.com/docs/
- **API Reference:** https://plaid.com/docs/api/
- **Quickstart:** https://github.com/plaid/quickstart
