---
name: fullstory-observe-callbacks
version: v2
description: Comprehensive guide for implementing Fullstory's Observer/Callback API (observe method) for web applications. Teaches proper event subscription, callback handling, observer cleanup, and reacting to Fullstory lifecycle events. Includes detailed good/bad examples for session URL capture, initialization handling, and integration with analytics platforms.
related_skills:
  - fullstory-async-methods
  - fullstory-capture-control
  - fullstory-logging
---

# Fullstory Observe (Callbacks & Delegates) API

## Overview

Fullstory's Observer API allows developers to register callbacks that react to Fullstory lifecycle events. Instead of polling or guessing when Fullstory is ready, you can subscribe to specific events and be notified when they occur. This is essential for:

- **Session URL Capture**: Get notified when session URL is available
- **Initialization Handling**: Know when Fullstory starts capturing
- **Third-party Integration**: Forward session URLs to other tools
- **Conditional Features**: Enable features based on FS state
- **Resource Management**: Clean up observers on component unmount

## Core Concepts

### Observer Types

| Type        | Fires When                    | Callback Receives |
| ----------- | ----------------------------- | ----------------- |
| `'start'`   | Fullstory begins capturing    | `undefined`       |
| `'session'` | Session URL becomes available | `{ url: string }` |

### Observer Lifecycle

```
FS('observe', {...})  →  Returns Observer  →  Callback fires when event occurs
                              ↓
                    Call observer.disconnect()  →  Stops listening
```

### Key Behaviors

| Behavior               | Description                                           |
| ---------------------- | ----------------------------------------------------- |
| **Immediate callback** | If event already occurred, callback fires immediately |
| **Multiple observers** | Can register multiple observers for same event        |
| **Disconnect cleanup** | Must disconnect to prevent memory leaks               |
| **Async version**      | Use `observeAsync` to wait for registration           |

---

## API Reference

### Basic Syntax

```javascript
const observer = FS('observe', {
  type: string,         // Required: Event type ('start' or 'session')
  callback: function    // Required: Function to call when event fires
});

// Later: stop observing
observer.disconnect();
```

### Async Version

```javascript
const observer = await FS('observeAsync', {
  type: string,
  callback: function
});

observer.disconnect();
```

### Parameters

| Parameter  | Type     | Required | Description                          |
| ---------- | -------- | -------- | ------------------------------------ |
| `type`     | string   | **Yes**  | Event type: `'start'` or `'session'` |
| `callback` | function | **Yes**  | Function called when event occurs    |

### Return Value

Observer object with:

- `disconnect()`: Method to stop observing

### Callback Arguments

| Event Type  | Callback Argument                                 |
| ----------- | ------------------------------------------------- |
| `'start'`   | `undefined`                                       |
| `'session'` | `{ url: string }` - Object containing session URL |

---

## ✅ GOOD IMPLEMENTATION EXAMPLES

### Example 1: Capture Session URL for Third-party Tools

```javascript
// GOOD: Forward session URL to support/analytics tools
function initializeSessionTracking() {
  const observer = FS('observe', {
    type: 'session',
    callback: (session) => {
      const sessionUrl = session.url

      // Send to support tool (e.g., Intercom, Zendesk)
      if (window.Intercom) {
        window.Intercom('update', {
          fullstory_url: sessionUrl,
        })
      }

      // Send to error tracking (e.g., Sentry, Bugsnag)
      if (window.Sentry) {
        window.Sentry.setTag('fullstory_url', sessionUrl)
      }

      // Store for later use
      window.__fullstorySessionUrl = sessionUrl

      console.log('Session URL captured:', sessionUrl)
    },
  })

  // Return cleanup function
  return () => observer.disconnect()
}

// Initialize on app load
const cleanup = initializeSessionTracking()

// On app cleanup (e.g., SPA unmount)
// cleanup();
```

**Why this is good:**

- ✅ Integrates with third-party tools
- ✅ Stores URL for later access
- ✅ Returns cleanup function
- ✅ Logs for debugging

### Example 2: React Hook for Session URL

