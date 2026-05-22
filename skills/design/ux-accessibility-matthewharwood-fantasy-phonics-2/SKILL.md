---
name: ux-accessibility
description: WCAG 2.2 accessibility patterns for web components. Use when implementing focus management, keyboard navigation, screen reader support, reduced motion, high contrast mode, or touch targets. Integrates with project's accessibility.css tokens. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Accessibility Skill

Accessibility-first design patterns for WCAG 2.2 AA compliance. This skill provides implementation guidance for making interactive components accessible to all users.

## Related Skills

- **`material-symbols-v3`**: Icon accessibility patterns (`aria-hidden`, `aria-label`)
- **`ux-iconography`**: Icon button patterns and screen reader text
- **`ux-component-states`**: ARIA state attributes for interactive elements

## Project Accessibility Tokens

This project defines accessibility tokens in `css/styles/accessibility.css`:

```css
:root {
  --focus-ring-width: 2px;
  --focus-ring-offset: 2px;
  --focus-ring-color: var(--color-primary);
  --min-touch-target: 44px;
  --transition-fast: 150ms ease;
}
```

## Focus Management

### Focus Ring Implementation

Always use the project's focus tokens for consistent visible focus:

```css
.interactive:focus-visible {
  outline: var(--focus-ring-width) solid var(--focus-ring-color);
  outline-offset: var(--focus-ring-offset);
}
```

### Focus Trap for Modals

When implementing modals or dialogs, trap focus using direct element references (NO querySelector):

```javascript
class ModalDialog extends HTMLElement {
  // Store focusable elements as direct references during construction
  #closeBtn;
  #confirmBtn;

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Build DOM imperatively, storing references
    this.#closeBtn = document.createElement('button');
    this.#closeBtn.className = 'close-btn';
    this.#closeBtn.textContent = '×';
    this.#closeBtn.setAttribute('part', 'close');

    this.#confirmBtn = document.createElement('button');
    this.#confirmBtn.className = 'confirm-btn';
    this.#confirmBtn.textContent = 'Confirm';
    this.#confirmBtn.setAttribute('part', 'confirm');

    const container = document.createElement('div');
    container.className = 'modal';
    container.setAttribute('part', 'container');
    container.appendChild(this.#closeBtn);
    container.appendChild(document.createElement('slot'));
    container.appendChild(this.#confirmBtn);

    this.shadowRoot.appendChild(container);
  }

  connectedCallback() {
    this.addEventListener('keydown', this);
  }

  disconnectedCallback() {
    this.removeEventListener('keydown', this);
  }

  handleEvent(e) {
    if (e.type === 'keydown' && e.key === 'Tab') {
      const active = this.shadowRoot.activeElement;

      if (e.shiftKey && active === this.#closeBtn) {
        e.preventDefault();
        this.#confirmBtn.focus();
      } else if (!e.shiftKey && active === this.#confirmBtn) {
        e.preventDefault();
        this.#closeBtn.focus();
      }
    }
  }
}
```

### Return Focus After Close

Store and restore focus when closing overlays:

```javascript
#previouslyFocused = null;

open() {
  this.#previouslyFocused = document.activeElement;
  this.showModal();
}

close() {
  this.close();
  this.#previouslyFocused?.focus();
}
```

## Keyboard Navigation

### Standard Patterns

| Component | Key | Action |
|-----------|-----|--------|
| Button | Enter, Space | Activate |
| Menu | Arrow keys | Navigate items |
| Dialog | Escape | Close |
| Tabs | Arrow keys | Switch tabs |
| Listbox | Arrow keys, Home, End | Navigate options |

### Implementation Example (Web Component)

