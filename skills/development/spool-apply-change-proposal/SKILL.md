---
name: spool-apply-change-proposal
description: Use when implementing, executing, applying, building, coding, or developing a feature, change, requirement, enhancement, fix, or modification. Use when running tasks from a spec, proposal, or plan.
---

Run the CLI-generated apply instructions for a specific change.

**Testing Policy (TDD + coverage)**

- Default workflow: RED/GREEN/REFACTOR (write a failing test, implement the minimum to pass, then refactor).
- Coverage target: 80% (guidance; projects may override in `.spool/config.json`).
- Follow the "Testing Policy" section printed by `spool agent instruction apply`; it should reflect project configuration.

**Steps**

1. Determine the target change ID.

   - If the user provides one, use it.
   - Otherwise run `spool list --ready` to see changes ready for implementation.
   - Ask the user which change to apply if multiple are ready.

2. Generate instructions (source of truth):

   ```bash
   spool agent instruction apply --change "<change-id>"
   ```

3. Follow the printed instructions exactly.

4. Use `spool tasks ready <change-id>` to see actionable tasks at any point.
