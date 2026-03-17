---
name: fullstory-ecommerce
version: v2
description: Industry-specific guide for implementing Fullstory in e-commerce and retail applications. Covers conversion funnel optimization, product interaction tracking, cart abandonment analysis, checkout flow privacy (PCI compliance), and customer journey mapping. Includes detailed examples for product pages, cart, checkout, and post-purchase experiences.
related_skills:
  - fullstory-privacy-controls
  - fullstory-privacy-strategy
  - fullstory-analytics-events
  - fullstory-page-properties
  - fullstory-element-properties
---

# Fullstory for E-Commerce & Retail

> ⚠️ **LEGAL DISCLAIMER**: This guidance is for educational purposes only and does not constitute legal, compliance, or regulatory advice. E-commerce regulations (PCI DSS for payments, GDPR, CCPA, consumer protection laws) vary by jurisdiction. Always consult with your legal and compliance teams before implementing any data capture solution. Your organization is responsible for ensuring compliance with all applicable regulations.

## Industry Overview

E-commerce has unique opportunities and requirements for session analytics:

- **High analytics value**: Product interactions, funnels, conversions directly impact revenue
- **Rich behavioral data**: Browse patterns, search, filters, comparisons
- **PCI compliance**: Payment flows require careful handling
- **Customer journey focus**: Multi-session journeys, cross-device behavior
- **A/B testing**: Variant analysis is crucial

### Key Goals for E-Commerce Implementations

1. **Optimize conversion funnels** from browse to purchase
2. **Understand product engagement** (views, interactions, comparisons)
3. **Reduce cart abandonment** by identifying friction
4. **Improve search and discovery** UX
5. **Analyze post-purchase experience** (returns, support)

---

## What Can Be Captured in E-Commerce

Unlike banking, e-commerce has more data that can (and should) be captured:

| Data Type        | Capture?    | Privacy Level | Why                        |
| ---------------- | ----------- | ------------- | -------------------------- |
| Product names    | ✅ Yes      | Unmask        | Core analytics value       |
| Product IDs/SKUs | ✅ Yes      | Unmask        | Segmentation               |
| Prices           | ✅ Yes      | Unmask        | Conversion analysis        |
| Categories       | ✅ Yes      | Unmask        | Journey analysis           |
| Search queries   | ⚠️ Consider | Unmask/Mask   | Usually OK, review for PII |
| Cart contents    | ✅ Yes      | Unmask        | Abandonment analysis       |
| Order totals     | ✅ Yes      | Unmask        | Revenue tracking           |
| Customer name    | ⚠️ Mask     | Mask          | PII but low risk           |
| Email            | ⚠️ Consider | Hash/Mask     | For user linking           |
| Shipping address | ⚠️ Mask     | Mask          | PII                        |
| Payment card     | ❌ Never    | Exclude       | PCI compliance             |
| CVV              | ❌ Never    | Exclude       | PCI compliance             |

---

## Implementation Architecture

### Privacy Zones for E-Commerce

```
┌─────────────────────────────────────────────────────────────────┐
│                    E-COMMERCE APPLICATION                        │
├─────────────────────────────────────────────────────────────────┤
│  FULLY VISIBLE (fs-unmask)                                       │
│  • Product listings and details                                  │
│  • Prices, discounts, promotions                                │
│  • Category navigation, filters                                  │
│  • Search results                                               │
│  • Cart contents                                                │
│  • Error messages                                               │
│  • UI controls, buttons                                         │
├─────────────────────────────────────────────────────────────────┤
│  MASKED (fs-mask)                                                │
│  • Customer names                                               │
│  • Email addresses                                              │
│  • Phone numbers                                                │
│  • Shipping/billing addresses                                   │
│  • Order confirmation numbers (optional)                        │
├─────────────────────────────────────────────────────────────────┤
│  EXCLUDED (fs-exclude)                                           │
│  • Credit card numbers                                          │
│  • CVV/security codes                                           │
│  • Full card expiry                                             │
│  • PayPal/payment credentials                                   │
│  • Gift card codes (if high value)                              │
│  • Promo codes (if single-use/valuable)                         │
└─────────────────────────────────────────────────────────────────┘
```

