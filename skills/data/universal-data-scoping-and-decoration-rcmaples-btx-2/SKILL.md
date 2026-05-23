---
name: fullstory-data-scoping-decoration
version: v2
description: Strategic meta-skill for Fullstory data semantic decoration. Teaches when to use page properties vs element properties vs user properties vs events. Provides a deterministic framework for scoping data at the right level to maximize searchability, avoid duplication, and maintain consistency. Essential foundation for proper Fullstory implementation across all API types.
related_skills:
  - fullstory-page-properties
  - fullstory-element-properties
  - fullstory-user-properties
  - fullstory-analytics-events
  - fullstory-identify-users
  - fullstory-getting-started
  - fullstory-privacy-controls
  - fullstory-privacy-strategy
  - fullstory-banking
  - fullstory-ecommerce
  - fullstory-gaming
  - fullstory-healthcare
  - fullstory-saas
  - fullstory-travel
  - fullstory-media-entertainment
---

# Universal Data Scoping and Decoration: The Unified Model (v4.0)

> A deterministic strategy for applying high-signal data attributes across web interfaces. Separate user context from page context from element context to maximize efficiency, searchability, and consistency.

---

## Overview

This meta-skill provides the strategic framework for deciding **where** to capture data in Fullstory. Before implementing any Fullstory API, use this guide to determine the appropriate scope for your data.

### The Data Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│  USER PROPERTIES (FS setIdentity / setProperties)           │
│  Scope: Across all sessions for this user                   │
│  Examples: plan, role, company, signup_date                 │
├─────────────────────────────────────────────────────────────┤
│  PAGE PROPERTIES (FS setProperties type: 'page')            │
│  Scope: Current page until URL path changes                 │
│  Examples: pageName, searchTerm, filters, productId         │
├─────────────────────────────────────────────────────────────┤
│  ELEMENT PROPERTIES (data-fs-properties-schema)             │
│  Scope: Individual element interactions                     │
│  Examples: itemId, position, variant, price                 │
├─────────────────────────────────────────────────────────────┤
│  EVENT PROPERTIES (FS trackEvent)                           │
│  Scope: Single discrete action                              │
│  Examples: orderId, revenue, source, action                 │
└─────────────────────────────────────────────────────────────┘
```

---

## I. Core Principles: Data Scope and Responsibility

### Rule 1: Capture Data at the Highest Relevant Scope

**Why?**

- Reduces duplication
- Improves searchability
- Makes data inheritance work correctly
- Simplifies semantic decoration

**Decision Matrix:**

| Data Characteristic           | Scope to Use       | API                                   |
| ----------------------------- | ------------------ | ------------------------------------- |
| Same for all user sessions    | User Properties    | `setIdentity` / `setProperties(user)` |
| Same for entire page          | Page Properties    | `setProperties(page)`                 |
| Different per element on page | Element Properties | `data-fs-*` attributes                |
| Discrete action/moment        | Event              | `trackEvent`                          |

### Rule 2: Never Duplicate Across Scopes

❌ **BAD**: Product ID on page AND on every element

```javascript
// Page properties
FS('setProperties', {type: 'page', properties: {productId: 'SKU-123'}})

// Also on element (REDUNDANT!)
;<button data-product-id="SKU-123">Add to Cart</button>
```

✅ **GOOD**: Product ID at page level only

```javascript
// Page properties (single source of truth)
FS('setProperties', {type: 'page', properties: {productId: 'SKU-123'}})

// Element just has element-specific data
;<button data-fs-element="Add to Cart Button">Add to Cart</button>
```

### Rule 3: Let Inheritance Work

Fullstory's property inheritance:

- **User properties** → Available on all sessions for that user
- **Page properties** → Available on all elements/events on that page
- **Element properties** → Inherited by child elements, AND child properties bubble up to parent on interaction

**Important: Child → Parent Inheritance**

When a user interacts with a parent element (e.g., clicks a form submit button), Fullstory captures properties from ALL child elements that have been interacted with:

```html
<form data-fs-element="CheckoutForm">
  <select
    data-fs-element="ShippingMethod"
    data-fs-properties-schema='{"value": {"type": "str", "name": "shipping"}}'
  >
    <option value="standard">Standard</option>
    <option value="express">Express</option>
  </select>
  <button type="submit">Place Order</button>
