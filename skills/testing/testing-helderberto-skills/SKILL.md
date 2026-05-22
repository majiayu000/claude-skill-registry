---
name: testing
description: Run test suite and report results. Use when user asks to "run tests", "/test", "/testing", "execute tests", or requests running the test suite.
---

# Testing

## Commands (Node/Frontend - Vitest)

- `npm test` - run tests
- `npm run test:watch` - watch mode
- `npm run test:ci` - with coverage

## Workflow

1. Run `npm test`
2. Report results concisely
3. Show failing test names and file paths

## Rules

- Default to `npm test`
- Don't modify tests unless requested
