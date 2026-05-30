---
description: Sync work between AI agents. Log actions, manage sessions, detect conflicts.
---

# Wormhole

Shared memory for AI agents. **Log every significant action** so others stay in sync.

## 🚨 Minimal Workflow

> Use the **absolute path of the current project directory** for every `project_path` (e.g., `/Users/you/Code/wormhole`). Avoid `.`.

1. `start_session` when you begin.
2. Pull context: `search_project_knowledge` + `get_recent`.
3. Before edits: `check_conflicts` on files.
4. During work: `log` every file_edit, cmd_run, decision, test_result, todos.
5. Capture learnings: `save_knowledge` (decisions/pitfalls/conventions/constraints).
6. Finish with `end_session` + summary.

## ✅ Logging Rules (no exceptions)

- After editing any file (include file_path + diff).
- After running commands (command + exit_code).
- After decisions, test results, todos, plan_output, feedback.

## Core tools (compact)

### start_session
```js
start_session({ project_path: "/absolute/path/to/project", agent_id: "github-copilot", name: "task-name" })
```

### log (use most)
```js
log({
  action: "file_edit",
  agent_id: "github-copilot",
  project_path: "/absolute/path/to/project",
  content: {
    file_path: "src/auth.ts",
    description: "Add JWT validation",
    diff: "--- a/src/auth.ts\n+++ b/src/auth.ts\n@@ ..."
  },
  tags: ["auth"]
})
```
Other actions: `cmd_run`, `decision`, `test_result`, `todos`, `plan_output`, `feedback`.

### get_recent
```js
get_recent({ project_path: "/absolute/path/to/project", related_to: ["src/auth.ts"] })
```

### check_conflicts
```js
check_conflicts({ project_path: "/absolute/path/to/project", files: ["src/auth.ts"] })
```

### search_project_knowledge (pull context)
```js
search_project_knowledge({ project_path: "/absolute/path/to/project", intent: "debugging", query: "auth" })
```

### save_knowledge (store learnings)
```js
save_knowledge({
  project_path: "/absolute/path/to/project",
  knowledge_type: "pitfall",
  title: "Avoid fs.readFileSync in handlers",
  content: "Blocks event loop; causes timeouts"
})
```

### end_session
```js
end_session({ session_id: "abc-123", summary: "Fixed auth timeout; tests pass" })
```

## 📋 Tiny workflow

```js
start_session({ project_path: "/absolute/path/to/project", agent_id: "github-copilot", name: "fix-auth" })
search_project_knowledge({ project_path: "/absolute/path/to/project", intent: "debugging", query: "auth" })
get_recent({ project_path: "/absolute/path/to/project" })
check_conflicts({ project_path: "/absolute/path/to/project", files: ["src/auth.ts"] })
log({ action: "file_edit", agent_id: "github-copilot", project_path: "/absolute/path/to/project", content: { file_path: "src/auth.ts", description: "Fix timeout" } })
log({ action: "cmd_run", agent_id: "github-copilot", project_path: "/absolute/path/to/project", content: { command: "npm test", exit_code: 0 } })
save_knowledge({ project_path: "/absolute/path/to/project", knowledge_type: "decision", title: "Use async DB client", content: "Prevents blocking" })
end_session({ session_id: "abc-123", summary: "Auth fixed; tests green" })
```
