---
name: api-request-validation
description: A skill for implementing robust API request validation in Python web frameworks like FastAPI using Pydantic. Covers Pydantic models, custom validators (email, password), field-level and cross-field validation, query/file validation, and structured error responses. Use when you need to validate incoming API requests.
---

# API Request Validation Skill

## Overview

This skill provides guidance and reusable components for implementing robust API request validation in Python, primarily using FastAPI and Pydantic.

It covers:
- Basic validation with Pydantic models.
- Custom validation logic for specific fields.
- Advanced validation scenarios like cross-field validation and query parameters.
- Standardized error handling for validation failures.

## Getting Started

The most common validation tasks are broken down into reference files. Start with the one that best fits your needs.

- **Basic Validation**: If you're new to Pydantic or need to validate a simple data structure, see `references/pydantic-models.md`.
- **Custom Rules**: For validating specific formats like emails or password strength, see `references/custom-validators.md`.
- **Complex Scenarios**: For validating query parameters, file uploads, or dependencies between fields, see `references/advanced-validation.md`.
- **Error Responses**: To customize how validation errors are returned to the client, see `references/error-handling.md`.

## Resources

### `references/`

- **`pydantic-models.md`**: Guide to creating basic Pydantic models for request body validation.
- **`custom-validators.md`**: How to write custom validator functions for fields.
- **`advanced-validation.md`**: Covers cross-field validation, query parameters, and file uploads.
- **`error-handling.md`**: Instructions for creating a custom FastAPI exception handler for validation errors.

### `scripts/`

- **`validators.py`**: A collection of reusable Pydantic validator functions (e.g., for email, password strength).
- **`error_handler.py`**: A pre-built FastAPI exception handler for `RequestValidationError`.
- **`main_example.py`**: A full FastAPI application demonstrating all validation techniques covered in this skill. You can run this file to see the validation in action.
