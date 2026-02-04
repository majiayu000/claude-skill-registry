---
name: plaid-expert
description: Expert guidance for Plaid banking API integration including Link, Auth, Transactions, Identity, and webhook handling. Invoke when user mentions Plaid, bank connections, financial data, ACH, or banking APIs.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
model: sonnet
---

# Plaid Integration Expert

## Purpose

Provide comprehensive guidance for integrating Plaid's financial data APIs to connect bank accounts, retrieve transactions, verify identities, and process ACH transfers.

## When to Use

Invoke when user mentions:
- "Plaid" or "banking API"
- "Link" (Plaid Link flow)
- "bank account connection" or "financial data"
- "ACH transfers" or "bank-to-bank payments"
- "transaction history" or "account balance"
- "income verification" or "identity verification"

## Core Products

### 1. Auth
**Purpose:** Retrieve bank account and routing numbers for ACH, wire transfers, and bank-to-bank payments.

**Use cases:**
- ACH payment processing
- Wire transfers
- Bank account verification

### 2. Transactions
**Purpose:** Access transaction history for budgeting, expense tracking, and financial insights.

**Features:**
- Up to 24 months of history
- Categorized transactions
- Merchant information
- Pending and posted transactions

### 3. Identity
**Purpose:** Verify user identity through bank account ownership.

**Data retrieved:**
- Account holder names
- Email addresses
- Phone numbers
- Physical addresses

### 4. Balance
**Purpose:** Real-time account balance checking to prevent payment failures.

**Use cases:**
- Insufficient funds detection
- Payment preflight checks
- Account monitoring

### 5. Investments
**Purpose:** Access holdings and transactions from investment accounts.

**Coverage:**
- Stocks, bonds, ETFs
- 401(k), IRA, brokerage accounts
- Real-time valuations

### 6. Liabilities
**Purpose:** Loan and credit data access.

**Coverage:**
- Student loans
- Mortgages
- Credit cards
- Auto loans

## Plaid Link Integration

### What is Link?

Plaid Link is the client-side component that users interact with to securely connect their bank accounts. It's a modal/iframe that handles the entire authentication flow.

### Link Flow

1. User clicks "Connect Bank Account"
2. Link modal opens
3. User searches for their bank
4. User enters credentials (or OAuth)
5. User selects accounts to link
6. Link returns a `public_token`
7. Exchange `public_token` for `access_token` server-side

### Frontend Integration (React)

**Install:**
```bash
npm install react-plaid-link
```

**Implementation:**
```tsx
import { usePlaidLink } from 'react-plaid-link';

function PlaidLinkButton() {
  const [linkToken, setLinkToken] = useState(null);

  // 1. Create link token (call your backend)
  useEffect(() => {
    async function createLinkToken() {
      const response = await fetch('/api/plaid/create-link-token', {
        method: 'POST',
      });
      const data = await response.json();
      setLinkToken(data.link_token);
    }
    createLinkToken();
  }, []);

  // 2. Configure Link
  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: async (public_token, metadata) => {
      // 3. Exchange public token for access token
      await fetch('/api/plaid/exchange-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ public_token }),
      });
    },
    onExit: (err, metadata) => {
      if (err) console.error(err);
    },
  });

  return (
    <button onClick={() => open()} disabled={!ready}>
      Connect Bank Account
    </button>
  );
}
```

### Backend: Create Link Token

