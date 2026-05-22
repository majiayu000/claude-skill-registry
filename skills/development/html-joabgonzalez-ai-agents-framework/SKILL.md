---
name: html
description: Semantic HTML best practices for web development. Proper element usage, document structure, forms, metadata. Trigger: When writing HTML markup, creating document structure, or implementing semantic HTML elements.
skills:
  - conventions
  - a11y
  - humanizer
allowed-tools:
  - documentation-reader
  - web-search
---

# HTML Skill

## Overview

Guidance for writing semantic, accessible HTML following modern web standards.

## Objective

Enable developers to create properly structured HTML with semantic elements, accessibility attributes, and best practices.

---

## When to Use

Use this skill when:

- Writing HTML markup for web pages
- Creating document structure with semantic elements
- Building forms with proper labels and inputs
- Adding metadata and head elements
- Ensuring valid, semantic HTML

Don't use this skill for:

- React JSX patterns (use react skill)
- Accessibility specifics (use a11y skill for detailed guidance)

---

## Critical Patterns

### ✅ REQUIRED: Use Semantic Elements

```html
<!-- ✅ CORRECT: Semantic elements -->
<header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>
<main>
  <article>
    <h1>Title</h1>
    <p>Content</p>
  </article>
</main>
<footer>Footer content</footer>

<!-- ❌ WRONG: Generic divs -->
<div class="header">
  <div class="nav">...</div>
</div>
<div class="main">...</div>
```

### ✅ REQUIRED: Proper Heading Hierarchy

```html
<!-- ✅ CORRECT: Sequential hierarchy -->
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>

<!-- ❌ WRONG: Skipping levels -->
<h1>Page Title</h1>
<h4>Section</h4>
<!-- Skipped h2, h3 -->
```

### ✅ REQUIRED: Button vs Anchor

```html
<!-- ✅ CORRECT: Button for actions -->
<button type="button" onclick="doSomething()">Click</button>

<!-- ✅ CORRECT: Anchor for navigation -->
<a href="/page">Go to Page</a>

<!-- ❌ WRONG: Anchor for actions -->
<a href="#" onclick="doSomething()">Click</a>
```

### ✅ REQUIRED: Essential Meta Tags

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta
      name="description"
      content="Page description for SEO (150-160 chars)"
    />
    <title>Page Title - Site Name</title>

    <!-- Open Graph for social sharing -->
    <meta property="og:title" content="Page Title" />
    <meta property="og:description" content="Description for social sharing" />
    <meta property="og:image" content="https://example.com/image.jpg" />
    <meta property="og:url" content="https://example.com/page" />
    <meta property="og:type" content="website" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Page Title" />
    <meta name="twitter:description" content="Description" />
    <meta name="twitter:image" content="https://example.com/image.jpg" />
  </head>
  <body>
    <!-- Content -->
  </body>
</html>
```

---

## Conventions

Refer to conventions for:

- Code organization
- Documentation

Refer to a11y for:

- Semantic elements
- ARIA attributes
- Keyboard navigation

### HTML Specific

- Use semantic elements (`<nav>`, `<main>`, `<article>`)
- Maintain proper heading hierarchy
- Include alt text for images
- Use `<button>` for actions, `<a>` for navigation
- Validate HTML markup
- **Always set `lang` attribute on `<html>`**
- **Include essential meta tags** (viewport, description, charset)
- **Use Open Graph and Twitter Card meta tags** for social sharing
- **Ensure valid document structure** (one `<main>`, proper nesting)

---

## Decision Tree

**Interactive element?** → Use `<button>` for actions (submit, toggle), `<a>` for navigation (page links).

**Text content?** → Use semantic elements: `<article>` for content, `<section>` for grouped content, `<aside>` for related info.

**Form field?** → Wrap in `<label>`, associate with `htmlFor`/`id`, use appropriate `type` attribute.

**List of items?** → Use `<ul>` for unordered, `<ol>` for ordered, `<dl>` for definition lists.

**Heading?** → Use `<h1>` through `<h6>` in sequential order, one `<h1>` per page.

**Image?** → Use `<img>` with descriptive `alt` text, or empty `alt=""` for decorative images.

**Tabular data?** → Use `<table>` with `<thead>`, `<tbody>`, `<th>`, `<td>`, and `scope` attributes.

---

## Example

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Page Title</title>
  </head>
  <body>
    <header>
      <nav aria-label="Main navigation">
        <ul>
          <li><a href="/">Home</a></li>
        </ul>
      </nav>
    </header>
    <main>
      <article>
        <h1>Article Title</h1>
        <p>Content</p>
      </article>
    </main>
  </body>
</html>
```

---

## Edge Cases

**Multiple h1 elements:** HTML5 allows multiple `<h1>` tags, but screen readers work better with one per page.

**Empty links:** Avoid `<a href="#">` without purpose. Use `<button>` for actions or provide proper href.

**Div soup:** Overuse of `<div>` harms semantics. Use semantic elements first, div as last resort.

**Form without action:** Forms should have `action` attribute or JavaScript handler. Omitting both causes page reload.

**Button without type:** Default type is `submit`. Always specify `type="button"` for non-submit buttons.

---

## References

- https://html.spec.whatwg.org/
- https://web.dev/learn/html/
