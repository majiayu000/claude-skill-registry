---
name: fullstory-analytics-events
version: v2
description: Comprehensive guide for implementing Fullstory's Analytics Events API (trackEvent) for web applications. Teaches proper event naming, property structuring, type handling, and e-commerce event patterns. Includes detailed good/bad examples for funnel tracking, feature usage, conversion events, and SaaS subscription flows to help developers capture meaningful business events for analytics and segmentation.
related_skills:
  - fullstory-page-properties
  - fullstory-user-properties
  - fullstory-element-properties
  - fullstory-data-scoping-decoration
  - fullstory-async-methods
  - fullstory-privacy-strategy
  - fullstory-ecommerce
  - fullstory-saas
  - fullstory-travel
  - fullstory-media-entertainment
---

# Fullstory Analytics Events API (trackEvent)

## Overview

Fullstory's Analytics Events API allows developers to send custom event data that captures meaningful user actions and business moments. Unlike automatic capture which records all interactions, `trackEvent` lets you define semantically meaningful events with rich context that can be used for:

- **Funnel Analysis**: Track conversion steps and drop-off points
- **Feature Adoption**: Measure feature usage and engagement
- **Business Metrics**: Capture revenue, conversions, and KPIs
- **User Journeys**: Define key moments in user workflows
- **Segmentation**: Create user segments based on behaviors

## Core Concepts

### Events vs Properties vs Elements

| API                    | Purpose                  | Data Type           | Example                           |
| ---------------------- | ------------------------ | ------------------- | --------------------------------- |
| `trackEvent`           | Discrete actions/moments | "What happened"     | "Order Completed", "Feature Used" |
| `setProperties` (user) | User attributes          | "Who they are"      | plan: "enterprise"                |
| `setProperties` (page) | Page context             | "Where they are"    | pageName: "Checkout"              |
| Element Properties     | Interaction context      | "What they clicked" | productId: "SKU-123"              |

### Event Naming Conventions

Fullstory recommends semantic event naming following industry standards:

```
[Object] [Action]

Examples:
- "Product Added"
- "Order Completed"
- "Feature Enabled"
- "Search Performed"
- "Video Played"
```

### Event Properties

Every event can include rich contextual properties that enable deep analysis:

- Product details for e-commerce events
- Feature names for adoption tracking
- Revenue values for business metrics
- Custom dimensions for segmentation

---

## API Reference

### Basic Syntax

```javascript
FS('trackEvent', {
  name: string,          // Required: Event name (max 250 chars)
  properties: object,    // Required: Event properties (max 512KB)
  schema?: object        // Optional: Type hints for properties
});
```

### Parameters

| Parameter    | Type   | Required | Description                            |
| ------------ | ------ | -------- | -------------------------------------- |
| `name`       | string | **Yes**  | Event name, max 250 characters         |
| `properties` | object | **Yes**  | Key/value pairs of event data          |
| `schema`     | object | No       | Explicit type inference for properties |

### Supported Property Types

| Type    | Description       | Examples                     |
| ------- | ----------------- | ---------------------------- |
| `str`   | String value      | "blue", "premium"            |
| `strs`  | Array of strings  | ["red", "blue", "green"]     |
| `int`   | Integer           | 42, -5, 0                    |
| `ints`  | Array of integers | [1, 2, 3]                    |
| `real`  | Float/decimal     | 99.99, -3.14                 |
| `reals` | Array of reals    | [10.5, 20.0]                 |
| `bool`  | Boolean           | true, false                  |
| `bools` | Array of booleans | [true, false]                |
| `date`  | ISO8601 date      | "2024-01-15T00:00:00Z"       |
| `dates` | Array of dates    | ["2024-01-01", "2024-02-01"] |

### Rate Limits

- **Sustained**: 60 calls per user per page per minute
- **Burst**: 40 calls per second

### Size Limits

- Event name: Max 250 characters
- Properties payload: Max 512KB
- Arrays of objects: NOT indexed (except Order Completed)

---

## ✅ GOOD IMPLEMENTATION EXAMPLES

