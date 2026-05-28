---
name: fullstory-identify-users
version: v2
description: Comprehensive guide for implementing Fullstory's User Identification API (setIdentity) across web applications. Teaches proper uid handling, property passing, re-identification behavior, and session management. Includes detailed good/bad examples for login flows, multi-account scenarios, and SPA applications to help developers correctly identify users for analytics and session replay.
related_skills:
  - fullstory-anonymize-users
  - fullstory-user-properties
  - fullstory-user-consent
  - fullstory-async-methods
  - fullstory-privacy-strategy
  - fullstory-banking
  - fullstory-healthcare
  - fullstory-saas
---

# Fullstory Identify Users API

## Overview

Fullstory's User Identification API allows developers to associate session data with your own unique customer identifiers. By calling `FS('setIdentity')`, you link a user's Fullstory session to their identity in your system, enabling you to:

- Search for sessions by customer ID
- View all sessions for a specific user across devices
- Connect Fullstory data with your internal analytics and CRM systems
- Attribute behavior patterns to known users

This skill covers implementation patterns, best practices, and common pitfalls for browser/web applications using the v2 Browser API.

## Core Concepts

### When Identification Happens

- **On Login**: Call `setIdentity` immediately after a successful authentication
- **On Page Load (Already Authenticated)**: Call `setIdentity` on every page load if the user is logged in
- **After Authentication Redirects**: Ensure identification persists across OAuth/SSO redirects

### User Identity vs Anonymous Sessions

- **Anonymous Session**: Default state before `setIdentity` is called. User is tracked via the `fs_uid` first-party cookie but not linked to your system.
- **Identified Session**: After `setIdentity`, the session is permanently linked to the provided `uid`.

### How Identification Works (Cookie Behavior)

Fullstory uses a **first-party cookie** (`fs_uid`) to track users across sessions.

#### Why First-Party Cookies Matter

| Aspect                  | First-Party (Fullstory)                      | Third-Party                              |
| ----------------------- | -------------------------------------------- | ---------------------------------------- |
| **Domain**              | Set on YOUR domain (example.com)             | Set on external domain (ads.tracker.com) |
| **Browser blocking**    | ✅ Not blocked by browsers or ad-blockers    | ❌ Often blocked by default              |
| **Cross-site tracking** | ❌ Cannot track users across different sites | ✅ Can track across sites                |
| **Privacy**             | ✅ Data stays within your domain context     | ❌ Aggregates data across web            |

> **Key Benefit**: Because Fullstory uses first-party cookies on YOUR domain, user identity cannot be connected between multiple sites using Fullstory. Each site has its own separate `fs_uid` cookie - your customers' data is isolated to your site only.

#### Cookie-Based Session Linking

1. **Before identification**: The `fs_uid` cookie links all sessions from the same browser/device together (persists for 1 year unless deleted)
2. **When `setIdentity` is called**: ALL previous anonymous sessions with that same `fs_uid` cookie are **retroactively merged** into the identified user
3. **Cross-device linking**: If the same `uid` is used on different devices, all sessions across all devices are linked

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Session Merging on Identification                     │
├─────────────────────────────────────────────────────────────────────────┤
│  Day 1: Anonymous visit          fs_uid: abc123  → "Anonymous User"     │
│  Day 3: Anonymous visit          fs_uid: abc123  → Same anonymous user  │
│  Day 7: User logs in, setIdentity(uid: "user_456")                      │
│         ↓                                                               │
│  Result: ALL sessions (Day 1, 3, 7) now linked to "user_456"           │
└─────────────────────────────────────────────────────────────────────────┘
```

> **Important**: This means a user's entire journey from first visit through conversion can be tracked, even if they only identify on their 5th session.
>
> **Reference**: [Why Fullstory uses First-Party Cookies](https://help.fullstory.com/hc/en-us/articles/360020829513-Why-Fullstory-uses-First-Party-Cookies)

### Re-identification Behavior

- **CRITICAL**: You cannot change a user's identity once assigned within a session
- If you call `setIdentity` with a different `uid`, Fullstory automatically splits the session into a new session
- This is by design to maintain data integrity and prevent identity pollution

### Key Principles

1. Use a **stable, unique identifier** (database ID, UUID) - never use PII like email as the uid
2. Call `setIdentity` **as early as possible** after authentication
3. Include **meaningful properties** for searchability (displayName, email)
4. Handle **logout properly** by calling anonymize

### setIdentity vs setProperties (User)

| Scenario                         | Use This API                    | Why                                         |
| -------------------------------- | ------------------------------- | ------------------------------------------- |
| User logs in                     | `setIdentity`                   | Links session to user identity              |
| Initial user properties at login | `setIdentity` with `properties` | Convenient to include with identification   |
| Update user properties later     | `setProperties` (type: 'user')  | Don't re-identify just to update properties |
| Properties for anonymous user    | `setProperties` (type: 'user')  | Works without identification!               |

> **Important**: The `properties` object in `setIdentity` is a convenience - you can include initial properties when identifying. However, for **updating** properties after identification or for **anonymous users**, use `setProperties` with `type: 'user'` instead. See the **fullstory-user-properties** skill for details.

```javascript
// At login - identify with initial properties
FS('setIdentity', {
  uid: user.id,
  properties: {displayName: user.name, email: user.email, plan: user.plan},
})

