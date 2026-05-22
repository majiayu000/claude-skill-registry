---
name: accessibility-wcag
description: Build accessible web applications following WCAG 2.1/2.2 guidelines with proper semantic HTML, ARIA attributes, keyboard navigation, screen reader support, and inclusive design. Use when implementing ARIA labels and roles, ensuring keyboard navigation, supporting screen readers, providing text alternatives for images, managing focus, creating accessible forms, building inclusive UI components, testing with accessibility tools, meeting WCAG compliance levels, or designing for users with disabilities.
---

# Accessibility (WCAG) - Building Inclusive Web Applications

## When to use this skill

- Implementing ARIA labels, roles, and properties
- Ensuring full keyboard navigation support
- Supporting screen readers (NVDA, JAWS, VoiceOver)
- Providing text alternatives for images and media
- Managing focus and focus indicators
- Creating accessible forms with proper labels
- Building inclusive, usable UI components
- Testing with axe DevTools or similar tools
- Meeting WCAG 2.1/2.2 AA or AAA compliance
- Designing for color blindness and low vision
- Implementing skip links and landmarks
- Ensuring sufficient color contrast ratios

## When to use this skill

- Designing UIs, implementing components, ensuring compliance with accessibility standards (WCAG 2.1/2.2).
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Designing UIs, implementing components, ensuring compliance with accessibility standards (WCAG 2.1/2.2).

## Core Principles (POUR)

1. **Perceivable** - Information available to all senses
2. **Operable** - Interface elements functional for all users
3. **Understandable** - Content and interface are clear
4. **Robust** - Works across technologies including assistive devices

## Essential Patterns

### Semantic HTML
```html
<!-- ✅ Proper semantic structure -->
<header><nav><ul><li><a></a></li></ul></nav></header>
<main><article><h1></h1><p></p></article></main>
<footer></footer>

<!-- ❌ Div soup -->
<div class="header"><div class="nav"></div></div>
```

### ARIA Labels & Roles
```html
<button aria-label="Close dialog">×</button>
<nav aria-label="Main navigation"></nav>
<input aria-describedby="email-error" />
<div role="alert" aria-live="polite">Success</div>
```

### Keyboard Navigation
```typescript
function Modal({ onClose }: { onClose: () => void }) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);
  
  return <div role="dialog" aria-modal="true" tabIndex={-1}>...</div>;
}
```

### Focus Management
```typescript
const firstFocusableElement = dialogRef.current?.querySelectorAll(
  'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
)[0];
firstFocusableElement?.focus();
```

## Resources
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [axe DevTools](https://www.deque.com/axe/devtools/)
