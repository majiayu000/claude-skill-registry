---
name: twilio-api
description: Use this skill when working with Twilio communication APIs for SMS/MMS messaging, voice calls, phone number management, TwiML, webhook integration, two-way SMS conversations, bulk sending, or production deployment of telephony features. Includes official Twilio patterns, production code examples from Twilio-Aldea (provider-agnostic webhooks, signature validation, TwiML responses), and comprehensive TypeScript examples.
---

# Twilio API - Comprehensive Communication Platform

## When to Use This Skill

Use this skill when working with Twilio's communication APIs for:

- **SMS/MMS Messaging** - Send and receive text messages programmatically
- **Voice Communication** - Build voice calling applications with TwiML
- **Phone Number Management** - Search, purchase, and configure phone numbers
- **Webhook Integration** - Handle real-time events and delivery notifications with TwiML responses
- **Two-Way SMS Conversations** - Build interactive SMS experiences
- **Bulk SMS Sending** - Send messages to multiple recipients with rate limiting
- **Message Scheduling** - Schedule messages for future delivery
- **Production Deployment** - Deploy messaging features with error handling and monitoring
- **A2P 10DLC Registration** - Register brands and campaigns for US A2P messaging compliance
- **Provider-Agnostic Architecture** - Build systems that support multiple SMS providers (Twilio + Telnyx)

This skill applies to building communication features in applications, setting up SMS notification systems, creating voice IVR systems, or integrating telephony capabilities.

## Quick Reference

### 1. Send Simple SMS (Node.js SDK)
```javascript
const twilio = require('twilio');

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

async function sendSMS(to, from, body) {
  const message = await client.messages.create({
    to: to,
    from: from,
    body: body
  });
  return message;
}

// Usage
await sendSMS('+14155552671', '+14155559999', 'Hello from Twilio!');
```

### 2. Send SMS with HTTP (No SDK)
```javascript
const https = require('https');

function sendSMS(to, from, body) {
  const accountSid = process.env.TWILIO_ACCOUNT_SID;
  const authToken = process.env.TWILIO_AUTH_TOKEN;

  const auth = Buffer.from(`${accountSid}:${authToken}`).toString('base64');

  const postData = new URLSearchParams({
    To: to,
    From: from,
    Body: body
  }).toString();

  const options = {
    hostname: 'api.twilio.com',
    port: 443,
    path: `/2010-04-01/Accounts/${accountSid}/Messages.json`,
    method: 'POST',
    headers: {
      'Authorization': `Basic ${auth}`,
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': postData.length
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => resolve(JSON.parse(data)));
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}
```

### 3. Validate Phone Numbers (E.164 Format)
```javascript
function validateE164(phoneNumber) {
  const e164Regex = /^\+[1-9]\d{1,14}$/;

  if (!e164Regex.test(phoneNumber)) {
    return {
      valid: false,
      error: 'Phone number must be in E.164 format (e.g., +14155552671)'
    };
  }

  return { valid: true };
}

// Normalize US phone numbers to E.164
function formatToE164(number) {
  let digits = number.replace(/\D/g, '');
  if (!digits.startsWith('1')) {
    digits = '1' + digits;
  }
  return '+' + digits;
}
```

### 4. Handle Incoming Messages (Webhook with TwiML)
```javascript
const express = require('express');
app.use(express.urlencoded({ extended: false }));

app.post('/webhooks/twilio', (req, res) => {
  const from = req.body.From;
  const body = req.body.Body;
  const to = req.body.To;

  console.log(`Received: "${body}" from ${from}`);

  // Respond with TwiML
  const twiml = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>Thanks for your message!</Message>
</Response>`;

  res.set('Content-Type', 'text/xml');
  res.send(twiml);
});
```

### 5. Verify Webhook Signatures (HMAC-SHA1)
```javascript
const crypto = require('crypto');

