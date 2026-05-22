---
name: react-ui
description: Apply React patterns and conventions when working on UI components. Use when editing files in src/ui/, creating React components, or discussing state management. Auto-apply for JSX files.
---

# React UI Skill

This project is migrating from Canvas-only to React + Canvas (Plan 127). Apply these patterns for UI work.

## Current Architecture

- **Debug Panel**: `src/ui/DebugPanel.jsx` - React-based debug UI
- **Stories**: `src/stories/*.stories.jsx` - Ladle for component development
- **Canvas**: Rendering layer remains Canvas 2D

## Component Patterns

### Functional Components Only
```javascript
// Prefer
export function DebugPanel({ gameState, onToggle }) {
  return <div>...</div>;
}

// Avoid class components
```

### Props Interface (JSDoc since no TypeScript)
```javascript
/**
 * @param {Object} props
 * @param {GameState} props.gameState - Current game state
 * @param {Function} props.onToggle - Toggle callback
 */
export function DebugPanel({ gameState, onToggle }) {
```

### State Management
- Use `useState` for local component state
- Use `useRef` for mutable values that don't trigger re-render
- Keep game state in parent, pass down as props

### Performance (Plan 128, 129)
```javascript
// Memoize expensive computations
const computedValue = useMemo(() => expensiveCalc(data), [data]);

// Memoize callbacks passed to children
const handleClick = useCallback(() => doThing(), [dependency]);

// Memoize components that receive stable props
const MemoizedChild = React.memo(ChildComponent);
```

## File Organization

```
src/ui/
├── DebugPanel.jsx       # Main debug panel component
├── DebugPanel.css       # Component styles
├── DebugPanel.test.jsx  # Component tests
└── [future components]
```

## Stories (Ladle)

Create stories for visual development:

```javascript
// src/stories/ComponentName.stories.jsx
export default {
  title: 'UI/ComponentName',
};

export const Default = () => <ComponentName />;
export const WithData = () => <ComponentName data={mockData} />;
```

## CSS Conventions

- Use CSS modules or plain CSS (no CSS-in-JS currently)
- Co-locate styles: `Component.jsx` + `Component.css`
- Use BEM-like naming: `.debug-panel__section`

### CSS Anti-Patterns for 60fps Updates

**NEVER use CSS transitions on elements updated via requestAnimationFrame or every-frame React renders:**

```css
/* BAD - transition fights with 60fps updates, causes flickering */
.progress-fill {
  transition: stroke-dashoffset 0.1s ease-out;
}

/* GOOD - no transition for frequently-updated elements */
.progress-fill {
  /* Direct value updates, no transition */
}
```

When React re-renders at 60fps, CSS transitions try to animate each change over their duration. But React updates faster than the transition completes, causing visual artifacts (flickering, "tweaking out").

**If smooth animation is needed**, use JavaScript animation (RAF) or React Spring, not CSS transitions.

## Testing React Components

```javascript
// src/ui/DebugPanel.test.jsx
import { render, screen } from '@testing-library/react';
import { DebugPanel } from './DebugPanel';

describe('DebugPanel', () => {
  it('renders wave info when gameState provided', () => {
    render(<DebugPanel gameState={mockState} />);
    expect(screen.getByText(/wave height/i)).toBeInTheDocument();
  });
});
```

## Reference Plans

- `plans/tooling/127-declarative-ui-layer.md` - React migration
- `plans/tooling/128-react-performance-optimization.md` - Performance
- `plans/tooling/129-react-18-concurrent-migration.md` - React 18 features