### Example 1: E-commerce - Product Added to Cart

```javascript
// GOOD: Comprehensive product add event
function handleAddToCart(product, quantity, source) {
  FS('trackEvent', {
    name: 'Product Added',
    properties: {
      // Product identification
      product_id: product.id,
      sku: product.sku,
      name: product.name,
      brand: product.brand,

      // Categorization
      category: product.category,
      subcategory: product.subcategory,

      // Pricing
      price: product.price,
      currency: 'USD',

      // Cart context
      quantity: quantity,
      cart_id: getCartId(),

      // Attribution
      position: product.listPosition,
      list_name: source.listName,

      // Product attributes
      variant: product.selectedVariant,
      size: product.selectedSize,
      color: product.selectedColor,

      // Promotion tracking
      coupon: getActiveCoupon(),

      // URLs for reference
      url: product.url,
      image_url: product.imageUrl,
    },
    schema: {
      price: 'real',
      quantity: 'int',
      position: 'int',
    },
  })
}
```

**Why this is good:**

- ✅ Follows standard e-commerce event naming
- ✅ Includes product identification (id, sku)
- ✅ Captures pricing with currency
- ✅ Includes attribution context (position, list)
- ✅ Proper typing for numeric fields

### Example 2: SaaS - Feature Usage Tracking

```javascript
// GOOD: Track feature usage with context
function trackFeatureUsage(featureName, context = {}) {
  FS('trackEvent', {
    name: 'Feature Used',
    properties: {
      // Feature identification
      feature_name: featureName,
      feature_category: getFeatureCategory(featureName),

      // Usage context
      usage_context: context.trigger || 'direct',
      entry_point: context.entryPoint || window.location.pathname,

      // User's feature state
      is_first_use: !hasUsedFeature(featureName),
      times_used_today: getDailyUsageCount(featureName),
      times_used_total: getTotalUsageCount(featureName),

      // Session context
      session_feature_count: getSessionFeatureCount(),
      time_in_session: getTimeInSession(),

      // Feature-specific data
      ...context.metadata,
    },
    schema: {
      is_first_use: 'bool',
      times_used_today: 'int',
      times_used_total: 'int',
      session_feature_count: 'int',
      time_in_session: 'int',
    },
  })
}

// Usage
trackFeatureUsage('advanced_export', {
  trigger: 'keyboard_shortcut',
  entryPoint: '/dashboard',
  metadata: {
    export_format: 'csv',
    row_count: 1500,
  },
})
```

**Why this is good:**

- ✅ Tracks both feature and context
- ✅ Captures first-use for adoption analysis
- ✅ Includes frequency metrics
- ✅ Flexible metadata for feature-specific data

### Example 3: Subscription/Billing Events

