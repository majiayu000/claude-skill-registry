---
name: ruff
description: This skill should be used when users need to lint, format, or validate Python code using the Ruff command-line tool. Use this skill for tasks involving Python code quality checks, automatic code formatting, enforcing style rules (PEP 8), identifying bugs and security issues, or modernizing Python code. This skill should be invoked PROACTIVELY whenever Python code is written or modified to ensure code quality.
---

# Ruff Skill

This skill provides expertise in using Ruff, an extremely fast Python linter and code formatter written in Rust. Ruff combines the functionality of multiple tools (Flake8, isort, Black, and more) into a single, high-performance package.

## IMPORTANT: Proactive Usage

**You MUST use this skill proactively in the following scenarios:**

1. **After writing or modifying Python code** - Always run ruff format and ruff check --fix after creating or editing Python files
2. **Before committing code** - Ensure all Python code passes linting and formatting checks
3. **When encountering linting errors** - Immediately fix them using this skill's guidance
4. **During code reviews** - Check code quality before finalizing changes

**Default workflow when writing Python code:**

```bash
# Step 1: Format the code
uv run ruff format .

# Step 2: Fix auto-fixable linting issues
uv run ruff check --fix .

# Step 3: Report any remaining issues
uv run ruff check .
```

**Use the project's just commands when available:**

```bash
# Format Python code (uses uv run ruff format)
just fmt-python

# Lint Python code (uses uv run ruff check)
just lint-python
```

## About Ruff

Ruff is designed to replace multiple Python development tools with a single, fast, and comprehensive solution. It's 10-100x faster than traditional Python linters while providing comparable or better functionality.

### Key Capabilities

- **Linting**: Check Python code against 800+ lint rules from popular tools
- **Formatting**: Format Python code with Black-compatible output
- **Auto-fixing**: Automatically fix many linting issues
- **Import Sorting**: Organize imports (isort-compatible)
- **Configuration**: Highly customizable via `pyproject.toml` or `ruff.toml`
- **Fast**: Written in Rust for exceptional performance
- **All-in-one**: Replaces Flake8, Black, isort, pydocstyle, pyupgrade, and more

## When to Use This Skill

Use this skill when users:

- Need to lint or format Python code
- Want to enforce Python code quality standards (PEP 8, etc.)
- Need to identify bugs, security issues, or code smells
- Want to automatically fix common Python issues
- Need to format and organize imports
- Want to modernize Python code (e.g., upgrade syntax)
- Need to integrate linting/formatting into CI/CD pipelines
- Ask about Python code quality best practices
- Want to configure custom linting or formatting rules
- Need faster alternatives to Flake8, Black, or isort

## How to Use This Skill

### Basic Ruff Workflow

Ruff has two main commands:

1. **`ruff check`**: Lint Python code (finds issues)
2. **`ruff format`**: Format Python code (fixes style)

### Linting with `ruff check`

#### Basic Linting

Check a single file:

```bash
ruff check script.py
```

Check a directory:

```bash
ruff check src/
ruff check .
```

Check multiple paths:

```bash
ruff check src/ tests/ script.py
```

#### Auto-fixing Issues

Fix issues automatically where possible:

```bash
ruff check --fix script.py
ruff check --fix src/
```

The `--fix` option will modify files in place to resolve fixable issues.

#### Unsafe Fixes

Some fixes are considered "unsafe" because they may change code behavior. To apply these:

```bash
ruff check --fix --unsafe-fixes script.py
```

Always review unsafe fixes carefully before committing.

#### Show Fixes Without Applying

Preview what fixes would be applied:

```bash
ruff check --diff script.py
```

#### Statistics and Reporting

Show statistics about issues found:

```bash
ruff check --statistics src/
```

Output in different formats:

```bash
ruff check --output-format=json src/
ruff check --output-format=github src/  # For GitHub Actions
ruff check --output-format=gitlab src/  # For GitLab CI
ruff check --output-format=junit src/   # For CI/CD tools
```

#### Rule Selection

Select specific rules or categories:

```bash
# Check only unused imports
ruff check --select F401 src/

# Check multiple rule categories
ruff check --select E,F,W src/

# Ignore specific rules
ruff check --ignore E501 src/

# Extend existing configuration
ruff check --extend-select B src/
```

Common rule prefixes:

- **F**: Pyflakes (errors, undefined names, unused imports)
- **E/W**: pycodestyle errors and warnings (PEP 8)
- **C90**: mccabe (complexity)
- **I**: isort (import sorting)
- **N**: pep8-naming
- **UP**: pyupgrade (modernize syntax)
- **B**: flake8-bugbear (likely bugs)
- **S**: flake8-bandit (security)
- **A**: flake8-builtins
- **Q**: flake8-quotes
- **SIM**: flake8-simplify

#### Watch Mode

Continuously watch for changes and re-lint:

