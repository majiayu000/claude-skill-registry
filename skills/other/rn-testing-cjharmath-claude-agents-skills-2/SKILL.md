---
name: rn-testing
description: Testing patterns for React Native with Jest and React Native Testing Library. Use when writing tests, mocking Expo modules, testing Zustand stores, or debugging test failures.
---

# React Native Testing

## Problem Statement

React Native testing requires extensive mocking of native modules, careful handling of async operations, and understanding of Zustand store testing patterns. This codebase has 30+ test files with established patterns.

---

## Pattern: Zustand Store Testing

**Problem:** Store state persists between tests, causing flaky tests.

```typescript
import { useAssessmentStore } from '@/stores/assessmentStore';

const initialState = {
  userAnswers: {},
  completedAssessmentAnswers: {},
  retakeAreas: new Set<string>(),
  loading: false,
};

describe('Assessment Store', () => {
  // Reset store before each test
  beforeEach(() => {
    useAssessmentStore.setState(initialState, true); // true = replace entire state
  });

  it('saves answer to store', async () => {
    const store = useAssessmentStore.getState();
    
    await store.saveAnswer('q1', 4);
    
    expect(useAssessmentStore.getState().userAnswers['q1']).toBe(4);
  });

  it('enables retake for skill area', async () => {
    const store = useAssessmentStore.getState();
    
    await store.enableSkillAreaRetake('fundamentals');
    
    expect(useAssessmentStore.getState().retakeAreas.has('fundamentals')).toBe(true);
  });
});
```

**Key points:**
- Use `setState(initialState, true)` to replace (not merge) state
- Get fresh state with `getState()` after async operations
- Don't rely on component re-renders in store tests

---

## Pattern: Async Store Operations

**Problem:** Testing async Zustand actions with proper waiting.

```typescript
import { act, waitFor } from '@testing-library/react-native';

it('loads completed answers', async () => {
  const store = useAssessmentStore.getState();
  
  // Wrap async store operations in act
  await act(async () => {
    await store.loadCompletedAssessmentAnswers('assessment-123');
  });
  
  // Verify state after async completes
  await waitFor(() => {
    const state = useAssessmentStore.getState();
    expect(Object.keys(state.completedAssessmentAnswers).length).toBeGreaterThan(0);
  });
});

// For complex flows, verify each step
it('completes retake flow', async () => {
  const store = useAssessmentStore.getState();
  
  // Step 1
  await act(async () => {
    await store.loadCompletedAssessmentAnswers('assessment-123');
  });
  expect(useAssessmentStore.getState().completedAssessmentAnswers).toBeDefined();
  
  // Step 2
  await act(async () => {
    await store.enableSkillAreaRetake('fundamentals');
  });
  expect(useAssessmentStore.getState().retakeAreas.has('fundamentals')).toBe(true);
  
  // Step 3
  await act(async () => {
    await store.saveAnswer('q1', 4);
  });
  expect(useAssessmentStore.getState().userAnswers['q1']).toBe(4);
});
```

---

## Pattern: Expo Module Mocking

**Problem:** Expo modules require mocks for Jest.

```typescript
// __mocks__/expo-router.ts (or in jest.setup.js)
jest.mock('expo-router', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    back: jest.fn(),
    dismiss: jest.fn(),
  }),
  useLocalSearchParams: () => ({}),
  useSegments: () => [],
  usePathname: () => '/',
  Link: ({ children }: { children: React.ReactNode }) => children,
  Stack: {
    Screen: () => null,
  },
}));

// expo-secure-store
jest.mock('expo-secure-store', () => ({
  getItemAsync: jest.fn(),
  setItemAsync: jest.fn(),
  deleteItemAsync: jest.fn(),
}));

// expo-constants
jest.mock('expo-constants', () => ({
  expoConfig: {
    extra: {
      apiUrl: 'http://test-api.local',
    },
  },
}));

// expo-haptics
jest.mock('expo-haptics', () => ({
  impactAsync: jest.fn(),
  notificationAsync: jest.fn(),
  selectionAsync: jest.fn(),
}));
```

**Check `jest.setup.js`** - many mocks are already configured globally.

---

## Pattern: React Query Testing

**Problem:** Components using React Query need QueryClientProvider.

```typescript
// Use existing utility from codebase
import { createTestQueryClient, QueryWrapper } from '@/__tests__/utils/react-query-test-utils';

// Or create wrapper
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
      },
    },
  });
}

function QueryWrapper({ children }: { children: React.ReactNode }) {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

// Usage in tests
import { render, waitFor } from '@testing-library/react-native';

it('fetches and displays data', async () => {
  const { getByText } = render(
    <QueryWrapper>
      <MyComponent />
    </QueryWrapper>
  );
  
  await waitFor(() => {
    expect(getByText('Loaded data')).toBeTruthy();
  });
});
```

---

## Pattern: Custom Hook Testing

```typescript
import { renderHook, act, waitFor } from '@testing-library/react-native';

describe('useAuth', () => {
  it('signs in user', async () => {
    const { result } = renderHook(() => useAuth(), {
      wrapper: AuthProvider, // If hook needs context
    });
    
    await act(async () => {
      await result.current.signIn('token', mockUser);
    });
    
    expect(result.current.user).toEqual(mockUser);
    expect(result.current.token).toBe('token');
  });
});

// Hook with Zustand
describe('useAssessmentAnswers', () => {
  beforeEach(() => {
    useAssessmentStore.setState(initialState, true);
  });

  it('returns current answers', () => {
    // Pre-populate store
    useAssessmentStore.setState({ userAnswers: { q1: 4 } });
    
    const { result } = renderHook(() => useAssessmentAnswers());
    
    expect(result.current.answers).toEqual({ q1: 4 });
  });
});
```

