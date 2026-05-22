---
name: fullstory-user-consent
version: v2
description: Comprehensive guide for implementing Fullstory's User Consent API for web applications. Teaches proper consent flow implementation, selective capture modes, GDPR/CCPA compliance patterns, and cookie consent integration. Includes detailed good/bad examples for consent banners, preference centers, and privacy-conscious recording to help developers implement privacy-compliant session recording.
related_skills:
  - fullstory-identify-users
  - fullstory-anonymize-users
  - fullstory-capture-control
---

# Fullstory User Consent API

## Overview

Fullstory's User Consent API allows developers to implement privacy-compliant session recording by conditioning capture on explicit user consent. This is essential for:

- **GDPR Compliance**: Obtain consent before recording EU users
- **CCPA Compliance**: Allow California users to opt-out
- **Cookie Consent Integration**: Tie Fullstory to your consent management platform (CMP)
- **Selective Capture**: Record only users who have consented
- **Privacy Controls**: Give users control over their data

## Core Concepts

### ⚠️ Critical: Two Different Consent Approaches

Fullstory has **two separate mechanisms** for consent. Using the wrong one is a common mistake:

| Approach                   | API                                              | What It Controls                                                          | Use Case                                          |
| -------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------- |
| **Element-Level Consent**  | `FS('setIdentity', { consent: true/false })`     | Only elements marked "Capture with consent" in Fullstory Privacy Settings | Selective capture of specific sensitive elements  |
| **Holistic Consent (CMP)** | `_fs_capture_on_startup = false` + `FS('start')` | **ALL** Fullstory capture                                                 | GDPR cookie banners, consent management platforms |

### Element-Level Consent (setIdentity with consent)

