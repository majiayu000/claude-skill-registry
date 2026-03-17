---
name: email-gateway
description: |
  Multi-provider email sending for Cloudflare Workers and Node.js applications.

  Build transactional email systems with Resend (React Email support), SendGrid (enterprise scale),
  Mailgun (developer webhooks), or SMTP2Go (reliable relay). Includes template patterns, webhook
  verification, attachment handling, and error recovery. Use when sending emails via API, handling
  bounces/complaints, or migrating between providers.
user-invocable: true

metadata:
  keywords:
    - resend
    - sendgrid
    - mailgun
    - smtp2go
    - email api
    - transactional email
    - react email
    - email webhooks
    - bounce handling
    - email templates
    - smtp relay
license: MIT
---

# Email Gateway (Multi-Provider)

**Status**: Production Ready ✅
**Last Updated**: 2026-01-10
**Providers**: Resend, SendGrid, Mailgun, SMTP2Go

---

## Quick Start

Choose your provider based on needs:

| Provider | Best For | Key Feature | Free Tier |
|----------|----------|-------------|-----------|
| **Resend** | Modern apps, React Email | JSX templates | 100/day, 3k/month |
| **SendGrid** | Enterprise scale | Dynamic templates | 100/day forever |
| **Mailgun** | Developer webhooks | Event tracking | 100/day |
| **SMTP2Go** | Reliable relay, AU | Simple API | 1k/month trial |

### Resend (Recommended for New Projects)

```typescript
const response = await fetch('https://api.resend.com/emails', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.RESEND_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    from: 'noreply@yourdomain.com',
    to: 'user@example.com',
    subject: 'Welcome!',
    html: '<h1>Hello World</h1>',
  }),
});

const data = await response.json();
// { id: "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794" }
```

### SendGrid (Enterprise)

```typescript
const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.SENDGRID_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    personalizations: [{
      to: [{ email: 'user@example.com' }],
    }],
    from: { email: 'noreply@yourdomain.com' },
    subject: 'Welcome!',
    content: [{
      type: 'text/html',
      value: '<h1>Hello World</h1>',
    }],
  }),
});

// Returns 202 on success (no body)
```

### Mailgun

```typescript
const formData = new FormData();
formData.append('from', 'noreply@yourdomain.com');
formData.append('to', 'user@example.com');
formData.append('subject', 'Welcome!');
formData.append('html', '<h1>Hello World</h1>');

const response = await fetch(
  `https://api.mailgun.net/v3/${env.MAILGUN_DOMAIN}/messages`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${btoa(`api:${env.MAILGUN_API_KEY}`)}`,
    },
    body: formData,
  }
);

const data = await response.json();
// { id: "<20111114174239.25659.5817@samples.mailgun.org>", message: "Queued. Thank you." }
```

### SMTP2Go

```typescript
const response = await fetch('https://api.smtp2go.com/v3/email/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    api_key: env.SMTP2GO_API_KEY,
    to: ['<user@example.com>'],
    sender: 'noreply@yourdomain.com',
    subject: 'Welcome!',
    html_body: '<h1>Hello World</h1>',
  }),
});

