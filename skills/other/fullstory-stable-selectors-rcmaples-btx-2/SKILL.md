---
name: fullstory-stable-selectors
version: v2
description: Framework-agnostic guide for implementing stable, semantic selectors in any web application. Solves the dynamic class name problem caused by CSS-in-JS, CSS Modules, and build tools. Includes patterns for React, Angular, Vue, Svelte, Next.js, Astro, and more. Future-proofed for Computer User Agents (CUA) and AI-powered automation tools. Provides TypeScript patterns, naming taxonomies, and enterprise-scale conventions.
related_skills:
  - fullstory-element-properties
  - fullstory-privacy-controls
  - fullstory-getting-started
  - universal-data-scoping-and-decoration
---

# Fullstory Stable Selectors

## Overview

Modern web applications use build tools and CSS methodologies that generate dynamic, unpredictable class names. This creates challenges for:

1. **Fullstory**: Reliable search, defined elements, click maps
2. **Automated Testing**: Stable E2E test selectors
3. **Computer User Agents (CUA)**: AI agents navigating your interface
4. **Accessibility Tools**: Programmatic element identification

**The Solution**: Add stable, semantic `data-*` attributes that describe **what** the element is, not how it's styled.

This skill teaches you how to implement stable selectors in **any framework** without requiring external plugins—and future-proofs your application for AI-powered tooling.

---

## The Problem

```html
<!-- What your code looks like -->
<button className="{styles.primaryButton}">Add to Cart</button>

<!-- What renders in the browser -->
<button class="Button_primaryButton__x7Ks2">Add to Cart</button>
↑ This hash changes every build!
```

**Dynamic class names come from:**

- ❌ CSS Modules (hash suffixes)
- ❌ styled-components / Emotion (random class names)
- ❌ Tailwind CSS (class purging changes the set)
- ❌ Build optimizations (minification, renaming)
- ❌ Component libraries (internal naming conventions)
- ❌ Shadow DOM / Web Components (encapsulated styles)

**Impact:**

| Tool                | Problem                                                                    |
| ------------------- | -------------------------------------------------------------------------- |
| **Fullstory**       | Searches break, defined elements stop matching, click maps lose continuity |
| **E2E Testing**     | Cypress/Playwright tests become brittle                                    |
| **AI Agents (CUA)** | Cannot reliably identify interactive elements                              |
| **Automation**      | Scripts break on every deployment                                          |

---

## Why This Matters for AI Agents (CUA)

Computer User Agents—AI systems that interact with web interfaces—rely on stable, semantic identifiers to understand and navigate your application.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  HOW CUAs "SEE" YOUR INTERFACE                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ❌ BRITTLE (AI struggles):                                             │
│     <button class="sc-3d8f2a btn_primary__xK7n2">Buy Now</button>      │
│                                                                         │
│  ✅ SEMANTIC (AI understands):                                          │
│     <button                                                             │
│       data-component="ProductCard"                                      │
│       data-element="purchase-button"                                    │
│       data-action="add-to-cart"                                        │
│       aria-label="Add to cart"                                          │
│     >Buy Now</button>                                                   │
│                                                                         │
│  The AI can now reliably:                                               │
│  • Find "the purchase button in ProductCard"                           │
│  • Understand the action it will trigger                               │
│  • Maintain stable automation across deployments                        │
└─────────────────────────────────────────────────────────────────────────┘
```

**Stable selectors provide CUAs with:**

- ✅ Consistent element identification across builds
- ✅ Semantic understanding of element purpose
- ✅ Hierarchical context (component → element relationship)
- ✅ Action hints for interaction planning

---

## The Solution

Add stable `data-*` attributes that survive build changes:

```html
<!-- Before: Brittle selector -->
<button class="Button_primaryButton__x7Ks2">Add to Cart</button>

<!-- After: Stable selector -->
<button
  class="Button_primaryButton__x7Ks2"
  data-component="ProductCard"
  data-element="add-to-cart-button"
>
  Add to Cart
