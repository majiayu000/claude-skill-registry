---
name: component-scaffold
description: Scaffold a new UI component following Pierre design system patterns
argument-hint: [ComponentName]
user-invocable: true
---

# Component Scaffold

Create a new React component following the Pierre design system conventions.

## Component: $ARGUMENTS

Generate a component with:

1. **File Location**: `frontend/src/components/[ComponentName].tsx`

2. **Standard Structure**:
```tsx
// ABOUTME: [Brief description of what this component does]
// ABOUTME: Part of the Pierre admin dashboard

import React from 'react';
import clsx from 'clsx';
import { Button, Card, CardHeader, Badge } from './ui';

interface [ComponentName]Props {
  // Define props with TypeScript
  className?: string;
}

export const [ComponentName]: React.FC<[ComponentName]Props> = ({
  className,
  ...props
}) => {
  return (
    <Card className={clsx('', className)}>
      {/* Component content */}
    </Card>
  );
};
```

3. **Requirements**:
   - Use design system components (Button, Card, Badge, etc.)
   - Use `pierre-*` color classes only
   - Follow Tailwind spacing scale
   - Include loading and error states if applicable
   - Add TypeScript interfaces for all props

4. **If this is a form component**:
   - Use `input-field` class for inputs
   - Use `label` class for labels
   - Include validation error display
   - Use `Button variant="primary"` for submit

5. **If this is a list component**:
   - Use `Card` for each item
   - Include empty state
   - Include loading skeleton state
   - Use `Badge` for status indicators

After scaffolding, run `/design-review` to validate compliance.
