---
name: pre-commit
description: When setting up automated code quality checks on git commit. When project has .pre-commit-config.yaml. When implementing git hooks for formatting, linting, or validation. When creating prepare-commit-msg hooks to modify commit messages. When distributing a tool as a pre-commit hook.
---

# Pre-commit Framework

Configure and implement git hooks using pre-commit or prek for automated code quality checks, formatting, linting, and commit message processing across multi-language projects.

## Alternative: prek

**prek** is a Rust-based reimplementation of pre-commit that offers:

- Faster execution (Rust vs Python)
- No Python dependency required
- **Drop-in replacement**: Uses same `.pre-commit-config.yaml` file
- **Identical CLI interface**: All commands work the same way

**Installation**:

```bash
# Using uv (recommended)
uv tool install prek

# Using pip
pip install prek

# Using cargo
cargo install prek
```

**Detection**: To determine which tool is installed in a repository, read `.git/hooks/pre-commit` (second line):

- Contains "pre-commit.com" → pre-commit is installed
- Contains "github.com/j178/prek" → prek is installed

**Throughout this skill**: Commands shown with `pre-commit` work identically with `prek`. Simply replace `pre-commit` with `prek` in any command.

## When to Use This Skill

Use this skill when:

- Setting up git hooks for code quality automation
- Implementing commit message validation or rewriting workflows
- Configuring pre-commit hooks for formatting tools (black, prettier, etc.)
- Creating custom hooks for project-specific quality checks
- Installing hooks for prepare-commit-msg stage (message modification)
- Troubleshooting hook installation or execution issues
- Designing hook definitions for distribution in tool repositories
- Managing hook stages and execution order

## Core Concepts

### Hook Stages

Pre-commit supports multiple git hook stages matching git hook names directly:

| Stage                | Purpose                     | Common Use Cases                  |
| -------------------- | --------------------------- | --------------------------------- |
| `pre-commit`         | Before commit creation      | Code formatting, linting, tests   |
| `prepare-commit-msg` | Before message editor opens | **Commit message rewriting**      |
| `commit-msg`         | After message written       | Message validation only           |
| `pre-push`           | Before push to remote       | Integration tests, security scans |
| `pre-merge-commit`   | Before merge commit         | Merge validation                  |
| `post-checkout`      | After checkout              | Environment setup                 |
| `post-commit`        | After commit created        | Notifications, logging            |
| `post-merge`         | After merge completes       | Dependency updates                |
| `manual`             | Explicit invocation only    | On-demand tasks                   |

### Critical Distinction: prepare-commit-msg vs commit-msg

| Feature                   | prepare-commit-msg                                              | commit-msg            |
| ------------------------- | --------------------------------------------------------------- | --------------------- |
| **Can modify message**    | **Yes**                                                         | No (validation only)  |
| **When it runs**          | Before editor opens                                             | After message written |
| **Environment variables** | `PRE_COMMIT_COMMIT_MSG_SOURCE`, `PRE_COMMIT_COMMIT_OBJECT_NAME` | None                  |
| **Use for**               | Rewriting, formatting                                           | Validation, rejection |

**For commit message rewriting:** Use `prepare-commit-msg` stage.

**For commit message validation:** Use `commit-msg` stage with tools like commitlint.

Activate the `commitlint` skill for commit message validation patterns:

```
Skill(command: "commitlint")
```

Activate the `conventional-commits` skill for commit message format standards:

```
Skill(command: "conventional-commits")
```

## Installation

### Install pre-commit or prek Tool

**pre-commit (Python-based)**:

```bash
# Using uv (recommended)
uv tool install pre-commit

# Using pip
pip install pre-commit

# Verify installation
pre-commit --version
```

**prek (Rust-based alternative)**:

```bash
# Using uv (recommended)
uv tool install prek

# Using pip
pip install prek

# Using cargo
cargo install prek

# Verify installation
prek --version
```

### Install Hooks in Repository

```bash
# Using pre-commit:
# Install default hook type (pre-commit stage only)
pre-commit install

# Install specific hook type (required for prepare-commit-msg)
pre-commit install --hook-type prepare-commit-msg

# Install multiple hook types
pre-commit install --hook-type pre-commit --hook-type prepare-commit-msg

# Install and setup environments immediately
pre-commit install --install-hooks

# Overwrite existing hooks
pre-commit install --overwrite

# Using prek (same commands, just replace 'pre-commit' with 'prek'):
prek install
prek install --hook-type prepare-commit-msg
# ... etc
```

### Configure Default Hook Types

To install `prepare-commit-msg` automatically with `pre-commit install` or `prek install`:

```yaml
# .pre-commit-config.yaml
default_install_hook_types: [pre-commit, prepare-commit-msg]
```

