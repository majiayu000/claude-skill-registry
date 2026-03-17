---
name: fullstory-user-properties
version: v2
description: Comprehensive guide for implementing Fullstory's User Properties API (setProperties with type 'user') for web applications. Teaches proper property naming, type handling, incremental updates, and special fields (displayName, email). Includes detailed good/bad examples for CRM integration, progressive profiling, and subscription tracking to help developers enrich user profiles for analytics and segmentation.
related_skills:
  - fullstory-identify-users
  - fullstory-page-properties
  - fullstory-analytics-events
  - fullstory-data-scoping-decoration
---

# Fullstory User Properties API

## Overview

Fullstory's User Properties API allows developers to capture custom user data that enriches user profiles for search, filtering, segmentation, and analytics. Unlike `setIdentity` which links a session to a known user ID, `setProperties` with `type: 'user'` lets you add or update attributes about **any** user - including anonymous users.

> **Important**: Every new browser/device starts as an anonymous user, tracked via the `fs_uid` first-party cookie (1-year expiry). You can set user properties on anonymous users _before_ they ever identify. These properties persist across sessions and transfer when/if the user later identifies via `setIdentity`.

Key use cases:

- **Anonymous User Enrichment**: Add attributes before the user logs in (referral source, landing page, visitor type)
- **Progressive Profiling**: Update properties as you learn more about the user
- **Subscription/Plan Changes**: Track plan upgrades without re-identifying
- **Preference Tracking**: Store user settings and preferences
- **CRM Sync**: Mirror key CRM fields in Fullstory

## Core Concepts

### setIdentity vs setProperties

| API                    | Purpose                                                       | When to Use                                            | Works for Anonymous?                 |
| ---------------------- | ------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------ |
| `setIdentity`          | Link session to a known user ID + optional initial properties | Login, authentication                                  | No (converts anonymous → identified) |
| `setProperties` (user) | Add/update properties for the current user                    | **Anytime** - works for anonymous AND identified users | **Yes** ✅                           |

> **Key Distinction**: Use `setIdentity` when you need to **link a session to a known user** (requires a `uid`). Use `setProperties` when you just want to **add or update attributes** about the current user - this works for both identified AND anonymous users.

### Anonymous Users in Fullstory

Every user starts as anonymous, tracked via the `fs_uid` first-party cookie:

- **Cookie-based identity**: Fullstory sets an `fs_uid` cookie (1-year expiry) that tracks the same anonymous user across sessions and page views
- **Persistent across sessions**: As long as the cookie exists, all sessions are linked to the same anonymous user
- **Can receive user properties**: Use `setProperties` to add attributes to anonymous users
- **Properties transfer on identification**: When `setIdentity` is called, ALL previous sessions (linked by the cookie) merge into the identified user
- **Searchable and segmentable**: Anonymous users work just like identified users in Fullstory

