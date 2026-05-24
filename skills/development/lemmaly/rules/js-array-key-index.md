---
id: js-array-key-index
title: key={index} on a list — breaks identity for reorderable items
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: javascript
tags: javascript, info
---

# key={index} on a list — breaks identity for reorderable items

`key={index}` is fine for a static list. For a list that reorders, inserts, or deletes in the middle, it forces React to mismatch component state with the wrong row — losing input focus, animation, and local state.

## Fix

Use a stable id when the list can reorder, insert, or delete in the middle.

## Incorrect

```tsx
{items.map((item, i) => <Row key={i} item={item} />)}
```

## Correct

```tsx
{items.map((item) => <Row key={item.id} item={item} />)}
```
