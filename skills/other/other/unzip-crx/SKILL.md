---
name: unzip-crx
description: Extract Chrome extension (.crx) files. Use when user needs to unzip, extract, or decompress a .crx file. Handles Chrome's special crx headers that standard unzip tools cannot process.
---

# Unzip CRX

Extract Chrome extension (.crx) files to a specified directory.

## Usage

Run the script with the crx file path:

```bash
node ~/.claude/skills/unzip-crx/scripts/unzip-crx.mjs <crx-file-path> [destination]
```

**Parameters:**
- `crx-file-path`: Path to the .crx file (required)
- `destination`: Output directory (optional, defaults to a folder named after the crx file in the same directory)

## Examples

Extract to default location (creates folder next to crx file):
```bash
node ~/.claude/skills/unzip-crx/scripts/unzip-crx.mjs /path/to/extension.crx
# Output: /path/to/extension/
```

Extract to specific directory:
```bash
node ~/.claude/skills/unzip-crx/scripts/unzip-crx.mjs /path/to/extension.crx /output/dir
```

## Notes

- The script auto-installs `@tomjs/unzip-crx` npm package on first run
- Requires Node.js installed on the system
