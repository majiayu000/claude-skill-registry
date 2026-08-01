---
name: test-organization
description: Test file structure and naming conventions for the music-app project.
---

# Test Organization Skill

## Purpose
Test file structure and naming conventions for the music-app project.

## File Structure
```
src/
├── components/
│   ├── NavBar.jsx
│   └── __tests__/
│       └── NavBar.test.jsx
├── services/
│   ├── tunesService.js
│   └── __tests__/
│       └── tunesService.test.js
```

## Naming Conventions
- Component tests: `ComponentName.test.jsx`
- Service tests: `serviceName.test.js`
- Test directory: `__tests__/` adjacent to source

## Test Structure
```javascript
describe('ComponentName', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('feature group', () => {
    test('specific behavior', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

## Best Practices
✅ Group related tests with describe
✅ Clear, descriptive test names
✅ One assertion per test (usually)
✅ Clean up in beforeEach/afterEach
❌ Don't skip tests without reason
❌ Don't test implementation details
