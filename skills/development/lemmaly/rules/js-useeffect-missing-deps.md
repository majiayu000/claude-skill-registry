---
id: js-useeffect-missing-deps
title: useEffect without a deps array — runs after every render
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: javascript
tags: javascript, warning
---

# useEffect without a deps array — runs after every render

A `useEffect` with no dependency array runs after every render. If the effect updates state, you can get a render loop or wasted work each frame.

## Fix

Add a deps array — `[]` for mount-only, `[a, b]` to track changes.

## Incorrect

```tsx
useEffect(() => {
  setUser(fetchUser(id));
}); // no deps — runs every render
```

## Correct

```tsx
useEffect(() => {
  setUser(fetchUser(id));
}, [id]); // runs when id changes
```
