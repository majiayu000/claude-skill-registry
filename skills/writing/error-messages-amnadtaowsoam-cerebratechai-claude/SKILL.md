---
name: Error Messages
description: Comprehensive guide to writing clear, helpful, and user-friendly error messages that guide users to solutions
---

# Error Messages

## Why Error Messages Matter

**Problem:** Bad error messages frustrate users and increase support tickets

### Bad Error Message
```
Error: 500
```

### Good Error Message
```
We couldn't process your payment

Your card was declined. Please check your card details or try a different payment method.

Need help? Contact support@example.com
```

---

## Principles of Good Error Messages

### 1. Explain What Happened
```
Bad:  "Error"
Good: "We couldn't save your changes"
```

### 2. Explain Why It Happened
```
Bad:  "Failed"
Good: "Your session expired after 30 minutes of inactivity"
```

### 3. Tell Users What to Do Next
```
Bad:  "Invalid input"
Good: "Email address is required. Please enter your email to continue."
```

### 4. Use Plain Language (No Jargon)
```
Bad:  "ERR_CONNECTION_REFUSED"
Good: "We couldn't connect to the server. Please check your internet connection."
```

### 5. Be Empathetic (Not Blaming)
```
Bad:  "You entered an invalid email"
Good: "This email address doesn't look right. Please check for typos."
```

---

## Error Message Structure

### Template
```
[What happened]

[Why it happened] (optional)

[What to do next]

[Additional help] (optional)
```

### Example
```
We couldn't create your account

An account with this email already exists.

Try logging in instead, or use a different email address.

Forgot your password? Reset it here.
```

---

## Types of Errors

### Validation Errors
```
Field is empty:
"Email is required"

Invalid format:
"Please enter a valid email address (example@domain.com)"

Out of range:
"Password must be at least 8 characters"

Duplicate:
"This username is already taken. Try another one."
```

### System Errors
```
Server error:
"Something went wrong on our end. We're working to fix it. Please try again in a few minutes."

Network error:
"We couldn't connect to the server. Please check your internet connection and try again."

Timeout:
"This is taking longer than expected. Please try again."
```

### Permission Errors
```
Not logged in:
"Please log in to continue"

Insufficient permissions:
"You don't have permission to access this page. Contact your admin for access."

Subscription required:
"This feature is only available on Pro plans. Upgrade to unlock it."
```

### Not Found Errors
```
Page not found:
"We couldn't find this page. It may have been moved or deleted."

Resource not found:
"This file doesn't exist anymore. It may have been deleted."
```

---

## Writing Guidelines

### Be Specific
```
Bad:  "Invalid input"
Good: "Password must contain at least one number"
```

### Be Concise
```
Bad:  "We apologize for the inconvenience, but we were unable to process your request at this time due to a technical issue on our end."
Good: "We couldn't process your request. Please try again."
```

### Be Helpful
```
Bad:  "Error 403"
Good: "You don't have permission to view this page. Contact support@example.com for access."
```

### Avoid Technical Jargon
```
Bad:  "ERR_SSL_PROTOCOL_ERROR"
Good: "This site's security certificate is invalid. Try again later."
```

### Don't Blame the User
```
Bad:  "You forgot to enter your email"
Good: "Email is required"
```

---

## Error Message Examples

### Form Validation
```html
<!-- Empty field -->
<div class="error">
  Email is required
</div>

<!-- Invalid format -->
<div class="error">
  Please enter a valid email address
</div>

<!-- Password too short -->
<div class="error">
  Password must be at least 8 characters
</div>

<!-- Passwords don't match -->
<div class="error">
  Passwords don't match. Please try again.
</div>
```

### Login Errors
```
Wrong password:
"Incorrect password. Try again or reset your password."

Account not found:
"We couldn't find an account with this email. Sign up instead?"

Account locked:
"Your account has been locked after multiple failed login attempts. Reset your password to unlock it."

Email not verified:
"Please verify your email before logging in. Didn't receive the email? Resend it."
```

### Payment Errors
```
Card declined:
"Your card was declined. Please check your card details or try a different payment method."

Insufficient funds:
"Your card has insufficient funds. Please try a different payment method."

Expired card:
"Your card has expired. Please update your payment method."

Invalid CVV:
"The security code (CVV) is incorrect. It's the 3-digit number on the back of your card."
```

### File Upload Errors
```
File too large:
"This file is too large. Maximum size is 10MB."

Invalid file type:
"This file type isn't supported. Please upload a JPG, PNG, or PDF."

Upload failed:
"We couldn't upload your file. Please check your internet connection and try again."
```

---

## Error Severity Levels

### Info (Blue)
```
"Your changes were saved as a draft"
```

### Warning (Yellow)
```
"Your session will expire in 5 minutes. Save your work."
```

