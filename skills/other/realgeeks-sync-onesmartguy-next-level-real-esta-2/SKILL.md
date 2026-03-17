---
name: realgeeks-sync
description: Bi-directional synchronization between RealGeeks CRM and conversational AI systems. Use when implementing webhook handlers, creating sync pipelines, handling lead deduplication, mapping activity data, or building real-time CRM integration workflows. Includes webhook security, retry logic, and data transformation patterns.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# RealGeeks Sync Skill

Expert guidance for implementing bi-directional synchronization between **RealGeeks CRM** and **Next Level Real Estate** AI calling platform. This skill provides patterns, best practices, and implementation strategies for seamless CRM integration.

## When to Use This Skill

Invoke this skill when you need to:
- ✅ Implement RealGeeks webhook handlers
- ✅ Design lead sync workflows
- ✅ Handle lead deduplication
- ✅ Map activities between systems
- ✅ Build real-time CRM integration
- ✅ Configure webhook security (HMAC)
- ✅ Implement retry and error handling
- ✅ Transform data between formats

## Sync Architecture Patterns

### Pattern 1: Event-Driven Sync (Recommended)

**Use When**: Real-time updates needed, leads must flow immediately

```
RealGeeks → Webhook → Your App → Process → ElevenLabs
    ↓
  Kafka/Queue
    ↓
  Workers
```

**Benefits**:
- Instant lead processing (<5 minutes)
- Scalable (queue handles bursts)
- Reliable (retry failed webhooks)
- Audit trail (all events logged)

**Implementation**:
```typescript
// Webhook receiver
app.post('/webhooks/realgeeks', async (req, res) => {
  try {
    // 1. Validate signature immediately
    const signature = req.headers['x-lead-router-signature']
    if (!validateSignature(req.rawBody, signature, SECRET)) {
      return res.status(401).json({ error: 'Invalid signature' })
    }

    // 2. Return 200 OK quickly
    res.status(200).json({ received: true })

    // 3. Process asynchronously
    const action = req.headers['x-lead-router-action']
    const messageId = req.headers['x-lead-router-message-id']

    await queue.publish('realgeeks.webhooks', {
      action,
      messageId,
      payload: req.body,
      receivedAt: new Date()
    })

  } catch (error) {
    console.error('Webhook error:', error)
    res.status(500).json({ error: 'Internal error' })
  }
})

// Worker processing
queue.subscribe('realgeeks.webhooks', async (message) => {
  const { action, messageId, payload } = message

  // Check if already processed (idempotency)
  if (await isProcessed(messageId)) {
    console.log(`Message ${messageId} already processed`)
    return
  }

  switch (action) {
    case 'created':
      await handleLeadCreated(payload)
      break
    case 'updated':
      await handleLeadUpdated(payload)
      break
    case 'activity_added':
      await handleActivityAdded(payload)
      break
  }

  // Mark as processed
  await markProcessed(messageId)
})
```

### Pattern 2: Batch Sync

**Use When**: Historical data import, nightly reconciliation

```
Cron Job → Fetch from RealGeeks → Transform → Load to DB
```

**Implementation**:
```typescript
// Nightly sync job
async function syncLeadsFromRealGeeks() {
  const leads = await fetchAllLeads(siteUuid)

  for (const lead of leads) {
    // Check if exists in our system
    const existing = await database.leads.findByEmail(lead.email)

    if (existing) {
      // Update if changed
      if (hasChanged(existing, lead)) {
        await database.leads.update(existing.id, transformLead(lead))
      }
    } else {
      // Create new
      await database.leads.insert(transformLead(lead))
    }
  }
}

// Run daily at 2 AM
cron.schedule('0 2 * * *', syncLeadsFromRealGeeks)
```

## Webhook Security Implementation

### HMAC-SHA256 Signature Validation

**Critical**: Always validate webhook signatures to prevent spoofing