```bash
ruff check --watch src/
```

### Formatting with `ruff format`

#### Basic Formatting

Format a single file:

```bash
ruff format script.py
```

Format a directory:

```bash
ruff format src/
ruff format .
```

#### Check Format Without Modifying

Check if files need formatting:

```bash
ruff format --check src/
```

This is useful in CI/CD to verify code is formatted without modifying files.

#### Show Formatting Differences

Show what changes would be made:

```bash
ruff format --diff src/
```

#### Format stdin

Format code from standard input:

```bash
echo "x=1" | ruff format -
cat script.py | ruff format -
```

### Configuration

#### Configuration Files

Ruff looks for configuration in the following order:

1. `ruff.toml`
2. `.ruff.toml`
3. `pyproject.toml` (under `[tool.ruff]`)

#### Basic Configuration (pyproject.toml)

```toml
[tool.ruff]
# Set the maximum line length to 100
line-length = 100

# Assume Python 3.11
target-version = "py311"

# Enable additional rule sets
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
    "S",    # flake8-bandit
    "SIM",  # flake8-simplify
]

# Ignore specific rules
ignore = [
    "E501",  # Line too long (handled by formatter)
]

# Exclude directories
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
]

# Allow autofix for all enabled rules
fixable = ["ALL"]
unfixable = []

[tool.ruff.per-file-ignores]
# Ignore specific rules in specific files
"tests/**/*.py" = ["S101"]  # Allow assert in tests
"__init__.py" = ["F401"]    # Allow unused imports

[tool.ruff.format]
# Use single quotes for strings
quote-style = "single"

# Indent with spaces (not tabs)
indent-style = "space"

# End files with a newline
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.ruff.isort]
# Configure import sorting
known-first-party = ["myapp"]
```

#### Standalone ruff.toml

```toml
line-length = 100
target-version = "py311"

select = ["E", "F", "I", "B", "UP"]
ignore = ["E501"]

[format]
quote-style = "double"
indent-style = "space"
```

#### Command-Line Configuration

Override configuration from command line:

```bash
# Set line length
ruff check --line-length=120 src/

# Select specific rules
ruff check --select=E,F,I src/

# Set target Python version
ruff check --target-version=py39 src/
```

### Common Workflows

#### Full Code Quality Check

Run both linting and formatting checks:

```bash
# Check formatting
ruff format --check .

# Run linter
ruff check .
```

#### Auto-fix Everything

Fix and format all code:

```bash
# Fix linting issues
ruff check --fix .

# Format code
ruff format .
```

#### Pre-commit Integration

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.0
    hooks:
      # Run the linter
      - id: ruff
        args: [--fix]
      # Run the formatter
      - id: ruff-format
```

#### CI/CD Integration

GitHub Actions example:

```yaml
- name: Ruff Linter
  run: ruff check --output-format=github .

- name: Ruff Formatter
  run: ruff format --check .
```

#### Migration from Other Tools

Replace existing tools with Ruff:

**From Black + isort + Flake8:**

```bash
# Old workflow
black .
isort .
flake8 .

# New workflow
ruff format .
ruff check --select I --fix .  # isort
ruff check .                    # flake8
```

**Configuration Migration:**

```toml
# Convert Black settings
[tool.ruff]
line-length = 88  # Black default

[tool.ruff.format]
quote-style = "double"  # Black default

# Convert isort settings
[tool.ruff.isort]
known-first-party = ["myapp"]
force-single-line = false

# Convert Flake8 settings
[tool.ruff]
select = ["E", "F", "W", "C90"]  # Flake8 defaults
ignore = ["E203", "E501", "W503"]  # Common ignores
```

#### Gradual Adoption

Introduce Ruff gradually to existing projects:

```bash
# Start with just errors and critical issues
ruff check --select=E,F .

# Add more rules progressively
ruff check --select=E,F,B .
ruff check --select=E,F,B,UP .

# Finally add formatting
ruff format .
```

Use `--add-noqa` to add `# noqa` comments for existing violations:

```bash
ruff check --add-noqa src/
```

This allows you to enforce rules for new code while temporarily allowing existing violations.

#### Fix Specific Issue Types

Fix only certain categories of issues:

```bash
# Fix only import sorting
ruff check --select I --fix .

# Fix only unused imports and variables
ruff check --select F401,F841 --fix .

# Apply pyupgrade modernizations
ruff check --select UP --fix .
```

### Rule Categories

#### Essential Rules (Start Here)

```toml
[tool.ruff]
select = [
    "F",   # Pyflakes - errors and undefined names
    "E",   # pycodestyle errors - PEP 8 violations
    "I",   # isort - import sorting
]
```

#### Recommended Rules (Add Next)

```toml
[tool.ruff]
select = [
    "F", "E", "I",
    "W",   # pycodestyle warnings
    "UP",  # pyupgrade - modernize syntax
    "B",   # bugbear - likely bugs
    "SIM", # simplify - simplification suggestions
]
```