</button>
```

**Benefits:**

- ✅ Survives all build changes
- ✅ Semantic and self-documenting
- ✅ Works in ANY framework
- ✅ Enables reliable Fullstory searches
- ✅ Powers defined elements and click maps
- ✅ No external plugins required

---

## Core Concepts

### The Attribute Taxonomy

#### Primary Attributes (Required)

| Attribute        | Purpose                       | Case       | Example                        |
| ---------------- | ----------------------------- | ---------- | ------------------------------ |
| `data-component` | Component boundary identifier | PascalCase | `ProductCard`, `CheckoutForm`  |
| `data-element`   | Element role within component | kebab-case | `add-to-cart`, `price-display` |

#### Extended Attributes (Recommended for CUA/AI)

| Attribute      | Purpose                               | When to Use                     |
| -------------- | ------------------------------------- | ------------------------------- |
| `data-action`  | Describes what happens on interaction | Buttons, links, toggles         |
| `data-state`   | Current state of the element          | Expandable, toggleable elements |
| `data-variant` | Visual or functional variant          | A/B tests, feature flags        |
| `data-testid`  | Unified test/automation identifier    | When aligning with E2E tests    |

#### Development Attributes (Strip in Production)

| Attribute          | Purpose                             |
| ------------------ | ----------------------------------- |
| `data-source-file` | Source file reference for debugging |
| `data-source-line` | Line number for debugging           |

### Attribute Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SEMANTIC HIERARCHY                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  data-component="CheckoutForm"                    ← Component boundary  │
│  │                                                                      │
│  ├── data-element="shipping-section"              ← Structural element  │
│  │   ├── data-element="address-input"             ← Interactive element │
│  │   └── data-element="city-input"                                      │
│  │                                                                      │
│  ├── data-element="payment-section"                                     │
│  │   └── data-element="card-input" + data-action="capture-payment"     │
│  │                                                                      │
│  └── data-element="submit-button"                                       │
│      + data-action="complete-purchase"            ← Action hint for AI  │
│      + data-state="enabled|disabled|loading"      ← Current state       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Aligning with Testing Tools

Many teams already use `data-testid` for Cypress/Playwright. You can unify:

```html
<!-- Option 1: Use both (redundant but safe) -->
<button data-element="add-to-cart" data-testid="add-to-cart-button">Add</button>

<!-- Option 2: Configure test tools to use data-element -->
// cypress.config.js Cypress.SelectorPlayground.defaults({ selectorPriority: ['data-element',
'data-component', 'data-testid', 'id'] }); // playwright.config.js use: { testIdAttribute:
'data-element' }
```

### Integration with ARIA (Accessibility + AI)

Stable selectors complement ARIA attributes—use both:

```html
<button
  data-component="ProductCard"
  data-element="add-to-cart"
  data-action="add-item"
  aria-label="Add Wireless Headphones to cart"
  aria-describedby="price-123"
>
  Add to Cart
</button>
```

| Attribute Type      | Purpose                          | Audience                         |
| ------------------- | -------------------------------- | -------------------------------- |
| `data-*` selectors  | Stable programmatic targeting    | Fullstory, Tests, AI Agents      |
| `aria-*` attributes | Semantic meaning & relationships | Screen readers, AI understanding |
| `role` attribute    | Element type override            | Accessibility, AI categorization |

> **CUA Best Practice**: AI agents use BOTH data-_ attributes for reliable targeting AND aria-_ attributes for understanding element purpose and relationships.

---

## Naming Conventions

### Formal Naming Grammar

```
┌─────────────────────────────────────────────────────────────────────────┐
│  NAMING GRAMMAR                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  data-component: [Namespace.]<Domain><Type>                             │
│                                                                         │
│    Examples:                                                            │
│    • ProductCard         (simple)                                       │
│    • CheckoutPaymentForm (domain + type)                               │
│    • Checkout.PaymentForm (namespaced for micro-frontends)             │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  data-element: <subject>-<descriptor>[-<qualifier>]                     │
│                                                                         │
│    Examples:                                                            │
│    • add-to-cart         (action verb)                                  │
│    • product-image       (subject + type)                              │
│    • shipping-address-input (subject + descriptor + type)              │
│    • nav-item-products   (type + qualifier)                            │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  data-action: <verb>[-<object>]                                         │
│                                                                         │
│    Examples:                                                            │
│    • add-item                                                           │
│    • submit-form                                                        │
│    • toggle-menu                                                        │
│    • expand-details                                                     │
│    • navigate-next                                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Names (`data-component`)

Use **PascalCase** matching your component/class names:

```html
<!-- ✅ GOOD: Matches component names -->
<div data-component="ProductCard">
  <div data-component="CheckoutForm">
    <div data-component="NavigationHeader">
      <div data-component="UserProfileDropdown">
        <!-- ✅ GOOD: Namespaced for micro-frontends -->
        <div data-component="Checkout.PaymentForm">
          <div data-component="Catalog.ProductCard">
            <!-- ❌ BAD: Generic names -->
            <div data-component="Container">
              <div data-component="Wrapper">
                <div data-component="Component">
                  <div data-component="Box"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

### Element Names (`data-element`)

Use **kebab-case** describing the element's purpose:

```html
<!-- ✅ GOOD: Describes purpose -->
<button data-element="add-to-cart">
  <input data-element="email-input" />
  <div data-element="product-image">
    <span data-element="price-display">
      <nav data-element="main-navigation">
        <!-- ✅ GOOD: Qualified names for disambiguation -->
        <input data-element="billing-address-line1" />
        <input data-element="shipping-address-line1" />

        <!-- ❌ BAD: Describes appearance or position -->
        <button data-element="blue-button">
          <button data-element="big-button">
            <button data-element="button-1">
              <button data-element="first-button">
                <div data-element="left-sidebar"></div>
              </button>
            </button>
          </button>
        </button></nav
    ></span>
  </div>
