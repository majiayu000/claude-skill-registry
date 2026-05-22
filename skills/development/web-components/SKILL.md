---
name: web-components-architecture
description: Build web components using Custom Elements v1 API with Declarative Shadow DOM, attribute-driven state, handleEvent pattern, and zero DOM selection. Use when creating custom elements, extending built-in HTML elements, or implementing component-based architecture. NO querySelector, NO innerHTML, NO external libraries - pure web platform APIs only.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Web Components Architecture

## Core Principles

This skill enforces a strict architectural pattern for web components:

1. **Zero DOM Selection**: NEVER use `querySelector`, `querySelectorAll`, or `getElementById`
2. **Attribute-Driven State**: All state flows through HTML attributes
3. **Event Delegation on `this`**: Use `this.addEventListener` and the `handleEvent` pattern
4. **No External Dependencies**: Use only standard Web Platform APIs
5. **Declarative Shadow DOM**: Use `<template shadowrootmode="open">` for instant rendering
6. **Progressive Enhancement**: Components work (degraded) even if JavaScript fails
7. **Customized Built-ins Over Autonomous**: Extend native elements when possible to preserve accessibility

## Relationship with JavaScript Best Practices

This skill defines the **architectural pattern** for building web components. When implementing components, combine this skill with `javascript-pragmatic-rules` for production-quality code:

**This skill provides the WHAT (component architecture):**
- Component structure (extends HTMLElement)
- Lifecycle callbacks (connectedCallback, disconnectedCallback)
- State management (attribute-driven)
- Event patterns (handleEvent, CustomEvent)
- Shadow DOM and encapsulation

**`javascript-pragmatic-rules` provides the HOW (implementation quality):**
- Async operation handling (timeouts, cancellation)
- Resource cleanup patterns
- Error handling strategies
- Memory leak prevention
- Performance optimization

**Example:** Building an `<async-button>` component:

```javascript
// Architecture from web-components-architecture skill
class AsyncButton extends HTMLButtonElement {
  #controller = null; // Private field for cleanup

  connectedCallback() {
    this.addEventListener('click', this);
  }

  // Using handleEvent pattern from web-components-architecture
  async handleEvent(e) {
    if (e.type === 'click') {
      // Rule 2 from javascript-pragmatic-rules: Timeout async operations
      this.#controller = new AbortController();
      const timeoutId = setTimeout(() => this.#controller.abort(), 5_000);

      try {
        const response = await fetch(this.getAttribute('data-url'), {
          signal: this.#controller.signal
        });
        clearTimeout(timeoutId);
        // Handle response...
      } catch (error) {
        // Rule 1 from javascript-pragmatic-rules: Handle rejections
        if (error.name === 'AbortError') {
          console.warn('Request timed out');
        } else {
          throw new Error('Request failed', { cause: error });
        }
      }
    }
  }

  // Rule 4 from javascript-pragmatic-rules: Clean up resources
  disconnectedCallback() {
    this.removeEventListener('click', this);
    if (this.#controller) this.#controller.abort();
  }
}
```

**Key Integration Points:**
- Use this skill's `connectedCallback` with `javascript-pragmatic-rules` Rule 4 (cleanup)
- Use this skill's `handleEvent` with `javascript-pragmatic-rules` Rules 1-2 (async safety)
- Use this skill's attribute patterns with `javascript-pragmatic-rules` Rule 5 (immutability)

See `javascript-pragmatic-rules` skill for comprehensive JavaScript best practices.

---

## Component Types

### 1. Customized Built-in Elements (PREFERRED)

Extend native HTML elements to preserve built-in accessibility and behavior.

```javascript
class AsyncAction extends HTMLButtonElement {
  connectedCallback() {
    // Principle: Event Delegation on Self
    this.addEventListener('click', this);
  }

  // Principle: HandleEvent pattern avoids binding 'this'
  async handleEvent(e) {
    if (e.type === 'click') {
      // Principle: Attribute-Driven State (Input)
      this.setAttribute('aria-busy', 'true');
      this.disabled = true;

      // Simulate async work
      await new Promise((resolve) => setTimeout(resolve, 1_500));

      this.removeAttribute('aria-busy');
      this.disabled = false;

      // Principle: Events are the ONLY output
      this.dispatchEvent(new CustomEvent('action-complete', {
        bubbles: true,
        detail: { originalEvent: e }
      }));
    }
  }

  disconnectedCallback() {
    this.removeEventListener('click', this);
  }
}

// Register with { extends: 'button' }
customElements.define('async-action', AsyncAction, { extends: 'button' });
```

