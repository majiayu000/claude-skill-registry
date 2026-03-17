---
description: Use this skill when the user describes a component in natural language, says "create a component with...", "I need a card that has...", "build a form with fields for...", "generate component from description", or provides detailed component requirements in plain English. Enables non-technical stakeholders to generate production-ready components through natural language descriptions.
---

# Natural Language Component Generation Skill

## Overview

Generate complete, production-ready components from natural language descriptions. Simply describe what you want in plain English, and get fully-typed TypeScript components with props, variants, stories, and tests.

**Example:**
> "Create a user profile card with an avatar on the left, name and title stacked vertically in the middle, and a follow button on the right. Include an online status indicator and verified badge."

→ Generates complete UserProfileCard component with all requested features, TypeScript interfaces, 8+ story variants, and accessibility baked in.

## How It Works

### 1. Parse Description

AI extracts structured requirements:
- **Component name**: Inferred from description
- **UI elements**: Avatar, buttons, badges, etc.
- **Layout structure**: Left/middle/right, grid, flex
- **Props**: Explicit (mentioned) + inferred (standard patterns)
- **Variants**: Success/error/warning states
- **Behavior**: Interactions, animations
- **Accessibility**: ARIA attributes based on component type

### 2. Generate Component Code

Creates complete implementation:
- **TypeScript interfaces**: Properly typed props
- **React component**: Functional component with hooks
- **Styling approach**: Tailwind/CSS modules/styled-components
- **Accessibility**: WCAG-compliant from start
- **Error handling**: Prop validation, edge cases

### 3. Create Stories

Comprehensive Storybook coverage:
- **All variants**: From description + inferred
- **Edge cases**: Empty state, loading, error
- **Interaction tests**: Play functions for behaviors
- **Accessibility tests**: axe-core validation

## Example Workflows

### Example 1: Notification Card

**User Input:**
> "I need a notification card with an icon, title, message, timestamp, and dismiss button. Support success, warning, error types with different colors. Auto-dismiss after 5 seconds but allow pinning."

**AI Analysis:**
```json
{
  "name": "NotificationCard",
  "elements": ["Icon", "Title", "Message", "Timestamp", "DismissButton"],
  "variants": ["Success", "Warning", "Error"],
  "props": {
    "type": "success | warning | error",
    "title": "string",
    "message": "string",
    "timestamp": "Date",
    "onDismiss": "() => void",
    "pinned": "boolean",
    "autoDismiss": "boolean"
  },
  "behavior": {
    "autoDismiss": { "delay": 5000, "conditional": "!pinned" }
  },
  "accessibility": {
    "role": "alert",
    "ariaLive": "polite"
  }
}
```

**Generated Output:**

```tsx
// NotificationCard.tsx
import { useEffect, useState } from 'react';
import { X, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

interface NotificationCardProps {
  type: 'success' | 'warning' | 'error';
  title: string;
  message: string;
  timestamp: Date;
  onDismiss: () => void;
  pinned?: boolean;
  autoDismiss?: boolean;
}

const icons = {
  success: CheckCircle,
  warning: AlertTriangle,
  error: XCircle,
};

const colors = {
  success: 'bg-green-50 border-green-200 text-green-900',
  warning: 'bg-yellow-50 border-yellow-200 text-yellow-900',
  error: 'bg-red-50 border-red-200 text-red-900',
};

export function NotificationCard({
  type,
  title,
  message,
  timestamp,
  onDismiss,
  pinned = false,
  autoDismiss = true,
}: NotificationCardProps) {
  const [isVisible, setIsVisible] = useState(true);
  const Icon = icons[type];

  useEffect(() => {
    if (autoDismiss && !pinned) {
      const timer = setTimeout(() => {
        setIsVisible(false);
        onDismiss();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [autoDismiss, pinned, onDismiss]);

  if (!isVisible) return null;

  return (
    <div
      className={`flex items-start gap-3 p-4 border rounded-lg ${colors[type]}`}
      role="alert"
      aria-live="polite"
    >
      <Icon className="w-5 h-5 mt-0.5" aria-hidden="true" />

      <div className="flex-1">
        <h3 className="font-semibold">{title}</h3>
        <p className="text-sm mt-1">{message}</p>
        <time className="text-xs opacity-75 mt-2 block">
          {timestamp.toLocaleTimeString()}
        </time>
      </div>

      <button
        onClick={onDismiss}
        className="p-1 hover:bg-black/5 rounded"
        aria-label="Dismiss notification"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}

// NotificationCard.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from 'storybook/test';
import { NotificationCard } from './NotificationCard';

const meta = {
  title: 'Components/NotificationCard',
  component: NotificationCard,
  args: {
    onDismiss: fn(),
    timestamp: new Date(),
  },
} satisfies Meta<typeof NotificationCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Success: Story = {
  args: {
    type: 'success',
    title: 'Payment successful',
    message: 'Your payment of $99.00 has been processed.',
  },
};

export const Warning: Story = {
  args: {
    type: 'warning',
    title: 'Storage almost full',
    message: 'You are using 90% of your storage quota.',
  },
};

export const Error: Story = {
  args: {
    type: 'error',
    title: 'Connection failed',
    message: 'Unable to connect to server. Please try again.',
  },
};

export const Pinned: Story = {
  args: {
    ...Success.args,
    pinned: true,
  },
};

export const NoAutoDismiss: Story = {
  args: {
    ...Success.args,
    autoDismiss: false,
  },
};
```