</button>
```

### Action Names (`data-action`)

Use **verb-first kebab-case** describing the outcome:

```html
<!-- ✅ GOOD: Clear action verbs -->
<button data-action="add-item">Add to Cart</button>
<button data-action="submit-order">Complete Purchase</button>
<button data-action="toggle-filter">Show Filters</button>
<a data-action="navigate-category">View All</a>

<!-- ❌ BAD: Nouns or unclear -->
<button data-action="cart">Add to Cart</button>
<button data-action="click-handler">Submit</button>
```

### What to Annotate

**Always annotate:**

- ✅ Buttons and clickable elements
- ✅ Form inputs (text, select, checkbox, etc.)
- ✅ Links and navigation items
- ✅ Cards and list items in repeating content
- ✅ Modals and dialog triggers
- ✅ Tab and accordion controls

**Skip annotation for:**

- ❌ Pure layout wrappers (unless interactive)
- ❌ Styling containers
- ❌ Text-only elements (unless key content)

---

## Implementation by Framework

### React

```jsx
// ProductCard.jsx
function ProductCard({product, onAddToCart}) {
  return (
    <div data-component="ProductCard" data-element="card" className={styles.card}>
      <img src={product.image} alt={product.name} data-element="product-image" />

      <h3 data-element="product-name">{product.name}</h3>

      <span data-element="price">${product.price}</span>

      <button data-element="add-to-cart" onClick={() => onAddToCart(product)}>
        Add to Cart
      </button>
    </div>
  )
}
```

#### React Helper (Optional)

```jsx
// useStableSelector.js
export function useStableSelector(componentName) {
  return {
    root: {
      'data-component': componentName,
    },
    element: (name) => ({
      'data-element': name,
    }),
  }
}

// Usage
function ProductCard({product}) {
  const sel = useStableSelector('ProductCard')

  return (
    <div {...sel.root} {...sel.element('card')}>
      <button {...sel.element('add-to-cart')}>Add to Cart</button>
    </div>
  )
}
```

---

### Angular

```html
<!-- product-card.component.html -->
<article data-component="ProductCard" data-element="card" class="product-card">
  <img [src]="product.image" [alt]="product.name" data-element="product-image" />

  <h3 data-element="product-name">{{ product.name }}</h3>

  <span data-element="price">{{ product.price | currency }}</span>

  <button data-element="add-to-cart" (click)="addToCart()">Add to Cart</button>
</article>
```

#### Angular Directive (Optional)

```typescript
// stable-selector.directive.ts
import { Directive, ElementRef, Input, OnInit } from '@angular/core';

@Directive({
  selector: '[fsComponent], [fsElement]'
})
export class StableSelectorDirective implements OnInit {
  @Input() fsComponent: string;
  @Input() fsElement: string;

  constructor(private el: ElementRef) {}

  ngOnInit() {
    if (this.fsComponent) {
      this.el.nativeElement.setAttribute('data-component', this.fsComponent);
    }
    if (this.fsElement) {
      this.el.nativeElement.setAttribute('data-element', this.fsElement);
    }
  }
}

// Usage in template
<div fsComponent="ProductCard" fsElement="card">
  <button fsElement="add-to-cart">Add to Cart</button>
</div>
```

---

### Vue

```vue
<!-- ProductCard.vue -->
<template>
  <article data-component="ProductCard" data-element="card" class="product-card">
    <img :src="product.image" :alt="product.name" data-element="product-image" />

    <h3 data-element="product-name">{{ product.name }}</h3>

    <span data-element="price">{{ formatPrice(product.price) }}</span>

    <button data-element="add-to-cart" @click="$emit('add-to-cart', product)">Add to Cart</button>
  </article>
</template>

<script setup>
defineProps(['product'])
defineEmits(['add-to-cart'])
</script>
```

#### Vue Directive (Optional)

```javascript
// main.js
app.directive('fs', {
  mounted(el, binding) {
    const {component, element} = binding.value
    if (component) el.setAttribute('data-component', component)
    if (element) el.setAttribute('data-element', element)
  },
})

