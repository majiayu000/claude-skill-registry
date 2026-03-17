---
name: typescript-generics
description: Apply when writing reusable functions, components, or utilities that work with multiple types while maintaining type safety.
---

## When to Use

Apply when writing reusable functions, components, or utilities that work with multiple types while maintaining type safety.

## Patterns

### Pattern 1: Generic Function
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/generics.html
function first<T>(array: T[]): T | undefined {
  return array[0];
}

const num = first([1, 2, 3]);       // number | undefined
const str = first(['a', 'b']);      // string | undefined
```

### Pattern 2: Generic with Constraints
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/generics.html
interface HasId {
  id: string;
}

function findById<T extends HasId>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// Works with any object that has 'id'
const user = findById(users, '123');
const post = findById(posts, '456');
```

### Pattern 3: Generic React Component
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/generics.html
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Usage with full type inference
<List
  items={users}
  renderItem={(user) => user.name}  // user is typed as User
  keyExtractor={(user) => user.id}
/>
```

### Pattern 4: Conditional Types
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/conditional-types.html
type ApiResponse<T> = T extends undefined
  ? { success: true }
  : { success: true; data: T };

// Result: { success: true }
type VoidResponse = ApiResponse<undefined>;

// Result: { success: true; data: User }
type UserResponse = ApiResponse<User>;
```

### Pattern 5: Multiple Generics
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/generics.html
function map<T, U>(array: T[], fn: (item: T) => U): U[] {
  return array.map(fn);
}

// T = User, U = string
const names = map(users, user => user.name);

// Merge objects
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}
```

### Pattern 6: Generic Defaults
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/2/generics.html
interface PaginatedResult<T = unknown> {
  data: T[];
  page: number;
  total: number;
}

// Uses default
const result: PaginatedResult = { data: [], page: 1, total: 0 };

// Explicit type
const users: PaginatedResult<User> = { data: [], page: 1, total: 0 };
```

### Pattern 7: NoInfer Utility (TypeScript 5.4+)
```typescript
// Source: https://www.typescriptlang.org/docs/handbook/utility-types.html
// Blocks inference to ensure parameter matches previously inferred type
function createStreetLight<C extends string>(
  colors: C[],
  defaultColor?: NoInfer<C>
) {
  return { colors, defaultColor };
}

createStreetLight(['red', 'yellow', 'green'], 'red');    // OK
createStreetLight(['red', 'yellow', 'green'], 'blue');   // Error
```

## Anti-Patterns

- **Generic where not needed** - Don't use if only one type ever used
- **Too many generics** - Keep under 3 for readability
- **No constraints** - Add `extends` to limit valid types
- **`any` instead of generic** - Generics preserve type info

## Verification Checklist

- [ ] Generic names are descriptive (T, TItem, TResponse)
- [ ] Constraints added where types need structure
- [ ] Default types provided where sensible
- [ ] Type inference works without explicit annotation
- [ ] Complex generics have usage examples
