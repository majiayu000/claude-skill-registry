---
name: accessibility-excellence
description: Master web accessibility (A11y) to ensure your product is usable by everyone, including people with disabilities. Covers WCAG standards, semantic HTML, keyboard navigation, screen readers, color contrast, and inclusive design practices. Accessibility is not a feature—it's a fundamental requirement.
---

# Accessibility Excellence

## Overview

Accessibility is the practice of making your product usable by everyone, including people with disabilities. It's not a feature to be added later—it's a fundamental requirement that should be built into every decision you make.

This skill teaches you to think about accessibility systematically: understanding WCAG standards, implementing semantic HTML, ensuring keyboard navigation, supporting screen readers, and designing inclusively.

## Core Philosophy: Accessibility is Inclusion

Accessibility benefits everyone, not just people with disabilities:

- **Captions** help people in noisy environments, not just deaf people
- **Keyboard navigation** helps people with motor disabilities, but also power users
- **Clear language** helps people with cognitive disabilities, but also non-native speakers
- **High contrast** helps people with low vision, but also people in bright sunlight
- **Transcripts** help deaf people, but also people who prefer reading

When you design for accessibility, you design for everyone.

## WCAG Standards

The Web Content Accessibility Guidelines (WCAG) define accessibility standards. There are three levels:

**WCAG 2.1 Levels:**
- **Level A** — Basic accessibility
- **Level AA** — Enhanced accessibility (recommended minimum)
- **Level AAA** — Advanced accessibility (ideal, but not always practical)

### The Four Principles (POUR)

**1. Perceivable**
Information must be perceivable to users. It can't be invisible to all senses.

**Guideline 1.1: Text Alternatives**
Provide text alternatives for all non-text content (images, videos, etc.).

```html
<!-- Good -->
<img src="chart.png" alt="Sales increased 25% in Q4" />

<!-- Bad -->
<img src="chart.png" alt="chart" />
<img src="chart.png" /> <!-- No alt text -->
```

**Guideline 1.4: Distinguishable**
Make it easy to see and hear content. Ensure sufficient contrast, readable text, and clear audio.

```css
/* Good - 4.5:1 contrast ratio (WCAG AA) */
color: #030712; /* dark text */
background-color: #F9FAFB; /* light background */

/* Bad - 2.5:1 contrast ratio (fails WCAG AA) */
color: #9CA3AF; /* medium gray text */
background-color: #F9FAFB; /* light background */
```

**2. Operable**
Users must be able to navigate and interact with your product. All functionality must be available from the keyboard.

**Guideline 2.1: Keyboard Accessible**
All functionality must be available from the keyboard.

```html
<!-- Good - keyboard accessible -->
<button onClick={handleClick}>Click Me</button>

<!-- Bad - not keyboard accessible -->
<div onClick={handleClick}>Click Me</div>

<!-- Good - keyboard accessible with proper focus management -->
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Click Me
</div>
```

**Guideline 2.4: Navigable**
Users must be able to navigate your product easily. Provide clear navigation, focus indicators, and skip links.

```html
<!-- Good - skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Good - clear heading structure -->
<h1>Page Title</h1>
<h2>Section 1</h2>
<h3>Subsection 1.1</h3>

<!-- Good - focus visible -->
<button style="outline: 2px solid #3B82F6; outline-offset: 2px;">
  Focused Button
</button>
```

**3. Understandable**
Users must be able to understand your content and how to use your product.

**Guideline 3.1: Readable**
Make text readable and understandable.

```html
<!-- Good - clear, simple language -->
<p>Save your document before closing.</p>

<!-- Bad - jargon, unclear -->
<p>Persist your artifact prior to terminating the session.</p>

<!-- Good - define abbreviations -->
<p>The <abbr title="World Wide Web Consortium">W3C</abbr> sets web standards.</p>
```

**Guideline 3.3: Predictable**
Make your product predictable. Users should know what will happen when they interact with it.

