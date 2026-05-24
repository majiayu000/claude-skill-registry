---
id: js-inline-object-jsx-prop
title: Inline object literal as JSX prop — new reference every render
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: javascript
tags: javascript, warning
---

# Inline object literal as JSX prop — new reference every render

An inline object literal in JSX creates a new reference every render. If the child is `React.memo`, this defeats the memoization. If it is a dependency of a hook in the child, it re-fires that hook every render.

## Fix

Hoist outside render, or wrap in useMemo if the child is React.memo.

## Incorrect

```tsx
<Chart options={{ animated: true, color: 'red' }} />
```

## Correct

```tsx
// Hoist if static
const CHART_OPTIONS = { animated: true, color: 'red' };
<Chart options={CHART_OPTIONS} />

// Memoize if derived
const options = useMemo(() => ({ animated, color }), [animated, color]);
<Chart options={options} />
```