**Usage in HTML:**
```html
<button is="async-action" aria-label="Add to cart">
  Add to Cart
</button>
```

### 2. Autonomous Custom Elements

Use for layout containers and composite components.

```javascript
class ProductCard extends HTMLElement {
  // Purely declarative - no logic needed if using DSD
}

customElements.define('product-card', ProductCard);
```

## Declarative Shadow DOM

Use `<template shadowrootmode="open">` for instant rendering without JavaScript.

```html
<product-card>
  <template shadowrootmode="open">
    <style>
      :host {
        display: block;
        max-width: 300px;
      }

      /* Attribute-Driven Styling */
      button[aria-busy="true"] {
        opacity: 0.7;
        cursor: wait;
      }

      .card {
        background: var(--card-bg, white);
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }

      .footer {
        margin-top: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
    </style>

    <article class="card" part="container">
      <slot name="header"></slot>
      <slot></slot>

      <div class="footer">
        <slot name="price">Free</slot>

        <button is="async-action" part="action-btn">
          Add to Cart
        </button>
      </div>
    </article>
  </template>

  <h3 slot="header">Product Title</h3>
  <p>Product description goes here.</p>
  <strong slot="price">$450.00</strong>
</product-card>
```

## Attribute-Driven State Pattern

State flows IN via attributes and OUT via events.

### Input: Reading Attributes

```javascript
class DataDisplay extends HTMLElement {
  connectedCallback() {
    // Read initial state from attributes
    const apiUrl = this.getAttribute('data-url');
    const refreshInterval = this.getAttribute('refresh-interval') || 5_000;

    this.setAttribute('status', 'loading');
    this.loadData(apiUrl);
  }

  async loadData(url) {
    try {
      const response = await fetch(url);
      const data = await response.json();

      // State change via attribute
      this.setAttribute('status', 'loaded');
      this.setAttribute('data-count', data.items.length);

      // Output via event
      this.dispatchEvent(new CustomEvent('data-loaded', {
        bubbles: true,
        detail: { data }
      }));
    } catch (error) {
      this.setAttribute('status', 'error');
      this.dispatchEvent(new CustomEvent('data-error', {
        bubbles: true,
        detail: { error: error.message }
      }));
    }
  }

  // Observe attribute changes
  static get observedAttributes() {
    return ['data-url', 'refresh-interval'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue === newValue) return;

    if (name === 'data-url' && newValue) {
      this.loadData(newValue);
    }
  }
}
```

### Output: Events Only

```javascript
// CORRECT: Dispatch events for output
this.dispatchEvent(new CustomEvent('value-changed', {
  bubbles: true,
  composed: true, // Cross shadow DOM boundaries
  detail: { value: newValue }
}));

// WRONG: Never modify external DOM
// document.querySelector('.result').textContent = value; // ❌ FORBIDDEN
```

## HandleEvent Pattern

Use the `handleEvent` interface to avoid `.bind(this)` and maintain clean memory management.

```javascript
class MultiEventHandler extends HTMLElement {
  connectedCallback() {
    // Single listener for multiple event types
    this.addEventListener('click', this);
    this.addEventListener('keydown', this);
    this.addEventListener('focus', this);
  }

  handleEvent(e) {
    // Route by event type
    switch(e.type) {
      case 'click':
        this.handleClick(e);
        break;
      case 'keydown':
        this.handleKeydown(e);
        break;
      case 'focus':
        this.handleFocus(e);
        break;
    }
  }

  handleClick(e) {
    this.setAttribute('last-interaction', 'click');
  }

  handleKeydown(e) {
    if (e.key === 'Enter' || e.key === ' ') {
      this.setAttribute('last-interaction', 'keyboard');
    }
  }

  handleFocus(e) {
    this.setAttribute('focused', 'true');
  }

  disconnectedCallback() {
    this.removeEventListener('click', this);
    this.removeEventListener('keydown', this);
    this.removeEventListener('focus', this);
  }
}
```

## Styling API

### CSS Custom Properties (Theming)

```css
/* Consumer defines theme */
:root {
  --primary-color: #6200ea;
  --bg-color: #ffffff;
  --spacing: 1rem;
}

product-card {
  --card-bg: var(--bg-color);
  --card-padding: var(--spacing);
}
```

