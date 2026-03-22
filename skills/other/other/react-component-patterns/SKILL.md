---
name: react-component-patterns
description: React + TypeScript component design patterns — composition, props API design, compound components, controlled vs uncontrolled, and memoization decisions
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[component file or pattern question]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: react, components, patterns
---

# React Component Patterns

## Overview

Reference guide for idiomatic React + TypeScript component design. Apply these patterns when building, reviewing, or refactoring React components to ensure type safety, composability, and performance.

## Composition Over Inheritance

Always compose components rather than extending them. React has no use case for class inheritance beyond `React.Component` itself.

```tsx
// GOOD: Composition via props and children
type CardProps = {
  children: React.ReactNode;
  variant?: "elevated" | "outlined";
};

function Card({ children, variant = "elevated" }: CardProps) {
  return <div className={`card card--${variant}`}>{children}</div>;
}

function UserCard({ user }: { user: User }) {
  return (
    <Card variant="elevated">
      <Avatar src={user.avatar} />
      <CardBody>
        <h3>{user.name}</h3>
        <p>{user.bio}</p>
      </CardBody>
    </Card>
  );
}
```

## Props API Design

### Discriminated Unions for Variant Props

Use discriminated unions when props change shape based on a type field. Never use `type?: string` with conditional props.

```tsx
// GOOD: Discriminated union — TypeScript enforces valid combinations
type ButtonProps =
  | { variant: "link"; href: string; onClick?: never }
  | { variant: "button"; onClick: () => void; href?: never }
  | { variant: "submit"; form: string; onClick?: never; href?: never };

function Button(props: ButtonProps) {
  switch (props.variant) {
    case "link":
      return <a href={props.href}>Link</a>;
    case "button":
      return <button onClick={props.onClick}>Click</button>;
    case "submit":
      return <button type="submit" form={props.form}>Submit</button>;
  }
}
```

### Children Patterns

Use `children` for content projection. Use render props only when the child needs data from the parent.

```tsx
// Content projection — simple, preferred
type ModalProps = {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
};

// Render prop — when child needs parent data
type ListProps<T> = {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
};

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, i) => (
        <li key={keyExtractor(item)}>{renderItem(item, i)}</li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={(user) => <UserRow user={user} />}
  keyExtractor={(user) => user.id}
/>
```

### Polymorphic `as` Prop

Allow consumers to change the rendered element while preserving type safety.

```tsx
type BoxProps<C extends React.ElementType> = {
  as?: C;
  children: React.ReactNode;
} & Omit<React.ComponentPropsWithoutRef<C>, "as" | "children">;

function Box<C extends React.ElementType = "div">({
  as,
  children,
  ...rest
}: BoxProps<C>) {
  const Component = as || "div";
  return <Component {...rest}>{children}</Component>;
}

// Usage — href is type-checked because as="a"
<Box as="a" href="/about">About</Box>
// Type error: href not valid on button
<Box as="button" href="/about">Nope</Box>
```

## Compound Components

Use compound components when a group of components share implicit state. Expose a clean API via dot notation.

```tsx
type TabsContextType = {
  activeTab: string;
  setActiveTab: (id: string) => void;
};

const TabsContext = createContext<TabsContextType | null>(null);

function useTabsContext() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error("Tabs compound components must be used within <Tabs>");
  return ctx;
}

function Tabs({ defaultTab, children }: { defaultTab: string; children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div role="tablist">{children}</div>;
}

function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useTabsContext();
  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab } = useTabsContext();
  if (activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
}

// Attach sub-components for dot notation
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage
<Tabs defaultTab="profile">
  <Tabs.List>
    <Tabs.Tab id="profile">Profile</Tabs.Tab>
    <Tabs.Tab id="settings">Settings</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel id="profile">Profile content</Tabs.Panel>
  <Tabs.Panel id="settings">Settings content</Tabs.Panel>
</Tabs>
```

## Controlled vs Uncontrolled

