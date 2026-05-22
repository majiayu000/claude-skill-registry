---
name: accessibility-patterns
description: Build inclusive web experiences following WCAG guidelines. Covers semantic HTML, ARIA, keyboard navigation, color contrast, and testing strategies. Triggers on accessibility, a11y, WCAG, screen readers, or inclusive design requests.
license: MIT
---

# Accessibility Patterns

Build for everyone from the start.

## Core Principles (POUR)

| Principle | Meaning | Example |
|-----------|---------|---------|
| **Perceivable** | Users can perceive content | Alt text, captions, contrast |
| **Operable** | Users can interact | Keyboard access, enough time |
| **Understandable** | Users can comprehend | Clear language, predictable |
| **Robust** | Works with assistive tech | Valid HTML, ARIA |

---

## WCAG Levels

| Level | Description | Target |
|-------|-------------|--------|
| A | Minimum | Must have |
| AA | Standard | Industry standard, legal requirement |
| AAA | Enhanced | Nice to have |

**Target Level AA** for most projects.

---

## Semantic HTML

### Use the Right Element

| Instead of | Use |
|------------|-----|
| `<div onclick>` | `<button>` |
| `<span class="link">` | `<a href>` |
| `<div class="header">` | `<header>` |
| `<div class="nav">` | `<nav>` |
| `<div class="main">` | `<main>` |
| `<b>` for emphasis | `<strong>` |
| `<i>` for emphasis | `<em>` |

### Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Descriptive Page Title</title>
</head>
<body>
  <a href="#main" class="skip-link">Skip to main content</a>
  
  <header>
    <nav aria-label="Main">
      <!-- navigation -->
    </nav>
  </header>
  
  <main id="main">
    <h1>Page Title</h1>
    <!-- Only one h1 per page -->
    
    <article>
      <h2>Section</h2>
      <h3>Subsection</h3>
    </article>
  </main>
  
  <aside aria-label="Related content">
    <!-- sidebar -->
  </aside>
  
  <footer>
    <!-- footer content -->
  </footer>
</body>
</html>
```

### Heading Hierarchy

```
h1 - Page title (one per page)
  h2 - Major sections
    h3 - Subsections
      h4 - Sub-subsections

Never skip levels (h1 → h3)
```

---

## Images & Media

### Alt Text

```html
<!-- Informative image -->
<img src="chart.png" alt="Bar chart showing sales increased 40% in Q4">

<!-- Decorative image -->
<img src="decorative-border.png" alt="" role="presentation">

<!-- Complex image -->
<figure>
  <img src="complex-diagram.png" alt="System architecture diagram">
  <figcaption>
    Detailed description of the system architecture...
  </figcaption>
</figure>

<!-- Image as link -->
<a href="/products">
  <img src="product.jpg" alt="View our products">
</a>
```

### Alt Text Guidelines

| Image Type | Alt Text Strategy |
|------------|-------------------|
| Informative | Describe content and function |
| Decorative | Empty alt="" |
| Functional | Describe the action |
| Complex | Brief alt + longer description |
| Text in image | Include all text |

### Video & Audio

```html
<!-- Video with captions -->
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="en" label="English">
  <track kind="descriptions" src="descriptions.vtt" srclang="en" label="Audio descriptions">
</video>

<!-- Audio with transcript -->
<audio controls>
  <source src="podcast.mp3" type="audio/mpeg">
</audio>
<a href="transcript.html">Read transcript</a>
```

---

## Forms

### Labels

```html
<!-- Explicit label (preferred) -->
<label for="email">Email address</label>
<input type="email" id="email" name="email">

<!-- Implicit label -->
<label>
  Email address
  <input type="email" name="email">
</label>

<!-- Required fields -->
<label for="name">
  Name <span aria-hidden="true">*</span>
  <span class="sr-only">(required)</span>
</label>
<input type="text" id="name" required aria-required="true">
```

### Error Handling

```html
<div role="alert" aria-live="polite">
  <p>Please fix the following errors:</p>
  <ul>
    <li><a href="#email">Email is required</a></li>
  </ul>
</div>

<label for="email">Email</label>
<input 
  type="email" 
  id="email" 
  aria-invalid="true"
  aria-describedby="email-error"
>
<span id="email-error" class="error">Please enter a valid email address</span>
```

### Form Groups

```html
<fieldset>
  <legend>Shipping Address</legend>
  
  <label for="street">Street</label>
  <input type="text" id="street">
  
  <label for="city">City</label>
  <input type="text" id="city">
