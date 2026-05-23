---
name: openspec-archive-change
description: Archive a completed change in the experimental workflow. Use when the user wants to finalize and archive a change after implementation is complete.
---

Archive a completed change in the experimental workflow.

**Input**: Optionally specify a change name. If omitted, MUST prompt for available changes.

**Steps**

1. **If no change name provided, prompt for selection**

   Run `openspec list --json` to get available changes. Use the **AskUserQuestion tool** to let the user select.

   Show only active changes (not already archived).
   Include the schema used for each change if available.

   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check artifact completion status**

   Run `openspec status --change "<name>" --json` to check artifact completion.

   Parse the JSON to understand:
   - `schemaName`: The workflow being used
   - `artifacts`: List of artifacts with their status (`done` or other)

   **If any artifacts are not `done`:**
   - Display warning listing incomplete artifacts
   - Use **AskUserQuestion tool** to confirm user wants to proceed
   - Proceed if user confirms

3. **Check task completion status**

   Read the tasks file (typically `tasks.md`) to check for incomplete tasks.

   Count tasks marked with `- [ ]` (incomplete) vs `- [x]` (complete).

   **If incomplete tasks found:**
   - Display warning showing count of incomplete tasks
   - Use **AskUserQuestion tool** to confirm user wants to proceed
   - Proceed if user confirms

   **If no tasks file exists:** Proceed without task-related warning.

4. **Check if delta specs need syncing**

   Check if `specs/` directory exists in the change with spec files.

   **If delta specs exist, perform a quick sync check:**

   a. **For each delta spec** at `openspec/changes/<name>/specs/<capability>/spec.md`:
      - Extract requirement names (lines matching `### Requirement: <name>`)
      - Note which sections exist (ADDED, MODIFIED, REMOVED)

   b. **Check corresponding main spec** at `openspec/specs/<capability>/spec.md`:
      - If main spec doesn't exist → needs sync
      - If main spec exists, check if ADDED requirement names appear in it
      - If any ADDED requirements are missing from main spec → needs sync

   c. **Report findings:**

      **If sync needed:**

      ```
      ⚠️ Delta specs may not be synced:
      - specs/auth/spec.md → Main spec missing requirement "Token Refresh"
      - specs/api/spec.md → Main spec doesn't exist yet

      Would you like to sync now before archiving?
      ```

      - Use **AskUserQuestion tool** with options: "Sync now", "Archive without syncing"
      - If user chooses sync, execute /opsx:sync logic (use the openspec-sync-specs skill)

      **If already synced (all requirements found):**
      - Proceed without prompting (specs appear to be in sync)

   **If no delta specs exist:** Proceed without sync-related checks.

5. **Perform the archive**

   Create the archive directory if it doesn't exist:

   ```bash
   mkdir -p openspec/changes/archive
   ```

   Generate target name using current date: `YYYY-MM-DD-<change-name>`

   **Check if target already exists:**
   - If yes: Fail with error, suggest renaming existing archive or using different date
   - If no: Move the change directory to archive

   ```bash
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```

6. **Display summary**

   Show archive completion summary including:
   - Change name
   - Schema that was used
   - Archive location
   - Whether specs were synced (if applicable)
   - Note about any warnings (incomplete artifacts/tasks)

**Output On Success**

```
## Archive Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** ✓ Synced to main specs (or "No delta specs" or "⚠️ Not synced")

All artifacts complete. All tasks complete.
```

**Guardrails**

- Always prompt for change selection if not provided
- Use artifact graph (openspec status --json) for completion checking
- Don't block archive on warnings - just inform and confirm
- Preserve .openspec.yaml when moving to archive (it moves with the directory)
- Show clear summary of what happened
- If sync is requested, use openspec-sync-specs approach (agent-driven)
- Quick sync check: look for requirement names in delta specs, verify they exist in main specs