```html
<!-- Good - clear form labels -->
<label for="email">Email Address</label>
<input id="email" type="email" />

<!-- Bad - unclear labels -->
<input type="email" placeholder="Enter your email" />

<!-- Good - clear error messages -->
<input type="email" aria-invalid="true" />
<span role="alert">Please enter a valid email address.</span>

<!-- Bad - unclear error messages -->
<input type="email" style="border: 1px solid red;" />
```

**4. Robust**
Your product must be robust enough to be interpreted by a wide variety of assistive technologies.

**Guideline 4.1: Compatible**
Maximize compatibility with assistive technologies. Use semantic HTML and ARIA appropriately.

```html
<!-- Good - semantic HTML -->
<nav>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- Bad - non-semantic HTML -->
<div class="nav">
  <div class="nav-item"><span onclick="navigate('/')">Home</span></div>
  <div class="nav-item"><span onclick="navigate('/about')">About</span></div>
</div>

<!-- Good - ARIA for custom components -->
<div
  role="button"
  tabIndex={0}
  aria-pressed={isPressed}
  onClick={toggle}
  onKeyDown={(e) => e.key === 'Enter' && toggle()}
>
  Toggle
</div>
```

## Semantic HTML

Semantic HTML is the foundation of accessibility. Use HTML elements that describe their meaning, not just their appearance.

### Common Semantic Elements

| Element | Purpose | When to Use |
| :--- | :--- | :--- |
| `<header>` | Introductory content | Top of page or section |
| `<nav>` | Navigation links | Main navigation, breadcrumbs |
| `<main>` | Main content | Primary content area |
| `<article>` | Self-contained content | Blog posts, news articles |
| `<section>` | Thematic grouping | Chapters, sections of content |
| `<aside>` | Tangential content | Sidebars, related links |
| `<footer>` | Footer content | Bottom of page or section |
| `<h1>-<h6>` | Headings | Page structure and hierarchy |
| `<button>` | Clickable button | User actions |
| `<a>` | Link | Navigation |
| `<form>` | Form container | Data collection |
| `<label>` | Form label | Associate text with form input |
| `<input>` | Form input | User input |
| `<textarea>` | Multi-line text input | Longer text input |
| `<select>` | Dropdown menu | Option selection |

### Semantic HTML Example

```html
<!-- Good - semantic HTML -->
<body>
  <header>
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <h1>Article Title</h1>
      <p>Article content...</p>
    </article>

    <aside>
      <h2>Related Articles</h2>
      <ul>
        <li><a href="/article-1">Article 1</a></li>
        <li><a href="/article-2">Article 2</a></li>
      </ul>
    </aside>
  </main>

  <footer>
    <p>&copy; 2026 My Company</p>
  </footer>
</body>
```

## Keyboard Navigation

### Tab Order

Ensure a logical tab order through your page. By default, tab order follows the HTML source order.

```html
<!-- Good - logical tab order -->
<button>First</button>
<button>Second</button>
<button>Third</button>

<!-- Bad - illogical tab order (don't use tabindex > 0) -->
<button tabIndex={3}>Third</button>
<button tabIndex={1}>First</button>
<button tabIndex={2}>Second</button>

<!-- Good - skip interactive elements that aren't visible -->
<a href="#main-content" className="skip-link">Skip to main content</a>
<nav><!-- navigation --></nav>
<main id="main-content"><!-- main content --></main>
```

### Focus Management

Ensure focus is visible and managed appropriately:

```css
/* Good - visible focus indicator */
button:focus-visible {
  outline: 2px solid #3B82F6;
  outline-offset: 2px;
}

/* Bad - no focus indicator */
button:focus {
  outline: none;
}

/* Good - focus trap in modal */
const Modal = () => {
  const firstButtonRef = useRef(null);
  const lastButtonRef = useRef(null);

  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstButtonRef.current) {
        e.preventDefault();
        lastButtonRef.current?.focus();
      } else if (!e.shiftKey && document.activeElement === lastButtonRef.current) {
        e.preventDefault();
        firstButtonRef.current?.focus();
      }
    }
  };

  return (
    <div role="dialog" onKeyDown={handleKeyDown}>
      <button ref={firstButtonRef}>First</button>
      <button>Middle</button>
      <button ref={lastButtonRef}>Last</button>
    </div>
  );
};
```

