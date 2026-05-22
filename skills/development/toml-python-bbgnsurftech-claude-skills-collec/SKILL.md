---
name: toml-python
description: When reading or writing pyproject.toml or .toml config files in Python. When editing TOML while preserving comments and formatting. When designing configuration file format for a Python tool. When code uses tomlkit or tomllib. When implementing atomic config file updates.
---

# TOML Python Integration

Work with TOML configuration files using the tomlkit library, which preserves comments and formatting during read-modify-write cycles.

## When to Use This Skill

Use this skill when:

- Reading or writing TOML configuration files (config.toml, pyproject.toml)
- Modifying existing TOML files while preserving comments and formatting
- Parsing TOML into Python data structures
- Creating TOML documents programmatically
- Handling TOML syntax errors and validation
- Implementing config file management for Python applications
- Working with XDG Base Directory specification for config locations

## Core Capabilities

### Library Selection: tomlkit vs tomllib

**Use tomlkit when:**

- Modifying existing config files (preserves comments and formatting)
- Building applications that write configuration
- Need single library for both reading and writing
- Python 3.8+ compatibility required

**Use tomllib (stdlib) when:**

- Python 3.11+ only
- Read-only access sufficient (no writing capability)
- Minimal dependencies preferred

**For config file management, tomlkit is the recommended choice.**

### Installation

```bash
# Using uv (recommended)
uv add tomlkit

# Using pip
pip install tomlkit
```

**Requirements:** Python >=3.8, tomlkit >=0.12.0

## tomlkit API Reference

### Reading TOML

```python
import tomlkit

# From string
doc = tomlkit.parse(toml_string)
doc = tomlkit.loads(toml_string)  # Alias for parse()

# From file object
with open('config.toml', 'r') as f:
    doc = tomlkit.load(f)

# Using TOMLFile class (convenient)
from tomlkit import TOMLFile

toml_file = TOMLFile('config.toml')
doc = toml_file.read()
```

**Returns:** `TOMLDocument` object (dict-like, preserves formatting)

### Writing TOML

```python
import tomlkit

# To string
toml_string = tomlkit.dumps(data)

# To file object
with open('config.toml', 'w') as f:
    tomlkit.dump(data, f)

# Using TOMLFile class
from tomlkit import TOMLFile

toml_file = TOMLFile('config.toml')
toml_file.write(doc)
```

### Creating TOML Documents

```python
from tomlkit import document, table, comment, nl, array, inline_table

# Create document
doc = document()
doc.add(comment("Configuration file"))
doc.add(nl())
doc.add("title", "My Config")

# Create table
db_config = table()
db_config["host"] = "localhost"
db_config["port"] = 5432
doc["database"] = db_config

# Create inline table
point = inline_table()
point.update({'x': 1, 'y': 2})
doc["point"] = point

# Create array
numbers = array()
numbers.extend([1, 2, 3])
doc["numbers"] = numbers
```

### Document Manipulation

```python
# Dict-like access
doc["section"]["key"] = "value"
value = doc["section"]["key"]

# Get with default
value = doc.get("key", "default")

# Check existence
if "key" in doc:
    pass

# Iterate
for key, value in doc.items():
    print(key, value)

# Remove key
doc.pop("key")
doc.remove("key")

# Convert to pure Python dict
pure_dict = doc.unwrap()

# Get as TOML string
toml_str = doc.as_string()
```

### Value Creation Helpers

```python
from tomlkit import (
    item,          # Auto-detect type
    string,        # String with options
    integer,       # Integer
    float_,        # Float
    boolean,       # Boolean
    datetime,      # Datetime
    date,          # Date
    time,          # Time
)

# Auto-detect type
doc["key"] = item(42)
doc["key"] = item([1, 2, 3])
doc["key"] = item({'nested': 'table'})

# Explicit string types
doc["basic"] = string("text")
doc["literal"] = string("text", literal=True)  # Single quotes
doc["multiline"] = string("line1\nline2", multiline=True)
```

## Error Handling

### Exception Types

```python
from tomlkit.exceptions import (
    TOMLKitError,           # Base exception
    ParseError,             # Syntax errors (has .line and .col)
    NonExistentKey,         # Missing key access
    KeyAlreadyPresent,      # Duplicate key
    ConvertError,           # Type conversion failure
)

# Handle parse errors
try:
    doc = tomlkit.parse(toml_string)
except ParseError as e:
    print(f"Parse error at line {e.line}, column {e.col}: {e}")

# Handle missing keys
try:
    value = doc["nonexistent"]
except (KeyError, NonExistentKey):
    value = "default"

# Handle file not found
try:
    with open('config.toml', 'r') as f:
        doc = tomlkit.load(f)
except FileNotFoundError:
    # Create default config
    doc = create_default_config()
```