```typescript
import crypto from 'crypto'

function validateWebhookSignature(
  body: string | Buffer,
  signature: string,
  secret: string
): boolean {
  try {
    // Ensure body is string
    const bodyString = typeof body === 'string' ? body : body.toString()

    // Create HMAC with SHA256
    const hmac = crypto.createHmac('sha256', secret)
    hmac.update(bodyString)
    const calculatedSignature = hmac.digest('hex')

    // Constant-time comparison (prevents timing attacks)
    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(calculatedSignature)
    )
  } catch (error) {
    console.error('Signature validation error:', error)
    return false
  }
}

// Usage in Express
app.use('/webhooks/realgeeks', express.raw({ type: 'application/json' }))

app.post('/webhooks/realgeeks', (req, res) => {
  const signature = req.headers['x-lead-router-signature']

  if (!validateWebhookSignature(req.body, signature, process.env.WEBHOOK_SECRET)) {
    return res.status(401).json({ error: 'Invalid signature' })
  }

  // Signature valid, process webhook
  // ...
})
```

### Webhook Headers Reference

```typescript
interface RealGeeksWebhookHeaders {
  'x-lead-router-action': 'created' | 'updated' | 'activity_added' | 'user_updated'
  'x-lead-router-message-id': string  // Unique per message
  'x-lead-router-signature': string   // HMAC-SHA256 hex
  'user-agent': 'RealGeeks-LeadRouter/1.0'
}
```

## Lead Deduplication Strategies

### Strategy 1: Email-Based Deduplication

**Assumption**: Email is most reliable unique identifier

```typescript
async function findOrCreateLead(leadData: any) {
  // 1. Try email first
  if (leadData.email) {
    const existing = await database.leads.findByEmail(leadData.email)
    if (existing) {
      console.log(`Lead found by email: ${existing.id}`)
      return { lead: existing, created: false }
    }
  }

  // 2. Try phone if no email match
  if (leadData.phone) {
    const existing = await database.leads.findByPhone(normalizePhone(leadData.phone))
    if (existing) {
      console.log(`Lead found by phone: ${existing.id}`)
      return { lead: existing, created: false }
    }
  }

  // 3. Try name + address
  if (leadData.first_name && leadData.last_name && leadData.address) {
    const existing = await database.leads.findByNameAddress(
      leadData.first_name,
      leadData.last_name,
      leadData.address
    )
    if (existing) {
      console.log(`Lead found by name+address: ${existing.id}`)
      return { lead: existing, created: false }
    }
  }

  // 4. No match, create new
  const newLead = await database.leads.create(leadData)
  console.log(`New lead created: ${newLead.id}`)
  return { lead: newLead, created: true }
}
```

### Strategy 2: Fuzzy Matching

**Use When**: Dealing with typos, formatting differences

```typescript
import { levenshtein } from 'fast-levenshtein'

function isFuzzyMatch(str1: string, str2: string, threshold = 0.8): boolean {
  const distance = levenshtein.get(str1.toLowerCase(), str2.toLowerCase())
  const maxLen = Math.max(str1.length, str2.length)
  const similarity = 1 - (distance / maxLen)
  return similarity >= threshold
}

async function findLeadFuzzy(leadData: any) {
  const candidates = await database.leads.search({
    first_name: leadData.first_name,
    last_name: leadData.last_name
  })

  for (const candidate of candidates) {
    // Check email similarity
    if (leadData.email && candidate.email) {
      if (isFuzzyMatch(leadData.email, candidate.email, 0.9)) {
        return candidate
      }
    }

    // Check phone similarity (after normalization)
    if (leadData.phone && candidate.phone) {
      const phone1 = normalizePhone(leadData.phone)
      const phone2 = normalizePhone(candidate.phone)
      if (phone1 === phone2) {
        return candidate
      }
    }
  }

  return null
}
```

## Activity Mapping

### ElevenLabs → RealGeeks Activity Mapping