Per the [official documentation](https://developer.fullstory.com/browser/fullcapture/user-consent/):

> "HTML Elements that have been configured to 'Capture data with user consent' in Fullstory's privacy settings are only captured after an invocation of `FS('setIdentity', { consent: true })`."

**This does NOT control all Fullstory capture** - only specific elements you've pre-configured in the Fullstory UI to require consent.

> **Why `setIdentity`?** This is Fullstory's API design choice - the `consent` parameter happens to be passed through the `setIdentity` method. You do **NOT** need to provide a `uid` or actually identify the user. You can simply call `FS('setIdentity', { consent: true })` for anonymous users - it just toggles the element-level consent flag.

```javascript
// This works - no uid required, user stays anonymous
FS('setIdentity', {consent: true})

// This also works - consent + identification combined
FS('setIdentity', {uid: 'user_123', consent: true})
```

| Consent State    | Effect                                         |
| ---------------- | ---------------------------------------------- |
| `consent: true`  | Capture elements marked "Capture with consent" |
| `consent: false` | Don't capture those specific elements          |
| Not set          | Those specific elements not captured           |

### Holistic Consent (Consent Management Platforms / GDPR)

For **cookie consent banners** and **consent management platforms** where you need to delay **ALL** Fullstory capture until consent is given, use the [capture delay approach](https://developer.fullstory.com/browser/fullcapture/capture-data/#manually-delay-data-capture):

```javascript
// BEFORE the Fullstory snippet loads
window['_fs_capture_on_startup'] = false

// ... Fullstory snippet loads but does NOT capture ...

// AFTER user gives consent via your CMP/cookie banner
FS('start') // NOW Fullstory begins capturing
```

### Choosing the Right Approach

```
Do you need to delay ALL Fullstory capture until consent?
│
├─ YES (GDPR cookie banner, CMP integration)
│  └─ Use: _fs_capture_on_startup = false + FS('start')
│
└─ NO (Just want some elements to require extra consent)
   └─ Use: FS('setIdentity', { consent: true/false })
```

### Combining Both Approaches

For maximum privacy compliance, you can use both:

```javascript
// Step 1: Delay all capture until cookie consent
window['_fs_capture_on_startup'] = false

// Step 2: User accepts cookies via your CMP
onCookieConsentAccepted(() => {
  FS('start') // Begin general capture

  // Step 3: Later, user opts into extra data sharing
  // (for elements marked "Capture with consent" in FS settings)
  if (userAcceptedEnhancedTracking) {
    FS('setIdentity', {consent: true})
  }
})
```

---

## API Reference

### Approach 1: Holistic Consent (Recommended for GDPR/CMP)

```javascript
// BEFORE Fullstory snippet - prevent capture on startup
window['_fs_capture_on_startup'] = false

// AFTER user consents - start all capture
FS('start')

// If user later revokes consent - stop all capture
FS('shutdown')

// If user consents again
FS('restart')
```

| Method                                     | Effect                                  |
| ------------------------------------------ | --------------------------------------- |
| `window['_fs_capture_on_startup'] = false` | Prevent ALL capture until `FS('start')` |
| `FS('start')`                              | Begin capture (after delay)             |
| `FS('shutdown')`                           | Stop all capture                        |
| `FS('restart')`                            | Resume capture after shutdown           |

### Approach 2: Element-Level Consent

```javascript
// Enable capture of elements marked "Capture with consent"
FS('setIdentity', { consent: true });

// Disable capture of those specific elements
FS('setIdentity', { consent: false });

// Combine with user identification
FS('setIdentity', {
  uid: string,
  consent: true,
  properties?: object
});
```

| Parameter    | Type    | Required | Description                                                    |
| ------------ | ------- | -------- | -------------------------------------------------------------- |
| `consent`    | boolean | Yes      | `true` enables, `false` disables element-level consent capture |
| `uid`        | string  | No       | User identifier (if also identifying)                          |
| `properties` | object  | No       | User properties (if identifying)                               |

### Rate Limits

- Standard API rate limits apply (30 calls/min sustained)

---

## ✅ GOOD IMPLEMENTATION EXAMPLES

### Example 1: GDPR Cookie Consent Banner (Holistic Approach)

```javascript
// GOOD: Holistic consent for GDPR/cookie banners
// This approach delays ALL Fullstory capture until consent is given

// STEP 1: In your HTML, BEFORE the Fullstory snippet
// <script>window['_fs_capture_on_startup'] = false;</script>
// <script>/* Fullstory snippet here */</script>

// STEP 2: Your consent manager class
class GDPRConsentManager {
  constructor() {
    this.consentKey = 'fs_consent'
    this.initFromStorage()
  }

  initFromStorage() {
    const storedConsent = localStorage.getItem(this.consentKey)

    if (storedConsent === 'granted') {
      this.grantConsent()
    }
    // If denied or not set, Fullstory stays disabled (capture never started)
  }

  grantConsent() {
    localStorage.setItem(this.consentKey, 'granted')

    // Start ALL Fullstory capture
    FS('start')

    // If user is logged in, also identify them
    const currentUser = getCurrentUser()
    if (currentUser) {
      FS('setIdentity', {
        uid: currentUser.id,
        properties: {
          displayName: currentUser.name,
          email: currentUser.email,
        },
      })
    }

    console.log('Fullstory capture started')
  }

  revokeConsent() {
    localStorage.setItem(this.consentKey, 'denied')

    // Stop ALL Fullstory capture
    FS('shutdown')

    console.log('Fullstory capture stopped')
  }

  hasConsent() {
    return localStorage.getItem(this.consentKey) === 'granted'
  }

  resetConsent() {
    localStorage.removeItem(this.consentKey)
    FS('shutdown') // Stop capture when consent is reset
    // Show banner again
    showConsentBanner()
  }
}

// Initialize
const consent = new GDPRConsentManager()

// Wire up to consent banner
document.getElementById('accept-cookies').addEventListener('click', () => {
  consent.grantConsent()
  hideConsentBanner()
})

document.getElementById('decline-cookies').addEventListener('click', () => {
  consent.revokeConsent()
  hideConsentBanner()
})
```

**Why this is good:**

- ✅ Uses `_fs_capture_on_startup = false` to **prevent ALL capture** until consent
- ✅ Uses `FS('start')` / `FS('shutdown')` for holistic control
- ✅ Persists consent choice in localStorage
- ✅ Restores consent state on page load
- ✅ Handles logged-in users properly
- ✅ Complies with GDPR requirement that NO tracking occurs before consent

### Example 2: Element-Level Consent (Selective Capture)

```javascript
// GOOD: Element-level consent for specific sensitive elements
// Use this when you want general capture but extra consent for certain elements

// First, in Fullstory Privacy Settings, mark specific elements as
// "Capture data with user consent" (e.g., form fields with sensitive data)

// Then in your code:
const ElementConsentManager = {
  // User opts into enhanced tracking (for elements marked "Capture with consent")
  enableEnhancedTracking() {
    FS('setIdentity', {consent: true})
    console.log('Enhanced tracking enabled for consent-marked elements')
  },

  // User opts out of enhanced tracking
  disableEnhancedTracking() {
    FS('setIdentity', {consent: false})
    console.log('Enhanced tracking disabled')
  },
}

// Usage in a preferences panel
document.getElementById('enhanced-tracking-checkbox').addEventListener('change', (e) => {
  if (e.target.checked) {
    ElementConsentManager.enableEnhancedTracking()
  } else {
    ElementConsentManager.disableEnhancedTracking()
  }
})
```

**Why this is good:**

- ✅ General Fullstory capture still works
- ✅ Only specific pre-configured elements require extra consent
- ✅ Gives users granular control over sensitive data capture

### Example 3: Region-Based Consent (GDPR for EU Only)

```javascript
// GOOD: Full GDPR-compliant consent flow with region detection
// IMPORTANT: Set window['_fs_capture_on_startup'] = false BEFORE snippet loads

const RegionalConsent = {
  // Check if user is in EU (simplified - use proper geolocation service in production)
  isEUUser() {
    return Intl.DateTimeFormat().resolvedOptions().timeZone.includes('Europe')
  },

  // Initialize based on region and consent state
  async initialize() {
    const needsConsent = this.isEUUser()
    const hasConsent = this.getStoredConsent()

    if (!needsConsent) {
      // Non-EU: can capture without explicit consent (check local laws)
      FS('start') // Use start() since we delayed capture
      return
    }

    if (hasConsent === 'granted') {
      FS('setIdentity', {consent: true})
    } else if (hasConsent === 'denied') {
      FS('setIdentity', {consent: false})
    } else {
      // No consent recorded - show banner, don't capture yet
      this.showConsentBanner()
    }
  },

  getStoredConsent() {
    return localStorage.getItem('gdpr_consent_analytics')
  },

  recordConsent(granted, method) {
    const consentRecord = {
      granted,
      timestamp: new Date().toISOString(),
      method, // 'banner', 'settings', etc.
      userAgent: navigator.userAgent,
    }

    localStorage.setItem('gdpr_consent_analytics', granted ? 'granted' : 'denied')
    localStorage.setItem('gdpr_consent_record', JSON.stringify(consentRecord))

    // Send to backend for compliance records
    fetch('/api/consent', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(consentRecord),
    }).catch(console.warn)

    // Update Fullstory
    FS('setIdentity', {consent: granted})
  },

  showConsentBanner() {
    document.getElementById('gdpr-banner').style.display = 'block'
  },

  hideConsentBanner() {
    document.getElementById('gdpr-banner').style.display = 'none'
  },

  // Required: Allow users to withdraw consent
  withdrawConsent() {
    this.recordConsent(false, 'user_withdrawal')

    // Clear any stored Fullstory data
    // Note: Fullstory doesn't store client-side, this is for other trackers

    alert('Your consent has been withdrawn. Session recording has been disabled.')
  },

  // Required: Export user data (for GDPR data access requests)
  async requestDataExport() {
    // Redirect to Fullstory's data request process
    // Or contact your Fullstory admin
    window.location.href = '/privacy/data-request'
  },
}

// Initialize on page load
GDPRConsent.initialize()

// Banner buttons
document.getElementById('accept-all').addEventListener('click', () => {
  GDPRConsent.recordConsent(true, 'banner')
  GDPRConsent.hideConsentBanner()
})

document.getElementById('reject-all').addEventListener('click', () => {
  GDPRConsent.recordConsent(false, 'banner')
  GDPRConsent.hideConsentBanner()
})

// Settings page withdrawal
document.getElementById('withdraw-consent').addEventListener('click', () => {
  GDPRConsent.withdrawConsent()
})
```

**Why this is good:**

- ✅ Region-based consent requirements
- ✅ Records consent for compliance
- ✅ Provides withdrawal mechanism
- ✅ Backend record keeping
- ✅ Non-EU users not blocked

### Example 3: CMP (Consent Management Platform) Integration

```javascript
// GOOD: Integrate with OneTrust, CookieBot, or similar CMP
class CMPIntegration {
  // OneTrust integration
  static initOneTrust() {
    // Listen for OneTrust consent changes
    window.OptanonWrapper = function () {
      const consentGroups = OnetrustActiveGroups || ''

      // Check if analytics category is consented
      // C0002 is typically the analytics category - verify your setup
      if (consentGroups.includes('C0002')) {
        FS('setIdentity', {consent: true})
      } else {
        FS('setIdentity', {consent: false})
      }
    }

    // Also handle initial state
    if (typeof OnetrustActiveGroups !== 'undefined') {
      window.OptanonWrapper()
    }
  }

  // CookieBot integration
  static initCookieBot() {
    window.addEventListener('CookiebotOnAccept', () => {
      if (Cookiebot.consent.statistics) {
        FS('setIdentity', {consent: true})
      }
    })

    window.addEventListener('CookiebotOnDecline', () => {
      FS('setIdentity', {consent: false})
    })

    // Check initial state
    if (typeof Cookiebot !== 'undefined' && Cookiebot.consent) {
      if (Cookiebot.consent.statistics) {
        FS('setIdentity', {consent: true})
      } else {
        FS('setIdentity', {consent: false})
      }
    }
  }

  // TrustArc integration
  static initTrustArc() {
    window.truste = window.truste || {}
    window.truste.eu = window.truste.eu || {}

    window.truste.eu.bindMap = {
      behaviorManager: {
        init: function () {
          // Check consent status
          const consent = truste.eu.getBehavior()
          if (consent.analytics === 'on') {
            FS('setIdentity', {consent: true})
          } else {
            FS('setIdentity', {consent: false})
          }
        },
      },
    }
  }

  // Generic CMP API (IAB TCF v2)
  static initTCFv2() {
    if (typeof __tcfapi === 'function') {
      __tcfapi('addEventListener', 2, (tcData, success) => {
        if (success && tcData.eventStatus === 'useractioncomplete') {
          // Check for purpose 1 (store and access) and purpose 5 (measurement)
          const hasConsent = tcData.purpose?.consents?.[1] && tcData.purpose?.consents?.[5]

          FS('setIdentity', {consent: hasConsent})
        }
      })
    }
  }
}

// Initialize based on your CMP
// CMPIntegration.initOneTrust();
// CMPIntegration.initCookieBot();
// CMPIntegration.initTCFv2();
```

**Why this is good:**

- ✅ Works with popular CMPs
- ✅ Handles consent changes
- ✅ Checks initial state
- ✅ IAB TCF v2 compliant option

### Example 4: React Consent Hook

```jsx
// GOOD: React hook for consent management
import {useState, useEffect, useCallback, createContext, useContext} from 'react'

const ConsentContext = createContext(null)

export function ConsentProvider({children}) {
  const [consentStatus, setConsentStatus] = useState(() => {
    return localStorage.getItem('analytics_consent') // 'granted', 'denied', or null
  })

  useEffect(() => {
    // Sync with Fullstory on mount and changes
    if (consentStatus === 'granted') {
      FS('setIdentity', {consent: true})
    } else if (consentStatus === 'denied') {
      FS('setIdentity', {consent: false})
    }
  }, [consentStatus])

  const grantConsent = useCallback(() => {
    localStorage.setItem('analytics_consent', 'granted')
    setConsentStatus('granted')
  }, [])

  const denyConsent = useCallback(() => {
    localStorage.setItem('analytics_consent', 'denied')
    setConsentStatus('denied')
  }, [])

  const resetConsent = useCallback(() => {
    localStorage.removeItem('analytics_consent')
    setConsentStatus(null)
  }, [])

  return (
    <ConsentContext.Provider
      value={{
        consentStatus,
        hasConsent: consentStatus === 'granted',
        needsConsent: consentStatus === null,
        grantConsent,
        denyConsent,
        resetConsent,
      }}
    >
      {children}
    </ConsentContext.Provider>
  )
}

export function useConsent() {
  return useContext(ConsentContext)
}

// Consent Banner Component
function ConsentBanner() {
  const {needsConsent, grantConsent, denyConsent} = useConsent()

  if (!needsConsent) return null

  return (
    <div className="consent-banner">
      <p>We use session recording to improve your experience.</p>
      <div className="consent-buttons">
        <button onClick={grantConsent}>Accept</button>
        <button onClick={denyConsent}>Decline</button>
      </div>
    </div>
  )
}

// Settings Component
function PrivacySettings() {
  const {hasConsent, grantConsent, denyConsent, resetConsent} = useConsent()

  return (
    <div className="privacy-settings">
      <h2>Privacy Settings</h2>
      <label>
        <input
          type="checkbox"
          checked={hasConsent}
          onChange={(e) => (e.target.checked ? grantConsent() : denyConsent())}
        />
        Allow session recording
      </label>
      <button onClick={resetConsent}>Reset Preferences</button>
    </div>
  )
}
```

**Why this is good:**

- ✅ React-friendly state management
- ✅ Context for app-wide access
- ✅ Persists to localStorage
- ✅ Syncs with Fullstory
- ✅ Reusable components

### Example 5: Consent with User Identification

```javascript
// GOOD: Handle consent and identification together
class FullstoryManager {
  constructor() {
    this.consentGranted = false
    this.currentUser = null
  }

  // Call when consent is granted (from banner)
  onConsentGranted() {
    this.consentGranted = true

    if (this.currentUser) {
      // User already logged in - identify them
      this.identifyUser(this.currentUser)
    } else {
      // Just enable capture anonymously
      FS('setIdentity', {consent: true})
    }
  }

  // Call when consent is denied
  onConsentDenied() {
    this.consentGranted = false
    FS('setIdentity', {consent: false})
  }

  // Call when user logs in
  onUserLogin(user) {
    this.currentUser = user

    if (this.consentGranted) {
      // Consent already granted - identify user
      this.identifyUser(user)
    }
    // If no consent, don't identify (they'll be identified when consent is granted)
  }

  // Call when user logs out
  onUserLogout() {
    this.currentUser = null

    if (this.consentGranted) {
      // Anonymize but keep capturing (they consented)
      FS('setIdentity', {anonymous: true, consent: true})
    }
  }

  identifyUser(user) {
    FS('setIdentity', {
      uid: user.id,
      consent: true,
      properties: {
        displayName: user.name,
        email: user.email,
        plan: user.plan,
      },
    })
  }
}

const fsManager = new FullstoryManager()

// Wire up to your auth system
authService.on('login', (user) => fsManager.onUserLogin(user))
authService.on('logout', () => fsManager.onUserLogout())

// Wire up to consent banner
consentBanner.on('accept', () => fsManager.onConsentGranted())
consentBanner.on('decline', () => fsManager.onConsentDenied())
```

**Why this is good:**

- ✅ Handles consent + identity together
- ✅ Correct order regardless of user flow
- ✅ Maintains consent through login/logout
- ✅ Covers all scenarios

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Capturing Before Consent

```javascript
// BAD: Capturing without checking consent first
// This is the default snippet behavior - problematic for GDPR

// Page loads, Fullstory immediately starts capturing
// User hasn't consented yet!

// Later, user clicks "Decline"
FS('setIdentity', {consent: false}) // Too late - already captured data!
```

**Why this is bad:**

- ❌ Data captured before consent given
- ❌ GDPR violation risk
- ❌ Can't un-capture what was already recorded

**CORRECTED VERSION:**

```javascript
// GOOD: Configure snippet to wait for consent
// In your Fullstory snippet config:
window['_fs_capture_on_startup'] = false

// Then enable capture only after consent
document.getElementById('accept').addEventListener('click', () => {
  FS('setIdentity', {consent: true}) // NOW we start capturing
})
```

### Example 2: Not Persisting Consent

```javascript
// BAD: Consent not persisted - user must consent on every page
document.getElementById('accept').addEventListener('click', () => {
  FS('setIdentity', {consent: true})
  // Consent not saved! On next page, user is asked again
})
```

**Why this is bad:**

- ❌ User must consent on every page
- ❌ Annoying user experience
- ❌ May miss capture on subsequent pages

**CORRECTED VERSION:**

```javascript
// GOOD: Persist and restore consent
document.getElementById('accept').addEventListener('click', () => {
  localStorage.setItem('fs_consent', 'granted')
  FS('setIdentity', {consent: true})
})

// On page load
const savedConsent = localStorage.getItem('fs_consent')
if (savedConsent === 'granted') {
  FS('setIdentity', {consent: true})
}
```

### Example 3: No Way to Withdraw Consent

```javascript
// BAD: Once granted, user can't withdraw consent
consentBanner.on('accept', () => {
  localStorage.setItem('consent', 'granted')
  FS('setIdentity', {consent: true})
  // No settings page to change this!
})
```

**Why this is bad:**

- ❌ GDPR requires ability to withdraw
- ❌ Users stuck with their choice
- ❌ Compliance violation

**CORRECTED VERSION:**

```javascript
// GOOD: Provide withdrawal mechanism
// In privacy settings page:
function withdrawConsent() {
  localStorage.setItem('consent', 'denied')
  FS('setIdentity', {consent: false})
  showConfirmation('Session recording has been disabled.')
}

// Make it easily accessible
// Link in footer: "Privacy Settings" -> withdrawal option
```

### Example 4: Consent Logic Race Condition

```javascript
// BAD: Race condition between consent check and identify
async function initApp() {
  const user = await getUser()

  // Race condition: identify might happen before consent is granted
  FS('setIdentity', {
    uid: user.id,
    properties: {name: user.name},
    // Missing consent check!
  })

  // Consent banner shown after - too late
  showConsentBannerIfNeeded()
}
```

**Why this is bad:**

- ❌ User identified before consent check
- ❌ Data captured without consent
- ❌ Order of operations wrong

**CORRECTED VERSION:**

```javascript
// GOOD: Check consent before identifying
async function initApp() {
  const user = await getUser()
  const hasConsent = localStorage.getItem('consent') === 'granted'

  if (hasConsent) {
    // Only identify if consent already granted
    FS('setIdentity', {
      uid: user.id,
      consent: true,
      properties: {name: user.name},
    })
  } else if (localStorage.getItem('consent') === null) {
    // No decision yet - show banner
    showConsentBanner()
  }
  // If explicitly denied, do nothing
}
```

### Example 5: Ignoring CMP Status

```javascript
// BAD: Not respecting CMP decisions
// CMP is configured, but Fullstory ignores it

// OneTrust says analytics is declined, but:
FS('setIdentity', {consent: true}) // BAD: Overriding CMP decision
```

**Why this is bad:**

- ❌ Ignores user's CMP choice
- ❌ Compliance violation
- ❌ Inconsistent consent state

**CORRECTED VERSION:**

```javascript
// GOOD: Respect CMP decisions
window.OptanonWrapper = function () {
  const groups = OnetrustActiveGroups || ''

  // Only enable if user consented to analytics in CMP
  if (groups.includes('C0002')) {
    FS('setIdentity', {consent: true})
  } else {
    FS('setIdentity', {consent: false})
  }
}
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Consent State Machine

```javascript
// State machine for consent handling
const ConsentStateMachine = {
  states: {
    UNKNOWN: 'unknown', // No choice made
    GRANTED: 'granted', // User accepted
    DENIED: 'denied', // User declined
    WITHDRAWN: 'withdrawn', // User withdrew consent
  },

  currentState: null,

  init() {
    const stored = localStorage.getItem('consent_state')
    this.currentState = stored || this.states.UNKNOWN
    this.applyState()
  },

  transition(newState) {
    const oldState = this.currentState
    this.currentState = newState
    localStorage.setItem('consent_state', newState)

    console.log(`Consent: ${oldState} -> ${newState}`)
    this.applyState()
  },

  applyState() {
    switch (this.currentState) {
      case this.states.GRANTED:
        FS('setIdentity', {consent: true})
        break
      case this.states.DENIED:
      case this.states.WITHDRAWN:
        FS('setIdentity', {consent: false})
        break
      case this.states.UNKNOWN:
        // Show banner, don't capture
        showConsentBanner()
        break
    }
  },

  accept() {
    this.transition(this.states.GRANTED)
  },
  decline() {
    this.transition(this.states.DENIED)
  },
  withdraw() {
    this.transition(this.states.WITHDRAWN)
  },
  reset() {
    this.transition(this.states.UNKNOWN)
  },
}
```

### Pattern 2: Consent Wrapper for All FS Calls

```javascript
// Wrapper that checks consent before any FS call
const ConsentManager = {
  _consentGranted: false,

  init(granted) {
    this._consentGranted = granted
    if (granted) {
      FS('setIdentity', {consent: true})
    }
  },

  setConsent(granted) {
    this._consentGranted = granted
    FS('setIdentity', {consent: granted})
  },

  // Wrapped methods that check consent
  trackEvent(name, properties) {
    if (!this._consentGranted) {
      console.debug('FS event skipped - no consent:', name)
      return
    }
    FS('trackEvent', {name, properties})
  },

  setProperties(type, properties) {
    if (!this._consentGranted) {
      console.debug('FS properties skipped - no consent')
      return
    }
    FS('setProperties', {type, properties})
  },

  identify(uid, properties) {
    if (!this._consentGranted) {
      console.debug('FS identify skipped - no consent')
      return
    }
    FS('setIdentity', {uid, consent: true, properties})
  },
}

// Usage
ConsentManager.init(checkStoredConsent())
ConsentManager.trackEvent('Page Viewed', {page: '/home'})
```

---

## SNIPPET CONFIGURATION

To require consent before capture, configure the Fullstory snippet:

```javascript
window['_fs_capture_on_startup'] = false // Don't capture until consent
window['_fs_org'] = 'YOUR_ORG_ID'
window['_fs_script'] = 'edge.fullstory.com/s/fs.js'
// ... rest of snippet
```

Then call `FS('setIdentity', { consent: true })` to start capture.

---

## TROUBLESHOOTING

### Capture Not Starting After Consent

**Symptom**: `consent: true` called but no session recorded

**Common Causes**:

1. ❌ Fullstory script not loaded
2. ❌ User on excluded page
3. ❌ Privacy mode blocking FS

**Solutions**:

- ✅ Verify FS is defined
- ✅ Check page isn't excluded
- ✅ Check browser privacy settings

### Sessions Missing Consent Status

**Symptom**: Can't tell which sessions had consent

**Solutions**:

- ✅ Set user property: `consentGranted: true`
- ✅ Log consent status
- ✅ Use page properties

---

## KEY TAKEAWAYS FOR AGENT

When helping developers with Consent API:

1. **Always emphasize**:
   - Configure snippet to wait for consent if GDPR applies
   - Persist consent to localStorage
   - Provide withdrawal mechanism
   - Check consent before identifying

2. **Common mistakes to watch for**:
   - Capturing before consent
   - Not persisting consent
   - No withdrawal option
   - Ignoring CMP status
   - Race conditions with identity

3. **Questions to ask developers**:
   - Do you need GDPR compliance?
   - Do you have an existing CMP?
   - How do users currently consent?
   - Is there a privacy settings page?

4. **Best practices to recommend**:
   - Integrate with existing CMP
   - Persist consent state
   - Provide easy withdrawal
   - Test consent flows thoroughly

---

## REFERENCE LINKS

- **User Consent**: https://developer.fullstory.com/browser/fullcapture/user-consent/
- **Help Center - Consent Mode**: https://help.fullstory.com/hc/en-us/articles/360020623374

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's User Consent API correctly for privacy-compliant web applications._
