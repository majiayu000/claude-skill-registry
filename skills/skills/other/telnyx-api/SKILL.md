---
name: telnyx-api
description: Use this skill when working with Telnyx communication APIs for SMS/MMS messaging, voice calls, phone number management, messaging profiles, webhook integration, two-way SMS conversations, bulk sending, message scheduling, or production deployment of telephony features. v2.0 includes official Telnyx documentation, production patterns from Twilio-Aldea (Ed25519 signature validation, provider-agnostic webhooks, idempotency), and TypeScript code examples.
---

# Telnyx API - Comprehensive Communication Platform

**v2.0 Enhancement**: This skill now includes official Telnyx documentation, production-tested patterns from Twilio-Aldea (including Ed25519 signature validation with tweetnacl, provider-agnostic webhook handlers, and database idempotency), and comprehensive TypeScript examples for SMS/MMS messaging.

## When to Use This Skill

Use this skill when working with Telnyx's communication APIs for:

- **SMS/MMS Messaging** - Send and receive text messages programmatically
- **Voice Communication** - Build voice calling applications with Call Control API
- **Phone Number Management** - Search, purchase, and configure phone numbers
- **Messaging Profiles** - Configure messaging settings and webhooks
- **Webhook Integration** - Handle real-time events and delivery notifications
- **Two-Way SMS Conversations** - Build interactive SMS experiences
- **Bulk SMS Sending** - Send messages to multiple recipients with rate limiting
- **Message Scheduling** - Schedule messages for future delivery
- **Production Deployment** - Deploy messaging features with error handling and monitoring
- **10DLC Registration** - Register brands and campaigns for US A2P messaging compliance

This skill applies to building communication features in applications, setting up SMS notification systems, creating voice IVR systems, or integrating telephony capabilities.

## Quick Reference

### 1. Send Simple SMS
```javascript
const axios = require('axios');

async function sendSMS(to, from, text) {
  const response = await axios.post(
    'https://api.telnyx.com/v2/messages',
    { from, to, text },
    {
      headers: {
        'Authorization': `Bearer ${process.env.TELNYX_API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );
  return response.data;
}

// Usage
await sendSMS('+14155552671', '+14155559999', 'Hello from Telnyx!');
```

### 2. Validate Phone Numbers (E.164 Format)
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

### 3. Handle Incoming Messages (Webhook)
```javascript
const express = require('express');
app.use(express.json());

app.post('/webhooks/telnyx', (req, res) => {
  const event = req.body.data;

  if (event.event_type === 'message.received') {
    const from = event.payload.from.phone_number;
    const text = event.payload.text;
    const to = event.payload.to[0].phone_number;

    console.log(`Received: "${text}" from ${from}`);

    // Auto-reply
    await sendSMS(from, to, 'Thanks for your message!');
  }

  res.status(200).send('OK');
});
```

### 4. Verify Webhook Signatures (Ed25519)
```javascript
const nacl = require('tweetnacl');

function verifyWebhook(rawBody, signature, timestamp, publicKey) {
  // Check timestamp freshness (prevent replay attacks)
  const timestampMs = parseInt(timestamp);
  const now = Date.now();
  if (Math.abs(now - timestampMs) > 5 * 60 * 1000) {
    return false; // Reject if older than 5 minutes
  }

  // Construct signed payload
  const signedPayload = `${timestamp}|${rawBody}`;

  // Decode signature and public key from hex
  const signatureBytes = Buffer.from(signature, 'hex');
  const publicKeyBytes = Buffer.from(publicKey, 'hex');

  // Verify Ed25519 signature
  return nacl.sign.detached.verify(
    Buffer.from(signedPayload, 'utf8'),
    signatureBytes,
    publicKeyBytes
  );
}

