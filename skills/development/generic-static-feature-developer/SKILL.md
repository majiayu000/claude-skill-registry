---
name: generic-static-feature-developer
description: Guide feature development for static HTML/CSS/JS sites. Covers patterns, automation workflows, and content validation. Use when adding features, modifying automation, or planning changes.
---

# Static Site Feature Developer

Guide feature development for minimalist static sites.

**Extends:** [Generic Feature Developer](../generic-feature-developer/SKILL.md) - Read base skill for development workflow, scope assessment, and build vs integrate decisions.

## Static Site Architecture

### Typical Structure

```
project/
├── index.html          # Main page
├── style.css           # All styles
├── script.js           # All interactions
├── assets/             # Images, icons
├── .github/workflows/  # Automation (optional)
└── docs/               # Documentation
```

### No Build Tools Philosophy

Edit → Save → Deploy (that's it)

- Pure HTML (no templating engines)
- Pure CSS (no Sass/Less/PostCSS)
- Pure JS (no bundling, no transpilation)
- No `node_modules` in production

## Development Workflow

### Local Testing

```bash
# Start local server (cross-platform options)
python -m http.server 8000   # Windows
python3 -m http.server 8000  # macOS/Linux
npx serve .                  # Node.js (recommended - all platforms)
# Visit http://localhost:8000
```

### Before Committing

1. Test in Chrome, Firefox, Safari
2. Test at 375px, 768px, 1024px
3. Run Lighthouse audit
4. Screenshot current state (for comparison)

## Progressive Enhancement

### Philosophy

1. **Content first** - Works without CSS/JS
2. **Enhance with CSS** - Better styling for capable browsers
3. **Enhance with JS** - Interactivity for JS-enabled browsers

### Example Pattern

```html
<!-- Works without JS -->
<details>
  <summary>Menu</summary>
  <nav>
    <a href="#about">About</a>
    <a href="#contact">Contact</a>
  </nav>
</details>
```

```javascript
// Enhancement: Custom animation when JS available
if ("IntersectionObserver" in window) {
  // Progressive enhancement
}
```

## Vanilla JavaScript Patterns

### Event Delegation

```javascript
// One listener for many elements
document.body.addEventListener("click", (e) => {
  if (e.target.matches(".menu-toggle")) {
    toggleMenu();
  }
  if (e.target.matches(".close-btn")) {
    closeModal();
  }
});
```

### DOM Ready

```javascript
// Modern approach
document.addEventListener("DOMContentLoaded", () => {
  initApp();
});

// Or: script at end of body (no event needed)
```

### Class Toggling

```javascript
// Toggle visibility
element.classList.toggle("visible");

// Add/remove
element.classList.add("active");
element.classList.remove("active");
```

## Automation (GitHub Actions)

### Simple Deploy Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

### Image Optimization

```bash
# Optimize before committing
# PNG
pngquant --quality=65-80 image.png

# JPEG
jpegoptim --max=80 image.jpg

# WebP conversion
cwebp -q 80 image.png -o image.webp
```

## Feature Checklist

**Before Starting:**

- [ ] Read CLAUDE.md for project constraints
- [ ] Check existing patterns to reuse
- [ ] Understand performance budget

**During Development:**

- [ ] One change at a time
- [ ] Test in multiple browsers
- [ ] Test responsiveness
- [ ] Keep page weight in budget

**Before Completion:**

- [ ] Lighthouse 95+ Performance
- [ ] All breakpoints tested
- [ ] Screenshots for comparison
- [ ] Documentation updated

## Performance Targets

| Metric                 | Target |
| ---------------------- | ------ |
| Total weight           | < 50KB |
| First Contentful Paint | < 1s   |
| Lighthouse Performance | 95+    |

## See Also

- [Generic Feature Developer](../generic-feature-developer/SKILL.md) - Workflow, decisions
- [Code Review Standards](../_shared/CODE_REVIEW_STANDARDS.md) - Quality requirements
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - UI patterns