// Usage in template
;<div v-fs="{ component: 'ProductCard', element: 'card' }">
  <button v-fs="{ element: 'add-to-cart' }">Add to Cart</button>
</div>
```

---

### Svelte

```svelte
<!-- ProductCard.svelte -->
<article
  data-component="ProductCard"
  data-element="card"
  class="product-card"
>
  <img
    src={product.image}
    alt={product.name}
    data-element="product-image"
  />

  <h3 data-element="product-name">{product.name}</h3>

  <span data-element="price">${product.price}</span>

  <button
    data-element="add-to-cart"
    data-action="add-item"
    on:click={() => dispatch('addToCart', product)}
  >
    Add to Cart
  </button>
</article>

<script>
  import { createEventDispatcher } from 'svelte';
  export let product;
  const dispatch = createEventDispatcher();
</script>
```

---

### Next.js (App Router / React Server Components)

Server components work identically—data attributes render to HTML:

```tsx
// app/products/[id]/page.tsx (Server Component)
export default async function ProductPage({params}: {params: {id: string}}) {
  const product = await getProduct(params.id)

  return (
    <main data-component="ProductPage" data-element="page">
      <ProductDetails product={product} />
      <AddToCartButton productId={product.id} />
    </main>
  )
}

// Client component with interactivity
;('use client')
function AddToCartButton({productId}: {productId: string}) {
  const [loading, setLoading] = useState(false)

  return (
    <button
      data-component="AddToCartButton"
      data-element="trigger"
      data-action="add-to-cart"
      data-state={loading ? 'loading' : 'idle'}
      data-product-id={productId}
      onClick={handleClick}
    >
      {loading ? 'Adding...' : 'Add to Cart'}
    </button>
  )
}
```

---

### Astro (Islands Architecture)

```astro
---
// ProductCard.astro
const { product } = Astro.props;
---

<article
  data-component="ProductCard"
  data-element="card"
  data-product-id={product.id}
>
  <img src={product.image} data-element="product-image" />
  <h3 data-element="product-name">{product.name}</h3>

  <!-- Interactive island -->
  <AddToCartButton client:visible productId={product.id} />
</article>
```

---

### Solid.js

```tsx
// ProductCard.tsx
function ProductCard(props: {product: Product}) {
  return (
    <article data-component="ProductCard" data-element="card">
      <img src={props.product.image} data-element="product-image" />
      <h3 data-element="product-name">{props.product.name}</h3>
      <button
        data-element="add-to-cart"
        data-action="add-item"
        onClick={() => addToCart(props.product)}
      >
        Add to Cart
      </button>
    </article>
  )
}
```

---

### TypeScript Type-Safe Selectors

Create compile-time safety for your selector values:

```typescript
// selectors.ts

// Define your component names as a union type
type ComponentName =
  | 'ProductCard'
  | 'CheckoutForm'
  | 'NavigationHeader'
  | 'UserProfile'
  | 'CartDrawer';

// Define element names per component
type ElementName<C extends ComponentName> =
  C extends 'ProductCard' ? 'card' | 'product-image' | 'product-name' | 'price' | 'add-to-cart' :
  C extends 'CheckoutForm' ? 'form' | 'shipping-section' | 'payment-section' | 'submit-button' :
  C extends 'CartDrawer' ? 'drawer' | 'item-list' | 'total' | 'checkout-button' :
  string;

// Type-safe selector builder
interface StableSelectors<C extends ComponentName> {
  'data-component': C;
  'data-element'?: ElementName<C>;
  'data-action'?: string;
  'data-state'?: string;
}

// Factory function
export function createSelectors<C extends ComponentName>(
  component: C
): {
  root: StableSelectors<C>;
  element: (name: ElementName<C>, action?: string) => Partial<StableSelectors<C>>;
} {
  return {
    root: { 'data-component': component },
    element: (name, action) => ({
      'data-element': name,
      ...(action && { 'data-action': action })
    })
  };
}

// Usage
function ProductCard({ product }: Props) {
  const sel = createSelectors('ProductCard');

  return (
    <div {...sel.root} {...sel.element('card')}>
      {/* TypeScript will error if you use 'invalid-element' */}
      <button {...sel.element('add-to-cart', 'add-item')}>
        Add to Cart
      </button>
    </div>
  );
}
```

---

### Vanilla JavaScript / Web Components

```javascript
// product-card.js
class ProductCard extends HTMLElement {
  connectedCallback() {
    const product = JSON.parse(this.getAttribute('product'))

    this.innerHTML = `
      <article data-component="ProductCard" data-element="card">
        <img 
          src="${product.image}" 
          alt="${product.name}"
          data-element="product-image"
        />
        <h3 data-element="product-name">${product.name}</h3>
        <span data-element="price">$${product.price}</span>
        <button data-element="add-to-cart">Add to Cart</button>
      </article>
    `

    this.querySelector('[data-element="add-to-cart"]').addEventListener('click', () =>
      this.handleAddToCart(product),
    )
  }
}

