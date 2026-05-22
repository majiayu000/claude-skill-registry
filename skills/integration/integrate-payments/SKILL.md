---
name: integrate-payments
description: Complete guide to integrating Payram payment creation and status checking across all supported languages and frameworks
---

# Integrate Payram Payments

## Overview

This skill provides comprehensive instructions for integrating Payram payment functionality into your application. You'll learn how to create payment checkouts, redirect customers to Payram's hosted payment page, and check payment status using either the official SDK (Node.js/TypeScript) or raw HTTP calls (Python, Go, PHP, Java).

## When to Use This Skill

Use this skill when you need to:

- Accept cryptocurrency payments from customers
- Create Payram payment checkouts programmatically
- Check the status of existing payments
- Integrate payments into Express, Next.js, or other frameworks
- Implement payment flows across different programming languages

## Prerequisites

Before starting, ensure you have:

- Completed the `setup-payram` skill (environment configured with API credentials)
- Reviewed `docs/payram-docs-live/api-integration/payments-api/create-payment.md`
- Decided whether to use the SDK (TypeScript/JavaScript) or HTTP approach (other languages)

---

## Instructions

### Part 1: Understanding Payment Flow

#### 1.1 Payment Creation Response

When you create a payment, Payram returns:

```typescript
{
  "reference_id": "unique-payment-identifier",
  "url": "https://checkout.payram.com/...",
  "host": "checkout.payram.com"
}
```

**Action:** Redirect your customer to the `url` field for payment completion. Store `reference_id` for status checks.

#### 1.2 Payment States

Payments transition through these states:

- `OPEN` - Payment created, awaiting customer action
- `FILLED` - Customer sent funds, awaiting confirmation
- `COMPLETED` - Payment confirmed and settled
- `EXPIRED` - Payment window closed
- `CANCELLED` - Payment manually cancelled

**Action:** Poll payment status using the `reference_id` to track state changes.

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

#### 2.2 Create Payment with SDK

**File:** `src/payram/payments/createPayment.ts`

```typescript
import { Payram, InitiatePaymentRequest, InitiatePaymentResponse, isPayramSDKError } from 'payram';

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

export async function createCheckout(
  payload: InitiatePaymentRequest,
): Promise<InitiatePaymentResponse> {
  try {
    const checkout = await payram.payments.initiatePayment(payload);
    console.log('Redirect customer to:', checkout.url);
    console.log('Payment reference:', checkout.reference_id);
    return checkout;
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        requestId: error.requestId,
        retryable: error.isRetryable,
      });
    }
    throw error;
  }
}

// Example usage
await createCheckout({
  customerEmail: 'customer@example.com',
  customerId: 'cust_123',
  amountInUSD: 49.99,
});
```

**Required Fields:**

- `customerEmail`: Customer's email address
- `customerId`: Your internal customer identifier
- `amountInUSD`: Payment amount in USD

**Optional Fields:**

- `settlementCurrency`: Currency for settlement (default: USD)
- `memo`: Internal reference or description
- `redirectUrl`: Custom URL to redirect after payment

#### 2.3 Check Payment Status with SDK

**File:** `src/payram/payments/paymentStatus.ts`

```typescript
import { Payram, PaymentRequestData, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function getPaymentStatus(referenceId: string): Promise<PaymentRequestData> {
  if (!referenceId) {
    throw new Error('referenceId is required to fetch a Payram payment.');
  }

  try {
    const payment = await payram.payments.getPaymentRequest(referenceId);
    console.log('Latest payment state:', payment.paymentState);
    console.log('Amount paid:', payment.amountPaid);
    console.log('Transaction hash:', payment.transactionHash);
    return payment;
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        errorCode: error.error,
        requestId: error.requestId,
      });
    }
    throw error;
  }
}
```

**Usage Pattern:**

```typescript
// After creating payment
const checkout = await createCheckout({ ... });

// Poll for status changes
const payment = await getPaymentStatus(checkout.reference_id);

if (payment.paymentState === 'COMPLETED') {
  // Process successful payment
  console.log('Payment completed! Tx:', payment.transactionHash);
}
```

---

### Part 3: HTTP Integration (Python, Go, PHP, Java)

#### 3.1 Python Payment Creation

**File:** `scripts/payram/create_payment.py`

