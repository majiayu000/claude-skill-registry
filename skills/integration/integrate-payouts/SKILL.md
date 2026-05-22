---
name: integrate-payouts
description: Complete guide to integrating Payram payout functionality for sending cryptocurrency payments to recipients
---

# Integrate Payram Payouts

## Overview

This skill provides comprehensive instructions for integrating Payram payout functionality into your application. Payouts enable you to send cryptocurrency payments to recipients programmatically. You'll learn how to create payouts, check their status, and handle the complete payout lifecycle using the official SDK.

## When to Use This Skill

Use this skill when you need to:

- Send cryptocurrency payments to customers, vendors, or partners
- Implement automated disbursement systems
- Create withdrawal/cashout functionality
- Process refunds or rewards in cryptocurrency
- Track payout status and transaction details

## Prerequisites

Before starting, ensure you have:

- Completed the `setup-payram` skill (environment configured with API credentials)
- Reviewed `docs/payram-docs-live/api-integration/payouts-apis/create-payouts.md`
- Installed the Payram SDK: `npm install payram`
- Sufficient balance in your merchant account for payouts

---

## Instructions

### Part 1: Understanding Payout Flow

#### 1.1 Payout Lifecycle

Payouts progress through these states:

1. **pending-otp-verification** - Awaiting OTP confirmation (if required)
2. **pending-approval** - Awaiting manual approval (if thresholds require it)
3. **pending** - Queued for processing
4. **initiated** - Processing has started
5. **sent** - Transaction broadcast to blockchain
6. **processed** - Confirmed on blockchain
7. **failed** - Transaction failed (insufficient balance, invalid address)
8. **rejected** - Manually rejected by admin
9. **cancelled** - Cancelled before processing

**Action:** Monitor payout status to track progression through these states.

#### 1.2 Required Information

To create a payout, you need:

- **email**: Merchant email associated with payout
- **blockchainCode**: Blockchain network (e.g., 'ETH', 'BTC', 'MATIC')
- **currencyCode**: Currency to send (e.g., 'USDC', 'USDT', 'BTC')
- **amount**: Amount as string (e.g., '125.50')
- **toAddress**: Recipient wallet address
- **customerID**: Your internal reference ID
- **mobileNumber**: Recipient phone number (format: +15555555555)
- **residentialAddress**: Recipient address (KYC/compliance)

---

### Part 2: SDK Integration (Node.js/TypeScript)

#### 2.1 Install SDK

```bash
npm install payram
# or
yarn add payram
# or
pnpm add payram
```

#### 2.2 Create Payout with SDK

**File:** `src/payram/payouts/createPayout.ts`

```typescript
import { Payram, CreatePayoutRequest, MerchantPayout, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
  config: {
    timeoutMs: 10_000, // Optional: request timeout
    maxRetries: 2, // Optional: retry failed requests
    retryPolicy: 'safe', // Optional: only retry safe methods
    allowInsecureHttp: false, // Optional: require HTTPS
  },
});

export async function createPayout(payload: CreatePayoutRequest): Promise<MerchantPayout> {
  try {
    const payout = await payram.payouts.createPayout(payload);

    console.log('Payout created:', {
      id: payout.id,
      status: payout.status,
      blockchain: payout.blockchainCode,
      currency: payout.currencyCode,
      amount: payout.amount,
    });

    return payout;
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        requestId: error.requestId,
        isRetryable: error.isRetryable,
        message: error.message,
      });
    }
    throw error;
  }
}

// Example invocation
await createPayout({
  email: 'merchant@example.com',
  blockchainCode: 'ETH',
  currencyCode: 'USDC',
  amount: '125.50',
  toAddress: '0xfeedfacecafebeefdeadbeefdeadbeefdeadbeef',
  customerID: 'cust_123',
  mobileNumber: '+15555555555',
  residentialAddress: '1 Market St, San Francisco, CA 94105',
});
```

**Field Details:**

- **email**: Must match a verified merchant email in your Payram account
- **blockchainCode**: See supported networks in `docs/payram-docs-live/support/supported-networks-and-coins.md`
- **currencyCode**: Token/coin code (must be supported on chosen blockchain)
- **amount**: String representation of amount (NOT a number) - e.g., '125.50', not 125.50
- **toAddress**: Recipient wallet address (validated for blockchain compatibility)
- **customerID**: Your internal reference (for tracking/reconciliation)
- **mobileNumber**: E.164 format required (+country_code + number)
- **residentialAddress**: Full address for compliance purposes

