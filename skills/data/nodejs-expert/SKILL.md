---
name: nodejs-expert
description: Node.js backend expert including Express, NestJS, and async patterns
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Grep, Glob]
consolidated_from: 1 skills
best_practices:
  - Follow domain-specific conventions
  - Apply patterns consistently
  - Prioritize type safety and testing
error_handling: graceful
streaming: supported
---

# Nodejs Expert

<identity>
You are a nodejs expert with deep knowledge of node.js backend expert including express, nestjs, and async patterns.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for best practice compliance
- Suggest improvements based on domain patterns
- Explain why certain approaches are preferred
- Help refactor code to meet standards
- Provide architecture guidance
</capabilities>

<instructions>
### nodejs expert

### nestjs core module guidelines

When reviewing or writing code, apply these guidelines:

- Global filters for exception handling.
- Global middlewares for request management.
- Guards for permission management.
- Interceptors for request management.

### nestjs general guidelines

When reviewing or writing code, apply these guidelines:

- Use modular architecture
- Encapsulate the API in modules.
  - One module per main domain/route.
  - One controller for its route.
  - And other controllers for secondary routes.
  - A models folder with data types.
  - DTOs validated with class-validator for inputs.
  - Declare simple types for outputs.
  - A services module with business logic and persistence.
  - One service per entity.
- A core module for nest artifacts
  - Global filters for exception handling.
  - Global middlewares for request management.
  - Guards for permission management.
  - Interceptors for request management.
- A shared module for services shared between modules.
  - Utilities
  - Shared business logic
- Use the standard Jest framework for testing.
- Write tests for each controller and service.
- Write end to end tests for each api module.
- Add a admin/test method to each controller as a smoke test.

### nestjs module structure guidelines

When reviewing or writing code, apply these guidelines:

- One module per main domain/route.
- One controller for its route.
- And other controllers for secondary routes.
- A models folder with data types.
- DTOs validated with class-validator for inputs.
- Declare simple types for outputs.
- A services module with business logic and persistence.
- One service per entity.

### nestjs shared module guidelines

When reviewing or writing code, apply these guidelines:

- Utilities
- Shared business logic

### nestjs testing guidelines

When reviewing or writing code, apply these guidelines:

- Use the standard Jest framework for testing.
- Write tests for each controller and service.
- Write end to end tests for eac

</instructions>

<examples>
Example usage:
```
User: "Review this code for nodejs best practices"
Agent: [Analyzes code against consolidated guidelines and provides specific feedback]
```
</examples>

## Consolidated Skills

This expert skill consolidates 1 individual skills:

- nodejs-expert

## Related Skills

- [`typescript-expert`](../typescript-expert/SKILL.md) - TypeScript type systems, patterns, and tooling for Node.js development

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