customElements.define('product-card', ProductCard)
```

---

### Server-Side Templates (PHP, Django, Rails, etc.)

```html
<!-- PHP/Blade -->
<article data-component="ProductCard" data-element="card">
  <img src="{{ $product->image }}" data-element="product-image" />
  <h3 data-element="product-name">{{ $product->name }}</h3>
  <button data-element="add-to-cart">Add to Cart</button>
</article>

<!-- Django -->
<article data-component="ProductCard" data-element="card">
  <img src="{{ product.image }}" data-element="product-image" />
  <h3 data-element="product-name">{{ product.name }}</h3>
  <button data-element="add-to-cart">Add to Cart</button>
</article>

<!-- Rails ERB -->
<article data-component="ProductCard" data-element="card">
  <img src="<%= product.image %>" data-element="product-image" />
  <h3 data-element="product-name"><%= product.name %></h3>
  <button data-element="add-to-cart">Add to Cart</button>
</article>
```

---

## Using Stable Selectors in Fullstory

### Searching by Selector

```
# Find all ProductCard components
css selector: [data-component="ProductCard"]

# Find add-to-cart buttons
css selector: [data-element="add-to-cart"]

# Find add-to-cart within ProductCard
css selector: [data-component="ProductCard"] [data-element="add-to-cart"]
```

### Creating Defined Elements

When creating defined elements in Fullstory, use stable selectors:

| Element Name       | Selector                                                         |
| ------------------ | ---------------------------------------------------------------- |
| Add to Cart Button | `[data-element="add-to-cart"]`                                   |
| Product Card       | `[data-component="ProductCard"]`                                 |
| Search Input       | `[data-element="search-input"]`                                  |
| Checkout Submit    | `[data-component="CheckoutForm"] [data-element="submit-button"]` |

### Combining with Element Properties

Stable selectors and Element Properties work together:

```html
<div
  data-component="ProductCard"
  data-element="card"
  data-fs-element="Product Card"
  data-fs-properties-schema='{"product_id":"string","price":"real"}'
  data-product-id="SKU-123"
  data-price="99.99"
>
  <!-- content -->
</div>
```

| Attribute                   | Purpose                              |
| --------------------------- | ------------------------------------ |
| `data-component`            | Stable selector for searching        |
| `data-element`              | Stable selector for specific element |
| `data-fs-element`           | Fullstory defined element name       |
| `data-fs-properties-schema` | Fullstory element properties schema  |

---

## ✅ GOOD Implementation Examples

### Example 1: E-commerce Product Grid

```html
<section data-component="ProductGrid" data-element="grid">
  <h2 data-element="section-title">Featured Products</h2>

  <div data-element="product-list">
    <!-- Each product card -->
    <article data-component="ProductCard" data-element="card">
      <img src="..." data-element="product-image" />
      <h3 data-element="product-name">Wireless Headphones</h3>
      <div data-element="pricing">
        <span data-element="current-price">$149.99</span>
        <span data-element="original-price">$199.99</span>
      </div>
      <div data-element="actions">
        <button data-element="add-to-cart">Add to Cart</button>
        <button data-element="wishlist">♡</button>
      </div>
    </article>

    <!-- More product cards... -->
  </div>

  <nav data-element="pagination">
    <button data-element="prev-page">Previous</button>
    <button data-element="next-page">Next</button>
  </nav>
</section>
```

### Example 2: Multi-Step Form

```html
<form data-component="CheckoutForm" data-element="form">
  <!-- Progress indicator -->
  <nav data-element="step-indicator">
    <span data-element="step" data-step="shipping">Shipping</span>
    <span data-element="step" data-step="payment">Payment</span>
    <span data-element="step" data-step="review">Review</span>
  </nav>

  <!-- Shipping step -->
  <fieldset data-element="shipping-step">
    <div data-element="name-field">
      <label>Full Name</label>
      <input type="text" data-element="name-input" />
    </div>
    <div data-element="address-field">
      <label>Address</label>
      <input type="text" data-element="address-input" />
    </div>
  </fieldset>

  <!-- Payment step (with privacy) -->
  <fieldset data-element="payment-step" class="fs-exclude">
    <div data-element="card-field">
      <label>Card Number</label>
      <input type="text" data-element="card-input" />
    </div>
  </fieldset>

  <!-- Actions -->
  <div data-element="form-actions">
    <button type="button" data-element="back-button">Back</button>
    <button type="submit" data-element="submit-button">Continue</button>
  </div>
