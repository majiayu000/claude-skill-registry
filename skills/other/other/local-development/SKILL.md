---
name: local-development
description: Running functions and web app locally, troubleshooting emulator issues, Storybook. Use when running or debugging locally.
---

# Local Development

## When to Use

Use this skill when running the web app or functions locally, troubleshooting emulator issues, or running Storybook.

## Important

The user runs functions and web app locally for testing. Claude writes code and creates PRs -- Claude does NOT deploy or run dev servers.

## Running Functions Locally (user runs this)

```bash
npx nx run functions:serve
```

This command:
1. Builds the functions
2. Copies `.env.dev` to `dist/apps/functions/.env`
3. Starts watch mode for rebuilds (background)
4. Runs `firebase serve --only functions --project=dev` on port 5001

## Running Web App Locally (user runs this)

```bash
npx nx run maple-spruce:serve
```

Runs on http://localhost:3000

## Running Storybook

```bash
npx nx run maple-spruce:storybook
# Opens http://localhost:6006
```

Building Storybook:
```bash
npx nx run maple-spruce:build-storybook
# Output: dist/storybook/maple-spruce
```

## Running Tests

```bash
npm test
```

## Deployment

User decides when to deploy to dev. Production deploys automatically via CI/CD on merge to main.

## Troubleshooting Local Functions

### Emulator prompts for environment variables

The Firebase emulator is not finding the `.env` file. This happens when:
- The build clears `dist/apps/functions/` before the `.env` is copied
- A stale watch process is interfering

**Fix:**
```bash
# Kill any stale processes
pkill -f "firebase serve"
pkill -f "nx run functions"

# Clean and restart
rm -rf dist/apps/functions
npx nx run functions:serve
```

**Why this happens:**
- Firebase reads `.env` from `dist/apps/functions/`
- The `nx run functions:build` clears this directory
- The serve command copies `.env.dev` after build, before starting the emulator
- If ordering is wrong or stale processes exist, the emulator starts without the `.env`

**Key indicator it's working:**
```
i  functions: Loaded environment variables from .env.
```