function verifyTwilioSignature(url, params, signature, authToken) {
  // Build data string from sorted params
  const data = Object.keys(params)
    .sort()
    .reduce((acc, key) => acc + key + params[key], url);

  // Generate HMAC-SHA1 signature
  const expectedSignature = crypto
    .createHmac('sha1', authToken)
    .update(Buffer.from(data, 'utf-8'))
    .digest('base64');

  return signature === expectedSignature;
}

// Usage in Express with body-parser
app.post('/webhooks/twilio', (req, res) => {
  const signature = req.headers['x-twilio-signature'];
  const url = `https://${req.headers.host}${req.url}`;

  if (!verifyTwilioSignature(url, req.body, signature, process.env.TWILIO_AUTH_TOKEN)) {
    return res.status(403).send('Forbidden');
  }

  // Process webhook...
  const twiml = '<Response></Response>';
  res.set('Content-Type', 'text/xml');
  res.send(twiml);
});
```

### 6. Twilio SDK Signature Validation
```javascript
const twilio = require('twilio');

app.post('/webhooks/twilio', (req, res) => {
  const signature = req.headers['x-twilio-signature'];
  const url = `https://${req.headers.host}${req.url}`;

  if (!twilio.validateRequest(
    process.env.TWILIO_AUTH_TOKEN,
    signature,
    url,
    req.body
  )) {
    return res.status(403).send('Forbidden');
  }

  // Process webhook...
  const twiml = new twilio.twiml.MessagingResponse();
  twiml.message('Thanks for your message!');

  res.set('Content-Type', 'text/xml');
  res.send(twiml.toString());
});
```

### 7. Send with Error Handling and Retry
```javascript
async function sendWithRetry(to, from, body, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await client.messages.create({ to, from, body });
    } catch (error) {
      if (error.status >= 500 && attempt < maxRetries) {
        // Server error - retry with exponential backoff
        const delayMs = Math.pow(2, attempt) * 1000;
        console.log(`Retry ${attempt} in ${delayMs}ms...`);
        await new Promise(resolve => setTimeout(resolve, delayMs));
      } else {
        throw error;
      }
    }
  }
}
```

### 8. Bulk Sending with Rate Limiting
```javascript
async function sendBulkSMS(recipients, from, body) {
  const delayMs = 100; // 10 messages/second
  const results = [];

  for (const recipient of recipients) {
    try {
      const result = await client.messages.create({ to: recipient, from, body });
      results.push({ success: true, to: recipient, sid: result.sid });
    } catch (error) {
      results.push({ success: false, to: recipient, error: error.message });
    }

    await new Promise(resolve => setTimeout(resolve, delayMs));
  }

  return results;
}
```

### 9. Provider-Agnostic Webhook Handler (Twilio + Telnyx)
```typescript
// From Twilio-Aldea production codebase
function detectProvider(payload: any): 'twilio' | 'telnyx' {
  // Telnyx uses JSON with data.event_type
  if (payload.data && payload.data.event_type) {
    return 'telnyx';
  }

  // Twilio uses form-urlencoded with MessageSid
  if (payload.MessageSid || payload.From) {
    return 'twilio';
  }

  throw new Error('Unknown SMS provider');
}

// Unified webhook handler
app.post('/api/sms/webhook', async (req, res) => {
  const providerType = detectProvider(req.body);

  if (providerType === 'twilio') {
    // Validate Twilio signature
    // Return TwiML response
    const twiml = '<?xml version="1.0"?><Response></Response>';
    res.set('Content-Type', 'text/xml');
    res.send(twiml);
  } else {
    // Validate Telnyx Ed25519 signature
    // Return JSON response
    res.status(200).json({ status: 'ok' });
  }
});
```

### 10. Handle Common Errors
```javascript
function handleTwilioError(error) {
  if (!error.status) {
    return { type: 'NETWORK_ERROR', retriable: true };
  }

  switch (error.status) {
    case 400:
    case 422:
      // Validation error
      return {
        type: 'VALIDATION_ERROR',
        message: error.message,
        code: error.code,
        retriable: false
      };

    case 401:
      // Check Account SID and Auth Token
      return { type: 'AUTH_ERROR', retriable: false };

    case 429:
      // Rate limit
      return {
        type: 'RATE_LIMIT',
        retriable: true,
        retryAfter: 60
      };

    case 500:
    case 502:
    case 503:
      // Server error
      return { type: 'SERVER_ERROR', retriable: true };

    default:
      return { type: 'UNKNOWN_ERROR', retriable: false };
  }
}
```

## Key Concepts

### 1. E.164 Phone Number Format
International phone number format: `+[country code][number]`
- US Example: `+14155552671`
- UK Example: `+442071234567`
- Always include the `+` prefix
- Maximum 15 digits (excluding +)

### 2. Authentication (Basic Auth)
Twilio uses HTTP Basic Authentication with Account SID as username and Auth Token as password:
```
Authorization: Basic base64(ACCOUNT_SID:AUTH_TOKEN)
```

### 3. TwiML (Twilio Markup Language)
XML-based response format for webhooks:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>Your message text here</Message>
</Response>
```

