---
name: fullstory-page-properties
version: v2
description: Comprehensive guide for implementing Fullstory's Page Properties API (setProperties with type 'page') for web applications. Teaches proper page naming, contextual data capture, SPA navigation handling, and session-scoped properties. Includes detailed good/bad examples for search results, checkout flows, dashboards, and content pages to help developers enrich page context for analytics and journey mapping.
related_skills:
  - fullstory-element-properties
  - fullstory-user-properties
  - fullstory-analytics-events
  - fullstory-data-scoping-decoration
---

# Fullstory Page Properties API

## Overview

Fullstory's Page Properties API allows developers to capture contextual information about the current page that enriches sessions for search, filtering, segmentation, and journey analysis. Unlike user properties that persist across sessions, page properties are session-scoped and reset when the URL path changes.

Key use cases:

- **Page Naming**: Define semantic page names that enrich ALL events on that page across Fullstory (Search, Segments, Funnels, Journeys, Metrics)
- **Search Context**: Capture search terms and filters on results pages
- **Checkout State**: Track cart value, step number, coupon codes
- **Content Context**: Capture article categories, author, publish date
- **Dynamic State**: Record filters, sort orders, view modes

## Core Concepts

### Page Property Lifecycle

```
Page Load  →  setProperties(page)  →  Properties Active  →  URL Change  →  Properties Reset
     ↓                                        ↓
  Same page, call again              Merged with existing props
```

### Key Behaviors

| Behavior                   | Description                                                    |
| -------------------------- | -------------------------------------------------------------- |
| **Session-scoped**         | Properties persist for the current page until URL path changes |
| **Merge on repeat calls**  | Multiple calls on same page merge properties                   |
| **Reset on navigation**    | Properties clear when URL host or path changes                 |
| **pageName special field** | Creates named Pages for use in Journeys                        |

### Page Properties vs Other Property Types

| Type               | Scope   | Persists         | Best For                      |
| ------------------ | ------- | ---------------- | ----------------------------- |
| User Properties    | User    | Across sessions  | User attributes, plan, role   |
| Page Properties    | Page    | Until URL change | Page context, search, filters |
| Element Properties | Element | Interaction      | Click-level context           |
| Event Properties   | Event   | One event        | Action-specific data          |

### ⚠️ Critical: Use Properties to Stay Within the 1,000 Page Limit

Fullstory limits you to **1,000 unique `pageName` values**. Once exceeded, additional page names are silently ignored.

**The Strategy**: Use a **generic page name** + **properties for variations**.

```
❌ BAD: Unique pageName for every product
   pageName: "iPhone 15 Pro Max 256GB Space Black"
   pageName: "iPhone 15 Pro Max 512GB Natural Titanium"
   pageName: "Samsung Galaxy S24 Ultra 256GB..."
   → Exhausts 1,000 limit quickly!

✅ GOOD: Generic pageName + properties for context
   pageName: "Product Detail"
   + productName: "iPhone 15 Pro Max"
   + productCategory: "Smartphones"
   + productBrand: "Apple"
   + productPrice: 1199
```

| Scenario       | ❌ Wrong (unique pageName) | ✅ Right (generic + properties)                                      |
| -------------- | -------------------------- | -------------------------------------------------------------------- |
| Product pages  | `"iPhone 15 Pro Detail"`   | `pageName: "Product Detail"` + `productName` property                |
| User profiles  | `"John Smith's Profile"`   | `pageName: "User Profile"` + `profileUserId` property                |
| Article pages  | `"How to Cook Pasta"`      | `pageName: "Article"` + `articleTitle`, `articleCategory` properties |
| Search results | `"Search: blue shoes"`     | `pageName: "Search Results"` + `searchTerm` property                 |
| Category pages | `"Men's Running Shoes"`    | `pageName: "Category"` + `categoryName`, `categoryPath` properties   |

> **Think of it this way**: `pageName` defines the **type** of page (e.g., "Product Detail", "Checkout", "Search Results"). Properties describe the **specific instance** (which product, what search term, etc.). This gives you unlimited variation tracking while staying well under the 1,000 limit.

---

## API Reference

### Basic Syntax

```javascript
FS('setProperties', {
  type: 'page',
  properties: object, // Required: Key/value pairs
})
```

### Parameters

| Parameter    | Type   | Required | Description                          |
| ------------ | ------ | -------- | ------------------------------------ |
| `type`       | string | **Yes**  | Must be `'page'` for page properties |
| `properties` | object | **Yes**  | Key/value pairs of page data         |

