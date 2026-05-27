---
name: cc-soul-shutdown
description: Gracefully stop the cc-soul daemon
execution: inline
---

# cc-soul-shutdown

Stop the chittad daemon gracefully.

## Usage

```bash
${CLAUDE_PLUGIN_ROOT}/hooks/subconscious.sh stop
```

This will:
1. Send SIGTERM to daemon process
2. Wait for graceful shutdown (saves learner state)
3. Force kill if still running after timeout
4. Clean up PID file
