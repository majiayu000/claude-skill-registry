---
name: test-parallel-a
description: Child A for parallel test
context: fork
---
Write the current timestamp (date +%s.%N) to /tmp/parallel-a-time.txt
Sleep for 3 seconds: sleep 3
Write "CHILD_A_DONE" to /tmp/parallel-a-done.txt
