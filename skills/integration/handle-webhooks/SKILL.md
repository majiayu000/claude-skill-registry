---
name: handle-webhooks
description: Complete guide to implementing Payram webhook handlers across all supported frameworks for real-time payment status updates
---

# Handle Payram Webhooks

## Overview

This skill provides comprehensive instructions for implementing Payram webhook handlers in your application. Webhooks enable real-time notifications when payment status changes, eliminating the need for polling. You'll learn how to create secure webhook endpoints, validate incoming requests, route events to appropriate handlers, and test your implementation across all supported frameworks.

## When to Use This Skill

Use this skill when you need to:

- Receive real-time payment status notifications
- Eliminate polling for payment updates
- Implement event-driven payment processing
- Handle payment lifecycle events (filled, cancelled, etc.)
- Build production-ready webhook endpoints with proper security
- Test webhook integration locally before deploying

## Prerequisites

Before starting, ensure you have:

- Completed the `setup-payram` skill (environment configured)
- Created payment functionality (`integrate-payments` skill)
- Configured `PAYRAM_WEBHOOK_SECRET` in your `.env` file
- Exposed a publicly accessible HTTPS endpoint (for production)
- Reviewed `docs/payram-webhook.yaml` for webhook payload schema

---

## Instructions

### Part 1: Understanding Webhook Flow

#### 1.1 Webhook Delivery

When a payment status changes, Payram sends an HTTP POST request:

```
POST https://your-domain.com/api/payram/webhook
Content-Type: application/json
API-Key: your-webhook-secret

{
  "reference_id": "ref_abc123",
  "invoice_id": "inv_xyz456",
  "customer_id": "cust_123",
  "customer_email": "customer@example.com",
  "status": "FILLED",
  "amount": 49.99,
  "filled_amount_in_usd": 49.99,
  "currency": "USD"
}
```

**Action:** Configure your webhook URL in Payram dashboard and store the shared secret in `PAYRAM_WEBHOOK_SECRET`.

#### 1.2 Payment Status Events

Webhooks notify you of these payment states:

- **OPEN** - Payment created, awaiting customer action
- **FILLED** - Payment completed successfully (exact amount paid)
- **PARTIALLY_FILLED** - Partial payment received (less than requested)
- **OVER_FILLED** - Overpayment received (more than requested)
- **CANCELLED** - Payment cancelled by customer or merchant
- **UNDEFINED** - Unknown status (future compatibility)

**Action:** Implement handlers for each status based on your business logic.

#### 1.3 Security Verification

All webhook requests include an `API-Key` header:

```
API-Key: your-webhook-secret-from-payram-dashboard
```

**Critical:** Always verify this header matches your stored secret before processing events.

---

### Part 2: TypeScript Type Definitions

#### 2.1 Create Webhook Types

**File:** `src/types/payramWebhook.ts` (or `lib/payram/webhookTypes.ts` for Next.js)

```typescript
export type PayramWebhookStatus =
  | 'OPEN'
  | 'CANCELLED'
  | 'FILLED'
  | 'PARTIALLY_FILLED'
  | 'OVER_FILLED'
  | 'UNDEFINED';

export interface PayramWebhookPayload {
  reference_id: string;
  invoice_id?: string;
  customer_id?: string;
  customer_email?: string;
  status: PayramWebhookStatus;
  amount?: number;
  filled_amount_in_usd?: number;
  currency?: string; // 3-letter ISO code
  [key: string]: unknown; // Allow additional fields
}

export interface PayramWebhookAck {
  message: string;
}
```

---

### Part 3: Event Router Implementation

#### 3.1 Create Status-Based Router

**File:** `src/services/payramWebhookRouter.ts`

