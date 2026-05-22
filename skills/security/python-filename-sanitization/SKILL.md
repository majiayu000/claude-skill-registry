---
name: python-filename-sanitization
description: |
  Secure filename sanitization pattern for Python web applications. Use when:
  (1) Accepting user-provided filenames for file operations, (2) Building file
  rename/upload functionality, (3) Preventing path traversal attacks (../../../etc/passwd),
  (4) Preventing shell injection through filenames, (5) FastAPI/Flask file handling.
  Provides regex-based whitelist approach with pathlib for safe file operations.
author: Claude Code
version: 1.0.0
date: 2025-01-31
---

# Python Filename Sanitization

## Problem
User-provided filenames can contain malicious characters that enable path traversal
attacks, shell injection, or filesystem corruption. Direct use of user input in
file paths is a security vulnerability.

## Context / Trigger Conditions
- Building file upload, rename, or download functionality
- User can specify filenames via API or form input
- Files are stored on server filesystem
- Need to prevent: `../`, shell metacharacters, null bytes, etc.

## Solution

### Complete Sanitization Function
```python
import re
from pathlib import Path

def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Sanitize a filename to prevent path traversal and shell injection.
    Only allows alphanumeric characters, spaces, hyphens, underscores,
    parentheses, and dots.
    """
    if not filename:
        raise ValueError("Filename cannot be empty")

    # Remove any path components (prevent path traversal)
    filename = Path(filename).name

    # Only allow safe characters: alphanumeric, space, hyphen, underscore, parentheses, dot
    # This regex removes anything that isn't in the allowed set
    safe_filename = re.sub(r'[^a-zA-Z0-9\s\-_().]', '', filename)

    # Collapse multiple spaces/dots
    safe_filename = re.sub(r'\s+', ' ', safe_filename)
    safe_filename = re.sub(r'\.+', '.', safe_filename)

    # Strip leading/trailing whitespace and dots
    safe_filename = safe_filename.strip(' .')

    # Limit length
    if len(safe_filename) > max_length:
        safe_filename = safe_filename[:max_length]

    if not safe_filename:
        raise ValueError("Filename contains no valid characters")

    return safe_filename
```

### FastAPI Integration Example
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

class RenameRequest(BaseModel):
    new_name: str

@router.patch("/files/{file_id}/rename")
async def rename_file(file_id: str, request: RenameRequest):
    """Rename a file with sanitized input."""
    file_dir = Path("/data/files") / file_id

    if not file_dir.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Find existing file
    files = list(file_dir.glob("*"))
    if not files:
        raise HTTPException(status_code=404, detail="No file found")

    current_file = files[0]
    current_extension = current_file.suffix

    # Sanitize the new name
    try:
        safe_name = sanitize_filename(request.new_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Preserve original extension
    if not safe_name.lower().endswith(current_extension.lower()):
        safe_name = safe_name + current_extension

    # Create new path (same directory, new filename)
    new_file = file_dir / safe_name

    # Check for conflicts
    if new_file.exists() and new_file != current_file:
        raise HTTPException(status_code=400, detail="A file with that name already exists")

    # Rename using pathlib (no shell commands!)
    current_file.rename(new_file)

    return {"status": "renamed", "new_filename": safe_name}
```

## Key Security Principles

### 1. Whitelist, Don't Blacklist
```python
# BAD: Trying to block dangerous characters
filename = filename.replace('../', '').replace('\x00', '')

# GOOD: Only allow known-safe characters
safe_filename = re.sub(r'[^a-zA-Z0-9\s\-_().]', '', filename)
```

### 2. Use pathlib, Not Shell Commands
```python
# BAD: Shell command (vulnerable to injection)
os.system(f'mv "{old_path}" "{new_path}"')

# GOOD: Pure Python (no shell)
old_path.rename(new_path)
```

### 3. Extract Basename First
```python
# BAD: User could submit "../../../etc/passwd"
filename = user_input

# GOOD: Extract just the filename part
filename = Path(user_input).name
```

### 4. Validate After Sanitization
```python
# Ensure something remains after sanitization
if not safe_filename:
    raise ValueError("Filename contains no valid characters")
```

## Verification
```python
# Test cases that should be handled safely
assert sanitize_filename("normal.txt") == "normal.txt"
assert sanitize_filename("../../../etc/passwd") == "etcpasswd"
assert sanitize_filename("file; rm -rf /") == "file rm -rf"
assert sanitize_filename("  spaces  .txt") == "spaces.txt"
assert sanitize_filename("$(whoami).txt") == "whoami.txt"

# Test cases that should raise errors
try:
    sanitize_filename("")  # Should raise ValueError
except ValueError:
    pass

try:
    sanitize_filename("$#@!")  # Should raise ValueError (no valid chars)
except ValueError:
    pass
```

## Notes
- This is intentionally restrictive; expand the regex if you need Unicode support
- For Unicode filenames, consider `unicodedata.normalize('NFKD', ...)` first
- Max length of 200 is conservative; filesystem limits vary (255 bytes typical)
- Always preserve file extensions when renaming to avoid breaking file associations
- Consider adding a UUID prefix for guaranteed uniqueness in upload scenarios

## References
- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)
- [Python pathlib documentation](https://docs.python.org/3/library/pathlib.html)
