---
name: fullstory-privacy-strategy
version: v2
description: Strategic guide for data privacy in Fullstory implementations. Teaches developers how to decide what data to send, mask, exclude, hash, or replace with joinable keys. Covers regulatory compliance (GDPR, HIPAA, PCI, CCPA), privacy-by-design principles, and balancing analytics value with privacy protection. Acts as a decision framework that references core privacy skills.
related_skills:
  - fullstory-privacy-controls
  - fullstory-user-consent
  - fullstory-identify-users
  - fullstory-user-properties
  - fullstory-analytics-events
  - fullstory-banking
  - fullstory-healthcare
  - fullstory-gaming
  - fullstory-ecommerce
  - fullstory-saas
  - fullstory-travel
  - fullstory-media-entertainment
---

# Fullstory Privacy Strategy

## Overview

This guide provides strategic guidance for implementing privacy-conscious Fullstory semantic decoration. It helps developers decide:

- What data to send to Fullstory
- What data to never send
- What data to hash/encrypt before sending
- When to use joinable keys instead of raw data
- How to balance analytics value with privacy protection

**Remember**: Fullstory is a tool for understanding user experience, NOT a database for storing customer data. Send only what's needed for analysis.

---

## Fullstory's Privacy Architecture

### First-Party Cookies (Not Third-Party)

Fullstory uses **first-party cookies** set on YOUR domain, which provides inherent privacy benefits:

| Privacy Aspect            | Fullstory Approach                                                   |
| ------------------------- | -------------------------------------------------------------------- |
| **Cookie Domain**         | Set on YOUR domain (e.g., `yoursite.com`), not Fullstory's           |
| **Cross-Site Tracking**   | ❌ Impossible - each site has its own isolated `fs_uid` cookie       |
| **Data Isolation**        | Your user data is completely isolated from other Fullstory customers |
| **Browser Compatibility** | ✅ First-party cookies aren't blocked by browsers or ad-blockers     |
| **User Control**          | Users can clear cookies to reset their identity on your site         |

> **Key Privacy Guarantee**: A user's identity CANNOT be connected across different sites using Fullstory. If the same person visits Site A and Site B (both using Fullstory), they have separate, unlinked identities on each site.

### Cookie Transparency

| Cookie   | Duration | Purpose                          | User Impact                |
| -------- | -------- | -------------------------------- | -------------------------- |
| `fs_uid` | 1 year   | Links sessions from same browser | Can clear to "start fresh" |
| `fs_cid` | 1 year   | Stores consent state             | Remembers consent choice   |
| `fs_lua` | 30 min   | Last activity timestamp          | Session timeout management |

