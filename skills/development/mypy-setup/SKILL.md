---
name: mypy-setup
description: Set up Mypy type checking configuration for a Python project
argument-hint: [--strict] [--django] [--format=<ini|toml>] [--install]
---

# mypy-setup

**Category**: Python Development

## Usage

```bash
/mypy-setup [--strict] [--django] [--format=<ini|toml>] [--install]
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--strict` | No | Use strict type checking configuration |
| `--django` | No | Add Django-specific configuration and plugin |
| `--format=<ini\|toml>` | No | Config format (default: ini) |
| `--install` | No | Install Mypy and required plugins |

## Purpose

Set up Mypy static type checking in a Python project:

1. **Create Configuration**: Generate mypy.ini or pyproject.toml config
2. **Install Dependencies**: Install Mypy and type stub packages
3. **Configure IDE**: Add Mypy settings for VS Code/PyCharm
4. **Setup CI/CD**: Generate GitHub Actions workflow
5. **Add Pre-commit**: Configure pre-commit hook for Mypy

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

### 1. Parse Arguments

```
STRICT_MODE = true if --strict specified
DJANGO_MODE = true if --django specified
FORMAT = value after --format= (default: "ini")
INSTALL = true if --install specified
```

### 2. Detect Project Type

Scan the project to determine:

```bash
# Check for Django
HAS_DJANGO=false
if [ -f "manage.py" ] || grep -q "django" requirements.txt 2>/dev/null; then
    HAS_DJANGO=true
    echo "✓ Django project detected"
fi

# Check for existing config
HAS_CONFIG=false
if [ -f "mypy.ini" ] || [ -f ".mypy.ini" ] || grep -q "\[tool.mypy\]" pyproject.toml 2>/dev/null; then
    HAS_CONFIG=true
    echo "⚠ Existing Mypy configuration found"
fi

# Check Python version
PYTHON_VERSION=$(python --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python version: $PYTHON_VERSION"
```

### 3. Install Mypy (if --install)

```bash
if [ "$INSTALL" = true ]; then
    echo "Installing Mypy..."

    # Use uv if available, otherwise pip
    if command -v uv &> /dev/null; then
        PKG_MANAGER="uv pip install"
    else
        PKG_MANAGER="pip install"
    fi

    # Install Mypy
    $PKG_MANAGER mypy

    # Install Django plugin if needed
    if [ "$DJANGO_MODE" = true ] || [ "$HAS_DJANGO" = true ]; then
        $PKG_MANAGER django-stubs mypy-django-plugin
    fi

    # Install common type stubs
    $PKG_MANAGER types-requests types-PyYAML types-redis

    echo "✓ Mypy installed successfully"
fi
```

### 4. Generate Configuration File

#### Option A: mypy.ini (default)

```bash
if [ "$FORMAT" = "ini" ]; then
    cat > mypy.ini << 'EOF'
[mypy]
# Python version
python_version = 3.11

# Import discovery
namespace_packages = True
explicit_package_bases = True
ignore_missing_imports = False

# Platform configuration
platform = linux

# Disallow dynamic typing
disallow_any_generics = True
disallow_subclassing_any = True

# Disallow untyped code
disallow_untyped_calls = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True

# None and Optional handling
no_implicit_optional = True
strict_optional = True

# Warnings
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_return_any = True
warn_unreachable = True

# Strictness flags
strict_equality = True
strict_concatenate = True

# Error messages
show_error_codes = True
show_column_numbers = True
show_error_context = True
pretty = True

# Miscellaneous
warn_unused_configs = True

# Per-module options for gradual typing
[mypy-tests.*]
disallow_untyped_defs = False

[mypy-migrations.*]
ignore_errors = True

EOF

    if [ "$STRICT_MODE" = true ]; then
        # Already strict by default
        echo "✓ Created strict mypy.ini"
    else
        # Relax some settings for gradual adoption
        cat >> mypy.ini << 'EOF'

# Relaxed settings for gradual adoption
# Remove these overrides as you add type hints
[mypy]
disallow_untyped_calls = False
disallow_untyped_defs = False
disallow_incomplete_defs = False

EOF
        echo "✓ Created mypy.ini (gradual mode)"
        echo "  Gradually enable stricter checks as you add type hints"
    fi

    # Add Django configuration
    if [ "$DJANGO_MODE" = true ] || [ "$HAS_DJANGO" = true ]; then
        cat >> mypy.ini << 'EOF'

# Django configuration
[mypy]
plugins = mypy_django_plugin.main

[mypy.plugins.django-stubs]
django_settings_module = "config.settings"  # Update with your settings module

EOF
        echo "✓ Added Django plugin configuration"
        echo "  Update django_settings_module in mypy.ini"
    fi
fi
```