```javascript
// GOOD: Track subscription lifecycle events
class SubscriptionTracker {
  trackTrialStarted(trial) {
    FS('trackEvent', {
      name: 'Trial Started',
      properties: {
        trial_plan: trial.plan,
        trial_duration_days: trial.durationDays,
        trial_features: trial.includedFeatures,
        source: trial.acquisitionSource,
        started_at: new Date().toISOString(),
      },
      schema: {
        trial_duration_days: 'int',
        trial_features: 'strs',
        started_at: 'date',
      },
    })
  }

  trackSubscriptionStarted(subscription) {
    FS('trackEvent', {
      name: 'Subscription Started',
      properties: {
        plan_name: subscription.plan,
        plan_tier: subscription.tier,
        billing_cycle: subscription.billingCycle,
        price: subscription.price,
        currency: subscription.currency,
        seats: subscription.seats,
        mrr: subscription.mrr,
        arr: subscription.arr,
        trial_converted: subscription.wasTrialing,
        payment_method: subscription.paymentMethod,
        promo_code: subscription.promoCode,
      },
      schema: {
        price: 'real',
        seats: 'int',
        mrr: 'real',
        arr: 'real',
        trial_converted: 'bool',
      },
    })
  }

  trackPlanChanged(change) {
    FS('trackEvent', {
      name: 'Plan Changed',
      properties: {
        from_plan: change.fromPlan,
        to_plan: change.toPlan,
        from_price: change.fromPrice,
        to_price: change.toPrice,
        price_change: change.toPrice - change.fromPrice,
        change_type: change.toPrice > change.fromPrice ? 'upgrade' : 'downgrade',
        from_seats: change.fromSeats,
        to_seats: change.toSeats,
        effective_date: change.effectiveDate,
        reason: change.reason,
      },
      schema: {
        from_price: 'real',
        to_price: 'real',
        price_change: 'real',
        from_seats: 'int',
        to_seats: 'int',
        effective_date: 'date',
      },
    })
  }

  trackChurnEvent(churn) {
    FS('trackEvent', {
      name: 'Subscription Cancelled',
      properties: {
        plan_name: churn.plan,
        tenure_days: churn.tenureDays,
        lifetime_value: churn.ltv,
        cancel_reason: churn.reason,
        cancel_feedback: churn.feedback,
        was_paying: churn.wasPaying,
        final_mrr: churn.finalMrr,
        churn_type: churn.immediate ? 'immediate' : 'end_of_period',
      },
      schema: {
        tenure_days: 'int',
        lifetime_value: 'real',
        was_paying: 'bool',
        final_mrr: 'real',
      },
    })
  }
}
```

**Why this is good:**

- ✅ Captures full subscription lifecycle
- ✅ Includes revenue metrics (MRR, ARR, LTV)
- ✅ Tracks upgrade/downgrade patterns
- ✅ Captures churn reasons for analysis

### Example 4: Search and Discovery

```javascript
// GOOD: Track search behavior
function trackSearch(searchData) {
  FS('trackEvent', {
    name: 'Search Performed',
    properties: {
      // Query details
      search_term: searchData.query,
      search_type: searchData.type, // 'keyword', 'filter', 'voice'

      // Results
      results_count: searchData.results.length,
      has_results: searchData.results.length > 0,

      // Filters applied
      filters_applied: Object.keys(searchData.filters),
      filter_count: Object.keys(searchData.filters).length,

      // Sorting
      sort_by: searchData.sortBy,
      sort_order: searchData.sortOrder,

      // Pagination
      page_number: searchData.page,
      results_per_page: searchData.perPage,

      // Performance
      response_time_ms: searchData.responseTime,

      // Context
      search_location: searchData.location, // 'header', 'page', 'modal'
      is_refinement: searchData.isRefinement,
    },
    schema: {
      results_count: 'int',
      has_results: 'bool',
      filters_applied: 'strs',
      filter_count: 'int',
      page_number: 'int',
      results_per_page: 'int',
      response_time_ms: 'int',
      is_refinement: 'bool',
    },
  })
}

// Track when user clicks a search result
function trackSearchResultClick(result, searchContext) {
  FS('trackEvent', {
    name: 'Search Result Clicked',
    properties: {
      search_term: searchContext.query,
      result_position: result.position,
      result_id: result.id,
      result_type: result.type,
      results_count: searchContext.totalResults,
      page_number: searchContext.page,
    },
    schema: {
      result_position: 'int',
      results_count: 'int',
      page_number: 'int',
    },
  })
}
```

**Why this is good:**

- ✅ Captures search intent (query, filters)
- ✅ Tracks result quality (count, has_results)
- ✅ Measures performance (response_time)
- ✅ Connects searches to clicks

### Example 5: Form/Funnel Tracking

