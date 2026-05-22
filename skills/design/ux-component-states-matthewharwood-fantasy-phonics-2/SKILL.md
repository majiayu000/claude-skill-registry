---
name: ux-component-states
description: Interactive component state patterns including hover, focus, active, disabled, loading, and error states. Use when building buttons, inputs, cards, or any interactive elements. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Component States Skill

Interactive state management for web components. This skill covers visual feedback for all interaction states, ensuring components feel responsive and accessible.

## Core States

### Default State

The baseline appearance when no interaction occurs:

```css
.button {
  background: var(--theme-surface-variant);
  color: var(--theme-on-surface);
  border: 1px solid var(--theme-outline);
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease;
}
```

### Hover State

Visual feedback when pointer enters element:

```css
.button:hover:not(:disabled) {
  background: var(--color-hover-overlay);
  border-color: var(--theme-outline);
}

/* For primary buttons */
.button-primary:hover:not(:disabled) {
  background: var(--theme-on-primary-container);
}
```

### Focus State

Visible focus for keyboard navigation (use `:focus-visible`):

```css
.button:focus-visible {
  outline: var(--focus-ring-width) solid var(--focus-ring-color);
  outline-offset: var(--focus-ring-offset);
}

/* Alternative with box-shadow */
.input:focus {
  border-color: var(--theme-primary);
  box-shadow: 0 0 0 3px var(--color-active-overlay);
}
```

### Active/Pressed State

Feedback during click/tap:

```css
.button:active:not(:disabled) {
  transform: scale(0.98);
  background: var(--color-active-overlay);
}
```

### Disabled State

Non-interactive appearance:

```css
.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

/* Alternative: muted colors */
.button:disabled {
  background: var(--theme-surface);
  color: var(--theme-on-surface-variant);
  border-color: var(--theme-outline-variant);
}
```

## Extended States

### Loading State

When awaiting response:

```css
.button[aria-busy="true"] {
  position: relative;
  color: transparent;
  pointer-events: none;
}

.button[aria-busy="true"]::after {
  content: '';
  position: absolute;
  inset: 0;
  margin: auto;
  width: 1em;
  height: 1em;
  border: 2px solid var(--theme-on-primary);
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { rotate: 360deg; }
}
```

### Selected/Active (Toggle)

For toggleable or selectable items:

```css
.tab[aria-selected="true"] {
  background: var(--theme-primary);
  color: var(--theme-on-primary);
  font-weight: 600;
}

.checkbox[aria-checked="true"] {
  background: var(--theme-primary);
  border-color: var(--theme-primary);
}
```

### Current/Active Navigation

For indicating current location:

```css
.nav-item[aria-current="page"] {
  background: var(--theme-primary);
  color: var(--theme-on-primary);
}

.step[aria-current="step"] {
  color: var(--theme-primary);
  font-weight: 600;
}
```

### Error State

For validation failures:

```css
.input[aria-invalid="true"] {
  border-color: var(--color-error);
}

.input[aria-invalid="true"]:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}

.error-message {
  color: var(--color-error);
  font-size: var(--step--1);
}
```

### Success State

For completed or correct items:

```css
.input[data-valid="true"] {
  border-color: var(--color-success);
}

.item[data-completed] {
  color: var(--color-success);
}

.item[data-completed] .icon {
  color: var(--color-success);
}

/* Add check icon via Material Symbols */
/* <span class="icon" aria-hidden="true">check</span> */
```

### Locked/Unavailable State

For items not yet accessible:

```css
.item[data-locked] {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(0.5);
}

.item[data-locked] .icon {
  /* Use Material Symbol: lock */
  /* <span class="icon" aria-hidden="true">lock</span> */
}
```

### Undefined State (Web Components)

Custom elements are "undefined" until JavaScript loads and registers them. Use `:not(:defined)` to prevent Flash of Unstyled Content (FOUC):

```css
/* Hide custom elements before JavaScript defines them */
site-nav:not(:defined),
word-card:not(:defined) {
  opacity: 0;
}

/* Reserve layout space for fixed elements to prevent CLS */
site-nav:not(:defined) {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  min-height: calc(var(--nav-height, 56px) + var(--space-s) * 2);
  background: var(--theme-surface);
}

/* Show once defined */
site-nav:defined {
  opacity: 1;
}
```

**Why `opacity: 0` instead of `display: none`?**
- `opacity: 0` preserves layout space, preventing CLS (Cumulative Layout Shift)
- `display: none` causes layout shift when element appears
- Reserve actual dimensions for fixed/positioned elements

**Combine with modulepreload for best results:**
```html
<link rel="modulepreload" href="/js/components/site-nav.js">
```

