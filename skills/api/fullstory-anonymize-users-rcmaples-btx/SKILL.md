---
name: fullstory-anonymize-users
version: v2
description: Comprehensive guide for implementing Fullstory's User Anonymization API (setIdentity with anonymous:true) for web applications. Teaches proper logout handling, session management, privacy compliance, and user switching scenarios. Includes detailed good/bad examples for logout flows, multi-user applications, and privacy-conscious implementations.
related_skills:
  - fullstory-identify-users
  - fullstory-user-consent
  - fullstory-capture-control
  - fullstory-async-methods
---

# Fullstory Anonymize Users API

## Overview

Fullstory's Anonymize Users API allows developers to release the identity of the current user and create a new anonymous session. This is essential for:

- **User Logout**: Properly ending an identified session when a user logs out
- **Account Switching**: Allowing users to switch between accounts cleanly
- **Privacy Compliance**: Implementing "forget me" or privacy-conscious features
- **Shared Devices**: Ensuring one user's session doesn't bleed into another's

When you call `FS('setIdentity', { anonymous: true })`, the current session ends and a fresh anonymous session begins. The previously identified user remains in Fullstory's records, but subsequent activity is no longer linked to them.

## Core Concepts

### What Happens When You Anonymize

1. **Current session is closed** and marked as belonging to the identified user
2. **A new `fs_uid` cookie is generated** - breaking the link to all previous sessions
3. **New anonymous session begins** with a new session ID and new cookie
4. **Previous user data is preserved** - anonymizing doesn't delete history
5. **Subsequent activity is anonymous** until a new `setIdentity` call