Support both patterns by detecting whether the value prop is provided.

```tsx
type InputProps = {
  value?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
};

function Input({ value: controlledValue, defaultValue = "", onChange }: InputProps) {
  const [internalValue, setInternalValue] = useState(defaultValue);
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : internalValue;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const next = e.target.value;
    if (!isControlled) setInternalValue(next);
    onChange?.(next);
  };

  return <input value={value} onChange={handleChange} />;
}
```

## Memoization Decision Tree

### When to use `React.memo`

Use `React.memo` only when you have **measured** a performance problem. Default: do not memo.

```
Should I use React.memo?
├── Is the component re-rendering frequently with the same props?
│   ├── YES → Does the render involve expensive computation or deep trees?
│   │   ├── YES → Use React.memo ✓
│   │   └── NO → Probably not worth it
│   └── NO → Don't use React.memo
└── Is the component a leaf node receiving only primitive props?
    └── YES, and parent re-renders often → React.memo is cheap here ✓
```

```tsx
// JUSTIFIED: Expensive list item, parent re-renders on every keystroke
const ExpensiveRow = React.memo(function ExpensiveRow({ data }: { data: RowData }) {
  const processed = heavyComputation(data);
  return <tr>{/* ... */}</tr>;
});
```

### `useMemo` — for expensive derived values

```tsx
// GOOD: Expensive filter/sort on large dataset
const filtered = useMemo(
  () => items.filter(matchesSearch).sort(byDate),
  [items, matchesSearch, byDate]
);

// BAD: Trivial computation — overhead of useMemo > savings
const fullName = useMemo(() => `${first} ${last}`, [first, last]);
// Just compute it:
const fullName = `${first} ${last}`;
```

### `useCallback` — for stable function references

Only needed when passing callbacks to memoized children or as effect dependencies.

```tsx
// GOOD: onClick passed to a React.memo child
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

// BAD: No memoized consumer, useCallback is wasted
const handleClick = useCallback(() => {
  console.log("clicked");
}, []);
// Just use a plain function:
const handleClick = () => console.log("clicked");
```

## Forwarding Refs

Use `forwardRef` for reusable primitive components that wrap DOM elements.

```tsx
type InputProps = React.ComponentPropsWithoutRef<"input"> & {
  label: string;
  error?: string;
};

const TextField = forwardRef<HTMLInputElement, InputProps>(
  function TextField({ label, error, ...props }, ref) {
    const id = useId();
    return (
      <div>
        <label htmlFor={id}>{label}</label>
        <input ref={ref} id={id} aria-invalid={!!error} {...props} />
        {error && <span role="alert">{error}</span>}
      </div>
    );
  }
);
```

## Anti-patterns

### Prop Drilling Beyond 2 Levels

If a prop passes through more than 2 intermediate components that do not use it, introduce context or composition.

```tsx
// BAD: theme drilled through 3 levels
<App theme={theme}>
  <Layout theme={theme}>
    <Sidebar theme={theme}>
      <NavItem theme={theme} />  // Only NavItem uses it

// GOOD: Use context
const ThemeContext = createContext<Theme>(defaultTheme);
// Or compose: pass <NavItem> as children so App can inject theme directly
```

### God Components

A component over 200 lines or with more than 5 state variables is too large. Extract sub-components or custom hooks.

### useEffect for Derived State

Never sync state from props via useEffect. Compute during render.

```tsx
// BAD
const [fullName, setFullName] = useState("");
useEffect(() => {
  setFullName(`${first} ${last}`);
}, [first, last]);

// GOOD — compute during render
const fullName = `${first} ${last}`;
```

### Boolean Prop Explosion

More than 2 boolean props usually means you need a discriminated union or a `variant` prop.

```tsx
// BAD: 2^4 = 16 possible states, most invalid
<Button primary large outlined disabled />

// GOOD: variant constrains valid states
<Button variant="primary" size="lg" disabled />
```
