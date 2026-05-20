---
name: smtp2go-api
description: Send transactional emails and SMS via SMTP2GO API. Covers authentication, /email/send and /email/mime endpoints, template management, attachments (base64/URL), webhooks for delivery events, statistics, and suppressions. Use when sending emails from Cloudflare Workers, building notifications, tracking delivery status, handling bounces. Prevents auth errors, attachment encoding issues.
---

# SMTP2GO API Integration

Build email and SMS delivery with the SMTP2GO transactional API.

## Quick Start

```typescript
// Send email with SMTP2GO
const response = await fetch('https://api.smtp2go.com/v3/email/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
  },
  body: JSON.stringify({
    sender: 'noreply@yourdomain.com',
    to: ['recipient@example.com'],
    subject: 'Hello from SMTP2GO',
    html_body: '<h1>Welcome!</h1><p>Your account is ready.</p>',
    text_body: 'Welcome! Your account is ready.',
  }),
});

const result = await response.json();
// { request_id: "uuid", data: { succeeded: 1, failed: 0, email_id: "1er8bV-6Tw0Mi-7h" } }
```

## Base URLs

| Region | Base URL |
|--------|----------|
| Global | `https://api.smtp2go.com/v3` |
| US | `https://us-api.smtp2go.com/v3` |
| EU | `https://eu-api.smtp2go.com/v3` |
| AU | `https://au-api.smtp2go.com/v3` |

## Authentication

Two methods supported:

```typescript
// Method 1: Header (recommended)
headers: {
  'X-Smtp2go-Api-Key': 'your-api-key'
}

// Method 2: Request body
body: JSON.stringify({
  api_key: 'your-api-key',
  // ... other params
})
```

Get API keys from SMTP2GO dashboard: **Sending > API Keys**

## Core Endpoints

### Send Standard Email

**POST** `/email/send`

```typescript
interface EmailSendRequest {
  // Required
  sender: string;           // Verified sender email
  to: string[];             // Recipients (max 100)
  subject: string;

  // Content (at least one required)
  html_body?: string;
  text_body?: string;

  // Optional
  cc?: string[];            // CC recipients (max 100)
  bcc?: string[];           // BCC recipients (max 100)
  reply_to?: string;
  custom_headers?: Array<{ header: string; value: string }>;
  attachments?: Attachment[];
  inlines?: InlineImage[];

  // Templates
  template_id?: string;
  template_data?: Record<string, any>;

  // Subaccounts
  subaccount_id?: string;
}

interface Attachment {
  filename: string;
  mimetype: string;
  fileblob?: string;        // Base64-encoded content
  url?: string;             // OR URL to fetch from
}

interface InlineImage {
  filename: string;
  mimetype: string;
  fileblob: string;
  cid: string;              // Content-ID for HTML reference
}
```

**Response:**

```typescript
interface EmailSendResponse {
  request_id: string;
  data: {
    succeeded: number;
    failed: number;
    failures: string[];
    email_id: string;
  };
}
```

### Send MIME Email

**POST** `/email/mime`

For pre-encoded MIME messages:

```typescript
const response = await fetch('https://api.smtp2go.com/v3/email/mime', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
  },
  body: JSON.stringify({
    mime_email: mimeEncodedString,
  }),
});
```

## Attachments

### Base64 Encoding

```typescript
// Convert file to base64
const fileBuffer = await file.arrayBuffer();
const base64 = btoa(String.fromCharCode(...new Uint8Array(fileBuffer)));

const email = {
  sender: 'noreply@example.com',
  to: ['user@example.com'],
  subject: 'Document attached',
  text_body: 'Please find the document attached.',
  attachments: [{
    filename: 'report.pdf',
    fileblob: base64,
    mimetype: 'application/pdf',
  }],
};
```

### URL Reference (Cached 24h)

```typescript
const email = {
  sender: 'noreply@example.com',
  to: ['user@example.com'],
  subject: 'Image attached',
  text_body: 'Photo from our event.',
  attachments: [{
    filename: 'photo.jpg',
    url: 'https://cdn.example.com/photos/event.jpg',
    mimetype: 'image/jpeg',
  }],
};
```

### Inline Images in HTML

```typescript
const email = {
  sender: 'noreply@example.com',
  to: ['user@example.com'],
  subject: 'Newsletter',
  html_body: '<h1>Welcome</h1><img src="cid:logo123" alt="Logo">',
  inlines: [{
    filename: 'logo.png',
    fileblob: logoBase64,
    mimetype: 'image/png',
    cid: 'logo123',  // Reference in HTML as src="cid:logo123"
  }],
};
```

**Limits:** Maximum total email size: 50 MB (content + attachments + headers)

## Templates

### Create Template

**POST** `/template/add`