### Error (Red)
```
"We couldn't save your changes. Please try again."
```

### Success (Green)
```
"Your changes were saved successfully"
```

---

## Inline vs Modal Errors

### Inline Errors (Preferred for Forms)
```html
<input type="email" class="error" />
<span class="error-message">Please enter a valid email</span>
```

**Pros:**
- Immediate feedback
- User can fix without dismissing
- Less disruptive

### Modal Errors (For Critical Errors)
```html
<div class="modal">
  <h2>Payment Failed</h2>
  <p>Your card was declined. Please try a different payment method.</p>
  <button>Try Again</button>
</div>
```

**Use for:**
- Critical errors
- Errors requiring immediate attention
- Errors blocking workflow

---

## Error Recovery

### Provide Clear Actions
```
Bad:
"Error occurred"
[OK]

Good:
"We couldn't save your changes"
[Try Again] [Save as Draft] [Cancel]
```

### Auto-Retry (When Appropriate)
```
"Connection lost. Retrying in 3 seconds..."

[Retry Now] [Cancel]
```

### Preserve User Data
```
"We couldn't submit your form. Your responses have been saved."

[Try Again]
```

---

## Error Prevention

### Validate Early
```html
<!-- Validate on blur -->
<input type="email" onblur="validateEmail()" />

<!-- Show format hint -->
<input type="password" />
<span class="hint">Must be at least 8 characters</span>
```

### Provide Examples
```
Phone number: (555) 123-4567
Date: MM/DD/YYYY
```

### Use Appropriate Input Types
```html
<!-- Email keyboard on mobile -->
<input type="email" />

<!-- Number keyboard on mobile -->
<input type="tel" />

<!-- Date picker -->
<input type="date" />
```

---

## Accessibility

### Use ARIA Labels
```html
<div role="alert" aria-live="polite">
  Email is required
</div>
```

### Associate Errors with Fields
```html
<input type="email" aria-describedby="email-error" />
<span id="email-error" class="error">
  Please enter a valid email
</span>
```

### Use Color + Text
```
Don't rely on color alone
✗ Red border only
✓ Red border + error icon + error text
```

---

## Error Tracking

### Log Errors for Analysis
```javascript
function logError(errorType, errorMessage, context) {
  analytics.track('Error Shown', {
    type: errorType,
    message: errorMessage,
    page: window.location.pathname,
    context: context
  });
}

// Usage
logError('validation', 'Invalid email', { field: 'email' });
```

### Monitor Error Rates
```
Track:
- Most common errors
- Error rate by page
- Time to resolve errors
- Errors leading to abandonment
```

---

## Testing Error Messages

### Test Scenarios
```
✓ Empty fields
✓ Invalid formats
✓ Network failures
✓ Server errors
✓ Permission errors
✓ Edge cases
```

### User Testing
```
Ask users:
- Do you understand what went wrong?
- Do you know how to fix it?
- Is the message helpful?
```

---

## Best Practices

### 1. Be Human
```
Bad:  "ERR_INVALID_INPUT_001"
Good: "Oops! This email doesn't look right."
```

### 2. Be Specific
```
Bad:  "Something went wrong"
Good: "We couldn't send your email. Please check the recipient's address."
```

### 3. Be Actionable
```
Bad:  "Error"
Good: "Connection lost. Check your internet and try again."
```

### 4. Be Empathetic
```
Bad:  "You entered the wrong password"
Good: "Incorrect password. Try again or reset it."
```

### 5. Be Consistent
```
Use same tone and structure across all errors
```

---

## Common Mistakes

### ❌ Too Technical
```
"ERR_CONNECTION_REFUSED: ECONNREFUSED"
```

### ❌ Too Vague
```
"Error occurred"
```

### ❌ Blaming User
```
"You didn't enter a valid email"
```

### ❌ No Solution
```
"Invalid input"
```

### ❌ All Caps
```
"ERROR: PAYMENT FAILED"
```

---

## Error Message Checklist

```
☐ Explains what happened
☐ Explains why (if helpful)
☐ Tells user what to do next
☐ Uses plain language
☐ Is empathetic (not blaming)
☐ Is specific (not vague)
☐ Is concise (not wordy)
☐ Provides help link (if needed)
☐ Is accessible (ARIA labels)
☐ Is tested with users
```

---

## Summary

**Good Error Messages:**
- Explain what happened
- Explain why
- Tell users what to do
- Use plain language
- Are empathetic

**Structure:**
```
[What happened]
[Why it happened]
[What to do next]
[Additional help]
```

**Types:**
- Validation errors
- System errors
- Permission errors
- Not found errors

**Best Practices:**
- Be human
- Be specific
- Be actionable
- Be empathetic
- Be consistent

**Avoid:**
- Technical jargon
- Vague messages
- Blaming users
- No solutions
- All caps
