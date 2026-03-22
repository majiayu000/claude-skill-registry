---
name: prepare-app
description: "Starts development server for E2E testing. Detects package manager and verifies server startup. Triggers on keywords: prepare app, start server, dev server, start app"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
---

# Prepare App Command

Start the development server for E2E testing.

## Pre-Flight Checks

1. **Check for package.json**
   - If missing: STOP with "No package.json found"

2. **Check node_modules**
   - If missing: Run package manager install first (npm/pnpm/yarn install)

## Execution

1. **Start Development Server**
   - Run in background: `${DEV_SERVER_CMD:-pnpm dev}`
   - Wait 5 seconds for server startup

2. **Verify Server Running**
   - Check if port ${DEFAULT_PORT:-5173} is responding
   - If not responding after 10s: Report error

3. **Report Status**
   - Confirm server is running
   - Display URL: `http://localhost:${DEFAULT_PORT:-5173}/`

## Notes
- Server runs in background
- Use Ctrl+C in terminal to stop server
- Default port: 5173 (Vite default)
- Override with DEFAULT_PORT environment variable
- Override dev command with DEV_SERVER_CMD environment variable (e.g., "npm run dev")
