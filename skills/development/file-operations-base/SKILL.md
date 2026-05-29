---
name: file-operations-base
description: Base module providing reusable file operations patterns for CUI workflow scripts
allowed-tools: Bash
---

# File Operations Base Skill

**Role**: Shared Python module providing atomic file operations, metadata parsing, JSON output helpers, and base directory configuration for CUI workflow scripts.

## What This Skill Provides

- Workflow base directory configuration (`.plan/` by default)
- Path construction helpers for workflow files
- Atomic file write (temp file + rename pattern)
- Directory creation (mkdir -p equivalent)
- JSON success/error output helpers
- Markdown key=value metadata parsing
- Markdown metadata generation

## When to Use

Import `file_ops` module in Python scripts that write to `.plan/` directories:
- Lessons learned scripts
- Plan file scripts
- Memory management scripts
- Any script requiring atomic writes to workflow directories

## Module: file_ops.py

**Location**: `scripts/file_ops.py`

### Functions

**Base Directory Functions**

**1. get_base_dir()**
- **Purpose**: Get the base directory for workflow files
- **Input**: None
- **Output**: `Path` - base directory (default: `.plan`)

**2. set_base_dir(path)**
- **Purpose**: Override the base directory for workflow files
- **Input**: `path` (str/Path) - new base directory
- **Output**: None
- **Note**: Primarily for testing; production uses `.plan` default

**3. base_path(*parts)**
- **Purpose**: Construct a path within the workflow base directory
- **Input**: `*parts` - path components to join
- **Output**: `Path` - full path including workflow base directory
- **Example**: `base_path('plans', 'my-task', 'plan.md')` → `.plan/plans/my-task/plan.md`

**File Operations**

**4. atomic_write_file(path, content)**
- **Purpose**: Write file atomically using temp file + rename
- **Input**: `path` (str/Path), `content` (str)
- **Output**: None (raises on error)
- **Pattern**: Creates temp file, writes, renames to target

**5. ensure_directory(path)**
- **Purpose**: Create directory and parents if needed
- **Input**: `path` (str/Path) - file or directory path
- **Output**: None
- **Note**: If path looks like file, creates parent directory

**JSON Output Helpers**

**6. output_success(operation, **kwargs)**
- **Purpose**: Print JSON success output to stdout
- **Input**: `operation` (str), additional kwargs
- **Output**: Prints JSON to stdout

**7. output_error(operation, error)**
- **Purpose**: Print JSON error output to stderr
- **Input**: `operation` (str), `error` (str)
- **Output**: Prints JSON to stderr

**Metadata Functions**

**8. parse_markdown_metadata(content)**
- **Purpose**: Parse key=value metadata from markdown
- **Input**: `content` (str) - full file content
- **Output**: `dict` - metadata key-value pairs
- **Format**: Supports `key=value` and `key.subkey=value` (dot notation)

**9. generate_markdown_metadata(data)**
- **Purpose**: Generate key=value metadata block
- **Input**: `data` (dict) - metadata to serialize
- **Output**: `str` - formatted metadata block

**10. update_markdown_metadata(content, updates)**
- **Purpose**: Update specific metadata fields in markdown content
- **Input**: `content` (str), `updates` (dict)
- **Output**: `str` - updated content

**11. get_metadata_content_split(content)**
- **Purpose**: Split markdown content into metadata and body
- **Input**: `content` (str)
- **Output**: `tuple[str, str]` - (metadata_block, body_content)

---

## Usage Example

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/path/to/file-operations-base/scripts')
from file_ops import (
    atomic_write_file,
    base_path,
    output_success,
    output_error,
    generate_markdown_metadata
)

def main():
    try:
        # Construct path within .plan directory
        filepath = base_path('lessons-learned', '2025-11-28-001.md')

        # Generate metadata
        metadata = generate_markdown_metadata({
            'id': '2025-11-28-001',
            'component.type': 'command',
            'applied': 'false'
        })

        # Write atomically (creates directories automatically)
        content = f"{metadata}\n# Lesson Title\n\nContent here..."
        atomic_write_file(filepath, content)

        output_success('write-lesson', file=str(filepath))
    except Exception as e:
        output_error('write-lesson', str(e))
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `file_ops.py` | Core file operations module (importable) |
| `test-file-ops.py` | Test suite for file operations |

---

## Integration

### With manage-lessons-learned

```python
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'file-operations-base' / 'scripts'))
from file_ops import atomic_write_file, base_path, output_success, output_error
```

### With plan-files

```python
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'plan-marshall' / 'skills' / 'file-operations-base' / 'scripts'))
from file_ops import atomic_write_file, base_path, output_success, output_error
```

## Directory Structure

Files are stored in `.plan/` directory:

```
.plan/                         # Workflow artifacts
├── run-configuration.json     # Command execution tracking
├── lessons-learned/           # Knowledge capture
│   └── *.md
├── memory/                    # Session state
│   ├── context/*.json
│   └── handoffs/*.json
└── plans/                     # Task plans
    └── {task-name}/
        ├── plan.md
        ├── config.toon
        └── references.toon
```

---

## Cross-Domain Access Pattern

When scripts in one domain (e.g., `pm-workflow:plan-files`) need to access resources in another domain (e.g., `plan-marshall:manage-lessons-learned`), follow the **ID-based access pattern**.

### Principle

**Scripts take IDs, not paths, for cross-domain resources.** The script resolves the ID to a path internally using `base_path()`.

### Why This Matters

- **Encapsulation**: Each domain owns its file structure; other domains should not construct paths
- **Maintainability**: Path format changes only require updating the owning domain's script
- **Testability**: ID-based APIs are easier to mock and test
- **Error clarity**: Scripts can provide domain-specific error messages for invalid IDs

### Correct Pattern

```python
# Script in planning domain needs to access lesson from lessons-learned domain
# CORRECT: Accept ID, resolve path internally

def copy_lesson_to_plan(lesson_id: str, plan_dir: Path) -> dict:
    # Resolve ID to path internally
    lesson_file = base_path("lessons-learned", f"{lesson_id}.md")

    if not lesson_file.exists():
        return {"success": False, "error": f"Lesson not found: {lesson_id}"}

    # Proceed with copy...
```

### Incorrect Pattern (Anti-Pattern)

```python
# WRONG: Orchestrator constructs path and passes it to script

# In orchestrator (phase-management SKILL.md):
python3 {script} --lesson-file {lesson.file}  # BAD: orchestrator builds path

# In script:
def copy_lesson_to_plan(lesson_file: Path, plan_dir: Path):  # BAD: accepts path
    pass
```

### When to Use ID-Based Access

| Scenario | Use ID-Based | Reason |
|----------|--------------|--------|
| Cross-domain resource access | Yes | Scripts own their domain's paths |
| Same-domain resource access | Optional | Same skill owns both paths |
| User-specified file | No | User explicitly provides path |
| Configuration files | No | Paths defined in config are explicit |

### Implementation Checklist

When creating scripts that access cross-domain resources:

1. [ ] Accept resource ID (e.g., `--lesson-id`) not path
2. [ ] Import `base_path` from file_ops
3. [ ] Resolve path internally: `base_path("domain-dir", f"{id}.md")`
4. [ ] Return clear error if resource not found
5. [ ] Document the expected ID format in help text

