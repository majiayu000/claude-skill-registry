---
name: env-standalone
description: Conditionally generates .env.standalone file for micro-frontend applications only. Enables running micro-frontends in standalone mode without single-spa launcher. Skipped for standalone applications.
---

# Environment Standalone Skill

## Purpose
Generate `.env.standalone` file for running micro-frontend applications in standalone mode (without single-spa launcher).

**Note**: This file should ONLY be created for micro-frontend applications (`application_type: "micro-frontend"`). Standalone applications do NOT need this file.

## Input Parameters
- `application_type`: Should be "micro-frontend" to generate this file

## Output
Create the file: `.env.standalone` (only if `application_type === "micro-frontend"`)


## Notes
- **Micro-Frontend Only**: This file is only relevant for micro-frontend applications
- **Standalone Apps**: Do NOT create this file for standalone applications
- `.env.standalone` enables standalone mode for development without the launcher
- When `STANDALONE_SINGLE_SPA=true`, the micro-frontend app runs independently
- Useful for local development and testing without single-spa dependencies
- This file can be committed to the repository (no secrets)
- Use with `npm run dev:standalone` or similar script (if using Vite modes)
- The application will mount directly without waiting for single-spa lifecycle