```javascript
// GOOD: Multi-step form/funnel tracking
class FunnelTracker {
  constructor(funnelName, steps) {
    this.funnelName = funnelName
    this.steps = steps
    this.startTime = null
    this.stepTimes = {}
  }

  startFunnel(context = {}) {
    this.startTime = Date.now()

    FS('trackEvent', {
      name: `${this.funnelName} Started`,
      properties: {
        funnel_name: this.funnelName,
        total_steps: this.steps.length,
        entry_point: window.location.pathname,
        ...context,
      },
      schema: {
        total_steps: 'int',
      },
    })
  }

  completeStep(stepIndex, stepData = {}) {
    const stepName = this.steps[stepIndex]
    const now = Date.now()
    const stepDuration = this.stepTimes[stepIndex - 1]
      ? now - this.stepTimes[stepIndex - 1]
      : now - this.startTime

    this.stepTimes[stepIndex] = now

    FS('trackEvent', {
      name: `${this.funnelName} Step Completed`,
      properties: {
        funnel_name: this.funnelName,
        step_number: stepIndex + 1,
        step_name: stepName,
        total_steps: this.steps.length,
        step_duration_ms: stepDuration,
        time_in_funnel_ms: now - this.startTime,
        ...stepData,
      },
      schema: {
        step_number: 'int',
        total_steps: 'int',
        step_duration_ms: 'int',
        time_in_funnel_ms: 'int',
      },
    })
  }

  completeFunnel(result = {}) {
    const totalDuration = Date.now() - this.startTime

    FS('trackEvent', {
      name: `${this.funnelName} Completed`,
      properties: {
        funnel_name: this.funnelName,
        total_steps: this.steps.length,
        total_duration_ms: totalDuration,
        ...result,
      },
      schema: {
        total_steps: 'int',
        total_duration_ms: 'int',
      },
    })
  }

  abandonFunnel(stepIndex, reason = 'unknown') {
    FS('trackEvent', {
      name: `${this.funnelName} Abandoned`,
      properties: {
        funnel_name: this.funnelName,
        abandoned_at_step: stepIndex + 1,
        abandoned_step_name: this.steps[stepIndex],
        total_steps: this.steps.length,
        time_in_funnel_ms: Date.now() - this.startTime,
        abandon_reason: reason,
      },
      schema: {
        abandoned_at_step: 'int',
        total_steps: 'int',
        time_in_funnel_ms: 'int',
      },
    })
  }
}

// Usage
const checkoutFunnel = new FunnelTracker('Checkout', [
  'Cart Review',
  'Shipping Info',
  'Payment Info',
  'Confirmation',
])

checkoutFunnel.startFunnel({cart_value: 150.0})
checkoutFunnel.completeStep(0, {items_count: 3})
checkoutFunnel.completeStep(1, {shipping_method: 'express'})
checkoutFunnel.completeStep(2, {payment_method: 'credit_card'})
checkoutFunnel.completeFunnel({order_id: 'ORD-123', total: 165.0})
```

**Why this is good:**

- ✅ Tracks full funnel journey
- ✅ Measures time per step
- ✅ Captures abandonment with context
- ✅ Reusable for any multi-step flow

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Event Name Too Generic

```javascript
// BAD: Vague event names
FS('trackEvent', {
  name: 'click', // BAD: Too generic
  properties: {
    element: 'button',
  },
})

FS('trackEvent', {
  name: 'action', // BAD: Meaningless
  properties: {
    type: 'purchase',
  },
})
```

**Why this is bad:**

- ❌ "click" doesn't describe what happened
- ❌ Can't build meaningful funnels
- ❌ No semantic meaning
- ❌ Hard to analyze

**CORRECTED VERSION:**

```javascript
// GOOD: Semantic event names
FS('trackEvent', {
  name: 'Add to Cart Button Clicked',
  properties: {
    product_id: 'SKU-123',
    button_location: 'product_page',
  },
})

FS('trackEvent', {
  name: 'Order Completed',
  properties: {
    order_id: 'ORD-456',
    total: 99.99,
  },
})
```

### Example 2: Missing Critical Properties

```javascript
// BAD: Order event without essential data
FS('trackEvent', {
  name: 'Order Completed',
  properties: {
    success: true, // This tells us almost nothing!
  },
})
```

**Why this is bad:**

- ❌ No order ID for reference
- ❌ No revenue data for metrics
- ❌ No product information
- ❌ Can't do meaningful analysis

**CORRECTED VERSION:**