> **Reference**: [Why Fullstory uses First-Party Cookies](https://help.fullstory.com/hc/en-us/articles/360020829513-Why-Fullstory-uses-First-Party-Cookies)

### Private by Default Mode

Fullstory offers a **Private by Default** mode—a privacy-first capture approach that inverts the default behavior:

| Mode                   | Default Behavior                                      | Best For                      |
| ---------------------- | ----------------------------------------------------- | ----------------------------- |
| **Standard**           | Capture everything, add fs-mask/fs-exclude to protect | Low-sensitivity sites         |
| **Private by Default** | Mask everything, add fs-unmask to reveal              | High-sensitivity applications |

**How Private by Default Works:**

1. **All text is masked by default** - No text captured unless explicitly unmasked
2. **Zero accidental exposure** - Impossible to accidentally capture sensitive data
3. **Selective unmasking** - Add `.fs-unmask` to navigation, buttons, product names
4. **Session replay shows wireframes** - See user behavior without seeing data

**Recommended for:**

- ✅ Healthcare applications (HIPAA)
- ✅ Banking/financial services (PCI, GLBA)
- ✅ Multi-tenant SaaS (customer data protection)
- ✅ Enterprise applications
- ✅ Any application where "default open" is too risky

**Enable via:**

- **New accounts**: Select during onboarding wizard
- **Existing accounts**: Contact Fullstory Support

> **Reference**: [Fullstory Private by Default](https://help.fullstory.com/hc/en-us/articles/360044349073-Fullstory-Private-by-Default)

---

## Core Privacy Principles

### 1. Minimum Necessary Data

> "Capture only what you need to understand the user experience."

| Data Category    | Ask Yourself                   | Recommendation                |
| ---------------- | ------------------------------ | ----------------------------- |
| User identifiers | Do I need to link sessions?    | Use hashed/internal IDs       |
| Names            | Do I need the actual name?     | Mask or use initials          |
| Emails           | Is email essential for lookup? | Hash or use user ID           |
| Addresses        | Do I need full address?        | Mask street, keep city/state  |
| Financial        | Do I need actual amounts?      | Use ranges ("$100-$500")      |
| Health           | Is this needed at all?         | Usually NO - exclude entirely |

### 2. Privacy by Design

Build privacy into your semantic decoration from the start, not as an afterthought:

```
┌───────────────────────────────────────────────────────────────┐
│  PHASE 1: DESIGN                                               │
│  - Identify all data fields                                    │
│  - Classify by sensitivity                                     │
│  - Determine minimum needed for analysis                       │
├───────────────────────────────────────────────────────────────┤
│  PHASE 2: IMPLEMENT                                            │
│  - Apply privacy controls (exclude/mask/unmask)                │
│  - Hash or tokenize identifiers                                │
│  - Use joinable keys for linkage                               │
├───────────────────────────────────────────────────────────────┤
│  PHASE 3: VERIFY                                               │
│  - Review session replays                                      │
│  - Audit captured properties/events                            │
│  - Test edge cases (errors, modals, dynamic content)           │
├───────────────────────────────────────────────────────────────┤
│  PHASE 4: MAINTAIN                                             │
│  - Regular privacy audits                                      │
│  - Update for new features/fields                              │
│  - Monitor for accidental exposure                             │
└───────────────────────────────────────────────────────────────┘
```

### 3. Data Classification Framework

| Classification   | Examples                       | Fullstory Handling                |
| ---------------- | ------------------------------ | --------------------------------- |
| **Public**       | Product names, prices, UI text | Unmask                            |
| **Internal**     | Order IDs, session IDs         | Send as-is or hash                |
| **Confidential** | Names, emails, addresses       | Mask or hash                      |
| **Restricted**   | SSN, credit cards, passwords   | Exclude always                    |
| **Regulated**    | Health data, financial data    | Exclude + comply with regulations |

---

## Decision Matrix: What Data to Send

### User Identification

| Approach         | When to Use                  | Example                                    |
| ---------------- | ---------------------------- | ------------------------------------------ |
| **Internal ID**  | Always preferred             | `setIdentity({ uid: "user_12345" })`       |
| **Hashed email** | Need email linkage           | `setIdentity({ uid: sha256(email) })`      |
| **Raw email**    | Only if required for support | `setIdentity({ uid: "user@example.com" })` |
| **Joinable key** | Link to external system      | `setIdentity({ uid: "cust_abc123" })`      |

### User Properties

| Data Type                  | Send Raw?   | Hash? | Joinable Key?   | Exclude?      |
| -------------------------- | ----------- | ----- | --------------- | ------------- |
| Account ID                 | ✅          |       |                 |               |
| Account tier (Gold/Silver) | ✅          |       |                 |               |
| Company name               | ⚠️ Consider |       | ✅ `company_id` |               |
| User's full name           |             |       | ✅ `user_id`    | ⚠️ Mask       |
| Email                      |             | ✅    | ✅ `user_id`    |               |
| Phone                      |             |       |                 | ❌ Don't send |
| Address                    |             |       |                 | ❌ Don't send |
| SSN/Tax ID                 |             |       |                 | ❌ Never      |
| Account balance            | ⚠️ Ranges   |       |                 |               |
| Credit score               |             |       |                 | ❌ Never      |

### Event Properties

| Data Type              | Recommendation | Example                                   |
| ---------------------- | -------------- | ----------------------------------------- |
| Product ID             | Send raw       | `{ product_id: "SKU-123" }`               |
| Product name           | Send raw       | `{ product_name: "Wireless Headphones" }` |
| Price                  | Send raw       | `{ price: 199.99 }`                       |
| Quantity               | Send raw       | `{ quantity: 2 }`                         |
| Order ID               | Send raw       | `{ order_id: "ORD-789" }`                 |
| Search query           | ⚠️ Consider    | May contain PII                           |
| Error message          | ⚠️ Sanitize    | May contain PII                           |
| User-generated content | ⚠️ Consider    | Comments, reviews                         |

---

## Joinable Keys Strategy

Instead of sending sensitive data to Fullstory, send an identifier that can be joined in your analytics warehouse:

### The Pattern

```
                    Fullstory                    Your Data Warehouse
                    ┌─────────────────┐          ┌─────────────────────┐
User Session:       │ user_id: "u123" │    →     │ user_id: "u123"     │
                    │ session_events  │          │ email: "john@co.com" │
                    │ page_views      │          │ name: "John Smith"   │
                    └─────────────────┘          │ ssn: "***-**-****"   │
                                                 └─────────────────────┘
                           ↓
                    JOIN ON user_id
                           ↓
                    ┌─────────────────────────────────────────────┐
                    │ Combined analytics with full PII context   │
                    │ (in YOUR secure data warehouse)             │
                    └─────────────────────────────────────────────┘
```

### Implementation Example

```javascript
// BAD: Sending PII directly to Fullstory
FS('setIdentity', {
  uid: user.email, // PII!
  displayName: user.fullName, // PII!
  email: user.email, // PII!
})

FS('setProperties', {
  type: 'user',
  properties: {
    ssn: user.ssn, // NEVER!
    phone: user.phone, // PII!
    address: user.address, // PII!
  },
})

// GOOD: Using joinable keys
FS('setIdentity', {
  uid: user.internalId, // Not PII, just an ID
})

FS('setProperties', {
  type: 'user',
  properties: {
    // Business context, not PII
    account_tier: user.tier,
    signup_date: user.createdAt,
    plan_type: user.subscription.plan,

    // Joinable keys for your warehouse
    crm_id: user.salesforceId, // Join to Salesforce
    support_id: user.zendeskId, // Join to Zendesk
  },
})
```

### Joinable Keys for Common Systems

| System      | Key to Send             | Join In Warehouse          |
| ----------- | ----------------------- | -------------------------- |
| Salesforce  | `salesforce_account_id` | Account, Contact objects   |
| HubSpot     | `hubspot_contact_id`    | Contact properties         |
| Zendesk     | `zendesk_user_id`       | User tickets, interactions |
| Stripe      | `stripe_customer_id`    | Payment, subscription data |
| Segment     | `segment_user_id`       | Full user profile          |
| Internal DB | `user_id`, `account_id` | All internal data          |

---

## Hashing Strategy

When you need to identify users but can't use internal IDs:

### When to Hash

| Scenario                          | Recommendation                           |
| --------------------------------- | ---------------------------------------- |
| Need email for session linking    | Hash email                               |
| Multiple systems use email as key | Hash email                               |
| Legal requires pseudonymization   | Hash all PII                             |
| Support needs to find user        | Consider: do they need Fullstory or CRM? |

### Hash Implementation

> ⚠️ **SECURITY WARNING**: Client-side hashing is **NOT a security control** - it's only a privacy measure. JavaScript code is inspectable, and unsalted hashes are reversible via rainbow tables. **True security requires server-side processing.** Use hashing only to prevent accidental PII exposure in Fullstory, not to protect against determined attackers.

```javascript
// PREFERRED: Hash on your backend, pass to frontend
// This keeps the hashing logic and any salt server-side
const userFromAPI = await fetchUser() // { id, hashedEmail: "5e884..." }

FS('setIdentity', {
  uid: userFromAPI.hashedEmail,
})

// ---

// ALTERNATIVE: Client-side hashing (less secure, but better than raw PII)
async function hashForFullstory(value) {
  const encoder = new TextEncoder()
  const data = encoder.encode(value.toLowerCase().trim())
  const hashBuffer = await crypto.subtle.digest('SHA-256', data)
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('')
}

const hashedEmail = await hashForFullstory(user.email)

FS('setIdentity', {
  uid: hashedEmail, // e.g., "5e884898da28047d..."
})
```

### Important Considerations

1. **Server-side hashing is preferred**: Hash on backend, send hash to client
2. **Consistent hashing**: Always lowercase, trim whitespace before hashing
3. **Salt optional for Fullstory**: Unsalted hashes allow you to join later
4. **Document mapping**: Keep record of hash → original for support lookups
5. **Not a security measure**: Hashing prevents accidental exposure, not malicious extraction

---

## Regulatory Compliance Guide

### GDPR (Europe)

| Requirement               | Fullstory Approach                               |
| ------------------------- | ------------------------------------------------ |
| Consent before processing | Use `FS('setIdentity', { consent: true/false })` |
| Right to be forgotten     | Use Fullstory's deletion API                     |
| Data minimization         | Use joinable keys, not raw PII                   |
| Purpose limitation        | Only capture UX-relevant data                    |
| Pseudonymization          | Hash identifiers                                 |

```javascript
// GDPR-compliant identification
function identifyUserGDPR(user, hasConsent) {
  FS('setIdentity', {
    uid: hashEmail(user.email), // Pseudonymized
    consent: hasConsent, // Explicit consent
  })

  if (hasConsent) {
    FS('setProperties', {
      type: 'user',
      properties: {
        // Only essential, non-PII data
        account_tier: user.tier,
        country: user.country, // May be needed for analysis
        language: user.language,
      },
    })
  }
}
```

### HIPAA (Healthcare - USA)

| Requirement       | Fullstory Approach                 |
| ----------------- | ---------------------------------- |
| PHI protection    | Exclude ALL health-related content |
| Minimum necessary | Capture only UX metrics            |
| Audit trail       | Use Fullstory's audit logs         |
| BAA required      | Ensure signed with Fullstory       |

```javascript
// HIPAA-compliant approach
// DO NOT capture:
// - Diagnoses, conditions
// - Medications
// - Treatment plans
// - Provider names
// - Insurance info
// - Any PHI

FS('setIdentity', {
  uid: patient.internalId, // Not PHI
})

FS('setProperties', {
  type: 'user',
  properties: {
    // OK: Non-PHI operational data
    portal_type: 'patient',
    preferred_language: 'en',
    login_method: 'SSO',

    // NOT OK - do not include:
    // diagnosis: patient.conditions  ❌
    // provider: patient.doctorName   ❌
  },
})
```

### PCI DSS (Payment Cards)

| Data Type       | Allowed in Fullstory?    |
| --------------- | ------------------------ |
| Card number     | ❌ Never (auto-excluded) |
| CVV/CVC         | ❌ Never (auto-excluded) |
| Expiry date     | ❌ Never (exclude)       |
| Cardholder name | ❌ No (exclude)          |
| Last 4 digits   | ⚠️ Maybe (for reference) |
| Card brand      | ✅ Yes (Visa, MC)        |
| Transaction ID  | ✅ Yes                   |
| Amount          | ✅ Yes                   |

```javascript
// PCI-compliant event tracking
FS('trackEvent', {
  name: 'purchase_completed',
  properties: {
    // OK: Non-sensitive transaction data
    order_id: order.id,
    amount: order.total,
    currency: order.currency,
    card_brand: order.payment.cardBrand, // "Visa"

    // NOT OK - do not include:
    // card_number: order.payment.number  ❌
    // cvv: order.payment.cvv             ❌
  },
})
```

### CCPA (California - USA)

| Requirement        | Fullstory Approach                    |
| ------------------ | ------------------------------------- |
| Right to know      | Document what Fullstory captures      |
| Right to delete    | Use Fullstory's deletion API          |
| Right to opt-out   | Use consent API                       |
| Non-discrimination | Same experience regardless of opt-out |

---

## Data Category Decision Trees

### User Identification Decision Tree

```
Should I send this identifier to Fullstory?
│
├─ Is it an internal ID (no PII)?
│  └─ YES → Send as uid ✅
│
├─ Is it an email address?
│  ├─ Is email required for support lookup?
│  │  ├─ YES → Consider: Can support use internal system instead?
│  │  │  ├─ YES → Send hashed email or internal ID
│  │  │  └─ NO → Send email (document justification)
│  │  └─ NO → Send hashed email
│  └─ Can you link via internal ID?
│     └─ YES → Use internal ID instead
│
├─ Is it a phone number?
│  └─ → Don't send, use internal ID ❌
│
├─ Is it a username?
│  └─ → Could be PII, prefer internal ID
│
└─ Is it SSN/Tax ID/Government ID?
   └─ → NEVER send ❌❌❌
```

### Property Decision Tree

```
Should I send this property to Fullstory?
│
├─ Is it regulated data (PHI, financial details)?
│  └─ YES → Don't send ❌
│
├─ Does it contain PII?
│  ├─ Is PII necessary for analysis?
│  │  ├─ YES → Can you generalize? (age range vs DOB)
│  │  │  ├─ YES → Send generalized
│  │  │  └─ NO → Document justification, minimize
│  │  └─ NO → Don't send, use joinable key
│  └─ Can you use a joinable key instead?
│     └─ YES → Send key, join in warehouse
│
├─ Is it business context (tier, plan, industry)?
│  └─ YES → Send ✅
│
├─ Is it behavioral (feature flags, A/B variant)?
│  └─ YES → Send ✅
│
└─ Is it operational (version, platform)?
   └─ YES → Send ✅
```

---

## Common Patterns by Data Type

### Names

```javascript
// Options for handling names

// Option 1: Don't send at all (use joinable key)
FS('setIdentity', {uid: user.id})
// Look up name in your CRM/database

// Option 2: Send only first name (if needed for greetings analysis)
FS('setProperties', {
  type: 'user',
  properties: {
    first_name_initial: user.firstName.charAt(0),
  },
})

// Option 3: Mask in UI, don't send as property
// (handled by fs-mask class in HTML)
```

### Email Addresses

```javascript
// Options for handling emails

// Option 1: Internal ID (preferred)
FS('setIdentity', {uid: user.id})

// Option 2: Hashed email (for cross-system linking)
FS('setIdentity', {uid: sha256(user.email.toLowerCase())})

// Option 3: Email domain only (for B2B analysis)
FS('setProperties', {
  type: 'user',
  properties: {
    email_domain: user.email.split('@')[1], // "company.com"
  },
})
```

### Monetary Values

```javascript
// Options for handling money

// Option 1: Send actual values (usually OK for transactions)
FS('trackEvent', {
  name: 'purchase',
  properties: {
    amount: 149.99,
    currency: 'USD',
  },
})

// Option 2: Send ranges (for sensitive financial data)
function getAmountRange(amount) {
  if (amount < 100) return '$0-$100'
  if (amount < 500) return '$100-$500'
  if (amount < 1000) return '$500-$1000'
  return '$1000+'
}

FS('setProperties', {
  type: 'user',
  properties: {
    account_balance_range: getAmountRange(user.balance),
  },
})

// Option 3: Percentiles (for comparative analysis)
FS('setProperties', {
  type: 'user',
  properties: {
    spending_percentile: user.spendingPercentile, // 75
  },
})
```

### Dates

```javascript
// Options for handling dates

// Option 1: Full date (usually OK for non-sensitive)
FS('setProperties', {
  type: 'user',
  properties: {
    signup_date: user.createdAt.toISOString(),
  },
})

// Option 2: Relative time (for age-sensitive data)
function getAgeRange(birthDate) {
  const age = calculateAge(birthDate)
  if (age < 18) return 'under-18'
  if (age < 25) return '18-24'
  if (age < 35) return '25-34'
  // etc.
}

FS('setProperties', {
  type: 'user',
  properties: {
    age_range: getAgeRange(user.dateOfBirth),
  },
})

// Option 3: Don't send DOB (link via joinable key)
```

### Locations

```javascript
// Options for handling location

// Option 1: Country/region only (usually OK)
FS('setProperties', {
  type: 'user',
  properties: {
    country: user.address.country,
    region: user.address.state,
  },
})

// Option 2: City (if needed for analysis)
FS('setProperties', {
  type: 'user',
  properties: {
    metro_area: user.address.city, // Consider privacy implications
  },
})

// Option 3: Don't send address details
// Full addresses are PII - mask in UI, don't send as properties
```

---

## Privacy Audit Checklist

Use this checklist before launch and periodically:

### Session Replay Audit

- [ ] Watch 10 random replays from each user type
- [ ] Check all form fields for proper masking/exclusion
- [ ] Verify error messages don't expose PII
- [ ] Check modals and pop-ups for sensitive content
- [ ] Review any user-generated content areas
- [ ] Verify third-party widgets are properly handled

### Properties Audit

- [ ] List all `setIdentity` calls and their values
- [ ] List all `setProperties` calls (user and page)
- [ ] List all `trackEvent` calls and their properties
- [ ] For each: Is this data necessary? Is it minimized?
- [ ] Verify no regulated data in properties
- [ ] Check that joinable keys are used where appropriate

### Console/Network Audit

- [ ] Check if console capture is enabled
- [ ] If yes, verify no PII in console logs
- [ ] Review network request capture settings
- [ ] Verify sensitive APIs are excluded

### Compliance Verification

- [ ] Consent mechanism implemented (if required)
- [ ] Deletion API integrated (if required)
- [ ] Privacy policy updated
- [ ] Team trained on privacy requirements

---

## KEY TAKEAWAYS FOR AGENT

When helping developers with privacy strategy:

1. **Default to privacy**: When in doubt, don't send it
2. **Joinable keys are your friend**: Send IDs, join PII in warehouse
3. **Hash when needed**: For cross-system linking without raw PII
4. **Know the regulations**: GDPR, HIPAA, PCI, CCPA have specific requirements
5. **Audit regularly**: Privacy leaks happen with new features

### Questions to Ask Developers

1. "What regulations apply to your business?"
2. "Can you use an internal ID instead of email?"
3. "Is this data necessary for understanding UX?"
4. "Can you join this data in your warehouse instead?"
5. "Have you tested session replay for PII exposure?"

### Common Mistakes to Watch For

- Sending email as uid when internal ID exists
- Including PII in event properties "for debugging"
- Not masking dynamically loaded content
- Forgetting about console log capture
- Assuming auto-detection catches everything

---

## REFERENCE LINKS

### Core Skills

- [Privacy Controls](../core/fullstory-privacy-controls/SKILL.md) - Technical implementation
- [User Consent](../core/fullstory-user-consent/SKILL.md) - Consent API
- [Identify Users](../core/fullstory-identify-users/SKILL.md) - User identification

### Fullstory Documentation

- **Privacy Overview**: https://help.fullstory.com/hc/en-us/articles/360020623574
- **Private by Default**: https://help.fullstory.com/hc/en-us/articles/360044349073
- **Data Deletion API**: https://developer.fullstory.com/deletion
- **GDPR Compliance**: https://www.fullstory.com/legal/gdpr

---

_This skill document provides strategic guidance for privacy-conscious Fullstory implementations. Always consult your legal and compliance teams for specific regulatory requirements._