// Later - user upgrades plan (DON'T re-identify!)
FS('setProperties', {
  type: 'user',
  properties: {plan: 'enterprise', upgraded_at: new Date().toISOString()},
})
```

---

## API Reference

### Basic Syntax

```javascript
FS('setIdentity', {
  uid: string,           // Required: Your unique user identifier
  properties?: object,   // Optional: Additional user properties
  schema?: object        // Optional: Type inference for properties
});
```

### Parameters

| Parameter    | Type   | Required | Description                                                                                           |
| ------------ | ------ | -------- | ----------------------------------------------------------------------------------------------------- |
| `uid`        | string | **Yes**  | A unique identifier for the user from your system. Must be stable and unique. Maximum 256 characters. |
| `properties` | object | No       | Key/value pairs of additional user information                                                        |
| `schema`     | object | No       | Type hints for property values (see Custom Properties)                                                |

### Special Property Fields

| Field         | Type   | Description                                          |
| ------------- | ------ | ---------------------------------------------------- |
| `displayName` | string | Shown in session list and user card in Fullstory app |
| `email`       | string | Enables search via HTTP API and email-based lookups  |

### Supported Property Types

| Type    | Description       | Examples                     |
| ------- | ----------------- | ---------------------------- |
| `str`   | String value      | "premium", "enterprise"      |
| `strs`  | Array of strings  | ["admin", "beta-tester"]     |
| `int`   | Integer           | 42, -5, 0                    |
| `ints`  | Array of integers | [1, 2, 3]                    |
| `real`  | Float/decimal     | 99.99, -3.14                 |
| `reals` | Array of reals    | [10.5, 20.0]                 |
| `bool`  | Boolean           | true, false                  |
| `bools` | Array of booleans | [true, false, true]          |
| `date`  | ISO8601 date      | "2024-01-15T00:00:00Z"       |
| `dates` | Array of dates    | ["2024-01-01", "2024-02-01"] |

### Rate Limits

- **Sustained**: 30 calls per page per minute
- **Burst**: 10 calls per second

---

## ✅ GOOD IMPLEMENTATION EXAMPLES

### Example 1: Basic Login Identification

```javascript
// GOOD: Call setIdentity immediately after successful login
async function handleLogin(credentials) {
  try {
    const response = await authenticateUser(credentials)
    const user = response.user

    // Identify user in Fullstory right after successful auth
    FS('setIdentity', {
      uid: user.id, // Use stable database ID, not email
      properties: {
        displayName: user.fullName,
        email: user.email,
        accountType: user.plan,
        signupDate: user.createdAt, // ISO8601 format
      },
    })

    // Continue with login flow
    redirectToDashboard()
  } catch (error) {
    handleLoginError(error)
  }
}
```

**Why this is good:**

- ✅ Uses stable database ID as uid, not PII
- ✅ Called immediately after successful authentication
- ✅ Includes displayName for easy identification in Fullstory
- ✅ Includes email for searchability
- ✅ Adds business-relevant properties (accountType, signupDate)

### Example 2: Page Load with Existing Session (SPA/SSR)

```javascript
// GOOD: Check authentication state and identify on every page load
function initializeFullstory() {
  const currentUser = getCurrentAuthenticatedUser()

  if (currentUser && currentUser.id) {
    // User is logged in - identify them
    FS('setIdentity', {
      uid: currentUser.id,
      properties: {
        displayName: currentUser.name,
        email: currentUser.email,
        role: currentUser.role,
        companyId: currentUser.organizationId,
        plan: currentUser.subscription.plan,
        trialEndsAt: currentUser.subscription.trialEnd,
      },
    })
  }
  // If not logged in, user remains anonymous (default state)
}