### Marketplace Considerations

For multi-vendor marketplaces, additional considerations apply:

| Scenario                    | Privacy Implication                                                  |
| --------------------------- | -------------------------------------------------------------------- |
| **Seller data**             | Mask seller personal info (name, location); keep store/business name |
| **Buyer-seller messaging**  | EXCLUDE all message content                                          |
| **Seller performance data** | Exclude revenue, exact sales counts; use bands                       |
| **Cross-seller analytics**  | Never capture data that reveals competitive intelligence             |
| **Seller onboarding**       | Exclude bank details, tax IDs; track flow completion only            |

```javascript
// Marketplace: Track seller interaction without revealing seller economics
FS('trackEvent', {
  name: 'seller_product_viewed',
  properties: {
    product_category: 'electronics',
    seller_rating_band: '4.5-5.0', // Band, not exact rating
    seller_review_volume: 'high', // "high", "medium", "low"
    marketplace_verified: true,
    // NEVER: seller revenue, exact sales, or seller contact info
  },
})
```

### User Identification Pattern

```javascript
// E-Commerce: Multiple identification stages

// 1. Anonymous visitor (before account creation)
// Fullstory auto-assigns anonymous ID

// 2. Email captured (newsletter, cart)
function onEmailCapture(email) {
  // Option A: Use hashed email (for cross-device matching)
  FS('setIdentity', {
    uid: sha256(email.toLowerCase().trim()),
  })

  // Option B: Wait for account creation, use customer ID
  // (Preferred if you have account system)
}

// 3. Account created or logged in
function onLogin(customer) {
  FS('setIdentity', {
    uid: customer.id, // e.g., "cust_12345"
    displayName: customer.firstName, // Just first name
  })

  FS('setProperties', {
    type: 'user',
    properties: {
      // Customer value metrics
      customer_type: customer.isGuest ? 'guest' : 'registered',
      account_age_days: daysSince(customer.createdAt),
      lifetime_order_count: customer.orderCount,
      lifetime_value_band: getValueBand(customer.ltv), // "$0-100", "$100-500", etc.

      // Engagement signals
      has_wishlist: customer.wishlistCount > 0,
      has_saved_payment: customer.hasSavedPayment,
      email_subscribed: customer.emailOptIn,
      loyalty_tier: customer.loyaltyTier, // "bronze", "silver", "gold"

      // Preferences
      preferred_category: customer.topCategory,
      preferred_brand: customer.topBrand,

      // Technical
      app_installed: customer.hasApp,
      push_enabled: customer.pushOptIn,
    },
  })
}
```

---

## Page-by-Page Implementation

### Homepage

```html
<!-- E-Commerce Homepage -->
<div class="homepage">
  <!-- Hero banner - visible -->
  <section class="hero fs-unmask">
    <h1>Holiday Sale - Up to 50% Off</h1>
    <a href="/sale" class="cta">Shop Now</a>
  </section>

  <!-- Category navigation - visible -->
  <nav class="category-nav fs-unmask">
    <a href="/electronics">Electronics</a>
    <a href="/clothing">Clothing</a>
    <a href="/home">Home & Garden</a>
  </nav>

  <!-- Featured products - visible -->
  <section class="featured-products fs-unmask">
    <h2>Featured Products</h2>
    <div class="product-grid">
      <div
        class="product-card"
        data-fs-element="Product Card"
        data-fs-properties-schema='{"product_id":"string","product_name":"string","price":"real","category":"string"}'
      >
        <img src="product.jpg" alt="Wireless Headphones" />
        <h3>Wireless Headphones</h3>
        <p class="price">$199.99</p>
        <button>Add to Cart</button>
      </div>
      <!-- More products... -->
    </div>
  </section>

  <!-- Personalized recommendations - visible (product data is not PII) -->
  <section class="recommendations fs-unmask">
    <h2>Recommended for You</h2>
    <!-- Products based on browsing history -->
  </section>
</div>
```

