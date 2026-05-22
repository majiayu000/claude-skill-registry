---
name: input-validation
description: Validate all user inputs against expected formats, lengths, and character sets Use when implementing security best practices. Security category skill.
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_input_validation
---

# Input Validation

Validate all user inputs against expected formats, lengths, and character sets. Use whitelist validation (allow known good) rather than blacklist (block known bad). Validate on the server side even if client-side validation exists. Use schema validation libraries (Zod, Joi, JSON Schema) for complex inputs. Reject invalid input early with clear error messages that don't expose implementation details.