```typescript
import { PayramWebhookPayload } from '../types/payramWebhook';

export async function handlePayramEvent(payload: PayramWebhookPayload) {
  console.log('Received Payram webhook:', payload.reference_id, payload.status);

  switch (payload.status) {
    case 'FILLED':
      await handleFilledPayment(payload);
      break;
    case 'OPEN':
      await handleOpenPayment(payload);
      break;
    case 'PARTIALLY_FILLED':
      await handlePartialPayment(payload);
      break;
    case 'OVER_FILLED':
      await handleOverfilledPayment(payload);
      break;
    case 'CANCELLED':
      await handleCancelledPayment(payload);
      break;
    case 'UNDEFINED':
    default:
      await handleUndefinedStatus(payload);
      break;
  }
}

async function handleFilledPayment(payload: PayramWebhookPayload) {
  // TODO: Mark order as paid, deliver goods, send confirmation email
  console.log('✅ Payment FILLED:', payload.reference_id);

  // Example: Update database
  // await db.payments.update({
  //   where: { payramReferenceId: payload.reference_id },
  //   data: { status: 'completed', paidAt: new Date() }
  // });

  // Example: Fulfill order
  // await fulfillOrder(payload.customer_id, payload.reference_id);
}

async function handleOpenPayment(payload: PayramWebhookPayload) {
  // TODO: Record that payment request was acknowledged
  console.log('🔵 Payment OPEN:', payload.reference_id);

  // Example: Update database
  // await db.payments.update({
  //   where: { payramReferenceId: payload.reference_id },
  //   data: { status: 'open', openedAt: new Date() }
  // });
}

async function handlePartialPayment(payload: PayramWebhookPayload) {
  // TODO: Update outstanding balance, notify finance team
  console.log('⚠️ Payment PARTIALLY_FILLED:', payload.reference_id, payload.filled_amount_in_usd);

  // Example: Calculate remaining amount
  // const remaining = (payload.amount || 0) - (payload.filled_amount_in_usd || 0);
  // await notifyFinance(`Partial payment received. Remaining: $${remaining}`);
}

async function handleOverfilledPayment(payload: PayramWebhookPayload) {
  // TODO: Queue manual review or process refund
  console.log('💰 Payment OVER_FILLED:', payload.reference_id, payload.filled_amount_in_usd);

  // Example: Queue refund
  // const excess = (payload.filled_amount_in_usd || 0) - (payload.amount || 0);
  // await queueRefund(payload.customer_id, excess);
}

async function handleCancelledPayment(payload: PayramWebhookPayload) {
  // TODO: Release inventory, notify customer
  console.log('❌ Payment CANCELLED:', payload.reference_id);

  // Example: Update database and release inventory
  // await db.payments.update({
  //   where: { payramReferenceId: payload.reference_id },
  //   data: { status: 'cancelled', cancelledAt: new Date() }
  // });
  // await releaseInventory(payload.customer_id, payload.reference_id);
}

async function handleUndefinedStatus(payload: PayramWebhookPayload) {
  // TODO: Log for investigation
  console.warn('⚡ Payment status UNDEFINED:', payload.reference_id, payload);

  // Example: Alert monitoring system
  // await alertMonitoring('Unknown payment status received', payload);
}
```

---

### Part 4: Framework-Specific Handlers

#### 4.1 Express.js Handler

**File:** `src/routes/payramWebhook.ts`

```typescript
import express, { Request, Response } from 'express';
import { handlePayramEvent } from '../services/payramWebhookRouter';
import { PayramWebhookPayload, PayramWebhookAck } from '../types/payramWebhook';

const router = express.Router();
router.use(express.json());

router.post('/api/payram/webhook', async (req: Request, res: Response) => {
  // 1. Verify webhook secret is configured
  const sharedSecret = process.env.PAYRAM_WEBHOOK_SECRET;
  if (!sharedSecret) {
    console.error('PAYRAM_WEBHOOK_SECRET not configured');
    return res.status(500).json({ error: 'webhook_not_configured' });
  }

  // 2. Validate API-Key header
  const incomingKey = req.get('API-Key');
  if (!incomingKey || incomingKey !== sharedSecret) {
    console.warn('Invalid webhook API-Key received');
    return res.status(401).json({ error: 'invalid-webhook-key' });
  }

  // 3. Validate payload structure
  const payload = req.body as PayramWebhookPayload;
  if (!payload?.reference_id || !payload?.status) {
    console.error('Invalid webhook payload:', payload);
    return res.status(400).json({ error: 'invalid-webhook-payload' });
  }

  // 4. Process event
  try {
    await handlePayramEvent(payload);
    const ack: PayramWebhookAck = { message: 'Webhook received successfully' };
    return res.json(ack);
  } catch (error) {
    console.error('Error handling Payram webhook', error);
    return res.status(500).json({ error: 'webhook_handler_error' });
  }
});

export default router;
```