## Configuration Files

### .pre-commit-config.yaml (User Repository)

Place in repository root to configure which hooks to use.

#### Essential Properties

| Property                     | Type | Default        | Purpose                         |
| ---------------------------- | ---- | -------------- | ------------------------------- |
| `repos`                      | list | Required       | Repository mappings             |
| `default_install_hook_types` | list | `[pre-commit]` | Hook types installed by default |
| `default_stages`             | list | all stages     | Default stages for hooks        |
| `fail_fast`                  | bool | `false`        | Stop on first hook failure      |

#### Repository Mapping

```yaml
repos:
  - repo: https://github.com/org/tool
    rev: v1.0.0  # Use immutable ref (tag or SHA)
    hooks:
      - id: hook-name
        stages: [prepare-commit-msg]
        args: [--option, value]
```

#### Hook Configuration Properties

| Property         | Type   | Purpose                            |
| ---------------- | ------ | ---------------------------------- |
| `id`             | string | Hook ID from repository (required) |
| `stages`         | list   | Override hook stages               |
| `args`           | list   | Additional arguments               |
| `files`          | regex  | File pattern to match              |
| `exclude`        | regex  | File pattern to exclude            |
| `types`          | list   | File types (AND logic)             |
| `always_run`     | bool   | Run even without matching files    |
| `pass_filenames` | bool   | Pass staged files to hook          |
| `verbose`        | bool   | Force output on success            |

#### Example Configuration

```yaml
# .pre-commit-config.yaml
default_install_hook_types: [pre-commit, prepare-commit-msg]

repos:
  # Standard code quality hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml

  # Python formatting
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  # Commit message processing
  - repo: https://github.com/your-org/commit-polish
    rev: v1.0.0
    hooks:
      - id: commit-polish
        stages: [prepare-commit-msg]
```

### .pre-commit-hooks.yaml (Hook Definition)

Place in hook repository to define available hooks for distribution.

#### Hook Definition Schema

| Property                     | Type   | Required            | Purpose                            |
| ---------------------------- | ------ | ------------------- | ---------------------------------- |
| `id`                         | string | **Yes**             | Unique hook identifier             |
| `name`                       | string | **Yes**             | Display name during execution      |
| `entry`                      | string | **Yes**             | Command to execute                 |
| `language`                   | string | **Yes**             | Hook language (python, node, etc.) |
| `stages`                     | list   | No                  | Git hooks to run for               |
| `pass_filenames`             | bool   | No (default: true)  | Pass staged files to hook          |
| `always_run`                 | bool   | No (default: false) | Run without matching files         |
| `files`                      | regex  | No                  | Pattern of files to run on         |
| `exclude`                    | regex  | No                  | Pattern to exclude                 |
| `types`                      | list   | No                  | File types (AND logic)             |
| `description`                | string | No                  | Hook description                   |
| `minimum_pre_commit_version` | string | No                  | Minimum pre-commit version         |

#### Example Hook Definition

```yaml
# .pre-commit-hooks.yaml
- id: commit-polish
  name: Polish Commit Message
  description: Rewrites commit messages to conventional format using LLM
  entry: commit-polish
  language: python
  stages: [prepare-commit-msg]
  pass_filenames: false  # Hook receives message file path
  always_run: true       # Run even without file changes
  minimum_pre_commit_version: '3.2.0'
```

## Implementing prepare-commit-msg Hooks

### Hook Arguments

The `prepare-commit-msg` hook receives:

1. **Positional argument** (`sys.argv[1]`): Path to commit message file (`.git/COMMIT_EDITMSG`)

2. **Environment variables**:
   - `PRE_COMMIT_COMMIT_MSG_SOURCE`: Message source (`message`, `template`, `merge`, `squash`, `commit`)
   - `PRE_COMMIT_COMMIT_OBJECT_NAME`: Commit SHA (for amend operations)

### Implementation Template

```python
#!/usr/bin/env python3
"""Hook entry point for prepare-commit-msg stage."""
import os
import sys


def main() -> int:
    """Entry point for pre-commit hook.

    Returns:
        0 on success, non-zero aborts the commit.
    """
    if len(sys.argv) < 2:
        print("Error: No commit message file provided", file=sys.stderr)
        return 1

    # Get commit message file path from pre-commit
    commit_msg_file = sys.argv[1]

    # Get optional environment info
    source = os.environ.get('PRE_COMMIT_COMMIT_MSG_SOURCE', '')
    commit_sha = os.environ.get('PRE_COMMIT_COMMIT_OBJECT_NAME', '')

    # Read current message
    with open(commit_msg_file, encoding='utf-8') as f:
        original_message = f.read()

    # Skip if message is empty
    if not original_message.strip():
        return 0

    # Process message
    new_message = process_commit_message(original_message)

    # Write back modified message
    with open(commit_msg_file, 'w', encoding='utf-8') as f:
        f.write(new_message)

    return 0  # Success - commit proceeds


def process_commit_message(message: str) -> str:
    """Transform the commit message.

    Args:
        message: Original commit message

    Returns:
        Transformed commit message
    """
    # Implement message transformation logic
    return message


if __name__ == "__main__":
    sys.exit(main())
```