```jsx
// GOOD: React hook for Fullstory session management
import {useState, useEffect, useCallback} from 'react'

function useFullstorySession() {
  const [sessionUrl, setSessionUrl] = useState(null)
  const [isCapturing, setIsCapturing] = useState(false)
  const [isReady, setIsReady] = useState(false)

  useEffect(() => {
    // Check if FS is available
    if (typeof FS === 'undefined') {
      return
    }

    const observers = []

    // Listen for capture start
    const startObserver = FS('observe', {
      type: 'start',
      callback: () => {
        setIsCapturing(true)
        setIsReady(true)
      },
    })
    observers.push(startObserver)

    // Listen for session URL
    const sessionObserver = FS('observe', {
      type: 'session',
      callback: (session) => {
        setSessionUrl(session.url)
      },
    })
    observers.push(sessionObserver)

    // Cleanup on unmount
    return () => {
      observers.forEach((obs) => obs.disconnect())
    }
  }, [])

  const copySessionUrl = useCallback(() => {
    if (sessionUrl) {
      navigator.clipboard.writeText(sessionUrl)
      return true
    }
    return false
  }, [sessionUrl])

  return {
    sessionUrl,
    isCapturing,
    isReady,
    copySessionUrl,
  }
}

// Usage in component
function SupportButton() {
  const {sessionUrl, isReady} = useFullstorySession()

  const handleSupportClick = () => {
    openSupportChat({
      fullstoryUrl: sessionUrl,
    })
  }

  return (
    <button onClick={handleSupportClick} disabled={!isReady}>
      Contact Support
      {sessionUrl && ' (Session will be attached)'}
    </button>
  )
}
```

**Why this is good:**

- ✅ Proper React lifecycle handling
- ✅ Cleanup on unmount prevents memory leaks
- ✅ Exposes useful state (isCapturing, isReady)
- ✅ Helper function for copying URL
- ✅ Graceful handling if FS unavailable

### Example 3: Initialize Analytics After Fullstory Ready

```javascript
// GOOD: Wait for Fullstory before initializing dependent features
class AnalyticsManager {
  constructor() {
    this.isFullstoryReady = false
    this.sessionUrl = null
    this.observers = []
    this.pendingEvents = []
  }

  initialize() {
    if (typeof FS === 'undefined') {
      console.warn('Fullstory not available')
      this.flushPendingEvents() // Send without FS context
      return
    }

    // Wait for Fullstory to start
    const startObserver = FS('observe', {
      type: 'start',
      callback: () => {
        this.isFullstoryReady = true
        this.flushPendingEvents()
      },
    })
    this.observers.push(startObserver)

    // Capture session URL
    const sessionObserver = FS('observe', {
      type: 'session',
      callback: (session) => {
        this.sessionUrl = session.url
        this.updateAnalyticsContext()
      },
    })
    this.observers.push(sessionObserver)
  }

  track(eventName, properties) {
    const enrichedEvent = {
      ...properties,
      fullstoryUrl: this.sessionUrl,
      fullstoryReady: this.isFullstoryReady,
    }

    if (this.isFullstoryReady) {
      this.sendToAnalytics(eventName, enrichedEvent)
    } else {
      // Queue until Fullstory is ready
      this.pendingEvents.push({eventName, properties: enrichedEvent})
    }
  }

  flushPendingEvents() {
    this.pendingEvents.forEach((event) => {
      this.sendToAnalytics(event.eventName, event.properties)
    })
    this.pendingEvents = []
  }

  updateAnalyticsContext() {
    // Update context in other analytics tools
    if (window.analytics) {
      window.analytics.identify({
        fullstoryUrl: this.sessionUrl,
      })
    }
  }

  sendToAnalytics(eventName, properties) {
    // Send to your analytics platform
    console.log('Analytics:', eventName, properties)
  }

  cleanup() {
    this.observers.forEach((obs) => obs.disconnect())
    this.observers = []
  }
}

// Usage
const analytics = new AnalyticsManager()
analytics.initialize()

// Track events (will be queued if FS not ready)
analytics.track('Page Viewed', {page: '/home'})
```

**Why this is good:**

- ✅ Queues events until FS ready
- ✅ Enriches events with session URL
- ✅ Handles FS not being available
- ✅ Proper cleanup method
- ✅ Updates other analytics tools

### Example 4: Async Observer Pattern

```javascript
// GOOD: Using async observers with error handling
async function setupFullstoryIntegration() {
  try {
    // Set up start observer
    const startObserver = await FS('observeAsync', {
      type: 'start',
      callback: () => {
        console.log('Fullstory started capturing')
        enableSessionReplayFeatures()
      },
    })

    // Set up session observer
    const sessionObserver = await FS('observeAsync', {
      type: 'session',
      callback: (session) => {
        console.log('Session URL:', session.url)
        notifyIntegrations(session.url)
      },
    })

    // Return combined cleanup
    return {
      cleanup: () => {
        startObserver.disconnect()
        sessionObserver.disconnect()
      },
      status: 'success',
    }
  } catch (error) {
    console.warn('Fullstory integration failed:', error)
    return {
      cleanup: () => {},
      status: 'failed',
      error,
    }
  }
}

// Usage
let fsIntegration = null

async function initApp() {
  fsIntegration = await setupFullstoryIntegration()

  if (fsIntegration.status === 'success') {
    showSessionReplayBadge()
  }
}

function cleanupApp() {
  if (fsIntegration) {
    fsIntegration.cleanup()
  }
}
```

