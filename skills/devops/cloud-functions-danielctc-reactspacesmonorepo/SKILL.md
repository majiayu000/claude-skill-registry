---
name: cloud-functions
description: Firebase Cloud Functions V2 patterns for this project. Use when writing or reviewing Cloud Functions.
license: MIT
---

# Firebase Cloud Functions

## When to Use

Activate when:

- Writing new Cloud Functions
- Adding security to callable functions
- Fixing function timeouts or performance
- Implementing rate limiting

## Project Structure

```
functions/
├── src/
│   ├── index.js          # Function exports
│   ├── analytics.js      # Analytics tracking
│   ├── rateLimiter.js    # Rate limiting utility
│   ├── chatCleanup.js    # Scheduled cleanup
│   └── rateLimitCleanup.js
├── package.json
└── .eslintrc.js
```

## Function Configuration

```javascript
const { onCall, HttpsError } = require('firebase-functions/v2/https');
const { onSchedule } = require('firebase-functions/v2/scheduler');

// Standard config
const functionConfig = {
  region: 'us-central1',
  memory: '256MiB',
  timeoutSeconds: 60,
  minInstances: 0, // Consider 1 for critical paths
};

exports.myFunction = onCall(functionConfig, async (request) => {
  // Implementation
});
```

## Security Patterns

### Authentication Check

```javascript
exports.secureFunction = onCall(functionConfig, async (request) => {
  // Must be authenticated
  if (!request.auth) {
    throw new HttpsError('unauthenticated', 'Must be logged in');
  }

  const uid = request.auth.uid;
  // Continue...
});
```

### Space Ownership Verification (CRITICAL)

```javascript
// ALWAYS verify ownership before writing to space data
async function verifySpaceAccess(uid, spaceId, db) {
  const spaceDoc = await db.collection('spaces').doc(spaceId).get();

  if (!spaceDoc.exists) {
    throw new HttpsError('not-found', 'Space not found');
  }

  const space = spaceDoc.data();

  // Check ownership or host status
  const userDoc = await db.collection('users').doc(uid).get();
  const userGroups = userDoc.data()?.groups || [];

  const hasAccess =
    userGroups.includes(`space_${spaceId}_owners`) ||
    userGroups.includes(`space_${spaceId}_hosts`) ||
    userGroups.includes('disruptiveAdmin');

  if (!hasAccess) {
    throw new HttpsError('permission-denied', 'No access to this space');
  }

  return space;
}
```

### Input Validation

```javascript
exports.trackAnalytics = onCall(functionConfig, async (request) => {
  const { spaceId, eventType, eventData } = request.data;

  // Validate required fields
  if (!spaceId || typeof spaceId !== 'string') {
    throw new HttpsError('invalid-argument', 'Invalid spaceId');
  }

  // Validate data size (prevent abuse)
  const dataSize = JSON.stringify(eventData || {}).length;
  if (dataSize > 10240) {
    // 10KB max
    throw new HttpsError('invalid-argument', 'Event data too large');
  }

  // Verify space access BEFORE writing
  await verifySpaceAccess(request.auth.uid, spaceId, db);

  // Continue with operation...
});
```

## Rate Limiting

```javascript
const { checkRateLimit } = require('./rateLimiter');

exports.rateLimitedFunction = onCall(functionConfig, async (request) => {
  const uid = request.auth?.uid || request.rawRequest.ip;

  const { allowed, remaining } = await checkRateLimit(uid, 'myFunction', {
    maxRequests: 100,
    windowMs: 60000, // 1 minute
  });

  if (!allowed) {
    throw new HttpsError('resource-exhausted', 'Rate limit exceeded');
  }

  // Continue...
});
```

## Scheduled Functions

```javascript
exports.cleanupOldData = onSchedule(
  {
    schedule: 'every day 02:00',
    timeZone: 'UTC',
    region: 'us-central1',
  },
  async (event) => {
    const cutoff = new Date();
    cutoff.setHours(cutoff.getHours() - 24);

    // Use batched deletes for large datasets
    const batch = db.batch();
    let count = 0;

    const snapshot = await db
      .collection('tempData')
      .where('createdAt', '<', cutoff)
      .limit(500) // Batch size
      .get();

    snapshot.docs.forEach((doc) => {
      batch.delete(doc.ref);
      count++;
    });

    if (count > 0) {
      await batch.commit();
    }

    console.log(`Cleaned up ${count} documents`);
  }
);
```

## Error Handling

### DO

```javascript
// Return generic errors to clients
throw new HttpsError('internal', 'Operation failed');

// Log detailed errors server-side
console.error('Detailed error:', error.message, error.stack);
```

### DON'T

```javascript
// Never leak internal details
throw new HttpsError('internal', error.message); // BAD
throw new HttpsError('internal', error.stack); // BAD
```

## Performance Tips

| Issue                 | Solution                                    |
| --------------------- | ------------------------------------------- |
| Cold starts           | Set `minInstances: 1` for critical paths    |
| Timeout on large data | Use pagination, `limit()` queries           |
| Sequential processing | Use `Promise.all()` for parallel operations |
| Document size bloat   | Archive old data, use subcollections        |

## Testing

```bash
# Start emulator
firebase emulators:start --only functions

# Deploy single function
firebase deploy --only functions:myFunction

# View logs
firebase functions:log
```

## Known Issues in This Project

| Issue                      | Location             | Fix                       |
| -------------------------- | -------------------- | ------------------------- |
| No space ownership check   | analytics.js:29, 143 | Add `verifySpaceAccess()` |
| No sessionData size limit  | analytics.js:163     | Add 10KB validation       |
| Error message leak         | chatCleanup.js:190   | Use generic error         |
| Sequential space iteration | chatCleanup.js:52    | Use `Promise.all()`       |

## Related Files

- `functions/src/analytics.js` - Analytics functions
- `functions/src/rateLimiter.js` - Rate limiting
- `functions/src/chatCleanup.js` - Scheduled cleanup
