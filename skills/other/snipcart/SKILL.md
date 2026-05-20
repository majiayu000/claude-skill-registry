---
name: snipcart
description: >-
  Add e-commerce to any website with Snipcart. Use when a user asks to add
  a shopping cart to a static site, sell products from a JAMstack site, add
  buy buttons to any HTML page, or integrate e-commerce without a backend.
license: Apache-2.0
compatibility: 'Any HTML website, JAMstack, static sites'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: business
  tags:
    - snipcart
    - ecommerce
    - cart
    - jamstack
    - static-site
---

# Snipcart

## Overview

Snipcart adds a full shopping cart to any website with just HTML attributes. No backend needed — it works with static sites, JAMstack, and any HTML page. Handles checkout, payments, shipping, taxes, and inventory.

## Instructions

### Step 1: Add to Any Page

```html
<!-- Add Snipcart scripts to your page -->
<link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.4.1/default/snipcart.css" />
<script async src="https://cdn.snipcart.com/themes/v3.4.1/default/snipcart.js"></script>
<div hidden id="snipcart" data-api-key="YOUR_PUBLIC_API_KEY"></div>

<!-- Product buy button — just HTML attributes -->
<button class="snipcart-add-item"
  data-item-id="tshirt-001"
  data-item-name="Premium T-Shirt"
  data-item-price="29.99"
  data-item-url="/products/tshirt"
  data-item-image="/images/tshirt.jpg"
  data-item-description="100% organic cotton"
  data-item-custom1-name="Size"
  data-item-custom1-options="S|M|L|XL">
  Add to Cart — $29.99
</button>

<!-- Cart summary button -->
<button class="snipcart-checkout">
  Cart (<span class="snipcart-items-count">0</span>)
</button>
```

### Step 2: Astro/Next.js Integration

```astro
---
// components/ProductCard.astro — Product card for static site
const { product } = Astro.props
---
<div class="product-card">
  <img src={product.image} alt={product.name} />
  <h3>{product.name}</h3>
  <p class="price">${product.price}</p>
  <button class="snipcart-add-item"
    data-item-id={product.id}
    data-item-name={product.name}
    data-item-price={product.price}
    data-item-url={`/products/${product.slug}`}
    data-item-image={product.image}>
    Add to Cart
  </button>
</div>
```

### Step 3: JavaScript API

```javascript
// Customize cart behavior with Snipcart JS API
document.addEventListener('snipcart.ready', () => {
  Snipcart.api.cart.items.added((item) => {
    console.log('Item added:', item.name)
    // Track in analytics
  })

  Snipcart.api.cart.confirmed((order) => {
    console.log('Order confirmed:', order.token)
    // Send to CRM, trigger email, etc.
  })
})
```

## Guidelines

- Snipcart takes 2% transaction fee + payment processor fees. No monthly fee.
- Products are validated against your HTML — Snipcart crawls the product URL to verify prices.
- Works with any SSG (Astro, Hugo, 11ty, Gatsby) — perfect for JAMstack e-commerce.
- Supports subscriptions, digital products, and multi-currency.
