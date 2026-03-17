---
name: api-integration-builder
description: Build reliable third-party API integrations including OAuth, webhooks, rate limiting, error handling, and data sync. Use when integrating with external services (Slack, Stripe, Gmail, etc.), building API connections, handling webhooks, or implementing OAuth flows.
license: Complete terms in LICENSE.txt
---

# API Integration Builder

Build reliable, maintainable integrations with third-party APIs.

## Core Principles

1. **Assume failure**: APIs will go down, rate limits will hit, data will be inconsistent
2. **Idempotency matters**: Retries shouldn't cause duplicate actions
3. **User experience first**: Never show users "API Error 429"
4. **Security always**: Tokens are secrets, validate all data, assume malicious input

## Integration Architecture

### Basic Integration Flow

```
Your App ←→ Integration Layer ←→ Third-Party API
            ├── Auth (OAuth, API keys)
            ├── Rate limiting
            ├── Retries
            ├── Error handling
            ├── Data transformation
            └── Webhooks (if supported)
```

### Components

1. **Authentication Layer**: Handle OAuth, refresh tokens, API keys
2. **Request Manager**: Make API calls with retries, rate limiting
3. **Webhook Handler**: Receive real-time updates from third parties
4. **Data Sync**: Keep your data in sync with external service
5. **Error Recovery**: Handle failures gracefully

## Authentication Patterns

### API Key Authentication

**Simple but limited**:

```typescript
interface APIKeyConfig {
  api_key: string
  api_secret?: string
}

class SimpleAPIClient {
  private apiKey: string

  async request(endpoint: string, options: RequestOptions) {
    return fetch(`https://api.service.com${endpoint}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      }
    })
  }
}
```

**Pros**: Simple, no complex flows
**Cons**: Can't act on behalf of users, no granular permissions

### OAuth 2.0 Flow

**The standard for user-authorized access**:

```typescript
// 1. Redirect user to authorize
app.get('/connect/slack', (req, res) => {
  const authUrl = new URL('https://slack.com/oauth/v2/authorize')
  authUrl.searchParams.set('client_id', SLACK_CLIENT_ID)
  authUrl.searchParams.set('redirect_uri', 'https://yourapp.com/auth/slack/callback')
  authUrl.searchParams.set('scope', 'channels:read,chat:write')
  authUrl.searchParams.set('state', generateSecureRandomString()) // CSRF protection

  res.redirect(authUrl.toString())
})

// 2. Handle callback
app.get('/auth/slack/callback', async (req, res) => {
  const { code, state } = req.query

  // Verify state to prevent CSRF
  if (state !== req.session.oauthState) {
    throw new Error('Invalid state')
  }

  // Exchange code for access token
  const tokenResponse = await fetch('https://slack.com/api/oauth.v2.access', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: SLACK_CLIENT_ID,
      client_secret: SLACK_CLIENT_SECRET,
      code: code,
      redirect_uri: 'https://yourapp.com/auth/slack/callback'
    })
  })

  const { access_token, refresh_token, expires_in } = await tokenResponse.json()

  // Store tokens securely (encrypted!)
  await db.storeIntegration({
    user_id: req.user.id,
    service: 'slack',
    access_token: encrypt(access_token),
    refresh_token: encrypt(refresh_token),
    expires_at: Date.now() + expires_in * 1000
  })

  res.redirect('/settings/integrations?success=slack')
})
```

**Token Refresh**:

```typescript
async function getValidAccessToken(userId: string, service: string) {
  const integration = await db.getIntegration(userId, service)

  // Token still valid?
  if (integration.expires_at > Date.now() + 60000) {
    // 1 min buffer
    return decrypt(integration.access_token)
  }

  // Refresh token
  const refreshResponse = await fetch('https://slack.com/api/oauth.v2.access', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: SLACK_CLIENT_ID,
      client_secret: SLACK_CLIENT_SECRET,
      grant_type: 'refresh_token',
      refresh_token: decrypt(integration.refresh_token)
    })
  })

  const { access_token, expires_in } = await refreshResponse.json()

  // Update stored tokens
  await db.updateIntegration(integration.id, {
    access_token: encrypt(access_token),
    expires_at: Date.now() + expires_in * 1000
  })

  return access_token
}
```

## Request Management

### Rate Limiting

**Client-side rate limiting**:

```typescript
import { RateLimiter } from 'limiter'

