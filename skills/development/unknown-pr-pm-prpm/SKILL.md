---
name: test-skill
description: A test skill for E2E conversion testing
tools: Read, Write, Edit, Bash
---

# Test Skill

## Overview
This is a comprehensive test skill for validating format conversion between Claude Skills and Cursor Rules.

## Core Principles
- Write clean, maintainable code
- Test thoroughly before deploying
- Document your work clearly
- Follow established patterns

## Workflow

1. **Understand Requirements**
   - Read the task description carefully
   - Identify all constraints and dependencies
   - Ask clarifying questions if needed

2. **Plan Implementation**
   - Break down the task into steps
   - Identify potential challenges
   - Consider edge cases

3. **Write Code**
   - Follow coding standards
   - Keep functions small and focused
   - Use meaningful variable names

4. **Test Thoroughly**
   - Write unit tests
   - Run integration tests
   - Verify edge cases

5. **Document Solution**
   - Add code comments
   - Update README if needed
   - Document any gotchas

## Best Practices

- **Version Control**: Commit often with clear messages
- **Code Review**: Always get feedback before merging
- **Refactoring**: Improve code structure continuously
- **Learning**: Stay updated with best practices

## Integration

This skill works well with:
- Systematic debugging approaches
- Test-driven development
- Code review practices

## Examples

### Good Code Pattern
```typescript
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Bad Code Pattern (Avoid)
```typescript
function calc(x) {
  let t = 0;
  for (let i = 0; i < x.length; i++) {
    t = t + x[i].p;
  }
  return t;
}
```

## Troubleshooting

- **Issue**: Code not working
  - **Solution**: Check syntax errors, verify inputs

- **Issue**: Tests failing
  - **Solution**: Review test assertions, check mock data

- **Issue**: Performance problems
  - **Solution**: Profile code, optimize bottlenecks
