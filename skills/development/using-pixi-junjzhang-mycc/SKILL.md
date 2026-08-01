---
name: using-pixi
description: Guidance for developing under a projects managed by pixi. Always use
  when workspace managed by pixi (have pixi.toml or pixi.lock in root directory.)
  Covers all you should know while developing under a
---

---
name: using-pixi
description: Guidance for developing under a projects managed by pixi. Always use when workspace managed by pixi (have pixi.toml or pixi.lock in root directory.) Covers all you should know while developing under a pixi-based project: pixi environment commands (install, run, shell, add, task), multi-environment management (-e flag, features), task configuration in pixi.toml, dependencies (conda vs PyPI), lock files, and development workflows. Helps with environment setup, package management, running tasks, debugging pixi.toml errors, and production deployment patterns.
---

# Pixi Helper

Expert guidance for using Pixi, a fast conda-based package manager for Python projects.

## Purpose

Help developers effectively use Pixi for managing conda/PyPI dependencies, running commands in isolated environments, and configuring multi-environment projects.

## When to Use

- Working with `pixi.toml` or `pixi.lock` files
- Installing or managing packages
- Running commands or tasks in pixi environments
- Setting up development/production environments
- Debugging pixi configuration errors

---

## Quick Command Reference

### Essential Commands

```bash
# Initialize & install
pixi init [project-name]
pixi install                         # install default environment
pixi install -e dev                  # install dev environment

# Add dependencies
pixi add python=3.11 pytorch pandas  # conda packages
pixi add --pypi transformers         # PyPI packages
pixi add --feature dev pytest ruff   # to dev feature

# Run commands
pixi run python script.py            # use default env
pixi run -e dev pytest               # use dev env
pixi shell                           # interactive shell
pixi shell -e dev                    # dev shell

# Tasks
pixi task add lint "ruff check ."
pixi task list
pixi run lint

# Production
pixi run --frozen --no-install train.py
```

### Key Flags

- `-e <env>`: Use specific environment
- `--frozen`: Don't update lock file (reproducible)
- `--no-install`: Skip installation
- `--feature <name>`: Target specific feature

---

## Core Concepts

### Workspace
Directory with:
- `pixi.toml`: Configuration (commit this)
- `pixi.lock`: Lock file (commit this)
- `.pixi/`: Environment cache (DON'T commit)

### Environments
Named dependency sets. Use `-e` flag to select:

```bash
pixi run python script.py       # default
pixi run -e dev pytest           # dev
pixi run -e prod train.py        # prod
```

### Features
Reusable dependency groups that compose into environments.

### Tasks
Predefined commands in pixi.toml. Run with `pixi run <task-name>`.

---

## Command Patterns

### When to Use What

| Goal | Command |
|------|---------|
| First-time setup | `pixi install` |
| Add package | `pixi add <pkg>` |
| Run one command | `pixi run <cmd>` |
| Interactive work | `pixi shell` |
| Execute task | `pixi run <task>` |
| Production | `pixi run --frozen --no-install` |

### Adding Dependencies

**Prefer conda first** (better compatibility, faster):
```bash
pixi add numpy pytorch
```

**Use PyPI when needed**:
```bash
pixi add --pypi transformers
```

**Why conda first?** Pixi resolves conda deps first, then PyPI.

---

## pixi.toml Configuration

### Project Metadata

```toml
[project]
name = "my-project"
channels = ["conda-forge", "pytorch"]  # order matters
platforms = ["linux-64", "osx-arm64"]
```

### Dependencies

```toml
[dependencies]
python = ">=3.10"
numpy = "*"
pytorch = ">=2.0,<3"

[pypi-dependencies]
transformers = "*"
my-pkg = { path = "./local", editable = true }
```

### Tasks

**Simple**:
```toml
[tasks]
test = "pytest tests/"
```

**With environment variables**:
```toml
[tasks.train]
cmd = "python train.py"
env = { CUDA_VISIBLE_DEVICES = "0,1" }
```

**With dependencies**:
```toml
[tasks]
clean = "rm -rf __pycache__"
test = { cmd = "pytest", depends-on = ["clean"] }
```

**Multi-line**:
```toml
[tasks.submit]
cmd = """
python train.py \
  --config config.yaml \
  --output results/
"""
```

### Features

```toml
[feature.dev.dependencies]
pytest = "*"
ruff = "*"

[feature.cuda.dependencies]
pytorch-cuda = "12.1"

[environments]
default = []
dev = ["dev"]
gpu = ["cuda"]
dev-gpu = ["dev", "cuda"]
```

### Activation Environment

```toml
[activation.env]
CUDA_HOME = "/usr/local/cuda"
PROJECT_ROOT = "$PIXI_PROJECT_ROOT"
```

---

## Common Workflows

### Your Patterns (susser-tod)

**Dev testing**:
```bash
pixi run -e dev pytest ./tests
```

**Type checking**:
```bash
pixi run typecheck
```

**Profiling**:
```bash
pixi run -e dev nsys profile python train.py
```

---

## Troubleshooting

### 1. Package Not Found

**Checks**:
1. Channel specified in `channels = [...]`?
2. Package name correct? Try: `pixi search <pkg>`
3. Try PyPI: `pixi add --pypi <pkg>`

### 2. Environment Not Activated

❌ **Wrong**: `python script.py` (bare python)
✅ **Correct**: `pixi run python script.py`

### 4. Lock File Conflicts

After merge conflicts:
```bash
pixi install              # regenerate lock
# or
rm pixi.lock && pixi install
```

### 5. Environment Variables Not Set

Variables from `[activation.env]` only work with:
- `pixi run <cmd>`
- Inside `pixi shell`

NOT with bare `python` outside pixi.

### 6. Dependency Version Conflicts

Use `solve-group` to isolate environments:

```toml
[environments]
default = { solve-group = "group1" }
dev = { features = ["dev"], solve-group = "group1" }  # shared
prod = { solve-group = "group2" }                     # isolated
```

---

## Best Practices

### Dependencies
✅ Conda first, PyPI when needed
✅ Pin critical versions: `pytorch = "2.1.*"`
✅ Version constraints: `python = ">=3.10,<3.12"`
❌ Don't mix conda + PyPI for same package

### Lock Files
✅ Commit `pixi.lock`
✅ Use `--frozen` in CI/production

### Environments
✅ Use features to organize deps
✅ Share solve-groups when possible
✅ 2-4 environments is ideal

---

## Reference

- **Detailed pixi.toml schema**: See [REFERENCE.md](./REFERENCE.md)
- **Official docs**: https://pixi.sh/latest/
- **pixi.toml spec**: https://pixi.sh/latest/reference/pixi_toml/

---

*Practical guidance for Pixi. For project-specific patterns, check your CLAUDE.md.*