---

## Pattern: Component Testing

```typescript
import { render, fireEvent, waitFor } from '@testing-library/react-native';

describe('SessionCard', () => {
  const mockSession = {
    id: '1',
    title: 'Serve Practice',
    totalDuration: 45, // Backend-calculated
  };

  it('displays session data from backend', () => {
    const { getByText } = render(<SessionCard session={mockSession} />);
    
    expect(getByText('Serve Practice')).toBeTruthy();
    expect(getByText('45 min')).toBeTruthy();
  });

  it('calls onPress when tapped', () => {
    const onPress = jest.fn();
    const { getByTestId } = render(
      <SessionCard session={mockSession} onPress={onPress} />
    );
    
    fireEvent.press(getByTestId('session-card'));
    
    expect(onPress).toHaveBeenCalledWith(mockSession.id);
  });
});
```

---

## Pattern: Navigation Testing

```typescript
import { useRouter } from 'expo-router';

jest.mock('expo-router');

describe('SettingsScreen', () => {
  const mockPush = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
      back: jest.fn(),
    });
  });

  it('navigates to profile on button press', () => {
    const { getByText } = render(<SettingsScreen />);
    
    fireEvent.press(getByText('Edit Profile'));
    
    expect(mockPush).toHaveBeenCalledWith('/profile/edit');
  });
});

// Testing with route params
jest.mock('expo-router', () => ({
  useLocalSearchParams: () => ({ id: 'test-assessment-123' }),
  useRouter: () => ({ push: jest.fn() }),
}));
```

---

## Pattern: Avoiding act() Warnings

**Problem:** "Warning: An update inside a test was not wrapped in act(...)"

```typescript
// WRONG - state update happens after test
it('loads data', () => {
  render(<DataComponent />);
  // Component fetches data async, updates state after test ends
});

// CORRECT - wait for async completion
it('loads data', async () => {
  const { getByText } = render(<DataComponent />);
  
  // Wait for loading to complete
  await waitFor(() => {
    expect(getByText('Data loaded')).toBeTruthy();
  });
});

// CORRECT - use findBy* (has built-in waitFor)
it('loads data', async () => {
  const { findByText } = render(<DataComponent />);
  
  const element = await findByText('Data loaded');
  expect(element).toBeTruthy();
});
```

---

## Pattern: Snapshot Testing

**When to use:**
- UI components with stable structure
- Design system components
- Components where visual regression matters

**When to avoid:**
- Components with dynamic content
- Components that change frequently
- Large component trees (brittle)

```typescript
// Good snapshot candidate - stable UI component
it('renders correctly', () => {
  const tree = render(<Button title="Submit" />);
  expect(tree.toJSON()).toMatchSnapshot();
});

// Bad snapshot candidate - dynamic content
it('renders user list', () => {
  // Don't snapshot - list content varies
  // Instead, test specific behaviors
});
```

---

## Pattern: Mocking API Calls

```typescript
// Mock Orval-generated hooks
jest.mock('@/api/generated/assessments', () => ({
  useGetAssessment: jest.fn(() => ({
    data: mockAssessment,
    isLoading: false,
    error: null,
  })),
  useSubmitAssessment: jest.fn(() => ({
    mutate: jest.fn(),
    isLoading: false,
  })),
}));

// Mock with different states
import { useGetAssessment } from '@/api/generated/assessments';

it('shows loading state', () => {
  (useGetAssessment as jest.Mock).mockReturnValue({
    data: null,
    isLoading: true,
    error: null,
  });
  
  const { getByTestId } = render(<AssessmentScreen />);
  expect(getByTestId('loading-spinner')).toBeTruthy();
});

it('shows error state', () => {
  (useGetAssessment as jest.Mock).mockReturnValue({
    data: null,
    isLoading: false,
    error: new Error('Failed to load'),
  });
  
  const { getByText } = render(<AssessmentScreen />);
  expect(getByText('Failed to load')).toBeTruthy();
});
```

---

## Recommended Test Utilities

```
__tests__/utils/react-query-test-utils.tsx  # QueryClient wrapper
jest.setup.js                                # Global mocks
```

### Test Commands
```bash
npm test                      # Run all tests
npm test -- --watch           # Watch mode
npm test -- --coverage        # Coverage report
npm test -- SessionCard       # Run specific test file
npm test -- --updateSnapshot  # Update snapshots
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| "Cannot find module" | Check jest.setup.js module mappings |
| act() warning | Wrap state updates in act(), use waitFor/findBy |
| Store state bleeding | Add beforeEach with setState reset |
| Async test timeout | Increase timeout or check for hanging promises |
| Mock not working | Verify mock path matches import path exactly |

---

## Relationship to Other Skills

- **rn-async-patterns**: Use post-condition validation in tests to verify async flows
- **rn-zustand-patterns**: Understand `getState()` behavior for store tests
- **rn-state-flows**: Integration tests should cover entire flows, not just units
