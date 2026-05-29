---
name: setup
description: Configures project permissions for the LearningAgents plugin. Adds required Bash and file access rules to .claude/settings.json.
---

# LearningAgents Setup

Configure the current project's `.claude/settings.json` so the LearningAgents plugin can run without permission prompts.

## Procedure

### 1. Read or initialize `.claude/settings.json`

Read `.claude/settings.json`. If it does not exist, start with:

```json
{
  "permissions": {
    "allow": []
  }
}
```

### 2. Add required permission rules

Add the following entries to `permissions.allow` if they are not already present:

| Rule | Purpose |
|------|---------|
| `Bash(learning_agents/scripts/*)` | Allow plugin scripts to run |
| `Bash(bash learning_agents/scripts/*)` | Allow plugin scripts invoked via `bash` |
| `Read(./.deepwork/tmp/**)` | Read session transcripts and temp files |
| `Write(./.deepwork/tmp/**)` | Write session logs and issue files |
| `Edit(./.deepwork/tmp/**)` | Edit issue files during investigation |

Do not duplicate rules that already exist. Preserve all existing rules and formatting.

### 3. Write `.claude/session_log_folder_info.md`

Create `.claude/session_log_folder_info.md` with content describing what was configured:

```
LearningAgents plugin setup completed.

Permissions added to .claude/settings.json:
- Bash(learning_agents/scripts/*) — plugin scripts
- Bash(bash learning_agents/scripts/*) — plugin scripts via bash
- Read(./.deepwork/tmp/**) — read session data
- Write(./.deepwork/tmp/**) — write session data
- Edit(./.deepwork/tmp/**) — edit session data
```

### 4. Confirm to the user

Tell the user setup is complete and they can now use `/learning-agents` commands.

## Guardrails

- Never remove existing permission rules
- Only add rules that are not already present
- Always create the setup info file so setup is not re-triggered
