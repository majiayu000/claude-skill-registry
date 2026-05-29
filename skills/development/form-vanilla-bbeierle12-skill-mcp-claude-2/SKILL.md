---
name: form-vanilla
description: Framework-free form validation using HTML5 Constraint Validation API enhanced with Zod for complex rules. Use when building forms without React/Vue or for progressive enhancement.
---

# Form Vanilla

Framework-free form patterns using native browser APIs enhanced with Zod.

## Quick Start

```html
<form id="login-form" novalidate>
  <div class="form-field">
    <label for="email">Email</label>
    <input 
      id="email" 
      name="email" 
      type="email" 
      autocomplete="email"
      required
    />
    <span class="error" aria-live="polite"></span>
  </div>
  
  <div class="form-field">
    <label for="password">Password</label>
    <input 
      id="password" 
      name="password" 
      type="password" 
      autocomplete="current-password"
      required
      minlength="8"
    />
    <span class="error" aria-live="polite"></span>
  </div>
  
  <button type="submit">Sign in</button>
</form>

<script type="module">
import { createFormValidator } from './vanilla-validator.js';
import { loginSchema } from './schemas.js';

const form = document.getElementById('login-form');
const validator = createFormValidator(form, loginSchema);

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const result = await validator.validate();
  if (result.valid) {
    console.log('Submit:', result.data);
  }
});
</script>
```

## HTML5 Constraint Validation API

### Built-in Attributes

```html
<!-- Required field -->
<input required />

<!-- Length constraints -->
<input minlength="3" maxlength="50" />

<!-- Number constraints -->
<input type="number" min="0" max="100" step="1" />

<!-- Pattern (regex) -->
<input pattern="[A-Za-z]{3}" title="Three letter code" />

<!-- Email validation -->
<input type="email" />

<!-- URL validation -->
<input type="url" />
```

### Validity State Properties

```javascript
const input = document.querySelector('input');

// Check individual constraints
input.validity.valueMissing;    // required but empty
input.validity.typeMismatch;    // email/url format wrong
input.validity.patternMismatch; // regex failed
input.validity.tooShort;        // < minlength
input.validity.tooLong;         // > maxlength
input.validity.rangeUnderflow;  // < min
input.validity.rangeOverflow;   // > max
input.validity.stepMismatch;    // not divisible by step
input.validity.badInput;        // browser can't parse
input.validity.customError;     // setCustomValidity called

// Check overall validity
input.validity.valid;           // all constraints pass
input.checkValidity();          // returns boolean
input.reportValidity();         // shows browser UI
```

### Custom Error Messages

```javascript
const input = document.querySelector('#email');

// Set custom validation message
input.addEventListener('invalid', (e) => {
  if (input.validity.valueMissing) {
    input.setCustomValidity('Please enter your email address');
  } else if (input.validity.typeMismatch) {
    input.setCustomValidity('Please enter a valid email (e.g., name@example.com)');
  }
});

// Clear custom message on input
input.addEventListener('input', () => {
  input.setCustomValidity('');
});
```

## Zod Integration

### Vanilla Validator Class