```python
import os
import requests

PAYRAM_BASE_URL = os.environ['PAYRAM_BASE_URL']
PAYRAM_API_KEY = os.environ['PAYRAM_API_KEY']

def create_payment(customer_email: str, customer_id: str, amount_in_usd: float):
    payload = {
        'customerEmail': customer_email,
        'customerId': customer_id,
        'amountInUSD': amount_in_usd,
    }

    headers = {
        'Content-Type': 'application/json',
        'API-Key': PAYRAM_API_KEY,  # Use API-Key header, NOT Authorization
    }

    response = requests.post(
        f"{PAYRAM_BASE_URL}/api/v1/payment",
        json=payload,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    checkout = response.json()
    print('Reference:', checkout['reference_id'])
    print('Checkout URL:', checkout['url'])
    return checkout

# Example usage
if __name__ == '__main__':
    checkout = create_payment('customer@example.com', 'cust_123', 49.99)
```

#### 3.2 Python Payment Status

**File:** `scripts/payram/payment_status.py`

```python
import os
import requests

PAYRAM_BASE_URL = os.environ['PAYRAM_BASE_URL']
PAYRAM_API_KEY = os.environ['PAYRAM_API_KEY']

def get_payment_status(reference_id: str):
    if not reference_id:
        raise ValueError('reference_id is required')

    headers = {
        'API-Key': PAYRAM_API_KEY,
        'Accept': 'application/json',
    }

    response = requests.get(
        f"{PAYRAM_BASE_URL}/api/v1/payment/reference/{reference_id}",
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    payment = response.json()
    print('Payment State:', payment['paymentState'])
    print('Amount Paid:', payment.get('amountPaid'))
    return payment

# Example usage
if __name__ == '__main__':
    payment = get_payment_status('your-reference-id-here')
```

#### 3.3 Go Payment Creation

**File:** `internal/payram/create_payment.go`

```go
package payram

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
)

type InitiatePaymentRequest struct {
    CustomerEmail string  `json:"customerEmail"`
    CustomerID    string  `json:"customerId"`
    AmountInUSD   float64 `json:"amountInUSD"`
}

type InitiatePaymentResponse struct {
    ReferenceID string `json:"reference_id"`
    URL         string `json:"url"`
    Host        string `json:"host"`
}

func CreatePayment(email, customerID string, amount float64) (*InitiatePaymentResponse, error) {
    body, err := json.Marshal(InitiatePaymentRequest{
        CustomerEmail: email,
        CustomerID:    customerID,
        AmountInUSD:   amount,
    })
    if err != nil {
        return nil, fmt.Errorf("marshal payment request: %w", err)
    }

    url := fmt.Sprintf("%s/api/v1/payment", os.Getenv("PAYRAM_BASE_URL"))
    req, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(body))
    if err != nil {
        return nil, fmt.Errorf("create request: %w", err)
    }

    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("API-Key", os.Getenv("PAYRAM_API_KEY"))

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("execute request: %w", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode >= 400 {
        return nil, fmt.Errorf("payram returned status %d", resp.StatusCode)
    }

    var checkout InitiatePaymentResponse
    if err := json.NewDecoder(resp.Body).Decode(&checkout); err != nil {
        return nil, fmt.Errorf("decode response: %w", err)
    }

    return &checkout, nil
}
```

#### 3.4 PHP Payment Creation

**File:** `app/Services/Payram/CreatePayment.php`

```php
<?php

namespace App\Services\Payram;

class CreatePayment
{
    public function execute(string $customerEmail, string $customerId, float $amountInUSD): array
    {
        $payload = [
            'customerEmail' => $customerEmail,
            'customerId' => $customerId,
            'amountInUSD' => $amountInUSD,
        ];

        $ch = curl_init(getenv('PAYRAM_BASE_URL') . '/api/v1/payment');
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'API-Key: ' . getenv('PAYRAM_API_KEY'),
            ],
            CURLOPT_POSTFIELDS => json_encode($payload),
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 30,
        ]);

        $response = curl_exec($ch);
        $statusCode = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);

        if ($response === false || $statusCode >= 400) {
            throw new \RuntimeException('Payram create payment failed: ' . curl_error($ch));
        }

        curl_close($ch);

        $checkout = json_decode($response, true);
        error_log('Payram Reference: ' . $checkout['reference_id']);
        error_log('Checkout URL: ' . $checkout['url']);

        return $checkout;
    }
}
```

#### 3.5 Java Payment Creation

