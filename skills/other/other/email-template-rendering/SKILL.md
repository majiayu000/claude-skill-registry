---
name: email-template-rendering
description: |
  Fix for Handlebars email template rendering issues in the notifications app.
  Use when: "Missing helper", template variables not rendering, partials not found,
  HTML escaping issues in emails. Only loads when working in apps/notifications/.
author: Memory Forge
version: 1.0.0
date: 2025-01-28
---

# Email Template Rendering Fixes

## Problem

Handlebars templates for email notifications fail to render correctly, showing raw variables, missing helpers, or escaped HTML.

## Trigger Conditions

- Error: `Missing helper: "formatDate"`
- Variables showing as `{{variable}}` in sent emails
- Error: `The partial X could not be found`
- HTML appearing escaped (`&lt;div&gt;` instead of `<div>`)
- Working in `apps/notifications/` directory

## Solution

### Issue 1: Missing Helpers

Register custom helpers before compiling templates:

```typescript
import Handlebars from 'handlebars';

// Register helpers BEFORE compiling templates
Handlebars.registerHelper('formatDate', (date: Date, format: string) => {
  return dayjs(date).format(format);
});

Handlebars.registerHelper('formatCurrency', (amount: number, currency: string) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency || 'USD',
  }).format(amount);
});

// Now compile
const template = Handlebars.compile(templateSource);
```

### Issue 2: HTML Escaping

Use triple braces for unescaped HTML:

```handlebars
{{! WRONG - HTML will be escaped }}
<div>{{htmlContent}}</div>

{{! CORRECT - HTML renders as-is }}
<div>{{{htmlContent}}}</div>
```

Or use `SafeString` in helpers:

```typescript
Handlebars.registerHelper('renderHtml', (html: string) => {
  return new Handlebars.SafeString(html);
});
```

### Issue 3: Partials Not Found

Register partials before use:

```typescript
// Register partial
Handlebars.registerPartial('header', headerTemplateSource);
Handlebars.registerPartial('footer', footerTemplateSource);

// Use in template
// {{> header}}
// ... content ...
// {{> footer}}
```

### Issue 4: Async Data in Templates

Handlebars is synchronous. Resolve all data before rendering:

```typescript
// WRONG
const template = Handlebars.compile(source);
const html = template({ user: await getUser() }); // ❌ Promise in template

// CORRECT
const user = await getUser();
const orders = await getOrders(user.id);
const template = Handlebars.compile(source);
const html = template({ user, orders }); // ✅ Resolved data
```

## Verification

1. Compile template without errors
2. Render with sample data
3. Check output HTML is correct
4. Send test email and verify in email client

## Notes

- This skill only loads when working in `apps/notifications/`
- Always precompile templates in production for performance
- Test emails in multiple clients (Gmail, Outlook, Apple Mail)
- Use inline CSS for email compatibility
