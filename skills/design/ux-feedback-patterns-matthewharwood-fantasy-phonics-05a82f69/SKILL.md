---
name: ux-feedback-patterns
description: User feedback patterns including success/error messages, loading states, confirmations, and progress indicators. Use when implementing notifications, toasts, or status updates. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Feedback Patterns Skill

User feedback mechanisms for communicating state changes, success, errors, and progress. This skill covers visual, auditory, and haptic feedback patterns.

## Related Skills

- **`material-symbols-v3`**: Icon names for status indicators (`check_circle`, `error`, `warning`)
- **`ux-iconography`**: Icon + text patterns for feedback
- **`ux-animation-motion`**: Anime.js animations for feedback effects

## Feedback Types

### 1. Inline Feedback

Immediate feedback near the action:

```html
<button>Save</button>
<span class="inline-feedback" role="status" aria-live="polite">
  Saved successfully
</span>
```

```css
.inline-feedback {
  font-size: var(--step--1);
  color: var(--color-success);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.inline-feedback.visible {
  opacity: 1;
}
```

### 2. Toast Notifications

Non-blocking temporary messages as a web component:

```javascript
class ToastContainer extends HTMLElement {
  #container;  // Direct reference - NO querySelector

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Build and store direct reference
    this.#container = document.createElement('div');
    this.#container.className = 'toast-container';
    this.#container.setAttribute('part', 'container');

    this.shadowRoot.appendChild(this.#container);
  }

  show(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('part', 'toast');
    toast.textContent = message;

    this.#container.appendChild(toast);  // Direct reference

    // Auto-dismiss
    setTimeout(() => {
      toast.classList.add('exiting');
      toast.addEventListener('animationend', () => toast.remove());
    }, duration);
  }
}

customElements.define('toast-container', ToastContainer);
```

```css
.toast {
  padding: var(--space-s) var(--space-m);
  background: var(--theme-surface-variant);
  border-radius: var(--space-2xs);
  animation: slideIn 0.2s ease;
}

.toast-success {
  border-left: 4px solid var(--color-success);
}

.toast-error {
  border-left: 4px solid var(--color-error);
}

.toast.exiting {
  animation: slideOut 0.2s ease forwards;
}
```

### 3. Confirmation Dialogs

For destructive or important actions:

```html
<dialog class="confirm-dialog">
  <h2>Confirm Action</h2>
  <p>Are you sure you want to proceed?</p>
  <div class="dialog-actions">
    <button class="btn-secondary">Cancel</button>
    <button class="btn-danger">Delete</button>
  </div>
</dialog>
```

### 4. Progress Indicators

For long-running operations:

```html
<!-- Determinate progress -->
<progress value="60" max="100" aria-label="Upload progress">60%</progress>

<!-- Indeterminate/spinner -->
<div class="spinner" role="status" aria-label="Loading">
  <span class="sr-only">Loading...</span>
</div>
```

## Success Feedback

### Visual Patterns

```css
/* Success color */
.success {
  color: var(--color-success);
}

/* Success icon - use Material Symbol */
/* <span class="icon" aria-hidden="true">check_circle</span> */
.icon-success {
  color: var(--color-success);
}

/* Success border */
.input-success {
  border-color: var(--color-success);
}
```

### Animation

```javascript
import { successBounce, glow } from '../../utils/animations.js';

// On successful action
successBounce(element);
glow(element, { color: 'rgba(74, 222, 128, 0.6)' });
```

### Announcements

```javascript
announce(message) {
  // For screen readers
  this.#announcer.textContent = '';
  requestAnimationFrame(() => {
    this.#announcer.textContent = message;
  });
}

// Usage
this.announce('Word completed! 3 points earned.');
```

## Error Feedback

### Visual Patterns

```css
/* Error color */
.error {
  color: var(--color-error);
}

/* Error state */
[aria-invalid="true"] {
  border-color: var(--color-error);
}

/* Error message */
.error-message {
  color: var(--color-error);
  font-size: var(--step--1);
}
```

### Shake Animation

```javascript
import { shake } from '../../utils/animations.js';

// On validation failure
shake(inputContainer, { intensity: 6 });
```

### Error Message Structure

```html
<div class="field">
  <input aria-invalid="true" aria-describedby="error-1">
  <span id="error-1" class="error-message" role="alert">
    Please enter a valid email address
  </span>
</div>
```

## Loading States

### Button Loading

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
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
```

### Skeleton Loading

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--theme-surface-variant) 25%,
    var(--theme-surface) 50%,
    var(--theme-surface-variant) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--space-2xs);
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Page Loading

```html
<div class="loading-overlay" role="status">
  <div class="spinner"></div>
  <span class="sr-only">Loading game...</span>
</div>
```

## Progress Indicators

### Linear Progress

```css
.progress-bar {
  height: 4px;
  background: var(--theme-outline-variant);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--theme-primary);
  transition: width 0.3s ease;
}
```

### Step Progress

```html
<ol class="steps" aria-label="Progress">
  <li data-status="complete" aria-current="false">Step 1</li>
  <li data-status="current" aria-current="step">Step 2</li>
  <li data-status="pending" aria-current="false">Step 3</li>
</ol>
```

```css
.steps [data-status="complete"] {
  color: var(--color-success);
}

.steps [data-status="current"] {
  color: var(--theme-primary);
  font-weight: 600;
}

.steps [data-status="pending"] {
  color: var(--theme-on-surface-variant);
}
```

### Circular Progress

```css
.progress-circle {
  --progress: 0;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: conic-gradient(
    var(--theme-primary) calc(var(--progress) * 1%),
    var(--theme-outline-variant) 0
  );
}
```

## Live Regions

### Status Updates

```html
<div role="status" aria-live="polite" aria-atomic="true">
  Score: 42 points
</div>
```

### Alerts

```html
<div role="alert" aria-live="assertive">
  Session expired. Please log in again.
</div>
```

### Implementation

```javascript
class Announcer {
  #region;

  constructor() {
    this.#region = document.createElement('div');
    this.#region.setAttribute('role', 'status');
    this.#region.setAttribute('aria-live', 'polite');
    this.#region.setAttribute('aria-atomic', 'true');
    this.#region.className = 'sr-only';
    document.body.appendChild(this.#region);
  }

  announce(message, priority = 'polite') {
    this.#region.setAttribute('aria-live', priority);
    this.#region.textContent = '';
    requestAnimationFrame(() => {
      this.#region.textContent = message;
    });
  }
}
```

## Timing Guidelines

| Feedback Type | Duration | Use Case |
|---------------|----------|----------|
| Micro-animation | 100-200ms | Button press, toggle |
| State transition | 200-300ms | Page change, modal |
| Toast display | 3-5 seconds | Success message |
| Error display | Until dismissed | Validation error |
| Loading indicator | Immediate | Any async operation |

## Accessibility Checklist

- [ ] Success/error announced to screen readers
- [ ] Focus moved to relevant element after action
- [ ] Loading states communicated with `aria-busy`
- [ ] Progress communicated with proper ARIA
- [ ] Animations respect `prefers-reduced-motion`
- [ ] Color is not the only indicator of state
- [ ] Error messages are associated with inputs