class RateLimitedAPIClient {
  private limiter: RateLimiter

  constructor(tokensPerInterval: number, interval: string) {
    this.limiter = new RateLimiter({
      tokensPerInterval,
      interval
    })
  }

  async request(endpoint: string, options: RequestOptions) {
    // Wait for rate limit token
    await this.limiter.removeTokens(1)

    return fetch(`https://api.service.com${endpoint}`, options)
  }
}

// Example: Slack allows ~1 request per second
const slackClient = new RateLimitedAPIClient(1, 'second')
```

**429 Response handling**:

```typescript
async function requestWithRetry(url: string, options: RequestOptions, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const response = await fetch(url, options)

    if (response.status === 429) {
      // Check Retry-After header
      const retryAfter = response.headers.get('Retry-After')
      const waitTime = retryAfter ? parseInt(retryAfter) * 1000 : Math.pow(2, attempt) * 1000

      console.log(`Rate limited, waiting ${waitTime}ms`)
      await sleep(waitTime)
      continue
    }

    return response
  }

  throw new Error('Max retries exceeded')
}
```

### Error Handling

**Comprehensive error handling**:

```typescript
class APIError extends Error {
  constructor(
    public statusCode: number,
    public response: any,
    public retryable: boolean
  ) {
    super(`API Error: ${statusCode}`)
  }
}

async function safeAPIRequest(endpoint: string, options: RequestOptions) {
  try {
    const response = await fetch(endpoint, options)

    // Success
    if (response.ok) {
      return await response.json()
    }

    // Client errors (4xx) - usually not retryable
    if (response.status >= 400 && response.status < 500) {
      if (response.status === 401) {
        // Token expired, refresh and retry
        await refreshAccessToken()
        return safeAPIRequest(endpoint, options)
      }

      if (response.status === 429) {
        // Rate limited, retry with backoff
        throw new APIError(429, await response.json(), true)
      }

      // Other 4xx errors - don't retry
      throw new APIError(response.status, await response.json(), false)
    }

    // Server errors (5xx) - retryable
    if (response.status >= 500) {
      throw new APIError(response.status, await response.json(), true)
    }
  } catch (error) {
    if (error instanceof APIError) throw error

    // Network errors - retryable
    throw new APIError(0, { message: error.message }, true)
  }
}
```

**Exponential backoff**:

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn()
    } catch (error) {
      if (error instanceof APIError && !error.retryable) {
        throw error // Don't retry non-retryable errors
      }

      if (attempt === maxRetries - 1) {
        throw error // Last attempt failed
      }

      // Exponential backoff with jitter
      const delay = baseDelay * Math.pow(2, attempt) * (0.5 + Math.random() * 0.5)
      console.log(`Attempt ${attempt + 1} failed, retrying in ${delay}ms`)
      await sleep(delay)
    }
  }

  throw new Error('Unreachable')
}

// Usage
const data = await retryWithBackoff(() => slackClient.postMessage('#general', 'Hello!'))
```

## Webhook Handling

### Receiving Webhooks

```typescript
interface WebhookPayload {
  event_type: string
  data: any
  timestamp: number
  signature: string
}

app.post('/webhooks/stripe', async (req, res) => {
  // 1. Verify signature (CRITICAL for security)
  const signature = req.headers['stripe-signature']
  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(req.body, signature, STRIPE_WEBHOOK_SECRET)
  } catch (error) {
    console.error('⚠️ Webhook signature verification failed:', error.message)
    return res.status(400).send('Webhook signature verification failed')
  }

  // 2. Respond immediately (don't make webhook wait)
  res.status(200).send('Received')

  // 3. Process asynchronously
  await queue.add('process-webhook', {
    event_type: event.type,
    event_id: event.id,
    data: event.data
  })
})

// Process webhook in background job
async function processWebhook(job: Job) {
  const { event_type, event_id, data } = job.data

  // Idempotency check (handle duplicate webhooks)
  const existing = await db.webhookEvents.findOne({ event_id })
  if (existing) {
    console.log(`Webhook ${event_id} already processed`)
    return
  }

  // Mark as processing
  await db.webhookEvents.create({ event_id, status: 'processing' })

  try {
    switch (event_type) {
      case 'payment_intent.succeeded':
        await handlePaymentSuccess(data)
        break

      case 'customer.subscription.deleted':
        await handleSubscriptionCancelled(data)
        break

      // ... other event types
    }

    // Mark as completed
    await db.webhookEvents.update(event_id, { status: 'completed' })
  } catch (error) {
    // Mark as failed, will retry
    await db.webhookEvents.update(event_id, {
      status: 'failed',
      error: error.message,
      retry_count: (existing?.retry_count || 0) + 1
    })
    throw error // Let queue retry
  }
}
```