</form>
```

### Example 3: Navigation with Dropdowns

```html
<header data-component="SiteHeader" data-element="header">
  <a href="/" data-element="logo">
    <img src="logo.svg" alt="Company" />
  </a>

  <nav data-component="MainNav" data-element="navigation">
    <ul data-element="nav-list">
      <li data-element="nav-item">
        <a href="/products" data-element="nav-link">Products</a>
        <ul data-element="dropdown-menu">
          <li><a href="/products/shoes" data-element="dropdown-item">Shoes</a></li>
          <li><a href="/products/bags" data-element="dropdown-item">Bags</a></li>
        </ul>
      </li>
      <li data-element="nav-item">
        <a href="/about" data-element="nav-link">About</a>
      </li>
    </ul>
  </nav>

  <div data-element="header-actions">
    <button data-element="search-toggle">🔍</button>
    <a href="/cart" data-element="cart-link"> Cart (<span data-element="cart-count">3</span>) </a>
    <button data-element="account-menu">Account</button>
  </div>
</header>
```

---

## ❌ BAD Implementation Examples

### Example 1: Generic Names

```html
<!-- ❌ BAD: Names are too generic -->
<div data-component="Component">
  <img data-element="image" />
  <span data-element="text" />
  <button data-element="button">Click</button>
</div>
```

**Why it's bad:** Every component has "image", "text", "button" - searches return everything.

**✅ CORRECTED:**

```html
<div data-component="ProductCard">
  <img data-element="product-image" />
  <span data-element="product-name" />
  <button data-element="add-to-cart">Click</button>
</div>
```

### Example 2: Position-Based Names

```html
<!-- ❌ BAD: Position-based naming -->
<div data-component="ProductList">
  <div data-element="item-0">First product</div>
  <div data-element="item-1">Second product</div>
  <div data-element="item-2">Third product</div>
</div>
```

**Why it's bad:** If sort order changes, "item-0" is now a different product.

**✅ CORRECTED:**

```html
<div data-component="ProductList">
  <div data-element="product-item" data-product-id="SKU-A">First product</div>
  <div data-element="product-item" data-product-id="SKU-B">Second product</div>
  <div data-element="product-item" data-product-id="SKU-C">Third product</div>
</div>
```

### Example 3: Appearance-Based Names

```html
<!-- ❌ BAD: Named by appearance -->
<button data-element="blue-button">Primary Action</button>
<button data-element="gray-button">Secondary Action</button>
<div data-element="left-sidebar">Navigation</div>
```

**Why it's bad:** If design changes (blue → green, sidebar moves right), names become wrong.

**✅ CORRECTED:**

```html
<button data-element="primary-action">Primary Action</button>
<button data-element="secondary-action">Secondary Action</button>
<div data-element="side-navigation">Navigation</div>
```

---

## Advanced Patterns

### Virtualized Lists / Infinite Scroll

For virtualized content where DOM elements are recycled:

```tsx
// React with react-window or react-virtualized
function VirtualizedProductList({products}) {
  return (
    <div data-component="ProductList" data-element="virtual-container">
      <FixedSizeList height={600} itemCount={products.length} itemSize={120}>
        {({index, style}) => (
          <div
            style={style}
            data-element="product-row"
            data-row-index={index}
            data-product-id={products[index].id} // Stable ID, not position!
          >
            <ProductCard product={products[index]} />
          </div>
        )}
      </FixedSizeList>
    </div>
  )
}
```

**Key Principle**: Use stable business identifiers (`data-product-id`), not positional indices.

---

### Shadow DOM / Web Components

Shadow DOM encapsulates styles but data attributes still work:

```javascript
class ProductCard extends HTMLElement {
  constructor() {
    super()
    this.attachShadow({mode: 'open'})
  }

  connectedCallback() {
    // Set attributes on the host element (light DOM)
    this.setAttribute('data-component', 'ProductCard')
    this.setAttribute('data-element', 'card')

    // Shadow DOM content also gets attributes
    this.shadowRoot.innerHTML = `
      <style>/* encapsulated styles */</style>
      <article>
        <slot name="image"></slot>
        <button data-element="add-to-cart" data-action="add-item">
          <slot name="button-text">Add to Cart</slot>
        </button>
      </article>
    `
  }
}