const data = await response.json();
// { data: { succeeded: 1, failed: 0, email_id: "..." } }
```

---

## Provider Comparison

### Features

| Feature | Resend | SendGrid | Mailgun | SMTP2Go |
|---------|--------|----------|---------|---------|
| **React Email** | ✅ Native | ❌ | ❌ | ❌ |
| **Dynamic Templates** | ✅ | ✅ | ✅ | ✅ |
| **Batch Sending** | 50/request | 1000/request | 1000/request | 100/request |
| **Webhooks** | ✅ | ✅ | ✅ | ✅ |
| **SMTP** | ✅ | ✅ | ✅ | ✅ Primary |
| **IP Warmup** | Managed | Manual | Manual | Managed |
| **Dedicated IPs** | Enterprise | $90+/mo | $80+/mo | Custom |
| **Analytics** | Basic | Advanced | Advanced | Good |
| **A/B Testing** | ❌ | ✅ | ✅ | ❌ |

### Rate Limits (Free Tier)

| Provider | Daily | Monthly | Overage Cost |
|----------|-------|---------|--------------|
| **Resend** | 100 | 3,000 | $1/1k |
| **SendGrid** | 100 | Forever | $15 for 10k |
| **Mailgun** | 100 | Forever | $15 for 10k |
| **SMTP2Go** | ~33 | 1,000 trial | $10 for 10k |

### API Limits

| Provider | Requests/sec | Burst | Retry After Header |
|----------|--------------|-------|-------------------|
| **Resend** | 10 | Yes | ✅ |
| **SendGrid** | 600 | Yes | ✅ |
| **Mailgun** | Varies | Yes | ✅ |
| **SMTP2Go** | 10 | Limited | ✅ |

### Message Limits

| Provider | Max Size | Attachments | Max Recipients |
|----------|----------|-------------|----------------|
| **Resend** | 40 MB | 40 MB total | 50/request |
| **SendGrid** | 20 MB | 20 MB total | 1000/request |
| **Mailgun** | 25 MB | 25 MB total | 1000/request |
| **SMTP2Go** | 50 MB | 50 MB total | 100/request |

---

## Configuration

### Environment Variables

```bash
# Resend
RESEND_API_KEY=re_xxxxxxxxx

# SendGrid
SENDGRID_API_KEY=SG.xxxxxxxxx

# Mailgun
MAILGUN_API_KEY=xxxxxxxx-xxxxxxxx-xxxxxxxx
MAILGUN_DOMAIN=mg.yourdomain.com
MAILGUN_REGION=us  # or eu

# SMTP2Go
SMTP2GO_API_KEY=api-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Wrangler Secrets (Cloudflare Workers)

```bash
# Set secrets
echo "re_xxxxxxxxx" | npx wrangler secret put RESEND_API_KEY
echo "SG.xxxxxxxxx" | npx wrangler secret put SENDGRID_API_KEY
echo "xxxxxxxx-xxxxxxxx-xxxxxxxx" | npx wrangler secret put MAILGUN_API_KEY
echo "api-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" | npx wrangler secret put SMTP2GO_API_KEY

# Deploy to activate
npx wrangler deploy
```

### TypeScript Types

```typescript
// Resend
interface ResendEmail {
  from: string;
  to: string | string[];
  subject: string;
  html?: string;
  text?: string;
  cc?: string | string[];
  bcc?: string | string[];
  replyTo?: string | string[];
  headers?: Record<string, string>;
  attachments?: Array<{
    filename: string;
    content: string; // base64
  }>;
  tags?: Record<string, string>;
  scheduledAt?: string; // ISO 8601
}

interface ResendResponse {
  id: string;
}

// SendGrid
interface SendGridEmail {
  personalizations: Array<{
    to: Array<{ email: string; name?: string }>;
    cc?: Array<{ email: string; name?: string }>;
    bcc?: Array<{ email: string; name?: string }>;
    subject?: string;
    dynamic_template_data?: Record<string, unknown>;
  }>;
  from: { email: string; name?: string };
  subject?: string;
  content?: Array<{
    type: 'text/plain' | 'text/html';
    value: string;
  }>;
  template_id?: string;
  attachments?: Array<{
    content: string; // base64
    filename: string;
    type?: string;
    disposition?: 'inline' | 'attachment';
  }>;
}

// Mailgun
interface MailgunEmail {
  from: string;
  to: string | string[];
  subject: string;
  html?: string;
  text?: string;
  cc?: string | string[];
  bcc?: string | string[];
  'h:Reply-To'?: string;
  template?: string;
  'h:X-Mailgun-Variables'?: string; // JSON
  attachment?: File | File[];
  inline?: File | File[];
  'o:tag'?: string | string[];
  'o:tracking'?: 'yes' | 'no';
  'o:tracking-clicks'?: 'yes' | 'no' | 'htmlonly';
  'o:tracking-opens'?: 'yes' | 'no';
}

interface MailgunResponse {
  id: string;
  message: string;
}

// SMTP2Go
interface SMTP2GoEmail {
  api_key: string;
  to: string[];
  sender: string;
  subject: string;
  html_body?: string;
  text_body?: string;
  custom_headers?: Array<{
    header: string;
    value: string;
  }>;
  attachments?: Array<{
    filename: string;
    fileblob: string; // base64
    mimetype?: string;
  }>;
}

interface SMTP2GoResponse {
  data: {
    succeeded: number;
    failed: number;
    failures?: string[];
    email_id?: string;
  };
}
```

