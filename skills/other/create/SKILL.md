---
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion, Bash(mkdir:*), Bash(echo $PPID), Bash(rm:*)
description: Create a new plan folder with a plan.md template
argument-hint: [plan name]
---

You are creating a new plan folder for the user.

To do this, follow these steps precisely:

1. Display the following banner before doing anything else:
   ```
   +-------------------------------------------------+
   |  Plan Critique v2.0.1 - Creating new plan       |
   +-------------------------------------------------+
   ```
2. Read `.claude/plan-critique-config.json` and get `plansFolder` path from settings.
   If the file doesn't exist or `plansFolder` is not set:
   - Ask the user: "Where would you like to store your plans? Provide a folder path (default `.planning`):".
     By default, the user should be presented with the option `.planning`.
   - Save the path as `plansFolder` in `.claude/plan-critique-config.json`
   - Create the folder if it doesn't exist
   - Create an `archived/` subfolder inside it
3. Determine the plan name:
   - If a name was passed as an argument, the text in `$ARGUMENTS` is the plan name. Use it directly.
   - Otherwise, ask the user directly, do not offer predefined options like "New Feature" or "Bug Fix"
     because the plan name must be unique: "Enter a name for this plan:"
   The plan name must have at least 3 characters. If it is empty or shorter, respond with
   "Plan name must be at least 3 characters." and ask the user to enter one.
4. Generate a slug from the plan name:
   - Convert to lowercase
   - Replace spaces with hyphens
   - Remove characters that are not alphanumeric or hyphens
   - Trim to max 50 characters
   - Example: "Add User Authentication" becomes `add-user-authentication`
5. Check if `[plansFolder]/[slug]/` already exists.
   If it does: Respond with "A plan with this name already exists at `[plansFolder]/[slug]/`. Choose a different name."
   Ask for a new name and repeat from step 4.
6. Create directory `[plansFolder]/[slug]/`
7. Link this session to the new plan:
   - Get the Claude Code process ID by running: `echo $PPID`
   - Create the sessions directory if needed: `[plansFolder]/.sessions/`
   - Write the slug to `[plansFolder]/.sessions/[PID]` (plain text, just the slug)
8. Create the plan template at `[plansFolder]/[slug]/plan.md` using the template in
   [plan-template.md](plan-template.md).
9. Respond with confirmation:
   ```
   Created new plan: [plansFolder]/[slug]/
   Edit your plan at: [plansFolder]/[slug]/plan.md
   When ready, run `/plan:critique` to review your plan.
   ```

Notes:

- The slug must be filesystem-safe (no special characters)
- Keep the original plan name with proper casing in the H1 heading of plan.md
- Only create plan.md initially (critique.md is created by `/plan:critique`)
- Always use `plansFolder` from settings as the base directory