```javascript
// Homepage tracking
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'homepage',
    has_active_promotion: true,
    promotion_name: 'holiday_sale_2024',
    featured_product_count: 8,
    recommendation_engine: 'collaborative_filtering',
  },
})
```

### Product Listing Page (PLP)

```html
<!-- Product Listing Page -->
<div class="plp">
  <!-- Breadcrumb - visible -->
  <nav class="breadcrumb fs-unmask">
    <a href="/">Home</a> &gt; <a href="/electronics">Electronics</a> &gt;
    <span>Headphones</span>
  </nav>

  <!-- Search/Filter bar - visible -->
  <div class="filter-bar fs-unmask">
    <div class="search-box">
      <input type="text" placeholder="Search headphones..." />
      <button>Search</button>
    </div>

    <div class="filters">
      <select name="brand">
        <option>All Brands</option>
        <option>Sony</option>
        <option>Bose</option>
      </select>

      <select name="price">
        <option>Any Price</option>
        <option>Under $50</option>
        <option>$50 - $100</option>
        <option>$100 - $200</option>
        <option>$200+</option>
      </select>

      <select name="sort">
        <option>Relevance</option>
        <option>Price: Low to High</option>
        <option>Price: High to Low</option>
        <option>Best Sellers</option>
        <option>Newest</option>
      </select>
    </div>
  </div>

  <!-- Results count - visible -->
  <p class="results-count fs-unmask">Showing 48 results</p>

  <!-- Product grid - fully visible -->
  <div class="product-grid fs-unmask">
    <div
      class="product-card"
      data-fs-element="Product Card"
      data-fs-properties-schema='{"product_id":"string","product_name":"string","price":"real","list_position":"int"}'
    >
      <img src="headphones.jpg" alt="Sony WH-1000XM5" />
      <h3>Sony WH-1000XM5</h3>
      <div class="rating">★★★★★ (2,345 reviews)</div>
      <p class="price">$349.99</p>
      <p class="badge">Best Seller</p>
      <button>Add to Cart</button>
      <button>♡ Wishlist</button>
    </div>
    <!-- More products... -->
  </div>

  <!-- Pagination - visible -->
  <div class="pagination fs-unmask">
    <button>Previous</button>
    <span>Page 1 of 4</span>
    <button>Next</button>
  </div>
</div>
```

```javascript
// PLP page properties
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'product_listing',
    category: 'Electronics > Headphones',
    category_depth: 2,
    result_count: 48,
    has_active_filters: true,
    active_filters: ['brand:Sony,Bose', 'price:100-200'],
    sort_order: 'relevance',
    page_number: 1,
  },
})

// Filter tracking
function onFilterChange(filters) {
  FS('trackEvent', {
    name: 'filter_applied',
    properties: {
      category: currentCategory,
      filter_type: filters.changed, // "brand", "price", "rating"
      filter_value: filters.value,
      result_count_after: filters.resultCount,
    },
  })
}

// Sort tracking
function onSortChange(sortOrder) {
  FS('trackEvent', {
    name: 'sort_changed',
    properties: {
      category: currentCategory,
      sort_order: sortOrder,
      result_count: resultCount,
    },
  })
}

// Product impression tracking
function trackProductImpressions(products) {
  products.forEach((product, index) => {
    FS('trackEvent', {
      name: 'product_impression',
      properties: {
        product_id: product.id,
        product_name: product.name,
        price: product.price,
        list_position: index + 1,
        list_type: 'category_listing',
      },
    })
  })
}
```

### Product Detail Page (PDP)

