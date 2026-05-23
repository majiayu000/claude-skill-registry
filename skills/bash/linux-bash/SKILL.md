---
name: Linux Bash
description: Expert assistance with Linux bash commands, shell scripting, system administration, file operations, and command-line utilities. Use this when working with bash scripts, Linux system operations, or command-line tasks.
---

# Linux Bash

Expert guidance for Linux bash operations, scripting, and system administration.

## Core Commands

### File Operations
- `ls -lah` - List files with details, including hidden
- `find /path -name "pattern"` - Find files by name
- `grep -r "pattern" /path` - Recursive text search
- `chmod +x file` - Make file executable
- `chown user:group file` - Change ownership
- `tar -czf archive.tar.gz dir/` - Create compressed archive
- `tar -xzf archive.tar.gz` - Extract archive

### Process Management
- `ps aux | grep process` - Find running processes
- `top` / `htop` - Monitor system resources
- `kill -9 PID` - Force kill process
- `nohup command &` - Run command in background
- `jobs` - List background jobs
- `fg %1` - Bring job to foreground

### System Information
- `df -h` - Disk usage human-readable
- `du -sh dir/` - Directory size
- `free -h` - Memory usage
- `uname -a` - System information
- `lsb_release -a` - Distribution info

### Text Processing
- `cat file | head -n 10` - First 10 lines
- `tail -f log.txt` - Follow log file
- `sed 's/old/new/g' file` - Replace text
- `awk '{print $1}' file` - Print first column
- `sort file | uniq` - Remove duplicates

## Shell Scripting Best Practices

### Script Template
```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Script description
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

main() {
    # Your logic here
    echo "Hello, World!"
}

main "$@"
```

### Error Handling
```bash
# Check command success
if ! command -v tool &> /dev/null; then
    echo "Error: tool not found" >&2
    exit 1
fi

# Trap errors
trap 'echo "Error on line $LINENO"' ERR
```

### Variables
```bash
# Constants (uppercase)
readonly CONFIG_FILE="/etc/app.conf"

# Variables (lowercase)
user_input="$1"

# Arrays
files=("file1.txt" "file2.txt")
for file in "${files[@]}"; do
    echo "$file"
done
```

## Common Patterns

### Check if file exists
```bash
if [[ -f "file.txt" ]]; then
    echo "File exists"
fi
```

### Loop through files
```bash
for file in *.txt; do
    echo "Processing $file"
done
```

### Read user input
```bash
read -p "Enter value: " user_value
```

### Function definition
```bash
my_function() {
    local arg1="$1"
    echo "Received: $arg1"
}
```

## Tips

1. **Quote variables**: Always use `"$variable"` to prevent word splitting
2. **Use [[ ]] for tests**: More features than [ ]
3. **Shellcheck**: Use `shellcheck script.sh` to validate scripts
4. **Exit codes**: Use `$?` to check last command status
5. **Debugging**: Use `set -x` to trace execution

## Safety First

- Always test scripts in safe environment first
- Use `set -e` to exit on errors
- Validate input parameters
- Quote file paths to handle spaces
- Use absolute paths when possible