```javascript
// GOOD: Comprehensive order event
FS('trackEvent', {
  name: 'Order Completed',
  properties: {
    order_id: order.id,
    revenue: order.total,
    currency: order.currency,
    item_count: order.items.length,
    shipping_method: order.shipping.method,
    payment_method: order.payment.method,
    coupon_code: order.coupon,
    discount_amount: order.discount,
    is_first_order: customer.orderCount === 1,
  },
  schema: {
    revenue: 'real',
    item_count: 'int',
    discount_amount: 'real',
    is_first_order: 'bool',
  },
})
```

### Example 3: Type Mismatches

```javascript
// BAD: Wrong value formats
FS('trackEvent', {
  name: 'Product Purchased',
  properties: {
    price: '$49.99', // BAD: Currency symbol
    quantity: '3 items', // BAD: Text in number
    in_stock: 'yes', // BAD: String instead of boolean
    purchase_date: 'today', // BAD: Not ISO8601
  },
  schema: {
    price: 'real',
    quantity: 'int',
    in_stock: 'bool',
    purchase_date: 'date',
  },
})
```

**Why this is bad:**

- ❌ '$49.99' won't parse as real
- ❌ '3 items' won't parse as int
- ❌ 'yes' is not a valid boolean
- ❌ 'today' is not ISO8601

**CORRECTED VERSION:**

```javascript
// GOOD: Properly formatted values
FS('trackEvent', {
  name: 'Product Purchased',
  properties: {
    price: 49.99,
    currency: 'USD',
    quantity: 3,
    in_stock: true,
    purchase_date: new Date().toISOString(),
  },
  schema: {
    price: 'real',
    quantity: 'int',
    in_stock: 'bool',
    purchase_date: 'date',
  },
})
```

### Example 4: Tracking Too Many Events

```javascript
// BAD: Tracking every micro-interaction
document.addEventListener('mousemove', (e) => {
  FS('trackEvent', {
    name: 'Mouse Moved',
    properties: {x: e.clientX, y: e.clientY},
  })
})

document.addEventListener('scroll', () => {
  FS('trackEvent', {
    name: 'Page Scrolled',
    properties: {position: window.scrollY},
  })
})
```

**Why this is bad:**

- ❌ Will hit rate limits immediately
- ❌ Drowns out meaningful events
- ❌ No analytical value
- ❌ Fullstory already captures these automatically

**CORRECTED VERSION:**

```javascript
// GOOD: Track meaningful scroll milestones only
const scrollMilestones = [25, 50, 75, 100]
const trackedMilestones = new Set()

window.addEventListener(
  'scroll',
  throttle(() => {
    const scrollPercent = Math.round(
      (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100,
    )

    scrollMilestones.forEach((milestone) => {
      if (scrollPercent >= milestone && !trackedMilestones.has(milestone)) {
        trackedMilestones.add(milestone)

        FS('trackEvent', {
          name: 'Scroll Depth Reached',
          properties: {
            depth_percent: milestone,
            page: window.location.pathname,
          },
        })
      }
    })
  }, 250),
)
```

### Example 5: Event Name Too Long

```javascript
// BAD: Event name exceeds 250 character limit
FS('trackEvent', {
  name: 'User clicked on the primary call-to-action button located in the hero section of the landing page after scrolling past the feature comparison table and reading the customer testimonials section which indicates strong purchase intent',
  properties: {clicked: true},
})
```

**Why this is bad:**

- ❌ Exceeds 250 character limit
- ❌ Event will be truncated or fail
- ❌ Context belongs in properties, not name

**CORRECTED VERSION:**

```javascript
// GOOD: Concise name, rich properties
FS('trackEvent', {
  name: 'CTA Button Clicked',
  properties: {
    button_location: 'hero_section',
    page_type: 'landing_page',
    scroll_depth_before_click: 75,
    sections_viewed: ['features', 'comparison', 'testimonials'],
    intent_signals: ['high_engagement', 'price_check'],
  },
  schema: {
    scroll_depth_before_click: 'int',
    sections_viewed: 'strs',
    intent_signals: 'strs',
  },
})
```

### Example 6: Duplicate Events