// For Fullstory to see shadow DOM content, enable deep capture:
// FS.setProperties({ type: 'page', properties: { shadowDomEnabled: true } });
```

**Fullstory Note**: Contact Fullstory support about Shadow DOM capture configuration for your account.

---

### Micro-Frontends

When multiple teams own different parts of the UI, namespace your selectors:

```html
<!-- Team Checkout owns this -->
<div data-component="Checkout.PaymentForm" data-team="checkout" data-element="form">
  <button data-element="submit-payment">Pay</button>
</div>

<!-- Team Catalog owns this -->
<div data-component="Catalog.ProductCard" data-team="catalog" data-element="card">
  <button data-element="add-to-cart">Add</button>
</div>
```

**Namespace Convention**: `{Team}.{Component}` prevents collisions.

---

### A/B Tests and Feature Flags

Track variants for analysis:

```html
<!-- Variant A: Original -->
<button
  data-component="CTAButton"
  data-element="hero-cta"
  data-variant="control"
  data-experiment="homepage-cta-2024"
>
  Get Started
</button>

<!-- Variant B: Test -->
<button
  data-component="CTAButton"
  data-element="hero-cta"
  data-variant="treatment-green"
  data-experiment="homepage-cta-2024"
>
  Start Free Trial
</button>
```

**In Fullstory**: Search by `[data-experiment="homepage-cta-2024"][data-variant="treatment-green"]` to analyze specific variants.

---

### Dynamic/Lazy-Loaded Content

Ensure selectors are present when content loads:

```tsx
// React with Suspense
function ProductDetails({productId}) {
  return (
    <Suspense
      fallback={
        <div data-component="ProductDetails" data-element="skeleton" data-state="loading">
          Loading...
        </div>
      }
    >
      <ProductDetailsContent productId={productId} />
    </Suspense>
  )
}

function ProductDetailsContent({productId}) {
  const product = use(fetchProduct(productId))

  return (
    <div
      data-component="ProductDetails"
      data-element="content"
      data-state="loaded"
      data-product-id={productId}
    >
      {/* content */}
    </div>
  )
}
```

**Note**: The `data-state` attribute helps distinguish loading vs loaded states in Fullstory searches.

---

### Iframes (Cross-Origin Limitations)

For same-origin iframes, selectors work normally. For cross-origin:

```html
<!-- Parent page -->
<iframe
  src="https://checkout.example.com/embed"
  data-component="CheckoutEmbed"
  data-element="iframe"
  title="Checkout"
></iframe>
```

**Limitation**: Fullstory cannot directly capture cross-origin iframe content. The iframe must have its own Fullstory snippet installed.

---

## Best Practices

### 1. Annotate at Development Time

Add annotations as you write components, not as an afterthought:

```jsx
// ✅ Good habit: Add annotations as you code
function ProductCard({product}) {
  return (
    <div data-component="ProductCard">
      <button data-element="add-to-cart">Add</button>
    </div>
  )
}
```

### 2. Document Your Conventions

Create a team style guide:

```markdown
## Stable Selector Conventions

### Component Names

- Use PascalCase: `ProductCard`, `CheckoutForm`
- Match your component file/class name

### Element Names

- Use kebab-case: `add-to-cart`, `search-input`
- Describe purpose, not appearance
- Be specific: `product-name` not `name`

### Required Annotations

- All buttons and links
- All form inputs
- All cards in lists
- Modal and dropdown triggers
```

### 3. Combine with Privacy Controls

```html
<!-- Annotate, but respect privacy -->
<form data-component="PaymentForm">
  <div data-element="card-field" class="fs-exclude">
    <input data-element="card-input" type="text" />
  </div>
  <button data-element="submit-payment">Pay Now</button>
</form>
```

### 4. Use Consistent Depth

Don't over-nest annotations:

```html
<!-- ✅ GOOD: Flat, specific selectors -->
<div data-component="ProductCard">
  <button data-element="add-to-cart">Add</button>
</div>

<!-- ❌ BAD: Deep nesting (unnecessary) -->
<div data-component="App">
  <div data-component="MainContent">
    <div data-component="ProductSection">
      <div data-component="ProductCard">
        <button data-element="add-to-cart">Add</button>
      </div>
    </div>
  </div>
