---
name: fastapi-jwt-auth
description: "Provides a complete solution for JWT-based authentication in FastAPI applications. Use this skill when a user wants to add secure token-based authentication to their FastAPI project. This skill handles JWT creation, decoding, signature and expiration verification, password hashing, and custom claims. It includes patterns for login endpoints, protected routes using dependencies, role-based access control decorators, token refresh mechanisms, and middleware-based validation."
---

# FastAPI JWT Authentication

This skill provides a robust and reusable solution for implementing JWT (JSON Web Token) authentication in FastAPI applications. It includes a Python script with core authentication logic and a detailed guide with integration patterns.

## Bundled Resources

This skill comes with the following pre-packaged resources:

- **`scripts/jwt_auth.py`**: A Python script containing all the core utility functions for handling JWTs. This includes:
    - Password hashing and verification (`passlib`).
    - Access and refresh token creation (`python-jose`).
    - Token decoding and validation.
    - A FastAPI dependency (`get_current_user`) for protecting endpoints.

- **`references/fastapi_integration.md`**: A comprehensive guide with code examples and patterns for integrating the authentication logic into a FastAPI application.

## Workflow

When a user asks to implement JWT authentication in FastAPI, follow this workflow:

### 1. Understand the User's Requirements

First, clarify the specific needs of the user:
- What custom claims should be in the token (e.g., `user_id`, `roles`, `email`)?
- Do they need role-based access control (RBAC)?
- Do they have an existing user model and database setup?

### 2. Review the Core Logic (If Necessary)

The core, reusable authentication logic is in `scripts/jwt_auth.py`. You should **not** need to modify this file in most cases. Familiarize yourself with the functions it provides:
- `create_access_token()` and `create_refresh_token()`
- `verify_password()` and `get_password_hash()`
- `get_current_user()` (the main dependency for protected routes)

### 3. Implement the Integration Patterns

The primary guide for implementation is `references/fastapi_integration.md`. **Read this file carefully.** It contains all the necessary code patterns to add authentication to the user's application.

Follow the steps outlined in the reference guide:
1.  **Setup and Dependencies**: Instruct the user on installing the required packages.
2.  **Pydantic Models**: Help the user create or update their Pydantic models for users and tokens.
3.  **Login Endpoint**: Use the pattern from the guide to create a `/token` endpoint that issues access and refresh tokens.
4.  **Protected Endpoints**: Use the `get_current_user` dependency to protect routes that require authentication.
5.  **Role-Based Access**: If required, use the decorator pattern from the guide to implement role-based access control.
6.  **Token Refresh**: Implement a `/refresh` endpoint so clients can get new access tokens.

Your goal is to adapt the patterns from `references/fastapi_integration.md` to the user's existing codebase, providing them with a fully working authentication system.