```html
<!-- Product Detail Page -->
<div class="pdp">
  <!-- Breadcrumb - visible -->
  <nav class="breadcrumb fs-unmask">
    <a href="/">Home</a> &gt; <a href="/electronics">Electronics</a> &gt;
    <a href="/headphones">Headphones</a> &gt;
    <span>Sony WH-1000XM5</span>
  </nav>

  <!-- Product main section - fully visible -->
  <div class="product-main fs-unmask">
    <!-- Images -->
    <div class="product-images">
      <img src="main.jpg" alt="Sony WH-1000XM5" class="main-image" />
      <div class="thumbnail-gallery">
        <img src="thumb1.jpg" alt="View 1" />
        <img src="thumb2.jpg" alt="View 2" />
        <img src="thumb3.jpg" alt="View 3" />
      </div>
    </div>

    <!-- Product info -->
    <div
      class="product-info"
      data-fs-element="Product Info"
      data-fs-properties-schema='{"product_id":"string","product_name":"string","brand":"string","price":"real","category":"string"}'
    >
      <h1>Sony WH-1000XM5 Wireless Headphones</h1>
      <p class="brand">by Sony</p>
      <div class="rating">★★★★★ 4.8 (2,345 reviews)</div>

      <div class="price-section">
        <span class="current-price">$349.99</span>
        <span class="original-price">$399.99</span>
        <span class="discount">Save 12%</span>
      </div>

      <!-- Variants - visible -->
      <div class="variants">
        <label>Color:</label>
        <div class="color-options">
          <button class="selected">Black</button>
          <button>Silver</button>
          <button>Midnight Blue</button>
        </div>
      </div>

      <!-- Add to cart - visible -->
      <div class="actions">
        <div class="quantity">
          <button>-</button>
          <input type="number" value="1" min="1" />
          <button>+</button>
        </div>
        <button class="add-to-cart">Add to Cart</button>
        <button class="wishlist">♡ Add to Wishlist</button>
      </div>

      <!-- Availability -->
      <p class="availability">✓ In Stock - Ships within 24 hours</p>
    </div>
  </div>

  <!-- Product details tabs - visible -->
  <div class="product-tabs fs-unmask">
    <div class="tab-nav">
      <button class="active">Description</button>
      <button>Specifications</button>
      <button>Reviews</button>
    </div>

    <div class="tab-content">
      <div class="description">
        <p>Industry-leading noise cancellation...</p>
      </div>
    </div>
  </div>

  <!-- Reviews section - visible (user names are public) -->
  <div class="reviews-section fs-unmask">
    <h2>Customer Reviews</h2>
    <div class="review">
      <div class="review-header">
        <span class="author">John D.</span>
        <span class="rating">★★★★★</span>
        <span class="date">Nov 15, 2024</span>
      </div>
      <p class="review-text">Amazing noise cancellation...</p>
    </div>
  </div>

  <!-- Related products - visible -->
  <div class="related-products fs-unmask">
    <h2>You May Also Like</h2>
    <!-- Product cards -->
  </div>
</div>
```

```javascript
// PDP page properties
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'product_detail',
    product_id: 'SKU-12345',
    product_name: 'Sony WH-1000XM5 Wireless Headphones',
    brand: 'Sony',
    category: 'Electronics > Headphones > Wireless',
    price: 349.99,
    original_price: 399.99,
    discount_percent: 12,
    is_on_sale: true,
    in_stock: true,
    review_count: 2345,
    average_rating: 4.8,
    variant_selected: 'Black',
  },
})

// Product view event
FS('trackEvent', {
  name: 'product_viewed',
  properties: {
    product_id: 'SKU-12345',
    product_name: 'Sony WH-1000XM5 Wireless Headphones',
    brand: 'Sony',
    category: 'Electronics > Headphones',
    price: 349.99,
    referrer_type: getReferrerType(), // "search", "category", "recommendation"
    time_on_page_seconds: 0, // Will be updated on exit
  },
})

// Variant selection
function onVariantSelect(variant) {
  FS('trackEvent', {
    name: 'variant_selected',
    properties: {
      product_id: product.id,
      variant_type: variant.type, // "color", "size"
      variant_value: variant.value, // "Black", "Large"
      price_change: variant.priceDiff,
    },
  })
}

// Image interaction
function onImageInteraction(action) {
  FS('trackEvent', {
    name: 'image_interaction',
    properties: {
      product_id: product.id,
      action: action, // "zoom", "gallery_view", "thumbnail_click"
      image_index: currentImageIndex,
    },
  })
}

// Tab view
function onTabClick(tabName) {
  FS('trackEvent', {
    name: 'product_tab_viewed',
    properties: {
      product_id: product.id,
      tab_name: tabName, // "description", "specifications", "reviews"
    },
  })
}
```

