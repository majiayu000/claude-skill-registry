---
name: test-parallel-b
description: Child B for parallel test
context: fork
---
Write the current timestamp (date +%s.%N) to /tmp/parallel-b-time.txt
Sleep for 3 seconds: sleep 3
Write "CHILD_B_DONE" to /tmp/parallel-b-done.txt