**Why this is good:**

- ✅ Uses async version for proper error handling
- ✅ Returns status for conditional UI
- ✅ Combined cleanup function
- ✅ Graceful handling of failures

### Example 5: Session URL for Error Reports

```javascript
// GOOD: Attach session URL to all error reports
class ErrorReporter {
  constructor() {
    this.sessionUrl = null
    this.observer = null
  }

  initialize() {
    // Set up session observer
    this.observer = FS('observe', {
      type: 'session',
      callback: (session) => {
        this.sessionUrl = session.url

        // Update Sentry context
        if (window.Sentry) {
          window.Sentry.setContext('fullstory', {
            sessionUrl: session.url,
          })
        }

        // Update Bugsnag
        if (window.Bugsnag) {
          window.Bugsnag.addMetadata('fullstory', {
            sessionUrl: session.url,
          })
        }
      },
    })

    // Set up global error handler
    window.addEventListener('error', (event) => {
      this.reportError(event.error, {
        source: 'window.onerror',
        filename: event.filename,
        lineno: event.lineno,
      })
    })

    window.addEventListener('unhandledrejection', (event) => {
      this.reportError(event.reason, {
        source: 'unhandledrejection',
      })
    })
  }

  reportError(error, context = {}) {
    const report = {
      error: error?.message || String(error),
      stack: error?.stack,
      fullstoryUrl: this.sessionUrl,
      timestamp: new Date().toISOString(),
      ...context,
    }

    // Send to your error service
    this.sendErrorReport(report)

    // Also log to Fullstory
    if (typeof FS !== 'undefined') {
      FS('log', {
        level: 'error',
        msg: report.error,
      })
    }
  }

  sendErrorReport(report) {
    // Send to backend
    fetch('/api/errors', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(report),
    }).catch(console.error)
  }

  cleanup() {
    if (this.observer) {
      this.observer.disconnect()
    }
  }
}

// Initialize on app start
const errorReporter = new ErrorReporter()
errorReporter.initialize()
```

**Why this is good:**

- ✅ Integrates with popular error tools
- ✅ Auto-attaches session URL to all errors
- ✅ Also logs to Fullstory
- ✅ Cleanup method available

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Not Disconnecting Observers

```javascript
// BAD: Observer never cleaned up
function setupSessionCallback() {
  FS('observe', {
    type: 'session',
    callback: (session) => {
      console.log('Session:', session.url)
    },
  })
  // Observer never stored or cleaned up!
}

// Called multiple times in SPA
setupSessionCallback() // Leak
setupSessionCallback() // Another leak
setupSessionCallback() // More leaks...
```

**Why this is bad:**

- ❌ Observer never disconnected
- ❌ Memory leak in long-running apps
- ❌ Multiple observers = multiple callbacks
- ❌ Callbacks pile up on each call

**CORRECTED VERSION:**

```javascript
// GOOD: Store and cleanup observer
let sessionObserver = null

function setupSessionCallback() {
  // Clean up existing observer first
  if (sessionObserver) {
    sessionObserver.disconnect()
  }

  sessionObserver = FS('observe', {
    type: 'session',
    callback: (session) => {
      console.log('Session:', session.url)
    },
  })
}

function cleanup() {
  if (sessionObserver) {
    sessionObserver.disconnect()
    sessionObserver = null
  }
}
```

### Example 2: Wrong Event Type

```javascript
// BAD: Invalid event type
FS('observe', {
  type: 'ready', // BAD: Not a valid type!
  callback: () => console.log('Ready!'),
})

FS('observe', {
  type: 'url', // BAD: Not a valid type!
  callback: (url) => console.log(url),
})
```

**Why this is bad:**

- ❌ 'ready' and 'url' are not valid types
- ❌ Callback will never fire
- ❌ No error thrown, silent failure

**CORRECTED VERSION:**

```javascript
// GOOD: Use valid event types
FS('observe', {
  type: 'start', // Valid: when capture starts
  callback: () => console.log('Fullstory started!'),
})

FS('observe', {
  type: 'session', // Valid: when session URL ready
  callback: (session) => console.log('URL:', session.url),
})
```

### Example 3: Expecting Callback Value for 'start'

