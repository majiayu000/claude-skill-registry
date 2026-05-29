---
name: handling-global-errors
description: Unified strategy for catching and displaying API and network errors. Use throughout the application logic.
---

# Global Error Handling System

## When to use this skill
- Wrapping server actions.
- Client-side API calls.
- Handling 404/500 pages.

## Workflow
- [ ] Use `try-catch` blocks.
- [ ] Parse Appwrite errors (code 401, 404, etc.).
- [ ] Trigger Toast notification with user-friendly message.
- [ ] Log technical errors to a service (optional).

## Instructions
- **User Friendly**: Never show "Internal Server Error" to a user; show "Something went wrong on our end, please try again."
- **Specifics**: Distinguish between "Wrong Password" and "Server Unreachable".