### Special Fields

| Field      | Behavior                                                                                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `pageName` | Creates a named Page used **across all of Fullstory** - not just Journeys. Limited to 1,000 unique values. Takes precedence over URL-based page definitions. |

### Why pageName and Page Properties Matter Across Fullstory

`pageName` and page properties aren't just for Journeys - they enrich **every event** that occurs on that page:

| Fullstory Feature  | How Page Properties Help                                                                 |
| ------------------ | ---------------------------------------------------------------------------------------- |
| **Search**         | Find sessions where `pageName = "Checkout"` AND `cartValue > 500`                        |
| **Segments**       | Create segments like "Users who visited Product pages with priceRange = 'premium'"       |
| **Funnels**        | Build funnels using pageName steps: "Home → Category → Product Detail → Cart → Checkout" |
| **Journeys**       | Map user flows across named pages                                                        |
| **Metrics**        | Track conversion rates per page type, filter by page properties                          |
| **Dashboards**     | Break down metrics by pageName or page properties                                        |
| **Event Analysis** | Every click, rage click, error on a page carries the page context                        |

```javascript
// When you set page properties...
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Product Detail',
    productCategory: 'Electronics',
    productPrice: 999,
    inStock: true,
  },
})

// ...every subsequent event on this page (clicks, errors, custom events)
// is automatically enriched with this context, enabling queries like:
// - "Show me rage clicks on Product Detail pages where productPrice > 500"
// - "Find errors on out-of-stock product pages"
// - "Compare conversion rates: Electronics vs Clothing product pages"
```

### Rate Limits

- **Sustained**: 30 calls per page per minute
- **Burst**: 10 calls per second

### Property Limits

- **50 unique properties** per single page (exclusive of pageName)
- **500 unique properties** across all pages
- **1,000 unique pageName values** site-wide

---

## ✅ GOOD IMPLEMENTATION EXAMPLES

### Example 1: Search Results Page

```javascript
// GOOD: Comprehensive search results context
function setSearchPageProperties(searchResults) {
  FS('setProperties', {
    type: 'page',
    properties: {
      // Page naming for Journeys
      pageName: 'Search Results',

      // Search context
      searchTerm: searchResults.query,
      searchType: searchResults.type, // 'keyword', 'category', 'tag'

      // Results info
      resultsCount: searchResults.total,
      resultsShown: searchResults.items.length,
      hasResults: searchResults.total > 0,

      // Filters applied
      activeFilters: Object.keys(searchResults.filters),
      filterCount: Object.keys(searchResults.filters).length,
      priceRangeMin: searchResults.filters.price?.min,
      priceRangeMax: searchResults.filters.price?.max,
      categoryFilter: searchResults.filters.category,

      // Sorting
      sortBy: searchResults.sortBy,
      sortOrder: searchResults.sortOrder,

      // Pagination
      currentPage: searchResults.page,
      totalPages: searchResults.totalPages,
    },
  })
}

// Call when search results load
const results = await performSearch(query, filters)
setSearchPageProperties(results)
```

**Why this is good:**

- ✅ Named page for Journey mapping
- ✅ Captures full search context
- ✅ Records filter state for analysis
- ✅ Enables "search with 0 results" segment

### Example 2: Product Detail Page

```javascript
// GOOD: Product page with full context
function setProductPageProperties(product) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Product Detail',

      // Product identification
      productId: product.id,
      productSku: product.sku,
      productName: product.name,

      // Categorization
      category: product.category,
      subcategory: product.subcategory,
      brand: product.brand,

      // Pricing
      price: product.price,
      originalPrice: product.originalPrice,
      onSale: product.price < product.originalPrice,
      discountPercent: product.discountPercent,
      currency: product.currency,

      // Inventory
      inStock: product.inStock,
      stockLevel: product.stockQuantity,

      // Ratings
      averageRating: product.rating.average,
      reviewCount: product.rating.count,

      // Variants
      availableColors: product.variants.colors,
      availableSizes: product.variants.sizes,
    },
  })
}

// Call when product page loads
setProductPageProperties(productData)
```

**Why this is good:**

- ✅ Full product context for session search
- ✅ Pricing data for conversion analysis
- ✅ Inventory context for experience analysis
- ✅ Can segment by "viewed out-of-stock items"

### Example 3: Checkout Flow with Step Tracking