> **Reference**: [Why Fullstory uses First-Party Cookies](https://help.fullstory.com/hc/en-us/articles/360020829513-Why-Fullstory-uses-First-Party-Cookies)

```javascript
// User lands on your site (anonymous - "User 4521" in Fullstory)
FS('setProperties', {
  type: 'user',
  properties: {
    landing_page: '/pricing',
    referral_source: 'google_ads',
    campaign: 'spring_sale_2024',
  },
})

// ... user browses for a while ...

// Later, user creates an account and logs in
FS('setIdentity', {
  uid: 'user_abc123',
  properties: {
    displayName: 'Jane Smith',
    email: 'jane@example.com',
  },
})
// The anonymous properties (landing_page, referral_source, campaign)
// are now attached to the identified user "Jane Smith"
```

### When to Use Each

```
User logs in → setIdentity({ uid: "user_123", properties: { displayName: "Jane" } })
                ↓
User updates profile → setProperties({ type: 'user', properties: { plan: "pro" } })
                ↓
User upgrades plan → setProperties({ type: 'user', properties: { plan: "enterprise" } })
```

**For anonymous users** (not yet logged in):

```javascript
// User hasn't logged in yet, but we know something about them
FS('setProperties', {
  type: 'user',
  properties: {
    visitor_type: 'returning',
    referral_source: 'google_ads',
    landing_page: '/pricing',
  },
})
// These properties will be associated with the anonymous user
// and will persist if/when they later identify
```

### Property Persistence

- User properties persist across sessions
- Properties can be updated at any time
- New properties are added; existing properties are overwritten
- Properties cannot be deleted via the API (contact support)

### Special Fields

| Field         | Behavior                                            |
| ------------- | --------------------------------------------------- |
| `displayName` | Shown in session list and user card in Fullstory UI |
| `email`       | Enables email-based search and HTTP API lookups     |

---

## API Reference

### Basic Syntax

```javascript
FS('setProperties', {
  type: 'user',
  properties: object,     // Required: Key/value pairs
  schema?: object         // Optional: Type hints
});
```

### Parameters

| Parameter    | Type   | Required | Description                            |
| ------------ | ------ | -------- | -------------------------------------- |
| `type`       | string | **Yes**  | Must be `'user'` for user properties   |
| `properties` | object | **Yes**  | Key/value pairs of user data           |
| `schema`     | object | No       | Explicit type inference for properties |

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

### Example 1: Post-Identification Profile Enrichment

```javascript
// GOOD: Add properties after initial identification
// Step 1: Identify user on login (minimal properties)
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.name,
    email: user.email,
  },
})

// Step 2: Enrich with additional data once loaded
async function loadUserProfile() {
  const profile = await fetchUserProfile(user.id)

  FS('setProperties', {
    type: 'user',
    properties: {
      companyName: profile.company.name,
      companySize: profile.company.employeeCount,
      industry: profile.company.industry,
      role: profile.role,
      department: profile.department,
      signupSource: profile.attribution.source,
      referralCode: profile.attribution.referralCode,
    },
  })
}
```

**Why this is good:**

- ✅ Quick identification on login (doesn't block on profile load)
- ✅ Rich data added once available
- ✅ Clean separation of concerns
- ✅ Properties available for segmentation

### Example 2: Subscription/Plan Updates

```javascript
// GOOD: Track subscription changes without re-identifying
async function handlePlanUpgrade(newPlan) {
  // Process the upgrade
  await processUpgrade(newPlan)

  // Update user properties to reflect new plan
  FS('setProperties', {
    type: 'user',
    properties: {
      plan: newPlan.name,
      planTier: newPlan.tier,
      monthlyPrice: newPlan.price,
      billingCycle: newPlan.billingCycle,
      planChangedAt: new Date().toISOString(),
      previousPlan: getCurrentPlan().name,
    },
    schema: {
      monthlyPrice: 'real',
      planChangedAt: 'date',
    },
  })

  // Also track as an event for funnel analysis
  FS('trackEvent', {
    name: 'Plan Upgraded',
    properties: {
      fromPlan: getCurrentPlan().name,
      toPlan: newPlan.name,
      priceDifference: newPlan.price - getCurrentPlan().price,
    },
  })
}
```

**Why this is good:**

- ✅ Updates user properties without re-identification
- ✅ Tracks both current state (property) and change (event)
- ✅ Uses schema for proper type handling
- ✅ Captures before/after for analysis

### Example 3: Progressive Profiling (Onboarding)

```javascript
// GOOD: Build up user profile through onboarding steps
class OnboardingFlow {
  // Step 1: Basic info collected
  completeBasicInfo(data) {
    FS('setProperties', {
      type: 'user',
      properties: {
        companyName: data.companyName,
        companySize: data.companySize,
        onboardingStep: 1,
        onboardingStartedAt: new Date().toISOString(),
      },
      schema: {
        onboardingStep: 'int',
        onboardingStartedAt: 'date',
      },
    })
  }

  // Step 2: Use case selection
  completeUseCaseSelection(useCases) {
    FS('setProperties', {
      type: 'user',
      properties: {
        primaryUseCase: useCases.primary,
        secondaryUseCases: useCases.secondary, // Array of strings
        onboardingStep: 2,
      },
      schema: {
        secondaryUseCases: 'strs',
        onboardingStep: 'int',
      },
    })
  }

  // Step 3: Integration setup
  completeIntegrationSetup(integrations) {
    FS('setProperties', {
      type: 'user',
      properties: {
        connectedIntegrations: integrations.connected,
        integrationCount: integrations.connected.length,
        onboardingStep: 3,
      },
      schema: {
        connectedIntegrations: 'strs',
        integrationCount: 'int',
        onboardingStep: 'int',
      },
    })
  }

  // Final step: Mark complete
  completeOnboarding() {
    FS('setProperties', {
      type: 'user',
      properties: {
        onboardingComplete: true,
        onboardingCompletedAt: new Date().toISOString(),
        onboardingStep: 4,
      },
      schema: {
        onboardingComplete: 'bool',
        onboardingCompletedAt: 'date',
        onboardingStep: 'int',
      },
    })
  }
}
```

**Why this is good:**

- ✅ Builds profile incrementally
- ✅ Each step adds relevant properties
- ✅ Tracks progress via onboardingStep
- ✅ Enables segment analysis of drop-off points

### Example 4: Feature Usage Tracking

```javascript
// GOOD: Track feature adoption at user level
class FeatureUsageTracker {
  trackFeatureFirstUse(featureName) {
    const propertyName = `firstUsed_${featureName}`

    FS('setProperties', {
      type: 'user',
      properties: {
        [propertyName]: new Date().toISOString(),
      },
      schema: {
        [propertyName]: 'date',
      },
    })
  }

  updateFeatureEngagement(features) {
    FS('setProperties', {
      type: 'user',
      properties: {
        featuresUsed: features.used,
        mostUsedFeature: features.mostUsed,
        featureUsageScore: features.engagementScore,
        lastActiveFeature: features.lastUsed,
        lastFeatureUseAt: new Date().toISOString(),
      },
      schema: {
        featuresUsed: 'strs',
        featureUsageScore: 'int',
        lastFeatureUseAt: 'date',
      },
    })
  }
}

// Usage
const tracker = new FeatureUsageTracker()
tracker.trackFeatureFirstUse('advanced_export')
tracker.updateFeatureEngagement({
  used: ['dashboard', 'reports', 'advanced_export'],
  mostUsed: 'reports',
  engagementScore: 85,
  lastUsed: 'advanced_export',
})
```

**Why this is good:**

- ✅ Tracks feature adoption dates
- ✅ Maintains engagement metrics
- ✅ Enables feature-based segmentation
- ✅ Supports adoption analysis

### Example 5: CRM Data Sync

```javascript
// GOOD: Sync key CRM fields to Fullstory
async function syncCRMData(userId) {
  const crmData = await fetchFromCRM(userId)

  FS('setProperties', {
    type: 'user',
    properties: {
      // Sales/Account info
      accountOwner: crmData.owner.name,
      accountStage: crmData.stage,
      dealValue: crmData.opportunity.value,
      closeDate: crmData.opportunity.expectedClose,

      // Health metrics
      healthScore: crmData.health.score,
      churnRisk: crmData.health.churnRisk,
      npsScore: crmData.health.nps,

      // Engagement
      lastContactDate: crmData.lastContact,
      meetingsScheduled: crmData.meetings.scheduled,
      supportTicketsOpen: crmData.support.openTickets,

      // Sync metadata
      crmSyncedAt: new Date().toISOString(),
    },
    schema: {
      dealValue: 'real',
      closeDate: 'date',
      healthScore: 'int',
      churnRisk: 'real',
      npsScore: 'int',
      lastContactDate: 'date',
      meetingsScheduled: 'int',
      supportTicketsOpen: 'int',
      crmSyncedAt: 'date',
    },
  })
}
```

**Why this is good:**

- ✅ Bridges CRM and product analytics
- ✅ Enables sales context in session replay
- ✅ Supports health-based segmentation
- ✅ Tracks sync time for data freshness

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Using setProperties Instead of setIdentity

```javascript
// BAD: Trying to use setProperties for initial identification
FS('setProperties', {
  type: 'user',
  properties: {
    uid: user.id, // This won't work!
    displayName: user.name,
    email: user.email,
  },
})
```

**Why this is bad:**

- ❌ setProperties doesn't establish identity
- ❌ uid as a property doesn't link sessions
- ❌ User remains anonymous
- ❌ Misunderstanding of API purpose

**CORRECTED VERSION:**

```javascript
// GOOD: Use setIdentity for identification
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.name,
    email: user.email,
  },
})
```

### Example 2: Calling Before Identification

```javascript
// BAD: Setting user properties before user is identified
function updateUserPreferences(preferences) {
  // This won't persist properly if user is anonymous!
  FS('setProperties', {
    type: 'user',
    properties: {
      theme: preferences.theme,
      language: preferences.language,
    },
  })
}
```

**Why this is bad:**

- ❌ Properties on anonymous users are session-scoped
- ❌ Data won't persist across sessions
- ❌ Can't segment by these properties reliably

**CORRECTED VERSION:**

```javascript
// GOOD: Check identification status first
function updateUserPreferences(preferences) {
  // Only set user properties if identified
  if (isUserIdentified()) {
    FS('setProperties', {
      type: 'user',
      properties: {
        theme: preferences.theme,
        language: preferences.language,
      },
    })
  }
  // For anonymous users, consider page properties or just skip
}
```

### Example 3: Excessive Calls

```javascript
// BAD: Calling setProperties too frequently
function handleFormFieldChange(fieldName, value) {
  // BAD: This fires on every keystroke!
  FS('setProperties', {
    type: 'user',
    properties: {
      [`form_${fieldName}`]: value,
    },
  })
}
```

**Why this is bad:**

- ❌ Will hit rate limits (30/min, 10/sec)
- ❌ Wastes API calls on intermediate states
- ❌ Transient form data isn't good for user properties

**CORRECTED VERSION:**

```javascript
// GOOD: Batch updates on form submission
function handleFormSubmit(formData) {
  // Set meaningful final values
  FS('setProperties', {
    type: 'user',
    properties: {
      preferredContact: formData.contactMethod,
      marketingOptIn: formData.optIn,
      timezone: formData.timezone,
    },
  })

  // Track the form submission as event
  FS('trackEvent', {
    name: 'Preferences Updated',
    properties: formData,
  })
}
```

### Example 4: Wrong Type for Properties

```javascript
// BAD: Missing type parameter
FS('setProperties', {
  properties: {
    plan: 'premium',
  },
  // Missing type: 'user'!
})
```

**Why this is bad:**

- ❌ Missing required `type` parameter
- ❌ API call will fail or behave unexpectedly
- ❌ Easy to miss in testing

**CORRECTED VERSION:**

```javascript
// GOOD: Include type parameter
FS('setProperties', {
  type: 'user', // Required!
  properties: {
    plan: 'premium',
  },
})
```

### Example 5: Type Mismatches

```javascript
// BAD: Incorrect value formats
FS('setProperties', {
  type: 'user',
  properties: {
    accountBalance: '$1,234.56', // BAD: Formatted currency
    loginCount: 'forty-two', // BAD: Written number
    isPremium: 'yes', // BAD: String instead of boolean
    signupDate: 'January 15, 2024', // BAD: Not ISO8601
  },
  schema: {
    accountBalance: 'real',
    loginCount: 'int',
    isPremium: 'bool',
    signupDate: 'date',
  },
})
```

**Why this is bad:**

- ❌ Values don't match declared types
- ❌ Parsing will fail
- ❌ Properties won't be queryable correctly

**CORRECTED VERSION:**

```javascript
// GOOD: Properly formatted values
FS('setProperties', {
  type: 'user',
  properties: {
    accountBalance: 1234.56,
    currency: 'USD', // Separate field for formatting
    loginCount: 42,
    isPremium: true,
    signupDate: '2024-01-15T00:00:00Z',
  },
  schema: {
    accountBalance: 'real',
    loginCount: 'int',
    isPremium: 'bool',
    signupDate: 'date',
  },
})
```

### Example 6: Overwriting Important Properties

```javascript
// BAD: Carelessly overwriting displayName
function updateLastActivity() {
  FS('setProperties', {
    type: 'user',
    properties: {
      displayName: 'Active User', // BAD: Overwrites the real name!
      lastActivityAt: new Date().toISOString(),
    },
  })
}
```

**Why this is bad:**

- ❌ Overwrites displayName with generic value
- ❌ Loses actual user name in Fullstory UI
- ❌ Makes sessions hard to identify

**CORRECTED VERSION:**

```javascript
// GOOD: Only update intended properties
function updateLastActivity() {
  FS('setProperties', {
    type: 'user',
    properties: {
      lastActivityAt: new Date().toISOString(),
      isRecentlyActive: true,
    },
    schema: {
      lastActivityAt: 'date',
      isRecentlyActive: 'bool',
    },
  })
}
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Property Manager Class

```javascript
// Centralized user property management
class UserPropertyManager {
  constructor() {
    this.pendingProperties = {}
    this.flushTimeout = null
  }

  // Queue properties for batched update
  queue(properties, schema = {}) {
    Object.assign(this.pendingProperties, properties)

    // Debounce to batch rapid updates
    if (this.flushTimeout) clearTimeout(this.flushTimeout)
    this.flushTimeout = setTimeout(() => this.flush(), 1000)
  }

  // Immediately send properties
  flush() {
    if (Object.keys(this.pendingProperties).length === 0) return

    FS('setProperties', {
      type: 'user',
      properties: this.pendingProperties,
    })

    this.pendingProperties = {}
    this.flushTimeout = null
  }

  // Update specific category of properties
  updateEngagement(data) {
    this.queue({
      lastActiveAt: new Date().toISOString(),
      sessionCount: data.sessionCount,
      pageViewsTotal: data.pageViews,
    })
  }

  updateSubscription(plan) {
    // Subscription updates are important - flush immediately
    FS('setProperties', {
      type: 'user',
      properties: {
        plan: plan.name,
        planTier: plan.tier,
        planUpdatedAt: new Date().toISOString(),
      },
    })
  }
}
```

### Pattern 2: Property Sync on Page Load

```javascript
// Sync important properties on each page load
async function syncUserProperties() {
  const user = await getCurrentUser()
  if (!user) return

  // Fetch latest data
  const [profile, subscription, usage] = await Promise.all([
    fetchProfile(user.id),
    fetchSubscription(user.id),
    fetchUsageStats(user.id),
  ])

  // Sync to Fullstory
  FS('setProperties', {
    type: 'user',
    properties: {
      // Profile
      displayName: profile.fullName,
      email: profile.email,
      role: profile.role,

      // Subscription
      plan: subscription.plan,
      planStatus: subscription.status,
      mrr: subscription.mrr,

      // Usage
      lastLoginAt: usage.lastLogin,
      totalLogins: usage.loginCount,
      daysActive: usage.activeDays,
    },
    schema: {
      mrr: 'real',
      lastLoginAt: 'date',
      totalLogins: 'int',
      daysActive: 'int',
    },
  })
}

// Run on app initialization
initApp().then(syncUserProperties)
```

### Pattern 3: Event-Driven Property Updates

```javascript
// Update properties based on key events
const eventPropertyMap = {
  trial_started: (event) => ({
    trialStartedAt: new Date().toISOString(),
    trialPlan: event.plan,
    isTrialing: true,
  }),

  trial_converted: (event) => ({
    trialConvertedAt: new Date().toISOString(),
    isTrialing: false,
    isPaying: true,
    plan: event.plan,
  }),

  trial_expired: (event) => ({
    trialExpiredAt: new Date().toISOString(),
    isTrialing: false,
    isPaying: false,
  }),

  feature_enabled: (event) => ({
    [`feature_${event.feature}_enabled`]: true,
    [`feature_${event.feature}_enabledAt`]: new Date().toISOString(),
  }),
}

function handleBusinessEvent(eventName, eventData) {
  // Track the event
  FS('trackEvent', {
    name: eventName,
    properties: eventData,
  })

  // Update user properties if mapping exists
  const propertyUpdater = eventPropertyMap[eventName]
  if (propertyUpdater) {
    FS('setProperties', {
      type: 'user',
      properties: propertyUpdater(eventData),
    })
  }
}
```

---

## RELATIONSHIP WITH OTHER APIs

### setIdentity + setProperties Workflow

```javascript
// Initial identification with core properties
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.name,
    email: user.email,
  },
})