#### 2.3 Check Payout Status

**File:** `src/payram/payouts/payoutStatus.ts`

```typescript
import { Payram, MerchantPayout, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function getPayoutStatus(payoutId: number): Promise<MerchantPayout> {
  if (!payoutId) {
    throw new Error('A numeric payoutId from the createPayout response is required.');
  }

  try {
    const payout = await payram.payouts.getPayoutById(payoutId);

    console.log('Payout status:', {
      id: payout.id,
      status: payout.status,
      transactionHash: payout.transactionHash,
      blockchain: payout.blockchainCode,
      currency: payout.currencyCode,
      amount: payout.amount,
      createdAt: payout.createdAt,
      updatedAt: payout.updatedAt,
    });

    return payout;
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        requestId: error.requestId,
        isRetryable: error.isRetryable,
      });
    }
    throw error;
  }
}

// Example usage
const payout = await getPayoutStatus(120);
```

**Response Fields:**

- **id**: Unique payout identifier
- **status**: Current payout state (see lifecycle above)
- **transactionHash**: Blockchain transaction hash (available when status is 'sent' or 'processed')
- **blockchainCode**: Network used for payout
- **currencyCode**: Currency sent
- **amount**: Amount sent (as string)
- **toAddress**: Recipient address
- **customerID**: Your reference ID
- **createdAt**: Payout creation timestamp
- **updatedAt**: Last status update timestamp

---

### Part 3: Status Monitoring Patterns

#### 3.1 Polling Pattern

Use polling when webhooks are not available:

```typescript
async function pollPayoutStatus(payoutId: number, maxAttempts = 20): Promise<MerchantPayout> {
  const finalStates = ['processed', 'failed', 'rejected', 'cancelled'];

  for (let i = 0; i < maxAttempts; i++) {
    const payout = await getPayoutStatus(payoutId);

    // Check if payout reached final state
    if (finalStates.includes(payout.status)) {
      return payout;
    }

    // Wait before next check (exponential backoff)
    const delay = Math.min(5000 * Math.pow(1.5, i), 60000); // Cap at 60s
    console.log(`Payout ${payoutId} status: ${payout.status}, checking again in ${delay}ms`);
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  throw new Error(`Payout ${payoutId} did not reach final state after ${maxAttempts} attempts`);
}

// Usage
try {
  const payout = await createPayout({ ... });
  const finalPayout = await pollPayoutStatus(payout.id);

  if (finalPayout.status === 'processed') {
    console.log('Payout successful! Tx:', finalPayout.transactionHash);
  } else {
    console.error('Payout failed with status:', finalPayout.status);
  }
} catch (error) {
  console.error('Payout processing error:', error);
}
```

#### 3.2 Webhook Pattern (Recommended)

For production systems, use webhooks for real-time updates:

```typescript
// See 'handle-webhooks' skill for complete webhook setup

// Express webhook handler example
router.post('/webhooks/payram/payout-status', async (req, res) => {
  const event = req.body;

  if (event.eventType === 'payout.status.updated') {
    const payoutId = event.data.id;
    const status = event.data.status;

    // Update your database
    await db.payouts.update({
      where: { payramPayoutId: payoutId },
      data: {
        status,
        transactionHash: event.data.transactionHash,
        updatedAt: new Date(),
      },
    });

    // Notify customer if payout completed
    if (status === 'processed') {
      await sendNotification(event.data.customerID, {
        message: 'Your payout has been processed!',
        transactionHash: event.data.transactionHash,
      });
    }
  }

  res.status(200).json({ received: true });
});
```

---

### Part 4: Framework Integration Examples

#### 4.1 Express.js Route

**File:** `src/routes/payram/payouts.ts`

