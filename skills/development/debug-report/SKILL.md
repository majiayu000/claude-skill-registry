---
description: How to debug a codebase when a test case fails to pass. If you cannot figure it out, how to report the bug through a Github Issue.
name: Debugging Report
---

If you failed to pass a test case, you should:
1. Read the name of the test case to understand what is functionality is tested.
2. Backtrace the call stack to find the function where the error occurs.
3. Check if you give the correct input to this function.
4. Feel free to add `print` statements to have the intermediate values printed to:
   1. locate where it goes to the wrong branch?
   2. where the value started to deviate from expected value and what is the right value at that point?
5. If you still cannot figure it out, stop and dump the phenomenon to user for help. This report should include:
   1. The name of the test case that fails.
   2. The error message and the call stack trace.
   3. The input values to the function where the error occurs.
   4. What is the value you observed at that point?
   5. What is the expected value at that point?
   6. Any other relevant information you think might help.
6. If this bug is related to an issue implementation (which can be found on your branch name), please upload this bug to this issue for user intervention.
7. If not, dump the above to the screen.