---

## Common Patterns

### 1. Transactional Emails

**Password Reset**:

```typescript
// templates/password-reset.ts
export async function sendPasswordReset(
  provider: 'resend' | 'sendgrid' | 'mailgun' | 'smtp2go',
  to: string,
  resetToken: string,
  env: Env
): Promise<{ success: boolean; id?: string; error?: string }> {
  const resetUrl = `https://yourapp.com/reset-password?token=${resetToken}`;

  const html = `
    <h1>Reset Your Password</h1>
    <p>Click the link below to reset your password:</p>
    <a href="${resetUrl}">Reset Password</a>
    <p>This link expires in 1 hour.</p>
  `;

  switch (provider) {
    case 'resend':
      return sendViaResend(to, 'Reset Your Password', html, env);
    case 'sendgrid':
      return sendViaSendGrid(to, 'Reset Your Password', html, env);
    case 'mailgun':
      return sendViaMailgun(to, 'Reset Your Password', html, env);
    case 'smtp2go':
      return sendViaSMTP2Go(to, 'Reset Your Password', html, env);
  }
}

async function sendViaResend(
  to: string,
  subject: string,
  html: string,
  env: Env
): Promise<{ success: boolean; id?: string; error?: string }> {
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'noreply@yourdomain.com',
      to,
      subject,
      html,
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    return { success: false, error };
  }

  const data = await response.json();
  return { success: true, id: data.id };
}
```

### 2. Batch Sending

**Resend (max 50 recipients)**:

```typescript
async function sendBatchResend(
  recipients: string[],
  subject: string,
  html: string,
  env: Env
): Promise<Array<{ email: string; id?: string; error?: string }>> {
  const results: Array<{ email: string; id?: string; error?: string }> = [];

  // Chunk into groups of 50
  for (let i = 0; i < recipients.length; i += 50) {
    const chunk = recipients.slice(i, i + 50);

    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'noreply@yourdomain.com',
        to: chunk,
        subject,
        html,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      chunk.forEach(email => results.push({ email, id: data.id }));
    } else {
      const error = await response.text();
      chunk.forEach(email => results.push({ email, error }));
    }
  }

  return results;
}
```

**SendGrid (max 1000 personalizations)**:

```typescript
async function sendBatchSendGrid(
  recipients: Array<{ email: string; name?: string; data?: Record<string, unknown> }>,
  templateId: string,
  env: Env
): Promise<{ success: boolean; error?: string }> {
  const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.SENDGRID_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      personalizations: recipients.map(r => ({
        to: [{ email: r.email, name: r.name }],
        dynamic_template_data: r.data || {},
      })),
      from: { email: 'noreply@yourdomain.com' },
      template_id: templateId,
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    return { success: false, error };
  }

  return { success: true };
}
```

### 3. React Email Templates (Resend Only)

**Install React Email**:

```bash
npm install react-email @react-email/components
```

**Create Template**:

```tsx
// emails/welcome.tsx
import {
  Html,
  Head,
  Body,
  Container,
  Heading,
  Text,
  Button,
} from '@react-email/components';

interface WelcomeEmailProps {
  name: string;
  confirmUrl: string;
}

export default function WelcomeEmail({ name, confirmUrl }: WelcomeEmailProps) {
  return (
    <Html>
      <Head />
      <Body style={{ fontFamily: 'Arial, sans-serif' }}>
        <Container>
          <Heading>Welcome, {name}!</Heading>
          <Text>Thanks for signing up. Please confirm your email address:</Text>
          <Button href={confirmUrl} style={{ background: '#000', color: '#fff' }}>
            Confirm Email
          </Button>
        </Container>
      </Body>
    </Html>
  );
}
```

**Send via Resend SDK (Node.js)**:

```typescript
import { Resend } from 'resend';
import WelcomeEmail from './emails/welcome';

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: 'noreply@yourdomain.com',
  to: 'user@example.com',
  subject: 'Welcome!',
  react: WelcomeEmail({ name: 'Alice', confirmUrl: 'https://...' }),
});
```

**Send via Workers (render to HTML first)**:

```typescript
import { render } from '@react-email/render';
import WelcomeEmail from './emails/welcome';