> **Cookie Behavior**: Normally, the `fs_uid` first-party cookie (1-year expiry) links all sessions from the same browser together. When `anonymize` is called, Fullstory generates a **new** `fs_uid` cookie, effectively creating a "new device" from Fullstory's perspective. Any future `setIdentity` calls will only merge sessions from the new cookie, not the old one.
>
> **Reference**: [Why Fullstory uses First-Party Cookies](https://help.fullstory.com/hc/en-us/articles/360020829513-Why-Fullstory-uses-First-Party-Cookies)

### Session Lifecycle

```
┌─────────────┐  Login   ┌─────────────┐  Logout  ┌─────────────┐
│  Anonymous  │ ───────► │ Identified  │ ───────► │ New Anon    │
│  Session A  │          │  Session B  │          │  Session C  │
└─────────────┘          └─────────────┘          └─────────────┘
                              │
              setIdentity     │    setIdentity
              (uid: 'xxx')    │    (anonymous: true)
```

### When to Anonymize

| Scenario                    | Should Anonymize? | Reason                                     |
| --------------------------- | ----------------- | ------------------------------------------ |
| User logs out               | ✅ Yes            | Prevents session attribution to wrong user |
| User switches accounts      | ✅ Yes            | Clean slate before new identification      |
| User requests data deletion | ❓ Consider       | Part of broader privacy implementation     |
| User clears browser data    | ❌ No             | Fullstory handles this automatically       |
| Page navigation             | ❌ No             | Identity persists across pages             |
| Session timeout             | ❓ Depends        | Based on your security requirements        |

---

## API Reference

### Basic Syntax

```javascript
FS('setIdentity', {anonymous: true})
```

### Parameters

| Parameter   | Type    | Required | Description                          |
| ----------- | ------- | -------- | ------------------------------------ |
| `anonymous` | boolean | **Yes**  | Must be `true` to anonymize the user |

### Rate Limits

- **Sustained**: 30 calls per page per minute
- **Burst**: 10 calls per second

### Async Version

```javascript
await FS('setIdentityAsync', {anonymous: true})
```

---

## ✅ GOOD IMPLEMENTATION EXAMPLES

### Example 1: Basic Logout Handler

```javascript
// GOOD: Proper logout with Fullstory anonymization
async function handleLogout() {
  try {
    // 1. Call your backend logout endpoint
    await fetch('/api/auth/logout', {method: 'POST'})

    // 2. Clear local authentication state
    clearAuthTokens()
    clearUserState()

    // 3. Anonymize in Fullstory BEFORE redirecting
    FS('setIdentity', {anonymous: true})

    // 4. Redirect to login page
    window.location.href = '/login'
  } catch (error) {
    console.error('Logout failed:', error)
    // Still anonymize even if backend fails
    FS('setIdentity', {anonymous: true})
    window.location.href = '/login'
  }
}
```

**Why this is good:**

- ✅ Anonymizes before redirect
- ✅ Handles errors gracefully
- ✅ Clears local state before anonymizing
- ✅ Ensures next user won't be associated with previous user

### Example 2: React Logout with Auth Context

```jsx
// GOOD: React hook pattern for logout with Fullstory
import {useCallback} from 'react'
import {useAuth} from './auth-context'
import {useNavigate} from 'react-router-dom'

function useLogout() {
  const {clearAuth} = useAuth()
  const navigate = useNavigate()

  const logout = useCallback(async () => {
    // Track the logout action before anonymizing
    FS('trackEvent', {
      name: 'User Logged Out',
      properties: {
        logoutMethod: 'manual',
        sessionDuration: getSessionDuration(),
      },
    })

    // Clear application auth state
    await clearAuth()

    // Anonymize the Fullstory session
    FS('setIdentity', {anonymous: true})

    // Navigate to home/login
    navigate('/login')
  }, [clearAuth, navigate])

  return logout
}

// Usage
function LogoutButton() {
  const logout = useLogout()
  return <button onClick={logout}>Sign Out</button>
}
```

**Why this is good:**

- ✅ Tracks logout event before anonymizing (preserves attribution)
- ✅ Integrated with React ecosystem
- ✅ Reusable across components
- ✅ Clean navigation after logout

### Example 3: Account Switching

```javascript
// GOOD: Clean account switching with proper session boundaries
async function switchAccount(newAccountId) {
  const newUser = await fetchAccountDetails(newAccountId)

  // Track the switch event under current user
  FS('trackEvent', {
    name: 'Account Switch Initiated',
    properties: {
      targetAccountId: newAccountId,
    },
  })

  // Step 1: Anonymize current session
  FS('setIdentity', {anonymous: true})

  // Step 2: Set up new account context
  await setupAccountContext(newUser)

  // Step 3: Identify as new user
  FS('setIdentity', {
    uid: newUser.id,
    properties: {
      displayName: newUser.name,
      email: newUser.email,
      accountType: newUser.type,
    },
  })

  // Refresh UI
  window.location.reload()
}
```

**Why this is good:**

- ✅ Tracks event before identity change
- ✅ Cleanly separates sessions between accounts
- ✅ No data contamination between accounts
- ✅ New user gets fresh identification

### Example 4: Session Timeout Handler

```javascript
// GOOD: Handling session timeout with Fullstory
class SessionManager {
  constructor() {
    this.timeoutDuration = 30 * 60 * 1000 // 30 minutes
    this.timeoutId = null
    this.lastActivity = Date.now()
  }

  startTimeout() {
    this.resetTimeout()
    document.addEventListener('click', () => this.resetTimeout())
    document.addEventListener('keypress', () => this.resetTimeout())
  }

  resetTimeout() {
    this.lastActivity = Date.now()
    if (this.timeoutId) clearTimeout(this.timeoutId)

    this.timeoutId = setTimeout(() => {
      this.handleSessionTimeout()
    }, this.timeoutDuration)
  }

  async handleSessionTimeout() {
    // Track timeout event while still identified
    FS('trackEvent', {
      name: 'Session Timeout',
      properties: {
        inactivityDuration: Date.now() - this.lastActivity,
        lastPage: window.location.pathname,
      },
    })

    // Anonymize the session
    FS('setIdentity', {anonymous: true})

    // Clear auth and redirect
    clearAuthState()
    showTimeoutModal()
  }
}
```

**Why this is good:**

- ✅ Tracks timeout before anonymizing
- ✅ Captures useful debugging info
- ✅ Clean session boundary on timeout
- ✅ User feedback via modal

### Example 5: Privacy-Conscious Implementation

```javascript
// GOOD: "Incognito mode" toggle for privacy-conscious users
class PrivacyManager {
  constructor() {
    this.isIncognitoMode = false
    this.originalUserId = null
  }

  async enableIncognitoMode(currentUserId) {
    // Store original user ID for potential re-identification
    this.originalUserId = currentUserId
    this.isIncognitoMode = true

    // Track before anonymizing
    FS('trackEvent', {
      name: 'Incognito Mode Enabled',
      properties: {},
    })

    // Anonymize - activity won't be linked to user
    FS('setIdentity', {anonymous: true})

    // Update UI
    showIncognitoIndicator()
  }

  async disableIncognitoMode() {
    if (!this.originalUserId) return

    this.isIncognitoMode = false

    // Re-identify user
    const user = await getCurrentUser()
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email,
      },
    })

    // Track re-enablement
    FS('trackEvent', {
      name: 'Incognito Mode Disabled',
      properties: {},
    })

    hideIncognitoIndicator()
    this.originalUserId = null
  }
}
```

**Why this is good:**

- ✅ Gives users control over tracking
- ✅ Maintains ability to re-identify
- ✅ Clear user feedback
- ✅ Events tracked at session boundaries

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Forgetting to Anonymize on Logout

```javascript
// BAD: No Fullstory anonymization on logout
function handleLogout() {
  clearAuthTokens()
  clearUserState()
  window.location.href = '/login'
  // Missing FS('setIdentity', { anonymous: true })!
}
```

**Why this is bad:**

- ❌ Next user's activity may be attributed to previous user
- ❌ Session continues under wrong identity
- ❌ Data integrity issues in analytics
- ❌ Privacy concern if sharing device

**CORRECTED VERSION:**

```javascript
// GOOD: Include Fullstory anonymization
function handleLogout() {
  clearAuthTokens()
  clearUserState()

  // Anonymize before redirect
  FS('setIdentity', {anonymous: true})

  window.location.href = '/login'
}
```

### Example 2: Anonymizing After Redirect

```javascript
// BAD: Anonymizing after navigation starts
function handleLogout() {
  window.location.href = '/login'

  // BAD: This may never execute - page is already navigating!
  FS('setIdentity', {anonymous: true})
}
```

**Why this is bad:**

- ❌ Navigation starts before anonymization
- ❌ FS call may not complete
- ❌ Session may not properly close

**CORRECTED VERSION:**

```javascript
// GOOD: Anonymize BEFORE navigation
async function handleLogout() {
  // Anonymize first
  await FS('setIdentityAsync', {anonymous: true})

  // Then navigate
  window.location.href = '/login'
}
```

### Example 3: Anonymizing Repeatedly

```javascript
// BAD: Calling anonymize multiple times
function handleLogout() {
  // Excessive calls
  FS('setIdentity', {anonymous: true})
  FS('setIdentity', {anonymous: true})
  FS('setIdentity', {anonymous: true})

  window.location.href = '/login'
}
```

**Why this is bad:**

- ❌ Wastes API call quota
- ❌ Creates unnecessary session splits
- ❌ May hit rate limits
- ❌ No benefit from multiple calls

**CORRECTED VERSION:**

```javascript
// GOOD: Single anonymization call
function handleLogout() {
  FS('setIdentity', {anonymous: true})
  window.location.href = '/login'
}
```

### Example 4: Using Wrong Parameter

```javascript
// BAD: Wrong way to anonymize
FS('setIdentity', {uid: null}) // BAD: uid shouldn't be null
FS('setIdentity', {uid: 'anonymous'}) // BAD: This identifies as user "anonymous"!
FS('setIdentity', {uid: ''}) // BAD: Empty string uid
FS('setIdentity', {}) // BAD: Missing required parameters
```

**Why this is bad:**

- ❌ uid: null may cause errors
- ❌ uid: 'anonymous' creates an identified user named "anonymous"
- ❌ Empty string uid is invalid
- ❌ Empty object doesn't anonymize

**CORRECTED VERSION:**

```javascript
// GOOD: Proper anonymization syntax
FS('setIdentity', {anonymous: true})
```

### Example 5: Anonymizing Without Tracking Important Events

```javascript
// BAD: Missing opportunity to track logout event
function handleLogout() {
  // Just anonymizing without capturing useful data
  FS('setIdentity', {anonymous: true})
  window.location.href = '/login'
}
```

**Why this is bad:**

- ❌ No record of intentional logout vs session timeout
- ❌ Can't analyze logout patterns
- ❌ Loses attribution for the logout event itself

**CORRECTED VERSION:**

```javascript
// GOOD: Track event before anonymizing
function handleLogout() {
  // Track while still identified
  FS('trackEvent', {
    name: 'User Logged Out',
    properties: {
      logoutMethod: 'user_initiated',
      pageAtLogout: window.location.pathname,
    },
  })

  // Then anonymize
  FS('setIdentity', {anonymous: true})
  window.location.href = '/login'
}
```

### Example 6: Anonymizing During Errors Instead of Proper Handling

```javascript
// BAD: Using anonymization to "hide" errors
function handleError(error) {
  // Don't use anonymization to hide error attribution!
  FS('setIdentity', {anonymous: true})
  console.error(error)
}
```

**Why this is bad:**

- ❌ Loses error attribution to user for debugging
- ❌ Makes it harder to help affected users
- ❌ Misuse of anonymization API
- ❌ Creates confusing session boundaries

**CORRECTED VERSION:**

```javascript
// GOOD: Log errors while identified, only anonymize on logout
function handleError(error) {
  // Track the error - attribution helps debugging!
  FS('trackEvent', {
    name: 'Application Error',
    properties: {
      errorMessage: error.message,
      errorCode: error.code,
      page: window.location.pathname,
    },
  })

  // Show error UI without anonymizing
  showErrorMessage(error)
}
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Logout Service

```javascript
// Centralized logout service
class LogoutService {
  static async logout(options = {}) {
    const {trackEvent = true, redirectUrl = '/login', reason = 'user_initiated'} = options

    // Track logout if requested
    if (trackEvent) {
      FS('trackEvent', {
        name: 'User Logged Out',
        properties: {
          reason: reason,
          sessionDuration: getSessionDuration(),
        },
      })
    }

    // Backend logout
    try {
      await fetch('/api/logout', {method: 'POST'})
    } catch (e) {
      console.warn('Backend logout failed:', e)
    }

    // Clear client state
    clearAuthTokens()
    clearUserState()
    clearLocalStorage()

    // Anonymize Fullstory
    FS('setIdentity', {anonymous: true})

    // Redirect
    if (redirectUrl) {
      window.location.href = redirectUrl
    }
  }
}

// Usage
await LogoutService.logout()
await LogoutService.logout({reason: 'session_timeout', redirectUrl: '/timeout'})
```

### Pattern 2: Multi-Tenant Application

```javascript
// For apps with workspace/tenant switching
class TenantManager {
  async switchTenant(newTenantId) {
    const currentUser = getCurrentUser()

    // Track switch under current context
    FS('trackEvent', {
      name: 'Tenant Switch',
      properties: {
        fromTenant: currentUser.tenantId,
        toTenant: newTenantId,
      },
    })

    // Start fresh session for new tenant context
    FS('setIdentity', {anonymous: true})

    // Update tenant context
    await loadTenantContext(newTenantId)

    // Re-identify with new tenant context
    FS('setIdentity', {
      uid: currentUser.id,
      properties: {
        displayName: currentUser.name,
        email: currentUser.email,
        tenantId: newTenantId,
        tenantName: await getTenantName(newTenantId),
      },
    })
  }
}
```

### Pattern 3: Kiosk/Shared Device Mode

```javascript
// For shared devices like kiosks
class KioskMode {
  sessionTimeout = 5 * 60 * 1000 // 5 minutes

  async startSession(user) {
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        deviceMode: 'kiosk',
        locationId: getKioskLocation(),
      },
    })

    // Auto-logout after timeout
    setTimeout(() => this.endSession(), this.sessionTimeout)
  }

  async endSession() {
    FS('trackEvent', {
      name: 'Kiosk Session Ended',
      properties: {
        endReason: 'timeout',
        location: getKioskLocation(),
      },
    })

    FS('setIdentity', {anonymous: true})

    // Reset to welcome screen
    showWelcomeScreen()
  }
}
```

---

## RELATIONSHIP WITH OTHER FS APIs

### Anonymize vs setProperties

```javascript
// setProperties updates user info without changing identity
FS('setProperties', {
  type: 'user',
  properties: {lastActiveAt: new Date().toISOString()},
})

