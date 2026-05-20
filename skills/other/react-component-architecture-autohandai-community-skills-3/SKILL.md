---
name: react-component-architecture
description: Modern React component patterns with hooks, composition, and TypeScript
license: MIT
compatibility: react 18+, typescript 5+
allowed-tools: read_file write_file apply_patch search_with_context
---

# React Component Architecture

## Component Design Principles

1. **Single Responsibility** - Each component does one thing well
2. **Composition Over Configuration** - Use children and render props over prop drilling
3. **Colocation** - Keep related code together (styles, tests, types)
4. **Controlled vs Uncontrolled** - Be explicit about state ownership

## Component Patterns

### Compound Components
For complex UI with shared state:

```typescript
const Tabs = ({ children, defaultValue }: TabsProps) => {
  const [active, setActive] = useState(defaultValue);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = TabsList;
Tabs.Trigger = TabsTrigger;
Tabs.Content = TabsContent;
```

### Render Props for Flexibility
When consumers need control over rendering:

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return items.map((item, i) => (
    <Fragment key={keyExtractor(item)}>{renderItem(item, i)}</Fragment>
  ));
}
```

### Custom Hooks for Logic Extraction
Extract reusable stateful logic:

```typescript
function useToggle(initial = false) {
  const [state, setState] = useState(initial);
  const toggle = useCallback(() => setState(s => !s), []);
  const setTrue = useCallback(() => setState(true), []);
  const setFalse = useCallback(() => setState(false), []);
  return { state, toggle, setTrue, setFalse } as const;
}
```

### Polymorphic Components
Components that render as different elements:

```typescript
type PolymorphicProps<E extends ElementType> = {
  as?: E;
} & ComponentPropsWithoutRef<E>;

function Box<E extends ElementType = 'div'>({
  as,
  ...props
}: PolymorphicProps<E>) {
  const Component = as || 'div';
  return <Component {...props} />;
}
```

## Props Patterns

### Discriminated Union Props
For mutually exclusive prop combinations:

```typescript
type ButtonProps =
  | { variant: 'link'; href: string; onClick?: never }
  | { variant: 'button'; onClick: () => void; href?: never };
```

### Default Props with Destructuring
```typescript
function Button({
  variant = 'primary',
  size = 'md',
  ...props
}: ButtonProps) {
  // ...
}
```

## Performance Patterns

1. **Memoize expensive computations** with `useMemo`
2. **Memoize callbacks** passed to children with `useCallback`
3. **Split contexts** by update frequency
4. **Use `React.memo`** for pure presentational components
5. **Virtualize long lists** with react-virtual or similar

## File Structure

```
components/
  Button/
    Button.tsx        # Component
    Button.test.tsx   # Tests
    Button.types.ts   # Types (if complex)
    index.ts          # Re-export
```