### Shopping Cart

```html
<!-- Shopping Cart Page -->
<div class="cart-page">
  <h1 class="fs-unmask">Your Cart (3 items)</h1>

  <!-- Cart items - fully visible (products, not PII) -->
  <div class="cart-items fs-unmask">
    <div
      class="cart-item"
      data-fs-element="Cart Item"
      data-fs-properties-schema='{"product_id":"string","product_name":"string","quantity":"int","unit_price":"real","line_total":"real"}'
    >
      <img src="headphones.jpg" alt="Sony WH-1000XM5" />
      <div class="item-details">
        <h3>Sony WH-1000XM5</h3>
        <p>Color: Black</p>
        <p class="price">$349.99</p>
      </div>
      <div class="quantity">
        <button>-</button>
        <input type="number" value="1" />
        <button>+</button>
      </div>
      <div class="line-total">$349.99</div>
      <button class="remove">Remove</button>
    </div>

    <!-- More items... -->
  </div>

  <!-- Promo code - consider masking single-use codes -->
  <div class="promo-code fs-unmask">
    <input type="text" placeholder="Enter promo code" />
    <button>Apply</button>
  </div>

  <!-- Order summary - visible -->
  <div class="order-summary fs-unmask">
    <div class="summary-row">
      <span>Subtotal</span>
      <span>$549.97</span>
    </div>
    <div class="summary-row">
      <span>Shipping</span>
      <span>FREE</span>
    </div>
    <div class="summary-row">
      <span>Estimated Tax</span>
      <span>$44.00</span>
    </div>
    <div class="summary-row total">
      <span>Total</span>
      <span>$593.97</span>
    </div>
  </div>

  <!-- Actions - visible -->
  <div class="cart-actions fs-unmask">
    <a href="/shop">Continue Shopping</a>
    <button class="checkout">Proceed to Checkout</button>
  </div>
</div>
```

```javascript
// Cart page properties
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'cart',
    cart_item_count: 3,
    cart_unique_products: 2,
    cart_subtotal: 549.97,
    cart_total: 593.97,
    has_promo_applied: false,
    shipping_type: 'free',
  },
})

// Cart view event
FS('trackEvent', {
  name: 'cart_viewed',
  properties: {
    cart_id: cart.id,
    item_count: cart.items.length,
    cart_value: cart.total,
    products: cart.items.map((item) => ({
      product_id: item.productId,
      product_name: item.name,
      quantity: item.quantity,
      price: item.price,
    })),
  },
})

// Quantity change
function onQuantityChange(item, newQty, oldQty) {
  FS('trackEvent', {
    name: 'cart_quantity_changed',
    properties: {
      product_id: item.productId,
      product_name: item.name,
      old_quantity: oldQty,
      new_quantity: newQty,
      quantity_change: newQty - oldQty,
    },
  })
}

// Item removed
function onRemoveItem(item) {
  FS('trackEvent', {
    name: 'product_removed_from_cart',
    properties: {
      product_id: item.productId,
      product_name: item.name,
      price: item.price,
      quantity: item.quantity,
      removal_method: 'remove_button', // or "quantity_zero"
    },
  })
}

// Promo code
function onPromoApply(code, success, discount) {
  FS('trackEvent', {
    name: 'promo_code_applied',
    properties: {
      success: success,
      discount_amount: success ? discount : 0,
      discount_type: success ? 'percentage' : null, // or "fixed"
      // Don't send the actual code (could be valuable)
    },
  })
}
```

### Checkout Flow

