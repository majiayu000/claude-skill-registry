---
name: run-shell-command-with-long-output
description: Run shell commands where long (many tokens) output is expected. Use when
  you need to
---

---
name: run-shell-command-with-long-output
description: Run shell commands where long (many tokens) output is expected. Use when you need to
run some command where you care only about gist of the output (like what failed, or if command was successful).
---

# Run Shell Commands With Long Output

Runs command through copilot CLI to get just the gist of output.

## Instructions

Ask copilot CLI to run the command for you and to provide you with just the details you need from the command's output. Use the `copilot -p "<instructions for copilot>" --model claude-haiku-4.5 --allow-all-tools` command.

Example:

```sh
copilot -p "Build the app with command 'just build' and tell me whether the result is successful(then just say 'success'), or not (then provide all the available details on what the issue is). Do not try any fixes or modifications!" --model claude-haiku-4.5 --allow-all-tools
```
