---
name: solid-core-jsx-attributes
description: "SolidJS advanced JSX attributes: @once for static values, attr:*/bool:*/prop:* for Web Components, textContent for text nodes, innerHTML for raw HTML."
---

# Advanced JSX Attributes

## @once

Compiler directive to prevent reactive wrapping for static values. Reduces overhead for values that never change.

```tsx
<MyComponent static={/*@once*/ state.wontUpdate} />
```

Works on children too:

```tsx
<MyComponent>{/*@once*/ state.wontUpdate}</MyComponent>
```

**When to use:**
- Values that are truly static
- Performance optimization for non-reactive props
- Compile-time optimization to reduce reactive overhead

## attr:*

Forces prop to be treated as an HTML attribute instead of a property. Essential for Web Components.

```tsx
<my-element attr:status={props.status} />
```

**Use case:** Web Components where you need to set attributes (not properties).

**Note:** Type definitions required when using TypeScript.

## bool:*

Controls presence of attribute based on truthy/falsy value. Most useful for Web Components.

```tsx
<my-element bool:status={prop.value} />
```

When `prop.value` is truthy:
```html
<my-element status />
```

When falsy:
```html
<my-element />
```

**Use case:** Conditional attributes for Web Components.

**Note:** Type definitions required when using TypeScript.

## prop:*

Forces prop to be treated as a DOM property instead of an attribute. For properties like `scrollTop`.

```tsx
<div prop:scrollTop={props.scrollPos} />
```

**Use case:** Setting DOM properties directly (e.g., `scrollTop`, custom properties).

**Note:** Type definitions required when using TypeScript.

## textContent

Sets the text content of an element. Replaces all child nodes with a single text node.

```tsx
<div textContent={message()} />
```

**Warning:** This replaces all children. Use carefully.

## innerHTML

Sets the HTML content directly. **Dangerous** - use only with sanitized content.

```tsx
<div innerHTML={sanitizedHtml()} />
```

**Security warning:**
- Only use with trusted, sanitized HTML
- Never use with user-generated content without sanitization
- Consider alternatives like `textContent` or structured JSX

## Best Practices

1. Use `@once` for truly static values to optimize performance
2. Use `attr:*`, `bool:*`, `prop:*` for Web Components integration
3. Use `textContent` only when you need to replace all children
4. Avoid `innerHTML` unless absolutely necessary and content is sanitized
5. Provide TypeScript definitions for custom attributes/properties