### ::part() Pseudo-element

```html
<template shadowrootmode="open">
  <style>
    .internal-element {
      /* internal styles */
    }
  </style>

  <!-- Expose parts for external styling -->
  <div class="internal-element" part="container">
    <button part="action-btn">Click me</button>
  </div>
</template>
```

```css
/* External styling via ::part() */
product-card::part(container) {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

product-card::part(action-btn) {
  background-color: var(--primary-color);
  color: white;
}
```

### :host and :host-context

```css
<style>
  /* Style the host element */
  :host {
    display: block;
    font-family: system-ui, sans-serif;
  }

  /* State-based styling */
  :host([disabled]) {
    opacity: 0.5;
    pointer-events: none;
  }

  /* Context-based styling */
  :host-context(.dark-mode) {
    background: #1a1a1a;
    color: #ffffff;
  }
</style>
```

## Lifecycle Callbacks

```javascript
class LifecycleExample extends HTMLElement {
  constructor() {
    super();
    // ONLY: Initialize instance variables
    // DO NOT: Access attributes, children, or DOM
  }

  connectedCallback() {
    // Element added to DOM
    // DO: Set up event listeners, start timers, fetch data
    this.addEventListener('click', this);

    const initialValue = this.getAttribute('value');
    if (initialValue) {
      this.initialize(initialValue);
    }
  }

  disconnectedCallback() {
    // Element removed from DOM
    // DO: Clean up event listeners, timers, connections
    this.removeEventListener('click', this);

    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  attributeChangedCallback(name, oldValue, newValue) {
    // Observed attribute changed
    if (oldValue === newValue) return;

    switch(name) {
      case 'value':
        this.updateValue(newValue);
        break;
      case 'disabled':
        this.updateDisabled(newValue !== null);
        break;
    }
  }

  adoptedCallback() {
    // Element moved to new document
    // Rarely needed - usually for iframes
  }

  static get observedAttributes() {
    return ['value', 'disabled', 'theme'];
  }
}
```

## Form Integration with ElementInternals

Use ElementInternals API for form-associated custom elements.

```javascript
class CustomInput extends HTMLElement {
  static formAssociated = true;

  constructor() {
    super();
    this.internals = this.attachInternals();
  }

  connectedCallback() {
    this.addEventListener('input', this);
    this.updateValue(this.getAttribute('value') || '');
  }

  handleEvent(e) {
    if (e.type === 'input') {
      const value = e.target.value;
      this.updateValue(value);
    }
  }

  updateValue(value) {
    // Update form value
    this.internals.setFormValue(value);

    // Validate
    if (!value) {
      this.internals.setValidity(
        { valueMissing: true },
        'This field is required'
      );
    } else {
      this.internals.setValidity({});
    }

    // Emit event
    this.dispatchEvent(new CustomEvent('value-changed', {
      bubbles: true,
      detail: { value }
    }));
  }

  // Form lifecycle callbacks
  formResetCallback() {
    this.updateValue('');
  }

  formDisabledCallback(disabled) {
    this.setAttribute('aria-disabled', disabled);
  }
}

customElements.define('custom-input', CustomInput);
```

## Accessibility Patterns

### ARIA Attributes

```javascript
class AccessibleToggle extends HTMLButtonElement {
  connectedCallback() {
    this.addEventListener('click', this);

    // Set initial ARIA state
    if (!this.hasAttribute('aria-pressed')) {
      this.setAttribute('aria-pressed', 'false');
    }
  }

  handleEvent(e) {
    if (e.type === 'click') {
      const isPressed = this.getAttribute('aria-pressed') === 'true';
      this.setAttribute('aria-pressed', String(!isPressed));

      this.dispatchEvent(new CustomEvent('toggle', {
        bubbles: true,
        detail: { pressed: !isPressed }
      }));
    }
  }
}

customElements.define('accessible-toggle', AccessibleToggle, { extends: 'button' });
```

### Keyboard Navigation

