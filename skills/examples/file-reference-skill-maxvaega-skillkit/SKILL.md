---
name: file-reference-skill
description: Example skill demonstrating secure file reference resolution with supporting files
allowed-tools: []
---

# File Reference Skill

This skill demonstrates how to use supporting files (scripts, templates, documentation) within a skill directory.

## Overview

This skill uses helper scripts and templates for data processing. All supporting files are accessible via relative paths from the skill's base directory.

## Available Supporting Files

### Scripts
- `scripts/data_processor.py` - Main data processing script
- `scripts/validator.py` - Input validation utilities
- `scripts/helper.sh` - Shell helper script

### Templates
- `templates/config.yaml` - Configuration template
- `templates/report.md` - Report generation template

### Documentation
- `docs/usage.md` - Detailed usage instructions
- `docs/examples.md` - Example use cases

## Usage

When this skill is invoked with arguments, it can access supporting files using the FilePathResolver:

```python
from pathlib import Path
from skillkit.core.path_resolver import FilePathResolver

# Get the skill's base directory (injected by BaseDirectoryProcessor)
base_dir = Path("<base_directory_from_context>")

# Resolve supporting files securely
processor_script = FilePathResolver.resolve_path(base_dir, "scripts/data_processor.py")
config_template = FilePathResolver.resolve_path(base_dir, "templates/config.yaml")
usage_docs = FilePathResolver.resolve_path(base_dir, "docs/usage.md")

# Read file contents
with open(processor_script) as f:
    script_code = f.read()
```

## Processing Arguments

The skill expects data file paths as arguments:

**Example invocation**: `file-reference-skill data/input.csv data/output.csv`

Processing steps:
1. Validate input using `scripts/validator.py`
2. Process data using `scripts/data_processor.py`
3. Generate report using `templates/report.md`
4. Output results to specified location

## Security Notes

- All file paths are validated to prevent directory traversal attacks
- Symlinks are resolved and verified to stay within skill directory
- Absolute paths and path traversal patterns (../) are blocked
- Any security violation raises PathSecurityError with detailed logging