Common TwiML verbs:
- `<Message>` - Send SMS/MMS reply
- `<Redirect>` - Redirect to another URL
- `<Dial>` - Make voice call
- `<Say>` - Text-to-speech
- `<Play>` - Play audio file

### 4. Webhook Events
Twilio sends form-urlencoded POST requests with:
- `MessageSid` - Unique message identifier
- `From` - Sender phone number
- `To` - Recipient phone number
- `Body` - Message text
- `MessageStatus` - Message status (queued, sent, delivered, failed, undelivered)
- `NumMedia` - Number of media attachments (MMS)

### 5. Message Status Lifecycle
- `queued` - Message accepted by Twilio
- `sending` - Being sent to carrier
- `sent` - Sent to carrier
- `delivered` - Delivered to recipient (requires StatusCallback)
- `undelivered` - Failed to deliver
- `failed` - Permanent failure

### 6. Signature Validation (HMAC-SHA1)
Twilio signs webhooks with HMAC-SHA1:
1. Concatenate URL + sorted parameters
2. Generate HMAC-SHA1 with Auth Token as key
3. Base64 encode the result
4. Compare with `X-Twilio-Signature` header

### 7. A2P 10DLC Registration
For US messaging, register:
1. **Brand** - Your business entity
2. **Campaign** - Use case (Customer Care, Marketing, 2FA, etc.)
3. **Phone Numbers** - Associate numbers with campaign

**Timeline**: 5-7 business days for approval

### 8. Message Encoding and Segmentation
- **GSM-7**: 160 chars/segment for standard ASCII
- **UCS-2**: 70 chars/segment for emoji/unicode
- Long messages split into segments (max 10)
- Multi-part: GSM-7 = 153 chars/segment, UCS-2 = 67 chars/segment

## Production Patterns from Twilio-Aldea

### Pattern 1: Provider-Agnostic Webhook Architecture
```typescript
// Support both Twilio and Telnyx from single endpoint
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const rawBody = await readRawBody(req);

  // Auto-detect provider
  let payload: any;
  try {
    payload = JSON.parse(rawBody); // Telnyx
  } catch {
    payload = parseFormUrlEncoded(rawBody); // Twilio
  }

  const providerType = detectProvider(payload);
  const provider = getProviderByType(providerType);

  // Validate signature
  const isValid = provider.validateSignature(req, rawBody);
  if (!isValid) {
    return res.status(403).json({ error: 'Invalid signature' });
  }

  // Process message
  await processIncomingSMS(payload, provider);

  // Return provider-specific response
  if (providerType === 'twilio') {
    res.set('Content-Type', 'text/xml');
    res.send('<?xml version="1.0"?><Response></Response>');
  } else {
    res.status(200).json({ status: 'ok' });
  }
}
```

### Pattern 2: Raw Body Preservation for Signature Validation
```typescript
// Next.js API route config
export const config = {
  api: {
    bodyParser: false,  // Preserve raw body
  },
};

async function readRawBody(req: NextApiRequest): Promise<string> {
  return new Promise<string>((resolve, reject) => {
    let data = '';
    req.setEncoding('utf8');
    req.on('data', (chunk) => { data += chunk; });
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}
```