### Entry Point Configuration

Configure entry point in `pyproject.toml`:

```toml
[project.scripts]
commit-polish = "commit_polish.hook:main"
```

### Hook Definition Configuration

```yaml
# .pre-commit-hooks.yaml
- id: commit-polish
  name: Polish Commit Message
  entry: commit-polish
  language: python
  stages: [prepare-commit-msg]
  pass_filenames: false  # Critical: hook receives message file path
  always_run: true       # Critical: run even without staged files
```

## Running Hooks

### Automatic Execution

Hooks run automatically during git operations (works with both pre-commit and prek):

```bash
git commit -m "message"  # Runs pre-commit and prepare-commit-msg hooks
git push                 # Runs pre-push hooks
```

### Manual Execution

```bash
# Using pre-commit:
# Run all hooks for default stage
pre-commit run

# Run specific hook
pre-commit run commit-polish

# Run specific hook stage
pre-commit run --hook-stage prepare-commit-msg

# Run on specific files (scoped operation - preferred)
pre-commit run --files path/to/file.py path/to/other.py

# Run with verbose output
pre-commit run commit-polish --verbose

# Using prek (identical commands):
prek run
prek run commit-polish
prek run --hook-stage prepare-commit-msg
prek run --files path/to/file.py
prek run commit-polish --verbose
```

**Important - Avoid `--all-files` Pattern**: Running hooks with `--all-files` formats code throughout the entire repository, not just your current changes. This causes:

- **Diff pollution**: Merge requests show formatting changes to files you didn't modify
- **Merge conflicts**: Formatting changes on files being worked on by other developers
- **Broken git blame**: Mass formatting obscures the actual author of meaningful changes

**Preferred Patterns**:

- `pre-commit run` (no args): Runs on staged files only
- `pre-commit run --files <paths>`: Runs on specific files you're working on
- Git hook auto-execution: Runs automatically on commit for staged files

**Exception**: Use `--all-files` ONLY when the user explicitly requests repository-wide cleanup (e.g., "format the entire codebase").

### Testing Hooks

```bash
# Test hook from local repository
pre-commit try-repo /path/to/hook-repo hook-id --verbose

# Test prepare-commit-msg hooks (provide message file)
pre-commit try-repo /path/to/repo commit-polish \
    --commit-msg-filename .git/COMMIT_EDITMSG

# Test hook manually without pre-commit framework
echo "test message" > /tmp/test-msg
python -m commit_polish.hook /tmp/test-msg
cat /tmp/test-msg
```

## Environment Variables

### Skip Hooks

```bash
# Skip specific hook
SKIP=commit-polish git commit -m "message"

# Skip multiple hooks
SKIP=commit-polish,trailing-whitespace git commit -m "message"

# Skip all pre-commit hooks
git commit --no-verify -m "message"
```

### Cache Location

```bash
# Default cache location
~/.cache/pre-commit

# Override cache location
export PRE_COMMIT_HOME=/custom/path

# Use XDG spec
export XDG_CACHE_HOME=/custom/cache
# Results in: /custom/cache/pre-commit
```

## Common Patterns

### Hook Configuration for Commit Message Tools

```yaml
# Commit message rewriting (prepare-commit-msg)
- repo: https://github.com/your-org/commit-polish
  rev: v1.0.0
  hooks:
    - id: commit-polish
      stages: [prepare-commit-msg]
      pass_filenames: false
      always_run: true

# Commit message validation (commit-msg)
- repo: https://github.com/alessandrojcm/commitlint-pre-commit-hook
  rev: v9.5.0
  hooks:
    - id: commitlint
      stages: [commit-msg]
      additional_dependencies: ['@commitlint/config-conventional']
```

### Language-Specific Formatters

```yaml
# Python
- repo: https://github.com/psf/black
  rev: 23.12.1
  hooks:
    - id: black
      language_version: python3.11

# JavaScript/TypeScript
- repo: https://github.com/pre-commit/mirrors-prettier
  rev: v3.1.0
  hooks:
    - id: prettier
      types_or: [javascript, jsx, ts, tsx, json, yaml, markdown]

# Rust
- repo: https://github.com/doublify/pre-commit-rust
  rev: v1.0
  hooks:
    - id: fmt
    - id: clippy
```