// Call on app initialization
document.addEventListener('DOMContentLoaded', initializeFullstory)
```

**Why this is good:**

- ✅ Handles both authenticated and anonymous states
- ✅ Calls on every page load to ensure identification survives navigation
- ✅ Includes organization context for B2B analytics
- ✅ Captures subscription data for segment analysis

### Example 3: React/Next.js Integration

```jsx
// GOOD: React hook for Fullstory identification
import {useEffect} from 'react'
import {useAuth} from './auth-context'

function useFullstoryIdentity() {
  const {user, isAuthenticated, isLoading} = useAuth()

  useEffect(() => {
    // Wait for auth state to be determined
    if (isLoading) return

    if (isAuthenticated && user) {
      FS('setIdentity', {
        uid: user.id,
        properties: {
          displayName: `${user.firstName} ${user.lastName}`,
          email: user.email,
          role: user.role,
          teamSize: user.team?.memberCount,
          features: user.enabledFeatures, // Array of strings
          lastLoginAt: new Date().toISOString(),
        },
      })
    }
  }, [user, isAuthenticated, isLoading])
}

// Usage in App component
function App() {
  useFullstoryIdentity()

  return <AppContent />
}
```

**Why this is good:**

- ✅ Waits for auth state to stabilize before identifying
- ✅ Re-runs when user state changes
- ✅ Handles loading states properly
- ✅ Captures feature flags for segmentation
- ✅ Updates lastLoginAt for recency tracking

### Example 4: OAuth/SSO Callback Handling

```javascript
// GOOD: Identify user after OAuth callback
async function handleOAuthCallback() {
  const urlParams = new URLSearchParams(window.location.search)
  const code = urlParams.get('code')

  if (!code) {
    redirectToLogin()
    return
  }

  try {
    // Exchange code for tokens and user info
    const {user, tokens} = await exchangeOAuthCode(code)

    // Store tokens
    setAuthTokens(tokens)

    // Identify in Fullstory BEFORE redirecting away
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email,
        authProvider: 'google', // Track SSO provider
        ssoOrganization: user.hostedDomain,
      },
    })

    // Now safe to redirect
    redirectToDashboard()
  } catch (error) {
    handleOAuthError(error)
  }
}
```

**Why this is good:**

- ✅ Identifies user before any redirects
- ✅ Captures authentication provider for analytics
- ✅ Handles SSO organization context
- ✅ Proper error handling flow

### Example 5: With Explicit Schema Types

```javascript
// GOOD: Using schema for explicit type control
FS('setIdentity', {
  uid: 'usr_a1b2c3d4e5',
  properties: {
    displayName: 'Sarah Johnson',
    email: 'sarah.johnson@company.com',
    accountBalance: 1500.5,
    loginCount: 42,
    isPremium: true,
    signupDate: '2023-06-15T00:00:00Z',
    permissions: ['read', 'write', 'admin'],
  },
  schema: {
    accountBalance: 'real',
    loginCount: 'int',
    isPremium: 'bool',
    signupDate: 'date',
    permissions: 'strs',
  },
})
```

**Why this is good:**

- ✅ Explicit schema ensures proper type handling
- ✅ Enables numeric comparisons in Fullstory search
- ✅ Boolean enables is/is-not filtering
- ✅ Date enables time-based queries
- ✅ String array enables "contains" searches

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Using Email as UID

```javascript
// BAD: Using email as the unique identifier
FS('setIdentity', {
  uid: user.email, // BAD: PII as uid
  properties: {
    displayName: user.name,
  },
})
```

**Why this is bad:**

- ❌ Email is PII - exposes it in Fullstory URLs and exports
- ❌ Email can change when user updates their email address
- ❌ May cause session linking issues if email is reused
- ❌ Violates privacy best practices

**CORRECTED VERSION:**

```javascript
// GOOD: Use stable database ID
FS('setIdentity', {
  uid: user.id, // Stable, non-PII identifier
  properties: {
    displayName: user.name,
    email: user.email, // Email as a searchable property, not the uid
  },
})
```

### Example 2: Identifying Before Authentication Completes

```javascript
// BAD: Calling setIdentity before auth is confirmed
function handleLoginClick() {
  const credentials = getFormCredentials()

  // BAD: Identifying with form data before server confirms identity
  FS('setIdentity', {
    uid: credentials.username,
    properties: {
      email: credentials.email,
    },
  })

  // This might fail - user isn't actually authenticated yet!
  authenticateUser(credentials)
}
```

**Why this is bad:**

- ❌ Identifies user before authentication succeeds
- ❌ If login fails, wrong identity is associated with session
- ❌ Username from form may not match actual user ID
- ❌ Creates data integrity issues

**CORRECTED VERSION:**

```javascript
// GOOD: Only identify after successful authentication
async function handleLoginClick() {
  const credentials = getFormCredentials()

  try {
    const response = await authenticateUser(credentials)

    // Only identify AFTER server confirms auth
    FS('setIdentity', {
      uid: response.user.id,
      properties: {
        displayName: response.user.name,
        email: response.user.email,
      },
    })

    redirectToDashboard()
  } catch (error) {
    // Login failed - user remains anonymous
    showLoginError(error)
  }
}
```

### Example 3: Attempting to Change Identity

```javascript
// BAD: Trying to switch users without proper anonymization
function switchUserAccount(newUser) {
  // This will cause a session split, not update the identity!
  FS('setIdentity', {
    uid: newUser.id,
    properties: {
      displayName: newUser.name,
    },
  })
}
```

**Why this is bad:**

- ❌ Cannot change identity of an already-identified user
- ❌ Causes automatic session split (may be unexpected)
- ❌ Creates confusing user journey in Fullstory
- ❌ May fragment analytics data

**CORRECTED VERSION:**

```javascript
// GOOD: Properly handle account switching
async function switchUserAccount(newUser) {
  // First, anonymize the current session
  FS('setIdentity', {anonymous: true})

  // Then identify as the new user (starts fresh session)
  FS('setIdentity', {
    uid: newUser.id,
    properties: {
      displayName: newUser.name,
      email: newUser.email,
    },
  })
}
```

### Example 4: Calling setIdentity on Every Interaction

```javascript
// BAD: Over-calling setIdentity
function handleButtonClick(buttonId) {
  // BAD: Don't call setIdentity on every interaction!
  FS('setIdentity', {
    uid: currentUser.id,
    properties: {
      displayName: currentUser.name,
      lastAction: buttonId, // Trying to track actions via identity
    },
  })

  performAction(buttonId)
}
```

**Why this is bad:**

- ❌ Wastes rate limit quota (30 calls/minute max)
- ❌ May hit burst limit (10 calls/second)
- ❌ Properties on identity shouldn't track transient actions
- ❌ Misuse of API - should use trackEvent for actions

**CORRECTED VERSION:**

```javascript
// GOOD: Identify once, use events for actions
// On page load / auth
FS('setIdentity', {
  uid: currentUser.id,
  properties: {
    displayName: currentUser.name,
    email: currentUser.email,
  },
})

