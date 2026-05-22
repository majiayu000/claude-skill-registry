---
name: ux-form-design
description: Form and input design patterns including validation, labels, error handling, and form-associated custom elements. Use when building forms, inputs, or interactive data collection. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Form Design Skill

Form patterns for data collection, validation, and user feedback. This skill covers accessible form design with custom elements.

## Form-Associated Custom Elements

### Basic Setup

**Important**: Store element references during construction - NEVER use querySelector.

```javascript
class CustomInput extends HTMLElement {
  static formAssociated = true;

  // Direct element references - created in constructor
  #input;
  #label;
  #hint;
  #error;

  constructor() {
    super();
    this.internals = this.attachInternals();
    this.attachShadow({ mode: 'open' });

    // Build DOM and store direct references
    this.#label = document.createElement('label');
    this.#label.setAttribute('part', 'label');

    this.#input = document.createElement('input');
    this.#input.setAttribute('part', 'input');

    this.#hint = document.createElement('span');
    this.#hint.className = 'hint';
    this.#hint.setAttribute('part', 'hint');

    this.#error = document.createElement('span');
    this.#error.className = 'error';
    this.#error.setAttribute('role', 'alert');
    this.#error.setAttribute('part', 'error');

    // Assemble shadow DOM
    const field = document.createElement('div');
    field.className = 'field';
    field.appendChild(this.#label);
    field.appendChild(this.#input);
    field.appendChild(this.#hint);
    field.appendChild(this.#error);

    this.shadowRoot.appendChild(field);
  }

  connectedCallback() {
    this.addEventListener('input', this);
    this.addEventListener('blur', this);
  }

  disconnectedCallback() {
    this.removeEventListener('input', this);
    this.removeEventListener('blur', this);
  }

  // Required: Set form value
  set value(val) {
    this.#input.value = val;
    this.internals.setFormValue(val);
  }

  get value() {
    return this.#input.value;
  }

  // Form lifecycle
  formResetCallback() {
    this.value = '';
  }

  formDisabledCallback(disabled) {
    this.toggleAttribute('disabled', disabled);
    this.#input.disabled = disabled;
  }
}
```

### Validation

```javascript
validate() {
  const value = this.#input.value.trim();  // Direct reference

  if (!value && this.hasAttribute('required')) {
    this.internals.setValidity(
      { valueMissing: true },
      'This field is required',
      this.#input  // Direct reference
    );
    this.setAttribute('aria-invalid', 'true');
    return false;
  }

  // Clear validation
  this.internals.setValidity({});
  this.removeAttribute('aria-invalid');
  return true;
}
```

## Input Field Structure

### Anatomy

```html
<div class="field">
  <label class="label" for="input-id">Field Label</label>
  <input class="input" id="input-id" aria-describedby="hint-id error-id">
  <span class="hint" id="hint-id">Optional hint text</span>
  <span class="error" id="error-id" role="alert"></span>
</div>
```

### CSS

```css
.field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2xs);
}

.label {
  font-family: var(--font-display);
  font-size: var(--step--1);
  font-weight: 600;
  color: var(--theme-on-surface);
}

.input {
  padding: var(--space-s);
  border: 1px solid var(--theme-outline);
  border-radius: var(--space-2xs);
  background: var(--theme-surface-variant);
  color: var(--theme-on-surface);
  font-size: var(--step-0);
  font-family: var(--font-sans);
}

.input:focus {
  outline: none;
  border-color: var(--theme-primary);
  box-shadow: 0 0 0 3px var(--color-active-overlay);
}

.hint {
  font-size: var(--step--2);
  color: var(--theme-on-surface-variant);
}

.error {
  font-size: var(--step--2);
  color: var(--color-error);
}
```

## Textarea (Auto-Resize)

### Modern Approach (field-sizing)

```css
.textarea {
  field-sizing: content;
  min-height: 3lh;
  max-height: 12lh;
  overflow-y: auto;
}
```

### Fallback for Older Browsers

Use direct element references (created in constructor):

