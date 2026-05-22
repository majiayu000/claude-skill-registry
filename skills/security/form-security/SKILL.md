---
name: form-security
description: Security patterns for web forms including autocomplete attributes for password managers, CSRF protection, XSS prevention, and input sanitization. Use when implementing authentication forms, payment forms, or any form handling sensitive data.
---

# Form Security

Security-first patterns for web forms. Ensures password manager compatibility, prevents common attacks, and protects user data.

## Quick Start

```tsx
// The 3 critical security patterns
<form>
  {/* 1. Autocomplete for password managers */}
  <input type="email" autoComplete="email" />
  <input type="password" autoComplete="current-password" />
  
  {/* 2. CSRF token */}
  <input type="hidden" name="_csrf" value={csrfToken} />
  
  {/* 3. Allow paste (never disable!) */}
  <input type="password" /> {/* No onPaste handler blocking */}
</form>
```

## Autocomplete Attributes

### Why It Matters

- **1Password, LastPass, Bitwarden** rely on `autocomplete` to identify fields
- Without correct values, password managers fail silently
- Users abandon forms when autofill doesn't work
- Security improves when users can use unique, strong passwords

### The Autocomplete Specification

```typescript
// autocomplete-config.ts
export const AUTOCOMPLETE = {
  // ===== IDENTITY =====
  name: 'name',                    // Full name
  honorificPrefix: 'honorific-prefix', // Mr., Mrs., Dr.
  givenName: 'given-name',         // First name
  additionalName: 'additional-name', // Middle name
  familyName: 'family-name',       // Last name
  honorificSuffix: 'honorific-suffix', // Jr., III
  nickname: 'nickname',
  
  // ===== AUTHENTICATION (CRITICAL) =====
  email: 'email',
  username: 'username',
  currentPassword: 'current-password',  // LOGIN forms
  newPassword: 'new-password',          // REGISTRATION + RESET forms
  oneTimeCode: 'one-time-code',         // 2FA/OTP codes
  
  // ===== CONTACT =====
  tel: 'tel',                      // Full phone
  telCountryCode: 'tel-country-code',
  telNational: 'tel-national',
  telAreaCode: 'tel-area-code',
  telLocal: 'tel-local',
  telExtension: 'tel-extension',
  
  // ===== ADDRESS =====
  streetAddress: 'street-address', // Full street (may be multiline)
  addressLine1: 'address-line1',   // Street line 1
  addressLine2: 'address-line2',   // Apt, Suite, etc.
  addressLine3: 'address-line3',
  addressLevel1: 'address-level1', // State/Province
  addressLevel2: 'address-level2', // City
  addressLevel3: 'address-level3', // District
  addressLevel4: 'address-level4', // Neighborhood
  postalCode: 'postal-code',
  country: 'country',
  countryName: 'country-name',
  
  // ===== PAYMENT (CRITICAL) =====
  ccName: 'cc-name',               // Name on card
  ccGivenName: 'cc-given-name',
  ccFamilyName: 'cc-family-name',
  ccNumber: 'cc-number',           // Card number
  ccExp: 'cc-exp',                 // Expiry (MM/YY)
  ccExpMonth: 'cc-exp-month',      // Expiry month
  ccExpYear: 'cc-exp-year',        // Expiry year
  ccCsc: 'cc-csc',                 // CVV/CVC
  ccType: 'cc-type',               // Visa, Mastercard, etc.
  
  // ===== ORGANIZATION =====
  organization: 'organization',
  organizationTitle: 'organization-title', // Job title
  
  // ===== DATES =====
  bday: 'bday',                    // Full birthday
  bdayDay: 'bday-day',
  bdayMonth: 'bday-month',
  bdayYear: 'bday-year',
  
  // ===== OTHER =====
  sex: 'sex',                      // Gender
  url: 'url',                      // Website
  photo: 'photo',                  // Photo URL
  language: 'language',
  
  // ===== SPECIAL VALUES =====
  off: 'off',                      // Disable autofill (use sparingly!)
  on: 'on'                         // Enable autofill (default)
} as const;

export type AutocompleteValue = typeof AUTOCOMPLETE[keyof typeof AUTOCOMPLETE];
```

### Critical Password Patterns

