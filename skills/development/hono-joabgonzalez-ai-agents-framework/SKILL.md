---
name: hono
description: "Hono framework patterns and best practices. Lightweight edge/serverless routing, middleware, and API design. Trigger: When building edge APIs or lightweight serverless apps with Hono."
skills:
  - conventions
  - typescript
  - javascript
dependencies:
  hono: ">=3.0.0 <4.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Hono Skill

## When to Use

- Building edge/serverless APIs
- Lightweight routing and middleware
- Deploying to edge platforms

## Critical Patterns

- Use app.route for modular APIs
- Middleware for auth/logging
- Typed request/response objects

## Decision Tree

- Edge or serverless? → Use Hono
- Middleware needed? → Use app.use
- Typed endpoints? → Use zod or typescript

## Edge Cases

- Cold start latency
- Platform-specific limits
- Streaming responses