#### Advanced Rules (Optional)

```toml
[tool.ruff]
select = [
    "F", "E", "I", "W", "UP", "B", "SIM",
    "S",     # bandit - security issues
    "N",     # pep8-naming - naming conventions
    "C90",   # mccabe - complexity checking
    "A",     # flake8-builtins - shadowing builtins
    "Q",     # flake8-quotes - quote consistency
    "RET",   # flake8-return - return statement issues
    "ARG",   # flake8-unused-arguments
    "PTH",   # flake8-use-pathlib - use pathlib instead of os.path
    "PD",    # pandas-vet - pandas best practices
]
```

### Inline Configuration

#### Disable Rules for Lines

Use `# noqa` comments to disable rules:

```python
# Ignore all rules for this line
import os  # noqa

# Ignore specific rule
import os  # noqa: F401

# Ignore multiple rules
x = 1  # noqa: E701, E702

# Ignore for entire file (at top)
# ruff: noqa

# Disable specific rule for entire file
# ruff: noqa: F401
```

#### Per-file Ignores in Config

```toml
[tool.ruff.per-file-ignores]
"tests/*.py" = ["S101", "PLR2004"]
"__init__.py" = ["F401"]
"scripts/*.py" = ["T201"]  # Allow print statements
```

### Troubleshooting

#### Too Many Issues

If you're overwhelmed by issues on an existing project:

1. Start with critical issues only:

   ```bash
   ruff check --select=F,E .
   ```

2. Add noqa comments to existing violations:

   ```bash
   ruff check --add-noqa .
   ```

3. Fix auto-fixable issues first:

   ```bash
   ruff check --fix .
   ```

4. Enable rules gradually over time

#### Configuration Not Loading

If configuration isn't being applied:

- Check file name: `ruff.toml`, `.ruff.toml`, or `pyproject.toml`
- Validate TOML syntax: `ruff check --config=ruff.toml .`
- Use absolute paths in `exclude` patterns if relative paths don't work
- Check for conflicting configurations in parent directories

#### Formatter vs Black Differences

Ruff formatter aims for 99% compatibility with Black. Known differences:

- Magic trailing comma handling in some edge cases
- Line break decisions in complex nested structures

To report differences: use `--diff` and compare with Black output

#### False Positives

If Ruff reports false positives:

1. Use `# noqa` comments for specific exceptions
2. Configure per-file ignores for patterns
3. Report issues to the Ruff project

#### Performance Issues

Ruff is typically very fast, but if experiencing slowness:

- Exclude large directories (venv, node_modules, build)
- Use `.ruffignore` file for complex exclusion patterns
- Check for large files or deeply nested directories

### Best Practices

1. **Start Simple**: Begin with basic rules (F, E, I) and expand gradually
2. **Format First**: Run `ruff format` before `ruff check` to avoid style conflicts
3. **Use --fix Liberally**: Most auto-fixes are safe and save time
4. **Review Unsafe Fixes**: Always review `--unsafe-fixes` changes before committing
5. **Configure Line Length**: Set `line-length` to match your team's preference
6. **Enable in CI/CD**: Enforce checks in CI to maintain code quality
7. **Per-file Ignores**: Use per-file configuration for test files, scripts, etc.
8. **Commit Configuration**: Keep `ruff.toml` or `pyproject.toml` in version control
9. **Document Exceptions**: Comment why specific rules are disabled
10. **Keep Updated**: Ruff evolves quickly; update regularly for new rules and fixes

### Integration with IDEs

#### VS Code

Install the official Ruff extension:

```json
{
  "ruff.enable": true,
  "ruff.organizeImports": true,
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

#### PyCharm/IntelliJ

Configure Ruff as an external tool or use the Ruff plugin.

#### Vim/Neovim

Use ALE, null-ls, or native LSP integration with Ruff's language server.

## Installation

Ruff can be installed via multiple methods:

**Using pip:**

```bash
pip install ruff
```

**Using pipx (recommended for CLI tool):**

```bash
pipx install ruff
```

**Using uv:**

```bash
uv tool install ruff
```

**Using Homebrew:**

```bash
brew install ruff
```

**Using Conda:**

```bash
conda install -c conda-forge ruff
```

Verify installation:

```bash
ruff --version
ruff check --help
ruff format --help
```

## Resources

- Official documentation: <https://docs.astral.sh/ruff/>
- Linter rules: <https://docs.astral.sh/ruff/rules/>
- Formatter docs: <https://docs.astral.sh/ruff/formatter/>
- GitHub repository: <https://github.com/astral-sh/ruff>
- Configuration options: <https://docs.astral.sh/ruff/configuration/>
- Migration guides: <https://docs.astral.sh/ruff/faq/#how-does-ruff-compare-to-flake8>
