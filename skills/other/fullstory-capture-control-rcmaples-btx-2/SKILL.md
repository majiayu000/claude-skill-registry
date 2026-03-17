---
name: fullstory-capture-control
version: v2
description: Comprehensive guide for implementing Fullstory's Capture Control APIs (shutdown/restart) for web applications. Teaches proper session management, capture pausing, and resource optimization. Includes detailed good/bad examples for performance-sensitive sections, privacy zones, and SPA cleanup to help developers control when Fullstory captures sessions.
related_skills:
  - fullstory-user-consent
  - fullstory-async-methods
  - fullstory-identify-users
  - fullstory-observe-callbacks
---

# Fullstory Capture Control API (Shutdown/Restart)

## Overview

Fullstory's Capture Control APIs allow developers to programmatically stop and restart session capture. This provides fine-grained control over when Fullstory records sessions, which is useful for:

- **Performance Optimization**: Pause capture during resource-intensive operations
- **Privacy Zones**: Stop capture in sensitive areas (PII entry, etc.)
- **Resource Management**: Reduce browser overhead when not needed
- **Testing**: Control capture during development/testing
- **Conditional Recording**: Only capture certain user journeys

## Core Concepts

### Shutdown vs Restart

| Method           | Effect                        | Use Case                                 |
| ---------------- | ----------------------------- | ---------------------------------------- |
| `FS('shutdown')` | Stops capture, clears session | End recording permanently or temporarily |
| `FS('restart')`  | Resumes capture, new session  | Resume after shutdown                    |

### Session Behavior

```
Active Session  →  FS('shutdown')  →  Capture Stopped (session ends)
                                              ↓
                                    FS('restart')
                                              ↓
                                    New Session Begins
```

### Key Points

| Behavior                   | Description                                                |
| -------------------------- | ---------------------------------------------------------- |
| **New session on restart** | Restart creates a new session, not continues old one       |
| **Identity preserved**     | If identified before shutdown, re-identify after restart   |
| **Properties cleared**     | Page/element properties reset on restart                   |
| **Async available**        | Both have async versions (`shutdownAsync`, `restartAsync`) |

---

## API Reference

### Shutdown

```javascript
// Stop capture
FS('shutdown')

// Async version
await FS('shutdownAsync')
```

### Restart

```javascript
// Resume capture (starts new session)
FS('restart')

// Async version
await FS('restartAsync')
```

### Parameters

Both methods take no parameters.

### Return Values

| Method           | Sync Return | Async Return                    |
| ---------------- | ----------- | ------------------------------- |
| `FS('shutdown')` | undefined   | Promise (resolves when stopped) |
| `FS('restart')`  | undefined   | Promise (resolves when started) |

---

## ✅ GOOD IMPLEMENTATION EXAMPLES

### Example 1: Pause During Heavy Operations

```javascript
// GOOD: Pause capture during performance-intensive operations
async function processLargeDataset(data) {
  // Pause Fullstory to free up resources
  await FS('shutdownAsync')

  console.log('Fullstory paused for data processing')

  try {
    // Perform heavy operation
    const result = await heavyProcessing(data)

    return result
  } finally {
    // Always restart, even if processing fails
    await FS('restartAsync')

    // Re-identify user (identity lost on restart)
    const user = getCurrentUser()
    if (user) {
      FS('setIdentity', {
        uid: user.id,
        properties: {
          displayName: user.name,
        },
      })
    }

    console.log('Fullstory resumed')
  }
}

// Usage
const results = await processLargeDataset(largeDataset)
```

**Why this is good:**

- ✅ Frees up resources during heavy processing
- ✅ Uses try/finally to ensure restart
- ✅ Re-identifies user after restart
- ✅ Logs state changes for debugging

### Example 2: Privacy Zone Implementation