</form>
<!-- When form is submitted, Fullstory captures shipping selection from child -->
```

### Rule 4: Consider Privacy at Each Scope

Different scopes have different privacy implications:

| Scope                  | Privacy Consideration                        | Recommendation                        |
| ---------------------- | -------------------------------------------- | ------------------------------------- |
| **User Properties**    | Persists across sessions, linked to identity | Hash/tokenize PII; use internal IDs   |
| **Page Properties**    | Visible in any session replay on this page   | Mask sensitive page context           |
| **Element Properties** | Captured on interaction                      | Use `fs-exclude` for sensitive inputs |
| **Events**             | Logged with timestamp                        | Never include PII in event properties |

```javascript
// ✅ GOOD: Privacy-conscious scoping
FS('setIdentity', {
  uid: 'usr_abc123', // Internal ID, not email
  properties: {
    plan: 'enterprise',
    account_age_days: 365,
    // NO: email, name, phone
  },
})

FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Account Settings',
    section: 'billing',
    // NO: account balance, card details
  },
})
```

> **Reference**: See `fullstory-privacy-controls` for fs-exclude/fs-mask/fs-unmask and `fullstory-privacy-strategy` for comprehensive privacy guidance.

### Rule 5: Anonymous Users Can Have Properties

User properties work for **anonymous users** (before `setIdentity` is called). Properties persist via the `fs_uid` first-party cookie and transfer when the user later identifies:

```javascript
// Anonymous user lands on site
FS('setProperties', {
  type: 'user',
  properties: {
    landing_page: '/pricing',
    referral_source: 'google_ads',
    campaign: 'spring_promo',
  },
})

// Later, user signs up - properties transfer automatically
FS('setIdentity', {
  uid: 'usr_newuser123',
  properties: {
    signup_date: '2024-01-15',
  },
})
// Now user has: landing_page, referral_source, campaign, AND signup_date
```

---

## II. Scope Selection by Scenario

### Scenario A: Single-Entity Detail Pages (1:1)

**Definition**: A page dedicated to one unique entity (product detail, flight itinerary, policy document).

**Strategy**: Entity attributes become **Page Properties**

```javascript
// ✅ CORRECT: Entity data at page level
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Product Detail',
    productId: 'SKU-123',
    productName: 'Wireless Headphones',
    category: 'Electronics',
    price: 199.99,
    inStock: true
  }
});

// ✅ CORRECT: Elements just have element-specific data
<button data-fs-element="Add to Cart">Add to Cart</button>
<button data-fs-element="Buy Now">Buy Now</button>
```

```javascript
// ❌ WRONG: Entity data duplicated on elements
<button
  data-fs-element="Add to Cart"
  data-product-id="SKU-123" // REDUNDANT - already at page level
  data-product-name="Wireless..." // REDUNDANT
>
  Add to Cart
</button>
```

**Why This Works:**

- All interactions inherit product context
- Search by "clicks on Product Detail page where price > 100" works
- No duplication, cleaner implementation

---

### Scenario B: Multi-Entity Listing Pages (1:Many)

**Definition**: Pages showing multiple distinct entities (search results, product grid, job listings).

**Strategy**:

- Search/filter context → **Page Properties**
- Individual item context → **Element Properties**

```javascript
// ✅ CORRECT: Search context at page level
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Search Results',
    searchTerm: 'wireless headphones',
    resultsCount: 50,
    sortBy: 'relevance',
    activeFilters: ['Electronics', 'In Stock'],
  },
})
```

```html
<!-- ✅ CORRECT: Item-specific data on elements -->
<div
  data-product-id="SKU-123"
  data-product-name="Wireless Headphones"
  data-price="199.99"
  data-position="1"
  data-fs-properties-schema='{
    "data-product-id": {"type": "str", "name": "productId"},
    "data-product-name": {"type": "str", "name": "productName"},
    "data-price": {"type": "real", "name": "price"},
    "data-position": {"type": "int", "name": "position"}
  }'
  data-fs-element="Product Card"
