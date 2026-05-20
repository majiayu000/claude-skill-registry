---
name: interaction-design
description: Creates intuitive user experiences through feedback patterns, microinteractions, and accessible interaction design. Use when designing loading states, error handling UX, animation guidelines, or touch interactions.
license: MIT
---

# Interaction Design

Create intuitive user experiences through thoughtful feedback and interaction patterns.

## Interaction Patterns

| Pattern | Duration | Use Case |
|---------|----------|----------|
| Microinteraction | 100-200ms | Button press, toggle |
| Transition | 200-400ms | Page change, modal |
| Entrance | 300-500ms | List items appearing |

## Loading States

```css
/* Skeleton loader */
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

```jsx
function LoadingState({ isLoading, children }) {
  if (isLoading) {
    return <div className="skeleton" style={{ height: 200 }} />;
  }
  return children;
}
```

## Error States

```jsx
function ErrorState({ error, onRetry }) {
  return (
    <div className="error-container" role="alert">
      <Icon name="warning" />
      <h3>Something went wrong</h3>
      <p>{error.message}</p>
      <button onClick={onRetry}>Try Again</button>
    </div>
  );
}
```

## Empty States

```jsx
function EmptyState({ title, description, action }) {
  return (
    <div className="empty-state">
      <Illustration name="empty-inbox" />
      <h3>{title}</h3>
      <p>{description}</p>
      {action && <button onClick={action.onClick}>{action.label}</button>}
    </div>
  );
}
```

## Accessibility

```jsx
// Announce state changes to screen readers
function StatusAnnouncer({ message }) {
  return (
    <div aria-live="polite" aria-atomic="true" className="sr-only">
      {message}
    </div>
  );
}

// Respect motion preferences
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```

## Animation Guidelines

- Keep animations under 500ms (longer feels sluggish)
- Use ease-out for entering, ease-in for exiting
- Respect `prefers-reduced-motion`
- Ensure focus indicators are always visible
- Test with keyboard navigation

## Best Practices

- Provide immediate feedback for all actions
- Show loading states for waits >0.5s
- Include clear error messages with recovery options
- Design meaningful empty states
- Support keyboard navigation