```typescript
// vanilla-validator.ts
import { z } from 'zod';

export interface ValidationResult<T> {
  valid: boolean;
  data?: T;
  errors: Record<string, string>;
}

export interface ValidatorOptions {
  /** When to validate */
  validateOn: 'blur' | 'input' | 'submit';
  
  /** When to re-validate after error */
  revalidateOn: 'input' | 'blur';
  
  /** Debounce delay for input validation (ms) */
  debounceMs?: number;
}

const defaultOptions: ValidatorOptions = {
  validateOn: 'blur',
  revalidateOn: 'input',
  debounceMs: 300
};

export function createFormValidator<T extends z.ZodType>(
  form: HTMLFormElement,
  schema: T,
  options: Partial<ValidatorOptions> = {}
): FormValidator<z.infer<T>> {
  const opts = { ...defaultOptions, ...options };
  const fieldErrors = new Map<string, string>();
  const touchedFields = new Set<string>();
  let debounceTimers = new Map<string, ReturnType<typeof setTimeout>>();

  // Get all form fields
  const fields = Array.from(form.elements).filter(
    (el): el is HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement =>
      el instanceof HTMLInputElement ||
      el instanceof HTMLSelectElement ||
      el instanceof HTMLTextAreaElement
  );

  // Attach event listeners
  fields.forEach(field => {
    if (!field.name) return;

    // Blur handler (punish late)
    field.addEventListener('blur', () => {
      touchedFields.add(field.name);
      if (opts.validateOn === 'blur') {
        validateField(field.name);
      }
    });

    // Input handler (real-time correction)
    field.addEventListener('input', () => {
      // Clear existing timer
      const timer = debounceTimers.get(field.name);
      if (timer) clearTimeout(timer);

      // Only validate if already has error (correction mode)
      if (fieldErrors.has(field.name) && opts.revalidateOn === 'input') {
        debounceTimers.set(
          field.name,
          setTimeout(() => validateField(field.name), opts.debounceMs)
        );
      }
    });
  });

  function getFormData(): Record<string, unknown> {
    const data: Record<string, unknown> = {};
    const formData = new FormData(form);
    
    formData.forEach((value, key) => {
      // Handle checkboxes
      const field = form.elements.namedItem(key);
      if (field instanceof HTMLInputElement && field.type === 'checkbox') {
        data[key] = field.checked;
      } else if (field instanceof HTMLInputElement && field.type === 'number') {
        data[key] = value === '' ? undefined : Number(value);
      } else {
        data[key] = value;
      }
    });
    
    return data;
  }

  function validateField(name: string): string | undefined {
    const data = getFormData();
    const result = schema.safeParse(data);
    
    if (result.success) {
      clearFieldError(name);
      return undefined;
    }
    
    const fieldError = result.error.errors.find(e => e.path[0] === name);
    if (fieldError) {
      setFieldError(name, fieldError.message);
      return fieldError.message;
    } else {
      clearFieldError(name);
      return undefined;
    }
  }

  function setFieldError(name: string, message: string): void {
    fieldErrors.set(name, message);
    
    const field = form.elements.namedItem(name) as HTMLInputElement | null;
    if (!field) return;
    
    // Set ARIA attributes
    field.setAttribute('aria-invalid', 'true');
    
    // Find error element
    const fieldWrapper = field.closest('.form-field');
    const errorEl = fieldWrapper?.querySelector('.error');
    if (errorEl) {
      errorEl.textContent = message;
      field.setAttribute('aria-describedby', errorEl.id || '');
    }
    
    // Add error class
    fieldWrapper?.classList.add('has-error');
    fieldWrapper?.classList.remove('is-valid');
    
    // Set custom validity for native UI
    field.setCustomValidity(message);
  }

  function clearFieldError(name: string): void {
    fieldErrors.delete(name);
    
    const field = form.elements.namedItem(name) as HTMLInputElement | null;
    if (!field) return;
    
    // Clear ARIA
    field.setAttribute('aria-invalid', 'false');
    field.removeAttribute('aria-describedby');
    
    // Clear error element
    const fieldWrapper = field.closest('.form-field');
    const errorEl = fieldWrapper?.querySelector('.error');
    if (errorEl) {
      errorEl.textContent = '';
    }
    
    // Update classes
    fieldWrapper?.classList.remove('has-error');
    if (touchedFields.has(name)) {
      fieldWrapper?.classList.add('is-valid');
    }
    
    // Clear custom validity
    field.setCustomValidity('');
  }

  function clearAllErrors(): void {
    fieldErrors.forEach((_, name) => clearFieldError(name));
  }

  async function validate(): Promise<ValidationResult<z.infer<T>>> {
    const data = getFormData();
    const result = schema.safeParse(data);
    
    if (result.success) {
      clearAllErrors();
      return { valid: true, data: result.data, errors: {} };
    }
    
    // Set errors for all fields
    const errors: Record<string, string> = {};
    result.error.errors.forEach(err => {
      const name = String(err.path[0]);
      errors[name] = err.message;
      setFieldError(name, err.message);
    });
    
    // Focus first error
    const firstErrorName = Object.keys(errors)[0];
    if (firstErrorName) {
      const field = form.elements.namedItem(firstErrorName) as HTMLElement;
      field?.focus();
    }
    
    return { valid: false, errors };
  }

  function reset(): void {
    form.reset();
    clearAllErrors();
    touchedFields.clear();
    debounceTimers.forEach(timer => clearTimeout(timer));
    debounceTimers.clear();
  }

  return {
    validate,
    validateField,
    setFieldError,
    clearFieldError,
    clearAllErrors,
    reset,
    getFormData
  };
}

export interface FormValidator<T> {
  validate(): Promise<ValidationResult<T>>;
  validateField(name: string): string | undefined;
  setFieldError(name: string, message: string): void;
  clearFieldError(name: string): void;
  clearAllErrors(): void;
  reset(): void;
  getFormData(): Record<string, unknown>;
}
```

