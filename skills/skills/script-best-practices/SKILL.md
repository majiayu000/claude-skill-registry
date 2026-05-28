---
name: script-best-practices
description: Best practices for bundling scripts in skills including error handling, constants documentation, and execution patterns. Use when creating script-enabled skills.
---

# Script Best Practices

Guidelines for bundling executable scripts in skills.

## When to Bundle Scripts

Bundle scripts when:
- Same code would be rewritten repeatedly
- Deterministic reliability needed
- Complex validation required
- Token cost of generation exceeds execution cost

## Error Handling

Always handle errors explicitly rather than punting to Claude:

```python
# Good: Handle errors explicitly
def process(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"Creating {path}")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        print(f"ERROR: Cannot access {path} - check permissions")
        return None

# Bad: Let errors propagate unexpectedly
def process(path):
    with open(path) as f:
        return f.read()  # Will crash on missing file
```

## Document Constants

Every magic number needs rationale:

```python
# Good: Document constants
TIMEOUT = 30  # HTTP requests typically complete in 30s
MAX_RETRIES = 3  # Most failures resolve by second retry
BATCH_SIZE = 100  # Balance between memory and API calls

# Bad: Magic numbers
TIMEOUT = 47  # Why 47?
MAX_RETRIES = 3  # Why 3?
```

## Clarify Intent in SKILL.md

Be explicit about how scripts should be used:

**Execute the script:**
```markdown
Run `scripts/analyze.py` to extract form fields from the PDF.
```

**Read as reference:**
```markdown
See `scripts/analyze.py` for the extraction algorithm (do not run directly).
```

## Script Organization

```
skill-name/
  SKILL.md
  scripts/
    analyze.py      # Main entry point
    validate.py     # Validation utilities
    helpers/        # Shared utilities
      formatting.py
      parsing.py
```

## Dependencies

Always list dependencies explicitly:

```markdown
## Requirements

Before running scripts:
```bash
pip install pdfplumber python-docx
```

Or with the provided requirements file:
```bash
pip install -r scripts/requirements.txt
```
```

## Exit Codes

Use consistent exit codes:

```python
import sys

EXIT_SUCCESS = 0
EXIT_INVALID_INPUT = 1
EXIT_FILE_NOT_FOUND = 2
EXIT_PERMISSION_ERROR = 3

def main():
    if not validate_input():
        sys.exit(EXIT_INVALID_INPUT)
    # ... process ...
    sys.exit(EXIT_SUCCESS)
```

## Output Formatting

Make output parseable:

```python
# Good: Structured output
import json

result = {
    "status": "success",
    "files_processed": 5,
    "errors": []
}
print(json.dumps(result))

# Bad: Unstructured output
print("Done! Processed 5 files with no errors.")
```

## Idempotency

Scripts should be safe to run multiple times:

```python
def ensure_directory(path):
    """Create directory if it doesn't exist (idempotent)."""
    os.makedirs(path, exist_ok=True)

def write_if_changed(path, content):
    """Only write if content differs (idempotent)."""
    if os.path.exists(path):
        with open(path) as f:
            if f.read() == content:
                return False  # No change needed
    with open(path, 'w') as f:
        f.write(content)
    return True
```
