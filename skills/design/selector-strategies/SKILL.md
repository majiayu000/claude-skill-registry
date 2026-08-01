---
name: selector-strategies
description: 'CSS/XPath selector best practices for web automation (dropdowns, dynamic
  tables, nested components). Use when: writing selectors, handling dynamic content,
  React apps, robust attributes, dynamic eleme'
---

---
name: selector-strategies
description: CSS/XPath selector best practices for web automation (dropdowns, dynamic tables, nested components). Use when: writing selectors, handling dynamic content, React apps, robust attributes, dynamic element handling, selector maintenance.
---

# Selector Strategies

Best practices for CSS and XPath selectors in RPA automation.

## Core Principles

1. **Prefer stable attributes**: `data-testid`, `aria-label`, `name` over classes/IDs
2. **Anchor to reliable parents**: Combine structural + semantic selectors
3. **Avoid brittle indices**: Never `nth-child`, `:first`, `[1]`
4. **Handle dynamic content**: Use text contains, partial matches, attributes
5. **Document intent**: Comment why selector was chosen

## Robust Attributes (Priority Order)

| Attribute | Stability | Notes |
|-----------|-----------|-------|
| `data-testid` | ★★★★★ | Made for testing, never changes for styling |
| `data-*` | ★★★★☆ | Custom data attributes are stable |
| `aria-label` | ★★★★☆ | Accessibility, rarely changes |
| `name` | ★★★★☆ | Form inputs, usually stable |
| `id` | ★★★☆☆ | Can be dynamic (e.g., `user-12345`) |
| `class` | ★★☆☆☆ | Often changes with CSS refactors |

## Selector Hierarchies

```
GOOD: Anchor → Semantic → Leaf
[data-testid="login-form"] → input[name="username"]

BAD: Deep chain of classes
div.container > div.row > div.col > input.form-control
```

## Dynamic Element Handling

| Pattern | CSS | XPath |
|---------|-----|-------|
| Text contains | `:has-text("Submit")` | `//*[contains(text(),"Submit")]` |
| Partial attr | `[href*="/products"]` | `//*[contains(@href,"/products")]` |
| Attr starts | `[id^="user-"]` | `//*[starts-with(@id,"user-")]` |
| Attr ends | `[class$="-active"]` | `//*[ends-with(@class,"-active")]` |
| Sibling | `h2 + p` | `//h2/following-sibling::p[1]` |

## Maintenance Tips

1. **Group selectors by feature**: Create selector constants per page/feature
2. **Version selectors**: Tag selectors with app version when known to break
3. **Fallback selectors**: Provide primary + backup for critical elements
4. **Wait strategies**: Combine selectors with proper wait conditions

## Anti-Patterns

```css
/* NEVER */
div:nth-child(3)           /* Brittle - breaks on DOM change */
.button:first             /* Fragile - assumes button order */
#react-root-12345         /* Dynamic ID - changes each render */
[class*="active"]         /* Too broad - matches multiple */
```

## Examples

See `examples/` folder for good/bad comparisons.

---

*Parent: [../_index.md](../_index.md)*
