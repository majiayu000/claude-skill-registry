---
name: start-http-registry
description: Start the local HTTP registry server for development. Use when testing infra scripts or commands that need a Abacus work private overrides such as RPC URLS.
---

# Start HTTP Registry Server

Start the http-registry server in the background.

**Instructions:**

1. First, find the monorepo root (working directory may have drifted):
   ```bash
   git rev-parse --show-toplevel
   ```
2. Run the command with `run_in_background: true`, prefixing with `cd` to the monorepo root:
   ```bash
   cd <MONOREPO_ROOT> && pnpm -C typescript/infra start:http-registry
   ```
3. After starting, report the task/shell ID to the user
4. Remind the user they can stop it later with `KillShell` using that ID
5. Note the URL that the registry is running on, which would be `http://localhost:<port>`, where the port can be found in the logs.

**Example output:**

> Started http-registry server in background (shell ID: `shell_abc123`).
> To stop it later, I can use KillShell or you can run `/stop-http-registry`.