```javascript
// GOOD: Stop capture in sensitive areas
class PrivacyZoneManager {
  constructor() {
    this.isInPrivacyZone = false
    this.userBeforeShutdown = null
  }

  async enterPrivacyZone(zoneName) {
    if (this.isInPrivacyZone) return

    // Store current user for re-identification later
    this.userBeforeShutdown = getCurrentUser()

    // Log entry before shutdown
    FS('log', {
      level: 'info',
      msg: `Entering privacy zone: ${zoneName}`,
    })

    // Track the transition
    FS('trackEvent', {
      name: 'Privacy Zone Entered',
      properties: {zone: zoneName},
    })

    // Shutdown capture
    await FS('shutdownAsync')
    this.isInPrivacyZone = true

    console.log(`Entered privacy zone: ${zoneName}`)
  }

  async exitPrivacyZone(zoneName) {
    if (!this.isInPrivacyZone) return

    // Restart capture
    await FS('restartAsync')
    this.isInPrivacyZone = false

    // Re-identify user
    if (this.userBeforeShutdown) {
      FS('setIdentity', {
        uid: this.userBeforeShutdown.id,
        properties: {
          displayName: this.userBeforeShutdown.name,
          email: this.userBeforeShutdown.email,
        },
      })
    }

    // Track the transition
    FS('trackEvent', {
      name: 'Privacy Zone Exited',
      properties: {zone: zoneName},
    })

    // Log exit
    FS('log', {
      level: 'info',
      msg: `Exited privacy zone: ${zoneName}`,
    })

    this.userBeforeShutdown = null
    console.log(`Exited privacy zone: ${zoneName}`)
  }
}

// Usage
const privacyManager = new PrivacyZoneManager()

// When navigating to sensitive page
await privacyManager.enterPrivacyZone('account-settings')

// When leaving sensitive page
await privacyManager.exitPrivacyZone('account-settings')
```

**Why this is good:**

- ✅ Clean API for privacy zones
- ✅ Preserves user identity for re-identification
- ✅ Logs and tracks zone transitions
- ✅ State management prevents double calls

### Example 3: SPA Route-Based Control

```javascript
// GOOD: Control capture based on route in SPA
const routeConfig = {
  '/dashboard': {capture: true},
  '/settings': {capture: true},
  '/settings/security': {capture: false}, // Privacy zone
  '/admin': {capture: false}, // Internal only
  '/checkout': {capture: true},
  '/checkout/payment': {capture: false}, // PCI compliance
}

class RouteBasedCapture {
  constructor() {
    this.isCapturing = true // Assume capturing on start
    this.currentUser = null

    this.setupRouteListener()
  }

  setupRouteListener() {
    // For React Router, Vue Router, etc.
    window.addEventListener('popstate', () => this.handleRouteChange())

    // Intercept pushState
    const originalPushState = history.pushState
    history.pushState = (...args) => {
      originalPushState.apply(history, args)
      this.handleRouteChange()
    }
  }

  async handleRouteChange() {
    const path = window.location.pathname
    const config = this.getRouteConfig(path)

    if (config.capture && !this.isCapturing) {
      await this.startCapture()
    } else if (!config.capture && this.isCapturing) {
      await this.stopCapture()
    }

    // Set page properties if capturing
    if (this.isCapturing && config.pageName) {
      FS('setProperties', {
        type: 'page',
        properties: {pageName: config.pageName},
      })
    }
  }

  getRouteConfig(path) {
    // Find matching config (exact match or parent)
    for (const [route, config] of Object.entries(routeConfig)) {
      if (path === route || path.startsWith(route + '/')) {
        return config
      }
    }
    return {capture: true} // Default: capture
  }

  async startCapture() {
    await FS('restartAsync')
    this.isCapturing = true

    // Re-identify
    this.currentUser = this.currentUser || getCurrentUser()
    if (this.currentUser) {
      FS('setIdentity', {
        uid: this.currentUser.id,
        properties: {
          displayName: this.currentUser.name,
        },
      })
    }

    console.log('Fullstory capture started')
  }

  async stopCapture() {
    // Save user before shutdown
    this.currentUser = getCurrentUser()

    await FS('shutdownAsync')
    this.isCapturing = false

    console.log('Fullstory capture stopped')
  }

  setUser(user) {
    this.currentUser = user
  }
}

// Initialize
const captureController = new RouteBasedCapture()
```

**Why this is good:**

- ✅ Configurable per-route capture
- ✅ Handles SPA navigation
- ✅ Re-identifies on restart
- ✅ Preserves user across shutdown

### Example 4: Development/Testing Controls

