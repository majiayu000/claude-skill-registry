---
name: list-files
description: Display the list of files in the current directory with optional detailed
  information.
---

# List Files

## Description
Display the list of files in the current directory with optional detailed information.

## Usage
This skill lists all files and directories in a specified path (defaults to current directory). It can show basic file names or detailed information including file sizes and types.

## Input
- `--path`: Optional path to list files from (default: current directory)
- `--details`: Optional flag to show detailed information about files including size and type indicators

## Output
Lists files and directories in the specified path, showing:
- Basic mode: File and directory names (directories marked with `/`)
- Details mode: Files with 📄 icon and size, directories with 📁 icon

## Examples
```bash
# List files in current directory
python3 list-files.py

# List files in specific directory
python3 list-files.py --path /workspace

# List files with detailed information
python3 list-files.py --details

# List files in specific directory with details
python3 list-files.py --path /workspace --details
```
