---
skill: add-component
description: Create a React component with TypeScript and optional tests
arguments: component name and optional props description
---

# Add Component: $ARGUMENTS

Create a new React component with proper TypeScript types.

## Process

### 1. Determine Component Type

Based on the name and description:
- **UI Component**: Presentational, receives props
- **Container**: Manages state, fetches data
- **Layout**: Wraps other components
- **Form**: Handles user input

### 2. Create Component File

Location: `components/[ComponentName].tsx`

```tsx
'use client'; // if using hooks or browser APIs

import { useState } from 'react';

interface ComponentNameProps {
  // Define props
  title: string;
  onAction?: () => void;
}

export default function ComponentName({ title, onAction }: ComponentNameProps) {
  return (
    <div data-testid="component-name" className="p-4">
      <h2>{title}</h2>
      {onAction && (
        <button onClick={onAction} data-testid="action-button">
          Action
        </button>
      )}
    </div>
  );
}
```

### 3. Add to Exports (if using barrel exports)

```typescript
// components/index.ts
export { default as ComponentName } from './ComponentName';
```

### 4. Create Test File (optional but recommended)

```typescript
// components/ComponentName.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import ComponentName from './ComponentName';

describe('ComponentName', () => {
  test('renders with title', () => {
    render(<ComponentName title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  test('calls onAction when button clicked', () => {
    const handleAction = jest.fn();
    render(<ComponentName title="Test" onAction={handleAction} />);
    fireEvent.click(screen.getByTestId('action-button'));
    expect(handleAction).toHaveBeenCalled();
  });
});
```

### 5. Validate

```bash
npm run build
npm run lint
```

## Component Patterns

**Controlled input:**
```tsx
interface InputProps {
  value: string;
  onChange: (value: string) => void;
}
```

**With children:**
```tsx
interface WrapperProps {
  children: React.ReactNode;
}
```

**With ref:**
```tsx
const Component = forwardRef<HTMLDivElement, Props>((props, ref) => {
  return <div ref={ref} {...props} />;
});
```

**With default props:**
```tsx
interface Props {
  size?: 'sm' | 'md' | 'lg';
}

function Component({ size = 'md' }: Props) { ... }
```
