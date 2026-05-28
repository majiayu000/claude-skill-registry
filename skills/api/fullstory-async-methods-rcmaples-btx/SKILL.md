---
name: fullstory-async-methods
version: v2
description: Comprehensive guide for implementing Fullstory's Asynchronous API methods (Async suffix variants) for web applications. Teaches proper Promise handling, await patterns, error handling, and when to use async vs fire-and-forget methods. Includes detailed good/bad examples for initialization waiting, session URL retrieval, and conditional flows to help developers handle Fullstory's asynchronous nature correctly.
related_skills:
  - fullstory-observe-callbacks
  - fullstory-identify-users
  - fullstory-analytics-events
  - fullstory-capture-control
---

# Fullstory Asynchronous Methods API

## Overview

Fullstory's Browser API provides asynchronous versions of all methods by appending `Async` to the method name. These async methods return Promise-like objects that resolve when Fullstory has started and the action completes. This is essential for:

- **Initialization Waiting**: Wait for Fullstory to fully bootstrap before taking actions
- **Session URL Retrieval**: Get the session replay URL for logging, support tickets, etc.
- **Error Handling**: Know if an API call succeeded or failed
- **Sequential Operations**: Ensure operations complete in order
- **Conditional Logic**: Take action based on Fullstory state

## Core Concepts

### Sync vs Async Methods

| Method Type             | Returns      | Use When                                   |
| ----------------------- | ------------ | ------------------------------------------ |
| `FS('methodName')`      | undefined    | Fire-and-forget, don't need result         |
| `FS('methodNameAsync')` | Promise-like | Need result, error handling, or sequencing |

### Promise-like Object

The object returned from async methods:

- Can be `await`ed
- Supports `.then()` chaining
- **Important**: `.catch()` may not work in older browsers without Promise polyfill
- May reject if Fullstory fails to initialize

### Available Async Methods

Every FS method has an async variant:

| Sync Method                  | Async Method                      |
| ---------------------------- | --------------------------------- |
| `FS('setIdentity', {...})`   | `FS('setIdentityAsync', {...})`   |
| `FS('setProperties', {...})` | `FS('setPropertiesAsync', {...})` |
| `FS('trackEvent', {...})`    | `FS('trackEventAsync', {...})`    |
| `FS('getSession')`           | `FS('getSessionAsync')`           |
| `FS('shutdown')`             | `FS('shutdownAsync')`             |
| `FS('restart')`              | `FS('restartAsync')`              |
| `FS('log', {...})`           | `FS('logAsync', {...})`           |

---

## API Reference

### Basic Syntax

```javascript
// Async/await pattern
const result = await FS('methodNameAsync', params)

// Promise pattern
FS('methodNameAsync', params).then((result) => {
  /* handle result */
})
```

### Return Values

| Method               | Resolves With                        |
| -------------------- | ------------------------------------ |
| `getSessionAsync`    | Session URL string                   |
| `setIdentityAsync`   | undefined (completion signal)        |
| `setPropertiesAsync` | undefined                            |
| `trackEventAsync`    | undefined                            |
| `shutdownAsync`      | undefined                            |
| `restartAsync`       | undefined                            |
| `observeAsync`       | Observer object with `.disconnect()` |

### Rejection Scenarios

The Promise may reject when:

- Malformed or missing configuration (no `_fs_org`)
- User on unsupported browser
- Error in `rec/settings` or `rec/page` calls
- Organization over quota
- Fullstory script blocked by ad blocker (may not reliably reject)

---

## ✅ GOOD IMPLEMENTATION EXAMPLES

### Example 1: Get Session URL for Support

```javascript
// GOOD: Get session URL for support ticket
async function attachSessionToSupportTicket(ticketId) {
  try {
    const sessionUrl = await FS('getSessionAsync')

    // Attach to support ticket
    await updateSupportTicket(ticketId, {
      fullstoryUrl: sessionUrl,
      attachedAt: new Date().toISOString(),
    })

    console.log('Session attached to ticket:', sessionUrl)
    return sessionUrl
  } catch (error) {
    console.warn('Could not get Fullstory session:', error)
    // Continue without session URL - non-critical
    return null
  }
}

// Usage
document.getElementById('help-button').addEventListener('click', async () => {
  const ticket = await createSupportTicket(userIssue)
  await attachSessionToSupportTicket(ticket.id)
  showTicketConfirmation(ticket)
})
```

