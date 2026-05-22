---
name: generic-static-code-reviewer
description: Review static site code for bugs, security issues, performance problems, accessibility gaps, and CLAUDE.md compliance. Enforces pure HTML/CSS/JS standards, minimal page weight, mobile-first design. Use when completing features, before commits, or reviewing changes.
---

# Static Site Code Reviewer

Review HTML/CSS/JS code against production quality standards.

**Extends:** [Generic Code Reviewer](../generic-code-reviewer/SKILL.md) - Read base skill for full code review methodology, P0/P1/P2 priority system, and judgment calls.

## Pre-Commit Checklist

```bash
# Local testing (cross-platform options)
python -m http.server 8000   # Windows
python3 -m http.server 8000  # macOS/Linux
npx serve .                  # Node.js (recommended - all platforms)

# Visual inspection
# - Test in Chrome, Firefox, Safari
# - Test at 375px, 768px, 1024px
# - Lighthouse audit
```

- [ ] Visual inspection passed
- [ ] Works in all major browsers
- [ ] Responsive at all breakpoints
- [ ] Lighthouse Performance 95+

## Static-Specific Checks

### No Build Tools Verification

Files should be served as-is:

- Pure `.html` files (no templating)
- Pure `.css` files (no Sass/Less)
- Pure `.js` files (no bundling/transpilation)
- No `node_modules` required for production

### Page Weight Targets (P1)

| Target                   | Max Size   |
| ------------------------ | ---------- |
| HTML                     | < 5KB      |
| CSS                      | < 10KB     |
| JavaScript               | < 5KB      |
| **Total (excl. images)** | **< 50KB** |
| Images (each)            | < 500KB    |

### HTML Quality

```html
<!-- Semantic structure -->
<header>
  <nav><a href="#">Link</a></nav>
</header>
<main>
  <article>
    <h1>Title</h1>
    <p>Content</p>
  </article>
</main>
<footer></footer>

<!-- Void elements (no closing slash needed in HTML5) -->
<img src="image.jpg" alt="Description" />
<br />
<input type="text" />
```

### CSS Quality

```css
/* CSS custom properties for theming */
:root {
  --bg-primary: #000000;
  --text-primary: #ffffff;
  --accent: #00ff00;
}

/* Mobile-first responsive */
.container {
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* Avoid !important - signals specificity problems */
```

### JavaScript Quality

```javascript
// ES6+ syntax (modern browsers support it)
const items = document.querySelectorAll(".item");
const handler = (e) => console.log(e.target);

// Event delegation (preferred)
document.body.addEventListener("click", (e) => {
  if (e.target.matches(".button")) {
    handleClick(e.target);
  }
});

// No jQuery dependencies
// No framework overhead
```

## Lighthouse Requirements (P1)

| Metric                 | Target |
| ---------------------- | ------ |
| Performance            | 95+    |
| Accessibility          | 90+    |
| Best Practices         | 100    |
| SEO                    | 100    |
| First Contentful Paint | < 1s   |

## See Also

- [Generic Code Reviewer](../generic-code-reviewer/SKILL.md) - Base methodology
- [Code Review Standards](../_shared/CODE_REVIEW_STANDARDS.md) - Full requirements
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - UI consistency