#### Option B: pyproject.toml

```bash
if [ "$FORMAT" = "toml" ]; then
    # Check if pyproject.toml exists
    if [ ! -f "pyproject.toml" ]; then
        cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

EOF
    fi

    # Add Mypy configuration
    cat >> pyproject.toml << 'EOF'

[tool.mypy]
python_version = "3.11"
namespace_packages = true
explicit_package_bases = true
ignore_missing_imports = false

# Strictness
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true

# None/Optional
no_implicit_optional = true
strict_optional = true

# Warnings
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_return_any = true
warn_unreachable = true

# Output
show_error_codes = true
show_column_numbers = true
show_error_context = true
pretty = true

# Per-module options
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true

EOF

    if [ "$DJANGO_MODE" = true ] || [ "$HAS_DJANGO" = true ]; then
        cat >> pyproject.toml << 'EOF'

[tool.mypy]
plugins = ["mypy_django_plugin.main"]

[tool.django-stubs]
django_settings_module = "config.settings"

EOF
    fi

    echo "✓ Created [tool.mypy] section in pyproject.toml"
fi
```

### 5. Create .mypy.ini in home directory (optional)

For user-specific defaults:

```bash
cat > ~/.mypy.ini << 'EOF'
[mypy]
# User-wide Mypy defaults
warn_unused_ignores = True
show_error_codes = True
pretty = True

EOF
```

### 6. Add to .gitignore

```bash
if [ -f ".gitignore" ]; then
    if ! grep -q ".mypy_cache" .gitignore; then
        echo "" >> .gitignore
        echo "# Mypy cache" >> .gitignore
        echo ".mypy_cache/" >> .gitignore
        echo "✓ Added .mypy_cache to .gitignore"
    fi
fi
```

### 7. Generate VS Code Settings

```bash
mkdir -p .vscode

if [ ! -f ".vscode/settings.json" ]; then
    cat > .vscode/settings.json << 'EOF'
{
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.linting.mypyArgs": [
    "--show-error-codes",
    "--show-column-numbers"
  ]
}
EOF
    echo "✓ Created .vscode/settings.json for Mypy"
else
    echo "⚠ .vscode/settings.json already exists"
    echo "  Add Mypy configuration manually if needed"
fi
```

### 8. Generate Pre-commit Hook

```bash
if [ -f ".pre-commit-config.yaml" ]; then
    # Check if Mypy already configured
    if ! grep -q "mirrors-mypy" .pre-commit-config.yaml; then
        cat >> .pre-commit-config.yaml << 'EOF'

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        args: [--show-error-codes]
        additional_dependencies:
          - types-requests
          - types-PyYAML
EOF
        if [ "$DJANGO_MODE" = true ] || [ "$HAS_DJANGO" = true ]; then
            cat >> .pre-commit-config.yaml << 'EOF'
          - django-stubs
          - mypy-django-plugin
EOF
        fi
        echo "✓ Added Mypy to .pre-commit-config.yaml"
    else
        echo "⚠ Mypy already in .pre-commit-config.yaml"
    fi
else
    # Create new pre-commit config
    cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        args: [--show-error-codes]
        additional_dependencies:
          - types-requests
          - types-PyYAML
EOF
    if [ "$DJANGO_MODE" = true ] || [ "$HAS_DJANGO" = true ]; then
        cat >> .pre-commit-config.yaml << 'EOF'
          - django-stubs
          - mypy-django-plugin
EOF
    fi
    echo "✓ Created .pre-commit-config.yaml with Mypy"
fi
```

