---
name: react-component-create
description: Create new React components following project patterns and best practices. Includes proper typing, testing, and documentation.
---

# React Component Create Skill

Create production-ready React components.

## Component Template

### Functional Component

```typescript
import { memo, useCallback, type FC } from "react";

interface ComponentNameProps {
  /** Description of prop */
  propName: string;
  /** Optional prop with default */
  optionalProp?: boolean;
  /** Callback handler */
  onAction?: (value: string) => void;
}

/**
 * ComponentName - Brief description
 *
 * @example
 * <ComponentName propName="value" onAction={handleAction} />
 */
export const ComponentName: FC<ComponentNameProps> = memo(
  ({ propName, optionalProp = false, onAction }) => {
    const handleClick = useCallback(() => {
      onAction?.(propName);
    }, [propName, onAction]);

    return <div className="component-name">{/* Component content */}</div>;
  }
);

ComponentName.displayName = "ComponentName";
```

### Test Template

```typescript
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ComponentName } from "./ComponentName";

describe("ComponentName", () => {
  it("renders correctly", () => {
    render(<ComponentName propName="test" />);
    expect(screen.getByText("test")).toBeInTheDocument();
  });

  it("calls onAction when clicked", () => {
    const onAction = vi.fn();
    render(<ComponentName propName="test" onAction={onAction} />);
    fireEvent.click(screen.getByRole("button"));
    expect(onAction).toHaveBeenCalledWith("test");
  });
});
```

## Directory Structure

```
components/
  ComponentName/
    index.ts          # Export barrel
    ComponentName.tsx # Component implementation
    ComponentName.test.tsx # Tests
    ComponentName.css # Styles (if needed)
```

## Checklist

- [ ] Props interface defined with JSDoc
- [ ] Component wrapped with memo if pure
- [ ] Callbacks wrapped with useCallback
- [ ] DisplayName set for debugging
- [ ] Tests cover main scenarios
- [ ] Accessibility attributes added
- [ ] Types exported if needed elsewhere
