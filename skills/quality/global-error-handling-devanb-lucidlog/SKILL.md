---
name: Global Error Handling
description: Implement user-friendly error handling with specific exception types, centralized error handling, graceful degradation, and proper resource cleanup. Use this skill when implementing error handling in controllers, services, or API endpoints, when creating custom exception classes, when writing try-catch blocks, when handling external service failures, when implementing retry strategies, when displaying error messages to users, when cleaning up resources in finally blocks, or when implementing fail-fast validation and error detection.
---

# Global Error Handling

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global error handling.

## When to use this skill

- When implementing error handling in controllers, services, or API endpoints
- When creating custom exception classes for specific error scenarios
- When writing try-catch blocks for error handling
- When providing user-friendly error messages without exposing technical details
- When implementing fail-fast validation and precondition checks
- When handling errors at appropriate boundaries (controllers, API layers)
- When implementing graceful degradation for non-critical service failures
- When creating retry strategies with exponential backoff for external services
- When cleaning up resources (file handles, database connections) in finally blocks
- When centralizing error handling rather than scattering try-catch everywhere
- When handling transient vs. permanent failures differently
- When logging errors appropriately while protecting sensitive information

## Instructions

For details, refer to the information provided in this file:
[global error handling](../../../agent-os/standards/global/error-handling.md)
