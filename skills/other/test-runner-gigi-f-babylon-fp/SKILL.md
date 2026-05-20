---
name: Test Runner
description: Run Vitest tests for the Babylon.js game project. Use when the user wants to run tests, check test coverage, debug failing tests, or validate code functionality.
---

# Test Runner

Run and manage Vitest tests for the project.

## Quick Start

### Run all tests
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npm test
```

### Run tests in watch mode
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npm run test:watch
```

### Run tests with coverage
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npm run test:coverage
```

## Test Commands

### Run specific test file
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest run tests/state/stateManager.test.ts
```

### Run tests matching pattern
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest run -t "StateManager"
```

### Run tests in specific directory
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest run tests/systems/
```

### Run with verbose output
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest run --reporter=verbose
```

## Test Analysis

### Show test summary
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest run --reporter=verbose | tail -20
```

### Check test count
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
find tests -name "*.test.ts" -exec echo {} \; | wc -l
echo "test files found"
```

### List all test files
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
find tests -name "*.test.ts" -o -name "*.spec.ts"
```

## Coverage Analysis

### Generate HTML coverage report
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npm run test:coverage
# Report will be in coverage/index.html
```

### Check coverage thresholds
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest run --coverage --coverage.reporter=text-summary
```

## Debugging Tests

### Run with console output
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest run --no-coverage --reporter=verbose
```

### Run single test file with debugging
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest run tests/systems/loopManager.test.ts --no-coverage
```

### Check for test failures
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npm test 2>&1 | grep -E "(FAIL|✓|✗|Error)"
```

## Test Quality Checks

### Count assertions per file
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
for file in tests/**/*.test.ts; do
  echo "$file: $(grep -c 'expect(' $file) assertions"
done
```

### Find test files without assertions
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
for file in tests/**/*.test.ts; do
  if ! grep -q 'expect(' "$file"; then
    echo "No assertions: $file"
  fi
done
```

## Continuous Testing

### Watch mode (auto-rerun on file changes)
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest watch
```

### Watch specific tests
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx vitest watch tests/systems/
```

## Test Organization

Current test structure:
- `tests/content/` - Content loading tests
- `tests/state/` - State management tests
- `tests/systems/` - System tests (LoopManager, TimeSync, etc.)
- `tests/ui/` - UI component tests
- `tests/helpers/` - Test utilities and mocks

## Best Practices

1. **Run tests before committing**: Ensure all tests pass
2. **Watch mode during development**: Catch issues immediately
3. **Coverage tracking**: Aim for >80% coverage on critical systems
4. **Test naming**: Use descriptive test names (describe/it pattern)
5. **Isolated tests**: Each test should be independent
6. **Mock external dependencies**: Use test helpers from `tests/helpers/`

## Common Test Patterns

### Testing async code
```typescript
it('should handle async operations', async () => {
  const result = await asyncFunction();
  expect(result).toBe(expected);
});
```

### Testing Babylon.js components
```typescript
import { mockScene, mockCamera } from '../helpers/testUtils';

it('should initialize scene', () => {
  const scene = mockScene();
  const camera = mockCamera(scene);
  expect(scene).toBeDefined();
});
```

### Testing state changes
```typescript
it('should update state', () => {
  stateManager.setState({ key: 'value' });
  expect(stateManager.getState('key')).toBe('value');
});
```