### Multi-Stage Hooks

```yaml
# Run formatting on pre-commit, validation on pre-push
- repo: local
  hooks:
    - id: python-tests
      name: Run Python Tests
      entry: uv run pytest
      language: system
      stages: [pre-commit]
      types: [python]
      pass_filenames: false

    - id: integration-tests
      name: Run Integration Tests
      entry: uv run pytest tests/integration
      language: system
      stages: [pre-push]
      pass_filenames: false
      always_run: true
```

## Common Issues

### Issue: Hook Not Running

**Symptoms:** Hook configured but doesn't execute during commits.

**Solutions:**

1. Verify hook type is installed:

   ```bash
   ls -la .git/hooks/prepare-commit-msg
   ```

2. Install specific hook type:

   ```bash
   pre-commit install --hook-type prepare-commit-msg
   ```

3. Check `default_install_hook_types` in `.pre-commit-config.yaml`

### Issue: pass_filenames: true with Message Hooks

**Symptoms:** Hook receives staged filenames instead of message file path.

**Solution:** Set `pass_filenames: false` for `prepare-commit-msg` and `commit-msg` stages:

```yaml
hooks:
  - id: commit-polish
    stages: [prepare-commit-msg]
    pass_filenames: false  # Critical
```

### Issue: Hook Skipped Without Files

**Symptoms:** Hook doesn't run when no files match patterns.

**Solution:** Set `always_run: true`:

```yaml
hooks:
  - id: commit-polish
    always_run: true  # Run even without matching files
```

### Issue: Mutable Reference Not Updating

**Symptoms:** Hook repository updates not reflected after `pre-commit autoupdate`.

**Solution:** Use immutable refs (tags or SHAs):

```yaml
# Wrong: branch names don't auto-update
rev: main

# Correct: tags and SHAs are immutable
rev: v1.0.0
rev: a1b2c3d4
```

### Issue: Hook Execution Order

**Symptoms:** Hooks run in unexpected order.

**Context:** Hooks run in the order listed in `.pre-commit-config.yaml` within each repository. Hooks from different repositories may run in parallel.

**Solution:** Group dependent hooks in the same repository, or use `require_serial: true`:

```yaml
hooks:
  - id: format-code
  - id: lint-code  # Runs after format-code
    require_serial: true
```

## Complete Example: Commit Message Workflow

### Repository Structure

```
commit-polish/
├── .pre-commit-hooks.yaml
├── pyproject.toml
└── src/
    └── commit_polish/
        ├── __init__.py
        └── hook.py
```

### Hook Definition

```yaml
# .pre-commit-hooks.yaml
- id: commit-polish
  name: Polish Commit Message
  description: Rewrites commit messages to conventional commits format
  entry: commit-polish
  language: python
  stages: [prepare-commit-msg]
  pass_filenames: false
  always_run: true
  minimum_pre_commit_version: '3.2.0'
```

### User Configuration

```yaml
# User's .pre-commit-config.yaml
default_install_hook_types: [pre-commit, prepare-commit-msg]

repos:
  - repo: https://github.com/your-org/commit-polish
    rev: v1.0.0
    hooks:
      - id: commit-polish
        stages: [prepare-commit-msg]
```

### Installation and Usage

```bash
# In user's repository
cd /path/to/user-repo

# Install hooks (both pre-commit and prepare-commit-msg)
pre-commit install

# Make a commit - hook rewrites message automatically
git add .
git commit -m "fix bug"
# Hook transforms message before editor opens
```

## Version Requirements

| Component  | Minimum Version | Notes                                 |
| ---------- | --------------- | ------------------------------------- |
| pre-commit | 3.2.0           | Stage values match hook names         |
| Python     | 3.8+            | For pre-commit framework              |
| Git        | 2.24+           | Required for `pre-merge-commit` stage |

## Related Skills

Activate related skills for comprehensive commit workflow:

- **conventional-commits**: Commit message format standards

  ```
  Skill(command: "conventional-commits")
  ```

- **commitlint**: Commit message validation rules
  ```
  Skill(command: "commitlint")
  ```

## References

See [./references/pre-commit-official-docs.md](./references/pre-commit-official-docs.md) for complete official documentation links and detailed specifications.

### Key Documentation

- [Pre-commit Official Site](https://pre-commit.com/)
- [Creating New Hooks](https://pre-commit.com/#creating-new-hooks)
- [Supported Git Hooks](https://pre-commit.com/#supported-git-hooks)
- [Git prepare-commit-msg Documentation](https://git-scm.com/docs/githooks#_prepare_commit_msg)
- [Pre-commit GitHub Repository](https://github.com/pre-commit/pre-commit)