### Keyboard Event Handling

Handle keyboard events appropriately:

```typescript
// Good - handle both click and keyboard
const Button = ({ onClick, children }) => {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClick?.();
    }
  };

  return (
    <button onClick={onClick} onKeyDown={handleKeyDown}>
      {children}
    </button>
  );
};

// Good - handle Escape key in modal
const Modal = ({ onClose }) => {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  return (
    <div role="dialog" onKeyDown={handleKeyDown}>
      {/* modal content */}
    </div>
  );
};
```

## Screen Reader Support

### ARIA (Accessible Rich Internet Applications)

ARIA provides additional semantic information for assistive technologies:

```html
<!-- Good - ARIA labels -->
<button aria-label="Close menu">×</button>

<!-- Good - ARIA live regions -->
<div aria-live="polite" aria-atomic="true">
  Item added to cart
</div>

<!-- Good - ARIA roles -->
<div role="alert">Error: Please fill in all required fields.</div>

<!-- Good - ARIA expanded -->
<button aria-expanded={isOpen} aria-controls="menu">
  Menu
</button>
<div id="menu" hidden={!isOpen}>
  {/* menu items */}
</div>

<!-- Good - ARIA current -->
<nav>
  <a href="/" aria-current="page">Home</a>
  <a href="/about">About</a>
</nav>
```

### Screen Reader Testing

Test with actual screen readers:

```html
<!-- Good - descriptive link text -->
<a href="/article">Read more about accessibility</a>

<!-- Bad - vague link text -->
<a href="/article">Read more</a>

<!-- Good - descriptive button text -->
<button>Delete account</button>

<!-- Bad - vague button text -->
<button>Delete</button>

<!-- Good - form labels associated with inputs -->
<label for="email">Email Address</label>
<input id="email" type="email" />

<!-- Bad - unassociated labels -->
<label>Email Address</label>
<input type="email" />
```

## Color Contrast

### Contrast Ratios

Ensure sufficient contrast between text and background:

```css
/* WCAG AA - Normal text (4.5:1) */
color: #030712; /* dark text */
background-color: #F9FAFB; /* light background */
/* Contrast ratio: 19:1 ✓ */

/* WCAG AA - Large text (3:1) */
color: #4B5563; /* medium gray text */
background-color: #F9FAFB; /* light background */
/* Contrast ratio: 6.5:1 ✓ */

/* WCAG AAA - Normal text (7:1) */
color: #030712; /* dark text */
background-color: #F9FAFB; /* light background */
/* Contrast ratio: 19:1 ✓ */

/* Fails WCAG AA */
color: #9CA3AF; /* light gray text */
background-color: #F9FAFB; /* light background */
/* Contrast ratio: 2.5:1 ✗ */
```

### Testing Contrast

Use tools like WebAIM Contrast Checker or Polished:

```javascript
import { readableColor } from 'polished';

const backgroundColor = '#3B82F6';
const textColor = readableColor(backgroundColor); // Returns #FFFFFF or #000000
```

## Inclusive Design Practices

### 1. Don't Rely on Color Alone

Use patterns, icons, or text labels in addition to color:

```html
<!-- Good - color + icon + text -->
<span style="color: green;">
  <CheckIcon />
  Success
</span>

<!-- Bad - color alone -->
<span style="color: green;">Success</span>

<!-- Good - color + pattern -->
<div style="background: repeating-linear-gradient(45deg, #3B82F6, #3B82F6 10px, #2563EB 10px, #2563EB 20px);">
  Pattern
</div>

<!-- Bad - color alone -->
<div style="background-color: #3B82F6;">Color</div>
```

### 2. Provide Alternatives for Images

