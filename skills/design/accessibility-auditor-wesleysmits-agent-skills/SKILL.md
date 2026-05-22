---
name: auditing-accessibility-wcag
description: Checks components and pages for WCAG 2.1 accessibility violations. Use when the user asks about a11y, WCAG compliance, screen readers, aria labels, keyboard navigation, or accessible patterns.
---

# Accessibility Auditor (WCAG 2.1)

## When to use this skill

- User asks about accessibility or a11y
- User mentions WCAG or compliance levels
- User wants to audit a component or page
- User asks about aria labels or roles
- User needs accessible alternative patterns

## Workflow

- [ ] Identify scope (component, page, site)
- [ ] Run automated audits
- [ ] Review manual checkpoints
- [ ] Categorize violations by severity
- [ ] Provide remediation examples
- [ ] Validate fixes

## Instructions

### Step 1: Run Automated Audits

**axe-core (CLI):**

```bash
npm install -D @axe-core/cli
npx axe http://localhost:3000 --exit
```

**Lighthouse accessibility audit:**

```bash
npx lighthouse http://localhost:3000 --only-categories=accessibility --output=json
```

**ESLint accessibility plugin:**

```bash
npm install -D eslint-plugin-jsx-a11y
```

```javascript
// eslint.config.js
import jsxA11y from "eslint-plugin-jsx-a11y";

export default [jsxA11y.flatConfigs.recommended];
```

### Step 2: WCAG 2.1 AA Checklist

| Principle      | Guideline             | Common Issues               |
| -------------- | --------------------- | --------------------------- |
| Perceivable    | 1.1 Text Alternatives | Missing alt text            |
| Perceivable    | 1.3 Adaptable         | Improper heading order      |
| Perceivable    | 1.4 Distinguishable   | Low color contrast          |
| Operable       | 2.1 Keyboard          | No focus styles             |
| Operable       | 2.4 Navigable         | Missing skip links          |
| Understandable | 3.1 Readable          | Missing lang attribute      |
| Understandable | 3.2 Predictable       | Unexpected focus changes    |
| Robust         | 4.1 Compatible        | Invalid HTML, missing roles |

### Step 3: Common Violations & Fixes

**Missing alt text:**

```tsx
// ❌ Violation
<img src="/hero.jpg" />

// ✅ Fixed - Informative image
<img src="/hero.jpg" alt="Team collaborating in modern office" />

// ✅ Fixed - Decorative image
<img src="/divider.svg" alt="" role="presentation" />
```

**Low color contrast (4.5:1 minimum for AA):**

```css
/* ❌ Violation - 2.5:1 ratio */
.text-muted {
  color: #999999;
  background: #ffffff;
}

/* ✅ Fixed - 4.6:1 ratio */
.text-muted {
  color: #767676;
  background: #ffffff;
}
```

**Missing form labels:**

```tsx
// ❌ Violation
<input type="email" placeholder="Email" />

// ✅ Fixed - Visible label
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// ✅ Fixed - Visually hidden label
<label htmlFor="email" className="sr-only">Email</label>
<input id="email" type="email" placeholder="Email" />
```

**Missing focus indicators:**

```css
/* ❌ Violation */
button:focus {
  outline: none;
}

/* ✅ Fixed */
button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

**Improper heading hierarchy:**

```tsx
// ❌ Violation - Skips h2
<h1>Page Title</h1>
<h3>Section Title</h3>

// ✅ Fixed
<h1>Page Title</h1>
<h2>Section Title</h2>
```

**Non-semantic buttons:**

```tsx
// ❌ Violation
<div onClick={handleClick}>Click me</div>

// ✅ Fixed
<button type="button" onClick={handleClick}>Click me</button>
```

**Missing skip link:**

```tsx
// ✅ Add at top of page
<a href="#main-content" className="skip-link">
  Skip to main content
</a>

// ... header/nav ...

<main id="main-content">
  {/* Page content */}
</main>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
  z-index: 999;
  padding: 1rem;
  background: var(--color-background);
  color: var(--color-text);
}

