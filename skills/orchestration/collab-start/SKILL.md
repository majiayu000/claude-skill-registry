---
name: collab-start
description: Start the mermaid-collab server and begin a collab session
user-invocable: true
allowed-tools: Bash, Skill
---

# Start Collab

Quick-start command that ensures the server is running and launches a collab session.

---

## Step 1: Check Server Status

```bash
curl -s http://localhost:3737 > /dev/null 2>&1 && echo "running" || echo "not running"
```

---

## Step 2: Start Server If Needed

**If not running:**

Get the plugin install path and start the server:

```bash
bun run <plugin-path>/bin/mermaid-collab.ts start
```

Where `<plugin-path>` is the directory containing this skill (the plugin root).

To find the plugin path, use the path of this skill file and go up two directories:
- This skill is at: `<plugin-path>/skills/collab-start/SKILL.md`
- Plugin root is: `<plugin-path>/`

Wait for server to start (the CLI will confirm).

**If already running:** Continue to Step 3.

---

## Step 3: Invoke Collab Skill

```
Invoke skill: collab
```

This hands off to the collab skill which will:
- Show existing sessions or create a new one
- Guide through the full collab workflow

---

## Notes

- This is a convenience command combining server startup + collab workflow
- The server runs in background and persists across sessions
- Use `bun run <plugin-path>/bin/mermaid-collab.ts stop` to stop the server manually
