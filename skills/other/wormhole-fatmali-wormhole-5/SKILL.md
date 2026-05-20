---
name: wormhole
description: Sync work between AI agents. Log actions, manage sessions, detect conflicts.
---

# Wormhole

Shared memory for AI agents. Log work so other agents know what you did.

## When to Use

| Situation | Tool |
|-----------|------|
| Starting work | `start_session` |
| After edits/commands | `log` |
| Resuming work | `get_recent` |
| Before editing | `check_conflicts` |
| Done | `end_session` |

## Tools

### log
```js
log({ action: "file_edit", agent_id: "claude-code", project_path: ".", content: { file_path: "src/x.ts", description: "Added auth" }})
```
Actions: `file_edit`, `cmd_run`, `decision`, `test_result`, `todos`

### start_session / end_session
```js
start_session({ project_path: ".", agent_id: "claude-code", name: "bugfix-auth" })
end_session({ session_id: "abc", summary: "Fixed timeout" })
```

### get_recent
```js
get_recent({ project_path: "." })
```

### check_conflicts
```js
check_conflicts({ project_path: ".", files: ["src/auth.ts"] })
```

## Tips
- Always start a session first
- Log significant actions only
- Use `get_recent` when resuming