**Why this is good:**

- ✅ Uses try/catch for error handling
- ✅ Gracefully handles Fullstory being unavailable
- ✅ Non-blocking failure (user can still submit ticket)
- ✅ Returns null on failure for caller to handle

### Example 2: Wait for Fullstory Before Critical Actions

```javascript
// GOOD: Ensure Fullstory is ready before identifying
async function initializeAnalytics(user) {
  try {
    // Wait for Fullstory to be ready
    await FS('setIdentityAsync', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email,
      },
    })

    console.log('User identified successfully')

    // Now safe to track initial events
    await FS('trackEventAsync', {
      name: 'Session Started',
      properties: {
        entryPage: window.location.pathname,
        referrer: document.referrer,
      },
    })

    return true
  } catch (error) {
    console.error('Fullstory initialization failed:', error)
    // Analytics failure shouldn't break the app
    return false
  }
}

// Usage in app bootstrap
async function bootstrap() {
  const user = await authenticateUser()

  // Initialize analytics (don't block on failure)
  initializeAnalytics(user)

  // Continue app initialization
  renderApp()
}
```

**Why this is good:**

- ✅ Waits for identification to complete
- ✅ Sequential: identify before tracking events
- ✅ Handles errors gracefully
- ✅ Doesn't block app on analytics failure

### Example 3: Session URL in Error Reports

```javascript
// GOOD: Include session URL in error logging
async function captureError(error, context = {}) {
  let sessionUrl = null

  try {
    // Try to get session URL, but don't let it block error reporting
    sessionUrl = await Promise.race([
      FS('getSessionAsync'),
      new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 2000)),
    ])
  } catch (e) {
    // Session URL unavailable - continue without it
  }

  // Send error to monitoring service
  await errorMonitor.captureException(error, {
    ...context,
    fullstoryUrl: sessionUrl,
    timestamp: new Date().toISOString(),
  })

  // Also log to Fullstory if available
  if (typeof FS !== 'undefined') {
    FS('log', {
      level: 'error',
      msg: error.message,
    })
  }
}

// Usage
window.addEventListener('error', (event) => {
  captureError(event.error, {
    source: 'window.onerror',
    filename: event.filename,
    lineno: event.lineno,
  })
})
```

**Why this is good:**

- ✅ Timeout prevents hanging on unresponsive FS
- ✅ Error reporting continues without session URL
- ✅ Enriches error context when available
- ✅ Logs error to Fullstory too

### Example 4: Observer Pattern with Async

```javascript
// GOOD: Set up Fullstory observers with proper cleanup
async function setupFullstoryObservers() {
  const observers = []

  try {
    // Observer for when Fullstory starts capturing
    const startObserver = await FS('observeAsync', {
      type: 'start',
      callback: () => {
        console.log('Fullstory started capturing')
        initializeSessionTracking()
      },
    })
    observers.push(startObserver)

    // Observer for session URL availability
    const sessionObserver = await FS('observeAsync', {
      type: 'session',
      callback: (session) => {
        console.log('Session URL:', session.url)
        storeSessionUrl(session.url)
      },
    })
    observers.push(sessionObserver)

    // Return cleanup function
    return () => {
      observers.forEach((obs) => obs.disconnect())
    }
  } catch (error) {
    console.warn('Could not set up Fullstory observers:', error)
    return () => {} // No-op cleanup
  }
}

// Usage with React
function App() {
  useEffect(() => {
    let cleanup = () => {}

    setupFullstoryObservers().then((cleanupFn) => {
      cleanup = cleanupFn
    })

    return () => cleanup()
  }, [])

  return <AppContent />
}
```

**Why this is good:**

- ✅ Proper async observer setup
- ✅ Cleanup function for component unmount
- ✅ Handles initialization failure
- ✅ Multiple observers managed together

### Example 5: Conditional Feature Based on FS Status

