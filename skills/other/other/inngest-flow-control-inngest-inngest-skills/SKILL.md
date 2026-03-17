---
name: inngest-flow-control
description: Configure Inngest flow control for functions. Covers concurrency limits with keys, throttling, rate limiting, debounce, priority, singleton, and event batching.
---

# Inngest Flow Control

Master Inngest flow control mechanisms to manage resources, prevent overloading systems, and ensure application reliability. This skill covers all flow control options with prescriptive guidance on when and how to use each.

> **These skills are focused on TypeScript.** For Python or Go, refer to the [Inngest documentation](https://www.inngest.com/llms.txt) for language-specific guidance. Core concepts apply across all languages.

## Quick Decision Guide

- **"Limit how many run at once"** → Concurrency
- **"Spread runs over time"** → Throttling
- **"Block after N runs in a period"** → Rate Limiting
- **"Wait for activity to stop, then run once"** → Debounce
- **"Only one run at a time for this key"** → Singleton
- **"Process events in groups"** → Batching
- **"Some runs are more important"** → Priority

## Concurrency

**When to use:** Limit the number of executing steps (not function runs) to manage computing resources and prevent system overwhelm.

**Key insight:** Concurrency limits active code execution, not function runs. A function waiting on `step.sleep()` or `step.waitForEvent()` doesn't count against the limit.

### Basic Concurrency

```typescript
inngest.createFunction(
  {
    id: "process-images",
    concurrency: 5
  },
  { event: "media/image.uploaded" },
  async ({ event, step }) => {
    // Only 5 steps can execute simultaneously
    await step.run("resize", () => resizeImage(event.data.imageUrl));
  }
);
```

### Concurrency with Keys (Multi-tenant)

Use `key` parameter to apply limit per unique value of the key.

```typescript
inngest.createFunction(
  {
    id: "user-sync",
    concurrency: [
      {
        key: "event.data.user_id",
        limit: 1
      }
    ]
  },
  { event: "user/profile.updated" },
  async ({ event, step }) => {
    // Only 1 step per user can execute at once
    // Prevents race conditions in user-specific operations
  }
);
```

### Account-level Shared Limits

```typescript
inngest.createFunction(
  {
    id: "ai-summary",
    concurrency: [
      {
        scope: "account",
        key: `"openai"`,
        limit: 60
      }
    ]
  },
  { event: "ai/summary.requested" },
  async ({ event, step }) => {
    // Share 60 concurrent OpenAI calls across all functions
  }
);
```

**When to use each:**

- Basic: Protect databases or limit general capacity
- Keyed: Multi-tenant fairness, prevent "noisy neighbor" issues
- Account-level: Share quotas across multiple functions (API limits)

## Throttling

**When to use:** Control the rate of function starts over time to work around API rate limits or smooth traffic spikes.

**Key difference from concurrency:** Throttling limits function run starts; concurrency limits step execution.

```typescript
inngest.createFunction(
  {
    id: "sync-crm-data",
    throttle: {
      limit: 10, // 10 function starts
      period: "60s", // per minute
      burst: 5, // plus 5 immediate bursts
      key: "event.data.customer_id" // per customer
    }
  },
  { event: "crm/contact.updated" },
  async ({ event, step }) => {
    // Respects CRM API rate limits: 10 calls/min per customer
    await step.run("sync", () => crmApi.updateContact(event.data));
  }
);
```

**Configuration:**

- `limit`: Functions that can start per period
- `period`: Time window (1s to 7d)
- `burst`: Extra immediate starts allowed
- `key`: Apply limits per unique key value

## Rate Limiting

**When to use:** Hard limit to prevent abuse or skip excessive duplicate events.

**Key difference from throttling:** Rate limiting discards events; throttling delays them.

```typescript
inngest.createFunction(
  {
    id: "webhook-processor",
    rateLimit: {
      limit: 1,
      period: "4h",
      key: "event.data.webhook_id"
    }
  },
  { event: "webhook/data.received" },
  async ({ event, step }) => {
    // Process each webhook only once per 4 hours
    // Prevents duplicate webhook spam
  }
);
```

**Use cases:**

- Prevent webhook duplicates
- Limit expensive operations per user
- Protection against abuse

## Debounce

**When to use:** Wait for a series of events to stop arriving before processing the latest one.

```typescript
inngest.createFunction(
  {
    id: "save-document",
    debounce: {
      period: "5m", // Wait 5min after last edit
      key: "event.data.document_id",
      timeout: "30m" // Force save after 30min max
    }
  },
  { event: "document/content.changed" },
  async ({ event, step }) => {
    // Saves document only after user stops editing
    // Uses the LAST event received
    await step.run("save", () => saveDocument(event.data));
  }
);
```

**Perfect for:**

- User input that changes rapidly (search, document editing)
- Noisy webhook events
- Ensuring latest data is processed

## Priority

**When to use:** Execute some function runs ahead of others based on dynamic data.

```typescript
inngest.createFunction(
  {
    id: "process-order",
    priority: {
      // VIP users get priority up to 120 seconds ahead
      run: "event.data.user_tier == 'vip' ? 120 : 0"
    }
  },
  { event: "order/placed" },
  async ({ event, step }) => {
    // VIP orders jump ahead in the queue
  }
);
```

**Advanced example:**

```typescript
inngest.createFunction(
  {
    id: "support-ticket",
    priority: {
      run: `
        event.data.severity == 'critical' ? 300 :
        event.data.severity == 'high' ? 120 :
        event.data.user_plan == 'enterprise' ? 60 : 0
      `
    }
  },
  { event: "support/ticket.created" },
  async ({ event, step }) => {
    // Critical tickets get highest priority (300s ahead)
    // High severity: 120s ahead
    // Enterprise users: 60s ahead
    // Everyone else: normal priority
  }
);
```

## Singleton

**When to use:** Ensure only one instance of a function runs at a time.

### Skip Mode (Preserve Current Run)

```typescript
inngest.createFunction(
  {
    id: "data-backup",
    singleton: {
      key: "event.data.database_id",
      mode: "skip"
    }
  },
  { event: "backup/requested" },
  async ({ event, step }) => {
    // Skip new backups if one is already running for this database
    await step.run("backup", () => performBackup(event.data.database_id));
  }
);
```

### Cancel Mode (Use Latest Event)

```typescript
inngest.createFunction(
  {
    id: "realtime-sync",
    singleton: {
      key: "event.data.user_id",
      mode: "cancel"
    }
  },
  { event: "user/data.changed" },
  async ({ event, step }) => {
    // Cancel previous sync and start with latest data
    await step.run("sync", () => syncUserData(event.data));
  }
);
```

## Batching

**When to use:** Process multiple events together for efficiency.

```typescript
inngest.createFunction(
  {
    id: "bulk-email-send",
    batchEvents: {
      maxSize: 100, // Up to 100 events
      timeout: "30s", // Or 30 seconds, whichever first
      // `key` groups events into separate batches per unique value
      // This is different from expressions `if` which filters events
      key: "event.data.campaign_id" // Batch per campaign
    }
  },
  { event: "email/send.queued" },
  async ({ events, step }) => {
    // Process array of events together
    const emails = events.map((evt) => ({
      to: evt.data.email,
      subject: evt.data.subject,
      body: evt.data.body
    }));

    await step.run("send-batch", () => emailService.sendBulk(emails));
  }
);
```

## Combining Flow Control

### Example: Fair AI Processing

```typescript
inngest.createFunction(
  {
    id: "ai-image-processing",
    // Global throttling for API limits
    throttle: {
      limit: 50,
      period: "60s",
      key: `"gpu-cluster"`
    },
    // Per-user concurrency for fairness
    concurrency: [
      {
        key: "event.data.user_id",
        limit: 3
      }
    ],
    // VIP users get priority
    priority: {
      run: "event.data.plan == 'pro' ? 60 : 0"
    }
  },
  { event: "ai/image.generate" },
  async ({ event, step }) => {
    // Combines multiple flow controls for optimal resource usage
  }
);
```

**Pro tip:** Most production functions benefit from combining 1-3 flow control mechanisms for optimal reliability and performance.
