---
name: init-pixi-project
description: Initialize and scaffold a new Pixi-managed Python project, or upgrade an existing one. Use when the user explicitly mentions "init", "initialize", or "setup" in conjunction with "pixi". Handles existing projects by prompting for confirmation before merging.
---

# Initialize Pixi Project

## References
- **Usage & Commands**: See [references/pixi-usage.md](references/pixi-usage.md) for details on `pixi search`, `add`, and `run`.

## Workflow

### 1. Safety Check & Parameters

1.  **Check for Existing Artifacts**: Look for `pixi.lock`, `pixi.toml`, or a `pyproject.toml` containing `[tool.pixi]`.
2.  **Prompt if Exists**: If any of these exist, **PAUSE and ASK** the user:
    > "Existing Pixi configuration detected. Proceeding will scaffold the directory structure and attempt to merge standard dependencies (scipy, ruff, etc.) into the current environment. This might affect existing functionality. Do you want to proceed?"
3.  **Abort if Rejected**: If the user declines, stop.
4.  **Determine Parameters** (if proceeding):
    - **Format**: Default to `pyproject` unless user specifies otherwise.
    - **Python Version**: Target one minor version behind latest stable (e.g., 3.12).

### 2. Initialization (Merge/Create)

Attempt to initialize Pixi.

- **Run**: `pixi init [PATH] --format [pyproject|pixi] -c conda-forge`
- **Handle Existing**:
    - If the command fails because the project is already initialized, verify that `[tool.pixi]` exists in the manifest.
    - If it exists, skip to the next step.
    - If `pyproject.toml` exists but lacks Pixi config, the agent should try to append the default Pixi configuration or ask the user if `pixi init` didn't do it automatically.

### 3. Post-Initialization Configuration

#### A. Handle Custom Project Name
If the user specified a project name different from the current directory name:
1.  **Rename Source**: `mv src/<dir_name> src/<project_name>`
2.  **Update Manifest**: Edit `pyproject.toml` to replace the old name with the new one in:
    - `[project] name = "..."`
    - `[tool.pixi.pypi-dependencies]` section (rename the key).

#### B. Scaffolding (Idempotent)
Run the scaffolding script. Pass the project name if custom.

```bash
python <path_to_skill>/scripts/scaffold_structure.py [PATH] --package-name <project_name>
```

#### C. Gitignore
Check `.gitignore`. Append the following if not present:
```gitignore
.pixi/
tmp/
.git/
```

#### D. Install Python and Dependencies (Smart Merge)

1.  **Check Python**: Check if `python` is already a dependency.
    - If yes, respect the existing version (or ask user if they want to override).
    - If no, add it: `pixi add python=<version>`
2.  **Add Standard Packages**:
    - Attempt to add the standard stack:
      ```bash
      pixi add --pypi scipy mdutils ruff mkdocs-material mypy attrs omegaconf imageio
      ```
    - **Conflict Handling**: If `pixi add` fails due to conflicts with existing packages, try to resolve by:
        - Installing the non-conflicting subset.
        - Reporting specific conflicts to the user and asking for guidance.
3.  **Finalize**: Run `pixi install`.

### 4. Verification

- Verify the environment is usable (`pixi shell` works).
- Verify directory structure.
