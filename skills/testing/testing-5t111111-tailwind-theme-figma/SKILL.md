---
name: testing
description: Guide for testing practices and frameworks
---

# Testing Skill

This skill provides a guide for testing practices and frameworks.

## Testing frameworks

- Use Deno's built-in testing framework for writing and running tests

## Writing Tests

- Write tests in separate files with the `.test.ts` extension in the same
  directory as the code being tested
- All public functions and methods must have corresponding tests
- Use descriptive names for test cases to clearly indicate their purpose
- Should cover edge cases and error handling in tests

## Running Tests

- Use the command `mise run test` to run all tests in the project
- Run tests before committing code changes to ensure no tests are failing
