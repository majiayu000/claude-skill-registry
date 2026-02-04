---
name: jobs
description: Show current work status (active increments, progress) and background jobs (imports, cloning). Even with no jobs, shows increment summary and helpful context.
argument-hint: [--all] [--id job-id]
---

# Background Jobs Monitor

**NOTE**: This command is normally intercepted by the UserPromptSubmit hook for instant execution (<100ms). If the hook output isn't displayed, execute the CLI fallback below.

When this command is invoked, extract any arguments from the user's prompt and execute:

```bash
specweave jobs
```

If the user provided arguments (e.g., `/sw:jobs --all`), pass them to the command.

**CRITICAL**: Execute the command directly with NO commentary before or after. Show the output to the user.
