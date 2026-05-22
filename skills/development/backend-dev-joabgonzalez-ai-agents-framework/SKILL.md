---
name: backend-dev
description: "Back-end development workflow and best practices. API design, data modeling, error handling, and deployment. Trigger: When building, refactoring, or scaling back-end applications."
skills:
  - conventions
  - typescript
  - nodejs
  - architecture-patterns
  - humanizer
allowed-tools:
  - documentation-reader
  - web-search
---

# Backend Development Skill

## Overview

This skill provides universal patterns for back-end development workflow, focusing on API design, data modeling, error handling, and deployment. It is technology-agnostic and emphasizes maintainability, scalability, and robustness.

## When to Use

- Designing, building, or refactoring APIs
- Modeling data and business logic
- Preparing for deployment or CI/CD
- Reviewing or improving code quality and structure

## Critical Patterns

### API Design

- Define clear, versioned contracts for endpoints
- Use RESTful or RPC conventions as appropriate
- Document APIs for consumers

### Data Modeling

- Normalize data structures for consistency
- Use validation at boundaries (input/output)
- Separate domain logic from persistence

### Error Handling

- Centralize error handling and logging
- Return meaningful error messages/codes
- Monitor and alert on failures

### Deployment

- Automate build, test, and deploy steps
- Use environment variables for config
- Monitor deployments for errors and rollbacks

## Decision Tree

- New endpoint? → Define contract/schema and document
- Data model change? → Migrate safely and validate
- Deployment? → Automate with CI/CD
- Bug found? → Add/expand test coverage

## Edge Cases

- Data migration failures (rollback, partial data)
- API versioning and backward compatibility
- Security edge cases (injection, auth, rate limiting)

## Practical Examples

### Before (no API versioning)

> All endpoints are on /api with no versioning, breaking clients on changes.

### After (versioned API)

> Endpoints use /api/v1, changes are documented and backward compatible.

### Before (no error handling)

> Errors are logged to console, users get generic 500 errors.

### After (robust error handling)

> Centralized error handler returns clear messages, logs with context, and triggers alerts.

## References

- Use with conventions, architecture-patterns, and process-documentation for best results.
