---
name: test-suite-generator
description: Generates comprehensive test suites for components, hooks, and utilities with proper mocking and assertions.
---

# Test Suite Generator Skill

## When to Use

- User needs tests for a new component
- User wants to add tests for utility functions
- User needs integration tests for API routes
- User asks to set up testing patterns

## What This Skill Does

1. Determines appropriate test types (unit, integration, e2e)
2. Sets up test files with proper structure
3. Creates mocks for dependencies
4. Writes comprehensive test cases
5. Adds edge case coverage

## Component Testing Pattern

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';
import { ActivityCard } from './ActivityCard';
import type { Activity } from '@repo/core';

describe('ActivityCard', () => {
  const mockActivity: Activity = {
    id: '1',
    name: 'Morning Run',
    type: 'run',
    distance: 5000,
    duration: 1800,
    startTime: new Date(),
  };

  it('renders activity name and stats', () => {
    render(<ActivityCard activity={mockActivity} />);

    expect(screen.getByText('Morning Run')).toBeTruthy();
    expect(screen.getByText('5.00 km')).toBeTruthy();
    expect(screen.getByText('30:00')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    render(<ActivityCard activity={mockActivity} onPress={onPress} />);

    fireEvent.press(screen.getByRole('button'));
    expect(onPress).toHaveBeenCalledWith('1');
  });
});
```

## Hook Testing Pattern

```typescript
import { renderHook, waitFor } from "@testing-library/react-native";
import { useActivityRecorder } from "./useActivityRecorder";

describe("useActivityRecorder", () => {
  it("starts in ready state", () => {
    const { result } = renderHook(() => useActivityRecorder("running"));

    expect(result.current.state).toBe("ready");
  });

  it("transitions to recording when started", async () => {
    const { result } = renderHook(() => useActivityRecorder("running"));

    act(() => {
      result.current.start();
    });

    await waitFor(() => {
      expect(result.current.state).toBe("recording");
    });
  });
});
```

## Utility Function Testing

```typescript
import { calculateTSS } from "./calculations";

describe("calculateTSS", () => {
  it("calculates TSS correctly for 1 hour at FTP", () => {
    const tss = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: 250,
    });

    expect(tss).toBe(100);
  });

  it("returns 0 for zero duration", () => {
    const tss = calculateTSS({
      normalizedPower: 250,
      duration: 0,
      ftp: 250,
    });

    expect(tss).toBe(0);
  });
});
```

## Test Coverage Requirements

- Happy path tests
- Edge cases (null, undefined, empty)
- Error conditions
- Boundary values
- Async operations
- User interactions