**File:** `src/main/java/com/acme/payram/PayramPaymentClient.java`

```java
package com.acme.payram;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class PayramPaymentClient {
    private final HttpClient http = HttpClient.newHttpClient();
    private final String baseUrl = System.getenv("PAYRAM_BASE_URL");
    private final String apiKey = System.getenv("PAYRAM_API_KEY");

    public HttpResponse<String> createPayment(
        String customerEmail,
        String customerId,
        double amountInUSD
    ) throws Exception {
        var payload = String.format("""
            {
              "customerEmail": "%s",
              "customerId": "%s",
              "amountInUSD": %.2f
            }
            """, customerEmail, customerId, amountInUSD);

        var request = HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + "/api/v1/payment"))
            .header("Content-Type", "application/json")
            .header("API-Key", apiKey)
            .POST(HttpRequest.BodyPublishers.ofString(payload))
            .build();

        HttpResponse<String> response = http.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() >= 400) {
            throw new RuntimeException("Payram create payment failed: " + response.statusCode());
        }

        System.out.println("Payment created: " + response.body());
        return response;
    }
}
```

---

### Part 4: Framework Integration

#### 4.1 Express.js Route

**File:** `src/routes/payram/payments.ts`

```typescript
import { Router } from 'express';
import { Payram, InitiatePaymentRequest, isPayramSDKError } from 'payram';

const router = Router();
const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

router.post('/api/payments/payram', async (req, res) => {
  const payload = req.body as Partial<InitiatePaymentRequest>;

  // Validate required fields
  if (!payload?.customerEmail || !payload.customerId || typeof payload.amountInUSD !== 'number') {
    return res.status(400).json({ error: 'MISSING_REQUIRED_FIELDS' });
  }

  try {
    const checkout = await payram.payments.initiatePayment({
      customerEmail: payload.customerEmail,
      customerId: payload.customerId,
      amountInUSD: payload.amountInUSD,
    });

    return res.status(201).json({
      referenceId: checkout.reference_id,
      checkoutUrl: checkout.url,
    });
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        requestId: error.requestId,
        retryable: error.isRetryable,
      });
    }
    return res.status(502).json({ error: 'PAYRAM_CREATE_PAYMENT_FAILED' });
  }
});

router.get('/api/payments/payram/:referenceId', async (req, res) => {
  const { referenceId } = req.params;

  try {
    const payment = await payram.payments.getPaymentRequest(referenceId);
    return res.json(payment);
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', error);
    }
    return res.status(502).json({ error: 'PAYRAM_STATUS_CHECK_FAILED' });
  }
});

export default router;
```

**Integration:** Wire into Express app:

```typescript
import payramPaymentsRouter from './routes/payram/payments';
app.use(payramPaymentsRouter);
```

#### 4.2 Next.js App Router

**File:** `app/api/payram/create-payment/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Payram, InitiatePaymentRequest, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function POST(request: NextRequest) {
  const payload = (await request.json()) as Partial<InitiatePaymentRequest>;

  // Validate required fields
  if (!payload?.customerEmail || !payload.customerId || typeof payload.amountInUSD !== 'number') {
    return NextResponse.json({ error: 'MISSING_REQUIRED_FIELDS' }, { status: 400 });
  }

  try {
    const checkout = await payram.payments.initiatePayment({
      customerEmail: payload.customerEmail,
      customerId: payload.customerId,
      amountInUSD: payload.amountInUSD,
    });

    return NextResponse.json({
      referenceId: checkout.reference_id,
      checkoutUrl: checkout.url,
    });
  } catch (error) {
    if (isPayramSDKError(error)) {
      console.error('Payram Error:', {
        status: error.status,
        requestId: error.requestId,
      });
    }
    return NextResponse.json({ error: 'PAYRAM_CREATE_PAYMENT_FAILED' }, { status: 502 });
  }
}
```

**File:** `app/api/payram/status/[referenceId]/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { Payram, isPayramSDKError } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

export async function GET(request: NextRequest, { params }: { params: { referenceId: string } }) {
  try {
    const payment = await payram.payments.getPaymentRequest(params.referenceId);
    return NextResponse.json(payment);
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

### 1. Authentication & Security

**Critical:** Payram uses `API-Key` header, NOT `Authorization: Bearer`.

```typescript
// ✅ CORRECT
headers: {
  'API-Key': process.env.PAYRAM_API_KEY
}