### Webhook Security

```typescript
// HMAC signature verification
function verifyWebhookSignature(payload: string, signature: string, secret: string): boolean {
  const expectedSignature = crypto.createHmac('sha256', secret).update(payload).digest('hex')

  // Constant-time comparison to prevent timing attacks
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSignature))
}

// Timestamp validation (prevent replay attacks)
function validateWebhookTimestamp(timestamp: number, toleranceSeconds = 300) {
  const now = Math.floor(Date.now() / 1000)
  return Math.abs(now - timestamp) < toleranceSeconds
}
```

## Data Synchronization

### Sync Strategy

```typescript
interface SyncStrategy {
  // Full sync: Get all data from API
  fullSync(): Promise<void>

  // Incremental sync: Get only changed data since last sync
  incrementalSync(since: Date): Promise<void>

  // Real-time sync: Use webhooks for instant updates
  realTimeSync(webhookData: any): Promise<void>
}

class GoogleCalendarSync implements SyncStrategy {
  async fullSync() {
    const calendars = await googleCalendar.list()

    for (const calendar of calendars) {
      const events = await googleCalendar.events.list({
        calendarId: calendar.id,
        maxResults: 2500
      })

      await db.events.bulkUpsert(events)
    }
  }

  async incrementalSync(since: Date) {
    const events = await googleCalendar.events.list({
      updatedMin: since.toISOString(),
      showDeleted: true // Important: track deletions
    })

    for (const event of events) {
      if (event.status === 'cancelled') {
        await db.events.delete(event.id)
      } else {
        await db.events.upsert(event)
      }
    }
  }

  async realTimeSync(webhookData: any) {
    // Google sends channel notifications
    const { resourceId, resourceUri } = webhookData

    // Fetch the changed resource
    const event = await googleCalendar.events.get(resourceId)
    await db.events.upsert(event)
  }
}
```

### Sync Scheduler

```typescript
interface SyncJob {
  user_id: string
  service: string
  type: 'full' | 'incremental'
}

// Schedule sync jobs
async function scheduleSyncJobs() {
  // Full sync: Weekly for all active integrations
  cron.schedule('0 0 * * 0', async () => {
    const integrations = await db.integrations.findActive()

    for (const integration of integrations) {
      await queue.add('sync', {
        user_id: integration.user_id,
        service: integration.service,
        type: 'full'
      })
    }
  })

  // Incremental sync: Every 15 minutes
  cron.schedule('*/15 * * * *', async () => {
    const integrations = await db.integrations.findActive()

    for (const integration of integrations) {
      await queue.add('sync', {
        user_id: integration.user_id,
        service: integration.service,
        type: 'incremental'
      })
    }
  })
}

// Process sync job
async function processSyncJob(job: Job<SyncJob>) {
  const { user_id, service, type } = job.data

  const sync = getSyncStrategy(service)

  if (type === 'full') {
    await sync.fullSync()
  } else {
    const lastSync = await db.syncLog.getLastSync(user_id, service)
    await sync.incrementalSync(lastSync.completed_at)
  }

  await db.syncLog.create({
    user_id,
    service,
    type,
    completed_at: new Date()
  })
}
```

## Common Integration Patterns

### Slack Integration

```typescript
class SlackIntegration {
  async postMessage(channel: string, text: string, attachments?: any[]) {
    const accessToken = await getValidAccessToken(userId, 'slack')

    return await retryWithBackoff(() =>
      fetch('https://slack.com/api/chat.postMessage', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          channel,
          text,
          attachments
        })
      })
    )
  }

  async getChannels() {
    const accessToken = await getValidAccessToken(userId, 'slack')

    const response = await fetch('https://slack.com/api/conversations.list', {
      headers: { Authorization: `Bearer ${accessToken}` }
    })

    const data = await response.json()

    if (!data.ok) {
      throw new Error(`Slack API error: ${data.error}`)
    }

    return data.channels
  }
}
```