```javascript
// GOOD: Checkout with step and cart context
class CheckoutPageProperties {
  setCartReviewStep(cart) {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Checkout',
        checkoutStep: 1,
        checkoutStepName: 'Cart Review',

        cartId: cart.id,
        cartValue: cart.subtotal,
        cartItemCount: cart.items.length,

        hasCoupon: !!cart.coupon,
        couponCode: cart.coupon,
        discountAmount: cart.discount,

        estimatedShipping: cart.shipping.estimate,
        estimatedTax: cart.tax.estimate,
        estimatedTotal: cart.total,
      },
    })
  }

  setShippingStep(cart, shippingOptions) {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Checkout',
        checkoutStep: 2,
        checkoutStepName: 'Shipping',

        cartValue: cart.subtotal,
        cartItemCount: cart.items.length,

        shippingOptionsCount: shippingOptions.length,
        cheapestShipping: shippingOptions[0]?.price,
        fastestShipping: shippingOptions.find((o) => o.fastest)?.name,
      },
    })
  }

  setPaymentStep(cart, selectedShipping) {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Checkout',
        checkoutStep: 3,
        checkoutStepName: 'Payment',

        cartValue: cart.subtotal,
        shippingMethod: selectedShipping.name,
        shippingCost: selectedShipping.price,

        totalBeforePayment: cart.total,
        paymentMethodsAvailable: getAvailablePaymentMethods(),
      },
    })
  }

  setConfirmationStep(order) {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Order Confirmation',
        checkoutStep: 4,
        checkoutStepName: 'Confirmation',

        orderId: order.id,
        orderTotal: order.total,
        paymentMethod: order.paymentMethod,
        shippingMethod: order.shippingMethod,
        estimatedDelivery: order.estimatedDelivery,
      },
    })
  }
}
```

**Why this is good:**

- ✅ Same pageName groups checkout steps
- ✅ Step numbers enable drop-off analysis
- ✅ Cart value context throughout
- ✅ Each step has relevant context

### Example 4: SPA Navigation Handler

```javascript
// GOOD: Handle SPA route changes with page properties
class SPAPagePropertyManager {
  constructor() {
    this.routeHandlers = new Map()
    this.setupRouteListener()
  }

  setupRouteListener() {
    // For React Router, Vue Router, etc.
    window.addEventListener('popstate', () => this.handleRouteChange())

    // Intercept pushState/replaceState
    const originalPushState = history.pushState
    history.pushState = (...args) => {
      originalPushState.apply(history, args)
      this.handleRouteChange()
    }
  }

  registerRoute(pathPattern, handler) {
    this.routeHandlers.set(pathPattern, handler)
  }

  handleRouteChange() {
    const path = window.location.pathname

    // Find matching route handler
    for (const [pattern, handler] of this.routeHandlers) {
      const match = path.match(pattern)
      if (match) {
        const properties = handler(match, path)
        if (properties) {
          FS('setProperties', {
            type: 'page',
            properties,
          })
        }
        return
      }
    }

    // Default page properties
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: this.inferPageName(path),
        path: path,
      },
    })
  }

  inferPageName(path) {
    const segments = path.split('/').filter(Boolean)
    return segments.length > 0
      ? segments.map((s) => s.charAt(0).toUpperCase() + s.slice(1)).join(' ')
      : 'Home'
  }
}

// Setup
const pageManager = new SPAPagePropertyManager()

pageManager.registerRoute(/^\/products\/([^/]+)$/, (match) => ({
  pageName: 'Product Detail',
  productSlug: match[1],
}))

pageManager.registerRoute(/^\/search$/, () => ({
  pageName: 'Search Results',
  // Additional properties set by search handler
}))

pageManager.registerRoute(/^\/checkout\/(.+)$/, (match) => ({
  pageName: 'Checkout',
  checkoutStepSlug: match[1],
}))
```

**Why this is good:**

- ✅ Handles SPA navigation properly
- ✅ Consistent page naming
- ✅ Route-specific properties
- ✅ Fallback for unregistered routes

### Example 5: Dashboard with Dynamic Context

```javascript
// GOOD: Dashboard with view state properties
function setDashboardPageProperties(dashboardState) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Dashboard',

      // View configuration
      dashboardView: dashboardState.activeView,
      dateRange: dashboardState.dateRange.label,
      dateRangeStart: dashboardState.dateRange.start,
      dateRangeEnd: dashboardState.dateRange.end,

      // Active filters
      segmentFilter: dashboardState.segment,
      channelFilter: dashboardState.channel,
      regionFilter: dashboardState.region,

      // Widget state
      visibleWidgets: dashboardState.widgets.map((w) => w.id),
      widgetCount: dashboardState.widgets.length,

      // Data state
      dataLoaded: dashboardState.isLoaded,
      hasData: dashboardState.hasData,
      recordCount: dashboardState.recordCount,
    },
  })
}

// Update properties when dashboard state changes
dashboardStore.subscribe((state) => {
  setDashboardPageProperties(state)
})
```

