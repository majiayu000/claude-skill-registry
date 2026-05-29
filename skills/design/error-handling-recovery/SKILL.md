---
name: error-handling-recovery
description: Design error states and recovery workflows that guide users to resolution. Learn context-aware error messages, graceful degradation, and recovery patterns. Use when handling validation errors, network failures, permission issues, or system errors. Triggers on "error handling", "error message", "error state", "recovery", "validation error", "network error".
---

# Error Handling & Recovery

## Overview

Errors are inevitable. The difference between a frustrating product and a caring one is how you handle them. This skill teaches you to design error states that guide users to resolution rather than leaving them stranded.

## Core Philosophy: Never Blame the User

The first principle of error design is **never blame the user**. Errors are opportunities to help, not to criticize.

**Bad Error Messages:**
- "Invalid input"
- "Error 404"
- "Something went wrong"

**Good Error Messages:**
- "Please enter a valid email address (e.g., user@example.com)"
- "We couldn't find that page. Try searching instead."
- "Your connection was lost. We saved your work. Reconnect when ready."

## Error Message Anatomy

### The Four Components

Every error message should include:

1. **What happened** — Clear, specific description
2. **Why it happened** — Context for the user
3. **What to do** — Actionable next steps
4. **Where to get help** — Support resources if needed

### Example: Complete Error Message

```
❌ Email already in use

This email is already associated with an account. 

Try:
- Sign in with this email instead
- Use a different email address
- Reset your password if you forgot it

Need help? Contact support@example.com
```

## Error Message Design Principles

### 1. Be Specific, Not Generic

```html
<!-- Bad - Generic -->
<div class="error">Error: Invalid field</div>

<!-- Good - Specific -->
<div class="error">
  <strong>Password must be at least 8 characters</strong>
  <p>Include uppercase, lowercase, and numbers</p>
</div>
```

### 2. Use Friendly, Human Language

```html
<!-- Bad - Technical jargon -->
<div class="error">CORS policy violation detected</div>

<!-- Good - Human language -->
<div class="error">
  We couldn't connect to the server. Check your internet and try again.
</div>
```

### 3. Place Errors Next to the Problem

```html
<!-- Bad - Error far from input -->
<div class="error-summary">Email is invalid</div>
<form>
  <input type="email" />
</form>

<!-- Good - Error next to input -->
<form>
  <div class="form-group">
    <label for="email">Email</label>
    <input id="email" type="email" />
    <div class="error">Please enter a valid email</div>
  </div>
</form>
```

### 4. Use Visual Indicators (Not Color Alone)

```css
/* Bad - Color only */
.error-input {
  border-color: red;
}

/* Good - Icon + color + text */
.error-input {
  border-color: var(--error-color);
  border-width: 2px;
}

.error-input::before {
  content: '⚠️';
  margin-right: 8px;
}
```

### 5. Provide Constructive Guidance

```html
<!-- Bad - Just says what's wrong -->
<div class="error">Password too weak</div>

<!-- Good - Explains how to fix -->
<div class="error">
  <strong>Password too weak</strong>
  <ul>
    <li>✓ At least 8 characters</li>
    <li>✗ At least one uppercase letter</li>
    <li>✓ At least one number</li>
    <li>✓ At least one special character</li>
  </ul>
</div>
```

## Error Types and Patterns

### 1. Validation Errors

Errors that occur when user input doesn't meet requirements.

**Timing:** Show after user leaves the field (blur event)

```javascript
// Good - Validate on blur, not while typing
const handleBlur = (e) => {
  const value = e.target.value;
  if (!isValidEmail(value)) {
    showError('Please enter a valid email');
  }
};

// Bad - Validate while typing
const handleChange = (e) => {
  if (!isValidEmail(e.target.value)) {
    showError('Invalid email');  // Too aggressive
  }
};
```

### 2. Network Errors

Errors that occur when the server is unreachable or requests fail.

**Pattern:** Show error, offer retry, allow offline continuation

```html
<div class="error-state">
  <span class="error-icon">📡</span>
  <h3>Connection Lost</h3>
  <p>We couldn't reach the server. Your changes are saved locally.</p>
  <button class="button-primary">Retry</button>
  <button class="button-secondary">Continue Offline</button>
</div>
```

### 3. Permission Errors

Errors that occur when user lacks permission to perform an action.

**Pattern:** Explain why, offer alternatives, suggest next steps

```html
<div class="error-state">
  <span class="error-icon">🔒</span>
  <h3>Permission Denied</h3>
  <p>You don't have permission to edit this document.</p>
  <p>Ask the owner to give you edit access.</p>
  <button class="button-secondary">Request Access</button>
</div>
```

### 4. System Errors

Errors that occur due to system failures or unexpected issues.

**Pattern:** Apologize, explain impact, offer workarounds

```html
<div class="error-state">
  <span class="error-icon">⚠️</span>
  <h3>Something Went Wrong</h3>
  <p>We're having trouble processing your request. Our team has been notified.</p>
  <p>Error ID: #12345 (share this if contacting support)</p>
  <button class="button-primary">Try Again</button>
  <button class="button-secondary">Contact Support</button>
</div>
```

### 5. 404 Errors

Errors that occur when requested resource doesn't exist.

**Pattern:** Acknowledge, explain, guide to alternatives