```javascript
class KeyboardNav extends HTMLElement {
  connectedCallback() {
    if (!this.hasAttribute('tabindex')) {
      this.setAttribute('tabindex', '0');
    }

    this.addEventListener('keydown', this);
  }

  handleEvent(e) {
    if (e.type === 'keydown') {
      switch(e.key) {
        case 'Enter':
        case ' ':
          e.preventDefault();
          this.activate();
          break;
        case 'Escape':
          this.deactivate();
          break;
      }
    }
  }

  activate() {
    this.setAttribute('active', 'true');
    this.dispatchEvent(new CustomEvent('activated', { bubbles: true }));
  }

  deactivate() {
    this.removeAttribute('active');
    this.dispatchEvent(new CustomEvent('deactivated', { bubbles: true }));
  }
}
```

## Complete Example: Async Action Button

```javascript
/* async-action.js */
class AsyncAction extends HTMLButtonElement {
  connectedCallback() {
    this.addEventListener('click', this);
  }

  async handleEvent(e) {
    if (e.type === 'click') {
      // Prevent double-clicks
      if (this.getAttribute('aria-busy') === 'true') {
        return;
      }

      // Set loading state
      this.setAttribute('aria-busy', 'true');
      this.disabled = true;

      const originalText = this.textContent;
      const loadingText = this.getAttribute('loading-text') || 'Loading...';
      this.textContent = loadingText;

      try {
        // Dispatch event for external handler
        const actionEvent = new CustomEvent('async-action', {
          bubbles: true,
          cancelable: true,
          detail: {
            button: this,
            originalEvent: e
          }
        });

        const shouldContinue = this.dispatchEvent(actionEvent);

        if (shouldContinue) {
          // Simulate async work (in real usage, parent handles this)
          await new Promise((resolve) => setTimeout(resolve, 1_500));

          // Success state
          this.setAttribute('aria-busy', 'false');
          this.removeAttribute('aria-busy');

          this.dispatchEvent(new CustomEvent('action-complete', {
            bubbles: true,
            detail: { success: true }
          }));
        }
      } catch (error) {
        // Error state
        this.setAttribute('aria-busy', 'false');
        this.removeAttribute('aria-busy');

        this.dispatchEvent(new CustomEvent('action-error', {
          bubbles: true,
          detail: { error: error.message }
        }));
      } finally {
        // Reset state
        this.textContent = originalText;
        this.disabled = false;
      }
    }
  }

  disconnectedCallback() {
    this.removeEventListener('click', this);
  }
}

customElements.define('async-action', AsyncAction, { extends: 'button' });
```

**HTML Usage:**
```html
<button
  is="async-action"
  loading-text="Saving..."
  aria-label="Save changes">
  Save
</button>

<script>
  document.addEventListener('async-action', async (e) => {
    // Handle the action
    const response = await fetch('/api/save', {
      method: 'POST',
      body: JSON.stringify({ data: 'example' })
    });

    if (!response.ok) {
      throw new Error('Save failed');
    }
  });
</script>
```

## Anti-Patterns (NEVER DO THIS)

### ❌ DOM Selection
```javascript
// WRONG
connectedCallback() {
  const button = this.querySelector('button'); // ❌
  button.addEventListener('click', ...);
}
```

### ❌ Direct DOM Manipulation of External Elements
```javascript
// WRONG
handleClick() {
  document.getElementById('result').textContent = 'Done'; // ❌
}
```

### ❌ innerHTML for Dynamic Content
```javascript
// WRONG
updateContent(data) {
  this.innerHTML = `<div>${data}</div>`; // ❌
}
```

### ❌ Imperative Shadow DOM Creation
```javascript
// WRONG (use Declarative Shadow DOM instead)
constructor() {
  super();
  this.attachShadow({ mode: 'open' }); // ❌
  this.shadowRoot.innerHTML = '<div>...</div>'; // ❌
}
```

### ❌ Global State
```javascript
// WRONG
let globalState = {}; // ❌

class MyComponent extends HTMLElement {
  connectedCallback() {
    globalState.value = 'bad'; // ❌
  }
}
```

## Testing Pattern

```javascript
// test.html
<!DOCTYPE html>
<html>
<head>
  <script type="module" src="./async-action.js"></script>
</head>
<body>
  <button is="async-action" id="test-btn">Test</button>

  <script type="module">
    const btn = document.getElementById('test-btn');

    // Test attribute-driven state
    btn.addEventListener('action-complete', (e) => {
      console.log('✓ Action completed', e.detail);
    });

    // Programmatically trigger
    btn.click();

    // Verify state
    console.assert(
      btn.getAttribute('aria-busy') === 'true',
      'Should be busy during action'
    );
  </script>
</body>
</html>
```

