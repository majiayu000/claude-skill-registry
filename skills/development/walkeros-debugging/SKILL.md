---
name: walkeros-debugging
description:
  Use when walkerOS events aren't reaching destinations, debugging event flow,
  or troubleshooting mapping issues. Covers common problems and debugging
  strategies.
---

# Debugging walkerOS Events

## Quick Diagnosis

| Symptom                            | Likely Cause                 | Check                                    |
| ---------------------------------- | ---------------------------- | ---------------------------------------- |
| No events at all                   | Source not initialized       | Console for errors, verify `startFlow()` |
| Events fire but destination silent | Mapping mismatch             | Event name matches mapping?              |
| Partial data missing               | Path doesn't exist           | Log event structure, check nested paths  |
| Consent blocking                   | Required consent not granted | Check `consent` config, grant consent    |
| Destination error                  | Vendor API issue             | Check network tab, vendor console        |

## Debugging Strategies

### 1. Console Logging

**Log all events at collector level:**

```typescript
import { startFlow } from '@walkeros/collector';

const { elb } = await startFlow({
  destinations: {
    debug: {
      push: async (event, context) => {
        console.log('[walkerOS Event]', {
          name: event.name,
          data: event.data,
          context: event.context,
          consent: event.consent,
          timestamp: event.timestamp,
        });
      },
      config: {},
    },
    // ... other destinations
  },
});
```

### 2. Network Tab Inspection

For destinations that make HTTP calls:

1. Open DevTools → Network tab
2. Filter by destination domain (e.g., `google-analytics.com`, `facebook.com`)
3. Trigger event
4. Inspect request payload

**What to look for:**

- Request being made at all?
- Correct endpoint URL?
- Payload structure matches vendor spec?

### 3. Vendor Debug Tools

| Vendor    | Debug Tool                                                                                    |
| --------- | --------------------------------------------------------------------------------------------- |
| GA4       | [GA4 DebugView](https://support.google.com/analytics/answer/7201382)                          |
| Meta      | [Facebook Pixel Helper](https://developers.facebook.com/docs/meta-pixel/support/pixel-helper) |
| Plausible | [Plausible Dashboard real-time](https://plausible.io/docs)                                    |

### 4. Dry Run Mode

Test mapping without sending to vendor:

```typescript
const destination = {
  ...actualDestination,
  config: {
    ...actualDestination.config,
    dryRun: true, // Events processed but not sent
  },
};
```

## Common Issues

### Event Name Mismatch

**Problem:** Event fires but destination doesn't receive it.

```typescript
// Event pushed
elb('product view', { id: 'P123' });

// Mapping expects different name
mapping: {
  Product: {
    // Wrong: capital P
    View: {
      // Wrong: capital V
      name: 'view_item';
    }
  }
}
```

**Fix:** Event names are case-sensitive. Use exact match:

```typescript
mapping: {
  product: {
    view: {
      name: 'view_item';
    }
  }
}
```

### Missing Nested Data

**Problem:** `items` array is empty in destination.

```typescript
// Event structure
{
  name: 'order complete',
  data: { total: 100 },
  nested: [
    { type: 'product', data: { id: 'P1' } }
  ]
}

// Mapping tries wrong path
data: {
  map: {
    items: {
      loop: [
        'data.items',  // Wrong: nested is at root, not in data
        { map: { id: 'data.id' } }
      ]
    }
  }
}
```

**Fix:** Use correct path to nested array:

```typescript
items: {
  loop: [
    'nested', // Correct: root-level nested
    { map: { item_id: 'data.id' } },
  ];
}
```

### Consent Blocking Events

**Problem:** Events not reaching destination.

**Check 1:** Does destination require consent?

```typescript
// Destination config
config: {
  consent: {
    marketing: true;
  } // Requires marketing consent
}
```

**Check 2:** Is consent granted?

```typescript
// Check current consent state
console.log(event.consent);

// Grant consent
elb('walker consent', { marketing: true });
```

### Vendor SDK Not Loaded

**Problem:** `TypeError: env.window.gtag is not a function`

**Cause:** Vendor script not loaded before push.

**Fix:** Ensure init() loads script:

```typescript
init: async (config, env) => {
  // Wait for script to load
  await loadScript('https://vendor.com/sdk.js');
  // Verify SDK available
  if (!env.window.vendorSdk) {
    throw new Error('Vendor SDK failed to load');
  }
},
```

### Function Mapping Errors

**Problem:** `Cannot read property 'price' of undefined`

```typescript
// Mapping with unsafe access
data: {
  map: {
    value: {
      fn: (e) => e.data.price * 100;
    } // Fails if data.price undefined
  }
}
```

**Fix:** Add null checks:

```typescript
value: {
  fn: (e) => (e.data?.price ?? 0) * 100;
}
```

## Debugging Checklist

When events aren't working:

1. [ ] **Console errors?** Check browser console for exceptions
2. [ ] **Event pushed?** Add debug destination to log all events
3. [ ] **Mapping matched?** Verify entity/action names exactly match
4. [ ] **Data paths correct?** Log full event structure, verify paths exist
5. [ ] **Consent granted?** Check consent requirements and state
6. [ ] **SDK loaded?** Verify vendor script loaded before push
7. [ ] **Network request?** Check DevTools network tab
8. [ ] **Vendor receiving?** Use vendor debug tools

## Testing in Isolation

Test destination push directly:

```typescript
import { push } from '@walkeros/web-destination-gtag';
import { mockEnv } from '@walkeros/core';

// Create test event
const event = {
  name: 'product view',
  data: { id: 'P123', price: 99 },
  // ... full event
};

// Mock env to capture calls
const calls = [];
const testEnv = mockEnv(baseEnv, (path, args) => {
  calls.push({ path, args });
});

// Test push directly
await push(event, { config: testConfig, env: testEnv });

// Inspect what was called
console.log(calls);
```

## Related Skills

- [walkeros-understanding-flow](../walkeros-understanding-flow/SKILL.md) - Event
  flow architecture
- [walkeros-understanding-destinations](../walkeros-understanding-destinations/SKILL.md) -
  Destination interface
- [walkeros-mapping-configuration](../walkeros-mapping-configuration/SKILL.md) -
  Mapping recipes