</fieldset>
```

---

## Keyboard Navigation

### Focus Management

```css
/* Never remove focus outline without replacement */
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Custom focus style */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* Hide outline for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

### Tab Order

```html
<!-- Natural tab order follows DOM order -->
<!-- Use tabindex only when necessary -->

<button>First</button>
<button>Second</button>
<button>Third</button>

<!-- tabindex="0" - adds to tab order -->
<div tabindex="0" role="button">Custom interactive element</div>

<!-- tabindex="-1" - focusable via JS, not tab -->
<div tabindex="-1" id="modal">Modal content</div>

<!-- Never use tabindex > 0 -->
```

### Skip Links

```html
<a href="#main" class="skip-link">Skip to main content</a>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px;
  background: #000;
  color: #fff;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
</style>
```

### Keyboard Patterns

| Component | Keys |
|-----------|------|
| Buttons | Enter, Space |
| Links | Enter |
| Menus | Arrows, Enter, Escape |
| Tabs | Arrows, Tab |
| Modals | Tab (trapped), Escape to close |

---

## ARIA

### When to Use ARIA

1. First, use semantic HTML
2. Then, add ARIA if needed
3. "No ARIA is better than bad ARIA"

### Common ARIA Patterns

```html
<!-- Live regions (for dynamic content) -->
<div aria-live="polite">Content updates will be announced</div>
<div aria-live="assertive">Urgent updates interrupt</div>

<!-- Expanded/collapsed -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu" hidden>...</ul>

<!-- Current page -->
<nav>
  <a href="/" aria-current="page">Home</a>
  <a href="/about">About</a>
</nav>

<!-- Busy state -->
<div aria-busy="true">Loading...</div>

<!-- Hidden from AT -->
<span aria-hidden="true">👍</span>

<!-- Labels -->
<button aria-label="Close">×</button>
<nav aria-label="Main navigation">...</nav>
<section aria-labelledby="section-heading">
  <h2 id="section-heading">Section Title</h2>
</section>
```

### ARIA Roles

```html
<!-- Landmarks -->
<div role="banner">Header</div>
<div role="navigation">Nav</div>
<div role="main">Main</div>
<div role="complementary">Sidebar</div>
<div role="contentinfo">Footer</div>

<!-- Widgets -->
<div role="button">Custom button</div>
<div role="dialog" aria-modal="true">Modal</div>
<div role="tablist">Tabs</div>
<div role="alert">Error message</div>
```

---

## Color & Contrast

### Contrast Requirements

| Text Size | Level AA | Level AAA |
|-----------|----------|-----------|
| Normal text (<18px) | 4.5:1 | 7:1 |
| Large text (≥18px bold, ≥24px) | 3:1 | 4.5:1 |
| UI components | 3:1 | - |

### Color Independence

```html
<!-- Don't rely on color alone -->

<!-- Bad -->
<span style="color: red">Error</span>

<!-- Good -->
<span style="color: red">
  ⚠️ Error: <span class="error-text">Please enter a valid email</span>
</span>
```

### Testing Tools

- WebAIM Contrast Checker
- Chrome DevTools color picker
- Stark (Figma plugin)
- axe DevTools

---

## Testing

### Automated Testing

```javascript
// Using jest-axe
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('should have no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing Checklist

- [ ] Navigate entire page with keyboard only
- [ ] Test with screen reader (VoiceOver, NVDA)
- [ ] Check color contrast
- [ ] Zoom to 200% - still usable?
- [ ] Disable CSS - still understandable?
- [ ] Check all images have alt text
- [ ] Verify form labels and errors
- [ ] Test focus visibility
- [ ] Check heading structure

### Screen Reader Testing

| OS | Screen Reader | Browser |
|----|---------------|---------|
| macOS | VoiceOver | Safari |
| Windows | NVDA | Firefox |
| Windows | JAWS | Chrome |
| Mobile | TalkBack | Chrome |
| iOS | VoiceOver | Safari |

---

## Common Patterns

### Modal Dialog

```html
<div 
  role="dialog" 
  aria-modal="true" 
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-desc">Are you sure you want to proceed?</p>
  
  <button>Cancel</button>
  <button>Confirm</button>
</div>
```

Focus management:
1. Move focus to modal on open
2. Trap focus inside modal
3. Return focus to trigger on close

### Tabs

```html
<div role="tablist" aria-label="Settings">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">
    General
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">
    Security
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  General settings content
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Security settings content
</div>
```

---

## References

- `references/wcag-checklist.md` - Full WCAG 2.1 checklist
- `references/aria-patterns.md` - Common ARIA patterns
- `references/testing-tools.md` - Testing tool setup