```javascript
// GOOD: Control capture for testing and development
const DevCaptureControls = {
  isOverridden: false,

  // Disable capture for current session (dev/testing)
  disableForSession() {
    sessionStorage.setItem('fs_disabled', 'true')
    FS('shutdown')
    this.isOverridden = true
    console.log('Fullstory disabled for this session')
  },

  // Re-enable capture
  enableForSession() {
    sessionStorage.removeItem('fs_disabled')
    if (this.isOverridden) {
      FS('restart')
      this.isOverridden = false
      console.log('Fullstory re-enabled')
    }
  },

  // Check if should capture on page load
  init() {
    if (sessionStorage.getItem('fs_disabled') === 'true') {
      FS('shutdown')
      this.isOverridden = true
      console.log('Fullstory disabled (session override)')
    }

    // Also check URL param for easy testing
    if (new URLSearchParams(window.location.search).has('no_fullstory')) {
      this.disableForSession()
    }
  },

  // Add keyboard shortcut (Ctrl+Shift+F)
  setupKeyboardShortcut() {
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'F') {
        if (this.isOverridden) {
          this.enableForSession()
        } else {
          this.disableForSession()
        }
      }
    })
  },
}

// Initialize on page load
DevCaptureControls.init()
DevCaptureControls.setupKeyboardShortcut()

// Also expose for console access
window.DevCaptureControls = DevCaptureControls
```

**Why this is good:**

- ✅ Easy toggle for developers
- ✅ Session-persistent disable
- ✅ URL parameter support
- ✅ Keyboard shortcut for quick toggle
- ✅ Console access for debugging

### Example 5: Conditional Capture Based on User State

```javascript
// GOOD: Only capture for specific user segments
class ConditionalCapture {
  constructor(captureRules) {
    this.rules = captureRules
    this.isCapturing = false
  }

  async evaluateAndUpdate(user) {
    const shouldCapture = this.shouldCaptureUser(user)

    if (shouldCapture && !this.isCapturing) {
      await this.startCapture(user)
    } else if (!shouldCapture && this.isCapturing) {
      await this.stopCapture()
    } else if (shouldCapture && this.isCapturing) {
      // Just update identity
      this.identifyUser(user)
    }
  }

  shouldCaptureUser(user) {
    // Evaluate rules
    for (const rule of this.rules) {
      if (!rule.check(user)) {
        console.log(`Capture blocked by rule: ${rule.name}`)
        return false
      }
    }
    return true
  }

  async startCapture(user) {
    await FS('restartAsync')
    this.isCapturing = true
    this.identifyUser(user)

    FS('log', {
      level: 'info',
      msg: `Capture started for user: ${user.id}`,
    })
  }

  async stopCapture() {
    await FS('shutdownAsync')
    this.isCapturing = false

    console.log('Capture stopped based on rules')
  }

  identifyUser(user) {
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        plan: user.plan,
        role: user.role,
      },
    })
  }
}

// Example rules
const captureRules = [
  {
    name: 'not_internal',
    check: (user) => !user.email.endsWith('@ourcompany.com'),
  },
  {
    name: 'not_bot',
    check: (user) => !user.isBot,
  },
  {
    name: 'has_consent',
    check: (user) => user.trackingConsent === true,
  },
  {
    name: 'paying_customer',
    check: (user) => user.plan !== 'free', // Only capture paid users
  },
]

const conditionalCapture = new ConditionalCapture(captureRules)

// On user load/change
authService.on('userChanged', (user) => {
  conditionalCapture.evaluateAndUpdate(user)
})
```

**Why this is good:**

- ✅ Configurable capture rules
- ✅ Filters out internal/bot traffic
- ✅ Respects consent
- ✅ Can segment by plan/role
- ✅ Logs why capture is blocked

### Example 6: Cleanup on Page Unload

```javascript
// GOOD: Clean shutdown on page unload
class CaptureLifecycleManager {
  constructor() {
    this.setupUnloadHandler()
    this.setupVisibilityHandler()
  }

  setupUnloadHandler() {
    window.addEventListener('beforeunload', () => {
      // Use sync version - async may not complete
      FS('shutdown')
    })
  }

  setupVisibilityHandler() {
    // Optional: pause when tab is hidden (saves resources)
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        // User switched tabs - could pause
        // FS('shutdown');  // Uncomment if you want this behavior
      } else {
        // User returned - could resume
        // FS('restart');  // Uncomment if pausing on hidden
      }
    })
  }

  // For SPAs: call when app unmounts
  cleanup() {
    FS('shutdown')
  }
}

// Initialize
const fsLifecycle = new CaptureLifecycleManager()

// For React apps
// useEffect(() => {
//   return () => fsLifecycle.cleanup();
// }, []);
```