See **`web-components`** skill for complete FOUC prevention patterns.

## State Attribute Patterns

### Use Data Attributes for Custom States

```javascript
// In component
this.dataset.status = 'loading';  // [data-status="loading"]
this.dataset.status = 'complete'; // [data-status="complete"]
this.dataset.status = 'error';    // [data-status="error"]
```

```css
[data-status="loading"] { /* ... */ }
[data-status="complete"] { /* ... */ }
[data-status="error"] { /* ... */ }
```

### Use ARIA for Semantic States

```javascript
// Toggle pressed state
this.setAttribute('aria-pressed', this.#pressed);

// Set disabled
this.setAttribute('aria-disabled', 'true');

// Set busy/loading
this.setAttribute('aria-busy', 'true');

// Set invalid
this.internals.setValidity({ valueMissing: true }, 'Required');
this.setAttribute('aria-invalid', 'true');
```

## State Transitions

### Smooth Transitions

```css
.interactive {
  transition:
    background-color 0.15s ease,
    border-color 0.15s ease,
    color 0.15s ease,
    transform 0.1s ease,
    opacity 0.15s ease;
}
```

### Respect Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  .interactive {
    transition: none;
  }
}
```

## Component Examples

### Button States

```css
.button {
  /* Default */
  background: var(--theme-surface-variant);
  border: 1px solid var(--theme-outline);
  color: var(--theme-on-surface);
  transition: all 0.15s ease;
}

.button:hover:not(:disabled) {
  background: var(--color-hover-overlay);
}

.button:focus-visible {
  outline: var(--focus-ring-width) solid var(--focus-ring-color);
  outline-offset: var(--focus-ring-offset);
}

.button:active:not(:disabled) {
  transform: scale(0.98);
}

.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

### Input States

```css
.input {
  /* Default */
  border: 1px solid var(--theme-outline);
  background: var(--theme-surface-variant);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.input:hover:not(:disabled) {
  border-color: var(--theme-outline);
}

.input:focus {
  outline: none;
  border-color: var(--theme-primary);
  box-shadow: 0 0 0 3px var(--color-active-overlay);
}

.input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input[aria-invalid="true"] {
  border-color: var(--color-error);
}

.input[aria-invalid="true"]:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}
```

### Card States

```css
.card {
  /* Default */
  background: var(--theme-surface-variant);
  border: 1px solid var(--theme-outline-variant);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.card:hover {
  border-color: var(--theme-outline);
}

.card:focus-within {
  border-color: var(--theme-primary);
}

.card[data-selected] {
  border-color: var(--theme-primary);
  box-shadow: 0 0 0 2px var(--theme-primary);
}
```

### Progress Indicator States

```css
.progress-dot {
  /* Pending */
  background: var(--theme-outline-variant);
}

.progress-dot[data-status="current"] {
  background: var(--theme-primary);
  animation: pulse 1.5s ease-in-out infinite;
}

.progress-dot[data-status="complete"] {
  background: var(--color-success);
}

.progress-dot[data-status="locked"] {
  opacity: 0.5;
}
```

## State Management in JavaScript

**Important**: Element references are stored during construction - NEVER use querySelector.

```javascript
class InteractiveComponent extends HTMLElement {
  // Direct element reference - created in constructor, never queried
  #button;

  static get observedAttributes() {
    return ['disabled', 'loading', 'selected'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Create and store direct reference during construction
    this.#button = document.createElement('button');
    this.#button.setAttribute('part', 'button');
    this.#button.appendChild(document.createElement('slot'));

    this.shadowRoot.appendChild(this.#button);
  }

  connectedCallback() {
    this.addEventListener('click', this);
  }

  disconnectedCallback() {
    this.removeEventListener('click', this);
  }

  handleEvent(e) {
    if (e.type === 'click') {
      this.dispatchEvent(new CustomEvent('button-click', {
        bubbles: true,
        composed: true
      }));
    }
  }

  attributeChangedCallback(name, oldVal, newVal) {
    if (oldVal === newVal) return;

    switch (name) {
      case 'disabled':
        this.#updateDisabled(newVal !== null);
        break;
      case 'loading':
        this.#updateLoading(newVal !== null);
        break;
      case 'selected':
        this.#updateSelected(newVal !== null);
        break;
    }
  }

  #updateDisabled(disabled) {
    this.setAttribute('aria-disabled', disabled);
    this.#button.disabled = disabled;  // Direct reference
  }

  #updateLoading(loading) {
    this.setAttribute('aria-busy', loading);
    this.#button.disabled = loading;   // Direct reference
  }

  #updateSelected(selected) {
    this.setAttribute('aria-pressed', selected);
  }
}

customElements.define('interactive-button', InteractiveComponent);
```