### Stripe Integration

```typescript
class StripeIntegration {
  async createSubscription(customerId: string, priceId: string) {
    try {
      const subscription = await stripe.subscriptions.create({
        customer: customerId,
        items: [{ price: priceId }],
        payment_behavior: 'default_incomplete',
        expand: ['latest_invoice.payment_intent'],
        metadata: {
          user_id: userId,
          plan: 'pro'
        }
      })

      return {
        subscription_id: subscription.id,
        client_secret: subscription.latest_invoice.payment_intent.client_secret
      }
    } catch (error) {
      if (error instanceof Stripe.errors.StripeError) {
        // Handle specific Stripe errors
        if (error.type === 'card_error') {
          throw new Error('Card was declined')
        }
      }
      throw error
    }
  }

  async cancelSubscription(subscriptionId: string) {
    // Cancel at period end (don't refund)
    await stripe.subscriptions.update(subscriptionId, {
      cancel_at_period_end: true
    })
  }
}
```

### Gmail/Google Calendar Integration

```typescript
import { google } from 'googleapis'

class GoogleIntegration {
  async sendEmail(to: string, subject: string, body: string) {
    const auth = await this.getOAuth2Client()
    const gmail = google.gmail({ version: 'v1', auth })

    const message = [`To: ${to}`, `Subject: ${subject}`, '', body].join('\n')

    const encodedMessage = Buffer.from(message)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '')

    await gmail.users.messages.send({
      userId: 'me',
      requestBody: {
        raw: encodedMessage
      }
    })
  }

  async listCalendarEvents(calendarId: string, timeMin: Date, timeMax: Date) {
    const auth = await this.getOAuth2Client()
    const calendar = google.calendar({ version: 'v3', auth })

    const response = await calendar.events.list({
      calendarId,
      timeMin: timeMin.toISOString(),
      timeMax: timeMax.toISOString(),
      singleEvents: true,
      orderBy: 'startTime'
    })

    return response.data.items
  }
}
```

## Testing Integrations

### Mock External APIs

```typescript
// tests/mocks/stripe.ts
export class MockStripe {
  subscriptions = {
    create: jest.fn().mockResolvedValue({
      id: 'sub_123',
      status: 'active'
    }),

    cancel: jest.fn().mockResolvedValue({
      id: 'sub_123',
      status: 'canceled'
    })
  }
}

// tests/integration.test.ts
describe('Stripe Integration', () => {
  let stripeIntegration: StripeIntegration

  beforeEach(() => {
    stripe = new MockStripe()
    stripeIntegration = new StripeIntegration(stripe)
  })

  it('creates a subscription', async () => {
    const result = await stripeIntegration.createSubscription('cus_123', 'price_123')

    expect(result.subscription_id).toBe('sub_123')
    expect(stripe.subscriptions.create).toHaveBeenCalledWith({
      customer: 'cus_123',
      items: [{ price: 'price_123' }]
      // ...
    })
  })

  it('handles card errors gracefully', async () => {
    stripe.subscriptions.create.mockRejectedValue(
      new Stripe.errors.StripeCardError('Card declined')
    )

    await expect(stripeIntegration.createSubscription('cus_123', 'price_123')).rejects.toThrow(
      'Card was declined'
    )
  })
})
```

### Webhook Testing

```typescript
// Generate valid webhook signatures for testing
function generateTestWebhook(payload: any, secret: string) {
  const timestamp = Math.floor(Date.now() / 1000)
  const signature = crypto
    .createHmac('sha256', secret)
    .update(`${timestamp}.${JSON.stringify(payload)}`)
    .digest('hex')

  return {
    payload,
    headers: {
      'stripe-signature': `t=${timestamp},v1=${signature}`
    }
  }
}

describe('Webhook Handler', () => {
  it('processes valid webhook', async () => {
    const webhook = generateTestWebhook(
      {
        type: 'payment_intent.succeeded',
        data: {
          /* ... */
        }
      },
      STRIPE_WEBHOOK_SECRET
    )

    const response = await request(app)
      .post('/webhooks/stripe')
      .set(webhook.headers)
      .send(webhook.payload)

    expect(response.status).toBe(200)
    // Verify processing happened
  })

  it('rejects invalid signature', async () => {
    const response = await request(app)
      .post('/webhooks/stripe')
      .set({ 'stripe-signature': 'invalid' })
      .send({ type: 'payment_intent.succeeded' })

    expect(response.status).toBe(400)
  })
})
```

