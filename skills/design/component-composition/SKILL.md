---
name: component-composition
description: Component composition patterns with nesting, slots, compound components, and render props. Use when creating reusable components, component APIs, or complex component hierarchies.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Component Composition

Advanced composition patterns for scalable components.

## Agent Workflow (MANDATORY)

Before implementation:
1. **fuse-ai-pilot:explore-codebase** - Check existing composition patterns
2. **fuse-ai-pilot:research-expert** - React 19 composition patterns

After: Run **fuse-ai-pilot:sniper** for validation.

## Pattern Overview

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| Children | Simple containers | Low |
| Slots | Named regions | Medium |
| Compound | Related sub-components | Medium |
| Render Props | Custom rendering | High |
| Context | Shared state | High |

## 1. Children Pattern (Basic)

```tsx
function Card({ children, className }: { children: React.ReactNode }) {
  return (
    <div className={cn("bg-surface rounded-2xl p-6", className)}>
      {children}
    </div>
  );
}

// Usage
<Card>
  <h2>Title</h2>
  <p>Content</p>
</Card>
```

## 2. Slots Pattern

```tsx
interface CardProps {
  header?: React.ReactNode;
  footer?: React.ReactNode;
  children: React.ReactNode;
}

function Card({ header, footer, children }: CardProps) {
  return (
    <div className="bg-surface rounded-2xl overflow-hidden">
      {header && (
        <div className="px-6 py-4 border-b border-border">
          {header}
        </div>
      )}
      <div className="p-6">{children}</div>
      {footer && (
        <div className="px-6 py-4 border-t border-border bg-muted/50">
          {footer}
        </div>
      )}
    </div>
  );
}

// Usage
<Card
  header={<h2>Settings</h2>}
  footer={<Button>Save</Button>}
>
  <p>Card content here</p>
</Card>
```

## 3. Compound Components

```tsx
const CardContext = createContext<{ variant: string }>({ variant: "default" });

function Card({ children, variant = "default" }) {
  return (
    <CardContext.Provider value={{ variant }}>
      <div className="bg-surface rounded-2xl">{children}</div>
    </CardContext.Provider>
  );
}

Card.Header = function CardHeader({ children }) {
  return <div className="px-6 py-4 border-b">{children}</div>;
};

Card.Body = function CardBody({ children }) {
  return <div className="p-6">{children}</div>;
};

Card.Footer = function CardFooter({ children }) {
  const { variant } = useContext(CardContext);
  return (
    <div className={cn("px-6 py-4", variant === "glass" && "bg-white/5")}>
      {children}
    </div>
  );
};

// Usage
<Card variant="glass">
  <Card.Header>
    <h2>Title</h2>
  </Card.Header>
  <Card.Body>
    <p>Content</p>
  </Card.Body>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card>
```

## 4. Render Props

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  renderEmpty?: () => React.ReactNode;
}

function List<T>({ items, renderItem, renderEmpty }: ListProps<T>) {
  if (items.length === 0) {
    return renderEmpty?.() ?? <p>No items</p>;
  }

  return (
    <ul className="space-y-2">
      {items.map((item, i) => (
        <li key={i}>{renderItem(item, i)}</li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={(user) => <UserCard user={user} />}
  renderEmpty={() => <EmptyState message="No users found" />}
/>
```

## 5. As Prop (Polymorphic)

```tsx
type ButtonProps<T extends React.ElementType> = {
  as?: T;
  children: React.ReactNode;
} & React.ComponentPropsWithoutRef<T>;

function Button<T extends React.ElementType = "button">({
  as,
  children,
  ...props
}: ButtonProps<T>) {
  const Component = as || "button";
  return (
    <Component
      className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
      {...props}
    >
      {children}
    </Component>
  );
}

// Usage
<Button>Click me</Button>
<Button as="a" href="/link">Link button</Button>
<Button as={Link} to="/route">Router link</Button>
```

## 6. Forwarded Refs

```tsx
const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  return (
    <input
      ref={ref}
      className="w-full px-4 py-2 rounded-lg border"
      {...props}
    />
  );
});
Input.displayName = "Input";

// Usage with ref
const inputRef = useRef<HTMLInputElement>(null);
<Input ref={inputRef} />
```

## Composition Guidelines

| DO | DON'T |
|----|-------|
| Use children for simple nesting | Over-engineer simple components |
| Use slots for named regions | Use too many slots (max 3-4) |
| Use compound for related parts | Create deep nesting (max 2 levels) |
| Forward refs for form elements | Forget displayName |

## Validation

```
[ ] Appropriate pattern for complexity
[ ] TypeScript props properly typed
[ ] displayName set on forwardRef
[ ] Context used sparingly
[ ] Max 2-3 composition levels
[ ] Documented API in JSDoc
```

## References

- `../../references/design-patterns.md` - Component patterns
- `../../references/component-examples.md` - Production examples