.skip-link:focus {
  left: 1rem;
  top: 1rem;
}
```

### Step 4: Interactive Component Patterns

**Accessible modal:**

```tsx
import { useEffect, useRef } from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      closeButtonRef.current?.focus();
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  // Trap focus inside modal
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") onClose();
    if (e.key === "Tab") {
      const focusable = modalRef.current?.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
      );
      if (!focusable?.length) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      ref={modalRef}
      onKeyDown={handleKeyDown}
    >
      <div className="modal-backdrop" onClick={onClose} aria-hidden="true" />
      <div className="modal-content">
        <h2 id="modal-title">{title}</h2>
        {children}
        <button ref={closeButtonRef} onClick={onClose} aria-label="Close modal">
          ×
        </button>
      </div>
    </div>
  );
}
```

**Accessible dropdown menu:**

```tsx
import { useState, useRef } from "react";

export function Dropdown({ label, items }: { label: string; items: string[] }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setActiveIndex((i) => Math.min(i + 1, items.length - 1));
        break;
      case "ArrowUp":
        e.preventDefault();
        setActiveIndex((i) => Math.max(i - 1, 0));
        break;
      case "Escape":
        setIsOpen(false);
        buttonRef.current?.focus();
        break;
      case "Enter":
      case " ":
        if (!isOpen) {
          setIsOpen(true);
          setActiveIndex(0);
        }
        break;
    }
  };

  return (
    <div onKeyDown={handleKeyDown}>
      <button
        ref={buttonRef}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        onClick={() => setIsOpen(!isOpen)}
      >
        {label}
      </button>
      {isOpen && (
        <ul role="listbox" aria-activedescendant={`item-${activeIndex}`}>
          {items.map((item, i) => (
            <li
              key={item}
              id={`item-${i}`}
              role="option"
              aria-selected={i === activeIndex}
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Step 5: Testing Tools

**Screen reader testing:**

- macOS: VoiceOver (Cmd+F5)
- Windows: NVDA (free) or JAWS
- Browser: ChromeVox extension

**Browser extensions:**

- axe DevTools
- WAVE Evaluation Tool
- Accessibility Insights

**Keyboard testing checklist:**

- [ ] All interactive elements reachable via Tab
- [ ] Focus order matches visual order
- [ ] Focus visible on all elements
- [ ] Escape closes modals/dropdowns
- [ ] Arrow keys navigate within components

### Step 6: Audit Report Template

```markdown
## Accessibility Audit Report

**URL**: https://example.com
**Date**: 2026-01-18
**Standard**: WCAG 2.1 AA
**Tools**: axe-core, Lighthouse, manual testing

### Summary

| Severity | Count |
| -------- | ----- |
| Critical | 2     |
| Serious  | 5     |
| Moderate | 8     |
| Minor    | 3     |

### Critical Issues

#### 1. Images missing alt text

- **WCAG**: 1.1.1 Non-text Content
- **Location**: Homepage hero, product cards
- **Impact**: Screen reader users cannot understand image content
- **Fix**: Add descriptive alt text to all informative images

#### 2. Form inputs missing labels

- **WCAG**: 1.3.1 Info and Relationships
- **Location**: Contact form, search box
- **Impact**: Users cannot identify form field purpose
- **Fix**: Associate `<label>` with each input via `for`/`id`

### Recommendations

1. Add eslint-plugin-jsx-a11y to catch issues during development
2. Include accessibility testing in CI pipeline
3. Train team on keyboard navigation testing
```

## Validation

Before completing:

- [ ] axe-core reports zero violations
- [ ] Lighthouse accessibility score ≥ 90
- [ ] Keyboard navigation works throughout
- [ ] Screen reader announces content correctly
- [ ] Color contrast meets 4.5:1 (text) / 3:1 (large text)
- [ ] Focus is visible on all interactive elements

## Error Handling

- **False positives**: Some automated tools flag valid patterns; verify manually.
- **Dynamic content**: Re-run audits after JavaScript loads; use axe-core in tests.
- **Third-party widgets**: Document inaccessible third-party components for vendor follow-up.
- **Complex widgets**: Reference WAI-ARIA Authoring Practices for correct patterns.

## Resources

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [axe-core Rules](https://dequeuniversity.com/rules/axe/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
