---
name: warp-fork
description: Fork a warp route from the local HTTP registry for development and testing. Use when the goal is try to simulate transactions on a set of anvil forks.
---

# Warp Fork

Fork a warp route using the local HTTP registry.

**Instructions:**

0. Check if `http://localhost:3333` is running. If not, run the start-http-registry SKILL. If that fails, use `AskUserQuestion` to prompt the user for an alternate registry URL to use instead of `http://localhost:3333`.

1. First, use `AskUserQuestion` to prompt the user for the warp route ID:
   - Question: "Which warp route would you like to fork?"
   - Header: "Warp Route"
   - Options: Provide 2-3 common examples if known, otherwise use generic placeholders. Note that the fork may fail if the warp routes are invalid. Re-prompt the user!

2. Run the command in the background:

   ```bash
   pnpm -C typescript/cli exec tsx cli.ts warp fork --registry $REGISTRY --warpRouteId $WARP_ROUTE_ID
   ```

   - Use the registry URL from step 0 for $REGISTRY (`http://localhost:3333` by default, or user-provided if the local registry failed)
   - Use `run_in_background: true` so it doesn't block the conversation.

3. After starting, report the task/shell ID and the fork registry server port back to the user.

4. Remind the user they can stop it later with `KillShell` using that ID

**Prerequisites:**

- The http-registry server must be running on port 3333. If not, start it first with `/start-http-registry`.

**Example output:**

> Started warp fork for `EZETH/ethereum-megaeth` in background (shell ID: `shell_abc123`).
> To stop it later, I can use KillShell with that ID.
