---
name: jest-generator
description: Generate Jest unit tests for JavaScript/TypeScript with mocking, coverage. Use for JS/TS modules, React components, test generation, or encountering missing coverage, improper mocking, test structure errors.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Jest Generator Skill

## Purpose

Generate Jest-based unit tests for JavaScript and TypeScript code, following Jest conventions and best practices with proper mocking, describe blocks, and code organization.

## When to Use

- Generate Jest tests for JavaScript/TypeScript modules
- Create test files for React components
- Add missing test coverage to existing code
- Need Jest-specific patterns (mocks, spies, snapshots)

## Test File Naming

**Source to Test Mapping:**
- `src/components/Feature.tsx` → `src/components/Feature.test.tsx`
- `src/utils/validator.ts` → `src/utils/validator.test.ts`
- `src/models/User.ts` → `src/models/User.test.ts`

## Running Tests

```bash
# Preferred: Using bun (faster)
bun test

# Run specific file
bun test src/utils/validator.test.ts

# Run with coverage
bun test --coverage

# Watch mode
bun test --watch

# Alternative: Using npm
npm test
npm test -- --coverage
```

## Jest Test Structure

```typescript
import { functionToTest, ClassToTest } from './Feature'

jest.mock('./dependency')

describe('ModuleName', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  describe('ClassName', () => {
    let instance: ClassToTest

    beforeEach(() => {
      instance = new ClassToTest()
    })

    it('should return expected result with valid input', () => {
      // Arrange
      const input = { key: 'value' }
      const expected = { processed: true }

      // Act
      const result = instance.method(input)

      // Assert
      expect(result).toEqual(expected)
    })

    it('should throw error with invalid input', () => {
      expect(() => instance.method(null)).toThrow('Invalid input')
    })
  })
})
```

## Jest-Specific Patterns

### Mocking

```typescript
// Mock entire module
jest.mock('./api', () => ({
  fetchData: jest.fn(),
}))

// Mock with implementation
const mockFn = jest.fn((x: number) => x * 2)

// Spy on method
const spy = jest.spyOn(obj, 'method').mockReturnValue('mocked')
spy.mockRestore()
```

### Async Testing

```typescript
it('should resolve with data', async () => {
  const result = await asyncFunction()
  expect(result).toBeDefined()
})

it('should reject with error', async () => {
  await expect(asyncFunction()).rejects.toThrow('Error')
})
```

### Timers

```typescript
beforeEach(() => jest.useFakeTimers())
afterEach(() => jest.useRealTimers())

it('should execute after timeout', () => {
  const callback = jest.fn()
  setTimeout(callback, 1000)
  jest.advanceTimersByTime(1000)
  expect(callback).toHaveBeenCalled()
})
```

### Common Matchers

```typescript
// Equality
expect(value).toBe(expected)
expect(value).toEqual(expected)

// Truthiness
expect(value).toBeTruthy()
expect(value).toBeNull()
expect(value).toBeDefined()

// Arrays/Objects
expect(array).toContain(item)
expect(obj).toHaveProperty('key')

// Functions/Promises
expect(fn).toThrow('error')
await expect(promise).resolves.toBe(value)

// Mock functions
expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledWith(arg)
```

### React Component Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import { Button } from './Button'

describe('Button', () => {
  it('should call onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

## Quality Checklist

- [ ] Test file properly named (`<module>.test.ts`)
- [ ] All exported functions/classes tested
- [ ] Happy path and edge cases included
- [ ] Error conditions tested
- [ ] External dependencies mocked
- [ ] Tests organized with describe blocks
- [ ] beforeEach/afterEach for setup/cleanup
- [ ] Descriptive test names
- [ ] Coverage ≥ 80%

## Best Practices

1. Use descriptive test names: `should <expected> when <condition>`
2. Organize with describe blocks
3. Mock external dependencies only
4. Test user behavior for components
5. Use test.each for parametrized tests
6. Keep tests independent
7. Test error conditions
8. Aim for 80%+ coverage
