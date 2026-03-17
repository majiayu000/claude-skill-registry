---
name: inspecting-skills
description: Discovers and indexes Python code in skills, enabling cross-skill imports. Use when importing functions from other skills or analyzing skill codebases.
metadata:
  version: 1.0.2
---

# Inspecting Skills

Discover Python code across skills and enable universal imports. Solves the dash-underscore naming mismatch between skill directories (e.g., `browsing-bluesky`) and Python imports (e.g., `browsing_bluesky`).

## Installation

```python
import sys
sys.path.insert(0, '/home/user/claude-skills')
from inspecting_skills import setup_skill_path, skill_import
```

## Quick Start

### Import a Skill

```python
from inspecting_skills import skill_import

# Import by skill name (dash or underscore form)
bsky = skill_import("browsing-bluesky")
posts = bsky.search_posts("python")

# Import specific functions
search, profile = skill_import("browsing-bluesky", ["search_posts", "get_profile"])
```

### Enable Transparent Imports

```python
from inspecting_skills import setup_skill_path

# Configure once at session start
setup_skill_path("/home/user/claude-skills")

# Now import skills directly (underscore form)
from browsing_bluesky import search_posts, get_profile
from remembering import remember, recall
```

### Discover Available Skills

```python
from inspecting_skills import list_importable_skills

skills = list_importable_skills()
for s in skills:
    print(f"{s['name']} -> import {s['module_name']}")
```

## Core Functions

### Discovery

| Function | Purpose |
|----------|---------|
| `discover_skill(path)` | Analyze a single skill directory |
| `discover_all_skills(root)` | Find all skills with Python code |
| `find_skill_by_name(name, root)` | Find skill by name (either form) |
| `skill_name_to_module(name)` | Convert "browsing-bluesky" to "browsing_bluesky" |

### Indexing

| Function | Purpose |
|----------|---------|
| `index_skill(layout)` | Extract symbols from a discovered skill |
| `index_all_skills(root)` | Index all skills in repository |
| `generate_registry(root, output)` | Create registry.json manifest |

### Importing

| Function | Purpose |
|----------|---------|
| `setup_skill_path(root)` | Enable transparent skill imports |
| `skill_import(name, symbols)` | Import skill or specific symbols |
| `register_skill(name, path)` | Register skill at custom path |
| `list_importable_skills()` | List all importable skills |

## Skill Layouts

Skills organize Python code in three patterns:

### 1. Scripts Directory
```
browsing-bluesky/
  SKILL.md
  __init__.py          # Re-exports from scripts/
  scripts/
    __init__.py
    bsky.py            # Main implementation
```

### 2. Root-Level Modules
```
remembering/
  SKILL.md
  __init__.py          # Re-exports functions
  memory.py            # Core functionality
  boot.py
  config.py
```

### 3. Simple Package
```
simple-skill/
  SKILL.md
  __init__.py          # Contains all code
```

## Generating a Registry

Create a `registry.json` for offline symbol lookup:

```python
from inspecting_skills import generate_registry
from pathlib import Path

registry = generate_registry(
    Path("/home/user/claude-skills"),
    output_path=Path("registry.json")
)

# Registry structure:
# {
#   "version": "1.0.0",
#   "skills": {
#     "browsing-bluesky": {
#       "module_name": "browsing_bluesky",
#       "exports": ["search_posts", "get_profile", ...],
#       "modules": [...]
#     }
#   }
# }
```

## Indexing a Single Skill

```python
from inspecting_skills import discover_skill, index_skill
from pathlib import Path

# Discover the skill layout
layout = discover_skill(Path("/home/user/claude-skills/remembering"))
print(f"Layout: {layout.layout_type}")
print(f"Has __init__.py: {layout.has_init}")
print(f"Python files: {[f.name for f in layout.python_files]}")

# Index symbols
index = index_skill(layout)
for module in index.modules:
    print(f"\n{module.file_path}:")
    for sym in module.symbols:
        print(f"  {sym.kind} {sym.name}{sym.signature or ''}")
```

## Integration with mapping-codebases

This skill complements `mapping-codebases` which generates `_MAP.md` files:

- **mapping-codebases**: Static documentation via tree-sitter, multi-language
- **inspecting-skills**: Runtime import support, Python-focused, dynamic discovery

Use both together:
1. `mapping-codebases` for navigation and code review
2. `inspecting-skills` for actual code imports and execution

## Troubleshooting

### Import Errors

```python
# If skill_import fails, check:

# 1. Skill exists and has __init__.py
from inspecting_skills import discover_skill
layout = discover_skill(Path("/path/to/skill"))
print(layout.has_init)  # Must be True for importing

# 2. Skills root is configured
from inspecting_skills import get_skills_root
print(get_skills_root())

# 3. Symbol is exported in __all__
import ast
init_code = open("/path/to/skill/__init__.py").read()
# Check for __all__ definition
```

### Path Not Found

```python
# Manually set skills root
from inspecting_skills import set_skills_root
set_skills_root("/home/user/claude-skills")
```

## API Reference

### SkillLayout

```python
@dataclass
class SkillLayout:
    name: str              # "browsing-bluesky"
    path: Path             # Full path to skill directory
    layout_type: str       # "scripts" | "root" | "package" | "none"
    python_files: list[Path]
    has_init: bool         # Can be imported as package
    entry_module: str      # "browsing_bluesky"
```

### SkillIndex

```python
@dataclass
class SkillIndex:
    name: str              # "browsing-bluesky"
    module_name: str       # "browsing_bluesky"
    layout_type: str
    modules: list[ModuleIndex]
    exports: list[str]     # From __all__
```

### Symbol

```python
@dataclass
class Symbol:
    name: str              # Function/class name
    kind: str              # "function" | "class" | "method"
    signature: str | None  # "(self, x: int)"
    line: int | None       # 1-indexed
    docstring: str | None  # First line
    children: list[Symbol] # Methods for classes
```