const html = render(WelcomeEmail({ name: 'Alice', confirmUrl: 'https://...' }));

await fetch('https://api.resend.com/emails', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.RESEND_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    from: 'noreply@yourdomain.com',
    to: 'user@example.com',
    subject: 'Welcome!',
    html,
  }),
});
```

### 4. Dynamic Templates

**SendGrid**:

```typescript
// 1. Create template in SendGrid dashboard with handlebars
// Subject: Welcome {{name}}!
// Body: <h1>Hi {{name}}</h1><p>Your code: {{confirmationCode}}</p>

// 2. Send with template ID
const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.SENDGRID_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    personalizations: [{
      to: [{ email: 'user@example.com' }],
      dynamic_template_data: {
        name: 'Alice',
        confirmationCode: 'ABC123',
      },
    }],
    from: { email: 'noreply@yourdomain.com' },
    template_id: 'd-xxxxxxxxxxxxxxxxxxxxxxxx',
  }),
});
```

**Mailgun**:

```typescript
// 1. Create template in Mailgun dashboard or via API
// Use {{name}} and {{confirmationCode}} variables

// 2. Send with template name
const formData = new FormData();
formData.append('from', 'noreply@yourdomain.com');
formData.append('to', 'user@example.com');
formData.append('subject', 'Welcome');
formData.append('template', 'welcome-template');
formData.append('h:X-Mailgun-Variables', JSON.stringify({
  name: 'Alice',
  confirmationCode: 'ABC123',
}));

const response = await fetch(
  `https://api.mailgun.net/v3/${env.MAILGUN_DOMAIN}/messages`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${btoa(`api:${env.MAILGUN_API_KEY}`)}`,
    },
    body: formData,
  }
);
```

### 5. Attachments

**Resend**:

```typescript
const fileBuffer = await file.arrayBuffer();
const base64Content = btoa(String.fromCharCode(...new Uint8Array(fileBuffer)));

await fetch('https://api.resend.com/emails', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.RESEND_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    from: 'noreply@yourdomain.com',
    to: 'user@example.com',
    subject: 'Your Invoice',
    html: '<p>Attached is your invoice.</p>',
    attachments: [{
      filename: 'invoice.pdf',
      content: base64Content,
    }],
  }),
});
```

**SendGrid**:

```typescript
const fileBuffer = await file.arrayBuffer();
const base64Content = btoa(String.fromCharCode(...new Uint8Array(fileBuffer)));

const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.SENDGRID_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    personalizations: [{
      to: [{ email: 'user@example.com' }],
    }],
    from: { email: 'noreply@yourdomain.com' },
    subject: 'Your Invoice',
    content: [{ type: 'text/html', value: '<p>Attached is your invoice.</p>' }],
    attachments: [{
      content: base64Content,
      filename: 'invoice.pdf',
      type: 'application/pdf',
      disposition: 'attachment',
    }],
  }),
});
```

**Mailgun** (uses FormData with File):

```typescript
const formData = new FormData();
formData.append('from', 'noreply@yourdomain.com');
formData.append('to', 'user@example.com');
formData.append('subject', 'Your Invoice');
formData.append('html', '<p>Attached is your invoice.</p>');
formData.append('attachment', file); // File object directly

const response = await fetch(
  `https://api.mailgun.net/v3/${env.MAILGUN_DOMAIN}/messages`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${btoa(`api:${env.MAILGUN_API_KEY}`)}`,
    },
    body: formData,
  }
);
```

### 6. Webhooks (Event Tracking)

**Resend Webhooks**:

Events: `email.sent`, `email.delivered`, `email.delivery_delayed`, `email.bounced`, `email.complained`, `email.opened`, `email.clicked`

```typescript
// Verify webhook signature
import { createHmac } from 'crypto';