## Progressive Enhancement

Components should degrade gracefully without JavaScript:

```html
<!-- Works as regular button if JS fails -->
<button is="async-action" formaction="/submit" formmethod="post">
  Submit Form
</button>

<!-- Works as regular link if JS fails -->
<a is="spa-link" href="/page">
  Navigate
</a>
```

## Integrating with Utopia Fluid Scales

When using this skill alongside Utopia skills (`utopia-fluid-scales`, `utopia-grid-layout`, `utopia-container-queries`), follow these patterns for CSS Custom Properties and shared styles.

### CSS Custom Properties Pierce Shadow Boundaries

Utopia tokens defined on `:root` automatically work inside shadow DOM via `var()`:

```css
/* Inside shadow DOM - these just work */
:host {
  display: block;
  container-type: inline-size; /* Required for cqi units */
}

.card {
  padding: var(--space-m);           /* Utopia spacing */
  font-size: var(--step-0);          /* Utopia typography */
  gap: var(--grid-gutter);           /* Utopia grid */
}

.title {
  font-size: var(--step-2);
  font-weight: 700;
}

.body {
  font-size: var(--step--1);
  color: var(--color-muted, #6b7280);
}
```

### Sharing Utility Classes via Constructable Stylesheets

Shadow DOM encapsulates styles, so global utility classes (`.u-stack`, `.u-grid`, `.u-cluster`) don't penetrate. Use **Constructable Stylesheets** with `adoptedStyleSheets` to share utilities without duplication:

```javascript
/* js/styles/shared-styles.js */

// Create stylesheets once - shared across all components
export const utopiaGridStyles = new CSSStyleSheet();
utopiaGridStyles.replaceSync(`
  .u-container {
    max-width: var(--grid-max-width, 77.5rem);
    margin-inline: auto;
    padding-inline: var(--grid-gutter, var(--space-s-l));
  }

  .u-grid {
    display: grid;
    gap: var(--grid-gutter, var(--space-s-l));
  }

  .u-grid-auto {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
    gap: var(--grid-gutter, var(--space-s-l));
  }

  .u-stack {
    display: flex;
    flex-direction: column;
    gap: var(--space-s);
  }

  .u-cluster {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-s);
    align-items: center;
  }
`);

export const utopiaTypeStyles = new CSSStyleSheet();
utopiaTypeStyles.replaceSync(`
  .u-step-5 { font-size: var(--step-5); }
  .u-step-4 { font-size: var(--step-4); }
  .u-step-3 { font-size: var(--step-3); }
  .u-step-2 { font-size: var(--step-2); }
  .u-step-1 { font-size: var(--step-1); }
  .u-step-0 { font-size: var(--step-0); }
  .u-step--1 { font-size: var(--step--1); }
  .u-step--2 { font-size: var(--step--2); }
`);

// Helper to create component-specific stylesheets
export function createStyleSheet(css) {
  const sheet = new CSSStyleSheet();
  sheet.replaceSync(css);
  return sheet;
}
```

### Component Using Shared Styles

**Note:** When using `adoptedStyleSheets`, imperative shadow DOM creation is acceptable. This is the exception to the "no imperative shadow DOM" rule.