```javascript
// GOOD: Enable features only if Fullstory is working
class SessionReplayFeature {
  constructor() {
    this.isAvailable = false
    this.sessionUrl = null
  }

  async initialize() {
    try {
      // Check if Fullstory is capturing
      this.sessionUrl = await FS('getSessionAsync')
      this.isAvailable = true
      return true
    } catch (error) {
      this.isAvailable = false
      console.info('Session replay feature unavailable:', error.message)
      return false
    }
  }

  getShareableLink() {
    if (!this.isAvailable || !this.sessionUrl) {
      return null
    }
    return this.sessionUrl
  }

  renderShareButton() {
    if (!this.isAvailable) {
      return null // Don't show button if FS unavailable
    }

    return `<button onclick="copySessionLink()">Share Session</button>`
  }
}

// Usage
const sessionReplay = new SessionReplayFeature()

async function initializeUI() {
  await sessionReplay.initialize()

  if (sessionReplay.isAvailable) {
    showSessionReplayUI()
  }
}
```

**Why this is good:**

- ✅ Graceful degradation when FS unavailable
- ✅ Feature flag based on actual FS status
- ✅ No broken UI if FS blocked
- ✅ Clear availability check

### Example 6: Sequential Operations

```javascript
// GOOD: Ensure proper sequence of FS operations
async function completeCheckout(orderData) {
  try {
    // 1. First, ensure user is identified
    await FS('setIdentityAsync', {
      uid: orderData.userId,
      properties: {
        displayName: orderData.customerName,
        email: orderData.customerEmail,
      },
    })

    // 2. Update user properties with purchase info
    await FS('setPropertiesAsync', {
      type: 'user',
      properties: {
        lifetimeValue: orderData.customerLTV,
        totalOrders: orderData.customerOrderCount,
        lastOrderAt: new Date().toISOString(),
      },
    })

    // 3. Track the purchase event
    await FS('trackEventAsync', {
      name: 'Order Completed',
      properties: {
        orderId: orderData.id,
        revenue: orderData.total,
        itemCount: orderData.items.length,
      },
    })

    // 4. Get session URL for order records
    const sessionUrl = await FS('getSessionAsync')

    // 5. Update order with session URL
    await saveOrderSessionUrl(orderData.id, sessionUrl)

    console.log('Checkout tracked successfully')
  } catch (error) {
    // Log but don't fail checkout
    console.error('Analytics tracking failed:', error)
  }
}
```

**Why this is good:**

- ✅ Operations happen in correct order
- ✅ User identified before properties set
- ✅ Event tracked after user data set
- ✅ Session URL captured at end
- ✅ Errors don't break checkout

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Blocking App on Fullstory

```javascript
// BAD: Blocking application startup on Fullstory
async function startApp() {
  // This will hang if Fullstory is blocked!
  const sessionUrl = await FS('getSessionAsync')

  // App never starts if FS fails
  renderApp()
}
```

**Why this is bad:**

- ❌ App hangs if Fullstory blocked by ad blocker
- ❌ Promise may never resolve
- ❌ Critical path depends on non-critical service
- ❌ No timeout or error handling

**CORRECTED VERSION:**

```javascript
// GOOD: Non-blocking initialization
async function startApp() {
  // Start app immediately
  renderApp()

  // Initialize analytics separately
  try {
    await Promise.race([
      FS('getSessionAsync'),
      new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 5000)),
    ])
    enableAnalyticsFeatures()
  } catch (error) {
    console.warn('Fullstory unavailable, continuing without analytics')
  }
}
```

### Example 2: Missing Error Handling

```javascript
// BAD: No error handling for async call
async function trackPurchase(order) {
  const sessionUrl = await FS('getSessionAsync') // May throw!
  saveSessionToOrder(order.id, sessionUrl) // Never runs if above fails

  await FS('trackEventAsync', {
    // Also may throw
    name: 'Purchase',
    properties: {orderId: order.id},
  })
}
```

**Why this is bad:**

- ❌ Unhandled promise rejection
- ❌ Subsequent code won't run on failure
- ❌ No graceful degradation
- ❌ Could crash in strict mode

**CORRECTED VERSION:**

```javascript
// GOOD: Proper error handling
async function trackPurchase(order) {
  let sessionUrl = null

  try {
    sessionUrl = await FS('getSessionAsync')
  } catch (error) {
    console.warn('Could not get session URL:', error)
  }

  if (sessionUrl) {
    saveSessionToOrder(order.id, sessionUrl)
  }

  try {
    await FS('trackEventAsync', {
      name: 'Purchase',
      properties: {
        orderId: order.id,
        hasSessionUrl: !!sessionUrl,
      },
    })
  } catch (error) {
    console.warn('Could not track purchase event:', error)
  }
}
```

### Example 3: Using .catch() Without Polyfill