**Integration:** Wire into Express app:

```typescript
import payramWebhookRouter from './routes/payramWebhook';
app.use(payramWebhookRouter);
```

#### 4.2 Next.js App Router Handler

**File:** `app/api/payram/webhook/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { handlePayramEvent } from '@/lib/payram/handlePayramEvent';
import { PayramWebhookPayload, PayramWebhookAck } from '@/lib/payram/webhookTypes';

export async function POST(request: NextRequest) {
  // 1. Verify webhook secret is configured
  const sharedSecret = process.env.PAYRAM_WEBHOOK_SECRET;
  if (!sharedSecret) {
    console.error('PAYRAM_WEBHOOK_SECRET not configured');
    return NextResponse.json({ error: 'webhook_not_configured' }, { status: 500 });
  }

  // 2. Validate API-Key header
  const incomingKey = request.headers.get('API-Key');
  if (!incomingKey || incomingKey !== sharedSecret) {
    console.warn('Invalid webhook API-Key received');
    return NextResponse.json({ error: 'invalid-webhook-key' }, { status: 401 });
  }

  // 3. Parse and validate payload
  let payload: PayramWebhookPayload;
  try {
    payload = (await request.json()) as PayramWebhookPayload;
  } catch (error) {
    console.error('Failed to parse webhook JSON:', error);
    return NextResponse.json({ error: 'invalid-json-payload' }, { status: 400 });
  }

  if (!payload.reference_id || !payload.status) {
    console.error('Invalid webhook payload:', payload);
    return NextResponse.json({ error: 'invalid-webhook-payload' }, { status: 400 });
  }

  // 4. Process event
  try {
    await handlePayramEvent(payload);
    const ack: PayramWebhookAck = { message: 'Webhook received successfully' };
    return NextResponse.json(ack);
  } catch (error) {
    console.error('Error handling Payram webhook', error);
    return NextResponse.json({ error: 'webhook_handler_error' }, { status: 500 });
  }
}
```

#### 4.3 FastAPI Handler

**File:** `app/webhooks/payram.py`

```python
import os
from fastapi import FastAPI, HTTPException, Request
from app.services.payram_webhook_router import handle_payram_event

app = FastAPI()

@app.post('/api/payram/webhook')
async def payram_webhook(request: Request):
    # 1. Verify webhook secret is configured
    shared_secret = os.getenv('PAYRAM_WEBHOOK_SECRET')
    if not shared_secret:
        raise HTTPException(status_code=500, detail='webhook_not_configured')

    # 2. Validate API-Key header
    incoming_key = request.headers.get('API-Key')
    if not incoming_key or incoming_key != shared_secret:
        raise HTTPException(status_code=401, detail='invalid-webhook-key')

    # 3. Parse and validate payload
    payload = await request.json()
    if 'reference_id' not in payload or 'status' not in payload:
        raise HTTPException(status_code=400, detail='invalid-webhook-payload')

    # 4. Process event
    await handle_payram_event(payload)
    return {'message': 'Webhook received successfully'}
```

**Event Router:** `app/services/payram_webhook_router.py`

```python
async def handle_payram_event(payload: dict):
    status = payload.get('status')
    reference_id = payload.get('reference_id')

    if status == 'FILLED':
        await handle_filled_payment(payload)
    elif status == 'OPEN':
        await handle_open_payment(payload)
    elif status == 'PARTIALLY_FILLED':
        await handle_partial_payment(payload)
    elif status == 'OVER_FILLED':
        await handle_overfilled_payment(payload)
    elif status == 'CANCELLED':
        await handle_cancelled_payment(payload)
    else:
        await handle_undefined_status(payload)

async def handle_filled_payment(payload: dict):
    print(f"✅ Payment FILLED: {payload['reference_id']}")
    # TODO: Mark order as paid, fulfill order

async def handle_open_payment(payload: dict):
    print(f"🔵 Payment OPEN: {payload['reference_id']}")
    # TODO: Record payment acknowledgement

async def handle_partial_payment(payload: dict):
    print(f"⚠️ Payment PARTIALLY_FILLED: {payload['reference_id']}")
    # TODO: Update outstanding balance

async def handle_overfilled_payment(payload: dict):
    print(f"💰 Payment OVER_FILLED: {payload['reference_id']}")
    # TODO: Queue refund

async def handle_cancelled_payment(payload: dict):
    print(f"❌ Payment CANCELLED: {payload['reference_id']}")
    # TODO: Release inventory

async def handle_undefined_status(payload: dict):
    print(f"⚡ Unknown status: {payload.get('status')}")
    # TODO: Log for investigation
```

