---
name: React TypeScript
description: TypeScript patterns specific to React components and hooks.
metadata:
  labels: [react, typescript, types]
  triggers:
    files: ['**/*.tsx']
    keywords: [ReactNode, FC, PropsWithChildren, ComponentProps]
---

# React TypeScript

## **Priority: P1 (OPERATIONAL)**

Type-safe React patterns.

## Implementation Guidelines

- **Components**: Return `JSX.Element`. Props interface over `React.FC`.
- **Children**: Use `ReactNode` or `PropsWithChildren<T>`.
- **Events**: `React.ChangeEvent<HTMLInputElement>`.
- **Hooks**: `useRef<HTMLDivElement>(null)`. `useState<User | null>(null)`.
- **Props**: Use `ComponentProps<'button'>` to mirror native els.
- **Generics**: `<T,>(props: ListProps<T>)`.
- **Polymorphism**: `as` prop patterns.

## Anti-Patterns

- **No `any`**: Use `unknown`.
- **No `React.FC`**: Implicit children is deprecated/bad practice.
- **No `Function`**: Use `(args: T) => void`.

## Code

```tsx
// Modern Props
type ButtonProps = ComponentProps<'button'> & {
  variant?: 'primary' | 'secondary';
};

// Generic Component
type ListProps<T> = {
  items: T[];
  render: (item: T) => ReactNode;
};

function List<T>({ items, render }: ListProps<T>) {
  return <ul>{items.map(render)}</ul>;
}

// Hook Ref
const inputRef = useRef<HTMLInputElement>(null);
```