```typescript
const response = await fetch('https://api.smtp2go.com/v3/template/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
  },
  body: JSON.stringify({
    template_name: 'welcome-email',
    html_body: '<h1>Welcome, {{ name }}!</h1><p>Thanks for joining {{ company }}.</p>',
    text_body: 'Welcome, {{ name }}! Thanks for joining {{ company }}.',
  }),
});
```

### Send with Template

```typescript
const email = {
  sender: 'noreply@example.com',
  to: ['user@example.com'],
  subject: 'Welcome aboard!',
  template_id: 'template-uuid-here',
  template_data: {
    name: 'John',
    company: 'Acme Corp',
  },
};
```

**Template Syntax:** HandlebarsJS with `{{ variable }}` placeholders.

### Template Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/template/add` | POST | Create new template |
| `/template/edit` | POST | Update existing template |
| `/template/delete` | POST | Remove template |
| `/template/search` | POST | List/search templates |
| `/template/view` | POST | Get template details |

## Webhooks

Configure webhooks to receive real-time delivery notifications.

### Event Types

**Email Events:**

| Event | Description |
|-------|-------------|
| `processed` | Email queued for delivery |
| `delivered` | Successfully delivered |
| `open` | Recipient opened email |
| `click` | Link clicked |
| `bounce` | Delivery failed |
| `spam` | Marked as spam |
| `unsubscribe` | User unsubscribed |
| `resubscribe` | User resubscribed |
| `reject` | Blocked (suppression/sandbox) |

**SMS Events:**

| Event | Description |
|-------|-------------|
| `sending` | Processing |
| `submitted` | Sent to provider |
| `delivered` | Confirmed delivery |
| `failed` | Delivery failed |
| `rejected` | Network blocked |
| `opt-out` | Recipient opted out |

### Webhook Payload (Email)

```typescript
interface WebhookPayload {
  event: string;
  time: string;           // Event timestamp
  sendtime: string;       // Original send time
  sender: string;
  from_address: string;
  rcpt: string;           // Recipient
  recipients: string[];
  email_id: string;
  subject: string;
  bounce?: string;        // Bounce type if applicable
  client?: string;        // Email client (for opens)
  'geoip-country'?: string;
}
```

### Webhook Configuration

**POST** `/webhook/add`

```typescript
await fetch('https://api.smtp2go.com/v3/webhook/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
  },
  body: JSON.stringify({
    url: 'https://api.yourdomain.com/webhooks/smtp2go',
    events: ['delivered', 'bounce', 'spam', 'unsubscribe'],
  }),
});
```

### Webhook Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook/view` | POST | List webhooks |
| `/webhook/add` | POST | Create webhook |
| `/webhook/edit` | POST | Update webhook |
| `/webhook/remove` | POST | Delete webhook |

**Retry Policy:** Up to 35 retries over 48 hours. Timeout: 10 seconds.

## Statistics

### Email Summary

**POST** `/stats/email_summary`

Combined report of bounces, cycles, spam, and unsubscribes.

```typescript
const response = await fetch('https://api.smtp2go.com/v3/stats/email_summary', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
  },
  body: JSON.stringify({}),
});
```

### Statistics Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/stats/email_summary` | POST | Combined statistics |
| `/stats/email_bounces` | POST | Bounce summary (30 days) |
| `/stats/email_cycle` | POST | Email cycle data |
| `/stats/email_history` | POST | Historical data |
| `/stats/email_spam` | POST | Spam reports |
| `/stats/email_unsubs` | POST | Unsubscribe data |

## Activity Search

**POST** `/activity/search` (Rate limited: 60/min)

Search for email events:

```typescript
const response = await fetch('https://api.smtp2go.com/v3/activity/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
  },
  body: JSON.stringify({
    // Filter parameters
  }),
});
```

**Note:** Returns max 1,000 items. For real-time data, use webhooks instead.

## Suppressions

Manage email addresses that should not receive emails.

### Add Suppression

**POST** `/suppression/add`

```typescript
await fetch('https://api.smtp2go.com/v3/suppression/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
  },
  body: JSON.stringify({
    email: 'blocked@example.com',
  }),
});
```

### Suppression Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/suppression/add` | POST | Add to suppression list |
| `/suppression/view` | POST | View suppressions |
| `/suppression/remove` | POST | Remove from list |

## SMS

**POST** `/sms/send`

```typescript
const response = await fetch('https://api.smtp2go.com/v3/sms/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
  },
  body: JSON.stringify({
    to: ['+61400000000'],  // Max 100 numbers
    message: 'Your verification code is 123456',
  }),
});
```

### SMS Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sms/send` | POST | Send SMS |
| `/sms/received` | POST | View received SMS |
| `/sms/sent` | POST | View sent SMS |
| `/sms/summary` | POST | SMS statistics |

## Response Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Success |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Invalid/missing API key |
| 402 | Request Failed | Valid params, request failed |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limited |
| 5xx | Server Error | SMTP2GO server issue |