```html
<!-- Checkout Page - MIXED PRIVACY -->
<div class="checkout-page">
  <h1 class="fs-unmask">Checkout</h1>

  <!-- Progress indicator - visible -->
  <div class="checkout-progress fs-unmask">
    <span class="active">1. Shipping</span>
    <span>2. Payment</span>
    <span>3. Review</span>
  </div>

  <!-- Shipping Information - MASK PII -->
  <section class="shipping-section">
    <h2 class="fs-unmask">Shipping Address</h2>

    <div class="address-form fs-mask">
      <div class="form-row">
        <label>First Name</label>
        <input type="text" name="firstName" />
      </div>
      <div class="form-row">
        <label>Last Name</label>
        <input type="text" name="lastName" />
      </div>
      <div class="form-row">
        <label>Email</label>
        <input type="email" name="email" />
      </div>
      <div class="form-row">
        <label>Phone</label>
        <input type="tel" name="phone" />
      </div>
      <div class="form-row">
        <label>Address</label>
        <input type="text" name="address1" />
      </div>
      <div class="form-row">
        <label>City</label>
        <input type="text" name="city" />
      </div>
      <div class="form-row">
        <label>State</label>
        <select name="state">
          <!-- States -->
        </select>
      </div>
      <div class="form-row">
        <label>ZIP Code</label>
        <input type="text" name="zip" />
      </div>
    </div>
  </section>

  <!-- Shipping Method - visible -->
  <section class="shipping-method fs-unmask">
    <h2>Shipping Method</h2>
    <label>
      <input type="radio" name="shipping" value="standard" />
      Standard (5-7 days) - FREE
    </label>
    <label>
      <input type="radio" name="shipping" value="express" />
      Express (2-3 days) - $9.99
    </label>
    <label>
      <input type="radio" name="shipping" value="overnight" />
      Overnight - $24.99
    </label>
  </section>

  <!-- Payment Information - EXCLUDE -->
  <section class="payment-section">
    <h2 class="fs-unmask">Payment Method</h2>

    <!-- Payment type selector - visible -->
    <div class="payment-type fs-unmask">
      <label>
        <input type="radio" name="payment" value="card" />
        Credit/Debit Card
      </label>
      <label>
        <input type="radio" name="payment" value="paypal" />
        PayPal
      </label>
      <label>
        <input type="radio" name="payment" value="applepay" />
        Apple Pay
      </label>
    </div>

    <!-- Card form - EXCLUDE completely -->
    <div class="card-form fs-exclude">
      <div class="form-row">
        <label>Card Number</label>
        <input type="text" name="cardNumber" autocomplete="cc-number" />
      </div>
      <div class="form-row">
        <label>Expiry</label>
        <input type="text" name="expiry" autocomplete="cc-exp" />
      </div>
      <div class="form-row">
        <label>CVV</label>
        <input type="text" name="cvv" autocomplete="cc-csc" />
      </div>
      <div class="form-row">
        <label>Name on Card</label>
        <input type="text" name="cardName" />
      </div>
    </div>

    <!-- PayPal button (3rd party - exclude) -->
    <div class="paypal-button fs-exclude">
      <!-- PayPal iframe -->
    </div>
  </section>

  <!-- Order summary - visible -->
  <aside class="order-summary fs-unmask">
    <h2>Order Summary</h2>
    <div class="summary-items">
      <!-- Cart items visible -->
    </div>
    <div class="summary-totals">
      <p>Subtotal: $549.97</p>
      <p>Shipping: $9.99</p>
      <p>Tax: $44.00</p>
      <p class="total">Total: $603.96</p>
    </div>
  </aside>

  <!-- Actions - visible -->
  <div class="checkout-actions fs-unmask">
    <button type="button">Back to Cart</button>
    <button type="submit">Place Order</button>
  </div>
</div>
```