### 9. Generate GitHub Actions Workflow

```bash
mkdir -p .github/workflows

cat > .github/workflows/type-check.yml << 'EOF'
name: Type Check

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  mypy:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mypy
EOF

if [ "$DJANGO_MODE" = true ] || [ "$HAS_DJANGO" = true ]; then
    cat >> .github/workflows/type-check.yml << 'EOF'
          pip install django-stubs mypy-django-plugin
EOF
fi

cat >> .github/workflows/type-check.yml << 'EOF'
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Type check with Mypy
        run: mypy .

      - name: Upload Mypy report
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: mypy-report
          path: .mypy_cache/
EOF

echo "✓ Created .github/workflows/type-check.yml"
```

### 10. Generate Summary Report

```
Mypy Setup Complete!
====================

Configuration:
  • Config file:     mypy.ini
  • Mode:            Strict
  • Django plugin:   Enabled
  • Python version:  3.11

Files Created:
  ✓ mypy.ini
  ✓ .vscode/settings.json
  ✓ .pre-commit-config.yaml
  ✓ .github/workflows/type-check.yml

Next Steps:
  1. Review and adjust mypy.ini settings
  2. Update Django settings module path (if applicable)
  3. Run: /mypy-check to test configuration
  4. Install pre-commit: pre-commit install
  5. Add type hints to your code gradually

Gradual Adoption Strategy:
  1. Start with new files (keep disallow_untyped_defs = True)
  2. Add type hints to critical paths (services, models)
  3. Enable stricter checks per module:
     [mypy-myapp.services.*]
     disallow_untyped_defs = True
  4. Expand coverage over time

Resources:
  • Mypy docs: https://mypy.readthedocs.io/
  • Cheat sheet: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
  • Django stubs: https://github.com/typeddjango/django-stubs

Run '/mypy-check' to verify your setup!
```

### 11. Interactive Setup (if no args)

If no arguments provided, ask user questions:

```
Mypy Setup Wizard
=================

1. Configuration format?
   [1] mypy.ini (recommended)
   [2] pyproject.toml

2. Strictness level?
   [1] Strict (recommended for new projects)
   [2] Gradual (for existing projects)

3. Project type?
   [1] Django
   [2] FastAPI
   [3] Generic Python

4. Install Mypy and plugins?
   [Y/n]

5. Setup IDE integration (VS Code)?
   [Y/n]

6. Add pre-commit hook?
   [Y/n]

7. Create GitHub Actions workflow?
   [Y/n]
```

---

## Examples

```bash
# Basic setup (interactive)
/mypy-setup

# Strict mode with mypy.ini
/mypy-setup --strict

# Django project with installation
/mypy-setup --django --install

# Use pyproject.toml format
/mypy-setup --format=toml

# Full setup for Django
/mypy-setup --strict --django --format=toml --install
```

## Configuration Templates

### Minimal (Gradual Adoption)

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
show_error_codes = True

# Start here, gradually enable more
```

### Balanced (Recommended)

```ini
[mypy]
python_version = 3.11
disallow_untyped_defs = True
warn_return_any = True
warn_unused_configs = True
no_implicit_optional = True
show_error_codes = True

[mypy-tests.*]
disallow_untyped_defs = False
```

### Strict (New Projects)

```ini
[mypy]
python_version = 3.11
strict = True
show_error_codes = True
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `python-experts:python-mypy` | Mypy type checking patterns |
| `python-experts:python-style` | Python coding standards |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/mypy-check` | Run type checking |
| `/python-experts:review-django-commands` | Review Django commands |

## Troubleshooting

### Django Settings Not Found

```bash
# Update in mypy.ini
[mypy.plugins.django-stubs]
django_settings_module = "your_project.settings"
```

### Import Errors

```bash
# Install missing type stubs
mypy --install-types
```

### Too Many Errors Initially

Start with:
```ini
[mypy]
ignore_missing_imports = True
check_untyped_defs = False
```

Then gradually remove these.
