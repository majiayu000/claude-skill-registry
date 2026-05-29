---
name: tree-view
description: Display directory tree structure with customizable depth, using fd and Python3 for fast and beautiful tree visualization.
---

# Tree View

Fast directory tree visualization using fd + Python3.

## When to Use

- Need a quick overview of directory structure
- Want to see files organized hierarchically
- Default `tree` command is not available or too slow
- Need customizable depth limits

## Usage

```bash
# Show directory tree (default 2 levels)
bun ~/.pi/agent/skills/tree-view/cli.ts

# Show 3 levels deep
DEPTH=3 bun ~/.pi/agent/skills/tree-view/cli.ts

# Show 4 levels deep
DEPTH=4 bun ~/.pi/agent/skills/tree-view/cli.ts
```

## Features

- **Fast**: Uses `fd` for efficient file discovery
- **Depth control**: Environment variable `DEPTH` controls levels
- **Clean output**: Proper tree structure with branch characters
- **Smart truncation**: Long filenames are truncated for readability

## Requirements

- `bun` - Bun runtime
- `fd` - Fast alternative to `find`
- `python3` - For tree formatting

## Output Format

```
docs/
├── adr/
│   └── 20240210-decision.md
├── issues/
│   ├── frontend/
│   │   └── 20240210-task.md
│   └── backend/
└── guides/
```

## Notes

- Directories are shown with trailing `/`
- Files are shown without trailing slash
- Names longer than 30 characters are truncated (`prefix...suffix`)