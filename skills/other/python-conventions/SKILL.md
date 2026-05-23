---
name: python-conventions
version: "1.0"
description: Team-specific Python conventions — credential management with dotenv, API client rules, LLM response parsing, TDD workflow, and testing patterns for data pipelines.
---

# Python Conventions — Team Patterns

## When to Activate

- When writing code that uses environment variables or credentials
- When creating or modifying `.env` files
- When writing tests or following TDD
- When building or modifying code that calls external APIs (GitHub, Stripe, LDAP)
- When reviewing code that handles HTTP responses or LLM output

## Conventions

Read `skills/conventions.md` for all team-specific rules: credential management patterns, API client rules (timeout, retry, logging), LLM response parsing, and testing patterns.

## Behavioral Rules

Read `guidelines.md` for hard limits on credential handling, API timeouts, and testing requirements.
