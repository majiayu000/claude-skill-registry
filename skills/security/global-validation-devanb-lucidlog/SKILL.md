---
name: Global Validation
description: Implement server-side validation with allowlists, specific error messages, type checking, and sanitization to prevent security vulnerabilities and ensure data integrity. Use this skill when creating or editing form request classes, when validating API inputs, when implementing validation rules in controllers or services, when writing client-side validation for user experience, when sanitizing user input to prevent injection attacks, when validating business rules, when implementing error message display, or when ensuring consistent validation across all application entry points.
---

# Global Validation

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global validation.

## When to use this skill

- When creating form request classes in `app/Http/Requests/` for validation logic
- When implementing validation rules in controllers, services, or API endpoints
- When validating user input from web forms or API requests
- When writing client-side validation for immediate user feedback (while ensuring server-side validation)
- When implementing allowlist-based validation (defining what's allowed)
- When sanitizing user input to prevent SQL injection, XSS, or command injection
- When creating specific, actionable error messages for validation failures
- When validating data types, formats, ranges, and required fields
- When implementing business rule validation (e.g., sufficient balance, valid date ranges)
- When ensuring consistent validation across web forms, API endpoints, and background jobs
- When validating file uploads, sizes, and formats
- When implementing custom validation rules or validators

## Instructions

For details, refer to the information provided in this file:
[global validation](../../../agent-os/standards/global/validation.md)
