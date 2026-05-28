---
name: script-executor
description: Executes shell scripts in a safe environment.
---
operations:
  execute_bash:
    description: Execute shell commands
    side_effects: potentially_destructive
    requires_human_approval: true

# Script Executor Skill

## 1. Objective
To execute provided shell scripts while enforcing security constraints (chmod +x, non-root).

## 2. Input
*   `script_path`: Absolute path to the .sh file.
*   `args`: Optional list of arguments.

## 3. Process
1.  Verify file existence.
2.  **Security Check:** Ensure the file has `chmod +x` (executable permission).
3.  Run the script using `subprocess`.
4.  Capture stdout/stderr.

## 4. Output
JSON object with exit code and logs.