**Why this is good:**

- ✅ Captures dashboard configuration
- ✅ Tracks filter/segment context
- ✅ Updates on state changes
- ✅ Enables analysis of how users configure dashboards

### Example 6: Content/Article Page

```javascript
// GOOD: Article page with content metadata
function setArticlePageProperties(article) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Article',

      // Content identification
      articleId: article.id,
      articleSlug: article.slug,
      articleTitle: article.title,

      // Categorization
      category: article.category,
      tags: article.tags,
      contentType: article.type, // 'blog', 'tutorial', 'news'

      // Author info
      authorId: article.author.id,
      authorName: article.author.name,

      // Dates
      publishDate: article.publishedAt,
      lastUpdated: article.updatedAt,

      // Content metrics
      wordCount: article.wordCount,
      estimatedReadTime: article.readTime,
      hasVideo: article.hasVideo,
      imageCount: article.images.length,

      // Engagement indicators
      commentCount: article.comments.count,
      likeCount: article.likes,
      shareCount: article.shares,
    },
  })
}

// Call when article loads
setArticlePageProperties(articleData)
```

**Why this is good:**

- ✅ Rich content metadata
- ✅ Enables content performance analysis
- ✅ Author attribution for patterns
- ✅ Engagement context

---

## ❌ BAD IMPLEMENTATION EXAMPLES

### Example 1: Missing pageName

```javascript
// BAD: No pageName - can't use in Journeys
FS('setProperties', {
  type: 'page',
  properties: {
    category: 'Electronics',
    sortBy: 'price',
  },
})
```

**Why this is bad:**

- ❌ Page won't appear in Journeys
- ❌ Hard to identify page type in search
- ❌ Missing semantic naming

**CORRECTED VERSION:**

```javascript
// GOOD: Include pageName
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Category Page',
    category: 'Electronics',
    sortBy: 'price',
  },
})
```

### Example 2: Wrong Type Parameter

```javascript
// BAD: Using 'user' type for page data
FS('setProperties', {
  type: 'user', // Wrong type!
  properties: {
    currentPage: 'Search Results',
    searchTerm: 'laptops',
  },
})
```

**Why this is bad:**

- ❌ Page context becomes user property
- ❌ Pollutes user profile with transient data
- ❌ Won't reset on navigation

**CORRECTED VERSION:**

```javascript
// GOOD: Use 'page' type
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Search Results',
    searchTerm: 'laptops',
  },
})
```

### Example 3: Exceeding pageName Limit

```javascript
// BAD: Dynamic pageName creating too many unique values
function setProductPage(product) {
  FS('setProperties', {
    type: 'page',
    properties: {
      // BAD: Product name as pageName creates 1000s of unique values
      pageName: product.name,
      productId: product.id,
    },
  })
}
```

**Why this is bad:**

- ❌ pageName limited to 1,000 unique values
- ❌ Will be ignored once limit reached
- ❌ Pollutes Journey definitions

**CORRECTED VERSION:**

```javascript
// GOOD: Generic pageName, specific properties
function setProductPage(product) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Product Detail', // Generic
      productName: product.name, // Specific as property
      productId: product.id,
      category: product.category,
    },
  })
}
```

### Example 4: Changing pageName on Same Page

```javascript
// BAD: Multiple different pageNames on same page
function updateFilters(filters) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: `Search - ${filters.category}`, // BAD: Changes pageName
      filters: Object.keys(filters),
    },
  })
}
```

**Why this is bad:**

- ❌ Later pageName calls are IGNORED
- ❌ Only first pageName sticks
- ❌ Creates confusion and missing data

**CORRECTED VERSION:**

```javascript
// GOOD: Set pageName once, update other properties
function setSearchPage(initialData) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Search Results', // Set once
      searchTerm: initialData.query,
    },
  })
}

function updateFilters(filters) {
  // Update properties without pageName
  FS('setProperties', {
    type: 'page',
    properties: {
      activeCategory: filters.category,
      filterCount: Object.keys(filters).length,
      filters: Object.keys(filters),
    },
  })
}
```

### Example 5: User Data in Page Properties

