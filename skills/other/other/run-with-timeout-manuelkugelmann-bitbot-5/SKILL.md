---
name: run-with-timeout
description: Run commands with timeout protection to prevent hanging. Use for potentially long-running tests or operations.
---

# Run With Timeout

Execute commands with timeout protection.

```bash
.claude/skills/run-with-timeout/scripts/run-with-timeout.sh 60 ./test-script.sh
```

Returns exit code 124 if timeout exceeded, otherwise command's exit code.