```javascript
class KeyboardNav extends HTMLElement {
  // Direct element references - NO querySelector
  #items = [];
  #currentIndex = 0;

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    // Build items during construction, store direct references
  }

  connectedCallback() {
    this.setAttribute('role', 'menu');
    this.setAttribute('tabindex', '0');
    this.addEventListener('keydown', this);
  }

  disconnectedCallback() {
    this.removeEventListener('keydown', this);
  }

  handleEvent(e) {
    if (e.type === 'keydown') {
      switch (e.key) {
        case 'Enter':
        case ' ':
          e.preventDefault();
          this.#activate();
          break;
        case 'Escape':
          this.#close();
          break;
        case 'ArrowDown':
          e.preventDefault();
          this.#focusNext();
          break;
        case 'ArrowUp':
          e.preventDefault();
          this.#focusPrevious();
          break;
      }
    }
  }

  #focusNext() {
    this.#currentIndex = Math.min(this.#currentIndex + 1, this.#items.length - 1);
    this.#items[this.#currentIndex]?.focus();
  }

  #focusPrevious() {
    this.#currentIndex = Math.max(this.#currentIndex - 1, 0);
    this.#items[this.#currentIndex]?.focus();
  }

  #activate() {
    this.dispatchEvent(new CustomEvent('item-activated', {
      bubbles: true,
      composed: true,
      detail: { index: this.#currentIndex }
    }));
  }

  #close() {
    this.dispatchEvent(new CustomEvent('menu-close', {
      bubbles: true,
      composed: true
    }));
  }
}
```

## Screen Reader Support

### ARIA Attributes

Required ARIA for interactive components:

```html
<!-- Button with state -->
<button
  role="button"
  aria-pressed="false"
  aria-label="Toggle menu">

<!-- Live region for announcements -->
<div role="status" aria-live="polite" aria-atomic="true">
  Score updated: 42 points
</div>

<!-- Dialog -->
<dialog
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title">
```

### Live Regions

Use for dynamic content updates. Store the announcer as a direct reference (NO querySelector):

```javascript
class AnnouncingComponent extends HTMLElement {
  #announcer;

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Create and store direct reference during construction
    this.#announcer = document.createElement('div');
    this.#announcer.setAttribute('role', 'status');
    this.#announcer.setAttribute('aria-live', 'polite');
    this.#announcer.setAttribute('aria-atomic', 'true');
    this.#announcer.className = 'sr-only';

    this.shadowRoot.appendChild(this.#announcer);
  }

  announce(message) {
    // Use direct reference - never querySelector
    this.#announcer.textContent = '';
    requestAnimationFrame(() => {
      this.#announcer.textContent = message;
    });
  }
}
```

### Screen Reader Only Content

Use the `.sr-only` utility for visually hidden but accessible content:

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

## Reduced Motion

### Respecting User Preferences

Always check for reduced motion preference:

```css
/* In component styles */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### JavaScript Animation Check

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  animate(element, { scale: [1, 1.1, 1], duration: 200 });
} else {
  // Apply instant state change
  element.classList.add('active');
}
```

## High Contrast Mode

### Forced Colors Support

```css
@media (forced-colors: active) {
  .button {
    border: 2px solid ButtonText;
    background: ButtonFace;
    color: ButtonText;
  }

  .button:focus {
    outline: 3px solid Highlight;
  }

  .icon {
    forced-color-adjust: auto;
  }
}
```

## Touch Targets

### Minimum Size Requirements

WCAG requires 44x44px minimum touch targets:

```css
.touch-target {
  min-width: var(--min-touch-target);
  min-height: var(--min-touch-target);
  padding: var(--space-xs);
}

/* For smaller visual elements, expand hit area */
.small-button {
  position: relative;
}

.small-button::after {
  content: '';
  position: absolute;
  inset: -8px; /* Expand clickable area */
}
```

## Color Contrast

### Minimum Ratios

- Normal text: 4.5:1 contrast ratio
- Large text (18pt+): 3:1 contrast ratio
- UI components: 3:1 contrast ratio

### Testing Contrast

Use project semantic colors which are pre-validated:
- `--color-text` on `--theme-surface`: Meets AA
- `--color-muted` for secondary text: Meets AA for large text
- `--color-primary` for interactive: Meets 3:1 for UI

## Skip Links

For keyboard users to bypass navigation:

```html
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  z-index: 1000;
  padding: var(--space-s) var(--space-m);
  background: var(--theme-surface);
  color: var(--color-text);
}

.skip-link:focus {
  top: 0;
}
</style>
```

## Checklist

Before shipping any interactive component:

- [ ] Focus visible on all interactive elements
- [ ] Keyboard operable (Enter, Space, Escape, Arrows)
- [ ] ARIA roles and labels present
- [ ] Color contrast meets 4.5:1 (text) or 3:1 (UI)
- [ ] Touch targets are 44x44px minimum
- [ ] Reduced motion respected
- [ ] High contrast mode tested
- [ ] Screen reader announcement for state changes
