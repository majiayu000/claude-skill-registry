---
name: env-handler
description: Manage environment variables securely. Handles distinction between .env (template) and .env.local (secrets).
---

# Environment Variable Handler

## Core Rules
1.  **NO `.env.example`**: Do not create this file. Use `.env` as the template.
2.  **Secrets in `.env.local`**: Actual sensitive values must live in `.env.local` (git-ignored).
3.  **Placeholders**: Every variable in `.env.local` MUST have a corresponding entry in `.env`.
    -   If sensitive: `KEY=""`
    -   If public/common: `KEY="default_value"`

## Instructions

### 1. Adding a New Sensitive Variable
When you need to add a secret (e.g., `REPLICATE_API_TOKEN`):

1.  **Update `.env`**:
    Add the variable with an empty string value.
    ```bash
    # .env
    REPLICATE_API_TOKEN=""
    ```

2.  **Ask the User**:
    Explicitly request the user to add the actual value to their local secrets file.
    > "I have added `REPLICATE_API_TOKEN` to your `.env` file. Please open `.env.local` and add the actual token: `REPLICATE_API_TOKEN=your_token_here`"

### 2. Adding a Non-Sensitive Variable
When adding a public or configuration variable (e.g., `NEXT_PUBLIC_APP_URL`):

1.  **Update `.env`**:
    Add the variable with its default or development value.
    ```bash
    # .env
    NEXT_PUBLIC_APP_URL="http://localhost:3000"
    ```

### 3. Reading Variables
-   Server-side: `process.env.KEY`
-   Client-side: `process.env.NEXT_PUBLIC_KEY`

## Checklist
- [ ] Is the variable in `.env`?
- [ ] If sensitive, is the value in `.env` empty?
- [ ] Did I ask the user to update `.env.local`?

