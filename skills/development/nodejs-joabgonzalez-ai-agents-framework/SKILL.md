---
name: nodejs
description: "Node.js backend patterns and best practices. Server setup, async I/O, process management, environment configuration. Trigger: When building backend services, CLI tools, or server-side scripts with Node.js."
skills:
  - conventions
  - typescript
  - architecture-patterns
dependencies:
  node: ">=18.0.0 <21.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Node.js Skill

## When to Use

- Building backend services or APIs
- Writing CLI tools or scripts
- Managing async I/O and processes

## Critical Patterns

- Use async/await for I/O
- Environment variable management
- Graceful shutdown and error handling

## Decision Tree

- HTTP server? → Use built-in http or framework
- CLI tool? → Use process.argv and commander/yargs
- Long-running process? → Use process signals

## Edge Cases

- Unhandled promise rejections
- Memory leaks in long-running apps
- Child process management