### Error Response Format

```typescript
interface ErrorResponse {
  request_id: string;
  data: {
    error: string;
    error_code: string;
    field_validation_errors?: Record<string, string>;
  };
}
```

Common error codes:
- `E_ApiResponseCodes.ENDPOINT_PERMISSION_DENIED` - API key lacks permission
- `E_ApiResponseCodes.NON_VALIDATING_IN_PAYLOAD` - Invalid JSON/email format
- `E_ApiResponseCodes.API_EXCEPTION` - General API error

## Rate Limiting

- **Activity Search:** 60 requests/minute
- **Email Search (deprecated):** 20 requests/minute
- **Other endpoints:** Configurable per API key

**Handling 429:**

```typescript
async function sendWithRetry(payload: any, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch('https://api.smtp2go.com/v3/email/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
      },
      body: JSON.stringify(payload),
    });

    if (response.status === 429) {
      await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
      continue;
    }

    return response.json();
  }
  throw new Error('Rate limit exceeded after retries');
}
```

## Cloudflare Workers Integration

```typescript
// wrangler.jsonc
{
  "name": "email-service",
  "vars": {
    "SMTP2GO_REGION": "api"  // or "us-api", "eu-api", "au-api"
  }
}

// .dev.vars
SMTP2GO_API_KEY=api-XXXXXXXXXXXX
```

```typescript
// src/index.ts
export default {
  async fetch(request: Request, env: Env) {
    const baseUrl = `https://${env.SMTP2GO_REGION}.smtp2go.com/v3`;

    // Send transactional email
    const response = await fetch(`${baseUrl}/email/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
      },
      body: JSON.stringify({
        sender: 'noreply@yourdomain.com',
        to: ['user@example.com'],
        subject: 'Order Confirmation',
        template_id: 'order-confirmation-template',
        template_data: {
          order_id: '12345',
          total: '$99.00',
        },
      }),
    });

    const result = await response.json();
    return Response.json(result);
  },
} satisfies ExportedHandler<Env>;

interface Env {
  SMTP2GO_API_KEY: string;
  SMTP2GO_REGION: string;
}
```

## Sender Verification

Before sending, verify your sender identity:

1. **Sender Domain (Recommended):** Add and verify domain in SMTP2GO dashboard for SPF/DKIM alignment
2. **Single Sender Email:** Verify individual email address

Unverified senders are rejected with 400 error.

## Common Patterns

### Contact Form Handler

```typescript
export async function handleContactForm(formData: FormData, env: Env) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;
  const message = formData.get('message') as string;

  const response = await fetch('https://api.smtp2go.com/v3/email/send', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Smtp2go-Api-Key': env.SMTP2GO_API_KEY,
    },
    body: JSON.stringify({
      sender: 'website@yourdomain.com',
      to: ['support@yourdomain.com'],
      reply_to: email,
      subject: `Contact form: ${name}`,
      text_body: `From: ${name} <${email}>\n\n${message}`,
      html_body: `
        <p><strong>From:</strong> ${name} &lt;${email}&gt;</p>
        <hr>
        <p>${message.replace(/\n/g, '<br>')}</p>
      `,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to send email');
  }

  return response.json();
}
```

### Webhook Handler

```typescript
export async function handleWebhook(request: Request) {
  const payload = await request.json();

  switch (payload.event) {
    case 'bounce':
      // Handle bounce - update user record, retry logic
      console.log(`Bounce: ${payload.rcpt} - ${payload.bounce}`);
      break;

    case 'unsubscribe':
      // Update preferences
      console.log(`Unsubscribe: ${payload.rcpt}`);
      break;

    case 'spam':
      // Add to suppression, alert team
      console.log(`Spam report: ${payload.rcpt}`);
      break;
  }

  return new Response('OK', { status: 200 });
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Missing/invalid API key | Check API key in header or body |
| 400 sender not verified | Unverified sender domain | Verify domain in SMTP2GO dashboard |
| 429 Too Many Requests | Rate limit exceeded | Implement exponential backoff |
| Attachment too large | Over 50MB total | Compress or use URL references |
| Template variables not replaced | Wrong syntax | Use `{{ variable }}` Handlebars syntax |
| Webhook not receiving events | Timeout/errors | Check endpoint returns 200 within 10s |

## References

- [SMTP2GO API Documentation](https://developers.smtp2go.com/)
- [API Reference](https://developers.smtp2go.com/reference/)
- [Getting Started Guide](https://developers.smtp2go.com/docs/getting-started)
- [Webhook Documentation](https://developers.smtp2go.com/docs/webhooks-overview)
- [Template Guide](https://developers.smtp2go.com/docs/getting-started-with-templates)

---

**Last Updated:** 2026-02-06
**API Version:** v3.0.3