### Pattern 3: Fast Mode vs Compute Mode
```typescript
// Environment variable: SMS_FAST_MODE=true/false
const fastMode = process.env.SMS_FAST_MODE?.toLowerCase() !== 'false';

if (fastMode) {
  // Return immediate acknowledgment
  res.status(200).send(twiml);

  // Process async in background
  processIncomingSMS(payload).catch(console.error);
} else {
  // Wait for AI processing
  await processIncomingSMS(payload);
  res.status(200).send(twiml);
}
```

### Pattern 4: TwiML Response Builder
```typescript
function buildTwiMLResponse(message?: string): string {
  if (!message) {
    return '<?xml version="1.0" encoding="UTF-8"?><Response></Response>';
  }

  // Escape XML special characters
  const escaped = message
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');

  return `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>${escaped}</Message>
</Response>`;
}
```

### Pattern 5: Idempotency with Database
```typescript
// PostgreSQL with unique constraint on message_sid
async function processWebhookIdempotent(messageSid: string, client: any) {
  try {
    await client.query('BEGIN');

    await client.query(
      'INSERT INTO processed_webhooks (message_sid, processed_at) VALUES ($1, NOW())',
      [messageSid]
    );

    await handleMessage(messageSid, client);
    await client.query('COMMIT');
  } catch (error: any) {
    await client.query('ROLLBACK');

    if (error.code === '23505') { // Duplicate key
      console.log('Message already processed');
      return;
    }

    throw error;
  }
}
```

### Pattern 6: Timeout Protection
```typescript
function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number = 25000
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), timeoutMs)
    ),
  ]);
}

// Usage
const result = await withTimeout(
  processIncomingSMS(payload),
  25000
);
```

## API Essentials

### Base URL
```
https://api.twilio.com/2010-04-01
```

### Authentication
```
Authorization: Basic base64(ACCOUNT_SID:AUTH_TOKEN)
```

### Environment Variables
```bash
# .env file
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+18005551234
```

### Rate Limits
- Messaging: 200 messages per second (enterprise)
- Voice: 100 concurrent calls (default)
- API requests: 10,000 per hour (default)

### Common Response Structure
```json
{
  "sid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "date_created": "Wed, 18 Aug 2021 20:01:14 +0000",
  "date_updated": "Wed, 18 Aug 2021 20:01:14 +0000",
  "date_sent": null,
  "account_sid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "to": "+14155552671",
  "from": "+14155559999",
  "body": "Hello from Twilio!",
  "status": "queued",
  "num_segments": "1",
  "num_media": "0",
  "direction": "outbound-api",
  "price": null,
  "price_unit": "USD",
  "uri": "/2010-04-01/Accounts/ACxxx/Messages/SMxxx.json"
}
```

## Quick Start Checklist