```html
<!-- Good - descriptive alt text -->
<img src="chart.png" alt="Sales increased 25% in Q4 2025" />

<!-- Bad - no alt text -->
<img src="chart.png" />

<!-- Good - alt text for decorative images -->
<img src="decoration.png" alt="" />

<!-- Good - long description for complex images -->
<img src="complex-chart.png" alt="Chart showing sales trends" />
<a href="/chart-description">View detailed chart description</a>
```

### 3. Provide Captions and Transcripts

```html
<!-- Good - captions for video -->
<video controls>
  <source src="video.mp4" type="video/mp4" />
  <track kind="captions" src="captions.vtt" srclang="en" label="English" />
</video>

<!-- Good - transcript for audio -->
<audio controls>
  <source src="audio.mp3" type="audio/mpeg" />
</audio>
<p><a href="/audio-transcript">Read transcript</a></p>
```

### 4. Design for Readability

```css
/* Good - readable font size */
body {
  font-size: 16px;
  line-height: 1.6;
}

/* Good - readable line length */
main {
  max-width: 65ch;
}

/* Good - sufficient whitespace */
section {
  padding: 2rem;
}

/* Bad - too small */
body {
  font-size: 12px;
  line-height: 1.2;
}
```

## How to Use This Skill with Claude Code

### Audit Accessibility

```
"I'm using the accessibility-excellence skill. Can you audit my product for accessibility?
- Check WCAG AA compliance
- Identify keyboard navigation issues
- Check screen reader compatibility
- Verify color contrast ratios
- Check for missing alt text
- Identify semantic HTML issues"
```

### Implement Accessibility

```
"Can you help me implement accessibility?
- Add semantic HTML
- Add ARIA labels and roles
- Implement keyboard navigation
- Ensure focus management
- Verify color contrast
- Add alt text to images"
```

### Create Accessibility Documentation

```
"Can you create accessibility documentation?
- WCAG AA checklist
- Keyboard navigation guide
- Screen reader testing guide
- Color contrast requirements
- Accessibility best practices"
```

### Test Accessibility

```
"Can you create an accessibility testing plan?
- Keyboard navigation testing
- Screen reader testing
- Color contrast verification
- Semantic HTML validation
- ARIA usage validation"
```

## Design Critique: Evaluating Accessibility

Claude Code can critique your accessibility:

```
"Can you evaluate my accessibility?
- Are my pages WCAG AA compliant?
- Is keyboard navigation working?
- Are my color contrasts sufficient?
- Is my semantic HTML correct?
- What's one thing I could improve immediately?"
```

## Integration with Other Skills

- **design-foundation** — Accessible tokens and design decisions
- **layout-system** — Accessible layouts and responsive design
- **typography-system** — Readable font sizes and line heights
- **color-system** — Sufficient contrast ratios
- **component-architecture** — Accessible components
- **interaction-design** — Accessible interactions

## Key Principles

**1. Accessibility is Inclusion**
Design for everyone, including people with disabilities.

**2. Semantic HTML is Foundation**
Use semantic HTML elements that describe their meaning.

**3. Keyboard Navigation is Essential**
All functionality must be available from the keyboard.

**4. Screen Readers Must Work**
Test with actual screen readers, not just automated tools.

**5. Contrast Matters**
Ensure sufficient contrast for readability.

## Checklist: Is Your Accessibility Ready?

- [ ] All pages are WCAG AA compliant
- [ ] Semantic HTML is used throughout
- [ ] Keyboard navigation works for all functionality
- [ ] Focus indicators are visible
- [ ] All images have descriptive alt text
- [ ] Form labels are associated with inputs
- [ ] Color contrast meets WCAG AA standards
- [ ] ARIA is used appropriately
- [ ] Screen reader testing has been done
- [ ] Videos have captions and transcripts
- [ ] Reduced motion preferences are respected
- [ ] Accessibility is tested regularly

Accessibility is not a feature—it's a fundamental requirement. Make it a priority.
