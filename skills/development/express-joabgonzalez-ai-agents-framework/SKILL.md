---
name: express
description: "Express.js server patterns and best practices. Routing, middleware, error handling, async flows. Trigger: When building REST APIs, middleware stacks, or server-side logic with Express."
skills:
  - conventions
  - nodejs
  - typescript
  - architecture-patterns
dependencies:
  express: ">=4.18.0 <5.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Express.js Skill

## When to Use

- Building REST APIs
- Composing middleware stacks
- Handling HTTP requests/responses

## Critical Patterns

- Use Router for modular routes
- Centralized error handling middleware
- Async/await in route handlers

## Decision Tree

- API versioning? → Use Router
- Auth needed? → Use middleware
- Error handling? → Use error middleware

## Edge Cases

- Async error propagation
- Middleware order bugs
- Large payload handling
