---
name: dependency-management
description: Standardized protocol for managing project dependencies using `uv` and handling system-level requirements.
---

# Dependency Management Skill
Standardized protocol for managing project dependencies using `uv` and handling system-level requirements.

## 🎯 Purpose
- Ensure consistent environment setup across local and CI environments.
- Resolve "ModuleNotFoundError" and "Build Error" issues efficiently.
- Explicitly handle the boundary between Python packages and System libraries.

## 🛠️ Core Tools
- **uv**: The primary package manager. Use `uv add`, `uv remove`, `uv sync`.
- **System Package Managers**: `apt` (Linux), `brew` (macOS), `choco`/`winget` (Windows). **Note**: Agents cannot run `sudo`. Suggest commands to the user if needed.

## 📋 Protocols

### 1. Adding Python Dependencies
Always prefer the project's dependency management over direct `pip` installs.
```bash
# Good
uv add package_name
uv add --dev package_name (for test/lint tools)

# Avoid (unless for checking versions)
uv pip install package_name
```

### 2. Identifying System Dependencies
If `uv add` fails with a compilation error (e.g., `pkg-config: not found`, `Could not find <header.h>`, `failed to build <package>`), it is likely a missing system library.

#### Common Patterns:
- **Pango/Cairo (Manim)**: Requires `libpango1.0-dev`, `libcairo2-dev`, `libffi-dev`.
- **CV2/Image Processing**: Requires `libgl1`.
- **FFmpeg**: Required for media operations.
- **Postgres (psycopg2)**: Requires `libpq-dev`.

### 3. Resolution Workflow
1. **Analyze Error**: Check the `stderr` for "missing", "not found", or "fatal error".
2. **Search for Package**: Use `apt-cache search` or `find` to see if it exists.
3. **Escalate**: If it requires `sudo apt install`, notify the user with the exact command.
   > [!IMPORTANT]
   > Do NOT attempt to run `sudo` commands. Provide the command to the user as a recommendation.

### 4. Updating Skill Registry
If a new skill requires specific system dependencies, document them in the skill's `SKILL.md` under a `Dependencies` section.

## 🚀 Examples

### Successful uv Add
```bash
uv add pydantic
```

### System Dependency Escalation
"I attempted to install `manim` using `uv`, but it failed because the system library `pangocairo` is missing. Please run the following command on your host to fix it:
`sudo apt-get install libpango1.0-dev libcairo2-dev`"