```javascript
// BAD: Putting user-specific data in page properties
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Dashboard',
    userId: user.id, // BAD: User data
    userEmail: user.email, // BAD: User data
    userPlan: user.plan, // BAD: User data
  },
})
```

**Why this is bad:**

- ❌ User data should be user properties
- ❌ Will reset on navigation
- ❌ Wrong scope for the data

**CORRECTED VERSION:**

```javascript
// GOOD: Separate user and page data
FS('setIdentity', {
  uid: user.id,
  properties: {
    email: user.email,
    plan: user.plan,
  },
})

FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Dashboard',
    dashboardView: 'analytics',
    dateRange: 'last30days',
  },
})
```

### Example 6: Not Calling on SPA Navigation

```javascript
// BAD: Only setting properties on initial load
document.addEventListener('DOMContentLoaded', () => {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Home',
    },
  })
  // Properties never updated for SPA navigation!
})
```

**Why this is bad:**

- ❌ SPA navigations don't trigger DOMContentLoaded
- ❌ Page properties become stale
- ❌ Wrong context after navigation

**CORRECTED VERSION:**

```javascript
// GOOD: Handle SPA navigation
function setPageProperties(route) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: route.name,
      ...route.properties,
    },
  })
}

// Call on initial load
setPageProperties(getCurrentRoute())

// Call on navigation
router.on('routeChange', (route) => {
  setPageProperties(route)
})
```

---

## COMMON IMPLEMENTATION PATTERNS

### Pattern 1: Page Property Initializer

```javascript
// Centralized page property management
class PagePropertyManager {
  constructor() {
    this.currentPageName = null
    this.baseProperties = {}
  }

  // Initialize page with base properties
  initialize(pageName, baseProps = {}) {
    this.currentPageName = pageName
    this.baseProperties = baseProps

    FS('setProperties', {
      type: 'page',
      properties: {
        pageName,
        ...baseProps,
        pageLoadTime: new Date().toISOString(),
      },
    })
  }

  // Add additional properties (merges with existing)
  addProperties(additionalProps) {
    FS('setProperties', {
      type: 'page',
      properties: additionalProps,
    })
  }

  // Update specific property
  updateProperty(key, value) {
    FS('setProperties', {
      type: 'page',
      properties: {
        [key]: value,
      },
    })
  }
}

// Usage
const pageProps = new PagePropertyManager()

// On page load
pageProps.initialize('Product Listing', {
  category: 'Electronics',
  totalProducts: 150,
})

// When user applies filter
pageProps.addProperties({
  activeFilters: ['brand:Apple', 'price:500-1000'],
  filteredCount: 23,
})
```

### Pattern 2: Route-Based Page Properties (React)

```jsx
// React component for automatic page properties
import {useEffect} from 'react'
import {useLocation, useParams} from 'react-router-dom'

function PagePropertySetter({pageName, children, getProperties}) {
  const location = useLocation()
  const params = useParams()

  useEffect(() => {
    const properties = getProperties ? getProperties(params, location) : {}

    FS('setProperties', {
      type: 'page',
      properties: {
        pageName,
        ...properties,
        path: location.pathname,
        queryParams: Object.fromEntries(new URLSearchParams(location.search)),
      },
    })
  }, [pageName, location, params, getProperties])

  return children
}

// Usage
function App() {
  return (
    <Routes>
      <Route
        path="/products/:category"
        element={
          <PagePropertySetter
            pageName="Product Listing"
            getProperties={(params) => ({
              category: params.category,
            })}
          >
            <ProductListingPage />
          </PagePropertySetter>
        }
      />
      <Route
        path="/product/:id"
        element={
          <PagePropertySetter
            pageName="Product Detail"
            getProperties={(params) => ({
              productId: params.id,
            })}
          >
            <ProductDetailPage />
          </PagePropertySetter>
        }
      />
    </Routes>
  )
}
```

### Pattern 3: Search Page Property Handler

```javascript
// Complete search page property management
class SearchPageProperties {
  constructor() {
    this.initialized = false
  }

  initialize() {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Search Results',
      },
    })
    this.initialized = true
  }

  setSearchContext(query, results) {
    if (!this.initialized) this.initialize()

    FS('setProperties', {
      type: 'page',
      properties: {
        searchTerm: query.term,
        searchCategory: query.category,
        resultsCount: results.total,
        hasResults: results.total > 0,
        responseTime: results.timing,
      },
    })
  }

  setFilters(filters) {
    FS('setProperties', {
      type: 'page',
      properties: {
        activeFilters: filters.active,
        filterCount: filters.active.length,
        priceMin: filters.price?.min,
        priceMax: filters.price?.max,
        brandFilters: filters.brands,
        ratingFilter: filters.minRating,
      },
    })
  }

  setSorting(sort) {
    FS('setProperties', {
      type: 'page',
      properties: {
        sortField: sort.field,
        sortDirection: sort.direction,
      },
    })
  }

  setPagination(page, total) {
    FS('setProperties', {
      type: 'page',
      properties: {
        currentPage: page,
        totalPages: total,
      },
    })
  }
}
```