>
  ...
</div>
```

```html
<!-- ❌ WRONG: Search context duplicated on elements -->
<div
  data-product-id="SKU-123"
  data-search-term="wireless headphones"  <!-- REDUNDANT - page level -->
  data-results-count="50"                  <!-- REDUNDANT - page level -->
>
```

---

### Scenario C: User Attributes

**Definition**: Data about WHO the user is (not what they're doing).

**Strategy**: Use **User Properties** via `setIdentity` or `setProperties(user)`

```javascript
// ✅ CORRECT: User attributes at user level
FS('setIdentity', {
  uid: user.id,
  properties: {
    displayName: user.name,
    email: user.email,
    plan: 'enterprise',
    role: 'admin',
    companyName: user.company,
    signupDate: user.createdAt,
  },
})
```

```javascript
// ❌ WRONG: User attributes in page/element properties
FS('setProperties', {
  type: 'page',
  properties: {
    userPlan: 'enterprise', // WRONG SCOPE - use user properties
    userRole: 'admin', // WRONG SCOPE
  },
})
```

---

### Scenario D: Discrete Actions (Events)

**Definition**: Something that **happened** at a point in time.

**Strategy**: Use **trackEvent** with action-specific properties

```javascript
// ✅ CORRECT: Action captured as event
FS('trackEvent', {
  name: 'Product Added to Cart',
  properties: {
    quantity: 2, // Action-specific
    addedFrom: 'quick-view', // Action-specific
    // productId inherited from page properties
    // userId inherited from user properties
  },
})
```

```javascript
// ❌ WRONG: Trying to track actions via properties
FS('setProperties', {
  type: 'user',
  properties: {
    lastAddedProduct: 'SKU-123', // Events shouldn't be properties
    lastAddedQuantity: 2,
    lastAddedTime: Date.now(),
  },
})
```

---

## III. Decision Flowchart

```
START: You have data to capture
          │
          ▼
    Is this data about WHO the user is?
    (plan, role, company, signup date)
          │
    YES ──┴── NO
     │         │
     ▼         ▼
  USER      Is this a discrete action/moment?
  PROPS     (purchase, signup, feature used)
               │
         YES ──┴── NO
          │         │
          ▼         ▼
       EVENT    Is this data the same for the entire page?
                (search term, product on detail page)
                      │
                YES ──┴── NO
                 │         │
                 ▼         ▼
              PAGE      ELEMENT
              PROPS     PROPS