```javascript
import { utopiaGridStyles, utopiaTypeStyles, createStyleSheet } from '../styles/shared-styles.js';

const componentStyles = createStyleSheet(`
  :host {
    display: block;
    container-type: inline-size;
  }

  /* Use :host([attr]) for attribute-based styling */
  :host([variant="primary"]) {
    --card-accent: var(--color-primary, #6366f1);
  }

  :host([variant="secondary"]) {
    --card-accent: var(--color-secondary, #8b5cf6);
  }

  .card {
    background: var(--card-bg, white);
    border: 2px solid var(--card-accent, #e5e7eb);
    border-radius: var(--space-xs);
    padding: var(--space-m);
  }

  .title {
    font-size: var(--step-1);
    font-weight: 700;
  }
`);

class FeatureCard extends HTMLElement {
  static get observedAttributes() {
    return ['title', 'variant'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Adopt shared + component styles (no duplication!)
    this.shadowRoot.adoptedStyleSheets = [
      utopiaGridStyles,
      utopiaTypeStyles,
      componentStyles
    ];

    // Now utility classes work inside shadow DOM
    this.shadowRoot.innerHTML = `
      <article class="card u-stack" part="container">
        <h3 class="title u-step-1" part="title"></h3>
        <slot></slot>
      </article>
    `;

    this._titleEl = this.shadowRoot.querySelector('.title');
  }

  connectedCallback() {
    this.addEventListener('click', this);
    this.render();
  }

  disconnectedCallback() {
    this.removeEventListener('click', this);
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal === newVal) return;
    if (this.isConnected) this.render();
  }

  handleEvent(e) {
    if (e.type === 'click') {
      this.dispatchEvent(new CustomEvent('card-selected', {
        bubbles: true,
        composed: true,
        detail: { title: this.getAttribute('title') }
      }));
    }
  }

  render() {
    this._titleEl.textContent = this.getAttribute('title') || '';
  }
}

customElements.define('feature-card', FeatureCard);
```

### Key Patterns for Utopia Integration

1. **Always set `container-type: inline-size` on `:host`** - Required for `cqi` units in Utopia fluid scales

2. **Use `var()` for all Utopia tokens** - They pierce shadow DOM automatically:
   - Typography: `var(--step-0)`, `var(--step-1)`, `var(--step--1)`
   - Spacing: `var(--space-xs)`, `var(--space-m)`, `var(--space-l)`
   - Grid: `var(--grid-gutter)`, `var(--grid-max-width)`

3. **Use `:host([attribute])` for variant styling** - Attribute-driven state maps directly to CSS:
   ```css
   :host([size="small"]) { --internal-padding: var(--space-xs); }
   :host([size="large"]) { --internal-padding: var(--space-l); }
   ```

4. **Create component-scoped custom properties** - Map Utopia tokens to semantic names:
   ```css
   :host {
     --card-padding: var(--space-m);
     --card-gap: var(--space-s);
     --title-size: var(--step-1);
   }
   ```

5. **Share CSSStyleSheet objects, not CSS strings** - `adoptedStyleSheets` references the same object across all components

### Container Query Checklist

When using Utopia's `cqi`-based fluid scales inside shadow DOM:

- [ ] `:host` has `container-type: inline-size`
- [ ] Parent elements in light DOM have `container-type: inline-size` where needed
- [ ] Typography uses `var(--step-*)` tokens
- [ ] Spacing uses `var(--space-*)` tokens
- [ ] Component is tested at various container widths

## FOUC Prevention (Flash of Unstyled Content)

Custom elements are "undefined" until JavaScript loads and registers them via `customElements.define()`. During this window, browsers render raw content without shadow DOM styles, causing a visible flash (FOUC) and layout shift (CLS).

### The Problem

```html
<!-- Before JavaScript loads, this shows raw slot content -->
<site-nav>
  <span slot="brand">My Site</span>
  <a slot="menu" href="/">Home</a>
</site-nav>
```

Without FOUC prevention:
1. HTML parses, custom element renders as inline element with raw slot content
2. JavaScript loads and defines the component
3. Shadow DOM attaches, styles apply, component "snaps" into place
4. Users see an ugly flash and layout shift

### Solution 1: CSS `:not(:defined)` Selector (Required)

The `:defined` pseudo-class targets elements that have been registered via `customElements.define()`. Use `:not(:defined)` to hide or style elements before definition:

```css
/* In global CSS (e.g., accessibility.css) */

/* Hide custom elements until JavaScript defines them */
site-nav:not(:defined),
nav-link-item:not(:defined) {
  opacity: 0;
}

/* Reserve layout space to prevent CLS */
site-nav:not(:defined) {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-sticky, 100);
  min-height: calc(var(--nav-height, 56px) + var(--space-s) * 2);
  background: var(--theme-surface);
  border-block-end: 1px solid var(--theme-outline);
}

/* Instant visibility once defined */
site-nav:defined {
  opacity: 1;
}
```

**Why `opacity: 0` instead of `display: none`?**
- `opacity: 0` preserves layout space, preventing CLS
- `display: none` causes layout shift when element appears
- `visibility: hidden` also works but can cause focus issues

### Solution 2: Module Preload (Recommended)

Preload critical above-the-fold components to reduce time-to-definition:

```html
<head>
  <!-- Styles first -->
  <link rel="stylesheet" href="/css/styles/index.css">

  <!-- Preload critical component scripts -->
  <link rel="modulepreload" href="/js/components/site-nav.js">
  <link rel="modulepreload" href="/js/components/nav-link-item.js">
  <link rel="modulepreload" href="/js/components/page-transition.js">

  <!-- Import maps -->
  <script type="importmap">...</script>
</head>
```

**Benefits:**
- Browser starts downloading modules in parallel with HTML parsing
- Reduces time between HTML render and component definition
- Works with ES modules (`type="module"` scripts)

### Solution 3: Declarative Shadow DOM (Best)

For server-rendered or static sites, use Declarative Shadow DOM for instant styling:

```html
<site-nav>
  <template shadowrootmode="open">
    <style>
      :host {
        display: block;
        position: fixed;
        top: 0;
        /* ... all component styles inline ... */
      }
    </style>
    <nav>
      <slot name="brand"></slot>
      <slot name="menu"></slot>
    </nav>
  </template>

  <!-- Light DOM content -->
  <span slot="brand">My Site</span>
  <a slot="menu" href="/">Home</a>
</site-nav>
```

**Benefits:**
- Styles apply immediately during HTML parsing
- No JavaScript required for initial render
- Best possible CLS score
- JavaScript enhances (adds interactivity) but doesn't enable styling

### Implementation Checklist

For every custom element in your application:

- [ ] Add `:not(:defined)` CSS rule in global stylesheet
- [ ] Reserve layout space for fixed/positioned elements
- [ ] Add `modulepreload` for above-the-fold components
- [ ] Consider Declarative Shadow DOM for critical-path components
- [ ] Test with network throttling to verify no FOUC
- [ ] Measure CLS in Lighthouse/PageSpeed Insights

### Project Pattern

This project handles FOUC in `css/styles/accessibility.css`:

```css
/* Navigation - reserve space and hide content */
site-nav:not(:defined) {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-sticky, 100);
  min-height: calc(var(--nav-height, 56px) + var(--space-s, 0.75rem) * 2);
  background: var(--theme-surface, #1f1b15);
  border-block-end: 1px solid var(--theme-outline, #5c4d3d);
  opacity: 0;
}

/* Cards and grids - hide until ready */
filterable-grid:not(:defined),
word-card:not(:defined) {
  opacity: 0;
}
```

And in HTML `<head>`:

```html
<!-- Modulepreload critical components to prevent FOUC -->
<link rel="modulepreload" href="/js/components/site-nav.js">
<link rel="modulepreload" href="/js/components/nav-link-item.js">
<link rel="modulepreload" href="/js/components/page-transition.js">
```

### Anti-Pattern: Generic Wildcard

**Avoid** hiding all undefined elements with a wildcard:

```css
/* DON'T DO THIS - breaks progressive enhancement */
*:not(:defined) {
  display: none;
}
```

This breaks elements that should be visible during progressive enhancement (forms, links, etc.). Instead, explicitly list the components that need FOUC prevention.

## When to Use This Pattern

- Building reusable UI components
- Creating design systems
- Server-side rendering (SSR) with hydration
- Progressive web apps (PWAs)
- Micro-frontends
- Accessibility-first applications

## When NOT to Use

- Simple static websites (use plain HTML)
- Heavy data visualization (consider Canvas/WebGL)
- Applications requiring IE11 support (no polyfills allowed)

## Instructions for Implementation

When implementing web components:

1. **Choose Element Type**: Prefer customized built-ins over autonomous elements
2. **Define State Contract**: Document all attributes and events
3. **Use HandleEvent**: Implement `handleEvent()` for event delegation
4. **Avoid DOM Selection**: NEVER use `querySelector` or similar methods
5. **Use DSD**: Implement Declarative Shadow DOM for instant rendering
6. **Expose Styling API**: Use CSS custom properties and `::part()`
7. **Implement Accessibility**: Add ARIA attributes and keyboard support
8. **Test Progressive Enhancement**: Verify behavior with JavaScript disabled
9. **Document Usage**: Provide clear HTML examples

## File Organization

```
components/
├── async-action/
│   ├── async-action.js
│   ├── async-action.test.html
│   └── README.md
├── product-card/
│   ├── product-card.js
│   ├── product-card.test.html
│   └── README.md
└── index.js (exports all components)
```

## References

- [Custom Elements Spec](https://html.spec.whatwg.org/multipage/custom-elements.html)
- [Declarative Shadow DOM](https://web.dev/declarative-shadow-dom/)
- [ElementInternals API](https://developer.mozilla.org/en-US/docs/Web/API/ElementInternals)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
