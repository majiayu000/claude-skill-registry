---
name: testing-standards
description: Ensures all new screens/components have unit tests with proper coverage. Validates test files exist for loading, error, success, and state-transition states. Checks that backend handlers have corresponding test files. Use when creating or modifying frontend screens, components, or backend handlers.
---

# Testing Standards

This skill enforces Ishkul's mandatory unit testing requirements to prevent production issues like the React error #310 caused by missing state transition tests.

## Frontend Testing Requirements

### Screens
Every new screen MUST have a test file at:
```
frontend/src/screens/__tests__/ScreenName.test.tsx
```

Required test coverage:
- **Loading state** - Initial loading UI
- **Error state** - Error handling and display
- **Empty state** - No data scenarios
- **Success state** - Data loaded correctly
- **State transitions** - Critical for catching React Rules of Hooks violations

### Test File Template for Screens
```typescript
describe('ScreenName', () => {
  describe('Loading State', () => {
    it('should display loading indicator', () => { /* test */ });
  });

  describe('Error State', () => {
    it('should display error message', () => { /* test */ });
    it('should allow retry', () => { /* test */ });
  });

  describe('Success State', () => {
    it('should display data correctly', () => { /* test */ });
  });

  describe('State Transitions (Rules of Hooks)', () => {
    it('should handle transition from loading to success', () => { /* test */ });
    it('should handle transition from loading to error', () => { /* test */ });
    it('should handle transition from error to loading (retry)', () => { /* test */ });
  });
});
```

### Components
Every new component MUST have a test file at:
```
frontend/src/components/__tests__/ComponentName.test.tsx
```

Required coverage:
- All props combinations
- User interactions (clicks, input changes)
- Edge cases (empty props, long text, etc.)

## Backend Testing Requirements

Every new handler MUST have a test file at:
```
backend/internal/handlers/handler_name_test.go
```

Required coverage:
- Success cases
- Error cases (invalid input, auth failures)
- Edge cases

## Running Tests

### Frontend
```bash
# Run specific test file
npm test -- --testPathPattern="YourNewFile.test"

# Run all tests
npm test
```

### Backend
```bash
go test ./...
```

## Why This Matters

Missing state transition tests caused a production crash (React error #310) in LessonScreen where hooks were called after conditional returns. Always include state transition tests to catch these issues before deployment.