## Common Patterns

### Pattern 1: Load or Create Config

```python
import tomlkit
from pathlib import Path

def load_or_create_config(path: Path) -> tomlkit.TOMLDocument:
    """Load existing config or create default if missing."""
    if path.exists():
        with open(path, 'r') as f:
            return tomlkit.load(f)

    # Create default
    doc = tomlkit.document()
    doc.add(tomlkit.comment("Default configuration"))
    doc.add(tomlkit.nl())

    doc["app"] = tomlkit.table()
    doc["app"]["name"] = "myapp"
    doc["app"]["version"] = "1.0.0"

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        tomlkit.dump(doc, f)

    return doc
```

### Pattern 2: Update Single Value (Preserving Comments)

```python
import tomlkit

def update_config_value(path: str, section: str, key: str, value):
    """Update single value while preserving all comments."""
    with open(path, 'r') as f:
        doc = tomlkit.load(f)

    if section not in doc:
        doc[section] = tomlkit.table()

    doc[section][key] = value

    with open(path, 'w') as f:
        tomlkit.dump(doc, f)

# Usage
update_config_value('config.toml', 'database', 'port', 5433)
```

### Pattern 3: Atomic Updates

```python
import tomlkit
from pathlib import Path
import tempfile
import shutil

def atomic_config_update(path: Path, updates: dict):
    """Update config atomically to prevent corruption."""
    with open(path, 'r') as f:
        doc = tomlkit.load(f)

    # Apply updates
    for section, values in updates.items():
        if section not in doc:
            doc[section] = tomlkit.table()
        for key, value in values.items():
            doc[section][key] = value

    # Write to temp file, then atomic move
    temp_fd, temp_path = tempfile.mkstemp(suffix='.toml')
    try:
        with open(temp_fd, 'w') as f:
            tomlkit.dump(doc, f)
        shutil.move(temp_path, path)
    except Exception:
        Path(temp_path).unlink(missing_ok=True)
        raise
```

### Pattern 4: Config Validation

```python
import tomlkit
from tomlkit.exceptions import ParseError

def validate_config(path: str) -> tuple[bool, str]:
    """Validate config structure. Returns (is_valid, error_message)."""
    try:
        with open(path, 'r') as f:
            doc = tomlkit.load(f)
    except FileNotFoundError:
        return False, "Config file not found"
    except ParseError as e:
        return False, f"Invalid TOML at line {e.line}, col {e.col}"

    required_sections = ['app', 'database']
    missing = [s for s in required_sections if s not in doc]

    if missing:
        return False, f"Missing sections: {', '.join(missing)}"

    if 'name' not in doc.get('app', {}):
        return False, "Missing required key: app.name"

    return True, ""
```

## XDG Base Directory Integration

For config file locations following XDG specification, activate the xdg-base-directory skill:

```
Skill(command: "xdg-base-directory")
```

**Standard config path pattern:**

```python
from pathlib import Path

def get_config_path(app_name: str) -> Path:
    """Get XDG-compliant config path."""
    config_dir = Path.home() / '.config' / app_name
    return config_dir / 'config.toml'

# Usage
config_path = get_config_path('myapp')
# Returns: ~/.config/myapp/config.toml
```

## TOML Syntax Quick Reference

### Basic Types

```toml
# Strings
string = "Hello, World!"
multiline = """
Multiple
lines
"""
literal = 'C:\path\no\escaping'

# Numbers
integer = 42
float = 3.14
scientific = 1e10

# Boolean
flag = true

# Date/Time
datetime = 2024-01-15T10:30:00Z
date = 2024-01-15
time = 10:30:00
```

### Tables and Arrays

```toml
# Standard table
[database]
host = "localhost"
port = 5432

# Nested table
[database.pool]
max_connections = 100

# Inline table
point = { x = 1, y = 2 }

# Array
numbers = [1, 2, 3]

# Array of tables
[[products]]
name = "Widget"
price = 9.99

[[products]]
name = "Gadget"
price = 19.99
```

## Type Mappings

| TOML Type        | Python Type         |
| ---------------- | ------------------- |
| String           | `str`               |
| Integer          | `int`               |
| Float            | `float`             |
| Boolean          | `bool`              |
| Offset Date-Time | `datetime.datetime` |
| Local Date-Time  | `datetime.datetime` |
| Local Date       | `datetime.date`     |
| Local Time       | `datetime.time`     |
| Array            | `list`              |
| Table            | `dict`              |