// anonymous: true ends the session entirely
FS('setIdentity', {anonymous: true}) // New session starts
```

### Anonymize + Re-identify Flow

```javascript
// Common pattern: switch users
FS('setIdentity', {anonymous: true}) // End session 1

// Some time passes, new user logs in

FS('setIdentity', {
  // Start session 2
  uid: newUser.id,
  properties: {displayName: newUser.name},
})
```

---

## TROUBLESHOOTING

### Session Not Properly Ending

**Symptom**: New user activity appears under old user

**Common Causes**:

1. ❌ Anonymize called after page navigation starts
2. ❌ Anonymize never called (missing from logout flow)
3. ❌ Using wrong syntax (uid: null instead of anonymous: true)

**Solutions**:

- ✅ Use async version and await completion
- ✅ Audit all logout paths to ensure anonymization
- ✅ Use `{ anonymous: true }` syntax

### Too Many Session Splits

**Symptom**: User has many short, fragmented sessions

**Common Causes**:

1. ❌ Calling anonymize on every page load
2. ❌ Calling anonymize on errors
3. ❌ Multiple anonymize calls in single flow

**Solutions**:

- ✅ Only anonymize on actual logout/switch events
- ✅ Audit code for unintended anonymize calls
- ✅ Use single anonymize call per logout flow

---

## LIMITS AND CONSTRAINTS

### Call Frequency

- **Sustained**: 30 calls per page per minute
- **Burst**: 10 calls per second
- Single call per logout is sufficient

### Session Behavior

- Anonymization creates a new session immediately
- Previous session data remains intact and attributed
- Subsequent activity is anonymous until next identification

---

## KEY TAKEAWAYS FOR AGENT

When helping developers implement User Anonymization:

1. **Always emphasize**:
   - Anonymize BEFORE navigation/redirects
   - Use `{ anonymous: true }` syntax exactly
   - Track important events BEFORE anonymizing
   - Single call per logout is sufficient

2. **Common mistakes to watch for**:
   - Forgetting to anonymize on logout
   - Anonymizing after redirect starts
   - Using wrong syntax (uid: null, uid: 'anonymous')
   - Over-calling anonymize
   - Missing trackEvent before anonymize

3. **Questions to ask developers**:
   - What are all the logout/signout paths in your app?
   - Do users switch between accounts?
   - Is this a shared device scenario?
   - What events should be tracked before logout?

4. **Integration considerations**:
   - Must anonymize in all logout paths
   - Consider session timeout handling
   - Account switching needs anonymize between identifications
   - Order matters: track events → anonymize → redirect

---

## REFERENCE LINKS

- **Anonymize Users**: https://developer.fullstory.com/browser/identification/anonymize-users/
- **Identify Users**: https://developer.fullstory.com/browser/identification/identify-users/
- **Help Center - Anonymizing**: https://help.fullstory.com/hc/en-us/articles/360020623514-Anonymizing-Users

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's User Anonymization API correctly for web applications._