export async function verifyResendWebhook(
  request: Request,
  secret: string
): Promise<boolean> {
  const signature = request.headers.get('svix-signature');
  const timestamp = request.headers.get('svix-timestamp');
  const body = await request.text();

  if (!signature || !timestamp) return false;

  const signedContent = `${timestamp}.${body}`;
  const expectedSignature = createHmac('sha256', secret)
    .update(signedContent)
    .digest('base64');

  return signature.includes(expectedSignature);
}

// Handle webhook
export async function handleResendWebhook(request: Request, env: Env) {
  const isValid = await verifyResendWebhook(request, env.RESEND_WEBHOOK_SECRET);
  if (!isValid) {
    return new Response('Invalid signature', { status: 401 });
  }

  const event = await request.json();

  switch (event.type) {
    case 'email.bounced':
      // Mark email as invalid
      await markEmailInvalid(event.data.email);
      break;
    case 'email.complained':
      // Unsubscribe user
      await unsubscribeUser(event.data.email);
      break;
  }

  return new Response('OK');
}
```

**SendGrid Webhooks**:

```typescript
// Verify webhook signature (requires express-style body parser)
import { EventWebhook, EventWebhookHeader } from '@sendgrid/eventwebhook';

export async function verifySendGridWebhook(
  request: Request,
  publicKey: string
): Promise<boolean> {
  const signature = request.headers.get(EventWebhookHeader.SIGNATURE());
  const timestamp = request.headers.get(EventWebhookHeader.TIMESTAMP());
  const body = await request.text();

  const eventWebhook = new EventWebhook();
  const ecPublicKey = eventWebhook.convertPublicKeyToECDSA(publicKey);

  return eventWebhook.verifySignature(
    ecPublicKey,
    body,
    signature!,
    timestamp!
  );
}

// Handle webhook
export async function handleSendGridWebhook(request: Request, env: Env) {
  const events = await request.json();

  for (const event of events) {
    switch (event.event) {
      case 'bounce':
        await markEmailInvalid(event.email);
        break;
      case 'spamreport':
        await unsubscribeUser(event.email);
        break;
    }
  }

  return new Response('OK');
}
```

**Mailgun Webhooks**:

```typescript
// Verify webhook signature
import { createHmac } from 'crypto';

export function verifyMailgunWebhook(
  timestamp: string,
  token: string,
  signature: string,
  signingKey: string
): boolean {
  const encoded = createHmac('sha256', signingKey)
    .update(`${timestamp}${token}`)
    .digest('hex');

  return encoded === signature;
}

// Handle webhook
export async function handleMailgunWebhook(request: Request, env: Env) {
  const data = await request.json();

  const isValid = verifyMailgunWebhook(
    data.signature.timestamp,
    data.signature.token,
    data.signature.signature,
    env.MAILGUN_WEBHOOK_SIGNING_KEY
  );

  if (!isValid) {
    return new Response('Invalid signature', { status: 401 });
  }

  switch (data['event-data'].event) {
    case 'failed':
      if (data['event-data'].severity === 'permanent') {
        await markEmailInvalid(data['event-data'].recipient);
      }
      break;
    case 'complained':
      await unsubscribeUser(data['event-data'].recipient);
      break;
  }

  return new Response('OK');
}
```

**SMTP2Go Webhooks**:

```typescript
// Verify webhook signature
import { createHmac } from 'crypto';

export function verifySMTP2GoWebhook(
  body: string,
  signature: string,
  secret: string
): boolean {
  const expectedSignature = createHmac('sha256', secret)
    .update(body)
    .digest('hex');

  return expectedSignature === signature;
}