```

---

## IV. Common Patterns by Industry

> **Detailed guidance**: See industry-specific skills for comprehensive implementation patterns.

### E-commerce (`fullstory-ecommerce`)

| Data Point           | Scope            | Implementation        |
| -------------------- | ---------------- | --------------------- |
| User's loyalty tier  | User Property    | `setIdentity`         |
| Search term          | Page Property    | `setProperties(page)` |
| Product ID (on PDP)  | Page Property    | `setProperties(page)` |
| Product ID (in grid) | Element Property | `data-fs-*`           |
| Cart value           | Page Property    | `setProperties(page)` |
| Purchase completed   | Event            | `trackEvent`          |

### SaaS (`fullstory-saas`)

| Data Point             | Scope            | Implementation        |
| ---------------------- | ---------------- | --------------------- |
| User role              | User Property    | `setIdentity`         |
| Team/org ID            | User Property    | `setIdentity`         |
| Dashboard being viewed | Page Property    | `setProperties(page)` |
| Report ID in list      | Element Property | `data-fs-*`           |
| Feature used           | Event            | `trackEvent`          |
| Setting changed        | Event            | `trackEvent`          |

### Media & Entertainment (`fullstory-media-entertainment`)

| Data Point             | Scope            | Implementation        |
| ---------------------- | ---------------- | --------------------- |
| Subscriber status      | User Property    | `setIdentity`         |
| Content category       | Page Property    | `setProperties(page)` |
| Content ID (on detail) | Page Property    | `setProperties(page)` |
| Related content IDs    | Element Property | `data-fs-*`           |
| Video played           | Event            | `trackEvent`          |
| Content shared         | Event            | `trackEvent`          |

### Banking & Finance (`fullstory-banking`)

| Data Point         | Scope            | Implementation                      |
| ------------------ | ---------------- | ----------------------------------- |
| Account type       | User Property    | `setIdentity`                       |
| Current section    | Page Property    | `setProperties(page)`               |
| Transaction type   | Page Property    | `setProperties(page)`               |
| Account selector   | Element Property | `data-fs-*` (ID only, mask details) |
| Transfer completed | Event            | `trackEvent` (no amounts)           |
| MFA step           | Event            | `trackEvent`                        |

### Gaming (`fullstory-gaming`)

| Data Point               | Scope            | Implementation                |
| ------------------------ | ---------------- | ----------------------------- |
| Player tier (VIP status) | User Property    | `setIdentity`                 |
| Game lobby section       | Page Property    | `setProperties(page)`         |
| Active game ID           | Page Property    | `setProperties(page)`         |
| Game tile in grid        | Element Property | `data-fs-*`                   |
| Wager placed             | Event            | `trackEvent` (for compliance) |
| Game launched            | Event            | `trackEvent`                  |

### Healthcare (`fullstory-healthcare`)

| Data Point                      | Scope            | Implementation                 |
| ------------------------------- | ---------------- | ------------------------------ |
| User role (patient/provider)    | User Property    | `setIdentity`                  |
| Section (appointments, records) | Page Property    | `setProperties(page)`          |
| Flow step                       | Page Property    | `setProperties(page)`          |
| Form field (non-PHI only)       | Element Property | `data-fs-*` + `fs-exclude`     |
| Appointment scheduled           | Event            | `trackEvent` (no PHI)          |
| Form submitted                  | Event            | `trackEvent` (completion only) |

### Travel & Hospitality (`fullstory-travel`)

| Data Point               | Scope            | Implementation        |
| ------------------------ | ---------------- | --------------------- |
| Loyalty tier             | User Property    | `setIdentity`         |
| Search criteria          | Page Property    | `setProperties(page)` |
| Selected flight/hotel    | Page Property    | `setProperties(page)` |
| Flight option in results | Element Property | `data-fs-*`           |
| Booking completed        | Event            | `trackEvent`          |
| Ancillary added          | Event            | `trackEvent`          |

---

## V. Anti-Patterns to Avoid

### Anti-Pattern 1: Everything as User Properties

```javascript
// ❌ BAD: Transient state as user property
FS('setProperties', {
  type: 'user',
  properties: {
    currentPage: '/checkout', // Should be page property
    cartItems: 5, // Should be page property
    lastClickedButton: 'submit', // Should be event
  },
})
```

### Anti-Pattern 2: Everything as Events

```javascript
// ❌ BAD: State as events
FS('trackEvent', {name: 'User Is Premium', properties: {}}) // User property
FS('trackEvent', {name: 'Page Has 5 Results', properties: {}}) // Page property
```

### Anti-Pattern 3: Duplicating Hierarchy

```javascript
// ❌ BAD: Same data at multiple levels
FS('setIdentity', {uid: '123', properties: {plan: 'premium'}})
FS('setProperties', {type: 'page', properties: {userPlan: 'premium'}}) // DUP
FS('trackEvent', {name: 'Click', properties: {userPlan: 'premium'}}) // DUP
```

### Anti-Pattern 4: Over-Granular Element Properties

```javascript
// ❌ BAD: Too much data on elements when page context would work
<button
  data-page-name="Checkout"          // Should be page property
  data-user-id="123"                 // Should be user property
  data-cart-total="99.99"            // Should be page property
  data-fs-element="Submit">
