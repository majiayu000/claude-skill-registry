---
name: jules-cli
description: Interact with the Jules CLI to manage asynchronous coding sessions. Use this skill sparingly for complex, isolated tasks that benefit from a remote VM.
binaries:
  - jules
  - python3
env:
  - HOME
---

# Jules CLI Skill

## Overview
This skill enables the agent to interact with the `jules` CLI. It supports task assignment, session monitoring, and result integration.

## Usage Guidelines (CRITICAL)

To prevent excessive and inappropriate session creation, you **must** follow these rules:

1.  **Local First**: If you can solve the task locally within your current environment (e.g., editing files, running tests, small refactors), **do not** use Jules.
2.  **Complexity Threshold**: Only use Jules for tasks that are:
    *   **Large-scale**: Touching many files or requiring significant architectural changes.
    *   **Isolated**: Benefiting from a clean, remote environment to avoid local dependency issues.
    *   **Exploratory**: Tasks where the solution isn't immediately obvious and requires iteration in a VM.
3.  **No Proliferation (One at a Time)**: 
    *   **Never** create multiple sessions for the same task.
    *   **Never** use a loop or parallel execution to spin up several sessions at once.
    *   Wait for a session to complete and inspect the results before deciding if another session is needed.
4.  **No "Small" Tasks**: Do not submit tasks like "Add a comment", "Change a variable name", or "Fix a typo".

---

## Security Guidelines

To ensure safe execution of CLI commands, you **must** adhere to the following security practices:

1.  **Input Validation**: Before running any command, validate that:
    *   **Repository names** follow the `owner/repo` format (alphanumeric, dots, hyphens, and underscores).
    *   **Session IDs** are alphanumeric (typically hyphens and underscores are also allowed).
2.  **Quoting**: Always wrap shell placeholders in double quotes (e.g., `"<repo>"`).
3.  **No Inline Injection**: Never embed user-provided data directly into script strings (like `python3 -c`). Use environment variables to pass such data safely.
4.  **Sanitization**: Ensure task descriptions do not contain malicious shell characters if passed directly to the shell.

---

## Safety Controls
*   **Approval Required (MANDATORY)**: You **must** ask for explicit user approval before running any of the following commands:
    *   `jules remote new`: Since this creates a remote session/VM.
    *   `jules remote pull --apply`: Since this modifies the local codebase.
    *   `jules teleport`: Since this clones and modifies the environment.
*   **Verification**: Always run `jules remote list --session` before creating a new one to ensure you don't already have a pending session for the same repository.
*   **Credentials**: If `jules login` is required, explain *why* to the user and wait for their confirmation before proceeding.

---

## Core Workflow (Manual Control)

Prefer using the CLI directly to maintain situational awareness.

### 1. Pre-flight Check
Verify repository access and format.
```bash
jules remote list --repo
```
*Note: Ensure the repo format is `GITHUB_USERNAME/REPO`.*

### 2. Submit Task
Create a session and capture the Session ID.
```bash
# Capture the output to get the ID
# Replace <repo> and task description with validated inputs
jules remote new --repo "<repo>" --session "Detailed task description" < /dev/null
```

### 3. Monitor Progress
List sessions and look for your ID. Use this robust one-liner to check the status (it handles statuses with spaces like "In Progress"):

**Check Status (Safe Method):**
```bash
# Use an environment variable to pass the Session ID safely to Python
export JULES_SESSION_ID="<SESSION_ID>"
jules remote list --session | python3 -c "
import sys, re, os
session_id = os.environ.get('JULES_SESSION_ID', '')
if not session_id: sys.exit(0)
for line in sys.stdin:
    line = line.strip()
    if line.startswith(session_id):
        # Extract status (the last column after multiple spaces)
        print(re.split(r'\s{2,}', line)[-1])
"
unset JULES_SESSION_ID
```

### 4. Integrate Results
Once the status is **Completed**, pull and apply the changes.
```bash
# Replace <SESSION_ID> with the validated Session ID
jules remote pull --session "<SESSION_ID>" --apply < /dev/null
```

---

## Error Handling & Troubleshooting

*   **Repository Not Found**: Verify format with `jules remote list --repo`. It must match the GitHub path.
*   **TTY Errors**: Always use `< /dev/null` for non-interactive automation with the raw `jules` command.
*   **Credentials**: If you see login errors, ensure `HOME` is set correctly or run `jules login`.

---

## Command Reference

| Command | Purpose |
| :--- | :--- |
| `jules remote list --repo` | Verify available repositories and their exact names. |
| `jules remote list --session` | List active and past sessions to check status. |
| `jules remote new` | Create a new coding task. |
| `jules remote pull` | Apply changes from a completed session. |
| `jules teleport "<id>"` | Clone and apply changes (useful for fresh environments). |