```javascript
// Checkout step tracking
function trackCheckoutStep(step, data) {
  FS('trackEvent', {
    name: 'checkout_step_completed',
    properties: {
      step_number: step,
      step_name: data.stepName, // "shipping", "payment", "review"
      cart_value: cart.total,
      item_count: cart.items.length,
    },
  })
}

// Shipping method selection
function onShippingMethodSelect(method) {
  FS('trackEvent', {
    name: 'shipping_method_selected',
    properties: {
      method: method.name, // "standard", "express", "overnight"
      cost: method.cost,
      delivery_days: method.deliveryDays,
    },
  })
}

// Payment method selection
function onPaymentMethodSelect(method) {
  FS('trackEvent', {
    name: 'payment_method_selected',
    properties: {
      method: method, // "card", "paypal", "applepay", "klarna"
    },
  })
}

// Checkout errors (sanitized)
function onCheckoutError(error) {
  FS('trackEvent', {
    name: 'checkout_error',
    properties: {
      step: currentStep,
      error_type: categorizeCheckoutError(error), // "validation", "payment_declined", "inventory"
      // NEVER include: card numbers, specific error messages with PII
    },
  })
}

// Order completed
function onOrderComplete(order) {
  FS('trackEvent', {
    name: 'purchase_completed',
    properties: {
      order_id: order.id,
      order_total: order.total,
      item_count: order.items.length,
      payment_method: order.paymentMethod,
      shipping_method: order.shippingMethod,
      has_promo: order.promoApplied,
      is_first_order: customer.orderCount === 1,
      // Product details
      products: order.items.map((item) => ({
        product_id: item.productId,
        product_name: item.name,
        category: item.category,
        price: item.price,
        quantity: item.quantity,
      })),
    },
  })
}
```

### Search Experience

```javascript
// Search tracking
function onSearch(query, results) {
  FS('trackEvent', {
    name: 'search_performed',
    properties: {
      search_query: query, // Usually OK, review for PII patterns
      result_count: results.length,
      has_results: results.length > 0,
      suggestion_used: wasSuggestionClicked,
      search_type: 'keyword', // or "voice", "visual"
    },
  })
}

// Search result click
function onSearchResultClick(product, position) {
  FS('trackEvent', {
    name: 'search_result_clicked',
    properties: {
      search_query: lastQuery,
      product_id: product.id,
      product_name: product.name,
      result_position: position,
      total_results: lastResultCount,
    },
  })
}

// No results
function onNoResults(query) {
  FS('trackEvent', {
    name: 'search_no_results',
    properties: {
      search_query: query,
      suggestions_shown: suggestionsShown,
    },
  })
}
```

---

## Cart Abandonment Analysis

### Key Events to Track

```javascript
// Add to cart
function onAddToCart(product, source) {
  FS('trackEvent', {
    name: 'product_added_to_cart',
    properties: {
      product_id: product.id,
      product_name: product.name,
      price: product.price,
      quantity: 1,
      category: product.category,
      add_source: source, // "pdp", "plp", "quick_add", "recommendation"
    },
  })
}

// Cart abandoned (on exit intent or timeout)
function onCartAbandoned(cart) {
  FS('trackEvent', {
    name: 'cart_abandoned',
    properties: {
      cart_id: cart.id,
      cart_value: cart.total,
      item_count: cart.items.length,
      time_since_last_activity_minutes: getInactivityMinutes(),
      checkout_step_reached: lastCheckoutStep || 'cart',
      abandonment_trigger: trigger, // "exit_intent", "timeout", "navigation_away"
    },
  })
}

// Session end with cart
window.addEventListener('beforeunload', () => {
  if (cart && cart.items.length > 0 && !orderCompleted) {
    FS('trackEvent', {
      name: 'session_ended_with_cart',
      properties: {
        cart_value: cart.total,
        item_count: cart.items.length,
        pages_viewed: pagesViewed,
        time_on_site_minutes: getSessionDuration(),
      },
    })
  }
})
```

---

## Common E-Commerce Patterns

### Product Interaction Tracking Component