// Usage in Express
app.post('/webhooks/telnyx', (req, res) => {
  const signature = req.headers['telnyx-signature-ed25519'];
  const timestamp = req.headers['telnyx-timestamp'];
  const rawBody = JSON.stringify(req.body);

  if (!verifyWebhook(rawBody, signature, timestamp, process.env.TELNYX_PUBLIC_KEY)) {
    return res.status(401).send('Invalid signature');
  }

  // Process webhook...
  res.status(200).send('OK');
});
```

### 5. Send with Error Handling and Retry
```javascript
async function sendWithRetry(to, from, text, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await sendSMS(to, from, text);
    } catch (error) {
      if (error.response?.status >= 500 && attempt < maxRetries) {
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

### 6. Bulk Sending with Rate Limiting
```javascript
async function sendBulkSMS(recipients, from, text) {
  const delayMs = 100; // 10 messages/second
  const results = [];

  for (const recipient of recipients) {
    try {
      const result = await sendSMS(recipient, from, text);
      results.push({ success: true, to: recipient, id: result.data.id });
    } catch (error) {
      results.push({ success: false, to: recipient, error: error.message });
    }

    await new Promise(resolve => setTimeout(resolve, delayMs));
  }

  return results;
}
```

### 7. Idempotent Webhook Processing (Database)
```javascript
// Using PostgreSQL with unique constraint
async function processWebhookIdempotent(event, client) {
  try {
    await client.query('BEGIN');

    // Try to insert event (will fail if duplicate due to unique constraint)
    await client.query(
      'INSERT INTO processed_webhooks (event_id, processed_at) VALUES ($1, NOW())',
      [event.id]
    );

    // Process event
    await handleEvent(event, client);

    await client.query('COMMIT');
  } catch (error) {
    await client.query('ROLLBACK');

    // If duplicate key error, event was already processed
    if (error.code === '23505') {
      console.log('Event already processed, skipping');
      return;
    }

    throw error;
  }
}
```

### 8. Two-Way Conversation State Machine
```javascript
const conversations = new Map();

app.post('/webhooks/telnyx', async (req, res) => {
  const event = req.body.data;

  if (event.event_type === 'message.received') {
    const from = event.payload.from.phone_number;
    const to = event.payload.to[0].phone_number;
    const text = event.payload.text.toLowerCase();

    let state = conversations.get(from) || 'start';
    let reply;

    switch (state) {
      case 'start':
        reply = "Welcome! What's your name?";
        conversations.set(from, 'asked_name');
        break;

      case 'asked_name':
        reply = `Nice to meet you, ${text}! How can I help?`;
        conversations.set(from, 'helping');
        break;

      case 'helping':
        reply = 'Thanks! A human will respond shortly.';
        conversations.delete(from);
        break;
    }

    await sendSMS(from, to, reply);
  }

  res.status(200).send('OK');
});
```

### 9. Check 10DLC Campaign Status
```bash
#!/bin/bash
# Monitor campaign approval status

CAMPAIGN_ID="your-campaign-id"
API_KEY="your-api-key"

STATUS=$(curl -s "https://api.telnyx.com/v2/10dlc/campaign/${CAMPAIGN_ID}" \
  -H "Authorization: Bearer ${API_KEY}" \
  | jq -r '.campaignStatus')

echo "Campaign status: ${STATUS}"

# Status values:
# - TCR_ACCEPTED: Campaign Registry approved (not yet ready)
# - MNO_PENDING: Waiting for carrier approval
# - MNO_PROVISIONED: Fully approved and ready for production
```

### 10. Handle Common Errors
```javascript
function handleTelnyxError(error) {
  if (!error.response) {
    return { type: 'NETWORK_ERROR', retriable: true };
  }

  const status = error.response.status;
  const errorData = error.response.data.errors?.[0];

  switch (status) {
    case 400:
    case 422:
      // Validation error - fix input
      return {
        type: 'VALIDATION_ERROR',
        message: errorData?.detail || 'Invalid request',
        retriable: false
      };

    case 401:
      // Check API key
      return { type: 'AUTH_ERROR', retriable: false };

    case 429:
      // Rate limit - wait and retry
      return {
        type: 'RATE_LIMIT',
        retriable: true,
        retryAfter: 60
      };

    case 500:
    case 502:
    case 503:
      // Server error - retry with backoff
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

### 2. Messaging Profiles
A configuration container that groups numbers and defines webhook settings. Benefits:
- Centralized webhook management
- Number pools for load distribution
- Alphanumeric sender IDs
- Easy number management
- Webhook failover URLs

### 3. Message Encoding and Segmentation
- **GSM-7**: 160 chars/segment for standard ASCII (cheaper)
- **UCS-2**: 70 chars/segment for emoji/unicode (more expensive)
- Long messages split into segments (max 10)
- Multi-part messages: GSM-7 = 153 chars/segment, UCS-2 = 67 chars/segment

### 4. Webhook Events
Real-time notifications about message status:
- `message.sent` - Sent to carrier
- `message.delivered` - Delivered to recipient
- `message.failed` - Delivery failed
- `message.received` - Inbound message received
- `message.finalized` - Reached final state

### 5. 10DLC Campaign Approval Stages
**Critical understanding for US messaging:**
1. **TCR_ACCEPTED** - Campaign Registry approved (can't send yet)
2. **MNO_PENDING** - Waiting for carrier approval (1-3 days)
3. **MNO_PROVISIONED** - Fully approved and ready (can associate numbers and send)

### 6. Authentication
All API requests require Bearer token authentication:
```
Authorization: Bearer YOUR_API_KEY
```
Store API keys in environment variables, never hardcode.

## Reference Files

The `references/` directory contains detailed documentation:

### authentication.md
Complete guide to API key management and security:
- Creating and managing API keys
- Environment variable setup (Node.js, Python, Docker, Kubernetes)
- Best practices for key rotation and security
- IP whitelisting configuration
- Webhook signature verification
- Common authentication errors and solutions

### messaging-api.md
Full Messaging API reference:
- Complete endpoint documentation (`/v2/messages`)
- All request/response parameters
- Message status values and lifecycle
- Character encoding details (GSM-7 vs UCS-2)
- Message segmentation rules
- MMS limitations and supported formats
- Pagination and filtering options

### webhooks.md
Comprehensive webhook reference:
- All webhook event types with payload examples
- Ed25519 signature verification (secure)
- HMAC-SHA256 signature verification (legacy)
- Webhook configuration (global, profile, per-message)
- Best practices (idempotency, async processing, retries)
- Testing webhooks locally with ngrok
- Complete webhook handler example
- Troubleshooting guide

### error-codes.md
Complete error reference and handling:
- All HTTP status codes and meanings
- Common error codes with solutions
- Validation errors (10001-10007)
- Rate limiting errors (429)
- Server errors (500, 502, 503)
- Webhook-specific delivery errors
- Comprehensive error handler implementation
- Retry strategies with exponential backoff

### best-practices.md
Production deployment patterns:
- Using messaging profiles in production
- Robust error handling patterns
- Exponential backoff retry logic
- Rate limiting for bulk sending
- Message tracking and status monitoring
- Phone number validation and formatting
- Message content optimization
- Character limit handling
- Webhook async processing with queues
- Idempotency implementation
- Structured logging and monitoring
- Cost optimization strategies
- Testing patterns
- Production deployment checklist

### number-management.md
Phone number operations:
- Searching available numbers
- Purchasing phone numbers
- Configuring number settings
- Porting existing numbers
- Number pool management

### 10dlc.md
10DLC (10-Digit Long Code) registration and compliance:
- **Campaign approval stages** (TCR_ACCEPTED → MNO_PENDING → MNO_PROVISIONED)
- Brand and campaign registration process
- Use case selection (Customer Care, Marketing, 2FA, etc.)
- TCPA and CTIA compliance requirements
- Required message elements (opt-in, opt-out, HELP)
- Monitoring campaign status via API
- Phone number association (portal-only, not via API)
- Cost structure and timeline expectations (3-5 business days)
- Common issues and troubleshooting
- Production checklist

## Official Telnyx Documentation (NEW)

Complete official documentation extracted from developers.telnyx.com:

- **`references/official-docs/webhooks.md`** - Complete webhook guide with signature verification, event types, and best practices
- **`references/official-docs/messaging.md`** - Messaging API reference with SMS/MMS endpoints, character encoding, and segmentation
- **`references/official-docs/authentication.md`** - API authentication, security, and best practices
- **`references/official-docs/sdks.md`** - Server-side SDK documentation for Node.js, Python, Ruby, PHP, Java, C#, Go

## Production Patterns (NEW)

Real-world patterns from Twilio-Aldea production codebase:

- **`references/production-patterns.md`** - 8 battle-tested patterns including:
  - **Pattern 1**: Ed25519 Signature Validation with tweetnacl (secure webhook authentication)
  - **Pattern 2**: Provider-Agnostic Webhook Handler (support Twilio + Telnyx from single endpoint)
  - **Pattern 3**: Raw Body Parsing for Signature Validation (preserve exact bytes)
  - **Pattern 4**: Idempotency with Database Unique Constraint (prevent duplicate processing)
  - **Pattern 5**: Messaging Profile Configuration (production-ready setup)
  - **Pattern 6**: Debugger Mode with Phone Number Detection (cost-free testing)
  - **Pattern 7**: Error Logging to Database with Categorization (persistent, queryable tracking)
  - **Pattern 8**: E.164 Phone Number Normalization (handle all formats)

## Code Examples (NEW)

Production-ready TypeScript examples:

- **`assets/examples/webhook-handler.ts`** - Complete webhook handler with Ed25519 signature validation
- **`assets/examples/send-sms.ts`** - SMS/MMS sending examples with error handling and retry logic
- **`assets/examples/provider-implementation.ts`** - Full production provider class from Twilio-Aldea

## GitHub Repository (NEW)

### `references/github/README.md`
Official Telnyx Node.js SDK README from GitHub (team-telnyx/telnyx-node, 62 stars)

### `references/github/issues.md`
16 GitHub issues showing common problems and solutions:
- Webhook signature validation issues
- TypeScript type definitions
- SDK initialization errors
- Rate limiting handling
- Environment configuration

### `references/github/CHANGELOG.md`
Complete SDK version history with breaking changes and migrations

### `references/github/releases.md`
81 GitHub releases with detailed SDK changelog

### `references/github/file_structure.md`
Repository structure (2,129 files) showing SDK source code organization

## Working with This Skill

### For Beginners

**Start Here:**
1. Use **Quick Reference Example #1** (Send Simple SMS)
2. Set up environment variables for API key
3. Use **Quick Reference Example #2** (Validate Phone Numbers)
4. Test sending to your own phone number
5. Set up **Quick Reference Example #3** (Handle Incoming Messages)
6. Test two-way messaging with ngrok

**Key Concepts to Learn:**
- E.164 phone number format (always starts with +)
- Bearer token authentication
- Basic webhook handling
- Message encoding (GSM-7 vs UCS-2)

**Reference Files:**
- Start with `authentication.md` for setup
- Check `messaging-api.md` for basic API usage
- Review `error-codes.md` when errors occur
- Use `webhooks.md` for receiving messages

**Common Beginner Mistakes:**
- Forgetting the `+` prefix in phone numbers
- Not using E.164 format (e.g., using `(415) 555-2671` instead of `+14155552671`)
- Hardcoding API keys instead of using environment variables
- Not validating webhook signatures

### For Intermediate Users

**Focus Areas:**
1. Implement **Quick Reference Example #4** (Verify Webhook Signatures with Ed25519)
2. Use **Quick Reference Example #5** (Error Handling with Retry)
3. Build conversation flows with **Quick Reference Example #8** (State Machine)
4. Create a messaging profile (see `best-practices.md`)
5. Implement **Quick Reference Example #7** (Database Idempotency)

**Key Concepts to Master:**
- Messaging profiles for production
- Ed25519 webhook signature verification (more secure than HMAC)
- Error handling patterns with retry logic
- Message segmentation and cost optimization
- Idempotency for webhook processing
- Rate limiting for bulk sending

**Reference Files:**
- Study `webhooks.md` for event types and security
- Review `best-practices.md` for production patterns
- Use `error-codes.md` for comprehensive error handling
- Check `production-patterns.md` for real-world implementations

**Production Considerations:**
- Always verify webhook signatures (use Ed25519, not HMAC-SHA256)
- Implement idempotency to prevent duplicate processing
- Use exponential backoff for retries
- Log all errors to a database for debugging
- Monitor message delivery rates

### For Advanced Users

**Advanced Patterns:**
1. Implement bulk messaging from `best-practices.md` with queue system (Bull/Redis)
2. Build provider-agnostic handlers (Pattern 2 in `production-patterns.md`)
3. Set up comprehensive error logging (Pattern 7 in `production-patterns.md`)
4. Implement debugger mode for cost-free testing (Pattern 6)
5. Optimize message costs with encoding strategies
6. Build IVR systems with Call Control API
7. Set up number pools for high-volume messaging
8. Implement comprehensive monitoring and alerting

**Key Topics:**
- Message queue systems (Bull/Redis) for async processing
- Database-backed idempotency with unique constraints
- Structured logging (Winston)
- Metrics collection (Prometheus)
- Production deployment patterns
- Multi-provider architectures with unified interfaces
- 10DLC campaign registration and monitoring
- Webhook failover and retry mechanisms

**Reference Files:**
- Deep dive into `best-practices.md` for all production patterns
- Study `error-codes.md` for comprehensive error handling
- Review `webhooks.md` for advanced webhook patterns
- Analyze `production-patterns.md` for battle-tested implementations
- Check `10dlc.md` for US A2P messaging compliance

**Architecture Patterns:**
- Provider-agnostic design (support multiple SMS providers)
- Event-driven architecture with message queues
- Database-backed state machines for conversations
- Webhook retry mechanisms with exponential backoff
- Cost optimization with debugger mode detection
- Multi-region deployment with failover

## API Essentials

### Base URL
```
https://api.telnyx.com/v2
```

### Authentication Header
```
Authorization: Bearer YOUR_API_KEY
```

### Environment Variables
```bash
# .env file
TELNYX_API_KEY=KEY019A080F468AAFD4AF4F6888D7795244_xxx
TELNYX_PUBLIC_KEY=your_public_key_for_webhook_validation
TELNYX_MESSAGING_PROFILE_ID=abc85f64-5717-4562-b3fc-2c9600000000
```

### Rate Limits
- Standard accounts: 10 requests/second per endpoint
- High-volume accounts: Contact Telnyx for increased limits
- Implement exponential backoff for 429 responses

### Common Response Structure
```json
{
  "data": {
    "id": "message-uuid",
    "type": "SMS",
    "from": { "phone_number": "+18445550001" },
    "to": [{ "phone_number": "+18665550001", "status": "queued" }],
    "text": "Hello!",
    "cost": { "amount": "0.0051", "currency": "USD" }
  }
}
```

## Quick Start Checklist

- [ ] Sign up for Telnyx account at https://telnyx.com/sign-up
- [ ] Generate API key in Mission Control Portal
- [ ] Set up environment variables (never hardcode keys)
- [ ] Purchase a phone number for testing
- [ ] Send your first test SMS (Quick Reference #1)
- [ ] Validate phone numbers (Quick Reference #2)
- [ ] Set up webhook endpoint (use ngrok for local dev)
- [ ] Implement webhook handler (Quick Reference #3)
- [ ] Add Ed25519 webhook signature verification (Quick Reference #4)
- [ ] Test two-way messaging
- [ ] Add error handling with retry logic (Quick Reference #5)
- [ ] Configure messaging profile for production
- [ ] (US only) Register for 10DLC if sending A2P messages

## Navigation by Experience Level

### Beginners (Getting Started)

1. Start with **Quick Reference Example #1** (Send Simple SMS)
2. Review `references/authentication.md` for API setup
3. Study `references/messaging-api.md` for message API basics
4. Use **Quick Reference Example #2** (Validate Phone Numbers)
5. Set up webhooks with **Quick Reference Example #3**
6. Test locally with ngrok

### Intermediate (Building Features)

1. Implement Ed25519 signature validation (**Quick Reference #4**)
2. Study `references/webhooks.md` for advanced webhook patterns
3. Use messaging profiles (see `best-practices.md`)
4. Implement idempotency (**Quick Reference #7**)
5. Build conversation state machines (**Quick Reference #8**)
6. Review `assets/examples/webhook-handler.ts` for complete implementation

### Advanced (Production Deployment)

1. Build provider-agnostic handlers (`production-patterns.md` Pattern 2)
2. Implement error logging and monitoring (`production-patterns.md` Pattern 7)
3. Design multi-provider architectures with unified interfaces
4. Optimize for production with all 8 patterns from `production-patterns.md`
5. Study Twilio-Aldea patterns for SMS-based AI platform architecture
6. Set up monitoring, alerting, and metrics collection

## Key Enhancements in v2.0

### Official Documentation Integration
- **Webhooks Guide**: Complete Ed25519 signature verification, event types, retry logic
- **Messaging API**: Full endpoint reference, character encoding (GSM-7 vs UCS-2), segmentation rules
- **Authentication**: API key management, security best practices, environment variable setup
- **SDK Reference**: Server-side SDK documentation for 7 languages

### Production Patterns
- **Ed25519 Signature Validation**: Production-tested tweetnacl implementation (solved security validation issues)
- **Provider-Agnostic Design**: Support multiple SMS providers from single endpoint
- **Raw Body Preservation**: Correct signature validation with exact byte sequences
- **Database Idempotency**: PostgreSQL unique constraint pattern (prevents duplicate processing)
- **Messaging Profiles**: Production deployment with centralized webhook management
- **Debugger Mode**: Cost-free testing pattern from live platform
- **Error Logging**: Database-backed error tracking with categorization
- **E.164 Normalization**: Handle all phone number formats correctly

### Code Examples
- **TypeScript Examples**: Webhook handler, SMS sending, complete provider class with full type safety
- **Production Patterns**: Real implementations from Twilio-Aldea SMS platform
- **Security Examples**: Ed25519 validation, raw body parsing, signature verification

### Data Sources
- **Official Telnyx Documentation** (via Firecrawl)
- **Exa Code Context** (8000+ tokens of Telnyx patterns from real repositories)
- **Twilio-Aldea Production Codebase** (SMS-based AI therapy platform deployed on Netlify)

## Version History

- **v2.0** (2025-11-01) - Enhanced with official Telnyx documentation, production patterns from Twilio-Aldea (Ed25519 validation, provider-agnostic webhooks, idempotency), TypeScript examples, and comprehensive messaging API guide
- **v1.0** - Initial skill creation with quick reference, error codes, and basic messaging patterns

## Additional Resources

- **Telnyx Developer Portal**: https://developers.telnyx.com/
- **API Reference**: https://developers.telnyx.com/api/
- **Mission Control Portal**: https://portal.telnyx.com/
- **Status Page**: https://status.telnyx.com/
- **Support Portal**: https://support.telnyx.com/
- **Official SDKs**: Node.js, Python, Ruby, PHP, Java, C#, Go

## Common Patterns

### Pattern: Message with Tracking
```javascript
const tracker = new Map();

async function sendTrackedMessage(to, from, text) {
  const response = await sendSMS(to, from, text);
  tracker.set(response.data.data.id, {
    to, from, text,
    status: 'queued',
    sentAt: new Date()
  });
  return response;
}

// In webhook handler
app.post('/webhooks/telnyx', (req, res) => {
  const event = req.body.data;
  if (event.event_type === 'message.delivered') {
    const msg = tracker.get(event.payload.id);
    if (msg) msg.status = 'delivered';
  }
  res.status(200).send('OK');
});
```

### Pattern: Format to E.164
```javascript
function formatToE164(number, defaultCountryCode = '1') {
  let digits = number.replace(/\D/g, '');
  if (!digits.startsWith(defaultCountryCode)) {
    digits = defaultCountryCode + digits;
  }
  return '+' + digits;
}

// Examples
formatToE164('415-555-2671');      // +14155552671
formatToE164('(415) 555-2671');    // +14155552671
formatToE164('+1 415-555-2671');   // +14155552671
```

### Pattern: Optimize Message Cost
```javascript
// Prefer GSM-7 encoding (cheaper, longer)
function optimizeForGSM7(text) {
  // Replace unicode quotes with GSM-7 quotes
  return text
    .replace(/[""]/g, '"')
    .replace(/['']/g, "'")
    .replace(/[—–]/g, '-')
    .replace(/…/g, '...');
}
```

## Support and Troubleshooting

### Getting Help
1. Check `error-codes.md` for specific error messages
2. Review `best-practices.md` for common patterns
3. Visit https://status.telnyx.com/ for service status
4. Contact support through Mission Control Portal
5. Check `10dlc.md` if having issues with US A2P messaging

### Common Issues
- **401 Unauthorized**: Check API key format (`Bearer YOUR_API_KEY`)
- **10001 Invalid phone number**: Ensure E.164 format (`+14155552671`)
- **429 Rate limit**: Implement rate limiting (Quick Reference #6)
- **Webhooks not received**: Verify URL is publicly accessible with valid SSL
- **Messages not delivering in US**: Check 10DLC campaign status (must be MNO_PROVISIONED)

### Debugging Tips
```javascript
// Enable request/response logging
axios.interceptors.request.use(request => {
  console.log('Request:', request.url, request.data);
  return request;
});

axios.interceptors.response.use(
  response => {
    console.log('Response:', response.status, response.data);
    return response;
  },
  error => {
    console.error('Error:', error.response?.data);
    return Promise.reject(error);
  }
);
```