```typescript
function mapToRealGeeksActivity(elevenlabsEvent: any) {
  const activityMap = {
    'call_initiated': {
      type: 'called',
      description: (e) => `AI call initiated to ${e.phone}`,
    },
    'call_completed': {
      type: 'called',
      description: (e) => `AI call completed. Duration: ${e.duration}s. Sentiment: ${e.sentiment}. ${e.summary}`,
    },
    'call_failed': {
      type: 'note',
      description: (e) => `AI call failed: ${e.error}`,
    },
    'voicemail_left': {
      type: 'note',
      description: (e) => `Voicemail left: ${e.message}`,
    },
    'opt_out_requested': {
      type: 'opted_out',
      description: (e) => `Lead requested opt-out during AI call`,
    },
    'viewing_scheduled': {
      type: 'tour_requested',
      description: (e) => `Property viewing scheduled for ${e.date}`,
    },
  }

  const mapping = activityMap[elevenlabsEvent.type]
  if (!mapping) {
    console.warn(`Unknown event type: ${elevenlabsEvent.type}`)
    return null
  }

  return {
    type: mapping.type,
    source: 'ElevenLabs AI',
    description: mapping.description(elevenlabsEvent),
    created: elevenlabsEvent.timestamp
  }
}

// Usage
async function logCallToRealGeeks(call: ElevenLabsCall) {
  const activity = mapToRealGeeksActivity({
    type: 'call_completed',
    phone: call.to,
    duration: call.duration,
    sentiment: call.sentiment,
    summary: call.transcript_summary
  })

  if (activity) {
    await clients.realgeeks.addActivities(
      siteUuid,
      call.leadId,
      [activity]
    )
  }
}
```

### RealGeeks → ElevenLabs Context Mapping

```typescript
function prepareElevenLabsContext(realgeeksLead: any) {
  return {
    leadData: {
      name: `${realgeeksLead.first_name} ${realgeeksLead.last_name}`,
      email: realgeeksLead.email,
      phone: realgeeksLead.phone,
      urgency: realgeeksLead.urgency,
      timeline: realgeeksLead.timeframe,
      role: realgeeksLead.role,
      source: realgeeksLead.source,
    },
    propertyInterests: realgeeksLead.activities
      ?.filter(a => a.type === 'property_viewed')
      .map(a => ({
        address: a.property?.address,
        price: a.property?.list_price,
        beds: a.property?.beds,
        baths: a.property?.baths,
      })) || [],
    previousInteractions: realgeeksLead.activities
      ?.filter(a => ['called', 'contact_emailed'].includes(a.type))
      .map(a => ({
        type: a.type,
        date: a.created,
        description: a.description,
      })) || [],
    strategyRules: {
      isHotLead: realgeeksLead.urgency === 'Hot',
      isBuyer: realgeeksLead.role?.includes('Buyer'),
      isSeller: realgeeksLead.role?.includes('Seller'),
      hasViewed Properties: realgeeksLead.activities?.some(a => a.type === 'property_viewed'),
    },
  }
}
```

## Retry and Error Handling

### Webhook Retry Strategy

RealGeeks retries failed webhooks:
- 1st retry: 10 minutes
- 2nd retry: 30 minutes
- 3rd retry: 1 hour
- 4th-8th retry: 2-4 hours

**Your Implementation**:

```typescript
// Track processed messages for idempotency
const processedMessages = new Set()

app.post('/webhooks/realgeeks', async (req, res) => {
  const messageId = req.headers['x-lead-router-message-id']

  // Idempotency check
  if (processedMessages.has(messageId)) {
    console.log(`Message ${messageId} already processed`)
    return res.status(200).json({ status: 'already_processed' })
  }

  try {
    await processWebhook(req.body)

    // Mark as processed
    processedMessages.add(messageId)

    res.status(200).json({ status: 'success' })

  } catch (error) {
    console.error('Webhook processing error:', error)

    // Permanent failure - stop retries
    if (error.code === 'PERMANENT_FAILURE') {
      return res.status(406).json({ error: 'Permanent failure' })
    }

    // Temporary failure - allow retries
    res.status(500).json({ error: 'Temporary failure' })
  }
})

// Clean up old message IDs (after 24 hours)
setInterval(() => {
  const cutoff = Date.now() - (24 * 60 * 60 * 1000)
  // Implement cleanup logic
}, 3600000)  // Every hour
```

### API Retry with Exponential Backoff

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn()
    } catch (error) {
      if (attempt === maxRetries) {
        throw error
      }

      // Exponential backoff: 1s, 2s, 4s, 8s...
      const delay = baseDelay * Math.pow(2, attempt - 1)
      console.log(`Retry attempt ${attempt} after ${delay}ms`)

      await sleep(delay)
    }
  }

  throw new Error('Max retries exceeded')
}