---

## RELATIONSHIP WITH OTHER APIs

### Page Properties + User Properties

```javascript
// User properties: who they are
FS('setIdentity', {
  uid: user.id,
  properties: {
    plan: 'enterprise',
    role: 'admin',
  },
})

// Page properties: where they are and what they're doing
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Reports Dashboard',
    reportType: 'revenue',
    dateRange: 'last_quarter',
  },
})
```

### Page Properties + Events

```javascript
// Set page context
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Product Detail',
    productId: 'SKU-123',
    price: 99.99,
  },
})

// Events inherit page context for search
FS('trackEvent', {
  name: 'Add to Cart',
  properties: {
    quantity: 2,
  },
})
// This event is searchable via: "Add to Cart on Product Detail page"
```

### Page Properties + Element Properties

```javascript
// Page-level context
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Search Results',
    searchTerm: 'laptop',
    resultsCount: 50,
  },
})

// Element-level context (on each product card)
// data-fs-properties-schema for product-specific data
// Elements inherit page properties automatically
```

---

## TROUBLESHOOTING

### pageName Not Showing in Journeys

**Symptom**: Pages don't appear in Journey builder

**Common Causes**:

1. ❌ pageName never set
2. ❌ Exceeded 1,000 unique pageName limit
3. ❌ Trying to change pageName on same page

**Solutions**:

- ✅ Always set pageName first
- ✅ Use generic pageName values
- ✅ Check pageName count in Fullstory

### Properties Not Persisting

**Symptom**: Properties disappear mid-session

**Common Causes**:

1. ❌ URL path changed (SPA navigation)
2. ❌ Using user type instead of page type
3. ❌ Properties overwritten, not merged

**Solutions**:

- ✅ Re-set properties after navigation
- ✅ Verify type: 'page' is used
- ✅ Properties merge automatically

### SPA Navigation Not Tracked

**Symptom**: All SPA pages have same properties

**Common Causes**:

1. ❌ Not calling setProperties on navigation
2. ❌ Only setting on initial page load
3. ❌ Route change not detected

**Solutions**:

- ✅ Listen for route changes
- ✅ Set properties on each navigation
- ✅ Use router hooks/events

---

## LIMITS AND CONSTRAINTS

### pageName Limits

- Maximum 1,000 unique pageName values site-wide
- Additional pageNames are ignored
- Use generic names, not dynamic values

### Property Limits

- 50 unique properties per page
- 500 unique properties across all pages
- Property names: alphanumeric, underscores, hyphens

### Call Frequency

- **Sustained**: 30 calls per page per minute
- **Burst**: 10 calls per second

---

## KEY TAKEAWAYS FOR AGENT

When helping developers implement Page Properties:

1. **Always emphasize**:
   - Include pageName - it enriches ALL events on that page (not just Journeys)
   - Use generic pageName values (max 1,000) + properties for variations
   - Re-set properties on SPA navigation
   - Page properties enable filtering across Search, Segments, Funnels, Metrics, and Dashboards

2. **Common mistakes to watch for**:
   - Missing pageName property
   - Dynamic pageName values (product names)
   - Changing pageName on same page (ignored)
   - User data in page properties
   - Not handling SPA navigation

3. **Questions to ask developers**:
   - Is this a SPA or traditional navigation?
   - What page types do you have?
   - What context is relevant to this page?
   - Do you need this in Journeys?

4. **Best practices to recommend**:
   - Set pageName first, then other properties
   - Use generic pageName (max 10-50 values)
   - Store product/user-specific data as properties, not pageName
   - Handle route changes in SPAs

---

## REFERENCE LINKS

- **Set Page Properties**: https://developer.fullstory.com/browser/set-page-properties/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Help Center - Page Properties**: https://help.fullstory.com/hc/en-us/articles/360020623454

---

_This skill document was created to help Agent understand and guide developers in implementing Fullstory's Page Properties API correctly for web applications._
