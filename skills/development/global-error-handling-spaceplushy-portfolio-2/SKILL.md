---
name: Global Error Handling
description: Implement comprehensive error handling strategies including try-catch blocks, API error responses, Content Collection error handling, custom error pages, and production error monitoring. Use this skill when handling data fetching errors, API route errors, validation failures, or implementing error boundaries. When working on API route error responses with proper HTTP status codes, data fetching logic with try-catch error handling, Content Collection getEntry/getCollection error handling, custom error pages (404.astro, 500.astro), React Error Boundaries for client-side components, client-side script error handling, error logging and monitoring integration (Sentry), build-time error handling, or retry logic with exponential backoff.
---

# Global Error Handling

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global error handling.

## When to use this skill

- When writing API routes that need consistent error responses with proper HTTP status codes
- When implementing data fetching logic that requires try-catch error handling
- When using Content Collections getEntry or getCollection methods
- When creating custom error pages (src/pages/404.astro, 500 error pages)
- When implementing React Error Boundaries for client-side component errors
- When writing client-side scripts that need error handling and logging
- When integrating error monitoring tools like Sentry for production tracking
- When handling build-time errors or Content Collection schema validation failures
- When implementing retry logic with exponential backoff for transient failures
- When ensuring graceful degradation for non-critical feature failures
- When logging errors with appropriate context and severity levels

## Instructions

For details, refer to the information provided in this file:
[global error handling](../../../agent-os/standards/global/error-handling.md)
