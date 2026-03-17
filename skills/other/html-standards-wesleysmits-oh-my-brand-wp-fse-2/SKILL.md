---
name: html-standards
description: HTML standards for Oh My Brand! theme. Semantic elements, accessibility requirements, ARIA attributes, and attribute best practices. Use when writing HTML templates or render output.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# HTML Standards

HTML standards and accessibility requirements for the Oh My Brand! WordPress FSE theme.

---

## When to Use

- Writing block render templates (`render.php`)
- Creating HTML structure for Web Components
- Ensuring accessibility compliance
- Adding proper ARIA labels and attributes

---

## Reference Files

| File | Purpose |
|------|---------|
| [gallery-block.html](references/gallery-block.html) | Complete semantic structure example |
| [aria-patterns.html](references/aria-patterns.html) | Live regions, tabs, dialogs, expandable |
| [image-patterns.html](references/image-patterns.html) | Alt text, lazy loading, LCP optimization |
| [interactive-elements.html](references/interactive-elements.html) | Buttons, links, forms |

---

## Semantic Element Usage

| Element | Usage |
|---------|-------|
| `<article>` | Self-contained content (blocks, posts) |
| `<section>` | Thematic grouping of content |
| `<header>` | Introductory content or navigational aids |
| `<nav>` | Navigation links |
| `<main>` | Main content of the document |
| `<aside>` | Tangentially related content |
| `<footer>` | Footer of section or page |
| `<figure>` | Self-contained content like images |
| `<figcaption>` | Caption for a figure |
| `<details>` | Disclosure widget (expandable) |
| `<summary>` | Summary for details element |

---

## Heading Hierarchy

Maintain logical heading hierarchy (never skip levels):

```html
<!-- ✅ Correct hierarchy -->
<h1>Page Title</h1>
    <h2>Section Title</h2>
        <h3>Subsection Title</h3>

<!-- ❌ Skip levels -->
<h1>Page Title</h1>
    <h3>Missing h2!</h3>
```

---

## Image Attributes

| Attribute | Purpose |
|-----------|---------|
| `alt` | Alternative text for accessibility |
| `width` / `height` | Prevents layout shift (CLS) |
| `loading="lazy"` | Defers off-screen images |
| `loading="eager"` | First image (LCP optimization) |
| `decoding="async"` | Non-blocking decode |
| `fetchpriority="high"` | Prioritize LCP image |

See [image-patterns.html](references/image-patterns.html) for complete examples.

---

## Button Attributes

| Attribute | Purpose |
|-----------|---------|
| `type="button"` | Prevents form submission |
| `aria-label` | Accessible name when text insufficient |
| `aria-expanded` | Toggle state for expandable content |
| `aria-controls` | ID of controlled element |
| `disabled` | Disables interaction |

---

## Link Attributes

| Attribute | Purpose |
|-----------|---------|
| `target="_blank"` | Opens in new tab |
| `rel="noopener noreferrer"` | Security for new tab links |
| `download` | Triggers file download |

---

## ARIA Patterns

### Live Regions

| Attribute | When to Use |
|-----------|-------------|
| `aria-live="polite"` | Non-urgent updates (status messages) |
| `aria-live="assertive"` | Urgent updates (errors) |
| `role="alert"` | Error messages |
| `aria-atomic="true"` | Announce entire region |

### Expandable Content

| Attribute | Purpose |
|-----------|---------|
| `aria-expanded` | Current expanded state |
| `aria-controls` | ID of controlled panel |
| `hidden` | Hide collapsed content |

### Tabs

| Attribute | Purpose |
|-----------|---------|
| `role="tablist"` | Container for tabs |
| `role="tab"` | Individual tab button |
| `role="tabpanel"` | Tab content panel |
| `aria-selected` | Currently selected tab |
| `aria-controls` | Links tab to panel |
| `aria-labelledby` | Links panel to tab |

### Modal Dialog

| Attribute | Purpose |
|-----------|---------|
| `aria-labelledby` | Links to dialog title |
| `aria-describedby` | Links to description |
| `aria-modal="true"` | Indicates modal behavior |

See [aria-patterns.html](references/aria-patterns.html) for complete examples.

---

## Form Input Attributes

| Attribute | Purpose |
|-----------|---------|
| `type` | Input type (email, tel, url, etc.) |
| `id` | Links to label |
| `name` | Form data key |
| `required` | Required field |
| `autocomplete` | Autofill hint |
| `aria-describedby` | Links to description/error |
| `aria-invalid` | Invalid state |

---

## Related Skills

- [php-standards](../php-standards/SKILL.md) - PHP output escaping
- [css-standards](../css-standards/SKILL.md) - Accessibility styling
- [web-components](../web-components/SKILL.md) - Web Component HTML structure
- [native-block-development](../native-block-development/SKILL.md) - Block render templates

---

## References

- [MDN Web Docs: HTML elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
- [W3C WAI-ARIA Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM: Web Accessibility](https://webaim.org/)
