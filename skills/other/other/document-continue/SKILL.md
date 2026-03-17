---
name: document-continue
description: Save current progress to a file before /clear so a fresh session can continue where you left off. Use when context is getting full mid-task.
disable-model-invocation: true
---

# Document & Continue

When context is getting full mid-task, save progress before `/clear`.

## Steps

1. **Create progress file** at `docs/plans/PROGRESS-<task-id>.md` (create `docs/plans/` if it doesn't exist: `mkdir -p docs/plans`) with:
   ```markdown
   # Progress: <Task Title>

   **Beads task:** <id>
   **Branch:** <current branch name>
   **Plan:** <path to plan file if one exists>
   **Step:** <current step number in plan>

   ## Modified Files
   - list every file changed in this session

   ## Intent
   - what you were trying to accomplish and WHY (not just what files changed)
   - the high-level goal this work serves

   ## Current State
   - what's working
   - what's failing (include test names and error messages)

   ## Next Steps
   - exactly what to do next
   - any decisions made with the user during this session
   ```

2. **User runs** `/clear`

3. **New session starts with:** "Read `docs/plans/PROGRESS-<task-id>.md` and continue from there"

## Tips

- Include exact test commands that were run
- Include any user decisions or preferences expressed during the session
- Be specific about what's left — "implement the remaining 3 mutations" not "finish the feature"