// Later: add more properties
FS('setProperties', {
  type: 'user',
  properties: {
    company: companyData.name,
    role: roleData.title,
  },
})
```

### setProperties (user) vs setProperties (page)

```javascript
// User properties: persist across sessions, about the person
FS('setProperties', {
  type: 'user',
  properties: {
    plan: 'enterprise',
    accountAge: 365,
  },
})

// Page properties: session-scoped, about the current context
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Dashboard',
    filters: ['active', 'recent'],
  },
})
```

### setProperties vs trackEvent

```javascript
// Properties: current state (what IS)
FS('setProperties', {
  type: 'user',
  properties: {
    plan: 'professional',
    seats: 10,
  },
})

// Events: actions/changes (what HAPPENED)
FS('trackEvent', {
  name: 'Plan Upgraded',
  properties: {
    from: 'starter',
    to: 'professional',
    seatChange: 5,
  },
})
```

---

## TROUBLESHOOTING

### Properties Not Appearing

**Symptom**: User properties don't show in Fullstory

**Common Causes**:

1. ❌ User not identified first
2. ❌ Missing `type: 'user'` parameter
3. ❌ Type mismatches in values
4. ❌ Rate limits exceeded

**Solutions**:

- ✅ Ensure setIdentity called first
- ✅ Always include `type: 'user'`
- ✅ Use schema for explicit typing
- ✅ Batch updates to avoid rate limits

### Properties Show Wrong Values

**Symptom**: Property values are incorrect or unexpected type

**Common Causes**:

1. ❌ Value format doesn't match schema type
2. ❌ Formatted strings for numeric values
3. ❌ Boolean as string ("true" vs true)

**Solutions**:

- ✅ Use clean numeric values
- ✅ Use actual boolean types
- ✅ Format dates as ISO8601
- ✅ Specify schema explicitly

### displayName Keeps Getting Overwritten

**Symptom**: User's display name changes unexpectedly

**Common Causes**:

1. ❌ Multiple places setting displayName
2. ❌ Automated scripts overwriting
3. ❌ Race conditions in property updates

**Solutions**:

- ✅ Set displayName only in identification flow
- ✅ Audit all setProperties calls
- ✅ Use dedicated fields for other "name" data

---

## LIMITS AND CONSTRAINTS

### Property Limits

- Check your Fullstory plan for specific limits
- Property names: alphanumeric, underscores, hyphens
- Avoid high-cardinality properties

### Call Frequency

- **Sustained**: 30 calls per page per minute
- **Burst**: 10 calls per second

### Value Requirements

- Strings: Must be valid UTF-8
- Numbers: Standard JSON number format
- Dates: ISO8601 format
- Arrays: Maximum length varies by plan

---

## KEY TAKEAWAYS FOR AGENT

When helping developers implement User Properties:

1. **Always emphasize**:
   - User must be identified first (setIdentity)
   - Include `type: 'user'` parameter
   - Use schema for non-string types
   - Batch updates to respect rate limits

2. **Common mistakes to watch for**:
   - Missing type parameter
   - Setting properties before identification
   - Excessive call frequency
   - Type mismatches in values
   - Overwriting displayName accidentally

3. **Questions to ask developers**:
   - Will the user be anonymous or identified? (Both work - setProperties doesn't require identification)
   - How often will these properties be updated?
   - What data types are these values?
   - Do you need to track the change as an event too?

4. **Best practices to recommend**:
   - Set core properties in setIdentity
   - Use setProperties for subsequent updates
   - Track important changes as events too
   - Consider property batching for frequent updates

---

## REFERENCE LINKS

- **Set User Properties**: https://developer.fullstory.com/browser/identification/set-user-properties/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Identify Users**: https://developer.fullstory.com/browser/identification/identify-users/
- **Help Center - Custom Properties**: https://help.fullstory.com/hc/en-us/articles/360020623234

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's User Properties API correctly for web applications._