// For tracking actions - use trackEvent instead
function handleButtonClick(buttonId) {
  FS('trackEvent', {
    name: 'Button Clicked',
    properties: {
      buttonId: buttonId,
      buttonSection: getButtonSection(buttonId),
    },
  })

  performAction(buttonId)
}
```

### Example 5: Missing displayName and email

```javascript
// BAD: Minimal identification with no useful properties
FS('setIdentity', {
  uid: user.id,
  // No properties at all!
})
```

**Why this is bad:**

- ❌ No displayName - sessions show cryptic ID in Fullstory UI
- ❌ No email - can't search users via email
- ❌ No business context - can't segment users effectively
- ❌ Wastes the opportunity to enrich user data

**CORRECTED VERSION:**

```javascript
// GOOD: Rich user context
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.fullName || user.username,
    email: user.email,
    role: user.role,
    plan: user.subscriptionPlan,
    companyName: user.organization?.name,
    signupDate: user.createdAt,
  },
})
```

### Example 6: Type Mismatches in Properties

```javascript
// BAD: Wrong value formats for intended types
FS('setIdentity', {
  uid: 'usr_123',
  properties: {
    displayName: 'John Doe',
    loginCount: '42', // BAD: String instead of number
    accountBalance: '$150.00', // BAD: Currency symbol in number
    isPremium: 'yes', // BAD: Should be boolean
    signupDate: 'June 15 2023', // BAD: Not ISO8601 format
  },
  schema: {
    loginCount: 'int',
    accountBalance: 'real',
    isPremium: 'bool',
    signupDate: 'date',
  },
})
```

**Why this is bad:**

- ❌ loginCount '42' won't parse correctly as int
- ❌ '$150.00' won't parse as real due to $ symbol
- ❌ 'yes' is not a valid boolean value
- ❌ Date format won't be recognized

**CORRECTED VERSION:**

```javascript
// GOOD: Properly formatted values
FS('setIdentity', {
  uid: 'usr_123',
  properties: {
    displayName: 'John Doe',
    loginCount: 42, // Number type
    accountBalance: 150.0, // Clean number
    currency: 'USD', // Currency as separate field
    isPremium: true, // Boolean type
    signupDate: '2023-06-15T00:00:00Z', // ISO8601 format
  },
  schema: {
    loginCount: 'int',
    accountBalance: 'real',
    isPremium: 'bool',
    signupDate: 'date',
  },
})
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Authentication State Machine