- [ ] Sign up for Twilio account at https://www.twilio.com/try-twilio
- [ ] Get Account SID and Auth Token from Console
- [ ] Set up environment variables
- [ ] Purchase a phone number for testing
- [ ] Send your first test SMS (Quick Reference #1)
- [ ] Validate phone numbers (Quick Reference #3)
- [ ] Set up webhook endpoint (use ngrok for local dev)
- [ ] Implement webhook handler with TwiML (Quick Reference #4)
- [ ] Add webhook signature verification (Quick Reference #5 or #6)
- [ ] Test two-way messaging
- [ ] Add error handling with retry logic (Quick Reference #7)
- [ ] (US only) Register for A2P 10DLC if sending to US numbers

## Working with This Skill

### For Beginners

**Start Here:**
1. Use **Quick Reference #1** (Send Simple SMS)
2. Set up environment variables
3. Use **Quick Reference #3** (Validate Phone Numbers)
4. Test sending to your own phone number
5. Set up **Quick Reference #4** (Handle Incoming Messages with TwiML)
6. Test two-way messaging with ngrok

**Key Concepts to Learn:**
- E.164 phone number format
- Basic Authentication (Account SID + Auth Token)
- TwiML XML responses for webhooks
- Message status lifecycle

**Common Beginner Mistakes:**
- Forgetting the `+` prefix in phone numbers
- Not using E.164 format
- Hardcoding credentials instead of environment variables
- Not returning TwiML from webhook endpoints
- Not validating webhook signatures

### For Intermediate Users

**Focus Areas:**
1. Implement **Quick Reference #5 or #6** (Signature Validation)
2. Use **Quick Reference #7** (Error Handling with Retry)
3. Build conversation flows with state machines
4. Implement idempotency (Production Pattern #5)
5. Handle StatusCallback webhooks for delivery notifications

**Key Concepts to Master:**
- HMAC-SHA1 signature validation
- TwiML advanced features
- Message segmentation and cost optimization
- Error handling patterns
- Rate limiting for bulk sending

### For Advanced Users

**Advanced Patterns:**
1. Build provider-agnostic handlers (Production Pattern #1)
2. Implement timeout protection (Production Pattern #6)
3. Design multi-provider architectures
4. Optimize with fast mode vs compute mode (Production Pattern #3)
5. Build IVR systems with Voice API
6. Set up comprehensive monitoring and alerting

**Key Topics:**
- Provider-agnostic webhook architecture
- Database-backed idempotency
- Structured logging and monitoring
- A2P 10DLC compliance
- Production deployment patterns

## Common Error Codes

### Authentication Errors
- `20003` - Authentication failed (check Account SID and Auth Token)
- `20005` - Account not active

### Validation Errors
- `21211` - Invalid 'To' phone number
- `21212` - Invalid 'From' phone number
- `21408` - Permission to send to this number not enabled
- `21610` - Attempt to send to unsubscribed recipient

### Rate Limit Errors
- `20429` - Too many requests (rate limited)

### Message Errors
- `30001` - Queue overflow (system overloaded)
- `30003` - Unreachable destination
- `30004` - Message blocked
- `30005` - Unknown destination
- `30006` - Landline or unreachable carrier
- `30007` - Message filtered (spam)
- `30008` - Unknown error

## Best Practices

### 1. Always Validate Webhook Signatures
```javascript
// Use Twilio SDK for built-in validation
const twilio = require('twilio');

if (!twilio.validateRequest(authToken, signature, url, params)) {
  return res.status(403).send('Forbidden');
}
```

### 2. Return TwiML Immediately
```javascript
// Don't do expensive processing before responding
app.post('/webhook', async (req, res) => {
  // Return TwiML immediately
  res.set('Content-Type', 'text/xml');
  res.send('<Response></Response>');

  // Process async
  processMessage(req.body).catch(console.error);
});
```

### 3. Use StatusCallback for Delivery Tracking
```javascript
await client.messages.create({
  to: '+14155552671',
  from: '+14155559999',
  body: 'Hello!',
  statusCallback: 'https://yourdomain.com/status'
});
```

### 4. Handle Message Segmentation
```javascript
// Keep messages under 160 characters for GSM-7
function optimizeForGSM7(text) {
  return text
    .replace(/[""]/g, '"')
    .replace(/['']/g, "'")
    .replace(/[—–]/g, '-')
    .replace(/…/g, '...');
}
```

### 5. Implement Exponential Backoff
```javascript
async function sendWithBackoff(to, from, body, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await client.messages.create({ to, from, body });
    } catch (error) {
      if (attempt < maxRetries && error.status >= 500) {
        await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
      } else {
        throw error;
      }
    }
  }
}
```

## Resources

- **Twilio Console**: https://console.twilio.com/
- **API Reference**: https://www.twilio.com/docs/api
- **Helper Libraries**: Node.js, Python, PHP, Ruby, C#, Java
- **Status Page**: https://status.twilio.com/
- **Support**: https://support.twilio.com/

## Version Notes

This skill includes:
- Official Twilio API patterns and best practices
- Production code examples from Twilio-Aldea SMS platform
- Provider-agnostic webhook architecture
- TwiML response patterns
- Complete signature validation examples
- TypeScript and JavaScript examples