```javascript
// BAD: Sending same event multiple times
function handleFormSubmit(formData) {
  // This might fire multiple times due to double-clicks or re-renders
  FS('trackEvent', {
    name: 'Form Submitted',
    properties: formData,
  })
}

// Without proper deduplication
submitButton.addEventListener('click', handleFormSubmit)
form.addEventListener('submit', handleFormSubmit) // Double event!
```

**Why this is bad:**

- ❌ Same event fires twice
- ❌ Inflates metrics
- ❌ Creates confusing analytics

**CORRECTED VERSION:**

```javascript
// GOOD: Deduplicate events
const eventTracker = {
  recentEvents: new Map(),

  track(name, properties, dedupeKey = null) {
    const key = dedupeKey || `${name}-${JSON.stringify(properties)}`
    const now = Date.now()
    const lastSent = this.recentEvents.get(key)

    // Don't send if same event sent within 1 second
    if (lastSent && now - lastSent < 1000) {
      return
    }

    this.recentEvents.set(key, now)

    FS('trackEvent', {
      name,
      properties,
    })
  },
}

// Usage
function handleFormSubmit(formData) {
  eventTracker.track('Form Submitted', formData, formData.formId)
}
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Event Tracking Service

```javascript
// Centralized event tracking with validation
class EventTracker {
  constructor() {
    this.eventSchemas = new Map()
  }

  // Register event schema for validation
  registerEvent(name, schema) {
    this.eventSchemas.set(name, schema)
  }

  // Track event with automatic schema
  track(name, properties) {
    const schema = this.eventSchemas.get(name)

    const eventPayload = {
      name,
      properties: {
        ...properties,
        tracked_at: new Date().toISOString(),
        page_url: window.location.href,
      },
    }

    if (schema) {
      eventPayload.schema = schema
    }

    FS('trackEvent', eventPayload)
  }
}

// Setup
const tracker = new EventTracker()

tracker.registerEvent('Order Completed', {
  revenue: 'real',
  item_count: 'int',
  is_first_order: 'bool',
})

// Usage
tracker.track('Order Completed', {
  order_id: 'ORD-123',
  revenue: 99.99,
  item_count: 3,
  is_first_order: false,
})
```

### Pattern 2: E-commerce Event Library

```javascript
// Standard e-commerce events
const ecommerceEvents = {
  productViewed(product) {
    FS('trackEvent', {
      name: 'Product Viewed',
      properties: {
        product_id: product.id,
        sku: product.sku,
        name: product.name,
        category: product.category,
        price: product.price,
        currency: product.currency,
        brand: product.brand,
        variant: product.variant,
      },
      schema: {price: 'real'},
    })
  },

  productAdded(product, cartId, quantity = 1) {
    FS('trackEvent', {
      name: 'Product Added',
      properties: {
        product_id: product.id,
        sku: product.sku,
        name: product.name,
        category: product.category,
        price: product.price,
        currency: product.currency,
        quantity: quantity,
        cart_id: cartId,
      },
      schema: {price: 'real', quantity: 'int'},
    })
  },

  checkoutStarted(cart) {
    FS('trackEvent', {
      name: 'Checkout Started',
      properties: {
        cart_id: cart.id,
        value: cart.total,
        currency: cart.currency,
        item_count: cart.items.length,
        coupon: cart.coupon,
      },
      schema: {value: 'real', item_count: 'int'},
    })
  },

  orderCompleted(order) {
    FS('trackEvent', {
      name: 'Order Completed',
      properties: {
        order_id: order.id,
        revenue: order.revenue,
        tax: order.tax,
        shipping: order.shipping,
        total: order.total,
        currency: order.currency,
        item_count: order.items.length,
        coupon: order.coupon,
        discount: order.discount,
        payment_method: order.paymentMethod,
      },
      schema: {
        revenue: 'real',
        tax: 'real',
        shipping: 'real',
        total: 'real',
        item_count: 'int',
        discount: 'real',
      },
    })
  },
}
```

### Pattern 3: Timed Event Tracking

```javascript
// Track events with timing
class TimedEventTracker {
  timers = new Map()