#### 4.4 Gin (Go) Handler

**File:** `internal/webhooks/payram.go`

```go
package webhooks

import (
    "net/http"
    "os"
    "github.com/gin-gonic/gin"
)

type PayramWebhookPayload struct {
    ReferenceID       string   `json:"reference_id" binding:"required"`
    InvoiceID         *string  `json:"invoice_id"`
    CustomerID        *string  `json:"customer_id"`
    CustomerEmail     *string  `json:"customer_email"`
    Status            string   `json:"status" binding:"required"`
    Amount            *float64 `json:"amount"`
    FilledAmountInUSD *float64 `json:"filled_amount_in_usd"`
    Currency          *string  `json:"currency"`
}

func RegisterPayramRoutes(router *gin.Engine) {
    router.POST("/api/payram/webhook", handlePayramWebhook)
}

func handlePayramWebhook(c *gin.Context) {
    // 1. Verify webhook secret is configured
    sharedSecret := os.Getenv("PAYRAM_WEBHOOK_SECRET")
    if sharedSecret == "" {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "webhook_not_configured"})
        return
    }

    // 2. Validate API-Key header
    if c.GetHeader("API-Key") != sharedSecret {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid-webhook-key"})
        return
    }

    // 3. Parse and validate payload
    var payload PayramWebhookPayload
    if err := c.ShouldBindJSON(&payload); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid-json-payload"})
        return
    }

    // 4. Process event
    if err := handlePayramEvent(payload); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "webhook_handler_error"})
        return
    }

    c.JSON(http.StatusOK, gin.H{"message": "Webhook received successfully"})
}

func handlePayramEvent(payload PayramWebhookPayload) error {
    switch payload.Status {
    case "FILLED":
        return handleFilledPayment(payload)
    case "OPEN":
        return handleOpenPayment(payload)
    case "PARTIALLY_FILLED":
        return handlePartialPayment(payload)
    case "OVER_FILLED":
        return handleOverfilledPayment(payload)
    case "CANCELLED":
        return handleCancelledPayment(payload)
    default:
        return handleUndefinedStatus(payload)
    }
}

func handleFilledPayment(payload PayramWebhookPayload) error {
    // TODO: Mark order as paid
    return nil
}

// Implement other handlers...
```

#### 4.5 Laravel Handler

**File:** `routes/api.php`

```php
use App\Http\Controllers\PayramWebhookController;

Route::post('/api/payram/webhook', [PayramWebhookController::class, 'handle']);
```

**File:** `app/Http/Controllers/PayramWebhookController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Services\PayramWebhookRouter;
use Illuminate\Http\Request;

class PayramWebhookController extends Controller
{
    public function __construct(private PayramWebhookRouter $router)
    {
    }

    public function handle(Request $request)
    {
        // 1. Verify webhook secret is configured
        $sharedSecret = env('PAYRAM_WEBHOOK_SECRET');
        if (!$sharedSecret) {
            return response()->json(['error' => 'webhook_not_configured'], 500);
        }

        // 2. Validate API-Key header
        if ($request->header('API-Key') !== $sharedSecret) {
            return response()->json(['error' => 'invalid-webhook-key'], 401);
        }

        // 3. Validate payload structure
        $payload = $request->json()->all();
        if (empty($payload['reference_id']) || empty($payload['status'])) {
            return response()->json(['error' => 'invalid-webhook-payload'], 400);
        }

        // 4. Process event
        $this->router->handle($payload);

        return response()->json(['message' => 'Webhook received successfully']);
    }
}
```