```typescript
import { Router } from 'express';
import { Payram, CreatePayoutRequest, isPayramSDKError } from 'payram';

const router = Router();
const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

router.post('/api/payouts/payram', async (req, res) => {
  const payload = req.body as Partial<CreatePayoutRequest>;

  // Validate required fields
  const requiredFields = [
    'email',
    'blockchainCode',
    'currencyCode',
    'amount',
    'toAddress',
    'customerID',
    'mobileNumber',
    'residentialAddress',
  ];

  const missing = requiredFields.filter((field) => !payload[field as keyof CreatePayoutRequest]);
  if (missing.length > 0) {
    return res.status(400).json({
      error: 'MISSING_REQUIRED_FIELDS',
      missing,
    });
  }

  try {
    const payout = await payram.payouts.createPayout(payload as CreatePayoutRequest);

    return res.status(201).json({
      id: payout.id,
      status: payout.status,
      blockchain: payout.blockchainCode,
      currency: payout.currencyCode,
      amount: payout.amount,
    });
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        requestId: error.requestId,
        retryable: error.isRetryable,
      });
    }
    return res.status(502).json({ error: 'PAYRAM_CREATE_PAYOUT_FAILED' });
  }
});

router.get('/api/payouts/payram/:payoutId', async (req, res) => {
  const payoutId = parseInt(req.params.payoutId, 10);

  if (isNaN(payoutId)) {
    return res.status(400).json({ error: 'INVALID_PAYOUT_ID' });
  }

  try {
    const payout = await payram.payouts.getPayoutById(payoutId);
    return res.json(payout);
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', error);
    }
    return res.status(502).json({ error: 'PAYRAM_STATUS_CHECK_FAILED' });
  }
});

export default router;
```

#### 4.2 Next.js App Router

**File:** `app/api/payram/create-payout/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Payram, CreatePayoutRequest, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function POST(request: NextRequest) {
  const payload = (await request.json()) as Partial<CreatePayoutRequest>;

  // Validate required fields
  const requiredFields = [
    'email',
    'blockchainCode',
    'currencyCode',
    'amount',
    'toAddress',
    'customerID',
    'mobileNumber',
    'residentialAddress',
  ];

  const missing = requiredFields.filter((field) => !payload[field as keyof CreatePayoutRequest]);
  if (missing.length > 0) {
    return NextResponse.json(
      {
        error: 'MISSING_REQUIRED_FIELDS',
        missing,
      },
      { status: 400 },
    );
  }

  try {
    const payout = await payram.payouts.createPayout(payload as CreatePayoutRequest);

    return NextResponse.json({
      id: payout.id,
      status: payout.status,
      blockchain: payout.blockchainCode,
      currency: payout.currencyCode,
      amount: payout.amount,
    });
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        requestId: error.requestId,
      });
    }
    return NextResponse.json({ error: 'PAYRAM_CREATE_PAYOUT_FAILED' }, { status: 502 });
  }
}
```

**File:** `app/api/payram/payout-status/[payoutId]/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Payram, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function GET(request: NextRequest, { params }: { params: { payoutId: string } }) {
  const payoutId = parseInt(params.payoutId, 10);

  if (isNaN(payoutId)) {
    return NextResponse.json({ error: 'INVALID_PAYOUT_ID' }, { status: 400 });
  }

  try {
    const payout = await payram.payouts.getPayoutById(payoutId);
    return NextResponse.json(payout);
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', error);
    }
    return NextResponse.json({ error: 'PAYRAM_STATUS_CHECK_FAILED' }, { status: 502 });
  }
}
```

---

## Best Practices

### 1. Amount Formatting

**Critical:** Amount must be a string, not a number.

```typescript
// ✅ CORRECT
amount: '125.50';

// ❌ WRONG - Will cause validation errors
amount: 125.5;
amount: 125;
```

**Why:** Ensures precision for financial calculations. JavaScript numbers lose precision with decimals.

### 2. Address Validation

Always validate recipient addresses before creating payouts:

```typescript
function validateAddress(address: string, blockchainCode: string): boolean {
  const patterns: Record<string, RegExp> = {
    ETH: /^0x[a-fA-F0-9]{40}$/,
    BTC: /^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$/,
    MATIC: /^0x[a-fA-F0-9]{40}$/,
    // Add more patterns as needed
  };

  const pattern = patterns[blockchainCode];
  if (!pattern) {
    throw new Error(`Unknown blockchain: ${blockchainCode}`);
  }

  return pattern.test(address);
}

// Usage
if (!validateAddress(toAddress, blockchainCode)) {
  throw new Error('Invalid recipient address for blockchain');
}
```

### 3. Balance Checking

Check merchant balance before creating large payouts:

```typescript
async function checkBalanceBeforePayout(
  blockchainCode: string,
  currencyCode: string,
  amount: string,
): Promise<boolean> {
  // Implement balance check via Payram API or your internal records
  const balance = await getMerchantBalance(blockchainCode, currencyCode);
  const requestedAmount = parseFloat(amount);

  if (balance < requestedAmount) {
    throw new Error(`Insufficient balance. Required: ${amount}, Available: ${balance}`);
  }

  return true;
}
```

