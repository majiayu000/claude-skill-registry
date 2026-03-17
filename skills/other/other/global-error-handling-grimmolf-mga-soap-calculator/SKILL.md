---
name: Global Error Handling
description: Implement loud failures with specific exception types, actionable error messages, centralized boundary handling, and graceful degradation with telemetry. Use this skill when writing try/catch blocks, error handlers, exception classes, logging statements, retry logic, or resource cleanup code. Applies to all error scenarios requiring context preservation for debugging, proper resource hygiene, and post-mortem-ready error capture across the entire application stack.
---

# Global Error Handling

## When to use this skill

- When writing try/catch/finally blocks or error handling code in any language or framework
- When defining custom exception classes to differentiate user errors, system failures, and timeouts
- When creating error messages for users (plain language) or operators (structured logs with context)
- When implementing centralized error translation at module or API boundaries
- When adding error logging with correlation IDs, stack traces, request IDs, or payload fingerprints
- When implementing graceful degradation with fallback behavior and telemetry alerts
- When writing retry logic with bounded attempts, jitter, and idempotency checks
- When ensuring resources (connections, files, locks) are released in both success and failure paths
- When capturing enough error context for post-mortems without reproducing crashes
- When letting errors bubble up through layers until meaningful context can be added
- When avoiding silent error swallowing that hides bugs from operators
- When instrumenting error paths to make degraded states visible through monitoring
- When implementing error boundaries in React or similar error containment patterns

# Global Error Handling

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global error handling.

## Instructions

For details, refer to the information provided in this file:
[global error handling](../../../agent-os/standards/global/error-handling.md)
