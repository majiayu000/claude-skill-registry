---
name: accessibility-audit
description: WCAG compliance checking and accessibility improvements. Use for auditing websites, fixing a11y issues, and implementing inclusive design.
---

# ♿ Accessibility Audit Skill

## WCAG 2.1 Principles (POUR)

| Principle | Description |
|-----------|-------------|
| **P**erceivable | Content viewable by all users |
| **O**perable | Interface usable by all users |
| **U**nderstandable | Clear and predictable |
| **R**obust | Works with assistive tech |

---

## Common Issues & Fixes

### Images
```html
<!-- Bad ❌ -->
<img src="logo.png">

<!-- Good ✅ -->
<img src="logo.png" alt="Company Logo">

<!-- Decorative (empty alt) -->
<img src="divider.png" alt="">
```

### Forms
```html
<!-- Bad ❌ -->
<input type="text" placeholder="Email">

<!-- Good ✅ -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email" required>
```

### Buttons
```html
<!-- Bad ❌ -->
<div onclick="submit()">Submit</div>

<!-- Good ✅ -->
<button type="submit">Submit</button>
```

### Links
```html
<!-- Bad ❌ -->
<a href="#">Click here</a>

<!-- Good ✅ -->
<a href="/products">View all products</a>
```

---

## Color Contrast

| Level | Ratio | Use For |
|-------|-------|---------|
| AA Normal | 4.5:1 | Regular text |
| AA Large | 3:1 | 18pt+ or 14pt bold |
| AAA Normal | 7:1 | Enhanced accessibility |

### CSS Example
```css
/* Good contrast */
.text {
  color: #1e293b;        /* Dark gray */
  background: #ffffff;   /* White */
  /* Contrast ratio: 13.5:1 ✅ */
}

/* Bad contrast */
.text {
  color: #94a3b8;        /* Light gray */
  background: #ffffff;   /* White */
  /* Contrast ratio: 2.8:1 ❌ */
}
```

---

## Keyboard Navigation

```javascript
// Focus management
element.focus();
element.blur();

// Focus trap for modals
const focusableElements = modal.querySelectorAll(
  'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
);
```

---

## Screen Reader Support

```html
<!-- Live regions for dynamic content -->
<div aria-live="polite" aria-atomic="true">
  Status: Loading...
</div>

<!-- Hidden visually but readable -->
<span class="sr-only">Opens in new tab</span>
```

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
```

---

## Audit Tools

```bash
# Lighthouse CLI
npx lighthouse https://example.com --view

# axe-core
npm install axe-core
```

## Checklist

- [ ] All images have alt text
- [ ] Color contrast meets WCAG AA
- [ ] All forms have labels
- [ ] Site navigable by keyboard
- [ ] Focus indicators visible
- [ ] ARIA used appropriately
- [ ] Tested with screen reader
