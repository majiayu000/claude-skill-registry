---
name: pattern-implement
description: Build sub-patterns with minimal UI
user-invocable: false
---

Use `Skill("ct")` for ct CLI documentation when running commands.

# Implement Sub-Pattern

## Core Rule
Write ONE sub-pattern with minimal stub UI. No styling, just basic inputs/buttons to verify data flow.

**Always use `pattern<Input, Output>()`** - expose actions as `Stream<T>` for testability.

## Order
1. Leaf patterns first (no dependencies on other patterns)
2. Container patterns (compose leaf patterns)
3. main.tsx last (composes everything)

## Read First
- `docs/common/patterns/` - especially `meta/` for generalizable idioms
- `docs/common/concepts/action.md` - action() for local state
- `docs/common/concepts/handler.md` - handler() for reusable logic
- `docs/common/concepts/reactivity.md` - Cell behavior, .get()/.set()
- `docs/common/concepts/identity.md` - equals() for object comparison

## Key Patterns

**action()** - Closes over local state in pattern body:
```tsx
const inputValue = Cell.of("");
const submit = action(() => {
  items.push({ text: inputValue.get() });
  inputValue.set("");
});
```

**handler()** - Reused with different bindings:
```tsx
const deleteItem = handler<void, { items: Writable<Item[]>; index: number }>(
  (_, { items, index }) => items.set(items.get().toSpliced(index, 1))
);
// In JSX: onClick={deleteItem({ items, index })}
```

**Rendering sub-patterns** - Use function calls, not JSX:
```tsx
// ✅ Correct
{items.map((item) => ItemPattern({ item, allItems: items }))}

// ❌ Wrong - JSX fails with typed Output
{items.map((item) => <ItemPattern item={item} />)}
```

## Done When
- Pattern compiles: `deno task ct check pattern.tsx --no-run`
- Minimal UI renders inputs/buttons
- Ready for testing