// Handle webhook
export async function handleSMTP2GoWebhook(request: Request, env: Env) {
  const signature = request.headers.get('X-Smtp2go-Signature');
  const body = await request.text();

  if (!signature || !verifySMTP2GoWebhook(body, signature, env.SMTP2GO_WEBHOOK_SECRET)) {
    return new Response('Invalid signature', { status: 401 });
  }

  const event = JSON.parse(body);

  switch (event.event) {
    case 'bounce':
      await markEmailInvalid(event.email);
      break;
    case 'spam':
      await unsubscribeUser(event.email);
      break;
  }

  return new Response('OK');
}
```

---

## Error Handling

### Resend Errors

| Status | Error | Cause | Fix |
|--------|-------|-------|-----|
| 401 | Unauthorized | Invalid API key | Check RESEND_API_KEY |
| 422 | Validation error | Invalid email format | Validate emails before sending |
| 429 | Rate limit exceeded | Too many requests | Implement exponential backoff |
| 500 | Internal error | Resend service issue | Retry with backoff |

**Common validation errors**:
- `to` field required
- Invalid email format
- `from` domain not verified
- Attachment size exceeds 40 MB

**Error response format**:

```json
{
  "statusCode": 422,
  "message": "Validation error",
  "name": "validation_error"
}
```

### SendGrid Errors

| Status | Error | Cause | Fix |
|--------|-------|-------|-----|
| 400 | Bad request | Malformed JSON | Check request structure |
| 401 | Unauthorized | Invalid API key | Check SENDGRID_API_KEY |
| 413 | Payload too large | Message > 20 MB | Reduce attachment size |
| 429 | Too many requests | Rate limit | Implement backoff |

**Common errors**:
- Missing `personalizations`
- Invalid template ID
- Unverified sender address
- Attachment encoding issues

**Error response format**:

```json
{
  "errors": [
    {
      "message": "The from email does not contain a valid address.",
      "field": "from.email",
      "help": "http://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/errors.html#message.from.email"
    }
  ]
}
```

### Mailgun Errors

| Status | Error | Cause | Fix |
|--------|-------|-------|-----|
| 400 | Bad request | Invalid parameters | Check FormData fields |
| 401 | Unauthorized | Invalid API key | Check MAILGUN_API_KEY |
| 402 | Payment required | Quota exceeded | Upgrade plan |
| 404 | Not found | Invalid domain | Check MAILGUN_DOMAIN |

**Common errors**:
- Domain not verified
- Wrong region (US vs EU)
- Invalid template variables
- Recipient address syntax

**Error response format**:

```json
{
  "message": "Domain not found: invalid.domain.com"
}
```

### SMTP2Go Errors

| Status | Error | Cause | Fix |
|--------|-------|-------|-----|
| 401 | Unauthorized | Invalid API key | Check SMTP2GO_API_KEY |
| 422 | Validation error | Invalid email format | Validate recipients |
| 429 | Rate limit | Too many requests | Implement backoff |

**Common errors**:
- Sender domain not verified
- Invalid recipient format (must use angle brackets: `<email@domain.com>`)
- API key not activated

**Error response format**:

```json
{
  "data": {
    "error": "Invalid sender email address",
    "error_code": "E_ApiResponseCodes_INVALID_SENDER_ADDRESS"
  }
}
```

---

## Rate Limiting & Retry

### Exponential Backoff Pattern

```typescript
async function sendWithRetry(
  sendFn: () => Promise<Response>,
  maxRetries = 3
): Promise<Response> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await sendFn();

      if (response.ok) {
        return response;
      }

      // Check if retryable
      if (response.status === 429 || response.status >= 500) {
        const retryAfter = response.headers.get('Retry-After');
        const delay = retryAfter
          ? parseInt(retryAfter) * 1000
          : Math.pow(2, attempt) * 1000;

        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }

      // Non-retryable error
      return response;
    } catch (error) {
      lastError = error as Error;
      if (attempt < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
  }

  throw lastError || new Error('Max retries exceeded');
}

// Usage
const response = await sendWithRetry(() =>
  fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(email),
  })
);
```

### Rate Limit Tracking

```typescript
// Use KV to track rate limits per provider
interface RateLimitState {
  count: number;
  resetAt: number;
}

