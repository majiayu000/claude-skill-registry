---
name: spool-review
description: Review and validate Spool changes, specs, or implementations. Use when the user wants a quality check, code review, or validation of project artifacts.
---

Run the CLI-generated review instructions for a specific change.

**Steps**

1. Determine the target change ID (ask the user if unclear).

2. Generate instructions (source of truth):

   ```bash
   spool agent instruction review --change "<change-id>"
   ```

3. Follow the printed instructions exactly.
