---
name: pathlib
description: Object-oriented filesystem paths
version: 3.11
ecosystem: python
license: PSF
---

## Imports

```python
from pathlib import Path
import os
```

## Core Patterns

### Basic Path Creation

Create and manipulate filesystem paths.

```python
from pathlib import Path

# Create a path
p = Path('/tmp/example.txt')

# Check if it exists
if p.exists():
    print(f"File exists: {p}")

# Get parts
print(f"Name: {p.name}")
print(f"Parent: {p.parent}")
```

### Reading Files

Read file contents using Path.

```python
from pathlib import Path

p = Path('/tmp/example.txt')

# Write
p.write_text('Hello World!')

# Read
content = p.read_text()
print(f"Content: {content}")
```

### Directory Iteration

Iterate over files in a directory.

```python
from pathlib import Path

# List all Python files
for file in Path('.').glob('*.py'):
    print(f"Found: {file.name}")
```

## Configuration

Path objects are immutable and work consistently across platforms.

## Pitfalls

**Wrong**: Using string concatenation for paths
```python
path = '/tmp' + '/' + 'file.txt'  # Platform-specific
```

**Right**: Use Path division operator
```python
from pathlib import Path
path = Path('/tmp') / 'file.txt'  # Cross-platform
```

## References

- Official Documentation: https://docs.python.org/3/library/pathlib.html