```javascript
// BAD: .catch() may not work in older browsers
FS('getSessionAsync')
  .then((url) => console.log('Session:', url))
  .catch((err) => console.error('Error:', err)) // May fail silently in IE11!
```

**Why this is bad:**

- ❌ `.catch()` not supported in browsers without Promise
- ❌ Fullstory's Promise-like object may not implement catch
- ❌ Errors may go unhandled

**CORRECTED VERSION:**

```javascript
// GOOD: Use try/catch with async/await
async function getSession() {
  try {
    const url = await FS('getSessionAsync')
    console.log('Session:', url)
    return url
  } catch (err) {
    console.error('Error:', err)
    return null
  }
}

// OR: Use .then() only with error callback
FS('getSessionAsync').then(
  (url) => console.log('Session:', url),
  (err) => console.error('Error:', err), // Second arg to .then() works
)
```

### Example 4: Unnecessary Async Usage

```javascript
// BAD: Using async when you don't need the result
async function handleButtonClick() {
  // Don't need to await fire-and-forget events
  await FS('trackEventAsync', {
    name: 'Button Clicked',
    properties: {buttonId: 'submit'},
  })

  // User waits unnecessarily
  proceedWithAction()
}
```

**Why this is bad:**

- ❌ Adds unnecessary latency to user action
- ❌ User waits for analytics to complete
- ❌ No value from awaiting (result not used)

**CORRECTED VERSION:**

```javascript
// GOOD: Fire-and-forget for events
function handleButtonClick() {
  // Don't await - fire and forget
  FS('trackEvent', {
    name: 'Button Clicked',
    properties: {buttonId: 'submit'},
  })

  // Proceed immediately
  proceedWithAction()
}
```

### Example 5: Race Condition with Async

```javascript
// BAD: Race condition between identify and track
async function onLogin(user) {
  // These run in parallel - trackEvent may fire before identity!
  FS('setIdentityAsync', {uid: user.id})
  FS('trackEventAsync', {name: 'Login'})
}
```

**Why this is bad:**

- ❌ Event may fire before identity is set
- ❌ Event could be attributed to anonymous user
- ❌ Data integrity issue

**CORRECTED VERSION:**

```javascript
// GOOD: Sequential with proper awaiting
async function onLogin(user) {
  // First identify
  await FS('setIdentityAsync', {
    uid: user.id,
    properties: {displayName: user.name},
  })

  // Then track event (now properly attributed)
  await FS('trackEventAsync', {
    name: 'Login',
    properties: {method: 'password'},
  })
}

// OR: For non-critical, use sync versions (they queue properly)
function onLogin(user) {
  FS('setIdentity', {uid: user.id}) // Queued first
  FS('trackEvent', {name: 'Login'}) // Queued second
  // Fullstory processes queue in order
}
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Safe Async Wrapper

```javascript
// Wrapper for safe FS async calls with timeout
async function safeFS(method, params, options = {}) {
  const {timeout = 5000, fallback = null} = options

  // Check if FS exists
  if (typeof FS === 'undefined') {
    console.warn(`FS not available for ${method}`)
    return fallback
  }

  try {
    const result = await Promise.race([
      FS(method, params),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error(`FS ${method} timeout`)), timeout),
      ),
    ])
    return result
  } catch (error) {
    console.warn(`FS ${method} failed:`, error.message)
    return fallback
  }
}

// Usage
const sessionUrl = await safeFS('getSessionAsync', undefined, {
  timeout: 3000,
  fallback: null,
})

await safeFS('trackEventAsync', {
  name: 'Page View',
  properties: {page: '/home'},
})
```

### Pattern 2: Initialization Status Manager

```javascript
// Track Fullstory initialization status
class CaptureStatusManager {
  constructor() {
    this.status = 'pending'
    this.sessionUrl = null
    this.error = null
    this.callbacks = []
  }

  async initialize() {
    try {
      this.sessionUrl = await FS('getSessionAsync')
      this.status = 'ready'
      this.callbacks.forEach((cb) => cb(this.sessionUrl))
    } catch (error) {
      this.status = 'failed'
      this.error = error
    }

    return this.status === 'ready'
  }

  onReady(callback) {
    if (this.status === 'ready') {
      callback(this.sessionUrl)
    } else if (this.status === 'pending') {
      this.callbacks.push(callback)
    }
    // If failed, don't call
  }

