---
name: setup
description: "Scaffold project: clone repo, install real library. Only invoke when explicitly requested by the user or by the yoink orchestrator."
argument-hint: "[--url GITHUB_URL] [--package PACKAGE_NAME]"
---

# Setup

> **Do not invoke this skill unless explicitly requested.** It is called by `/yoink:yoink` or run standalone by the user.

Execute the setup script to scaffold the project:

```bash
"${CLAUDE_SKILL_DIR}/scripts/setup.sh" $ARGUMENTS
```

After the setup script runs, print its full output to the user verbatim.

CRITICAL: After setup completes, check the cloned repo for a Python package (e.g., `pyproject.toml`, `setup.py`, or `setup.cfg` in `.yoink/reference/`). If none are found, inform the user that YOINK currently only supports Python packages and exit. You MUST NOT proceed to subsequent phases.