// Usage
await retryWithBackoff(async () => {
  return await clients.realgeeks.createLead(siteUuid, leadData)
}, 3, 1000)
```

## Data Transformation

### Phone Number Normalization

```typescript
function normalizePhone(phone: string): string {
  // Remove all non-digit characters
  const digits = phone.replace(/\D/g, '')

  // US/Canada number (10 digits)
  if (digits.length === 10) {
    return `+1${digits}`
  }

  // Already has country code
  if (digits.length === 11 && digits[0] === '1') {
    return `+${digits}`
  }

  // International
  if (digits.length > 11) {
    return `+${digits}`
  }

  // Invalid
  console.warn(`Invalid phone number: ${phone}`)
  return phone
}

// Comparison
function phonesMatch(phone1: string, phone2: string): boolean {
  return normalizePhone(phone1) === normalizePhone(phone2)
}
```

### Date/Time Handling

```typescript
// RealGeeks uses ISO 8601
function formatDateForRealGeeks(date: Date): string {
  return date.toISOString()
}

// Parse RealGeeks date
function parseRealGeeksDate(dateString: string): Date {
  return new Date(dateString)
}

// Compare dates
function isRecent(dateString: string, hoursAgo: number): boolean {
  const date = parseRealGeeksDate(dateString)
  const cutoff = Date.now() - (hoursAgo * 60 * 60 * 1000)
  return date.getTime() > cutoff
}
```

## Monitoring and Observability

### Key Metrics to Track

```typescript
interface SyncMetrics {
  // Webhook metrics
  webhooksReceived: number
  webhooksProcessed: number
  webhooksFailed: number
  signatureValidationFailures: number

  // Lead metrics
  leadsCreated: number
  leadsUpdated: number
  leadsDuplicate: number

  // Activity metrics
  activitiesLogged: number
  activitiesFailed: number

  // Performance
  avgWebhookProcessingTime: number
  avgAPIResponseTime: number

  // Sync lag
  oldestUnprocessedWebhook: number  // milliseconds
}

// Prometheus-style metrics
const metrics = {
  webhooksReceived: new Counter('realgeeks_webhooks_received_total'),
  webhookProcessingTime: new Histogram('realgeeks_webhook_processing_seconds'),
  apiRequestDuration: new Histogram('realgeeks_api_request_duration_seconds'),
  syncErrors: new Counter('realgeeks_sync_errors_total', ['error_type']),
}

// Usage
app.post('/webhooks/realgeeks', async (req, res) => {
  const start = Date.now()
  metrics.webhooksReceived.inc()

  try {
    await processWebhook(req.body)

    const duration = (Date.now() - start) / 1000
    metrics.webhookProcessingTime.observe(duration)

    res.status(200).json({ success: true })
  } catch (error) {
    metrics.syncErrors.inc({ error_type: error.code })
    res.status(500).json({ error: error.message })
  }
})
```

### Health Check Endpoint

```typescript
app.get('/health/realgeeks', async (req, res) => {
  const health = {
    status: 'healthy',
    checks: {
      apiConnectivity: false,
      recentWebhooks: false,
      syncLag: 0,
    },
    timestamp: new Date().toISOString(),
  }

  try {
    // Test API
    await clients.realgeeks.listUsers(siteUuid)
    health.checks.apiConnectivity = true
  } catch (error) {
    health.status = 'unhealthy'
    console.error('API health check failed:', error)
  }

  // Check recent webhook activity
  const lastWebhook = await getLastWebhookTimestamp()
  if (lastWebhook && Date.now() - lastWebhook < 3600000) {
    health.checks.recentWebhooks = true
  }

  // Calculate sync lag
  health.checks.syncLag = await calculateSyncLag()

  if (health.checks.syncLag > 300000) {  // 5 minutes
    health.status = 'degraded'
  }

  res.status(health.status === 'healthy' ? 200 : 503).json(health)
})
```

## Testing Strategies

### Webhook Testing with Ngrok

```bash
# 1. Start your local server
npm run dev