  isReady() {
    return this.status === 'ready'
  }

  getSessionUrl() {
    return this.sessionUrl
  }
}

// Global instance
const fsStatus = new CaptureStatusManager()

// Initialize once
fsStatus.initialize()

// Use anywhere
fsStatus.onReady((url) => {
  console.log('FS ready with session:', url)
})
```

### Pattern 3: Analytics Queue with Fallback

```javascript
// Queue analytics calls with sync fallback
class AnalyticsQueue {
  constructor() {
    this.useAsync = true
    this.pending = []
  }

  async track(eventName, properties) {
    if (this.useAsync) {
      try {
        await FS('trackEventAsync', {
          name: eventName,
          properties,
        })
      } catch (error) {
        // Fall back to sync
        console.warn('Async tracking failed, using sync')
        this.useAsync = false
        FS('trackEvent', {name: eventName, properties})
      }
    } else {
      FS('trackEvent', {name: eventName, properties})
    }
  }

  async identify(uid, properties) {
    if (this.useAsync) {
      try {
        await FS('setIdentityAsync', {uid, properties})
      } catch (error) {
        this.useAsync = false
        FS('setIdentity', {uid, properties})
      }
    } else {
      FS('setIdentity', {uid, properties})
    }
  }
}
```

---

## WHEN TO USE ASYNC VS SYNC

### Use Async When:

| Scenario              | Why                               |
| --------------------- | --------------------------------- |
| Need session URL      | Must wait for URL to be available |
| Error handling needed | Need to know if call failed       |
| Sequential operations | Must ensure order of operations   |
| Conditional logic     | Need result to decide next action |
| Initialization checks | Need to know when FS is ready     |

### Use Sync (Fire-and-Forget) When:

| Scenario                   | Why                         |
| -------------------------- | --------------------------- |
| Simple event tracking      | Don't need confirmation     |
| Non-critical operations    | Failure is acceptable       |
| Performance critical paths | Don't want to add latency   |
| Rapid-fire events          | Queueing handles order      |
| User-facing actions        | Don't delay user experience |

---

## TROUBLESHOOTING

### Promise Never Resolves

**Symptom**: `await FS('methodAsync')` hangs forever

**Common Causes**:

1. ❌ Fullstory script blocked by ad blocker
2. ❌ Script failed to load
3. ❌ Network issues preventing initialization

**Solutions**:

- ✅ Always use timeout wrapper
- ✅ Don't block critical paths
- ✅ Implement fallback behavior

### Rejection Errors

**Symptom**: Promise rejects with error

**Common Causes**:

1. ❌ Missing `_fs_org` configuration
2. ❌ Unsupported browser
3. ❌ Organization over quota
4. ❌ Configuration error

**Solutions**:

- ✅ Check Fullstory setup
- ✅ Verify configuration
- ✅ Handle rejections gracefully

### .catch() Not Working

**Symptom**: Errors not caught by `.catch()`

**Common Causes**:

1. ❌ Browser doesn't have native Promise
2. ❌ Fullstory's Promise-like doesn't implement catch

**Solutions**:

- ✅ Use async/await with try/catch
- ✅ Use `.then()` with error callback

---

## KEY TAKEAWAYS FOR AGENT

When helping developers with Async Methods:

1. **Always emphasize**:
   - Use timeouts to prevent hanging
   - Handle rejections gracefully
   - Don't block critical paths on FS
   - Use try/catch, not .catch()

2. **Common mistakes to watch for**:
   - Blocking app startup on FS
   - Missing error handling
   - Using async when sync would work
   - Race conditions between calls
   - .catch() without polyfill check

3. **Questions to ask developers**:
   - Do you need the result?
   - Is this on a critical path?
   - What should happen if FS fails?
   - Is proper sequencing required?

4. **Best practices to recommend**:
   - Wrap in timeout for safety
   - Use sync for fire-and-forget
   - Graceful degradation always
   - Don't let analytics break core features

---

## REFERENCE LINKS

- **Asynchronous Methods**: https://developer.fullstory.com/browser/asynchronous-methods/
- **Get Session Details**: https://developer.fullstory.com/browser/get-session-details/
- **Callbacks and Delegates**: https://developer.fullstory.com/browser/fullcapture/callbacks-and-delegates/

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's Asynchronous Methods correctly for web applications._
