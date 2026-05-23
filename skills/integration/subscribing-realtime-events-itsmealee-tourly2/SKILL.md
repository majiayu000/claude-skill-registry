---
name: subscribing-realtime-events
description: Subscribes to Appwrite Realtime events for live updates. Use when building dashboards or live booking counters.
---

# Realtime Event Subscriptions

## When to use this skill
- Live notifications.
- Updating tour availability in real-time.
- Chat or support features.

## Workflow
- [ ] Identify the channel: `databases.[DB_ID].collections.[COLL_ID].documents`.
- [ ] Use `client.subscribe(channel, callback)`.
- [ ] Handle cleanup in `useEffect` return.

## Syntax (Verified via Context7)
```javascript
const unsubscribe = client.subscribe(
    'databases.tourly_db.collections.bookings.documents',
    (response) => {
        // Handle: .create, .update, .delete
    }
);
```

## Instructions
- **Payload Handling**: Inspect `response.payload` for the updated document data.
- **Scope**: Keep subscriptions specific to the current page to avoid memory leaks.
