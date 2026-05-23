---
name: "Setting Up Projects"
description: "Automates project setup with best practices including pre-commit hooks, linting, formatting, and boilerplate. Activates when creating new projects, missing configuration files, or setting up development environment. Ensures quality tooling from the start."
---

# Setting Up Projects

You are activating project setup automation. Your role is to establish best practices, quality tooling, and proper configuration for new or existing projects.

## When to Activate

This skill activates when:

- User is creating a new project
- Project lacks pre-commit hooks configuration
- Missing essential config files (.gitignore, .editorconfig, etc.)
- Setting up development environment
- User asks about project setup or best practices
- Establishing quality baselines

## Philosophy

### Quality from the Start

- **Automate Quality**: Pre-commit hooks catch issues before commit
- **Consistency**: Formatting and linting enforce standards
- **Security**: Detect secrets and vulnerabilities early
- **Productivity**: Proper setup accelerates development

### Progressive Enhancement

Start with essentials, add more as needed:

1. Core configs (Git, editor, dependencies)
2. Quality tooling (linting, formatting)
3. Pre-commit hooks (automation)
4. CI/CD pipelines (continuous validation)

## Setup Process

### 1. Assess Current State

Check what exists:

```bash
ls -la  # Check for config files
git status  # Check Git state
```

Identify gaps:

- [ ] `.gitignore` present?
- [ ] `.editorconfig` for consistency?
- [ ] Package manager config (package.json, requirements.txt, etc.)?
- [ ] Linter config?
- [ ] Formatter config?
- [ ] Pre-commit hooks?
- [ ] CI/CD config?

### 2. Create Core Configs

#### .gitignore

Generate appropriate ignore patterns:

- Language-specific (node_modules, **pycache**, etc.)
- IDE files (.vscode, .idea, etc.)
- OS files (.DS_Store, Thumbs.db, etc.)
- Environment files (.env, .env.local)
- Build artifacts (dist/, build/, \*.pyc)

#### .editorconfig

Ensure consistent formatting across editors:

```ini
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false
```

### 3. Set Up Quality Tooling

#### Python Projects

**Linting & Formatting**:

- **Ruff**: Fast all-in-one tool (replaces black, flake8, isort)
- **Pyright** or **Mypy**: Type checking

**Configuration** (pyproject.toml):

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.pyright]
typeCheckingMode = "basic"
```

#### JavaScript/TypeScript Projects

**Linting & Formatting**:

- **Prettier**: Code formatting
- **ESLint**: Linting

**Configuration**:

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}

// .eslintrc.json
{
  "extends": ["eslint:recommended"],
  "env": {
    "node": true,
    "es2021": true
  }
}
```

### 4. Install Pre-commit Hooks

Pre-commit runs checks automatically before each commit.

#### Installation

```bash
pip install pre-commit
pre-commit install
```

#### Configuration (.pre-commit-config.yaml)

**Python Project**:

```yaml
repos:
  # Universal checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ["--maxkb=500"]

  # Python: Ruff (linting + formatting)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.5
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Python: Type checking
  - repo: https://github.com/RobertCraigie/pyright-python
    rev: v1.1.338
    hooks:
      - id: pyright

  # Security: Detect secrets
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
```

**JavaScript/TypeScript Project**:

```yaml
repos:
  # Universal checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files

  # JavaScript: Prettier
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, yaml, markdown]

  # JavaScript: ESLint
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.54.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]

  # Security
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

### 5. Initialize Baseline

For existing projects, create baseline to avoid flagging existing issues:

```bash
# Create secrets baseline (won't flag existing patterns)
detect-secrets scan > .secrets.baseline

# Run pre-commit on all files
pre-commit run --all-files
```

### 6. Document Setup

Create or update README.md with:

- Setup instructions
- Development workflow
- Quality tooling in use
- How to run tests
- How to contribute

## Language-Specific Setups

### Python

**Essential Files**:

- `requirements.txt` or `pyproject.toml`
- `.python-version` (for version pinning)
- `pytest.ini` or `pyproject.toml` (test config)

**Virtual Environment**:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### JavaScript/TypeScript

**Essential Files**:

- `package.json`
- `tsconfig.json` (TypeScript)
- `.nvmrc` (Node version)

**Install Dependencies**:

```bash
npm install
# or
yarn install
```

### Rust

**Essential Files**:

- `Cargo.toml`
- `rustfmt.toml`
- `clippy.toml`

**Setup**:

```bash
cargo build
cargo fmt
cargo clippy
```

### Go

**Essential Files**:

- `go.mod`
- `.golangci.yml`

**Setup**:

```bash
go mod download
go fmt ./...
go vet ./...
```

## Configuration Templates

### Full Python Project Setup

Create comprehensive setup:

```
project/
├── .gitignore
├── .editorconfig
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── src/
│   └── project/
│       └── __init__.py
└── tests/
    └── __init__.py
