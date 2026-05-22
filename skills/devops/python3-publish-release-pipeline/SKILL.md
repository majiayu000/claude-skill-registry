---
name: python3-publish-release-pipeline
description: Set up CI/CD pipeline for Python package publishing to PyPI. Use when preparing to publish a package, when setting up automated releases, or when configuring GitHub Actions or GitLab CI for Python projects.
user-invocable: true
argument-hint: "[github|gitlab]"
---

# Python Release Pipeline Configuration

The model configures CI/CD pipelines for automated Python package publishing.

## Arguments

$ARGUMENTS

If no argument provided, detect from repository (look for `.github/` or `.gitlab-ci.yml`).

## Instructions

1. **Detect CI platform** (GitHub Actions or GitLab CI)
2. **Create workflow files** for testing, linting, and publishing
3. **Configure secrets** documentation for PyPI tokens
4. **Set up version management** with git tags
5. **Document release process**

---

## GitHub Actions Pipeline

### Directory Structure

```text
.github/
├── workflows/
│   ├── ci.yml           # Run on every push/PR
│   ├── release.yml      # Run on version tags
│   └── docs.yml         # Optional: documentation
└── dependabot.yml       # Optional: dependency updates
```

### CI Workflow (ci.yml)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Set up Python
        run: uv python install 3.11

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run ruff
        run: |
          uv run ruff check src/ tests/
          uv run ruff format --check src/ tests/

      - name: Run mypy
        run: uv run mypy src/

  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run tests
        run: uv run pytest tests/ -v --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: false
```

### Release Workflow (release.yml)

```yaml
name: Release

on:
  push:
    tags:
      - "v*.*.*"

