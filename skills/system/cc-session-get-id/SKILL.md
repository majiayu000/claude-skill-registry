---
name: cc-get-session-id
description: Get the current Claude Code session ID. Use when you need to reference or display the session ID.
---

# Get Session ID

Run this to get the current session ID:

```bash
CWD_HASH=$(echo -n "$PWD" | md5 | cut -c1-8)
cat "/tmp/claude-session-id-${CWD_HASH}" 2>/dev/null || cat /tmp/claude-session-id
```

The session ID is a UUID like `d201921f-1916-4ad3-bca8-74f8d54e9da1`.
