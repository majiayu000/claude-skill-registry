---
name: add-dep
description: Safely install a Python package, verify it imports correctly, and pin it to requirements.txt
---

# Add Dependency Skill

Safely add a new Python dependency to the project with verification and pinning.

## When to Use

- User asks to "add", "install", or "use" a new package
- You need to add a dependency for implementing a feature
- Upgrading or changing an existing dependency

## Process

### Step 1: Install the Package

```bash
pip install --no-input PACKAGE_NAME
```

For a specific version:

```bash
pip install --no-input PACKAGE_NAME==1.2.3
```

### Step 2: Verify Import Works

```bash
python -c "import PACKAGE_NAME; print(f'{PACKAGE_NAME.__name__} v{getattr(PACKAGE_NAME, \"__version__\", \"unknown\")} OK')"
```

For packages with different import names:

```bash
# PIL is imported as pillow
python -c "from PIL import Image; print('Pillow OK')"

# sklearn is imported from scikit-learn
python -c "import sklearn; print('scikit-learn OK')"
```

### Step 3: Get Installed Version

```bash
pip show PACKAGE_NAME | grep Version
```

### Step 4: Pin to requirements.txt

Add the exact installed version to `requirements.txt` with robust duplicate checking:

```bash
# Get the exact version using pip show (not grep which can match partial names)
VERSION=$(pip show PACKAGE_NAME | grep "^Version:" | cut -d' ' -f2)

# Check if package already exists (case-insensitive, any version specifier, handles whitespace)
# Matches: package==1.0, package >= 1.0, package~=1.0, Package==1.0, etc.
if grep -iEq "^PACKAGE_NAME[[:space:]]*[<>=!~\[]" requirements.txt 2>/dev/null || grep -iq "^PACKAGE_NAME$" requirements.txt 2>/dev/null; then
    # Update existing entry (handles optional whitespace around operators)
    sed -i "s/^[Pp][Aa][Cc][Kk][Aa][Gg][Ee]_[Nn][Aa][Mm][Ee][[:space:]]*[<>=!~\[].*/PACKAGE_NAME==$VERSION/I" requirements.txt
    sed -i "s/^[Pp][Aa][Cc][Kk][Aa][Gg][Ee]_[Nn][Aa][Mm][Ee]$/PACKAGE_NAME==$VERSION/I" requirements.txt
    echo "Updated PACKAGE_NAME==$VERSION in requirements.txt"
else
    # Add new entry
    echo "PACKAGE_NAME==$VERSION" >> requirements.txt
    echo "Added PACKAGE_NAME==$VERSION to requirements.txt"
fi
```

**Important Notes**:

- Uses case-insensitive matching (`-i` flag) to catch `Requests` vs `requests`
- Handles whitespace around operators (`requests >= 2.0` and `requests>=2.0`)
- Detects any version specifier: `==`, `>=`, `<=`, `~=`, `!=`, `[extras]`
- Also catches bare package names without version specifiers
- Do NOT use `pip freeze | grep` as it can match partial names (e.g., `requests` matching `requests-oauthlib`)

### Step 5: Verify requirements.txt

```bash
# Use case-insensitive match to verify
grep -i "^PACKAGE_NAME" requirements.txt
```

## Common Package Mappings

Some packages have different install and import names:

| pip install      | python import |
| ---------------- | ------------- |
| `Pillow`         | `PIL`         |
| `scikit-learn`   | `sklearn`     |
| `beautifulsoup4` | `bs4`         |
| `python-dotenv`  | `dotenv`      |
| `PyYAML`         | `yaml`        |
| `opencv-python`  | `cv2`         |

## Example: Adding requests

```bash
# 1. Install
pip install --no-input requests

# 2. Verify
python -c "import requests; print(requests.__version__)"

# 3. Pin (with case-insensitive duplicate check, handles whitespace)
VERSION=$(pip show requests | grep "^Version:" | cut -d' ' -f2)
if ! grep -iEq "^requests[[:space:]]*[<>=!~\[]" requirements.txt 2>/dev/null; then
    echo "requests==$VERSION" >> requirements.txt
fi

# 4. Confirm
grep "^requests==" requirements.txt
```

Output:

```
2.31.0
requests==2.31.0
```

## Example: Adding pandas with specific version

```bash
# 1. Install specific version
pip install --no-input pandas==2.1.0

# 2. Verify
python -c "import pandas as pd; print(pd.__version__)"

# 3. Pin
echo "pandas==2.1.0" >> requirements.txt
```

## Dev Dependencies

For development-only dependencies (testing, linting), add to `requirements-dev.txt`:

```bash
pip install --no-input pytest
VERSION=$(pip show pytest | grep "^Version:" | cut -d' ' -f2)
if ! grep -iEq "^pytest[[:space:]]*[<>=!~\[]" requirements-dev.txt 2>/dev/null; then
    echo "pytest==$VERSION" >> requirements-dev.txt
fi
```

## Handling Failures

### Installation Fails

```bash
# Check if package name is correct
pip search PACKAGE_NAME  # May be disabled

# Try with verbose output
pip install --no-input -v PACKAGE_NAME
```

### Import Fails

```bash
# Check installed packages
pip list | grep -i PACKAGE_NAME

# Check for correct import name
pip show PACKAGE_NAME | grep -E "Name|Location"
```

### Version Conflict

```bash
# See what's conflicting
pip check

# See dependency tree
pip install --no-input pipdeptree && pipdeptree
```

## Web Environment Notes

In Claude Code Web (headless):

- Always use `--no-input` flag
- Suppress progress bar with `--progress-bar off`
- Verify immediately after install (session may restart)

```bash
pip install --no-input --progress-bar off PACKAGE_NAME && \
python -c "import PACKAGE_NAME; print('OK')"
```