## Key Features of tomlkit

### Comment Preservation

```python
import tomlkit

original = """
# Configuration file
[database]
# Database host
host = "localhost"
# Database port
port = 5432
"""

doc = tomlkit.parse(original)
doc['database']['port'] = 5433

result = tomlkit.dumps(doc)
# Comments are preserved in result
```

**Reason:** User-added comments in config files should survive application updates.

### Format Preservation

tomlkit maintains:

- Original indentation
- Whitespace patterns
- Key ordering
- Comment placement
- Quote style preferences

**Reason:** Minimal diffs in version control when config changes.

### Table Creation Helpers

```python
from tomlkit import document, table

doc = document()

# Regular table
config = table()
config["key"] = "value"
doc["config"] = config

# Super table (parent of nested tables)
parent = table(is_super_table=True)
child = table()
child["x"] = 1
parent.append("child", child)
doc.append("parent", parent)

print(doc.as_string())
# [parent.child]
# x = 1
```

## Common Pitfalls

### Issue: Losing Comments

```python
# ❌ Wrong: Using unwrap() loses formatting
doc = tomlkit.load(f)
pure_dict = doc.unwrap()
# Modifications to pure_dict lose all comments

# ✓ Correct: Modify doc directly
doc = tomlkit.load(f)
doc["section"]["key"] = "value"
# Comments preserved
```

### Issue: Type Mismatches

```python
# ❌ Wrong: Assuming types
value = doc["port"]  # Might be string or int

# ✓ Correct: Validate types
port = doc["port"]
if not isinstance(port, int):
    raise ValueError(f"Expected int for port, got {type(port)}")
```

### Issue: Missing Keys

```python
# ❌ Wrong: Direct access without checking
value = doc["section"]["key"]  # KeyError if missing

# ✓ Correct: Use .get() with defaults
value = doc.get("section", {}).get("key", "default")
```

## Configuration File Example

```toml
# ~/.config/myapp/config.toml
# Application configuration

[app]
# Application name
name = "myapp"
# Application version
version = "1.0.0"
# Debug mode
debug = false

[database]
# Database connection settings
host = "localhost"
port = 5432
name = "myapp_db"
pool_size = 10

[logging]
# Logging configuration
level = "INFO"
file = "/var/log/myapp/app.log"
max_size_mb = 100

[features]
# Feature flags
enable_api = true
enable_web = true
enable_workers = false
```

## Dataclass Integration Pattern

```python
from dataclasses import dataclass
import tomlkit
from pathlib import Path

@dataclass
class AppConfig:
    name: str
    version: str
    debug: bool = False

@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    pool_size: int = 10

@dataclass
class Config:
    app: AppConfig
    database: DatabaseConfig

def load_config(path: Path) -> Config:
    """Load TOML config into dataclasses."""
    with open(path, 'r') as f:
        data = tomlkit.load(f)

    return Config(
        app=AppConfig(**data.get('app', {})),
        database=DatabaseConfig(**data.get('database', {})),
    )

def save_config(config: Config, path: Path):
    """Save dataclasses to TOML, preserving existing comments."""
    if path.exists():
        with open(path, 'r') as f:
            doc = tomlkit.load(f)
    else:
        doc = tomlkit.document()

    # Update from dataclasses
    if 'app' not in doc:
        doc['app'] = tomlkit.table()
    doc['app']['name'] = config.app.name
    doc['app']['version'] = config.app.version
    doc['app']['debug'] = config.app.debug

    if 'database' not in doc:
        doc['database'] = tomlkit.table()
    doc['database']['host'] = config.database.host
    doc['database']['port'] = config.database.port
    doc['database']['name'] = config.database.name
    doc['database']['pool_size'] = config.database.pool_size

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        tomlkit.dump(doc, f)
```

## References

### Official Documentation

- [tomlkit Documentation](https://tomlkit.readthedocs.io/) - Complete API reference
- [tomlkit PyPI](https://pypi.org/project/tomlkit/) - Package information
- [tomlkit GitHub](https://github.com/sdispater/tomlkit) - Source code
- [TOML Specification](https://toml.io/en/) - TOML v1.0.0 specification
- [Python tomllib](https://docs.python.org/3.11/library/tomllib.html) - Stdlib alternative (read-only)

### Related Skills

- `xdg-base-directory` - For XDG-compliant config file locations
- `python3-development` - For Python development patterns
- `uv` - For dependency management

### Tools

- `tomlkit` - Comment-preserving TOML library (read/write)
- `tomllib` - Stdlib TOML parser (read-only, Python 3.11+)
- `tomli_w` - Stdlib-compatible TOML writer
