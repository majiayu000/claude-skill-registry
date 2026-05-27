---
document_name: "component-development.skill.md"
location: ".claude/skills/component-development.skill.md"
codebook_id: "CB-SKILL-COMPDEV-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for UI component development"
skill_metadata:
  category: "development"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Frontend framework knowledge"
    - "TypeScript/JavaScript"
category: "skills"
status: "active"
tags:
  - "skill"
  - "frontend"
  - "component"
  - "react"
  - "ui"
ai_parser_instructions: |
  This skill defines procedures for component development.
  Used by Frontend Engineer agent.
---

# Component Development Skill

=== PURPOSE ===

Procedures for creating and maintaining UI components.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(frontend-engineer) @ref(CB-AGENT-FRONTEND-001) | Primary skill for component work |

=== PROCEDURE: Component Structure ===

**File Organization:**
```
ComponentName/
├── ComponentName.tsx        # Main component
├── ComponentName.test.tsx   # Tests
├── ComponentName.styles.ts  # Styles (CSS-in-JS)
├── ComponentName.module.css # Styles (CSS Modules)
├── ComponentName.types.ts   # TypeScript interfaces
├── ComponentName.stories.tsx # Storybook stories
└── index.ts                 # Public exports
```

**Barrel Export:**
```typescript
// index.ts
export { ComponentName } from './ComponentName';
export type { ComponentNameProps } from './ComponentName.types';
```

=== PROCEDURE: Component Template ===

**Functional Component (React):**
```typescript
import { type FC, memo } from 'react';
import type { ComponentNameProps } from './ComponentName.types';
import styles from './ComponentName.module.css';

export const ComponentName: FC<ComponentNameProps> = memo(({
  title,
  children,
  onAction,
  variant = 'primary',
}) => {
  const handleClick = () => {
    onAction?.();
  };

  return (
    <div className={styles.container} data-variant={variant}>
      <h2 className={styles.title}>{title}</h2>
      <div className={styles.content}>{children}</div>
      <button onClick={handleClick}>Action</button>
    </div>
  );
});

ComponentName.displayName = 'ComponentName';
```

**Types File:**
```typescript
// ComponentName.types.ts
import type { ReactNode } from 'react';

export interface ComponentNameProps {
  /** The title displayed at the top */
  title: string;
  /** Content to render inside */
  children?: ReactNode;
  /** Callback when action is triggered */
  onAction?: () => void;
  /** Visual variant */
  variant?: 'primary' | 'secondary' | 'danger';
}
```

=== PROCEDURE: Props Design ===

**Naming Conventions:**
```typescript
interface Props {
  // Boolean: is/has/can/should prefix
  isLoading?: boolean;
  hasError?: boolean;
  canEdit?: boolean;

  // Events: on prefix
  onClick?: () => void;
  onChange?: (value: string) => void;
  onSubmit?: (data: FormData) => void;

  // Render props: render prefix
  renderHeader?: () => ReactNode;
  renderItem?: (item: Item) => ReactNode;

  // Refs: ref suffix
  inputRef?: RefObject<HTMLInputElement>;
}
```

**Prop Grouping:**
```typescript
interface ButtonProps {
  // Required props first
  label: string;

  // Optional appearance props
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';

  // Optional behavior props
  isDisabled?: boolean;
  isLoading?: boolean;

  // Events last
  onClick?: () => void;
}
```

=== PROCEDURE: Component Testing ===

**Test Structure:**
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  // Rendering tests
  describe('rendering', () => {
    it('renders title correctly', () => {
      render(<ComponentName title="Test Title" />);
      expect(screen.getByText('Test Title')).toBeInTheDocument();
    });

    it('renders children', () => {
      render(<ComponentName title="Title">Child content</ComponentName>);
      expect(screen.getByText('Child content')).toBeInTheDocument();
    });
  });

  // Interaction tests
  describe('interactions', () => {
    it('calls onAction when button clicked', () => {
      const onAction = jest.fn();
      render(<ComponentName title="Title" onAction={onAction} />);

      fireEvent.click(screen.getByRole('button'));
      expect(onAction).toHaveBeenCalledTimes(1);
    });
  });

  // Variant tests
  describe('variants', () => {
    it.each(['primary', 'secondary', 'danger'] as const)(
      'applies %s variant class',
      (variant) => {
        render(<ComponentName title="Title" variant={variant} />);
        expect(screen.getByTestId('container')).toHaveAttribute(
          'data-variant',
          variant
        );
      }
    );
  });
});
```

=== PROCEDURE: Accessibility ===

**Required Practices:**
```typescript
// Semantic HTML
<button>Click me</button>  // Not <div onClick>

// ARIA labels for icons
<button aria-label="Close dialog">
  <CloseIcon aria-hidden />
</button>

// Form labels
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Role for custom components
<div role="tablist">
  <button role="tab" aria-selected={active}>Tab 1</button>
</div>

// Focus management
const dialogRef = useRef<HTMLDivElement>(null);
useEffect(() => {
  dialogRef.current?.focus();
}, []);
```

**Keyboard Navigation:**
```typescript
const handleKeyDown = (e: KeyboardEvent) => {
  switch (e.key) {
    case 'Enter':
    case ' ':
      handleSelect();
      break;
    case 'Escape':
      handleClose();
      break;
    case 'ArrowDown':
      focusNext();
      break;
    case 'ArrowUp':
      focusPrevious();
      break;
  }
};
```

=== PROCEDURE: Performance ===

**Memoization:**
```typescript
// Memoize expensive calculations
const expensiveValue = useMemo(
  () => calculateExpensive(data),
  [data]
);

// Memoize callbacks
const handleClick = useCallback(
  () => onClick(item.id),
  [onClick, item.id]
);

// Memoize components
export const ListItem = memo(({ item, onSelect }) => (
  <div onClick={() => onSelect(item)}>{item.name}</div>
));
```

**Lazy Loading:**
```typescript
// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));

// Use with Suspense
<Suspense fallback={<Loading />}>
  <HeavyChart data={data} />
</Suspense>
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(frontend-patterns) | Architecture context |
| @skill(design-system) | Design tokens |
| @skill(accessibility) | A11y requirements |