// ❌ WRONG - Will be rejected
headers: {
  'Authorization': `Bearer ${process.env.PAYRAM_API_KEY}`
}
```

**Actions:**

- Never expose API keys in client-side code
- Create payments only from server-side routes
- Use environment variables for credentials
- Rotate API keys periodically

### 2. Error Handling

**SDK Errors:**

```typescript
if (isPayramSDKError(error)) {
  // Access structured error data
  console.error({
    status: error.status, // HTTP status code
    requestId: error.requestId, // Trace request in logs
    retryable: error.isRetryable, // Safe to retry?
    message: error.message,
  });
}
```

**HTTP Errors:**

```python
try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
except requests.HTTPError as e:
    # Log error details for debugging
    print(f"Status: {e.response.status_code}")
    print(f"Body: {e.response.text}")
    raise
```

### 3. Status Polling

**Pattern:**

```typescript
async function pollPaymentStatus(referenceId: string, maxAttempts = 10) {
  for (let i = 0; i < maxAttempts; i++) {
    const payment = await getPaymentStatus(referenceId);

    if (payment.paymentState === 'COMPLETED') {
      return payment;
    }

    if (payment.paymentState === 'EXPIRED' || payment.paymentState === 'CANCELLED') {
      throw new Error(`Payment ${payment.paymentState.toLowerCase()}`);
    }

    // Wait before next check (exponential backoff)
    await new Promise((resolve) => setTimeout(resolve, Math.min(1000 * Math.pow(2, i), 30000)));
  }

  throw new Error('Payment status check timeout');
}
```

**Alternative:** Use webhooks (see `handle-webhooks` skill) for real-time status updates instead of polling.

### 4. Reference ID Storage

**Database Schema Example:**

```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    payram_reference_id VARCHAR(255) UNIQUE NOT NULL,
    amount_usd DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'OPEN',
    checkout_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_payram_reference ON payments(payram_reference_id);
CREATE INDEX idx_customer_id ON payments(customer_id);
```

**Action:** Always store `reference_id` immediately after creating payment.

---

## Troubleshooting

### Error: "API key invalid" (401)

**Cause:** Using wrong header or incorrect API key.

**Solution:**

1. Verify you're using `API-Key` header (NOT `Authorization`)
2. Check `.env` file has correct `PAYRAM_API_KEY`
3. Ensure no extra spaces/newlines in API key
4. Verify API key hasn't been rotated/revoked

### Error: "Merchant not found" (404)

**Cause:** Incorrect base URL or merchant doesn't exist.

**Solution:**

1. Verify `PAYRAM_BASE_URL` in `.env`
2. Ensure URL includes protocol (`https://`)
3. Check for typos in merchant subdomain
4. Confirm merchant account is active

### Error: "Invalid amount" (400)

**Cause:** Amount validation failed.

**Solution:**

- Ensure `amountInUSD` is a positive number
- Check amount has maximum 2 decimal places
- Verify amount meets minimum threshold (typically $1.00)
- Don't send amount as string (use number type)

### Payment stuck in OPEN state

**Cause:** Customer hasn't completed payment or payment expired.

**Solution:**

- Check payment expiration time (default: 30 minutes)
- Verify customer was redirected to checkout URL
- Generate new payment if expired
- Review webhook logs for missed updates

### SDK installation fails

**Cause:** Package registry issues or version conflicts.

**Solution:**

```bash
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install payram

# Try alternative registry
npm install payram --registry=https://registry.npmjs.org/
```

---

## Related Skills

- **setup-payram**: Configure environment and test connectivity
- **handle-webhooks**: Receive real-time payment status updates
- **integrate-payouts**: Send cryptocurrency payments to customers

---

## Summary

You now have complete payment integration across all supported languages:

1. **SDK approach** (Node.js/TypeScript): Use `payram` package for type-safe integration
2. **HTTP approach** (Python/Go/PHP/Java): Direct REST API calls with proper authentication
3. **Framework integration**: Ready-to-use Express and Next.js route handlers
4. **Best practices**: Secure authentication, error handling, status polling patterns

**Next Steps:**

- Implement payment creation in your chosen language
- Store `reference_id` in your database
- Add status polling or webhook handlers
- Test with small amounts before going live
- Review `docs/payram-docs-live/api-integration/payments-api.md` for advanced options