async function checkRateLimit(
  provider: string,
  kv: KVNamespace
): Promise<{ allowed: boolean; resetAt?: number }> {
  const key = `rate-limit:${provider}`;
  const stateJson = await kv.get(key);
  const state: RateLimitState = stateJson ? JSON.parse(stateJson) : null;

  const now = Date.now();

  if (!state || now > state.resetAt) {
    // Reset window
    const limits: Record<string, number> = {
      resend: 10,
      sendgrid: 600,
      mailgun: 100,
      smtp2go: 10,
    };

    const newState: RateLimitState = {
      count: 1,
      resetAt: now + 1000, // 1 second window
    };

    await kv.put(key, JSON.stringify(newState), { expirationTtl: 60 });
    return { allowed: true };
  }

  const limits: Record<string, number> = {
    resend: 10,
    sendgrid: 600,
    mailgun: 100,
    smtp2go: 10,
  };

  if (state.count >= limits[provider]) {
    return { allowed: false, resetAt: state.resetAt };
  }

  state.count++;
  await kv.put(key, JSON.stringify(state), { expirationTtl: 60 });
  return { allowed: true };
}
```

---

## Migration Between Providers

### Provider Abstraction

```typescript
// types.ts
export interface EmailProvider {
  send(email: EmailMessage): Promise<EmailResult>;
  sendBatch(emails: EmailMessage[]): Promise<EmailResult[]>;
}

export interface EmailMessage {
  from: string;
  to: string | string[];
  subject: string;
  html?: string;
  text?: string;
  attachments?: Attachment[];
  tags?: Record<string, string>;
}

export interface EmailResult {
  success: boolean;
  id?: string;
  error?: string;
}

export interface Attachment {
  filename: string;
  content: string; // base64
}

// providers/resend.ts
export class ResendProvider implements EmailProvider {
  constructor(private apiKey: string) {}

  async send(email: EmailMessage): Promise<EmailResult> {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: email.from,
        to: email.to,
        subject: email.subject,
        html: email.html,
        text: email.text,
        attachments: email.attachments,
        tags: email.tags,
      }),
    });

    if (!response.ok) {
      return { success: false, error: await response.text() };
    }

    const data = await response.json();
    return { success: true, id: data.id };
  }

  async sendBatch(emails: EmailMessage[]): Promise<EmailResult[]> {
    return Promise.all(emails.map(email => this.send(email)));
  }
}

// providers/sendgrid.ts
export class SendGridProvider implements EmailProvider {
  constructor(private apiKey: string) {}

  async send(email: EmailMessage): Promise<EmailResult> {
    const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        personalizations: [{
          to: Array.isArray(email.to)
            ? email.to.map(e => ({ email: e }))
            : [{ email: email.to }],
        }],
        from: { email: email.from },
        subject: email.subject,
        content: email.html
          ? [{ type: 'text/html', value: email.html }]
          : [{ type: 'text/plain', value: email.text || '' }],
        attachments: email.attachments?.map(a => ({
          content: a.content,
          filename: a.filename,
        })),
      }),
    });

    if (!response.ok) {
      return { success: false, error: await response.text() };
    }

    return { success: true };
  }

  async sendBatch(emails: EmailMessage[]): Promise<EmailResult[]> {
    // SendGrid supports batch via personalizations
    const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        personalizations: emails.map(email => ({
          to: Array.isArray(email.to)
            ? email.to.map(e => ({ email: e }))
            : [{ email: email.to }],
          subject: email.subject,
        })),
        from: { email: emails[0].from },
        content: emails[0].html
          ? [{ type: 'text/html', value: emails[0].html }]
          : [{ type: 'text/plain', value: emails[0].text || '' }],
      }),
    });

    if (!response.ok) {
      return emails.map(() => ({ success: false, error: await response.text() }));
    }

    return emails.map(() => ({ success: true }));
  }
}

// Usage
const provider = env.EMAIL_PROVIDER === 'resend'
  ? new ResendProvider(env.RESEND_API_KEY)
  : new SendGridProvider(env.SENDGRID_API_KEY);