**Why this is good:**

- ✅ Clean session end on page close
- ✅ Optional tab visibility handling
- ✅ SPA cleanup method
- ✅ Uses sync version for beforeunload

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Not Re-identifying After Restart

```javascript
// BAD: Forgot to re-identify after restart
async function pauseAndResume() {
  await FS('shutdownAsync')

  // ... do work ...

  await FS('restartAsync')
  // BAD: User is now anonymous! Identity was lost on shutdown
}
```

**Why this is bad:**

- ❌ Identity lost on shutdown
- ❌ New session is anonymous
- ❌ Can't link sessions together

**CORRECTED VERSION:**

```javascript
// GOOD: Re-identify after restart
async function pauseAndResume() {
  const user = getCurrentUser() // Save before shutdown

  await FS('shutdownAsync')

  // ... do work ...

  await FS('restartAsync')

  // Re-identify
  if (user) {
    FS('setIdentity', {
      uid: user.id,
      properties: {displayName: user.name},
    })
  }
}
```

### Example 2: Using Shutdown for Consent (Wrong API)

```javascript
// BAD: Using shutdown instead of consent API
function handleConsentDeclined() {
  FS('shutdown') // BAD: Wrong approach for consent
}

function handleConsentGranted() {
  FS('restart') // BAD: Should use consent API
}
```

**Why this is bad:**

- ❌ shutdown/restart not designed for consent
- ❌ Doesn't properly signal consent state
- ❌ Consent API exists for this purpose

**CORRECTED VERSION:**

```javascript
// GOOD: Use consent API for consent
function handleConsentDeclined() {
  FS('setIdentity', {consent: false})
}

function handleConsentGranted() {
  FS('setIdentity', {consent: true})
}
```

### Example 3: Shutdown Without Restart Logic

```javascript
// BAD: Shutdown with no way to restart
function handleSensitiveArea() {
  FS('shutdown')
  // No mechanism to restart when leaving sensitive area!
}
```

**Why this is bad:**

- ❌ Capture permanently stopped
- ❌ No way to resume
- ❌ Loses rest of session

**CORRECTED VERSION:**

```javascript
// GOOD: Paired shutdown/restart
let isShutdown = false

function enterSensitiveArea() {
  if (!isShutdown) {
    FS('shutdown')
    isShutdown = true
  }
}

function leaveSensitiveArea() {
  if (isShutdown) {
    FS('restart')
    isShutdown = false
    // Re-identify user
    reidentifyUser()
  }
}
```

### Example 4: Async Version in beforeunload

```javascript
// BAD: Using async in beforeunload (won't complete)
window.addEventListener('beforeunload', async () => {
  await FS('shutdownAsync') // BAD: Won't complete before page unloads
})
```

**Why this is bad:**

- ❌ Async code may not complete before unload
- ❌ Session may not end cleanly
- ❌ beforeunload doesn't wait for promises

**CORRECTED VERSION:**

```javascript
// GOOD: Use sync version in beforeunload
window.addEventListener('beforeunload', () => {
  FS('shutdown') // Sync version - fires immediately
})
```

### Example 5: Rapid Shutdown/Restart Cycles

```javascript
// BAD: Toggling too rapidly
document.addEventListener('scroll', () => {
  if (isInSensitiveArea()) {
    FS('shutdown') // Called on every scroll event!
  } else {
    FS('restart') // Creates new session every scroll!
  }
})
```

**Why this is bad:**

- ❌ Excessive API calls
- ❌ Creates many fragmented sessions
- ❌ Performance impact
- ❌ Data loss from constant restarts

**CORRECTED VERSION:**

