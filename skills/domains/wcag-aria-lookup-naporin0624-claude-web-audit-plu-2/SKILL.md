---
name: wcag-aria-lookup
description: Looks up WCAG 2.1 AA criteria and WAI-ARIA patterns, returning official W3C URLs with concise summaries. Use when user asks about accessibility standards, WCAG criteria (e.g., "1.4.3", "contrast"), ARIA attributes (e.g., "aria-expanded", "role=dialog"), or accessible component patterns (e.g., "accessible tabs", "modal dialog a11y").
---

# WCAG & ARIA Lookup

Quick lookup for WCAG 2.1 AA criteria and WAI-ARIA patterns with official W3C references.

## Lookup Workflow

1. **Identify the query type**:
   - WCAG criterion (e.g., "contrast", "1.4.3", "keyboard")
   - ARIA attribute (e.g., "aria-expanded", "aria-live")
   - ARIA role (e.g., "role=dialog", "role=tablist")
   - Component pattern (e.g., "tabs", "modal", "accordion")

2. **Search the appropriate index**:
   - For WCAG: Read [wcag-index.json](wcag-index.json)
   - For ARIA: Read [aria-index.json](aria-index.json)

3. **Return results**:
   - Summary (1-2 sentences)
   - Official W3C URL
   - Quick reference URL (if available)

4. **For detailed implementation**:
   - Suggest fetching the official URL
   - Or reference WAI-ARIA Authoring Practices

## Response Format

When returning lookup results, use this format:

```
### [Criterion/Pattern Name]

**Summary**: [1-2 sentence explanation]

**Key Requirements**:
- [Requirement 1]
- [Requirement 2]

**Official Reference**: [URL]
**Quick Reference**: [URL] (if applicable)
```

## Quick Reference

### WCAG 2.1 AA - Most Common Issues

| ID | Name | Key Point |
|----|------|-----------|
| 1.1.1 | Non-text Content | All images need alt text |
| 1.4.3 | Contrast | 4.5:1 normal, 3:1 large text |
| 2.1.1 | Keyboard | All interactive elements keyboard accessible |
| 2.4.7 | Focus Visible | Focus indicator must be visible |
| 4.1.2 | Name, Role, Value | Custom widgets need ARIA |

### ARIA - First Rule

> Don't use ARIA if native HTML works.

```html
<!-- Prefer native HTML -->
<button>Submit</button>           <!-- Not: <div role="button"> -->
<input type="checkbox">           <!-- Not: <div role="checkbox"> -->
```

### Common ARIA Patterns

| Pattern | Key Roles | Key Attributes |
|---------|-----------|----------------|
| Dialog | `dialog` | `aria-modal`, `aria-labelledby` |
| Tabs | `tablist`, `tab`, `tabpanel` | `aria-selected`, `aria-controls` |
| Accordion | - | `aria-expanded`, `aria-controls` |
| Combobox | `combobox`, `listbox`, `option` | `aria-expanded`, `aria-activedescendant` |
| Menu | `menu`, `menuitem` | `aria-haspopup`, `aria-expanded` |

## Contrast Quick Check

| Text Type | Minimum Ratio | Example |
|-----------|---------------|---------|
| Normal text | 4.5:1 | `#595959` on `#fff` (7:1) |
| Large text (18pt/14pt bold) | 3:1 | `#767676` on `#fff` (4.5:1) |
| UI components | 3:1 | Button borders, form inputs |

## External Resources

- [WCAG 2.1 Full Spec](https://www.w3.org/TR/WCAG21/)
- [WCAG Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [Understanding WCAG](https://www.w3.org/WAI/WCAG21/Understanding/)
- [WAI-ARIA 1.2 Spec](https://www.w3.org/TR/wai-aria-1.2/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