# 2. Expose with ngrok
ngrok http 3000

# 3. Configure RealGeeks webhook URL
# Use the ngrok URL: https://abc123.ngrok.io/webhooks/realgeeks

# 4. Trigger test webhook from RealGeeks
# Or use curl to simulate:
curl -X POST https://localhost:3000/webhooks/realgeeks \
  -H "Content-Type: application/json" \
  -H "X-Lead-Router-Action: created" \
  -H "X-Lead-Router-Message-Id: test-123" \
  -H "X-Lead-Router-Signature: $(echo -n '{"test":"data"}' | openssl dgst -sha256 -hmac 'your_secret' | cut -d' ' -f2)" \
  -d '{"test":"data"}'
```

### Unit Testing

```typescript
import { describe, it, expect, vi } from 'vitest'

describe('RealGeeks Sync', () => {
  it('should validate webhook signature', () => {
    const body = JSON.stringify({ test: 'data' })
    const secret = 'test_secret'
    const validSignature = createHmacSignature(body, secret)

    expect(validateWebhookSignature(body, validSignature, secret)).toBe(true)
    expect(validateWebhookSignature(body, 'invalid', secret)).toBe(false)
  })

  it('should deduplicate leads by email', async () => {
    const lead1 = { email: 'test@example.com', first_name: 'John' }
    const lead2 = { email: 'test@example.com', first_name: 'Johnny' }

    const result1 = await findOrCreateLead(lead1)
    const result2 = await findOrCreateLead(lead2)

    expect(result1.created).toBe(true)
    expect(result2.created).toBe(false)
    expect(result1.lead.id).toBe(result2.lead.id)
  })

  it('should map ElevenLabs events to RealGeeks activities', () => {
    const callEvent = {
      type: 'call_completed',
      duration: 180,
      sentiment: 'positive',
      summary: 'Lead qualified'
    }

    const activity = mapToRealGeeksActivity(callEvent)

    expect(activity.type).toBe('called')
    expect(activity.source).toBe('ElevenLabs AI')
    expect(activity.description).toContain('180s')
    expect(activity.description).toContain('positive')
  })
})
```

## Best Practices Checklist

### Security
- [ ] Always validate HMAC signatures
- [ ] Use HTTPS for webhook endpoints
- [ ] Rotate webhook secrets regularly
- [ ] Log all webhook attempts
- [ ] Rate limit webhook endpoint

### Reliability
- [ ] Implement idempotency (check message_id)
- [ ] Return 200 OK within 30 seconds
- [ ] Process webhooks asynchronously
- [ ] Use queue for high volume
- [ ] Implement retry with exponential backoff
- [ ] Handle API rate limits

### Data Integrity
- [ ] Deduplicate leads before creating
- [ ] Normalize phone numbers
- [ ] Validate required fields
- [ ] Handle partial data gracefully
- [ ] Maintain audit trail
- [ ] Sync activities bidirectionally

### Monitoring
- [ ] Track webhook receipt and processing
- [ ] Monitor sync lag
- [ ] Alert on high error rates
- [ ] Log all API calls
- [ ] Dashboard for key metrics
- [ ] Health check endpoint

## Troubleshooting Guide

| Issue | Symptom | Solution |
|-------|---------|----------|
| Webhooks not received | No incoming data | Check webhook URL registration in RealGeeks |
| Signature validation fails | 401 errors | Verify webhook secret matches |
| Duplicate leads created | Same lead multiple times | Implement deduplication logic |
| Activities not appearing | Missing call logs | Check activity type and format |
| Sync lag increasing | Old webhooks unprocessed | Scale workers, check for bottlenecks |
| API rate limit hit | 429 errors | Implement request throttling |

## Resources

- [RealGeeks Incoming API](https://developers.realgeeks.com/incoming-leads-api/)
- [RealGeeks Outgoing API](https://developers.realgeeks.com/outgoing-leads-api/)
- [Activities Reference](https://developers.realgeeks.com/activities/)
- [HMAC Security](https://en.wikipedia.org/wiki/HMAC)

---

**Remember:** Robust sync is critical for lead response time. Prioritize reliability, security, and observability in your implementation.
