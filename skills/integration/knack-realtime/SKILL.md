---
name: Knack Realtime
description: Simulates live updates between Knack backend and Vercel dashboards. Enables near-real-time synchronization of HTI operational data without constant...
allowed-tools: Read
---

# Knack Realtime

## Purpose
Simulates live updates between Knack backend and Vercel dashboards. Enables near-real-time synchronization of HTI operational data without constant polling.

## Core Concepts

Knack doesn't offer native WebSocket support, so we implement:
1. **Polling**: Periodic checks for data changes
2. **Webhooks**: Knack triggers external endpoints on record events
3. **Incremental Updates**: Fetch only changed records

## Core Functions

### poll_updates
**Purpose**: Check for data changes at regular intervals

**Parameters**:
- `object_key` (string, required): Knack object to monitor
- `interval_seconds` (integer, optional): Polling frequency (default: 60)
- `last_check_timestamp` (datetime, optional): Only fetch records modified since this time
- `on_change` (function, optional): Callback when changes detected

**Example**:
```javascript
// Poll for new laptops every 60 seconds
poll_updates({
  object_key: "object_1",
  interval_seconds: 60,
  last_check_timestamp: new Date(),
  on_change: (new_records) => {
    console.log(`${new_records.length} new laptops acquired`);
    updateDashboard(new_records);
  }
});
```

**Implementation**:
```javascript
async function poll_updates({ object_key, interval_seconds, on_change }) {
  let last_check = new Date();

  setInterval(async () => {
    const changes = await get_records(object_key, {
      filters: build_filter({
        rules: [{
          field: "field_modified_date",
          operator: "is after",
          value: last_check.toISOString()
        }]
      })
    });

    if (changes.records.length > 0) {
      on_change(changes.records);
    }

    last_check = new Date();
  }, interval_seconds * 1000);
}
```

### register_webhook
**Purpose**: Configure Knack to push updates to Vercel endpoint

**Parameters**:
- `trigger` (string, required): "record_created" | "record_updated" | "record_deleted"
- `object_key` (string, required): Which object to monitor
- `url` (string, required): Vercel API route to receive webhook
- `secret` (string, optional): Shared secret for webhook validation

**Knack Setup** (Manual in Knack Builder):
1. Navigate to Settings → API & Code → Webhooks
2. Create new webhook:
   - **Trigger**: After Record Create/Update/Delete
   - **Object**: Select target object (e.g., Laptop Inventory)
   - **URL**: `https://your-vercel-app.vercel.app/api/knack-webhook`
   - **Method**: POST

**Vercel API Route** (`/api/knack-webhook.js`):
```javascript
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { object_key, record, action } = req.body;

  // Validate webhook (optional)
  const signature = req.headers['x-knack-signature'];
  if (!validateSignature(signature, req.body)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // Process update
  if (action === 'created') {
    console.log(`New record in ${object_key}:`, record);
    await updateCache(object_key, record);
  }

  return res.status(200).json({ received: true });
}
```

### detect_changes
**Purpose**: Identify which records have changed since last sync

**Example**:
```javascript
const changed = await detect_changes({
  object_key: "object_1",
  since: last_sync_timestamp,
  fields_to_watch: ["field_status", "field_county"]
});
```

**Logic**:
- Query records modified after timestamp
- Compare field values to cached state
- Return only records with actual changes

## HTI-Specific Use Cases

### Dashboard Live Updates

#### Device Status Changes
```javascript
// Real-time status updates for ops dashboard
poll_updates({
  object_key: "object_1",
  interval_seconds: 30, // Check every 30 seconds
  on_change: (devices) => {
    const ready = devices.filter(d => d.status === "Ready for Donation");
    if (ready.length > 0) {
      notifyTeam(`${ready.length} new devices ready for distribution`);
    }
  }
});
```

#### Training Session Registrations
```javascript
// Monitor new sign-ups for digital literacy classes
poll_updates({
  object_key: "object_training",
  interval_seconds: 120, // Every 2 minutes
  on_change: (sessions) => {
    updateCapacityWidget(sessions);
  }
});
```

### Webhook-Driven Updates

#### New Donation Notification
```javascript
// Webhook fires when new donation record created
register_webhook({
  trigger: "record_created",
  object_key: "object_donations",
  url: "https://hubdash.vercel.app/api/donation-alert",
  on_receive: async (donation) => {
    await sendSlackNotification({
      channel: "#donations",
      text: `New donation: ${donation.org_name} - ${donation.laptop_count} laptops`
    });
  }
});
```

#### Status Change Workflow
```javascript
// When device status changes to "Ready", trigger distribution workflow
register_webhook({
  trigger: "record_updated",
  object_key: "object_1",
  url: "https://hubdash.vercel.app/api/device-ready",
  filter_condition: (record) => record.status === "Ready for Donation"
});
```

## Performance Optimization

### Smart Polling
```javascript
// Adaptive polling: slower when idle, faster when active
let poll_interval = 60; // Start at 60 seconds

poll_updates({
  object_key: "object_1",
  interval_seconds: poll_interval,
  on_change: (records) => {
    if (records.length > 10) {
      poll_interval = 15; // Speed up if lots of activity
    } else {
      poll_interval = Math.min(poll_interval + 15, 180); // Slow down if quiet
    }
  }
});
```

### Delta Sync
```javascript
// Only fetch modified fields, not entire records
const changes = await poll_updates({
  object_key: "object_1",
  fields: ["field_status", "field_county"], // Only these fields
  since: last_check
});
```

## Rate Limit Considerations

**Knack Limit**: 10 requests/second

**Polling Strategy**:
- Short interval (30s) = 2 requests/minute
- Medium interval (60s) = 1 request/minute
- Long interval (120s) = 0.5 requests/minute

**Best Practice**: Use webhooks for critical updates, polling for less urgent data

## Error Handling

```javascript
async function robust_poll(object_key) {
  try {
    const updates = await poll_updates({ object_key });
    return updates;
  } catch (error) {
    if (error.status === 429) {
      // Rate limit - increase interval
      console.warn("Rate limit hit, slowing polling...");
      await sleep(5000);
    } else if (error.status >= 500) {
      // Server error - retry with backoff
      await exponentialBackoff(poll_updates, { object_key });
    } else {
      throw error;
    }
  }
}
```

## Vercel Integration

### API Route Structure
```
/api
  /knack-webhook.js       # Receives Knack webhooks
  /poll-updates.js        # Serverless function for polling
  /cache-invalidate.js    # Clear cache on updates
```

### Environment Variables
```bash
KNACK_WEBHOOK_SECRET=your_secret_here
KNACK_APP_ID=your_app_id
KNACK_API_KEY=your_api_key
```

## Testing

### Webhook Testing
```bash
# Simulate Knack webhook locally
curl -X POST http://localhost:3000/api/knack-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "object_key": "object_1",
    "action": "created",
    "record": { "id": "test123", "status": "Ready" }
  }'
```

### Polling Simulation
```javascript
// Test polling logic without hitting Knack API
const mock_changes = [
  { id: "1", status: "Ready" },
  { id: "2", status: "Converted" }
];

on_change(mock_changes);
```

## Integration Points

- **knack_reader**: Fetch changed records
- **knack_filter_sort**: Filter for modified_since queries
- **knack_cache_optimizer**: Invalidate cache on updates
- **knack_dashboard_ai**: Trigger metric recalculation on changes
- **knack_reporting_sync**: Real-time progress toward goals

## Grant Compliance
- Log all webhook triggers for audit trail
- Track real-time progress toward 3,500 laptop goal
- Alert when approaching quarterly reporting deadlines
- Monitor training session capacity in real-time