```tsx
// ✅ LOGIN: Use current-password
<form action="/login">
  <input type="email" autoComplete="email" />
  <input type="password" autoComplete="current-password" />
</form>

// ✅ REGISTRATION: Use new-password (BOTH fields)
<form action="/register">
  <input type="email" autoComplete="email" />
  <input type="password" autoComplete="new-password" />
  <input type="password" autoComplete="new-password" /> {/* confirm */}
</form>

// ✅ PASSWORD RESET: Use new-password
<form action="/reset-password">
  <input type="password" autoComplete="new-password" />
  <input type="password" autoComplete="new-password" /> {/* confirm */}
</form>

// ✅ CHANGE PASSWORD: current + new
<form action="/change-password">
  <input type="password" autoComplete="current-password" /> {/* old */}
  <input type="password" autoComplete="new-password" />     {/* new */}
  <input type="password" autoComplete="new-password" />     {/* confirm */}
</form>

// ✅ 2FA/OTP: Use one-time-code
<form action="/verify-2fa">
  <input 
    type="text" 
    inputMode="numeric" 
    autoComplete="one-time-code" 
    pattern="[0-9]*"
  />
</form>
```

### Why `new-password` for Registration

```tsx
// ❌ WRONG: Using current-password on registration
// Password manager tries to fill EXISTING password
<input type="password" autoComplete="current-password" />

// ✅ CORRECT: Using new-password
// Password manager offers to GENERATE a new password
<input type="password" autoComplete="new-password" />
```

### Payment Form Pattern

```tsx
<form action="/checkout">
  <input 
    type="text" 
    autoComplete="cc-name" 
    placeholder="Name on card"
  />
  
  <input 
    type="text" 
    inputMode="numeric"
    autoComplete="cc-number" 
    placeholder="Card number"
  />
  
  <input 
    type="text" 
    autoComplete="cc-exp" 
    placeholder="MM/YY"
  />
  
  <input 
    type="text" 
    inputMode="numeric"
    autoComplete="cc-csc" 
    placeholder="CVV"
  />
</form>
```

### Address Form Pattern

```tsx
<fieldset>
  <legend>Shipping Address</legend>
  
  <input autoComplete="name" placeholder="Full name" />
  <input autoComplete="address-line1" placeholder="Street address" />
  <input autoComplete="address-line2" placeholder="Apt, Suite, etc." />
  <input autoComplete="address-level2" placeholder="City" />
  <input autoComplete="address-level1" placeholder="State" />
  <input autoComplete="postal-code" placeholder="ZIP code" />
  <select autoComplete="country">
    <option value="US">United States</option>
    {/* ... */}
  </select>
</fieldset>
```

## CSRF Protection

### Token Generation (Server)

```typescript
// server/csrf.ts
import crypto from 'crypto';

export function generateCsrfToken(): string {
  return crypto.randomBytes(32).toString('hex');
}

// Store in session
app.use((req, res, next) => {
  if (!req.session.csrfToken) {
    req.session.csrfToken = generateCsrfToken();
  }
  res.locals.csrfToken = req.session.csrfToken;
  next();
});
```

### Token Inclusion (Client)

```tsx
// React pattern
function Form({ csrfToken }) {
  return (
    <form method="POST">
      <input type="hidden" name="_csrf" value={csrfToken} />
      {/* form fields */}
    </form>
  );
}

// With fetch
async function submitForm(data: FormData) {
  const response = await fetch('/api/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken
    },
    body: JSON.stringify(data)
  });
}
```

### Token Validation (Server)

```typescript
// Middleware
function validateCsrf(req, res, next) {
  const tokenFromBody = req.body._csrf;
  const tokenFromHeader = req.headers['x-csrf-token'];
  const sessionToken = req.session.csrfToken;
  
  const providedToken = tokenFromBody || tokenFromHeader;
  
  if (!providedToken || providedToken !== sessionToken) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  
  next();
}

// Apply to state-changing routes
app.post('/api/*', validateCsrf);
app.put('/api/*', validateCsrf);
app.delete('/api/*', validateCsrf);
```

### Double Submit Cookie Pattern

```typescript
// Alternative: Cookie + Header must match
// Server sets cookie
res.cookie('csrf', token, { httpOnly: false, sameSite: 'strict' });

// Client reads cookie and sends in header
const csrfToken = document.cookie
  .split('; ')
  .find(row => row.startsWith('csrf='))
  ?.split('=')[1];

fetch('/api/submit', {
  headers: { 'X-CSRF-Token': csrfToken }
});

// Server validates cookie === header
```

