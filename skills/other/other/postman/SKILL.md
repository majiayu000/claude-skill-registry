---
name: postman
description: Postman API platform for testing and documentation. Use for API testing.
---

# Postman

Postman is the complete API lifecycle platform. 2025 features **AI Agent Builder** (orchestrating multi-step workflows) and **Postbot** (AI driven testing).

## When to Use

- **API Development**: Documentation, Mock Servers, and Monitors.
- **Testing**: Automated testing in CI via `newman` CLI.
- **Collaboration**: Workspaces and "Forks" of collections.

## Core Concepts

### Collections

Groups of requests. Can be run as a suite.

### Environments

Variables (`{{base_url}}`) that change between Dev, Staging, and Prod.

### Pre-request Scripts

JavaScript code that runs before a request (e.g. generating an HMAC signature).

## Best Practices (2025)

**Do**:

- **Use AI Agents**: Build workflows that chain requests intelligently using natural language.
- **Use Mock Servers**: Design the API first, create a mock, and let frontend devs build against it before backend is ready.
- **Use `newman`**: Run collections in GitHub Actions.

**Don't**:

- **Don't hardcode auth**: Use "Auth" tab variables.

## References

- [Postman Documentation](https://learning.postman.com/docs/introduction/overview/)