**File:** `app/Services/PayramWebhookRouter.php`

```php
<?php

namespace App\Services;

class PayramWebhookRouter
{
    public function handle(array $payload): void
    {
        $status = $payload['status'] ?? null;

        match ($status) {
            'FILLED' => $this->handleFilledPayment($payload),
            'OPEN' => $this->handleOpenPayment($payload),
            'PARTIALLY_FILLED' => $this->handlePartialPayment($payload),
            'OVER_FILLED' => $this->handleOverfilledPayment($payload),
            'CANCELLED' => $this->handleCancelledPayment($payload),
            default => $this->handleUndefinedStatus($payload),
        };
    }

    private function handleFilledPayment(array $payload): void
    {
        // TODO: Mark order as paid
        \Log::info('Payment FILLED: ' . $payload['reference_id']);
    }

    // Implement other handlers...
}
```

#### 4.6 Spring Boot Handler

**File:** `src/main/java/com/example/webhooks/PayramWebhookController.java`

```java
package com.example.webhooks;

import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/payram")
public class PayramWebhookController {

    private final PayramWebhookRouter router;

    public PayramWebhookController(PayramWebhookRouter router) {
        this.router = router;
    }

    @PostMapping("/webhook")
    public ResponseEntity<?> handleWebhook(
            @RequestBody Map<String, Object> payload,
            @RequestHeader(value = "API-Key", required = false) String apiKey) {

        // 1. Verify webhook secret is configured
        String sharedSecret = System.getenv("PAYRAM_WEBHOOK_SECRET");
        if (sharedSecret == null || sharedSecret.isBlank()) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "webhook_not_configured"));
        }

        // 2. Validate API-Key header
        if (apiKey == null || !apiKey.equals(sharedSecret)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "invalid-webhook-key"));
        }

        // 3. Validate payload structure
        if (!payload.containsKey("reference_id") || !payload.containsKey("status")) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(Map.of("error", "invalid-webhook-payload"));
        }

        // 4. Process event
        router.handle(payload);

        return ResponseEntity.ok(Map.of("message", "Webhook received successfully"));
    }
}
```

**File:** `src/main/java/com/example/webhooks/PayramWebhookRouter.java`

```java
package com.example.webhooks;

import java.util.Map;
import org.springframework.stereotype.Service;

@Service
public class PayramWebhookRouter {

    public void handle(Map<String, Object> payload) {
        String status = (String) payload.get("status");

        switch (status) {
            case "FILLED" -> handleFilledPayment(payload);
            case "OPEN" -> handleOpenPayment(payload);
            case "PARTIALLY_FILLED" -> handlePartialPayment(payload);
            case "OVER_FILLED" -> handleOverfilledPayment(payload);
            case "CANCELLED" -> handleCancelledPayment(payload);
            default -> handleUndefinedStatus(payload);
        }
    }

    private void handleFilledPayment(Map<String, Object> payload) {
        // TODO: Mark order as paid
        System.out.println("Payment FILLED: " + payload.get("reference_id"));
    }

    // Implement other handlers...
}
```

---

### Part 5: Local Testing

#### 5.1 Using curl

**File:** `scripts/test-webhook.sh`

```bash
#!/bin/bash

# Set your local webhook URL and secret
WEBHOOK_URL="${MOCK_WEBHOOK_URL:-http://localhost:3000/api/payram/webhook}"
WEBHOOK_SECRET="${PAYRAM_WEBHOOK_SECRET:-your-webhook-secret}"

# Send mock FILLED event
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "API-Key: $WEBHOOK_SECRET" \
  -d '{
    "reference_id": "ref_test_001",
    "invoice_id": "inv_test_001",
    "customer_id": "cust_123",
    "customer_email": "test@example.com",
    "status": "FILLED",
    "amount": 49.99,
    "filled_amount_in_usd": 49.99,
    "currency": "USD"
  }'
```

**Usage:**

```bash
chmod +x scripts/test-webhook.sh
./scripts/test-webhook.sh
```

#### 5.2 Using Python

**File:** `scripts/test_webhook.py`