```javascript
// BAD: Expecting session data from 'start' callback
FS('observe', {
  type: 'start',
  callback: (session) => {
    // BAD: session is undefined for 'start' type!
    console.log('Session URL:', session.url) // Error!
  },
})
```

**Why this is bad:**

- ❌ 'start' callback receives no arguments
- ❌ Will throw error accessing .url of undefined
- ❌ Wrong event type for the use case

**CORRECTED VERSION:**

```javascript
// GOOD: Use 'session' type for URL
FS('observe', {
  type: 'session', // Correct type for getting URL
  callback: (session) => {
    console.log('Session URL:', session.url) // Works!
  },
})
```

### Example 4: Blocking on Observer

```javascript
// BAD: Blocking app initialization on observer
async function initApp() {
  let sessionUrl = null

  // This will never resolve because observe doesn't return a promise
  // that waits for the callback!
  await new Promise((resolve) => {
    FS('observe', {
      type: 'session',
      callback: (session) => {
        sessionUrl = session.url
        resolve()
      },
    })
  })

  // If Fullstory is blocked, this never runs
  startApp(sessionUrl)
}
```

**Why this is bad:**

- ❌ If FS blocked, promise never resolves
- ❌ App initialization hangs forever
- ❌ Observer registration is sync, callback is async

**CORRECTED VERSION:**

```javascript
// GOOD: Non-blocking with timeout
async function initApp() {
  let sessionUrl = null

  // Set up observer but don't block
  const sessionPromise = new Promise((resolve) => {
    if (typeof FS === 'undefined') {
      resolve(null)
      return
    }

    FS('observe', {
      type: 'session',
      callback: (session) => {
        sessionUrl = session.url
        resolve(session.url)
      },
    })

    // Timeout after 5 seconds
    setTimeout(() => resolve(null), 5000)
  })

  // Start app immediately
  startApp(null)

  // Update with session URL when available
  sessionPromise.then((url) => {
    if (url) updateAppWithSessionUrl(url)
  })
}
```

### Example 5: Registering Observer Before FS Loads

```javascript
// BAD: Using FS before it's defined
<script>
  // FS might not be defined yet!
  FS('observe', {
    type: 'session',
    callback: (session) => {
      console.log(session.url);
    }
  });
</script>
<script src="fullstory-snippet.js"></script>
```

**Why this is bad:**

- ❌ FS is not defined when observer is registered
- ❌ Will throw ReferenceError
- ❌ Script order matters

**CORRECTED VERSION:**

```javascript
// GOOD: Check FS exists first, or use after snippet
<script src="fullstory-snippet.js"></script>
<script>
  if (typeof FS !== 'undefined') {
    FS('observe', {
      type: 'session',
      callback: (session) => {
        console.log(session.url);
      }
    });
  }
</script>

// OR: Use DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  if (typeof FS !== 'undefined') {
    FS('observe', {...});
  }
});
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Observer Manager Class

```javascript
// Centralized observer management
class FullstoryObserverManager {
  constructor() {
    this.observers = new Map()
  }

  register(name, type, callback) {
    // Disconnect existing observer with same name
    if (this.observers.has(name)) {
      this.observers.get(name).disconnect()
    }

    if (typeof FS === 'undefined') {
      console.warn(`Cannot register observer '${name}': FS not available`)
      return false
    }

    const observer = FS('observe', {type, callback})
    this.observers.set(name, observer)
    return true
  }

  unregister(name) {
    if (this.observers.has(name)) {
      this.observers.get(name).disconnect()
      this.observers.delete(name)
    }
  }

  unregisterAll() {
    this.observers.forEach((obs) => obs.disconnect())
    this.observers.clear()
  }
}

// Usage
const fsObservers = new FullstoryObserverManager()

fsObservers.register('session', 'session', (session) => {
  console.log('Session URL:', session.url)
})

fsObservers.register('start', 'start', () => {
  console.log('Fullstory started')
})

// Cleanup
fsObservers.unregisterAll()
```

### Pattern 2: Vue Composable

```javascript
// Vue 3 composable for Fullstory session
import { ref, onMounted, onUnmounted } from 'vue';

export function useFullstorySession() {
  const sessionUrl = ref(null);
  const isCapturing = ref(false);
  const observers = [];

  onMounted(() => {
    if (typeof FS === 'undefined') return;

    observers.push(
      FS('observe', {
        type: 'start',
        callback: () => {
          isCapturing.value = true;
        }
      })
    );

    observers.push(
      FS('observe', {
        type: 'session',
        callback: (session) => {
          sessionUrl.value = session.url;
        }
      })
    );
  });

  onUnmounted(() => {
    observers.forEach(obs => obs.disconnect());
  });

  return {
    sessionUrl,
    isCapturing
  };
}