await provider.send({
  from: 'noreply@yourdomain.com',
  to: 'user@example.com',
  subject: 'Welcome',
  html: '<h1>Hello</h1>',
});
```

---

## Testing

### Test Provider Connectivity

```typescript
export async function testEmailProvider(
  provider: 'resend' | 'sendgrid' | 'mailgun' | 'smtp2go',
  env: Env
): Promise<{ success: boolean; error?: string }> {
  const testEmail = {
    from: 'test@yourdomain.com',
    to: 'test@yourdomain.com',
    subject: 'Test Email',
    html: '<p>This is a test email.</p>',
  };

  try {
    switch (provider) {
      case 'resend': {
        const response = await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${env.RESEND_API_KEY}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(testEmail),
        });

        if (!response.ok) {
          return { success: false, error: await response.text() };
        }

        return { success: true };
      }

      case 'sendgrid': {
        const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${env.SENDGRID_API_KEY}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            personalizations: [{ to: [{ email: testEmail.to }] }],
            from: { email: testEmail.from },
            subject: testEmail.subject,
            content: [{ type: 'text/html', value: testEmail.html }],
          }),
        });

        if (!response.ok) {
          return { success: false, error: await response.text() };
        }

        return { success: true };
      }

      case 'mailgun': {
        const formData = new FormData();
        formData.append('from', testEmail.from);
        formData.append('to', testEmail.to);
        formData.append('subject', testEmail.subject);
        formData.append('html', testEmail.html);

        const response = await fetch(
          `https://api.mailgun.net/v3/${env.MAILGUN_DOMAIN}/messages`,
          {
            method: 'POST',
            headers: {
              'Authorization': `Basic ${btoa(`api:${env.MAILGUN_API_KEY}`)}`,
            },
            body: formData,
          }
        );

        if (!response.ok) {
          return { success: false, error: await response.text() };
        }

        return { success: true };
      }

      case 'smtp2go': {
        const response = await fetch('https://api.smtp2go.com/v3/email/send', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            api_key: env.SMTP2GO_API_KEY,
            to: [`<${testEmail.to}>`],
            sender: testEmail.from,
            subject: testEmail.subject,
            html_body: testEmail.html,
          }),
        });

        if (!response.ok) {
          return { success: false, error: await response.text() };
        }

        const data = await response.json();
        if (data.data.failed > 0) {
          return { success: false, error: data.data.failures?.join(', ') };
        }

        return { success: true };
      }
    }
  } catch (error) {
    return { success: false, error: (error as Error).message };
  }
}
```

---

## Quick Reference

### API Endpoints

| Provider | Endpoint |
|----------|----------|
| Resend | `https://api.resend.com/emails` |
| SendGrid | `https://api.sendgrid.com/v3/mail/send` |
| Mailgun US | `https://api.mailgun.net/v3/{domain}/messages` |
| Mailgun EU | `https://api.eu.mailgun.net/v3/{domain}/messages` |
| SMTP2Go | `https://api.smtp2go.com/v3/email/send` |

### Authentication Headers

| Provider | Header | Format |
|----------|--------|--------|
| Resend | `Authorization` | `Bearer {API_KEY}` |
| SendGrid | `Authorization` | `Bearer {API_KEY}` |
| Mailgun | `Authorization` | `Basic {base64(api:API_KEY)}` |
| SMTP2Go | Body field | `api_key: {API_KEY}` |

### Webhook Events

| Event Type | Resend | SendGrid | Mailgun | SMTP2Go |
|------------|--------|----------|---------|---------|
| Delivered | `email.delivered` | `delivered` | `delivered` | `delivered` |
| Bounced | `email.bounced` | `bounce` | `failed` | `bounce` |
| Spam | `email.complained` | `spamreport` | `complained` | `spam` |
| Opened | `email.opened` | `open` | `opened` | `open` |
| Clicked | `email.clicked` | `click` | `clicked` | `click` |

### Support Links

- **Resend**: https://resend.com/docs
- **SendGrid**: https://www.twilio.com/docs/sendgrid
- **Mailgun**: https://documentation.mailgun.com
- **SMTP2Go**: https://developers.smtp2go.com

---

**Production Notes**:
- Always verify sender domains before production
- Set up DKIM/SPF/DMARC records for deliverability
- Use dedicated IPs for high-volume sending (>100k/month)
- Implement webhook handlers for bounce/complaint management
- Monitor sender reputation via provider dashboards
- Keep unsubscribe mechanisms compliant (CAN-SPAM, GDPR)
