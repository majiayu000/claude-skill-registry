---
name: clean-code-guide
description: Helps you write better Python code by following clean code principles and software engineering best practices.
---

# Clean Code Guide

## General Principles

- Write clean, readable code
- Use meaningful variable names instead of single letters
- Keep functions small and focused on one thing
- Don't repeat yourself (DRY)
- Handle errors properly with try/except
- Add comments to explain complex logic
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values

## Testing

- Write tests for your code
- Use pytest as the test framework
- Aim for 80% code coverage
- Test edge cases like empty inputs, None values, and large datasets
- Mock external services in unit tests

## Code Review Checklist

- Are variable names descriptive?
- Are functions under 50 lines?
- Is there code duplication?
- Are errors handled correctly?
- Are there security issues?
- Is the code well-documented?

## Git Workflow

- Write descriptive commit messages
- Use feature branches
- Don't commit secrets or .env files
- Run tests before pushing