// Usage in component
<script setup>
import { useFullstorySession } from './useFullstorySession';

const { sessionUrl, isCapturing } = useFullstorySession();
</script>

<template>
  <div v-if="isCapturing">
    Session is being recorded
    <a v-if="sessionUrl" :href="sessionUrl" target="_blank">
      View Session
    </a>
  </div>
</template>
```

### Pattern 3: Event Emitter Pattern

```javascript
// Event emitter for Fullstory events
class FullstoryEventEmitter {
  constructor() {
    this.listeners = {
      start: [],
      session: [],
    }
    this.state = {
      started: false,
      sessionUrl: null,
    }
    this.observers = []

    this.initialize()
  }

  initialize() {
    if (typeof FS === 'undefined') return

    this.observers.push(
      FS('observe', {
        type: 'start',
        callback: () => {
          this.state.started = true
          this.emit('start')
        },
      }),
    )

    this.observers.push(
      FS('observe', {
        type: 'session',
        callback: (session) => {
          this.state.sessionUrl = session.url
          this.emit('session', session)
        },
      }),
    )
  }

  on(event, callback) {
    this.listeners[event]?.push(callback)

    // If event already occurred, call immediately
    if (event === 'start' && this.state.started) {
      callback()
    }
    if (event === 'session' && this.state.sessionUrl) {
      callback({url: this.state.sessionUrl})
    }

    return () => this.off(event, callback)
  }

  off(event, callback) {
    const idx = this.listeners[event]?.indexOf(callback)
    if (idx > -1) {
      this.listeners[event].splice(idx, 1)
    }
  }

  emit(event, data) {
    this.listeners[event]?.forEach((cb) => cb(data))
  }

  destroy() {
    this.observers.forEach((obs) => obs.disconnect())
    this.listeners = {start: [], session: []}
  }
}

// Global instance
const fsEvents = new FullstoryEventEmitter()

// Usage
const unsubscribe = fsEvents.on('session', (session) => {
  console.log('Session URL:', session.url)
})

// Later
unsubscribe()
```

---

## TROUBLESHOOTING

### Callback Never Fires

**Symptom**: Observer registered but callback never called

**Common Causes**:

1. ❌ Fullstory not loaded or blocked
2. ❌ Wrong event type
3. ❌ Fullstory not capturing (e.g., excluded page)

**Solutions**:

- ✅ Verify FS is defined
- ✅ Check event type is 'start' or 'session'
- ✅ Check Fullstory console for errors

### Multiple Callbacks

**Symptom**: Callback fires multiple times unexpectedly

**Common Causes**:

1. ❌ Multiple observers registered
2. ❌ Observer not cleaned up in SPA
3. ❌ Component re-mounts without cleanup

**Solutions**:

- ✅ Store and reuse observer reference
- ✅ Clean up on component unmount
- ✅ Check for existing observer before registering

### Memory Leaks

**Symptom**: Memory usage grows over time

**Common Causes**:

1. ❌ Observers never disconnected
2. ❌ New observers on each navigation
3. ❌ Missing cleanup in React/Vue

**Solutions**:

- ✅ Always call disconnect()
- ✅ Use useEffect cleanup in React
- ✅ Use onUnmounted in Vue

---

## KEY TAKEAWAYS FOR AGENT

When helping developers with Observer API:

1. **Always emphasize**:
   - Store observer reference
   - Call disconnect() on cleanup
   - Use 'session' for URL, 'start' for capture start
   - Handle FS not being available

2. **Common mistakes to watch for**:
   - Not disconnecting observers (memory leak)
   - Wrong event type
   - Expecting URL from 'start' callback
   - Blocking on observer callback
   - Multiple observers without cleanup

3. **Questions to ask developers**:
   - Is this a SPA or traditional app?
   - Do you need the session URL or just capture status?
   - What framework are you using?
   - How will you clean up the observer?

4. **Best practices to recommend**:
   - Use framework-specific patterns (hooks, composables)
   - Implement cleanup in lifecycle methods
   - Don't block critical paths on callbacks
   - Handle immediate callback for already-occurred events

---

## REFERENCE LINKS

- **Callbacks and Delegates**: https://developer.fullstory.com/browser/fullcapture/callbacks-and-delegates/
- **Get Session Details**: https://developer.fullstory.com/browser/get-session-details/
- **Asynchronous Methods**: https://developer.fullstory.com/browser/asynchronous-methods/

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's Observer/Callback API correctly for web applications._