```javascript
class AutoResizeTextarea extends HTMLElement {
  #textarea;  // Direct reference - NO querySelector
  #maxHeight = 300;

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    this.#textarea = document.createElement('textarea');
    this.#textarea.setAttribute('part', 'textarea');
    this.shadowRoot.appendChild(this.#textarea);
  }

  connectedCallback() {
    if (!CSS.supports('field-sizing', 'content')) {
      this.addEventListener('input', this);
    }
  }

  disconnectedCallback() {
    this.removeEventListener('input', this);
  }

  handleEvent(e) {
    if (e.type === 'input') {
      this.#autoResize();
    }
  }

  #autoResize() {
    this.#textarea.style.height = 'auto';
    this.#textarea.style.height = `${Math.min(this.#textarea.scrollHeight, this.#maxHeight)}px`;
  }
}
```

## Form Layout

### Vertical Stack

```css
.form {
  display: flex;
  flex-direction: column;
  gap: var(--space-m);
}
```

### Inline Fields

```css
.form-row {
  display: flex;
  gap: var(--space-s);
  flex-wrap: wrap;
}

.form-row > * {
  flex: 1;
  min-width: 150px;
}
```

### Form Actions

```css
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-s);
  margin-block-start: var(--space-m);
}
```

## Validation Patterns

### Real-Time Validation

```javascript
handleEvent(e) {
  if (e.type === 'input') {
    // Validate on input after first blur
    if (this.#touched) {
      this.validate();
    }
  }
  if (e.type === 'blur') {
    this.#touched = true;
    this.validate();
  }
}
```

### Submit Validation

Use direct element references (stored during construction):

```javascript
// Assumes #input, #container, #error are private fields
submit() {
  const value = this.#input.value.trim();  // Direct reference

  if (!value) {
    this.#input.focus();  // Direct reference
    this.internals.setValidity(
      { valueMissing: true },
      'Please enter a value',
      this.#input  // Direct reference
    );
    // Visual shake feedback using Anime.js
    import { shake } from '../../utils/animations.js';
    shake(this.#container);  // Direct reference
    return;
  }

  // Clear and submit
  this.internals.setValidity({});
  this.dispatchEvent(new CustomEvent('form-submit', {
    bubbles: true,
    composed: true,
    detail: { value }
  }));
}
```

### Error Display

```javascript
// Assumes #error and #input are private fields
showError(message) {
  this.#error.textContent = message;  // Direct reference
  this.setAttribute('aria-invalid', 'true');
}

clearError() {
  this.#error.textContent = '';  // Direct reference
  this.removeAttribute('aria-invalid');
}
```

## Accessibility Requirements

### Labels

Every input MUST have an associated label:

```html
<!-- Explicit association -->
<label for="name">Name</label>
<input id="name">

<!-- Implicit association -->
<label>
  Name
  <input>
</label>

<!-- ARIA label for icon-only -->
<input aria-label="Search">
```

### Required Fields

```html
<label>
  Email <span aria-hidden="true">*</span>
  <span class="sr-only">(required)</span>
</label>
<input required aria-required="true">
```

### Error Association

```html
<input aria-invalid="true" aria-describedby="email-error">
<span id="email-error" role="alert">Please enter a valid email</span>
```

### Keyboard Submission

Support Ctrl/Cmd+Enter for textarea forms:

```javascript
handleEvent(e) {
  if (e.type === 'keydown') {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      this.submit();
    }
  }
}
```

## Input Types

### Text Variations

```html
<input type="text" inputmode="text">
<input type="email" inputmode="email">
<input type="tel" inputmode="tel">
<input type="url" inputmode="url">
<input type="number" inputmode="numeric">
```

### Autocomplete

```html
<input name="name" autocomplete="name">
<input name="email" autocomplete="email">
<input name="current-password" autocomplete="current-password">
```

## Placeholder Best Practices

### Do

```css
/* Subtle placeholder */
.input::placeholder {
  color: var(--theme-on-surface-variant);
  opacity: 0.7;
}
```

### Don't

- Never use placeholder as label replacement
- Avoid long placeholder text
- Don't include required format in placeholder alone

### Correct Pattern

```html
<label for="phone">Phone Number</label>
<input id="phone" placeholder="555-555-5555" aria-describedby="phone-format">
<span id="phone-format" class="hint">Format: XXX-XXX-XXXX</span>
```

## Touch Targets

Ensure inputs meet minimum touch target size:

```css
.input {
  min-height: var(--min-touch-target);
  padding: var(--space-s);
}

.checkbox-wrapper {
  min-width: var(--min-touch-target);
  min-height: var(--min-touch-target);
  display: flex;
  align-items: center;
  justify-content: center;
}
```

## Disabled vs Read-Only

```css
/* Disabled: Cannot interact */
.input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: var(--theme-surface);
}

/* Read-only: Can select/copy but not edit */
.input:read-only {
  background: var(--theme-surface);
  border-style: dashed;
}
```