permissions:
  contents: write
  id-token: write  # Required for trusted publishing

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.11

      - name: Build package
        run: uv build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  # Option 1: Trusted Publishing (Recommended)
  publish-pypi:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/your-package
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        # No token needed with trusted publishing!

  # Option 2: Token-based Publishing (Alternative)
  # publish-pypi:
  #   needs: build
  #   runs-on: ubuntu-latest
  #   steps:
  #     - name: Download artifacts
  #       uses: actions/download-artifact@v4
  #       with:
  #         name: dist
  #         path: dist/
  #
  #     - name: Publish to PyPI
  #       uses: pypa/gh-action-pypi-publish@release/v1
  #       with:
  #         password: ${{ secrets.PYPI_API_TOKEN }}

  github-release:
    needs: [build, publish-pypi]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: dist/*
          generate_release_notes: true
```

---

## GitLab CI Pipeline

### .gitlab-ci.yml

```yaml
stages:
  - lint
  - test
  - build
  - publish

variables:
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.uv-cache"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

default:
  image: python:3.11-slim
  before_script:
    - pip install uv
    - uv sync --all-extras
  cache:
    key: "${CI_JOB_NAME}"
    paths:
      - .uv-cache/
      - .pip-cache/
      - .venv/

lint:
  stage: lint
  script:
    - uv run ruff check src/ tests/
    - uv run ruff format --check src/ tests/
    - uv run mypy src/

test:
  stage: test
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.11", "3.12", "3.13"]
  image: python:${PYTHON_VERSION}-slim
  script:
    - uv run pytest tests/ -v --cov=src --cov-report=xml --junitxml=report.xml
  coverage: '/TOTAL.*\s+(\d+%)/'
  artifacts:
    reports:
      junit: report.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  script:
    - uv build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

# Publish to PyPI on tags
publish:pypi:
  stage: publish
  rules:
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/
  script:
    - uv publish --token $PYPI_TOKEN
  environment:
    name: pypi
    url: https://pypi.org/project/your-package

# Publish to GitLab Package Registry on tags
publish:gitlab:
  stage: publish
  rules:
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/
  script:
    - |
      TWINE_PASSWORD=${CI_JOB_TOKEN} \
      TWINE_USERNAME=gitlab-ci-token \
      uv publish --publish-url ${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/pypi
  environment:
    name: gitlab-registry
```

---

## Trusted Publishing Setup (PyPI)

### Why Trusted Publishing?

- No API tokens to manage
- No secrets to rotate
- Cannot be leaked
- Scoped to specific workflows

### Setup Steps

1. **Go to PyPI** → Your Project → Publishing

2. **Add GitHub Publisher**:

   - Owner: `your-username`
   - Repository: `your-repo`
   - Workflow name: `release.yml`
   - Environment: `pypi` (optional but recommended)

3. **Create GitHub Environment**:
   - Settings → Environments → New environment: `pypi`
   - Add protection rules (optional):
     - Required reviewers
     - Restrict to tags only

### Alternative: API Token

If trusted publishing isn't available:

1. **Create PyPI Token**:

   - PyPI → Account Settings → API tokens
   - Create token scoped to your project

2. **Add to Repository Secrets**:
   - GitHub: Settings → Secrets → `PYPI_API_TOKEN`
   - GitLab: Settings → CI/CD → Variables → `PYPI_TOKEN`

---

## Version Management

### Manual Version (pyproject.toml)

Update version in `pyproject.toml` before tagging:

```toml
[project]
version = "1.2.3"
```

### Dynamic Version from Git Tags

**Using hatch-vcs**:

```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
dynamic = ["version"]

[tool.hatch.version]
source = "vcs"

[tool.hatch.build.hooks.vcs]
version-file = "src/my_package/_version.py"
```

### Release Workflow

```bash
# 1. Update CHANGELOG.md

# 2. Commit changes
git add -A
git commit -m "Prepare release v1.2.3"

# 3. Create annotated tag
git tag -a v1.2.3 -m "Release v1.2.3"

# 4. Push with tags
git push origin main --tags
```

---

## TestPyPI for Testing

### GitHub Actions TestPyPI Job

```yaml
publish-testpypi:
  needs: build
  runs-on: ubuntu-latest
  environment:
    name: testpypi
    url: https://test.pypi.org/p/your-package
  steps:
    - uses: actions/download-artifact@v4
      with:
        name: dist
        path: dist/

    - uses: pypa/gh-action-pypi-publish@release/v1
      with:
        repository-url: https://test.pypi.org/legacy/
```

### Manual TestPyPI Upload

```bash
# Build
uv build

# Upload to TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/ --token $TESTPYPI_TOKEN

# Test install
uv pip install --index-url https://test.pypi.org/simple/ your-package
```

---

## Required Configuration Files

### Minimum Files for Publishing

```text
your-package/
├── pyproject.toml          # Package metadata and build config
├── README.md               # Required by PyPI
├── LICENSE                 # Required for distribution
├── src/
│   └── your_package/
│       ├── __init__.py
│       └── py.typed        # PEP 561 marker
└── .github/
    └── workflows/
        ├── ci.yml
        └── release.yml
```

### pyproject.toml Checklist

```text
- [ ] [build-system] with requires and build-backend
- [ ] [project] with name, version, description
- [ ] readme = "README.md"
- [ ] license specified
- [ ] requires-python = ">=3.11"
- [ ] authors with name and email
- [ ] classifiers (Development Status, License, Python versions)
- [ ] dependencies list
- [ ] [project.urls] with Documentation, Issues, Source
- [ ] [project.scripts] if CLI tool
```

---

## Security Best Practices

1. **Use Trusted Publishing** over API tokens
2. **Scope tokens** to specific projects (not account-wide)
3. **Use environments** with protection rules
4. **Pin action versions** with full SHA or version tags
5. **Review workflow changes** carefully
6. **Enable branch protection** on main

---

## Troubleshooting

### Build Fails

```bash
# Check package metadata
uv run python -m build --no-isolation
uvx twine check dist/*
```

### Upload Fails

```bash
# Verify token
echo $PYPI_TOKEN | head -c 10

# Check package name availability
curl https://pypi.org/pypi/your-package/json
```

### Version Already Exists

PyPI doesn't allow re-uploading the same version. Increment version and create new tag.

---

## References

- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [GitLab CI/CD for Python](https://docs.gitlab.com/ee/ci/examples/python.html)
- [uv Publishing](https://docs.astral.sh/uv/guides/publish/)