### Example 2: Data Table

**User Input:**
> "Create a data table component with sortable columns, row selection, pagination, and a search bar. Include actions menu for each row."

**Generated:** Complete DataTable component with:
- Sortable column headers
- Checkbox selection
- Pagination controls
- Search input with debounce
- Row action dropdown
- TypeScript interfaces for data
- 10+ story variants (empty, loading, error, etc.)

## Intelligent Defaults

AI infers standard patterns:

### Form Components
- **Labels**: Automatically add for inputs
- **Validation**: Prop for validation errors
- **Submit handler**: onSubmit callback
- **Loading states**: Disabled during submission

### Card Components
- **Header/Body/Footer**: Standard card structure
- **Padding**: Consistent spacing
- **Border/Shadow**: Design system tokens
- **Hover states**: Interactive feedback

### Button Components
- **Variants**: Primary, secondary, outline, ghost
- **Sizes**: Small, medium, large
- **States**: Default, hover, active, disabled, loading
- **Icon support**: Leading/trailing icons

## Accessibility by Default

Every generated component includes:
- **Semantic HTML**: Proper element usage
- **ARIA attributes**: Based on component type
- **Keyboard navigation**: Tab order, Enter/Space handlers
- **Screen reader text**: sr-only labels where needed
- **Focus indicators**: Visible focus states

## Component Agent

The `component-generator-agent` handles complex generation:
- Analyzes requirements
- Maps to existing patterns
- Generates code + stories + tests
- Validates output
- Applies accessibility fixes

See: `agents/component-generator.md`

## Best Practices

### Be Specific
```
❌ "Create a card component"
✅ "Create a product card with image, title, price, rating stars, and add to cart button"
```

### Mention Layout
```
❌ "Create a user card with avatar and name"
✅ "Create a user card with avatar on the left, name and bio stacked on the right"
```

### Include States
```
❌ "Create a button"
✅ "Create a button with loading state, disabled state, and success state after click"
```

### Specify Interactions
```
❌ "Create a modal"
✅ "Create a modal that opens on button click, has a close X button, closes on ESC key, and closes on backdrop click"
```

## Templates

Pre-built patterns for common requests:
- **Form components**: Input, Select, Checkbox, Radio, TextArea
- **Layout components**: Container, Grid, Stack, Spacer
- **Feedback components**: Alert, Toast, Modal, Tooltip
- **Data display**: Table, List, Card, Badge
- **Navigation**: Tabs, Breadcrumbs, Pagination, Menu

See: `skills/natural-language-generation/examples/common-patterns.md`

## Integration with Other Skills

- **component-scaffold**: Uses NL generation for initial setup
- **accessibility-remediation**: Auto-fixes any generated issues
- **testing-suite**: Adds interaction tests to generated stories
- **server-components**: Can generate Server/Client components

## Limitations

**What Works:**
- UI structure and layout
- Standard interactions (click, hover, input)
- Form validation patterns
- Data display components

**What Needs Manual Work:**
- Complex business logic
- Custom animations (Framer Motion, GSAP)
- Third-party library integration (beyond common ones)
- Advanced state management (Zustand, Redux)

For complex requirements, NL generation provides 80% scaffold + manual refinement.

## Summary

Natural language → Production code in seconds:
1. Describe component in plain English
2. AI extracts structured requirements
3. Generates TypeScript component + stories + tests
4. Accessibility and best practices built-in
5. Ready for customization and integration

**Result:** 10x faster prototyping, accessible to non-developers.