### 4. Database Storage

Store payout records for reconciliation:

```sql
CREATE TABLE payouts (
    id SERIAL PRIMARY KEY,
    payram_payout_id INTEGER UNIQUE NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    blockchain_code VARCHAR(50) NOT NULL,
    currency_code VARCHAR(50) NOT NULL,
    amount DECIMAL(20, 8) NOT NULL,
    to_address VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    transaction_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_payram_payout_id ON payouts(payram_payout_id);
CREATE INDEX idx_customer_id ON payouts(customer_id);
CREATE INDEX idx_status ON payouts(status);
```

### 5. Error Handling

Implement comprehensive error handling:

```typescript
async function createPayoutWithRetry(
  payload: CreatePayoutRequest,
  maxRetries = 3,
): Promise<MerchantPayout> {
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await createPayout(payload);
    } catch (error) {
      lastError = error as Error;

      if (isPayramSDKError(error)) {
        // Don't retry validation errors
        if (error.status === 400) {
          throw error;
        }

        // Don't retry if not retryable
        if (!error.isRetryable) {
          throw error;
        }
      }

      if (attempt < maxRetries) {
        const delay = 1000 * Math.pow(2, attempt);
        console.log(`Payout attempt ${attempt} failed, retrying in ${delay}ms`);
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError || new Error('Payout creation failed after retries');
}
```

---

## Troubleshooting

### Error: "Insufficient balance" (400)

**Cause:** Merchant account doesn't have enough funds.

**Solution:**

1. Check merchant balance in Payram dashboard
2. Deposit funds to merchant account
3. Verify correct blockchain/currency combination
4. Account for gas fees in balance calculation

### Error: "Invalid address format" (400)

**Cause:** Recipient address doesn't match blockchain format.

**Solution:**

- Ethereum/Polygon: Must start with '0x' and be 42 characters
- Bitcoin: Must start with '1' or '3' and be 26-35 characters
- Validate address with blockchain-specific regex patterns
- Test address format before submitting payout

### Error: "Unsupported blockchain/currency" (400)

**Cause:** Requested blockchain or currency not supported.

**Solution:**

1. Check `docs/payram-docs-live/support/supported-networks-and-coins.md`
2. Verify currency is available on chosen blockchain
3. Use correct currency codes (e.g., 'USDC' not 'usdc')
4. Ensure merchant account supports requested network

### Payout stuck in "pending-approval"

**Cause:** Payout exceeds auto-approval threshold.

**Solution:**

- Contact Payram support to adjust approval thresholds
- Wait for manual approval from admin
- Configure approval rules in merchant dashboard
- Split large payouts into smaller amounts

### Error: "Invalid mobile number format" (400)

**Cause:** Phone number not in E.164 format.

**Solution:**

```typescript
// ✅ CORRECT
mobileNumber: '+15555555555';

// ❌ WRONG
mobileNumber: '555-555-5555';
mobileNumber: '5555555555';
```

Use E.164 format: +[country_code][number] (no spaces, dashes, or parentheses)

### Payout failed after "sent" status

**Cause:** Blockchain transaction reverted or failed.

**Solution:**

- Check transaction hash on blockchain explorer
- Verify recipient address accepts the currency
- Check for smart contract issues (ERC-20 tokens)
- Review gas price settings (may be too low)
- Contact Payram support with transaction hash

---

## Related Skills

- **setup-payram**: Configure environment and test connectivity
- **integrate-payments**: Accept cryptocurrency payments from customers
- **handle-webhooks**: Receive real-time payout status updates

---

## Summary

You now have complete payout integration:

1. **Payout creation**: Use `payram.payouts.createPayout()` with required fields
2. **Status monitoring**: Poll with `getPayoutById()` or use webhooks
3. **Framework integration**: Ready-to-use Express and Next.js handlers
4. **Best practices**: Amount formatting, address validation, balance checking, error handling

**Key Reminders:**

- Amount must be a string (e.g., '125.50')
- Validate addresses before creating payouts
- Store payout IDs for status tracking
- Use webhooks for production systems
- Handle all payout states in your application

**Next Steps:**

- Implement payout creation endpoint
- Add status polling or webhook handlers
- Set up database tables for payout records
- Test with small amounts first
- Review `docs/payram-docs-live/api-integration/payouts-apis.md` for advanced options