</div>
```

---

## Troubleshooting

### Selectors Not Working in Fullstory

**Check in browser DevTools:**

1. Inspect the element
2. Verify `data-component` and `data-element` attributes exist
3. Check for typos in attribute names

**Common issues:**

- Framework stripping data attributes in production
- SSR/hydration mismatch
- Conditional rendering removing the element

### Too Many Search Results

**Problem:** Searching `[data-element="button"]` returns hundreds of results

**Solution:** Be more specific:

```
[data-component="ProductCard"] [data-element="add-to-cart"]
```

### Attributes Stripped in Production

Check your build tool configuration:

```javascript
// webpack.config.js - DON'T strip data-* attributes
optimization: {
  minimizer: [
    new HtmlWebpackPlugin({
      minify: {
        // Keep data-* attributes
        removeDataAttributes: false,
      },
    }),
  ]
}
```

---

## KEY TAKEAWAYS FOR AGENT

When helping developers implement stable selectors:

### Core Principles

1. **Framework-agnostic solution**: Works in React, Angular, Vue, Svelte, Next.js, Astro, vanilla JS, server-side templates
2. **Primary attributes**: `data-component` (PascalCase) and `data-element` (kebab-case)
3. **Extended attributes for AI/CUA**: `data-action`, `data-state`, `data-variant`
4. **Name by purpose, not appearance**: "add-to-cart" not "blue-button"
5. **Annotate interactive elements**: Buttons, inputs, links, cards in lists
6. **Combine with Element Properties**: Stable selectors for search, Element Properties for analytics data
7. **Combine with ARIA**: Use both data-_ and aria-_ for maximum AI/accessibility compatibility
8. **No plugins required**: Manual annotation works everywhere

### CUA/AI Agent Considerations

- **`data-action`**: Helps AI understand what interaction will do ("add-item", "submit-form", "toggle-menu")
- **`data-state`**: Helps AI understand current element state ("loading", "disabled", "expanded")
- **ARIA integration**: Ensure `aria-label` provides human-readable context alongside data-\* targeting
- **Consistent naming**: AI agents learn patterns—be consistent across your codebase

### Questions to Ask Developers

1. "What framework are you using?" (React, Vue, Angular, Next.js, Astro, etc.)
2. "Are your class names dynamic?" (CSS Modules, styled-components, Tailwind)
3. "What elements do you need to reliably search for in Fullstory?"
4. "Do you have a component naming convention already?"
5. "Are you using E2E testing tools?" (May want to align with data-testid)
6. "Do you use micro-frontends or multiple teams?" (Need namespace strategy)
7. "Is AI/automation tooling on your roadmap?" (Add extended attributes now)

### Implementation Checklist

```markdown
Phase 1: Core Implementation
□ Identify interactive elements that need tracking
□ Add data-component to component root elements  
□ Add data-element to buttons, inputs, links, cards
□ Use specific, purpose-based names (not appearance/position)
□ Test selectors in browser DevTools
□ Verify attributes survive production build
□ Create defined elements in Fullstory using data-\* selectors

Phase 2: AI/CUA Readiness (Recommended)
□ Add data-action to buttons and interactive elements
□ Add data-state for elements with multiple states
□ Ensure ARIA attributes complement data-\* selectors
□ Document naming conventions for team consistency

Phase 3: Enterprise Scale (If Applicable)
□ Implement TypeScript type-safe selectors
□ Add namespace prefixes for micro-frontends
□ Add data-variant for A/B test tracking
□ Configure E2E tools to use data-element
```

### Selector Evolution Strategy

When you need to change selectors:

1. **Add new selector alongside old** (don't remove immediately)
2. **Update Fullstory defined elements** to use new selector
3. **Verify data continuity** in Fullstory dashboards
4. **Remove old selector** after confirming migration

---

## REFERENCE LINKS

### Fullstory Documentation

- **CSS Selectors in Search**: https://help.fullstory.com/hc/en-us/articles/360020623294
- **Defined Elements**: https://help.fullstory.com/hc/en-us/articles/360020828113
- **Element Properties Guide**: ../core/fullstory-element-properties/SKILL.md

### Testing Tool Integration

- **Cypress Best Practices (Selecting Elements)**: https://docs.cypress.io/guides/references/best-practices#Selecting-Elements
- **Playwright Locators**: https://playwright.dev/docs/locators
- **Testing Library Queries**: https://testing-library.com/docs/queries/about

### Accessibility & AI

- **WAI-ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/
- **MDN: Using Data Attributes**: https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes

### Historical Context

These skills consolidate and extend patterns from:

- `fullstorydev/eslint-plugin-annotate-react` (React-specific)
- `fullstorydev/fullstory-babel-plugin-annotate-react` (Build-time injection)

The manual approach in this skill is more flexible and works across all frameworks.

---

_This skill provides a universal, future-proof pattern for stable selectors that works in any framework. Optimized for Fullstory analytics, E2E testing, and AI-powered Computer User Agents. No external plugins required._
