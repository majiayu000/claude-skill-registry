---
name: component-composition
description: Use when creating reusable components, component APIs, or complex hierarchies. Covers children, slots, compound components, render props.
versions:
  react: "19"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
related-skills: generating-components
---

# Component Composition

## Agent Workflow (MANDATORY)

Before implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Check existing composition patterns
2. **fuse-ai-pilot:research-expert** - React 19 composition patterns

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| Children | Simple containers | Low |
| Slots | Named regions | Medium |
| Compound | Related sub-components | Medium |
| Render Props | Custom rendering | High |

---

## Quick Reference

### Children Pattern

```tsx
function Card({ children }: { children: React.ReactNode }) {
  return <div className="bg-surface rounded-2xl p-6">{children}</div>;
}
```

### Slots Pattern

```tsx
function Card({ header, footer, children }: CardProps) {
  return (
    <div className="bg-surface rounded-2xl">
      {header && <div className="px-6 py-4 border-b">{header}</div>}
      <div className="p-6">{children}</div>
      {footer && <div className="px-6 py-4 border-t">{footer}</div>}
    </div>
  );
}
```

### Compound Components

```tsx
function Card({ children, variant }) {
  return (
    <CardContext.Provider value={{ variant }}>
      <div className="bg-surface rounded-2xl">{children}</div>
    </CardContext.Provider>
  );
}

Card.Header = ({ children }) => <div className="px-6 py-4">{children}</div>;
Card.Body = ({ children }) => <div className="p-6">{children}</div>;
Card.Footer = ({ children }) => <div className="px-6 py-4">{children}</div>;

// Usage
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
```

### Polymorphic Components

```tsx
function Button<T extends React.ElementType = "button">({
  as,
  children,
  ...props
}: ButtonProps<T>) {
  const Component = as || "button";
  return <Component className="btn" {...props}>{children}</Component>;
}

// Usage
<Button as="a" href="/link">Link</Button>
```

---

## Validation Checklist

```
[ ] Appropriate pattern for complexity
[ ] TypeScript props properly typed
[ ] displayName set on forwardRef
[ ] Max 2-3 composition levels
```

---

## Best Practices

### DO
- Use children for simple nesting
- Use slots for named regions (max 3-4)
- Forward refs for form elements
- Set displayName

### DON'T
- Over-engineer simple components
- Create deep nesting (max 2 levels)
- Forget TypeScript types
- Skip ref forwarding