```html
<div class="error-state">
  <h1>404 - Page Not Found</h1>
  <p>The page you're looking for doesn't exist or has been moved.</p>
  <form class="search-form">
    <input type="search" placeholder="Search for what you need..." />
    <button type="submit">Search</button>
  </form>
  <nav class="error-nav">
    <a href="/">Home</a>
    <a href="/help">Help Center</a>
    <a href="/contact">Contact Us</a>
  </nav>
</div>
```

## Error Message Styling

### CSS for Error States

```css
/* Error container */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
  background: var(--error-bg);
  border-radius: 8px;
  border-left: 4px solid var(--error-color);
}

/* Error icon */
.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

/* Error title */
.error-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--error-color);
  margin-bottom: 8px;
}

/* Error description */
.error-state p {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 24px;
  max-width: 400px;
}

/* Error input */
.error-input {
  border-color: var(--error-color);
  border-width: 2px;
  background-color: var(--error-bg);
}

.error-input:focus {
  border-color: var(--error-color);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

/* Error message below input */
.error-message {
  display: flex;
  align-items: center;
  margin-top: 8px;
  font-size: 14px;
  color: var(--error-color);
  animation: slideDown 300ms ease-out;
}

.error-message::before {
  content: '⚠️';
  margin-right: 8px;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

## Recovery Workflows

### Pattern 1: Inline Recovery

For simple errors, provide recovery action inline.

```html
<div class="form-group">
  <label for="email">Email</label>
  <input id="email" type="email" />
  <div class="error">
    This email is already registered.
    <button class="link-button">Sign in instead</button>
  </div>
</div>
```

### Pattern 2: Modal Recovery

For critical errors, use a modal to guide recovery.

```html
<div class="modal error-modal">
  <div class="modal-content">
    <h2>Payment Failed</h2>
    <p>Your card was declined. Please try another payment method.</p>
    <form>
      <div class="form-group">
        <label>Card Number</label>
        <input type="text" placeholder="1234 5678 9012 3456" />
      </div>
      <button class="button-primary">Try Again</button>
      <button class="button-secondary">Use Different Method</button>
    </form>
  </div>
</div>
```

### Pattern 3: Progressive Recovery

For complex errors, guide users through steps.

```html
<div class="recovery-steps">
  <div class="step active">
    <h3>Step 1: Check Connection</h3>
    <p>Make sure you're connected to the internet.</p>
    <button class="button-primary">Retry</button>
  </div>
  <div class="step">
    <h3>Step 2: Clear Cache</h3>
    <p>Clear your browser cache and try again.</p>
    <button class="button-secondary">Learn How</button>
  </div>
  <div class="step">
    <h3>Step 3: Contact Support</h3>
    <p>If the problem persists, contact our support team.</p>
    <button class="button-secondary">Contact Support</button>
  </div>
</div>
```

## Graceful Degradation

When features fail, degrade gracefully rather than breaking the entire interface.

### Example: Image Loading Error

```html
<!-- Show fallback when image fails -->
<img 
  src="image.jpg" 
  alt="Product photo"
  onerror="this.src='placeholder.jpg'"
/>
```

### Example: Feature Unavailable

```html
<!-- Disable feature, explain why -->
<button disabled title="Feature unavailable in offline mode">
  Share
</button>
<p class="help-text">
  You're offline. Sharing will be available when you reconnect.
</p>
```

## Accessibility in Error Handling

### 1. Announce Errors to Screen Readers

```html
<div role="alert" aria-live="polite">
  Please enter a valid email address
</div>
```

### 2. Use ARIA Attributes

```html
<input 
  type="email" 
  aria-invalid="true"
  aria-describedby="email-error"
/>
<div id="email-error" class="error-message">
  Please enter a valid email
</div>
```

### 3. Don't Rely on Color Alone

```css
/* Bad - Color only */
.error-input {
  border-color: red;
}

/* Good - Icon + color + text */
.error-input {
  border: 2px solid red;
}

.error-input::after {
  content: '⚠️';
}
```

## How to Use This Skill with Claude Code

### Design Error States

```
"I'm using the error-handling-recovery skill. Can you help me design error states for:
- Form validation errors
- Network failures
- Permission denied
- 404 pages
Include specific error messages and recovery actions"
```

### Create Error Message Guidelines

```
"Can you create error message guidelines for my app?
- Never blame the user
- Always provide next steps
- Include error IDs for support
- Use friendly language"
```

### Audit Error Handling

```
"Can you audit my error handling?
- Are my error messages specific?
- Do I provide recovery actions?
- Are errors accessible?
- Can users recover without support?"
```

## Integration with Other Skills

- **component-architecture** — Error components
- **accessibility-excellence** — Accessible error messages
- **interaction-design** — Error animations and transitions
- **typography-system** — Error message typography

## Key Principles

**1. Never Blame the User**
Errors are opportunities to help, not criticize.

**2. Be Specific**
Generic errors leave users confused and frustrated.

**3. Provide Recovery**
Always offer a path forward.

**4. Be Human**
Use friendly, conversational language.

**5. Make It Accessible**
Errors must be perceivable to everyone.

## Checklist: Is Your Error Handling Ready?

- [ ] Error messages are specific, not generic
- [ ] Error messages use friendly language
- [ ] Errors are placed next to the problem
- [ ] Visual indicators are used (not color alone)
- [ ] Recovery actions are provided
- [ ] Errors are announced to screen readers
- [ ] Error IDs are provided for support
- [ ] Network errors offer retry options
- [ ] Permission errors explain why
- [ ] 404 pages guide to alternatives

Thoughtful error handling transforms frustration into confidence.