```javascript
// React component for product cards with built-in tracking
function ProductCard({product, listType, position}) {
  const handleClick = () => {
    FS('trackEvent', {
      name: 'product_clicked',
      properties: {
        product_id: product.id,
        product_name: product.name,
        price: product.price,
        list_type: listType, // "search", "category", "recommendation", "cart_upsell"
        position: position,
      },
    })
  }

  const handleAddToCart = (e) => {
    e.stopPropagation()
    FS('trackEvent', {
      name: 'product_added_to_cart',
      properties: {
        product_id: product.id,
        product_name: product.name,
        price: product.price,
        add_source: listType,
      },
    })
    // Add to cart logic...
  }

  const handleWishlist = (e) => {
    e.stopPropagation()
    FS('trackEvent', {
      name: 'product_added_to_wishlist',
      properties: {
        product_id: product.id,
        product_name: product.name,
        price: product.price,
      },
    })
    // Wishlist logic...
  }

  return (
    <div
      className="product-card fs-unmask"
      onClick={handleClick}
      data-fs-element="Product Card"
      data-fs-properties-schema={JSON.stringify({
        product_id: 'string',
        product_name: 'string',
        price: 'real',
      })}
    >
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p className="price">${product.price}</p>
      <button onClick={handleAddToCart}>Add to Cart</button>
      <button onClick={handleWishlist}>♡</button>
    </div>
  )
}
```

### Customer Lifetime Value Bands

```javascript
// Convert LTV to privacy-safe bands
function getValueBand(ltv) {
  if (ltv === 0) return 'new'
  if (ltv < 100) return '$1-$99'
  if (ltv < 500) return '$100-$499'
  if (ltv < 1000) return '$500-$999'
  if (ltv < 5000) return '$1k-$5k'
  return '$5k+'
}
```

---

## A/B Testing Integration

```javascript
// Track A/B test variant
FS('setProperties', {
  type: 'user',
  properties: {
    // Experiment tracking
    ab_checkout_flow: experimentVariant('checkout_flow'), // "control", "variant_a"
    ab_product_recommendations: experimentVariant('recommendations'),
    ab_search_algorithm: experimentVariant('search'),
  },
})

// Track variant-specific events
function trackExperimentExposure(experimentName, variant) {
  FS('trackEvent', {
    name: 'experiment_exposure',
    properties: {
      experiment_name: experimentName,
      variant: variant,
      page: currentPage,
    },
  })
}
```

---

## KEY TAKEAWAYS FOR AGENT

When helping e-commerce clients with Fullstory:

1. **Product data is valuable**: Unlike banking, product names/prices/categories are core analytics - capture them
2. **PCI compliance still applies**: Payment forms must be excluded
3. **Cart abandonment is gold**: Track every step of the funnel
4. **Element properties on product cards**: Enable click analysis
5. **Search queries are usually OK**: But review for PII patterns (searching for people's names, addresses)
6. **Customer PII should be masked**: Names, addresses, emails
7. **Order details are valuable**: Capture order totals, item counts, product details

### Questions to Ask E-Commerce Clients

1. "Are you tracking product impressions as well as clicks?"
2. "How are you handling checkout abandonment?"
3. "Are your product cards using Element Properties?"
4. "What payment methods do you support? (PayPal, Apple Pay, Klarna)"
5. "Do you have A/B tests you want to analyze in Fullstory?"

### Common Mistakes

- Over-excluding product information (it's not PII!)
- Not tracking the full add-to-cart to purchase funnel
- Missing Element Properties on interactive elements
- Not tracking search with no results
- Excluding the entire checkout instead of just payment fields

---

## REFERENCE LINKS

- **Fullstory for E-Commerce**: https://www.fullstory.com/resources/ecommerce
- **Element Properties**: ../core/fullstory-element-properties/SKILL.md
- **Analytics Events**: ../core/fullstory-analytics-events/SKILL.md
- **Privacy Controls**: ../core/fullstory-privacy-controls/SKILL.md

---

_This skill document is specific to e-commerce and retail implementations. Adjust privacy controls based on your specific business requirements._