## Monitoring & Observability

### Integration Health Checks

```typescript
interface IntegrationHealth {
  service: string
  status: 'healthy' | 'degraded' | 'down'
  last_success: Date
  last_failure?: Date
  error_rate_24h: number
}

async function checkIntegrationHealth(service: string): Promise<IntegrationHealth> {
  const logs = await db.integrationLogs.findRecent(service, '24h')

  const total = logs.length
  const failures = logs.filter(l => l.status === 'failed').length
  const errorRate = failures / total

  let status: 'healthy' | 'degraded' | 'down'
  if (errorRate < 0.01) status = 'healthy'
  else if (errorRate < 0.1) status = 'degraded'
  else status = 'down'

  return {
    service,
    status,
    last_success: logs.find(l => l.status === 'success')?.timestamp,
    last_failure: logs.find(l => l.status === 'failed')?.timestamp,
    error_rate_24h: errorRate
  }
}
```

### Logging & Alerts

```typescript
// Log all API requests
async function logAPIRequest(
  service: string,
  endpoint: string,
  statusCode: number,
  duration: number,
  error?: Error
) {
  await db.apiLogs.create({
    service,
    endpoint,
    status_code: statusCode,
    duration_ms: duration,
    error: error?.message,
    timestamp: new Date()
  })

  // Alert on high error rates
  if (statusCode >= 500) {
    const recentErrors = await db.apiLogs.count({
      service,
      status_code: { $gte: 500 },
      timestamp: { $gte: new Date(Date.now() - 5 * 60 * 1000) } // Last 5 min
    })

    if (recentErrors > 10) {
      await sendAlert({
        title: `High error rate for ${service} integration`,
        message: `${recentErrors} errors in last 5 minutes`
      })
    }
  }
}
```

## User Experience

### Integration Status UI

```typescript
interface IntegrationStatus {
  connected: boolean
  last_sync: Date
  sync_in_progress: boolean
  error?: string
}

// Show integration status to user
<Card>
  <IntegrationIcon service="slack" />
  <div>
    <h3>Slack</h3>
    {status.connected ? (
      <>
        <Badge color="green">Connected</Badge>
        <p>Last synced {formatRelative(status.last_sync)}</p>
        {status.sync_in_progress && <Spinner />}
      </>
    ) : (
      <>
        <Badge color="red">Disconnected</Badge>
        {status.error && <p className="error">{status.error}</p>}
        <Button onClick={reconnect}>Reconnect</Button>
      </>
    )}
  </div>
  <Button variant="secondary" onClick={disconnect}>
    Disconnect
  </Button>
</Card>
```

## Quick Start Checklist

### Setting Up Your First Integration

- [ ] Choose integration type (OAuth vs API key)
- [ ] Register OAuth app (get client ID/secret)
- [ ] Implement authentication flow
- [ ] Store tokens securely (encrypted)
- [ ] Implement token refresh
- [ ] Add rate limiting
- [ ] Add error handling with retries
- [ ] Set up webhook endpoint (if available)
- [ ] Add webhook signature verification
- [ ] Implement idempotency for webhooks
- [ ] Add monitoring & logging
- [ ] Test thoroughly (including failures)

## Common Pitfalls

❌ **Storing tokens unencrypted**: Always encrypt access/refresh tokens
❌ **No token refresh**: Tokens expire, implement refresh flow
❌ **Synchronous webhook processing**: Process webhooks in background jobs
❌ **No idempotency**: Webhooks may be delivered multiple times
❌ **Ignoring rate limits**: Implement client-side rate limiting
❌ **Poor error messages**: Show helpful errors, not "API Error 500"
❌ **No retry logic**: APIs are unreliable, always retry with backoff
❌ **Missing signature verification**: Attackers can forge webhooks

## Summary

Great API integrations:

- ✅ Handle auth flows properly (OAuth, refresh tokens)
- ✅ Respect rate limits
- ✅ Retry transient failures with exponential backoff
- ✅ Verify webhook signatures
- ✅ Process webhooks idempotently
- ✅ Monitor health and error rates
- ✅ Show clear status to users
- ✅ Store credentials securely