```
┌─────────────────┐
│  Anonymous      │ ← Initial state (no setIdentity called)
│  Session        │
└────────┬────────┘
         │ User logs in
         ▼
┌─────────────────┐
│  Identified     │ ← setIdentity({ uid: 'xxx' }) called
│  Session        │
└────────┬────────┘
         │ User logs out
         ▼
┌─────────────────┐
│  New Anonymous  │ ← setIdentity({ anonymous: true }) called
│  Session        │
└─────────────────┘
```

### Pattern 2: Multi-Account Application

```javascript
// For apps where users can switch between accounts
class FullstoryIdentityManager {
  currentUserId = null

  identify(user) {
    if (this.currentUserId && this.currentUserId !== user.id) {
      // Different user - must anonymize first
      this.anonymize()
    }

    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email,
      },
    })

    this.currentUserId = user.id
  }

  anonymize() {
    FS('setIdentity', {anonymous: true})
    this.currentUserId = null
  }

  updateProperties(properties) {
    // Use setProperties for property-only updates
    FS('setProperties', {
      type: 'user',
      properties: properties,
    })
  }
}
```

### Pattern 3: Progressive Identification

```javascript
// For apps with guest checkout → account creation flow
class ProgressiveIdentification {
  // During guest checkout - don't identify yet
  handleGuestCheckout(cart) {
    // User remains anonymous
    // Track the checkout event instead
    FS('trackEvent', {
      name: 'Guest Checkout Started',
      properties: {
        cartValue: cart.total,
        itemCount: cart.items.length,
      },
    })
  }

  // When guest creates account after checkout
  handleAccountCreation(user) {
    // NOW identify them - this links all prior anonymous activity
    FS('setIdentity', {
      uid: user.id,
      properties: {
        displayName: user.name,
        email: user.email,
        accountCreatedDuringCheckout: true,
      },
    })
  }
}
```

---

## INTEGRATION WITH OTHER FS APIS

### Identification + User Properties