### Usage Example

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .form-field {
      margin-bottom: 1rem;
    }
    
    .form-field label {
      display: block;
      margin-bottom: 0.25rem;
    }
    
    .form-field input {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    
    .form-field.has-error input {
      border-color: #dc2626;
    }
    
    .form-field.is-valid input {
      border-color: #059669;
    }
    
    .form-field .error {
      color: #dc2626;
      font-size: 0.875rem;
      margin-top: 0.25rem;
    }
  </style>
</head>
<body>
  <form id="contact-form" novalidate>
    <div class="form-field">
      <label for="name">Name</label>
      <input id="name" name="name" type="text" autocomplete="name" />
      <span class="error" id="name-error" aria-live="polite"></span>
    </div>
    
    <div class="form-field">
      <label for="email">Email</label>
      <input id="email" name="email" type="email" autocomplete="email" />
      <span class="error" id="email-error" aria-live="polite"></span>
    </div>
    
    <div class="form-field">
      <label for="message">Message</label>
      <textarea id="message" name="message" rows="4"></textarea>
      <span class="error" id="message-error" aria-live="polite"></span>
    </div>
    
    <button type="submit">Send</button>
  </form>

  <script type="module">
    import { z } from 'https://cdn.jsdelivr.net/npm/zod@3/+esm';
    import { createFormValidator } from './vanilla-validator.js';
    
    const schema = z.object({
      name: z.string().min(1, 'Please enter your name'),
      email: z.string().email('Please enter a valid email'),
      message: z.string().min(10, 'Message must be at least 10 characters')
    });
    
    const form = document.getElementById('contact-form');
    const validator = createFormValidator(form, schema);
    
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const result = await validator.validate();
      if (result.valid) {
        console.log('Submitting:', result.data);
        // Send to server...
        alert('Message sent!');
        validator.reset();
      }
    });
  </script>
</body>
</html>
```

## Progressive Enhancement

### Base HTML (Works Without JS)

```html
<form action="/submit" method="POST">
  <div class="form-field">
    <label for="email">Email *</label>
    <input 
      id="email" 
      name="email" 
      type="email" 
      required
      autocomplete="email"
    />
  </div>
  
  <div class="form-field">
    <label for="password">Password *</label>
    <input 
      id="password" 
      name="password" 
      type="password" 
      required
      minlength="8"
      autocomplete="current-password"
    />
  </div>
  
  <button type="submit">Sign in</button>
</form>
```

### Enhanced With JS

```javascript
// Only runs if JS is available
const form = document.querySelector('form');

if (form) {
  // Disable native validation UI
  form.setAttribute('novalidate', '');
  
  // Add ARIA live regions for errors
  form.querySelectorAll('.form-field').forEach(field => {
    const input = field.querySelector('input');
    if (input && input.name) {
      const errorEl = document.createElement('span');
      errorEl.className = 'error';
      errorEl.id = `${input.name}-error`;
      errorEl.setAttribute('aria-live', 'polite');
      field.appendChild(errorEl);
    }
  });
  
  // Attach validator
  const validator = createFormValidator(form, schema);
  
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const result = await validator.validate();
    if (result.valid) {
      form.submit(); // Native submit
    }
  });
}
```

## Common Patterns

### Password Visibility Toggle

```html
<div class="form-field password-field">
  <label for="password">Password</label>
  <div class="input-wrapper">
    <input 
      id="password" 
      name="password" 
      type="password"
      autocomplete="current-password"
    />
    <button 
      type="button" 
      class="toggle-password"
      aria-label="Show password"
    >
      👁
    </button>
  </div>
</div>

<script>
document.querySelectorAll('.toggle-password').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = btn.previousElementSibling;
    const isPassword = input.type === 'password';
    
    input.type = isPassword ? 'text' : 'password';
    btn.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
    btn.textContent = isPassword ? '🙈' : '👁';
  });
});
</script>
```

### Character Counter

```html
<div class="form-field">
  <label for="bio">Bio</label>
  <textarea id="bio" name="bio" maxlength="500"></textarea>
  <span class="char-count"><span id="bio-count">0</span>/500</span>
</div>

<script>
const textarea = document.getElementById('bio');
const counter = document.getElementById('bio-count');

textarea.addEventListener('input', () => {
  counter.textContent = textarea.value.length;
});
</script>
```

### Form Submission with Fetch

```javascript
const form = document.getElementById('my-form');
const submitBtn = form.querySelector('button[type="submit"]');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const result = await validator.validate();
  if (!result.valid) return;
  
  // Disable button
  submitBtn.disabled = true;
  submitBtn.textContent = 'Sending...';
  
  try {
    const response = await fetch(form.action, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': document.querySelector('[name="_csrf"]').value
      },
      body: JSON.stringify(result.data)
    });
    
    if (!response.ok) {
      const error = await response.json();
      // Handle server errors
      if (error.field) {
        validator.setFieldError(error.field, error.message);
      } else {
        alert(error.message);
      }
      return;
    }
    
    // Success
    alert('Form submitted!');
    validator.reset();
    
  } catch (err) {
    alert('Network error. Please try again.');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Submit';
  }
});
```

## File Structure

```
form-vanilla/
├── SKILL.md
├── references/
│   └── constraint-validation.md  # HTML5 Constraint API reference
└── scripts/
    ├── vanilla-validator.ts      # Main validator class
    ├── vanilla-validator.js      # Compiled JS
    ├── progressive-enhance.js    # Progressive enhancement utils
    └── examples/
        ├── login-form.html
        ├── contact-form.html
        └── checkout-form.html
```

## Reference

- `references/constraint-validation.md` — HTML5 Constraint Validation API reference