```

---

## VI. Implementation Checklist

Before implementing, answer these questions:

- [ ] **Who is this data about?**
  - The user → User Properties
  - The page/context → Page Properties
  - A specific element → Element Properties
  - An action → Event

- [ ] **How long is this data relevant?**
  - Entire user lifetime → User Properties
  - This page view → Page Properties
  - This interaction → Element/Event Properties

- [ ] **Is this data already available at a higher scope?**
  - If yes → Don't duplicate, let inheritance work
  - If no → Add at appropriate scope

- [ ] **Can this data be searched/segmented?**
  - User properties → Segment users
  - Page properties → Find sessions with this page context
  - Element properties → Find clicks on elements with this data
  - Events → Funnel analysis, conversion tracking

---

## VII. Related Skills

### Core API Skills

| API                 | Skill Document                 |
| ------------------- | ------------------------------ |
| User Identification | `fullstory-identify-users`     |
| User Properties     | `fullstory-user-properties`    |
| Page Properties     | `fullstory-page-properties`    |
| Element Properties  | `fullstory-element-properties` |
| Events              | `fullstory-analytics-events`   |
| Privacy Controls    | `fullstory-privacy-controls`   |

### Industry Skills

| Industry              | Skill Document                  |
| --------------------- | ------------------------------- |
| Banking & Finance     | `fullstory-banking`             |
| E-commerce & Retail   | `fullstory-ecommerce`           |
| Gaming                | `fullstory-gaming`              |
| Healthcare            | `fullstory-healthcare`          |
| B2B SaaS              | `fullstory-saas`                |
| Travel & Hospitality  | `fullstory-travel`              |
| Media & Entertainment | `fullstory-media-entertainment` |

### Strategic Skills

| Topic            | Skill Document               |
| ---------------- | ---------------------------- |
| Getting Started  | `fullstory-getting-started`  |
| Privacy Strategy | `fullstory-privacy-strategy` |
| Stable Selectors | `fullstory-stable-selectors` |

---

## VIII. Version History

- **4.0** (Current)
  - Added YAML front matter for skill metadata
  - Integrated with core skill documents
  - Added decision flowchart
  - Expanded industry-specific patterns
  - Added explicit anti-patterns section
  - Aligned format with element-properties skill
- **3.0**
  - Generalized naming and examples
  - Added explicit Good/Bad implementation guides
  - Renamed properties for universal application

- **2.0**
  - Merged Scoping and Element Naming into one unified document

---

## Key Takeaways for Agent

When helping developers with data scoping:

1. **Always ask first**:
   - What data are you trying to capture?
   - Is this about the user, the page, an element, or an action?
   - Will this data be the same across multiple elements?
   - Is this data sensitive? What privacy level is needed?

2. **Common mistakes to watch for**:
   - User data in page properties
   - Page-level data duplicated on elements
   - Actions captured as properties instead of events
   - Same data at multiple scopes
   - PII in user properties without hashing
   - Forgetting that anonymous users can have properties

3. **Golden rules**:
   - Capture at the HIGHEST relevant scope
   - Let inheritance do the work (both parent→child AND child→parent)
   - User → Page → Element → Event (hierarchy)
   - Don't duplicate across scopes
   - Consider privacy at every scope

4. **Quick decision**:
   - WHO = User Properties (works for anonymous users too!)
   - WHERE = Page Properties
   - WHAT (specific item) = Element Properties
   - WHAT HAPPENED = Events

5. **Privacy quick reference**:
   - Sensitive user data → Hash/tokenize or use internal IDs
   - Sensitive page context → Consider masking
   - Sensitive elements → Use `fs-exclude`
   - Sensitive events → Never include PII in properties

---

_This meta-skill document provides strategic guidance for Fullstory data semantic decoration. Refer to individual API skill documents for detailed implementation examples._
