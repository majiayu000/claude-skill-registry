---
name: Jest Test Framework
description: Execute and generate Jest tests for JavaScript/TypeScript projects with support for unit, integration, and E2E testing
version: 1.0.0
---

# Jest Test Framework

## Purpose

Provide comprehensive Jest test execution and generation capabilities for JavaScript and TypeScript projects, supporting:
- Test file generation from bug reports
- Test execution with detailed output parsing
- Unit, integration, and E2E test patterns
- TypeScript and modern JavaScript syntax

## Usage

### Generate Test File

Create a test file from a bug report or feature description:

```bash
node generate-test.js \
  --source src/components/Button.js \
  --output tests/components/Button.test.js \
  --type unit \
  --description "Button component fails to handle click events"
```

### Execute Tests

Run Jest tests and return structured results:

```bash
node run-test.js \
  --file tests/components/Button.test.js \
  --config jest.config.js
```

## Command Line Options

### generate-test.js

- `--source <path>` - Source file to test (required)
- `--output <path>` - Output test file path (required)
- `--type <unit|integration|e2e>` - Test type (default: unit)
- `--description <text>` - Bug description or test purpose
- `--framework <react|node|express>` - Framework-specific patterns

### run-test.js

- `--file <path>` - Test file to execute (required)
- `--config <path>` - Jest config file (optional)
- `--coverage` - Run with coverage report
- `--watch` - Run in watch mode (not recommended for CI)

## Output Format

### Test Generation

Returns JSON with generated test file information:

```json
{
  "success": true,
  "testFile": "tests/components/Button.test.js",
  "testCount": 3,
  "template": "unit-test",
  "framework": "react"
}
```

### Test Execution

Returns JSON with test results:

```json
{
  "success": false,
  "passed": 2,
  "failed": 1,
  "total": 3,
  "duration": 1.234,
  "failures": [
    {
      "test": "Button handles click events",
      "error": "Expected onClick to be called",
      "file": "tests/components/Button.test.js",
      "line": 15
    }
  ]
}
```

## Templates

### Unit Test Template

For testing individual functions or components in isolation:
- Minimal dependencies
- Fast execution
- Focused on single responsibility

### Integration Test Template

For testing multiple components working together:
- Real dependencies (minimal mocking)
- Database/API integration
- Multi-component workflows

### E2E Test Template

For testing complete user journeys:
- Full application stack
- Browser automation (if applicable)
- End-to-end scenarios

## Framework-Specific Patterns

### React Components

```javascript
import { render, fireEvent, screen } from '@testing-library/react';
import { Button } from '../components/Button';

describe('Button', () => {
  it('handles click events', () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(onClick).toHaveBeenCalled();
  });
});
```

### Node.js/Express

```javascript
const request = require('supertest');
const app = require('../app');

describe('GET /api/users', () => {
  it('returns list of users', async () => {
    const res = await request(app).get('/api/users');
    expect(res.status).toBe(200);
    expect(res.body).toBeInstanceOf(Array);
  });
});
```

## Integration with deep-debugger

The deep-debugger agent uses this skill for:

1. **Test Recreation**: Generate failing test from bug report
2. **Test Validation**: Execute test to verify it fails consistently
3. **Fix Verification**: Re-run test after fix to ensure it passes

Example workflow:
```markdown
1. deep-debugger receives bug report
2. Invokes test-detector to identify Jest
3. Invokes jest-test/generate-test.js to create failing test
4. Invokes jest-test/run-test.js to validate test fails
5. Delegates fix to appropriate specialist agent
6. Invokes jest-test/run-test.js to verify fix
```

## Dependencies

Requires Jest to be installed in the project:

```bash
npm install --save-dev jest @types/jest
```

For React testing:
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

## Error Handling

### Test Generation Errors

```json
{
  "success": false,
  "error": "Source file not found",
  "file": "src/components/Missing.js"
}
```

### Test Execution Errors

```json
{
  "success": false,
  "error": "Jest configuration not found",
  "config": "jest.config.js"
}
```

## See Also

- [REFERENCE.md](REFERENCE.md) - Detailed Jest API reference and best practices
- [templates/](templates/) - Test file templates for different scenarios
