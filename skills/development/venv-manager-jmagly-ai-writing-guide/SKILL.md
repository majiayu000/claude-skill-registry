---
name: venv-manager
description: Create, manage, and validate Python virtual environments. Use for project isolation and dependency management.
tools: Read, Write, Bash
---

# Virtual Environment Manager Skill

## Purpose

Single responsibility: Create and manage Python virtual environments for project isolation. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Python interpreter available and version known
- [ ] Target directory exists and is writable
- [ ] No conflicting venv already active
- [ ] requirements.txt or pyproject.toml exists (for install)

**DO NOT create venv without confirming Python version.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Multiple Python versions available - which to use?
- Existing venv found - replace or use?
- requirements.txt vs pyproject.toml both present
- Development vs production dependencies

**NEVER delete existing venv without confirmation.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Python version, project deps, venv path | Application code |
| PERIPHERAL | CI/CD requirements | Test configurations |
| DISTRACTOR | Deployment configs | Other language envs |

## Workflow Steps

### Step 1: Check Python Environment (Grounding)

```bash
# Available Python versions
which python3
python3 --version

# Check for existing venv
ls -la venv/ 2>/dev/null || ls -la .venv/ 2>/dev/null || echo "No venv found"

# Current active environment
echo "VIRTUAL_ENV: $VIRTUAL_ENV"
```

### Step 2: Create Virtual Environment

```bash
# Standard creation
python3 -m venv venv

# With specific Python version
python3.11 -m venv venv

# With system packages access
python3 -m venv venv --system-site-packages

# Verify creation
ls -la venv/bin/python
```

### Step 3: Activate and Install Dependencies

```bash
# Activate
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install from requirements.txt
pip install -r requirements.txt

# Or from pyproject.toml
pip install -e .

# Development dependencies
pip install -r requirements-dev.txt
```

### Step 4: Validate Environment

```bash
# List installed packages
pip list

# Check for missing deps
pip check

# Export current state
pip freeze > requirements-lock.txt
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Don't delete corrupted venv
2. **DIAGNOSE** - Check error type:
   - `venv creation failed` → Check Python installation
   - `pip install failed` → Check network, package availability
   - `activation failed` → Check shell compatibility
   - `dependency conflict` → Use pip-tools or poetry
3. **ADAPT** - Try alternative approach (rebuild, different Python)
4. **RETRY** - With fresh venv (max 3 attempts)
5. **ESCALATE** - Report with pip debug info

**Rollback command:**
```bash
rm -rf venv && python3 -m venv venv
```

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/venv-manager/`

```
checkpoints/venv-manager/
├── python_version.txt       # Python used
├── pip_freeze.txt           # Installed packages
├── creation_log.txt         # Creation output
└── validation_status.json   # Health check results
```

## Common Commands

| Command | Purpose |
|---------|---------|
| `python3 -m venv venv` | Create venv |
| `source venv/bin/activate` | Activate (bash/zsh) |
| `venv\Scripts\activate` | Activate (Windows) |
| `deactivate` | Deactivate |
| `pip freeze > requirements.txt` | Export deps |
| `pip install -r requirements.txt` | Install deps |

## Best Practices

1. **Naming**: Use `venv/` or `.venv/` consistently
2. **Git**: Add venv to `.gitignore`
3. **Lock files**: Use `pip freeze` or `pip-tools`
4. **Isolation**: Always create project-specific venvs
5. **Documentation**: Document Python version in README

## References

- Python venv docs: https://docs.python.org/3/library/venv.html
- REF-001: Production-Grade Agentic Workflows (BP-4)
- REF-002: LLM Failure Modes (Archetype 1 grounding)