```javascript
// setIdentity can include properties
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.name,
    email: user.email,
    plan: 'starter', // Initial plan at signup
  },
})

// Later, update properties without re-identifying
// (user upgraded their plan)
FS('setProperties', {
  type: 'user',
  properties: {
    plan: 'professional',
    upgradedAt: new Date().toISOString(),
  },
})
```

### Identification + Events

```javascript
// Identify user
FS('setIdentity', {
  uid: user.id,
  properties: {displayName: user.name},
})

// Events are automatically linked to identified user
FS('trackEvent', {
  name: 'Feature Used',
  properties: {
    featureName: 'Advanced Export',
    exportFormat: 'CSV',
  },
})
```

### Identification + Page Properties

```javascript
// User identity
FS('setIdentity', {
  uid: user.id,
  properties: {displayName: user.name},
})

// Page context (separate concern)
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Dashboard',
    dashboardView: 'analytics',
  },
})
```

---

## TROUBLESHOOTING

### Sessions Not Linking to User

**Symptom**: User appears anonymous despite calling setIdentity

**Common Causes**:

1. ❌ setIdentity called after Fullstory script fully loaded
2. ❌ uid is undefined, null, or empty string
3. ❌ Fullstory blocked by ad blocker
4. ❌ Browser privacy mode preventing storage

**Solutions**:

- ✅ Verify uid is a non-empty string before calling
- ✅ Check browser console for Fullstory errors
- ✅ Use async API: `await FS('setIdentityAsync', {...})`
- ✅ Verify Fullstory snippet is loading correctly

### Unexpected Session Splits

**Symptom**: User has many fragmented sessions

**Common Causes**:

1. ❌ Calling setIdentity with different uid
2. ❌ Calling setIdentity on every page without checking current identity
3. ❌ Identity state not persisting across page navigations

**Solutions**:

- ✅ Track current identity state in your app
- ✅ Only call setIdentity when actually identifying/changing users
- ✅ Use proper logout flow with anonymize

### Properties Not Appearing

**Symptom**: User properties don't show in Fullstory

**Common Causes**:

1. ❌ Property values have wrong types
2. ❌ Property names have invalid characters
3. ❌ Hitting property limits

**Solutions**:

- ✅ Use schema to specify types explicitly
- ✅ Use camelCase or snake_case for property names
- ✅ Check property limits (varies by plan)

---

## LIMITS AND CONSTRAINTS

### UID Requirements

- Maximum 256 characters
- Must be a non-empty string
- Should be stable and unique per user
- Should NOT be PII (don't use email, phone, etc.)

### Property Limits

- Check your Fullstory plan for specific limits
- Property names: alphanumeric, underscores, hyphens
- High cardinality properties may be limited

### Call Frequency

- **Sustained**: 30 calls per page per minute
- **Burst**: 10 calls per second
- Exceeding limits may result in dropped calls

---

## KEY TAKEAWAYS FOR AGENT

When helping developers implement User Identification:

1. **Always emphasize**:
   - Use stable database IDs as uid, never PII
   - Call setIdentity AFTER successful authentication
   - Include displayName and email as properties
   - You cannot change identity without anonymizing first

2. **Common mistakes to watch for**:
   - Using email as uid
   - Identifying before auth completes
   - Calling setIdentity excessively
   - Trying to update identity instead of using setProperties
   - Missing displayName/email properties

3. **Questions to ask developers**:
   - What's your unique user identifier? (database ID, UUID)
   - When does authentication complete in your flow?
   - Do users switch between accounts in your app?
   - What user attributes are important for segmentation?

4. **Integration considerations**:
   - SPA: Ensure identification survives client-side navigation
   - SSR: Call on both server hydration and client-side auth changes
   - OAuth: Identify in the callback, before redirects
   - Mobile web: Handle app-to-browser identity handoffs

---

## REFERENCE LINKS

- **Identify Users**: https://developer.fullstory.com/browser/identification/identify-users/
- **Anonymize Users**: https://developer.fullstory.com/browser/identification/anonymize-users/
- **Set User Properties**: https://developer.fullstory.com/browser/identification/set-user-properties/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Help Center - Identifying Users**: https://help.fullstory.com/hc/en-us/articles/360020623294-Identifying-users

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's User Identification API correctly for web applications._