```python
import os
import requests

WEBHOOK_URL = os.getenv('MOCK_WEBHOOK_URL', 'http://localhost:3000/api/payram/webhook')
WEBHOOK_SECRET = os.getenv('PAYRAM_WEBHOOK_SECRET', 'your-webhook-secret')

def test_filled_event():
    payload = {
        'reference_id': 'ref_test_001',
        'invoice_id': 'inv_test_001',
        'customer_id': 'cust_123',
        'customer_email': 'test@example.com',
        'status': 'FILLED',
        'amount': 49.99,
        'filled_amount_in_usd': 49.99,
        'currency': 'USD',
    }

    response = requests.post(
        WEBHOOK_URL,
        headers={
            'Content-Type': 'application/json',
            'API-Key': WEBHOOK_SECRET
        },
        json=payload,
    )

    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')

if __name__ == '__main__':
    test_filled_event()
```

**Usage:**

```bash
python scripts/test_webhook.py
```

#### 5.3 Test All Status Events

Create a test suite that sends all possible status events:

```typescript
// scripts/test-all-webhooks.ts
const statuses = ['OPEN', 'FILLED', 'PARTIALLY_FILLED', 'OVER_FILLED', 'CANCELLED'];

async function testAllWebhooks() {
  for (const status of statuses) {
    const payload = {
      reference_id: `ref_test_${status.toLowerCase()}`,
      status,
      customer_id: 'cust_test',
      amount: 100,
      filled_amount_in_usd: status === 'PARTIALLY_FILLED' ? 50 : 100,
    };

    const response = await fetch('http://localhost:3000/api/payram/webhook', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'API-Key': process.env.PAYRAM_WEBHOOK_SECRET!,
      },
      body: JSON.stringify(payload),
    });

    console.log(`${status}: ${response.status} - ${await response.text()}`);
  }
}

testAllWebhooks();
```

---

## Best Practices

### 1. Security

**Always validate the API-Key header:**

```typescript
// ❌ INSECURE - Never skip validation
router.post('/webhook', async (req, res) => {
  await handleEvent(req.body);
  res.json({ message: 'ok' });
});

// ✅ SECURE - Always verify secret
router.post('/webhook', async (req, res) => {
  if (req.get('API-Key') !== process.env.PAYRAM_WEBHOOK_SECRET) {
    return res.status(401).json({ error: 'unauthorized' });
  }
  await handleEvent(req.body);
  res.json({ message: 'ok' });
});
```

**Additional security measures:**

