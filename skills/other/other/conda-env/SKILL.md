---
name: conda-env
description: Conda environment activation for Python commands. Use when running Python scripts, pip, or conda-dependent tools.
user-invocable: false
---

# Conda Environment Management

Claude Code runs in a non-interactive shell where conda isn't automatically initialized. Always source the conda setup script before activating environments.

## Activation Pattern

```bash
source ~/miniconda3/etc/profile.d/conda.sh && conda activate ENV_NAME && YOUR_COMMAND
```

Or for miniforge3:
```bash
source ~/miniforge3/etc/profile.d/conda.sh && conda activate ENV_NAME && YOUR_COMMAND
```

> **Customize**: Replace `~/miniconda3` or `~/miniforge3` with your actual conda installation path. Find it with `conda info --base`.

## Before Running Commands

1. **Check if the project has a conda environment:**
   - Look for `environment.yml`, `environment.yaml`, or conda env name in project's `.claude/CLAUDE.md`
   - Check for an env name matching the project directory name

2. **List available environments:**
   ```bash
   source ~/miniconda3/etc/profile.d/conda.sh && conda env list
   ```

3. **If the project specifies a conda environment**, always activate it before running:
   - Python scripts
   - Shell commands that depend on conda packages
   - Tools like quarto (in some setups)

## Package Installation

**Always install packages into the project's conda environment, never into the system Python or base env.**

1. **Prefer `conda install`** — it resolves dependencies against the full environment:
   ```bash
   source ~/miniconda3/etc/profile.d/conda.sh && conda activate ENV_NAME && conda install PACKAGE
   ```

2. **Fall back to `pip` only within the active conda env** — if a package isn't available via conda/conda-forge:
   ```bash
   source ~/miniconda3/etc/profile.d/conda.sh && conda activate ENV_NAME && pip install PACKAGE
   ```

3. **Never run bare `pip install`** without first activating the project's conda environment. This would install into the wrong Python and cause confusion.

4. When suggesting install commands to users (e.g., for students or collaborators), always include the conda activation step.

## One-Time Configuration

Run once on a new machine to ensure consistent package resolution:

```bash
conda config --set channel_priority strict
conda config --set solver libmamba
conda config --add channels conda-forge
```

- **strict channel priority**: When a package exists in multiple channels, conda uses only the highest-priority channel. Prevents mixing incompatible builds.
- **libmamba solver**: Dramatically speeds up environment creation and package installation. The default solver can be very slow with complex dependencies.
- **conda-forge channel**: Community-maintained packages, often more up-to-date than `defaults`.

## Environment Export

Always use `--from-history` for portable environment files:

```bash
conda env export --from-history > environment.yml
```

This records only explicitly installed packages (not platform-specific transitive dependencies), making the file portable across OS and architectures.

## Shared Environments

### `lab-general` — shared environment for general projects

All general-type projects (documentation sites, infrastructure tools, Quarto books, utility scripts) use the shared `lab-general` conda environment by default, regardless of whether they currently use Python. This ensures a consistent environment is always available if Python is needed later.

**Contents:** python 3.11, ipykernel, pyyaml, requests, pandas

**When to use `lab-general`:**
- Documentation projects (Quarto books/sites)
- Infrastructure and tooling projects
- Small utility scripts that don't need specialized packages
- Any `project-type: general` project without complex dependencies

**When to create a project-specific env instead:**
- The project needs packages that would conflict with or bloat `lab-general`
- The project has strict reproducibility requirements (pin exact versions)
- Data science projects (always project-specific — see lab policy below)

**Identifying which env a project uses:** Check the project's `.claude/CLAUDE.md` — it will say either `lab-general` (shared) or `{project_name}` (project-specific) in the Environment section.

## Lab Policy

1. **Never install into the `base` environment** — always use a named environment
2. **Data science projects: one environment per project** — named to match the project directory
3. **General projects: `lab-general` by default** — use the shared environment unless the project needs specialized dependencies, in which case create a project-specific one
4. **Always include `ipykernel`** — required for Quarto to execute Python chunks
5. **Prefer `conda install`** over `pip install` — conda resolves dependencies holistically. Use pip only as a fallback for packages not available via conda/conda-forge
6. **Install conda packages before pip packages** — if mixing both, conda packages first to avoid conflicts

## Shell Environment

- **Shell**: zsh (macOS default)
- **Conda base**: Typically `~/miniconda3` or `~/miniforge3` — customize to match your installation