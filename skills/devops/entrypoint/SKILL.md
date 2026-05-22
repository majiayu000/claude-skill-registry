---
name: entrypoint
description: Generates entrypoint.sh script for Docker container runtime environment variable injection. Replaces placeholder values in built assets with actual environment variables at container startup.
---

# Entrypoint Script Skill

## Purpose
Generate entrypoint.sh script for Docker container runtime environment variable injection.

## Output
Create the file: `entrypoint.sh` in the root directory

## Example File
See: `examples.md` in this directory for complete examples and detailed explanations.

## Conditional Logic

### JS Environment Substitution
- **If** `application_type: "standalone"` → Include the for loop that processes app*.js files with envsubst
- **If** `application_type: "micro-frontend"` → Omit the for loop (launcher handles environment injection)

Note: The `{{JS_ENV_SUBSTITUTION}}` placeholder in the template should be replaced with the actual for loop code or removed based on application_type.

## Notes
- Enables runtime environment variable injection into built assets
- Uses `envsubst` to replace placeholders with actual environment variable values
- Always processes index.html for VITE_CONTEXT_PATH
- Conditionally processes JavaScript files for standalone apps only
- Sets errexit and nounset for safer script execution
- Starts nginx in foreground mode for Docker container
- Requires gettext-base package for envsubst command
- Must be executable (chmod +x entrypoint.sh)

