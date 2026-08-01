---
name: data-orchestration
description: '> Purpose: Build multi-system integrations, ETL workflows, and API connections.
  Design Make/n8n scenarios, implement webhooks, and create event-driven data pipelines.'
---

# Data Orchestration & API Integration Skill

> **Purpose:** Build multi-system integrations, ETL workflows, and API connections. Design Make/n8n scenarios, implement webhooks, and create event-driven data pipelines.

## When to Use This Skill

Use this skill when:
- Building multi-system integrations (Clay → HubSpot → Slack)
- Designing Make or n8n automation scenarios
- Implementing REST API connections
- Creating webhook handlers
- Building ETL pipelines
- Setting up monitoring and error handling

---

## Integration Architecture

### Clay → HubSpot Pattern

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Clay     │────▶│  Webhook    │────▶│  HubSpot    │
│   (table)   │     │  (Make/n8n) │     │   (CRM)     │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │              Transform           Create/Update
       │              Validate            Associate
       └──────────────────────────────────────┘
                    Error Handling
```

### Multi-System Orchestration

```
Event Source (Clay, HubSpot, Webhook)
              ↓
        ┌─────────────┐
        │  Orchestrator│ (Make/n8n)
        │             │
        ├─── Route ───┤
        │             │
        ▼             ▼
   ┌─────────┐   ┌─────────┐
   │ System A│   │ System B│
   │(HubSpot)│   │ (Slack) │
   └─────────┘   └─────────┘
        │             │
        └─────────────┘
              ↓
         Log & Monitor
```

---

## Make Scenario Patterns

### Basic Webhook Handler

```
[Webhook] → [JSON Parse] → [Router]
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
              [HubSpot]   [Slack]   [Airtable]
              [Update]    [Post]    [Create]
```

### Error Handling Pattern

```
[Trigger]
    │
    ▼
[Try Action]
    │
    ├── Success ──▶ [Continue Flow]
    │
    └── Error ────▶ [Error Handler]
                         │
                    ┌────┴────┐
                    ▼         ▼
              [Log Error] [Alert Slack]
                    │
                    ▼
              [Retry or Skip]
```

### Rate Limit Pattern

```
[Trigger: Batch of Records]
         │
         ▼
[Iterator: Process One at a Time]
         │
         ▼
[API Call]
         │
         ▼
[Sleep: 200ms] ←── Avoid rate limits
         │
         ▼
[Next Record]
```

---

## API Integration Best Practices

### REST API Call Pattern

```javascript
// Headers
{
  "Authorization": "Bearer {api_key}",
  "Content-Type": "application/json"
}

// Request with retry logic
async function callAPI(url, payload, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(payload)
      });

      if (response.status === 429) {
        // Rate limited - wait and retry
        await sleep(Math.pow(2, i) * 1000);
        continue;
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
    }
  }
}
```

### Authentication Patterns

| Type | Use Case | Implementation |
|------|----------|----------------|
| **API Key** | Simple integrations | Header: `Authorization: Bearer {key}` |
| **OAuth 2.0** | User context needed | Token refresh workflow |
| **Basic Auth** | Legacy systems | Header: `Authorization: Basic {base64}` |

---

## Webhook Implementation

### Webhook Receiver Setup

```
POST /webhook/clay-enrichment

Headers:
  Content-Type: application/json
  X-Webhook-Secret: {validation_token}

Body:
{
  "event": "row_updated",
  "table_id": "...",
  "row_data": {
    "company_name": "...",
    "enrichment_data": {...}
  }
}
```

### Validation Checklist

- [ ] Verify webhook signature/secret
- [ ] Validate required fields present
- [ ] Check data types match expected
- [ ] Log raw payload for debugging
- [ ] Return 200 quickly, process async

---

## ETL Patterns

### Extract → Transform → Load

```
EXTRACT                TRANSFORM              LOAD
─────────────────────────────────────────────────────
API Pull      →    Clean/Normalize    →    Database
CSV Import    →    Enrich/Join        →    CRM
Webhook       →    Calculate Fields   →    Data Warehouse
Scrape        →    Validate/Filter    →    Analytics
```

### Data Transformation

| Operation | Example |
|-----------|---------|
| **Normalize** | `ACME, Inc.` → `acme` (domain) |
| **Enrich** | Add firmographic data from API |
| **Calculate** | `signal_score = (intent * 0.4) + (fit * 0.6)` |
| **Filter** | Remove rows with invalid email |
| **Deduplicate** | Match on domain, keep most recent |

---

## Monitoring & Observability

### What to Monitor

| Metric | Alert Threshold |
|--------|-----------------|
| **Workflow errors** | > 5% failure rate |
| **API latency** | > 2s average |
| **Queue depth** | > 1000 pending |
| **Rate limit hits** | > 10/hour |

### Logging Pattern

```json
{
  "timestamp": "2025-01-04T12:00:00Z",
  "workflow": "clay_to_hubspot",
  "event": "record_processed",
  "record_id": "abc123",
  "status": "success",
  "duration_ms": 450,
  "metadata": {
    "source": "clay",
    "destination": "hubspot",
    "action": "update"
  }
}
```

---

## Common Integration Recipes

### Clay Enrichment → HubSpot + Slack

```
1. Clay table row updated (webhook)
2. Parse enrichment data
3. Lookup company in HubSpot by domain
4. IF exists:
   - Update properties
   - IF signal_score > 80:
     - Notify Slack #high-intent
5. ELSE:
   - Create company
   - Create associated contact
6. Log success/failure
```

### Multi-Touch Attribution

```
1. HubSpot form submission (trigger)
2. Fetch all previous touchpoints for contact
3. Apply attribution model:
   - First touch: 40%
   - Last touch: 40%
   - Middle touches: 20% split
4. Update contact properties
5. Aggregate to campaign performance
6. Push to data warehouse
```

---

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| **Webhook not received** | Check URL, firewall | Verify endpoint accessible |
| **Data not syncing** | Check field mapping | Log raw payload, verify transform |
| **Rate limited** | Too many calls | Add delays, batch requests |
| **Duplicate records** | Missing dedup logic | Add lookup before create |
| **Stale data** | Caching issue | Check cache TTL, force refresh |

---

## Security Considerations

1. **Never log sensitive data** (API keys, PII)
2. **Validate webhook signatures** before processing
3. **Use secrets management** (not hardcoded keys)
4. **Implement IP allowlisting** where possible
5. **Encrypt data in transit** (HTTPS only)
6. **Audit access logs** regularly
