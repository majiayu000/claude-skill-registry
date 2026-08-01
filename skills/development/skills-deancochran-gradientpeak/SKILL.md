---
name: skills-deancochran-gradientpeak
description: 'Last Updated: 2026-01-21'
---

# Testing Skill

**Last Updated**: 2026-01-21
**Version**: 1.0.0
**Maintained By**: Skill Creator Agent

## Core Principles

1. **Test Behavior, Not Implementation** - Focus on what code does
2. **Isolated Tests** - Each test independent, no execution order dependencies
3. **Descriptive Names** - Test names describe scenario and expected outcome
4. **Coverage Targets** - 80% for critical paths, 100% for new features
5. **Mock External Dependencies Only** - Don't mock stable internal functions
6. **Clean Up After Tests** - Remove listeners, timers, state

## Patterns to Follow

### Pattern 1: Pure Function Testing

```typescript
describe('calculateTSS', () => {
  it('should calculate TSS correctly for 1 hour at FTP', () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: 250,
    });
    expect(result).toBe(100);
  });

  it('should return 0 for zero duration', () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 0,
      ftp: 250,
    });
    expect(result).toBe(0);
  });

  it('should handle missing FTP', () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: undefined,
    });
    expect(result).toBeNull();
  });
});
```

### Pattern 2: Component Testing (Mobile)

```typescript
import { render, fireEvent } from '@testing-library/react-native';
import { ActivityCard } from '../ActivityCard';

describe('ActivityCard', () => {
  const mockActivity = {
    id: '1',
    name: 'Morning Run',
    type: 'run',
    distance: 5000,
    duration: 1800,
  };

  it('should render activity name', () => {
    const { getByText } = render(<ActivityCard activity={mockActivity} />);
    expect(getByText('Morning Run')).toBeTruthy();
  });

  it('should call onPress when tapped', () => {
    const onPress = jest.fn();
    const { getByTestId } = render(
      <ActivityCard activity={mockActivity} onPress={onPress} />
    );

    fireEvent.press(getByTestId('activity-card'));
    expect(onPress).toHaveBeenCalledWith(mockActivity.id);
  });
});
```

### Pattern 3: Hook Testing

```typescript
import { renderHook, waitFor } from '@testing-library/react-native';
import { useActivityRecorder } from '../useActivityRecorder';

describe('useActivityRecorder', () => {
  const mockProfile = { id: '1', ftp: 250, maxHeartRate: 190 };

  it('should initialize service with profile', () => {
    const { result } = renderHook(() => useActivityRecorder(mockProfile));
    expect(result.current).toBeDefined();
    expect(result.current.getState()).toBe('pending');
  });

  it('should clean up on unmount', () => {
    const { result, unmount } = renderHook(() => useActivityRecorder(mockProfile));
    const cleanupSpy = jest.spyOn(result.current, 'cleanup');

    unmount();
    expect(cleanupSpy).toHaveBeenCalled();
  });
});
```

### Pattern 4: tRPC Router Testing

```typescript
describe('activityRouter', () => {
  let db: Database;
  let ctx: Context;

  beforeEach(async () => {
    db = await createTestDatabase();
    ctx = createInnerTRPCContext({ session: mockSession, db });
  });

  afterEach(async () => {
    await db.clear();
  });

  describe('create', () => {
    it('should create activity with valid input', async () => {
      const caller = activityRouter.createCaller(ctx);

      const activity = await caller.create({
        name: 'Test Activity',
        type: 'run',
      });

      expect(activity.id).toBeDefined();
      expect(activity.name).toBe('Test Activity');
    });

    it('should require authentication', async () => {
      const unauthCtx = createInnerTRPCContext({ session: null });
      const caller = activityRouter.createCaller(unauthCtx);

      await expect(
        caller.create({ name: 'Test', type: 'run' })
      ).rejects.toThrow('UNAUTHORIZED');
    });
  });
});
```

## Test Naming Convention

**Pattern**: `[Subject] [Condition] - [Expected Result]`

**Examples**:
```
"outdoor run with GPS - shows map, tracks location"
"form with invalid email - displays validation error"
"user clicks submit button - calls onSubmit handler"
"service receives sensor data - updates readings state"
```

## Mock Patterns

```typescript
// Mock Bluetooth sensor
const mockSensor = {
  id: 'hr-1',
  read: jest.fn().mockResolvedValue({ heartRate: 150 }),
  connect: jest.fn().mockResolvedValue(true),
};

// Mock tRPC
const trpcMsw = createTRPCMsw<AppRouter>();
const handlers = [
  trpcMsw.activities.list.query(() => [mockActivity]),
];

// Mock Supabase
jest.mock('@supabase/supabase-js', () => ({
  createClient: jest.fn(() => ({
    from: jest.fn(() => ({
      select: jest.fn().mockReturnThis(),
      eq: jest.fn().mockResolvedValue({ data: mockData }),
    })),
  })),
}));
```

## Checklist

- [ ] Test names are descriptive
- [ ] Each test is independent
- [ ] Edge cases covered
- [ ] Error states tested
- [ ] Cleanup functions present
- [ ] Mocks used appropriately
- [ ] Tests run quickly (<30s)
- [ ] Coverage meets targets

## Related Skills

- [Core Package Skill](./core-package-skill.md) - Pure function testing
- [Mobile Frontend Skill](./mobile-frontend-skill.md) - Component testing
- [Backend Skill](./backend-skill.md) - API testing

## Version History

- **1.0.0** (2026-01-21): Initial version

---

**Next Review**: 2026-02-21
