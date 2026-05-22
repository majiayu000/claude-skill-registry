---
name: tipalti-integration-specialist
description: "Tipalti payment integration guide for payee onboarding, payment processing, webhooks, and tax compliance. Use when implementing payment features."
---

# Tipalti Integration Specialist

Use this skill when implementing Tipalti payment integrations, including payee onboarding, payment processing, webhooks, and tax compliance for Ballee.

## Overview

**Tipalti** is a global payables automation platform. Fever already uses Tipalti heavily for payments.

### Architecture

| Role | Entity | Responsibility |
|------|--------|----------------|
| **Payer** | Fever | Owns Tipalti account, funds flow from Fever to dancers |
| **Orchestrator** | Ballee | Integrates with Fever's Tipalti via API credentials |
| **Payees** | Dancers | Onboard to Fever's Tipalti payee portal via Ballee UI |

**Money Flow**: `Fever → Tipalti → Dancers` (Ballee never touches funds)

### Tipalti Products Used

| Product | Purpose | Use Case in Ballee |
|---------|---------|-------------------|
| **Mass Payments** | Pay contractors/freelancers globally | Pay dancers for performances |
| **AP Automation** | Invoice processing & vendor payments | Receive payments from clients (Fever) |

**Key Principle**: Ballee stores `tipalti_payee_id` references only - NO bank account numbers, tax IDs, or sensitive PII. All payment data lives in Tipalti (Fever's account).

---

## Authentication

### API Keys

```bash
# Environment variables required
TIPALTI_API_URL=https://api.sandbox.tipalti.com  # Sandbox
TIPALTI_API_URL=https://api.tipalti.com          # Production
TIPALTI_PAYER_NAME=ballee
TIPALTI_API_KEY=your_api_key
TIPALTI_API_SECRET=your_api_secret
TIPALTI_WEBHOOK_SECRET=your_webhook_secret
```

### Request Signing

Tipalti uses HMAC-SHA256 for request authentication:

```typescript
import crypto from 'crypto';

function signRequest(
  payerName: string,
  payeeId: string,
  timestamp: number,
  secret: string
): string {
  const payload = `${payerName}${payeeId}${timestamp}`;
  return crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
}
```

### iFrame Dynamic Key

For embedded iFrame security, use `GetDynamicKey`:

```typescript
interface DynamicKeyResponse {
  key: string;    // Use to sign query string
  token: string;  // Include in iFrame URL as ?token=xxx
  expiresAt: number;
}

async function getDynamicKey(payeeId: string): Promise<DynamicKeyResponse> {
  const timestamp = Math.floor(Date.now() / 1000);
  const signature = signRequest(PAYER_NAME, payeeId, timestamp, API_SECRET);

  // Call Tipalti GetDynamicKey API
  const response = await fetch(`${API_URL}/v9/PayeeFunctions.asmx/GetDynamicKey`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      payerName: PAYER_NAME,
      idap: payeeId,
      timestamp,
      key: signature
    })
  });

  return response.json();
}
```

---

## Payee Onboarding

### Methods

| Method | Best For | Implementation |
|--------|----------|----------------|
| **iFrame** | User self-service | Embed Tipalti's hosted UI |
| **API** | Backend automation | `UpdateOrCreatePayeeInfo` SOAP call |
| **CSV Upload** | Bulk migration | Tipalti admin portal |

### iFrame Integration (Recommended for Dancers)

```typescript
// packages/features/tipalti/src/components/tipalti-iframe.tsx
'use client';

interface TipaltiIframeProps {
  payeeId: string;
  onComplete: () => void;
  height?: number;
}

export function TipaltiIframe({ payeeId, onComplete, height = 600 }: TipaltiIframeProps) {
  const [iframeUrl, setIframeUrl] = useState<string | null>(null);

  useEffect(() => {
    const loadIframe = async () => {
      const { token } = await getDynamicKeyAction(payeeId);
      const url = new URL(process.env.NEXT_PUBLIC_TIPALTI_IFRAME_URL!);
      url.searchParams.set('idap', payeeId);
      url.searchParams.set('payer', process.env.NEXT_PUBLIC_TIPALTI_PAYER_NAME!);
      url.searchParams.set('token', token);
      setIframeUrl(url.toString());
    };
    loadIframe();
  }, [payeeId]);

  // Listen for postMessage from Tipalti
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.origin !== process.env.NEXT_PUBLIC_TIPALTI_IFRAME_ORIGIN) return;

      if (event.data.type === 'TIPALTI_ONBOARDING_COMPLETE') {
        onComplete();
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [onComplete]);

  if (!iframeUrl) return <Spinner />;

  return (
    <iframe
      src={iframeUrl}
      width="100%"
      height={height}
      frameBorder="0"
      allow="encrypted-media"
      sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
    />
  );
}
```

### API Payee Creation

```typescript
interface CreatePayeeInput {
  email: string;
  firstName: string;
  lastName: string;
  country: string;
  externalId: string;  // Your user ID
}

async function createPayee(input: CreatePayeeInput): Promise<string> {
  const timestamp = Math.floor(Date.now() / 1000);
  const idap = `dancer_${input.externalId}`;  // Generate Tipalti payee ID

  const response = await tipaltiSoapClient.call('UpdateOrCreatePayeeInfo', {
    payerName: PAYER_NAME,
    idap,
    timestamp,
    key: signRequest(PAYER_NAME, idap, timestamp, API_SECRET),
    skipNulls: 1,
    item: {
      Email: input.email,
      FirstName: input.firstName,
      LastName: input.lastName,
      Country: input.country,
      ExternalId: input.externalId,
      PayeeEntityType: 'Individual'
    }
  });

  return idap;
}
```

### Payee Status Checks

Before processing payments, verify payee is "Payable":

```typescript
type PayeeStatus =
  | 'Active'           // Can receive payments
  | 'Pending'          // Onboarding incomplete
  | 'RequiresReview'   // Manual review needed
  | 'Blocked'          // Cannot receive payments
  | 'Inactive';

async function getPayeeStatus(payeeId: string): Promise<{
  status: PayeeStatus;
  paymentMethodStatus: string;
  taxFormStatus: string;
}> {
  const response = await tipaltiClient.call('GetExtendedPayeeDetails', {
    payerName: PAYER_NAME,
    idap: payeeId,
    timestamp: Math.floor(Date.now() / 1000),
    key: signRequest(...)
  });

  return {
    status: response.PayeeStatus,
    paymentMethodStatus: response.PaymentMethodStatus,
    taxFormStatus: response.TaxFormStatus
  };
}
```

---

## Payment Processing

### Submit Payment

```typescript
interface PaymentInput {
  payeeId: string;
  amount: number;
  currency: string;
  invoiceRefNumber: string;
  description: string;
}

async function submitPayment(input: PaymentInput): Promise<string> {
  // First verify payee is payable
  const status = await getPayeeStatus(input.payeeId);
  if (status.status !== 'Active') {
    throw new Error(`Payee not payable: ${status.status}`);
  }

  const response = await tipaltiClient.call('ProcessPayments', {
    payerName: PAYER_NAME,
    timestamp: Math.floor(Date.now() / 1000),
    key: signRequest(...),
    payments: [{
      Idap: input.payeeId,
      Amount: input.amount,
      Currency: input.currency,
      RefCode: input.invoiceRefNumber,
      Description: input.description
    }]
  });

  return response.PaymentId;
}
```

### Payment Statuses

| Status | Description | Action |
|--------|-------------|--------|
| `Submitted` | Payment sent to Tipalti | Wait for processing |
| `Processing` | Being processed | Monitor via webhook |
| `Completed` | Successfully paid | Update invoice as paid |
| `Failed` | Payment failed | Check error, retry or notify |
| `Cancelled` | Cancelled before processing | Mark as cancelled |

---

## Webhooks (IPN - Instant Payment Notifications)

### Supported Events

| Event Type | Trigger | Use Case |
|------------|---------|----------|
| `payee.onboarding.completed` | Payee finishes iFrame setup | Mark dancer as payment-ready |
| `payee.payment_method.updated` | Bank details changed | Audit log |
| `payment.status.changed` | Payment status update | Sync invoice status |
| `payment.completed` | Payment successful | Mark invoice as paid |
| `payment.failed` | Payment failed | Alert admin, retry |
| `tax_form.submitted` | W9/W8-BEN submitted | Update tax status |
| `tax_form.approved` | Tax form validated | Clear for payments |

### Webhook Handler

```typescript
// apps/web/app/api/webhooks/tipalti/route.ts
import { NextResponse } from 'next/server';
import crypto from 'crypto';

export async function POST(request: Request) {
  const signature = request.headers.get('X-Tipalti-Signature');
  const body = await request.text();

  // Verify signature
  const expectedSignature = crypto
    .createHmac('sha256', process.env.TIPALTI_WEBHOOK_SECRET!)
    .update(body)
    .digest('hex');

  if (!crypto.timingSafeEqual(
    Buffer.from(signature || ''),
    Buffer.from(expectedSignature)
  )) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  const payload = JSON.parse(body);

  // Store event for audit
  await supabase.from('tipalti_webhook_events').insert({
    event_type: payload.eventType,
    payload
  });

  // Process event
  switch (payload.eventType) {
    case 'payment.completed':
      await handlePaymentCompleted(payload);
      break;
    case 'payment.failed':
      await handlePaymentFailed(payload);
      break;
    case 'payee.onboarding.completed':
      await handleOnboardingComplete(payload);
      break;
  }

  return NextResponse.json({ received: true });
}

async function handlePaymentCompleted(payload: any) {
  // Update payment request
  await supabase
    .from('tipalti_payment_requests')
    .update({
      status: 'paid',
      paid_at: new Date().toISOString(),
      tipalti_metadata: payload
    })
    .eq('tipalti_payment_id', payload.paymentId);

  // Update invoice
  const { data: paymentRequest } = await supabase
    .from('tipalti_payment_requests')
    .select('invoice_id')
    .eq('tipalti_payment_id', payload.paymentId)
    .single();

  if (paymentRequest) {
    await supabase
      .from('invoices')
      .update({
        payment_status: 'paid',
        paid_at: new Date().toISOString()
      })
      .eq('id', paymentRequest.invoice_id);
  }
}
```

---

## Self-Billing Invoices

Tipalti can auto-generate invoices for payees (dancers), reducing admin work:

```typescript
interface SelfBillingInvoice {
  payeeId: string;
  invoiceNumber: string;
  invoiceDate: string;
  dueDate: string;
  amount: number;
  currency: string;
  lineItems: Array<{
    description: string;
    quantity: number;
    unitPrice: number;
  }>;
}

async function createSelfBillingInvoice(invoice: SelfBillingInvoice): Promise<string> {
  const response = await tipaltiClient.call('CreateOrUpdateInvoices', {
    payerName: PAYER_NAME,
    timestamp: Math.floor(Date.now() / 1000),
    key: signRequest(...),
    invoices: [{
      Idap: invoice.payeeId,
      InvoiceRefCode: invoice.invoiceNumber,
      InvoiceDate: invoice.invoiceDate,
      InvoiceDueDate: invoice.dueDate,
      TotalAmount: invoice.amount,
      Currency: invoice.currency,
      LineItems: invoice.lineItems.map(li => ({
        Description: li.description,
        Quantity: li.quantity,
        UnitPrice: li.unitPrice
      }))
    }]
  });

  return response.InvoiceId;
}
```

---

## Tax Compliance

### Supported Tax Forms

| Form | For | Countries |
|------|-----|-----------|
| **W-9** | US persons | USA |
| **W-8BEN** | Non-US individuals | International |
| **W-8BEN-E** | Non-US entities | International |

### Tax Form Flow

1. Payee completes onboarding in iFrame
2. Tipalti prompts for appropriate tax form based on country
3. Payee fills tax form digitally
4. Tipalti validates (IRS TIN matching for W-9)
5. Webhook notifies: `tax_form.submitted` → `tax_form.approved`
6. Payee cleared for payments

### 1099 Reporting (US)

Tipalti handles year-end 1099 generation for US payees:
- Automatic threshold tracking ($600 minimum)
- Electronic filing with IRS
- Payee copies generated automatically

---

## Multi-Currency Support

Tipalti handles currency conversion automatically:

```typescript
// Pay a French dancer in EUR
await submitPayment({
  payeeId: 'dancer_123',
  amount: 500,
  currency: 'EUR',  // Dancer receives EUR
  invoiceRefNumber: 'INV-2024-001',
  description: 'Performance fee - Swan Lake Dec 15'
});
```

**Supported currencies**: USD, EUR, GBP, CAD, AUD, CHF, and 100+ more

**Exchange rate locking**: Rates locked at time of payment submission

---

## Ballee Database Schema

### tipalti_payees

```sql
CREATE TABLE tipalti_payees (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) UNIQUE,
  tipalti_payee_id TEXT NOT NULL UNIQUE,

  onboarding_status TEXT NOT NULL DEFAULT 'pending'
    CHECK (onboarding_status IN ('pending', 'started', 'completed', 'requires_review')),
  payment_method_status TEXT DEFAULT 'not_set'
    CHECK (payment_method_status IN ('not_set', 'pending', 'verified', 'rejected')),
  tax_form_status TEXT DEFAULT 'not_submitted'
    CHECK (tax_form_status IN ('not_submitted', 'submitted', 'approved', 'rejected')),

  country_code TEXT,
  currency TEXT,
  last_synced_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}'::jsonb,

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### tipalti_payment_requests

```sql
CREATE TABLE tipalti_payment_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES invoices(id),
  tipalti_payee_id TEXT NOT NULL,
  tipalti_payment_id TEXT UNIQUE,

  amount DECIMAL(10,2) NOT NULL,
  currency TEXT NOT NULL DEFAULT 'EUR',

  status TEXT NOT NULL DEFAULT 'pending_approval'
    CHECK (status IN (
      'pending_approval', 'approved', 'submitted',
      'processing', 'paid', 'failed', 'cancelled'
    )),

  submitted_at TIMESTAMPTZ,
  paid_at TIMESTAMPTZ,
  failure_reason TEXT,
  tipalti_metadata JSONB DEFAULT '{}'::jsonb,

  approved_by UUID REFERENCES auth.users(id),
  approved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `PAYEE_NOT_FOUND` | Invalid payee ID | Check tipalti_payee_id mapping |
| `PAYEE_NOT_PAYABLE` | Onboarding incomplete | Redirect to iFrame |
| `INVALID_SIGNATURE` | Auth failure | Check API keys, timestamp |
| `INSUFFICIENT_FUNDS` | Payer balance low | Add funds to Tipalti account |
| `DUPLICATE_PAYMENT` | RefCode already used | Use unique invoice numbers |
| `INVALID_CURRENCY` | Currency not supported | Check payee's supported currencies |

### Retry Strategy

```typescript
async function submitPaymentWithRetry(
  input: PaymentInput,
  maxRetries = 3
): Promise<string> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await submitPayment(input);
    } catch (error) {
      if (error.code === 'RATE_LIMITED' && attempt < maxRetries) {
        await sleep(1000 * attempt);  // Exponential backoff
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

---

## Sandbox Testing

### Test Credentials

```bash
TIPALTI_API_URL=https://api.sandbox.tipalti.com
```

### Testing Checklist

1. Create test payee via API
2. Complete onboarding in iFrame sandbox
3. Submit test payment (<$5 recommended)
4. Verify webhook receipt
5. Confirm payment status updates

### Test Payee IDs

Use prefix `test_` for sandbox payees:
- `test_dancer_001`
- `test_dancer_002`

---

## Integration Checklist

- [ ] Configure environment variables
- [ ] Set up webhook endpoint and verify signature
- [ ] Implement payee registration flow
- [ ] Embed onboarding iFrame in dancer setup
- [ ] Create payment submission flow
- [ ] Handle all webhook events
- [ ] Add error handling and retries
- [ ] Test end-to-end in sandbox
- [ ] Switch to production credentials
- [ ] Monitor webhook delivery

---

## Resources

- [Tipalti Developer Hub](https://tipalti.com/product/platform/api/)
- [SOAP API Reference](https://soap-support.tipalti.com/Content/Topics/APIs/Intro.htm)
- [Payee Onboarding Guide](https://soap-support.tipalti.com/Content/Topics/GetStarted/QuickstartGuides/PayeeOnboardingviaAPI.htm)
- [Sandbox Testing](https://soap-support.tipalti.com/Content/Topics/GetStarted/QuickstartGuides/SandboxTestingGuidelines/PayeeOnboardingSandbox.htm)
- [Tipalti Help Center](https://help.tipalti.com/)