- Use HTTPS in production (Payram won't send webhooks to HTTP)
- Store webhook secret in environment variables
- Rotate secrets periodically
- Log failed authentication attempts
- Consider IP whitelisting if Payram provides static IPs

### 2. Idempotency

Handle duplicate webhook deliveries gracefully:

```typescript
async function handleFilledPayment(payload: PayramWebhookPayload) {
  // Check if already processed
  const existing = await db.payments.findUnique({
    where: { payramReferenceId: payload.reference_id },
  });

  if (existing && existing.status === 'completed') {
    console.log('Payment already processed, skipping:', payload.reference_id);
    return; // Idempotent - safe to receive multiple times
  }

  // Process payment
  await db.payments.update({
    where: { payramReferenceId: payload.reference_id },
    data: { status: 'completed', paidAt: new Date() },
  });

  await fulfillOrder(payload.customer_id, payload.reference_id);
}
```

### 3. Error Handling

Return appropriate HTTP status codes:

- **200**: Webhook processed successfully
- **400**: Invalid payload structure
- **401**: Invalid API-Key
- **500**: Internal processing error (Payram will retry)

**Retry behavior:** If you return 5xx, Payram will retry with exponential backoff.

```typescript
try {
  await handlePayramEvent(payload);
  return res.status(200).json({ message: 'success' });
} catch (error) {
  console.error('Webhook processing failed:', error);

  // Determine if retryable
  if (error instanceof DatabaseConnectionError) {
    // Temporary issue - return 500 to trigger retry
    return res.status(500).json({ error: 'temporary_failure' });
  } else {
    // Permanent issue - return 200 to prevent retries
    console.error('Permanent failure, not retrying:', error);
    return res.status(200).json({ message: 'acknowledged' });
  }
}
```

### 4. Logging

Log all webhook events for debugging:

```typescript
async function handlePayramEvent(payload: PayramWebhookPayload) {
  // Log incoming event
  console.log('Webhook received:', {
    reference_id: payload.reference_id,
    status: payload.status,
    timestamp: new Date().toISOString(),
  });

  try {
    await routeEventByStatus(payload);

    // Log success
    console.log('Webhook processed successfully:', payload.reference_id);
  } catch (error) {
    // Log error with context
    console.error('Webhook processing failed:', {
      reference_id: payload.reference_id,
      status: payload.status,
      error: error.message,
      stack: error.stack,
    });
    throw error;
  }
}
```

### 5. Database Transactions

Use transactions for critical operations:

```typescript
async function handleFilledPayment(payload: PayramWebhookPayload) {
  await db.$transaction(async (tx) => {
    // Update payment status
    await tx.payments.update({
      where: { payramReferenceId: payload.reference_id },
      data: { status: 'completed' },
    });

    // Fulfill order
    await tx.orders.update({
      where: { paymentReferenceId: payload.reference_id },
      data: { status: 'fulfilled', fulfilledAt: new Date() },
    });

    // Update inventory
    await tx.inventory.decrement({
      where: { orderId: order.id },
      data: { quantity: order.quantity },
    });
  });
}
```

---

## Troubleshooting

### Webhook not received

**Causes:**

- Webhook URL not configured in Payram dashboard
- Endpoint not publicly accessible
- Firewall blocking Payram's IP addresses
- HTTPS certificate issues

**Solutions:**

1. Verify webhook URL in Payram dashboard
2. Use ngrok for local testing: `ngrok http 3000`
3. Check firewall rules
4. Ensure valid SSL certificate (Let's Encrypt recommended)
5. Test endpoint with curl from external server

### Getting 401 errors in logs

**Cause:** `API-Key` header mismatch.

**Solutions:**

- Verify `PAYRAM_WEBHOOK_SECRET` in `.env` matches dashboard value
- Check for extra whitespace in environment variable
- Ensure header name is exact: `API-Key` (case-sensitive)
- Restart server after updating `.env`

### Webhooks timing out

**Cause:** Handler taking too long to respond.

**Solutions:**

- Move heavy processing to background jobs
- Return 200 immediately, process asynchronously
- Use message queue (Redis, RabbitMQ) for processing

```typescript
router.post('/webhook', async (req, res) => {
  const payload = req.body;

  // Validate quickly
  if (!validatePayload(payload)) {
    return res.status(400).json({ error: 'invalid' });
  }

  // Queue for processing
  await queue.add('process-webhook', payload);

  // Respond immediately
  return res.status(200).json({ message: 'queued' });
});
```

### Duplicate events received

**Cause:** Payram retries on 5xx or timeout.

**Solution:** Implement idempotency (see Best Practices #2).

### Missing status updates

**Causes:**

- Endpoint returned error
- Processing crashed before responding
- Webhook not configured for all events

**Solutions:**

- Check webhook logs in Payram dashboard
- Implement proper error handling
- Add comprehensive logging
- Use status polling as fallback

---

## Related Skills

- **setup-payram**: Configure environment and credentials
- **integrate-payments**: Create payments that trigger webhooks
- **integrate-payouts**: Handle payout status webhooks

---

## Summary

You now have complete webhook integration across all frameworks:

1. **Security**: API-Key header validation for all requests
2. **Event routing**: Status-based handlers for all payment states
3. **Framework handlers**: Ready-to-use implementations for Express, Next.js, FastAPI, Laravel, Gin, Spring Boot
4. **Testing**: Local testing tools for all webhook events
5. **Best practices**: Idempotency, error handling, logging, transactions

**Key Reminders:**

- Always validate `API-Key` header
- Implement idempotency for all handlers
- Return 200 for successfully processed events
- Return 5xx only for retryable errors
- Use HTTPS in production
- Test locally with mock events before deploying

**Next Steps:**

- Implement webhook handler for your framework
- Configure webhook URL in Payram dashboard
- Set `PAYRAM_WEBHOOK_SECRET` environment variable
- Test with mock events locally
- Deploy and verify production webhooks
- Monitor webhook logs for issues