**Node.js example:**
```javascript
const plaid = require('plaid');

const client = new plaid.PlaidApi(
  new plaid.Configuration({
    basePath: plaid.PlaidEnvironments.sandbox,
    baseOptions: {
      headers: {
        'PLAID-CLIENT-ID': process.env.PLAID_CLIENT_ID,
        'PLAID-SECRET': process.env.PLAID_SECRET,
      },
    },
  })
);

// Create link token
app.post('/api/plaid/create-link-token', async (req, res) => {
  const request = {
    user: {
      client_user_id: req.user.id, // Your app's user ID
    },
    client_name: 'Your App Name',
    products: ['auth', 'transactions'],
    country_codes: ['US'],
    language: 'en',
  };

  try {
    const response = await client.linkTokenCreate(request);
    res.json({ link_token: response.data.link_token });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Backend: Exchange Public Token

**Store access token securely in your database:**
```javascript
app.post('/api/plaid/exchange-token', async (req, res) => {
  const { public_token } = req.body;

  try {
    const response = await client.itemPublicTokenExchange({
      public_token: public_token,
    });

    const access_token = response.data.access_token;
    const item_id = response.data.item_id;

    // Store access_token securely in your database
    await db.users.update(req.user.id, {
      plaid_access_token: access_token,
      plaid_item_id: item_id,
    });

    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

## Retrieving Data

### Get Auth (Account/Routing Numbers)

```javascript
async function getAuthData(access_token) {
  const response = await client.authGet({
    access_token: access_token,
  });

  const accounts = response.data.accounts;
  const numbers = response.data.numbers;

  // ACH numbers
  const ach = numbers.ach[0];
  console.log('Account:', ach.account);
  console.log('Routing:', ach.routing);

  return { accounts, numbers };
}
```

### Get Transactions

```javascript
async function getTransactions(access_token) {
  const request = {
    access_token: access_token,
    start_date: '2024-01-01',
    end_date: '2024-12-31',
  };

  const response = await client.transactionsGet(request);
  let transactions = response.data.transactions;

  // Handle pagination
  while (transactions.length < response.data.total_transactions) {
    const paginatedRequest = {
      ...request,
      offset: transactions.length,
    };
    const paginatedResponse = await client.transactionsGet(paginatedRequest);
    transactions = transactions.concat(paginatedResponse.data.transactions);
  }

  return transactions;
}
```

**Transaction object structure:**
```javascript
{
  transaction_id: 'abc123',
  account_id: 'xyz789',
  amount: 12.34, // Positive = money out, Negative = money in
  date: '2024-11-16',
  name: 'Starbucks',
  merchant_name: 'Starbucks',
  category: ['Food and Drink', 'Restaurants', 'Coffee Shop'],
  pending: false,
  payment_channel: 'in store'
}
```

### Get Balance

```javascript
async function getBalance(access_token) {
  const response = await client.accountsBalanceGet({
    access_token: access_token,
  });

  const accounts = response.data.accounts;
  accounts.forEach(account => {
    console.log(`${account.name}: ${account.balances.current}`);
  });

  return accounts;
}
```

### Get Identity

```javascript
async function getIdentity(access_token) {
  const response = await client.identityGet({
    access_token: access_token,
  });

  const identity = response.data.accounts[0].owners[0];
  console.log('Name:', identity.names[0]);
  console.log('Email:', identity.emails[0].data);
  console.log('Phone:', identity.phone_numbers[0].data);

  return response.data;
}
```

## Webhooks

### Setup Webhook URL

Configure in Plaid Dashboard or via API when creating link token:
```javascript
{
  webhook: 'https://your-domain.com/api/plaid/webhook',
}
```

### Webhook Verification

**Verify webhook authenticity:**
```javascript
const crypto = require('crypto');

app.post('/api/plaid/webhook', express.json(), async (req, res) => {
  const { webhook_type, webhook_code } = req.body;

  // Verify webhook signature
  const plaidSignature = req.headers['plaid-verification'];
  const timestamp = req.headers['plaid-timestamp'];

  const payload = JSON.stringify(req.body);
  const hash = crypto
    .createHmac('sha256', process.env.PLAID_WEBHOOK_SECRET)
    .update(`${timestamp}.${payload}`)
    .digest('hex');

  if (hash !== plaidSignature) {
    return res.status(401).send('Invalid signature');
  }

  // Handle webhook events
  if (webhook_type === 'TRANSACTIONS') {
    switch (webhook_code) {
      case 'INITIAL_UPDATE':
        console.log('Initial transactions available');
        break;
      case 'DEFAULT_UPDATE':
        console.log('New transactions available');
        // Fetch new transactions
        break;
      case 'TRANSACTIONS_REMOVED':
        console.log('Transactions removed');
        break;
    }
  }

  res.json({ received: true });
});
```

**Common webhook events:**
- `TRANSACTIONS: INITIAL_UPDATE` - First batch ready
- `TRANSACTIONS: DEFAULT_UPDATE` - New transactions available
- `ITEM: ERROR` - Connection issue
- `ITEM: PENDING_EXPIRATION` - Credentials expiring soon
- `AUTH: AUTOMATICALLY_VERIFIED` - Micro-deposit verification complete

## Environments

**Sandbox** (testing):
```javascript
basePath: plaid.PlaidEnvironments.sandbox
```
- Test credentials: `user_good` / `pass_good`
- No real bank connections
- Simulate transactions

**Development** (limited live connections):
```javascript
basePath: plaid.PlaidEnvironments.development
```
- Up to 100 live bank connections
- Free for testing

**Production** (live):
```javascript
basePath: plaid.PlaidEnvironments.production
```
- Real bank connections
- Requires approval and billing

## Error Handling

### Update Mode (Re-authentication)

When credentials expire or change:
```javascript
const { open } = usePlaidLink({
  token: linkToken,
  onSuccess: async (public_token, metadata) => {
    // Item re-linked successfully
  },
});

// Create link token with update mode
const request = {
  access_token: existing_access_token,
  // ... other config
};
```

### Common Errors

**ITEM_LOGIN_REQUIRED:**
- User needs to re-authenticate
- Solution: Trigger Link in update mode

**RATE_LIMIT_EXCEEDED:**
- Too many requests
- Solution: Implement exponential backoff

**PRODUCT_NOT_READY:**
- Data still syncing
- Solution: Wait for webhook or retry

## Security Best Practices

1. **Never expose secret keys client-side:**
   - Use `PLAID_CLIENT_ID` and `PLAID_SECRET` server-side only
   - Link tokens are safe for client use

2. **Encrypt access tokens:**
   - Store access tokens encrypted in database
   - Never log access tokens

3. **Verify webhook signatures:**
   - Prevents forged webhooks
   - Use crypto verification

4. **Use HTTPS:**
   - Required for webhook endpoints
   - Required for production

5. **Implement proper user consent:**
   - Clear disclosure about data access
   - Follow Plaid's branding guidelines

## Next.js API Route Example

**Create link token:**
```typescript
// app/api/plaid/create-link-token/route.ts
import { NextResponse } from 'next/server';
import { Configuration, PlaidApi, PlaidEnvironments } from 'plaid';

const client = new PlaidApi(
  new Configuration({
    basePath: PlaidEnvironments.sandbox,
    baseOptions: {
      headers: {
        'PLAID-CLIENT-ID': process.env.PLAID_CLIENT_ID!,
        'PLAID-SECRET': process.env.PLAID_SECRET!,
      },
    },
  })
);

export async function POST(req: Request) {
  const session = await getSession();

  const response = await client.linkTokenCreate({
    user: { client_user_id: session.user.id },
    client_name: 'Your App',
    products: ['auth', 'transactions'],
    country_codes: ['US'],
    language: 'en',
  });

  return NextResponse.json({ link_token: response.data.link_token });
}
```

## Testing in Sandbox

**Test credentials:**
- Username: `user_good`
- Password: `pass_good`
- MFA: `1234`

**Test institutions:**
- "Platypus Bank" - Full feature support
- "Tartan Bank" - OAuth flow
- "Houndstooth Bank" - Error testing

## Useful Resources

- **Official Docs:** https://plaid.com/docs/
- **API Reference:** https://plaid.com/docs/api/
- **Plaid Link:** https://plaid.com/docs/link/
- **Webhooks:** https://plaid.com/docs/api/webhooks/
- **Quickstart:** https://github.com/plaid/quickstart

## Implementation Checklist

- [ ] Sign up for Plaid account
- [ ] Get client ID and secret keys
- [ ] Install Plaid SDK: `npm install plaid react-plaid-link`
- [ ] Set environment variables
- [ ] Implement link token creation endpoint
- [ ] Implement token exchange endpoint
- [ ] Integrate Plaid Link on frontend
- [ ] Store access tokens securely (encrypted)
- [ ] Set up webhook endpoint with verification
- [ ] Handle ITEM_LOGIN_REQUIRED errors
- [ ] Test with sandbox credentials
- [ ] Request production access
- [ ] Implement error handling and retry logic
- [ ] Add proper user consent/disclosure
