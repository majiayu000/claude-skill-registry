---
name: Global Validation
description: Validate inputs and preconditions before work begins using symmetric validation across layers, allowlist thinking, and contextual business rules with auditability. Use this skill when writing input validation, form handling, API request validation, or domain logic checks. Applies to all boundary validation requiring structured error responses, edge-case coverage, sanitization, escaping, and contract tests ensuring consistent validation across clients, APIs, background jobs, and CLIs.
---

# Global Validation

## When to use this skill

- When validating user inputs in forms, API endpoints, CLI commands, or background job parameters
- When implementing request validation middleware or decorators that check preconditions early
- When mirroring validation rules across frontend and backend to prevent data sneaking around guardrails
- When designing validators using real-world edge cases (empty strings, nulls, extremes, race conditions)
- When returning structured error payloads with field names, constraint violations, and remediation guidance
- When using allowlist validation (define what's valid, reject everything else) instead of blocklist approaches
- When implementing domain-specific business rules in the domain layer rather than as tribal knowledge
- When logging validation failures with context (user IDs, request IDs) for audit trails
- When sanitizing inputs and escaping outputs appropriate to the sink (SQL, HTML, shell commands)
- When writing contract tests that explicitly verify required fields, optional fields, and mutual exclusivity
- When validating data at multiple layers (client, API, database) for defense in depth
- When creating validation schemas using libraries like Zod, Joi, Pydantic, or similar
- When ensuring validation happens before allocating compute resources or calling dependencies

# Global Validation

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global validation.

## Instructions

For details, refer to the information provided in this file:
[global validation](../../../agent-os/standards/global/validation.md)