## XSS Prevention

### Never Trust User Input

```typescript
// ❌ DANGEROUS: Directly rendering user input
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ SAFE: React auto-escapes by default
<div>{userInput}</div>

// ✅ SAFE: Explicit sanitization when HTML needed
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

### Input Sanitization

```typescript
// sanitize.ts
import DOMPurify from 'dompurify';

// For plain text (strip all HTML)
export function sanitizeText(input: string): string {
  return DOMPurify.sanitize(input, { ALLOWED_TAGS: [] });
}

// For rich text (allow safe HTML)
export function sanitizeHtml(input: string): string {
  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'title']
  });
}

// For URLs
export function sanitizeUrl(url: string): string {
  const sanitized = DOMPurify.sanitize(url);
  // Only allow http(s) and relative URLs
  if (/^(https?:\/\/|\/[^\/])/i.test(sanitized)) {
    return sanitized;
  }
  return '';
}
```

### Content Security Policy

```typescript
// Set CSP headers (Express)
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
  );
  next();
});
```

## Password Field Security

### Never Disable Paste

```tsx
// ❌ DANGEROUS: Disabling paste
<input type="password" onPaste={(e) => e.preventDefault()} />

// ✅ CORRECT: Allow paste (password managers need it!)
<input type="password" />
```

### Password Visibility Toggle

```tsx
function PasswordInput({ ...props }) {
  const [visible, setVisible] = useState(false);
  
  return (
    <div className="password-input">
      <input
        type={visible ? 'text' : 'password'}
        {...props}
      />
      <button
        type="button"
        onClick={() => setVisible(!visible)}
        aria-label={visible ? 'Hide password' : 'Show password'}
      >
        {visible ? <EyeOffIcon /> : <EyeIcon />}
      </button>
    </div>
  );
}
```

### Don't Log Passwords

```typescript
// ❌ DANGEROUS
console.log('Login attempt:', { email, password });

// ✅ SAFE
console.log('Login attempt:', { email, password: '[REDACTED]' });
```

## Secure Form Submission

### HTTPS Only

```typescript
// Redirect HTTP to HTTPS
app.use((req, res, next) => {
  if (req.headers['x-forwarded-proto'] !== 'https') {
    return res.redirect(`https://${req.headers.host}${req.url}`);
  }
  next();
});
```

### Secure Cookies

```typescript
// Set secure cookie flags
res.cookie('session', sessionId, {
  httpOnly: true,     // Prevent XSS access
  secure: true,       // HTTPS only
  sameSite: 'strict', // CSRF protection
  maxAge: 3600000     // 1 hour
});
```

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts. Please try again later.'
});

app.post('/login', loginLimiter, handleLogin);
```

## Security Checklist

### Authentication Forms

- [ ] `autocomplete="email"` on email field
- [ ] `autocomplete="current-password"` on login password
- [ ] `autocomplete="new-password"` on registration/reset password
- [ ] `autocomplete="one-time-code"` on 2FA field
- [ ] Paste is allowed on all password fields
- [ ] CSRF token included
- [ ] Rate limiting enabled
- [ ] HTTPS enforced

### Payment Forms

- [ ] `autocomplete="cc-*"` attributes on all card fields
- [ ] `inputMode="numeric"` on number fields
- [ ] CSRF token included
- [ ] PCI DSS compliance (use Stripe/Braintree)
- [ ] No card data logged

### All Forms

- [ ] Input validation (client + server)
- [ ] Output encoding (XSS prevention)
- [ ] Error messages don't leak sensitive info
- [ ] Secure cookie settings
- [ ] CSP headers configured

## File Structure

```
form-security/
├── SKILL.md
├── references/
│   ├── autocomplete-spec.md    # Full autocomplete reference
│   └── csrf-patterns.md        # CSRF implementation patterns
└── scripts/
    ├── autocomplete-config.ts  # Autocomplete constants
    ├── csrf-token.ts           # CSRF token utilities
    ├── sanitize.ts             # Input sanitization
    └── secure-input.tsx        # Secure input components
```

## Reference

- `references/autocomplete-spec.md` — Complete autocomplete attribute reference
- `references/csrf-patterns.md` — CSRF implementation patterns
