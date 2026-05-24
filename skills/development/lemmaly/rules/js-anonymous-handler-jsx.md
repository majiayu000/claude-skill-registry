---
id: js-anonymous-handler-jsx
title: Anonymous arrow handler in JSX — breaks memoized-child equality
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: javascript
tags: javascript, warning
---

# Anonymous arrow handler in JSX — breaks memoized-child equality

An anonymous arrow handler is a new function every render. For an ordinary child, this is fine. For a `React.memo` child, it breaks equality and forces a re-render every time.

## Fix

Wrap with useCallback if the child is memoized. Otherwise ignore.

## Incorrect

```tsx
// Child is React.memo — this defeats it
<MemoButton onClick={() => save(id)} />
```

## Correct

```tsx
const onClick = useCallback(() => save(id), [id]);
<MemoButton onClick={onClick} />
```