  start(eventName, properties = {}) {
    this.timers.set(eventName, {
      startTime: Date.now(),
      properties,
    })
  }

  complete(eventName, additionalProperties = {}) {
    const timer = this.timers.get(eventName)
    if (!timer) return

    const duration = Date.now() - timer.startTime

    FS('trackEvent', {
      name: eventName,
      properties: {
        ...timer.properties,
        ...additionalProperties,
        duration_ms: duration,
        completed: true,
      },
      schema: {
        duration_ms: 'int',
        completed: 'bool',
      },
    })

    this.timers.delete(eventName)
  }

  cancel(eventName, reason = 'cancelled') {
    const timer = this.timers.get(eventName)
    if (!timer) return

    const duration = Date.now() - timer.startTime

    FS('trackEvent', {
      name: eventName,
      properties: {
        ...timer.properties,
        duration_ms: duration,
        completed: false,
        cancel_reason: reason,
      },
      schema: {
        duration_ms: 'int',
        completed: 'bool',
      },
    })

    this.timers.delete(eventName)
  }
}

// Usage
const timedTracker = new TimedEventTracker()

timedTracker.start('Video Watched', {video_id: 'VID-123'})
// ... user watches video ...
timedTracker.complete('Video Watched', {percent_watched: 85})
```

---

## ASYNC VERSION

For cases where you need to confirm the event was sent:

```javascript
try {
  await FS('trackEventAsync', {
    name: 'Order Completed',
    properties: {
      order_id: order.id,
      revenue: order.total,
    },
  })
  console.log('Event sent successfully')
} catch (error) {
  console.error('Event failed:', error)
  // Fallback: queue for retry
}
```

---

## TROUBLESHOOTING

### Events Not Appearing

**Symptom**: Events don't show in Fullstory

**Common Causes**:

1. ❌ Fullstory script not loaded
2. ❌ Event name exceeds 250 chars
3. ❌ Properties exceed 512KB
4. ❌ Rate limits exceeded

**Solutions**:

- ✅ Verify FS function is available
- ✅ Keep event names concise
- ✅ Reduce property payload size
- ✅ Throttle high-frequency events

### Events Have Missing Properties

**Symptom**: Some properties missing in Fullstory

**Common Causes**:

1. ❌ Property values are undefined
2. ❌ Type mismatches with schema
3. ❌ Unsupported array types (arrays of objects)

**Solutions**:

- ✅ Validate properties before sending
- ✅ Match value formats to schema types
- ✅ Flatten object arrays

---

## LIMITS AND CONSTRAINTS

### Size Limits

- Event name: 250 characters
- Properties payload: 512KB

### Rate Limits

- **Sustained**: 60 calls per user per page per minute
- **Burst**: 40 calls per second

### Array Handling

- Arrays of primitives (strings, numbers): ✅ Indexed
- Arrays of objects: ❌ NOT indexed (except Order Completed)

---

## KEY TAKEAWAYS FOR AGENT

When helping developers implement Analytics Events:

1. **Always emphasize**:
   - Use semantic event names (Object + Action)
   - Include meaningful properties
   - Use schema for non-string types
   - Don't track what Fullstory captures automatically

2. **Common mistakes to watch for**:
   - Generic event names ("click", "action")
   - Missing critical properties (order_id, revenue)
   - Type format mismatches
   - Over-tracking micro-interactions

3. **Questions to ask developers**:
   - What business questions will this event answer?
   - What properties are needed for segmentation?
   - How often will this event fire?
   - Is this redundant with auto-captured data?

4. **Best practices to recommend**:
   - Follow e-commerce/SaaS event standards
   - Include context (page, source, timing)
   - Deduplicate rapid-fire events
   - Test events appear in Fullstory

---

## REFERENCE LINKS

- **Analytics Events**: https://developer.fullstory.com/browser/capture-events/analytics-events/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Help Center - Custom Events**: https://help.fullstory.com/hc/en-us/articles/360020623274

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's Analytics Events API correctly for web applications._
