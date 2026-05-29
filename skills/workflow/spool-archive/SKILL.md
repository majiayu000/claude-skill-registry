---
name: spool-archive
description: Archive a completed change and update main specifications. Use when the user has finished implementing and wants to integrate the change into the main codebase.
---

Run the CLI-generated archive instructions for a specific change.

**Rules**

- Do NOT archive without explicit user confirmation.

**Steps**

1. Determine the target change ID:
   - If the user provided a change ID, use it.
   - If no change ID was provided, run:
      ```bash
      spool list --completed --json
      ```
      - Related filters (not for archiving, but useful for triage):
        ```bash
        spool list --partial
        spool list --pending
        ```
      - If no completed changes exist, inform the user: "No completed changes found. Run `spool list` to see all changes and their status."
      - If one or more completed changes exist, present them to the user and ask which one to archive.

2. Generate instructions (source of truth):

   ```bash
   spool agent instruction archive --change "<change-id>"
   ```

3. Follow the printed instructions exactly.
