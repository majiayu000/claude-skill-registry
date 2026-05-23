---
name: managing-env-vars
description: Manages environment variables and security. Distinguishes between public and secret keys. Use when setting up project configuration or adding API keys.
---

# Environment and Security Variables

## When to use this skill
- During project setup.
- When adding new Appwrite services (Storage, Databases).
- When deploying to production.

## Workflow
- [ ] Create `.env.local` for local development.
- [ ] Distinguish between `NEXT_PUBLIC_` (Client access) and secret keys (Server access).
- [ ] Add `.env*` to `.gitignore`.
- [ ] Use `process.env.VARIABLE_NAME` with fallback or validation.

## Required Variables
- `NEXT_PUBLIC_APPWRITE_ENDPOINT`: Your Appwrite API endpoint.
- `NEXT_PUBLIC_APPWRITE_PROJECT_ID`: Your project ID.
- `APPWRITE_API_KEY`: Secret key for server-side operations (DO NOT prefix with NEXT_PUBLIC).

## Instructions
- **Leak Prevention**: Never commit `.env` files.
- **Validation**: Use a `env.ts` file with Zod to validate variables at runtime if possible.