```

### Full JavaScript Project Setup

```
project/
├── .gitignore
├── .editorconfig
├── .pre-commit-config.yaml
├── .prettierrc
├── .eslintrc.json
├── package.json
├── tsconfig.json
├── README.md
├── src/
│   └── index.ts
└── tests/
    └── index.test.ts
```

## Integration Points

### Invokes

- **Builder Agent**: For code generation
- **Templates**: Language-specific boilerplate
- **Pre-commit Setup**: See `Specs/PreCommitHooks.md`

### References

- **Project Structure**: `Specs/ProjectStructure.md`
- **Best Practices**: Language-specific guides
- **Templates**: `.claude/templates/`

## Recommendations

### Always Recommend

These are essential for all projects:

1. `.gitignore` - Prevent committing unwanted files
2. `.editorconfig` - Consistent formatting
3. Pre-commit hooks - Automated quality
4. README.md - Documentation

### Recommend for Teams

When multiple developers:

1. Code formatting (Prettier, Black, etc.)
2. Linting (ESLint, Ruff, etc.)
3. Type checking (TypeScript, Mypy, etc.)
4. CI/CD pipeline

### Recommend for Production

When shipping to users:

1. Security scanning (detect-secrets, etc.)
2. Dependency checking (Dependabot, etc.)
3. Test coverage tracking
4. Performance monitoring

## Example Workflow

```
User: "I'm starting a new Python project for a REST API."

Setting Up Projects Skill:

Great! Let me set up a solid foundation for your Python REST API project.

## Setup Plan

I'll create:
1. Project structure with best practices
2. Pre-commit hooks for automated quality
3. Python configs (ruff, pyright)
4. Git ignore patterns
5. README template

## Project Structure

Creating:
```

api-project/
├── .gitignore # Ignore patterns
├── .editorconfig # Editor consistency
├── .pre-commit-config.yaml # Pre-commit hooks
├── pyproject.toml # Python config + dependencies
├── README.md # Documentation
├── requirements.txt # Production dependencies
├── requirements-dev.txt # Development dependencies
├── src/
│ └── api/
│ ├── **init**.py
│ ├── main.py # FastAPI app entry
│ └── routers/ # API routes
├── tests/
│ ├── **init**.py
│ └── test_main.py
└── .env.example # Environment template

````

## Quality Tooling

Installing:
- **Ruff**: Fast linting + formatting
- **Pyright**: Type checking
- **Detect-secrets**: Prevent credential leaks
- **Pre-commit**: Automated checks

## Pre-commit Hooks

Configured to run on every commit:
- Trailing whitespace removal
- File ending fixes
- YAML/JSON validation
- Large file detection
- Ruff linting + formatting
- Type checking with pyright
- Secret detection

## Setup Instructions

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial check
pre-commit run --all-files
````

## Next Steps

1. [ ] Review generated configuration
2. [ ] Customize as needed
3. [ ] Start implementing API endpoints
4. [ ] Set up CI/CD (GitHub Actions recommended)

Ready to create these files?

```

## Quality Checklist

Before completing setup:
- [ ] All essential configs present
- [ ] Pre-commit hooks installed and tested
- [ ] README documents setup process
- [ ] .gitignore covers common patterns
- [ ] Quality tooling configured
- [ ] Dependencies documented
- [ ] Example .env file provided (no secrets!)
- [ ] Tests directory created

## Common Mistakes to Avoid

### 1. No .gitignore
**Problem**: Commits unwanted files (node_modules, .env, etc.)
**Fix**: Create comprehensive .gitignore first

### 2. Inconsistent Formatting
**Problem**: Merge conflicts from formatting differences
**Fix**: Set up Prettier/Black and .editorconfig

### 3. No Pre-commit Hooks
**Problem**: Issues caught late in CI or code review
**Fix**: Install pre-commit hooks from start

### 4. Hardcoded Secrets
**Problem**: Credentials committed to Git
**Fix**: Use .env files + detect-secrets hook

### 5. Missing Type Checking
**Problem**: Type errors caught at runtime
**Fix**: Enable TypeScript/Mypy from start

### 6. No Documentation
**Problem**: New developers struggle with setup
**Fix**: Maintain clear README with setup steps

## Success Criteria

Good project setup:
- Developer can clone and run in <5 minutes
- Quality checks run automatically
- Consistent formatting across team
- No secrets in repository
- Clear documentation
- Minimal friction for contributors

## Related Capabilities

- **Skill**: "Architecting Solutions" for design decisions
- **Skill**: "Reviewing Code" for quality validation
- **Agent**: Builder agent for code generation
- **Documentation**: `Specs/PreCommitHooks.md`
- **Templates**: `.claude/templates/`

---

Remember: Time spent on setup saves exponentially more time fixing avoidable issues later. Start with quality automation from day one.
```
