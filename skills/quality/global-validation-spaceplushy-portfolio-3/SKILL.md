---
name: Global Validation
description: Implement runtime validation and type safety using Zod schemas for Content Collections, API inputs, form data, and environment variables. Use this skill when validating user input, API requests, content schemas, or ensuring data integrity. When working on Content Collections schema definitions in src/content/config.ts, API route input validation with Zod, form validation (server-side and client-side), environment variable validation, component prop validation with runtime checks, URL and query parameter validation, request body and form data sanitization, TypeScript runtime type validation, or custom Zod refinements and transformations.
---

# Global Validation

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global validation.

## When to use this skill

- When defining Content Collection Zod schemas in src/content/config.ts
- When validating API route inputs (query params, request body, headers)
- When implementing server-side form validation in API endpoints
- When validating environment variables on application startup
- When adding client-side HTML5 form validation attributes
- When sanitizing user input to prevent XSS attacks
- When validating URLs, emails, or other formatted data types
- When implementing component prop validation for critical components
- When using Zod safeParse for validation with detailed error messages
- When creating custom Zod refinements for complex validation rules
- When ensuring type safety at runtime, not just compile-time

## Instructions

For details, refer to the information provided in this file:
[global validation](../../../agent-os/standards/global/validation.md)
