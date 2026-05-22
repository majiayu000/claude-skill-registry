---
name: xss-prevention
description: XSS attack prevention with input sanitization, output encoding, Content Security Policy. Use for user-generated content, rich text editors, web application security, or encountering stored XSS, reflected XSS, DOM manipulation, script injection errors.

  Keywords: sanitization, HTML-encoding, DOMPurify, CSP, Content-Security-Policy, rich-text-editor, user-input, escaping, innerHTML, DOM-manipulation, stored-XSS, reflected-XSS, input-validation, output-encoding, trusted-types, XSS-attacks, web-security, user-generated-content, secure-coding, script-injection, DOM-based-XSS
license: MIT
---

# XSS Prevention

## Overview

Implement comprehensive Cross-Site Scripting attack prevention through input sanitization, output encoding, Content Security Policy headers, and secure coding practices.

## When to Use

- User-generated content display
- Rich text editors
- Comment systems
- Search functionality
- Dynamic HTML generation
- Template rendering scenarios

## XSS Attack Types

| Type | Vector | Defense |
|------|--------|---------|
| Reflected | URL parameters | Output encoding |
| Stored | Database content | Input sanitization |
| DOM-based | Client-side JS | Safe DOM APIs |
| Mutation | HTML parser quirks | Strict sanitization |

## Output Encoding (Node.js)

```javascript
function encodeHTML(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

function encodeForAttribute(str) {
  return str.replace(/[^\w.-]/g, char =>
    `&#x${char.charCodeAt(0).toString(16)};`
  );
}

// Usage in templates
app.get('/profile', (req, res) => {
  const username = encodeHTML(req.query.name);
  res.send(`<h1>Welcome, ${username}</h1>`);
});
```

## DOMPurify Sanitization

```javascript
import DOMPurify from 'dompurify';

const config = {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
  ALLOWED_ATTR: ['href', 'title'],
  ALLOW_DATA_ATTR: false
};

function sanitizeHTML(dirty) {
  return DOMPurify.sanitize(dirty, config);
}

// React component
function RichContent({ html }) {
  return (
    <div dangerouslySetInnerHTML={{ __html: sanitizeHTML(html) }} />
  );
}
```

## Content Security Policy

```javascript
// Express middleware
app.use((req, res, next) => {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.locals.nonce = nonce;

  res.setHeader('Content-Security-Policy', [
    "default-src 'self'",
    `script-src 'self' 'nonce-${nonce}'`,
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "connect-src 'self' https://api.example.com",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "form-action 'self'"
  ].join('; '));

  next();
});
```

## Safe DOM APIs

```javascript
// DANGEROUS - avoid these
element.innerHTML = userInput;        // XSS risk
element.outerHTML = userInput;        // XSS risk
document.write(userInput);            // XSS risk
eval(userInput);                      // Code injection

// SAFE - use these instead
element.textContent = userInput;      // Escaped automatically
element.setAttribute('data-id', id);  // Safe for attributes
document.createTextNode(userInput);   // Creates safe text node
```

## URL Validation

```javascript
function isSafeURL(url) {
  try {
    const parsed = new URL(url);
    return ['http:', 'https:'].includes(parsed.protocol);
  } catch {
    return false;
  }
}

// Usage
const href = isSafeURL(userURL) ? userURL : '#';
```

## Context-Specific Encoding

Different contexts require different encoding approaches:

- **HTML Entity Encoding**: Safest option for text content
- **Attribute Encoding**: For HTML attributes
- **JavaScript Escaping**: For script contexts
- **URL Encoding**: For URL parameters
- **CSS Escaping**: For stylesheet contexts

Always encode output by the specific context where data will be rendered.

## Additional Implementations

See [references/python-sanitization.md](references/python-sanitization.md) for:
- Python bleach library usage
- Flask/Django template escaping
- Server-side validation patterns

See [references/nodejs-advanced.md](references/nodejs-advanced.md) for:
- Complete XSSPrevention class with all methods
- Express middleware (xssProtection)
- React components (SafeText, SafeHTML, SafeLink, useSanitizedInput)
- Helmet CSP configuration

## Best Practices

**✅ DO:**
- Encode output by default
- Use templating engines with auto-escaping
- Implement CSP headers
- Sanitize rich content with allowlists
- Validate URLs with protocol whitelisting
- Use HTTPOnly cookies
- Conduct regular security testing
- Leverage secure frameworks

**❌ DON'T:**
- Trust user input
- Use unsafe functions (eval, innerHTML)
- Disable security features for convenience
- Rely solely on client-side validation
- Use blocklists instead of allowlists
- Skip context-specific encoding
- Allow arbitrary script execution

## Security Checklist

- [ ] Encode all output by context (HTML, attribute, JS)
- [ ] Sanitize HTML with allowlist (not blocklist)
- [ ] Implement strict CSP headers
- [ ] Use HTTPOnly cookies for sessions
- [ ] Validate and sanitize URLs
- [ ] Avoid innerHTML with user content
- [ ] Regular security testing

## Resources

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [DOMPurify Documentation](https://github.com/cure53/DOMPurify)
- [Content Security Policy Reference](https://content-security-policy.com/)
- [Web Security by Mozilla](https://developer.mozilla.org/en-US/docs/Web/Security)