```javascript
// GOOD: Debounced state changes
let isCapturing = true

const updateCaptureState = debounce(() => {
  const shouldCapture = !isInSensitiveArea()

  if (shouldCapture && !isCapturing) {
    FS('restart')
    reidentifyUser()
    isCapturing = true
  } else if (!shouldCapture && isCapturing) {
    FS('shutdown')
    isCapturing = false
  }
}, 500)

document.addEventListener('scroll', updateCaptureState)
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Capture Controller Singleton

```javascript
// Singleton for capture state management
const CaptureController = {
  _isCapturing: true,
  _user: null,

  isCapturing() {
    return this._isCapturing
  },

  setUser(user) {
    this._user = user
  },

  async pause(reason = 'unspecified') {
    if (!this._isCapturing) return

    // Log before shutdown
    FS('log', {
      level: 'info',
      msg: `Capture paused: ${reason}`,
    })

    await FS('shutdownAsync')
    this._isCapturing = false

    console.log(`FS capture paused: ${reason}`)
  },

  async resume(reason = 'unspecified') {
    if (this._isCapturing) return

    await FS('restartAsync')
    this._isCapturing = true

    // Re-identify
    if (this._user) {
      FS('setIdentity', {
        uid: this._user.id,
        properties: {
          displayName: this._user.name,
        },
      })
    }

    // Log after restart
    FS('log', {
      level: 'info',
      msg: `Capture resumed: ${reason}`,
    })

    console.log(`FS capture resumed: ${reason}`)
  },
}

// Usage
await CaptureController.pause('entering-payment-form')
await CaptureController.resume('leaving-payment-form')
```

### Pattern 2: React Hook for Capture Control

```jsx
// React hook for capture control
import {useEffect, useRef, useCallback} from 'react'

function useCaptureControl() {
  const isCapturingRef = useRef(true)
  const userRef = useRef(null)

  const setUser = useCallback((user) => {
    userRef.current = user
  }, [])

  const pause = useCallback(async () => {
    if (!isCapturingRef.current) return

    await FS('shutdownAsync')
    isCapturingRef.current = false
  }, [])

  const resume = useCallback(async () => {
    if (isCapturingRef.current) return

    await FS('restartAsync')
    isCapturingRef.current = true

    if (userRef.current) {
      FS('setIdentity', {
        uid: userRef.current.id,
        properties: {displayName: userRef.current.name},
      })
    }
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      FS('shutdown')
    }
  }, [])

  return {pause, resume, setUser}
}

// Privacy zone component
function PrivacyZone({children}) {
  const {pause, resume} = useCaptureControl()

  useEffect(() => {
    pause()
    return () => resume()
  }, [pause, resume])

  return children
}

// Usage
function PaymentForm() {
  return (
    <PrivacyZone>
      <form>
        {/* Capture is paused within this component */}
        <CreditCardInput />
      </form>
    </PrivacyZone>
  )
}
```

---

## TROUBLESHOOTING

### Sessions Not Resuming

**Symptom**: After restart, no new session created

**Common Causes**:

1. ❌ Fullstory blocked by ad blocker
2. ❌ Page excluded from capture
3. ❌ Rate limits hit

**Solutions**:

- ✅ Check browser console for errors
- ✅ Verify page isn't excluded
- ✅ Add delay between shutdown/restart

### Identity Lost After Restart

**Symptom**: User is anonymous after restart

**Common Causes**:

1. ❌ Forgot to re-identify
2. ❌ User data not saved before shutdown

**Solutions**:

- ✅ Always re-identify after restart
- ✅ Save user data before shutdown

### Fragmented Sessions

**Symptom**: Many short sessions for same user

**Common Causes**:

1. ❌ Too many restart calls
2. ❌ Shutdown/restart in rapid succession
3. ❌ Missing debounce

**Solutions**:

- ✅ Minimize shutdown/restart cycles
- ✅ Add debouncing
- ✅ Use state tracking

---

## KEY TAKEAWAYS FOR AGENT

When helping developers with Capture Control:

1. **Always emphasize**:
   - Re-identify after restart (identity is lost)
   - Use sync version in beforeunload
   - Debounce rapid state changes
   - Use consent API for consent, not shutdown

2. **Common mistakes to watch for**:
   - Forgetting to re-identify
   - Using shutdown for consent
   - Async in beforeunload
   - Rapid shutdown/restart cycles
   - No restart logic after shutdown

3. **Questions to ask developers**:
   - Why do you need to pause capture?
   - Is this for privacy/consent or performance?
   - How will users resume capture?
   - Do you need to preserve user identity?

4. **Best practices to recommend**:
   - Use consent API for consent management
   - Create paired enter/exit for privacy zones
   - Always save user before shutdown
   - Debounce state transitions

---

## REFERENCE LINKS

- **Capture Data**: https://developer.fullstory.com/browser/fullcapture/capture-data/
- **Asynchronous Methods**: https://developer.fullstory.com/browser/asynchronous-methods/

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's Capture Control APIs correctly for web applications._
