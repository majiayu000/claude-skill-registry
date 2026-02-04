---
name: file-organization-assistant
version: "1.0.0"
category: coordination
description: "File Organization AI Assistant"
---

# File Organization AI Assistant

> **Version:** 1.0.0
> **Created:** 2026-01-05
> **Category:** workspace-hub
> **Related Skills:** knowledge-base-system, compliance-check

## Overview

AI-driven file organization following FILE_ORGANIZATION_STANDARDS.md. Proposes folder structure when 5+ files accumulate, waits for approval, then executes organization with import updates.

## Trigger Conditions

**Propose organization when:**
- 5+ files of similar type in one directory
- Logical grouping emerges (analysis, validation, etc.)
- Module complexity requires separation
- Code duplication suggests shared functionality

## Organization Workflow

### Step 1: Recognize Need

```python
def check_organization_needed(directory):
    """Detect when organization is needed."""
    files = list(directory.glob('*.py'))

    if len(files) >= 5:
        # Analyze for patterns
        patterns = detect_patterns(files)
        if patterns:
            return propose_structure(patterns)

    return None
```

### Step 2: Propose Structure

```
AI: "I notice 12 files related to data analysis. I propose:

data_analysis/
├── processing/    # Data processing (4 files)
├── validation/    # Data validation (3 files)
├── visualization/ # Plotting and charts (3 files)
└── reporting/     # Report generation (2 files)

Each subfolder organized by function.
Should I proceed with this organization?"
```

### Step 3: Wait for Approval

```python
user_approval = wait_for_approval()

if not user_approval:
    return  # Don't proceed

# Only proceed after explicit approval
organize_files(proposed_structure)
```

### Step 4: Execute Organization

```python
def organize_files(structure):
    """Organize files and update imports."""
    for folder, files in structure.items():
        # Create subfolder
        folder_path = create_folder(folder)

        # Move files
        for file in files:
            move_file(file, folder_path)

        # Update imports in moved files
        update_imports(files)

        # Update imports in files that reference moved files
        update_referencing_files(files)

    # Commit with clear message
    git_commit(f"Organize {module_name} into subfolders\n\n{structure_description}")
```

## Naming Conventions

### Domain-Driven (Top Level)

**Good:**
- `marine_analysis/` (domain: marine engineering)
- `data_processing/` (domain: data operations)
- `authentication/` (domain: user auth)

**Bad:**
- `python_files/` (technical, not domain)
- `misc/` (unclear purpose)

### Functional (Subfolders)

```
marine_analysis/
├── loads/         # Load calculations
├── stress/        # Stress analysis
├── validation/    # Result validation
└── reporting/     # Report generation
```

## Standard Structures

### Python Module

```
module_name/
├── __init__.py
├── core/          # Core functionality
│   ├── __init__.py
│   └── processor.py
├── models/        # Data models
│   ├── __init__.py
│   └── schema.py
├── utils/         # Module utilities
│   ├── __init__.py
│   └── helpers.py
└── io/            # Input/output
    ├── __init__.py
    └── readers.py
```

### Test Organization (Mirror src/)

```
tests/
├── unit/
│   └── module_name/
│       ├── test_core.py
│       └── test_utils.py
├── integration/
│   └── test_pipeline.py
└── fixtures/
    └── sample_data.csv
```

## Import Update Automation

```python
def update_imports(file_path, old_path, new_path):
    """Update imports after file move."""
    content = file_path.read_text()

    # Update relative imports
    old_import = f"from {old_path}"
    new_import = f"from {new_path}"
    content = content.replace(old_import, new_import)

    # Update absolute imports
    old_import = f"import {old_path}"
    new_import = f"import {new_path}"
    content = content.replace(old_import, new_import)

    file_path.write_text(content)
```

## Validation

**Before organizing:**
- [ ] Identified 5+ files for organization
- [ ] Recognized clear pattern or domain
- [ ] Folder depth won't exceed 5 levels
- [ ] Prepared clear proposal with rationale

**After organizing:**
- [ ] All imports updated
- [ ] All tests still passing
- [ ] Documentation updated
- [ ] Git commit with clear message

---

**Remember: Good organization emerges naturally. Wait until patterns are clear!** 📁
