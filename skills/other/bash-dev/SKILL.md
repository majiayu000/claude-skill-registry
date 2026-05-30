---
name: bash-dev
description: Bash scripting development standards, error handling, and best practices. Activated when working with .sh files or Bash scripts.
allowed-tools: ['Read', 'Grep', 'Bash']
---

# Bash Development Expert

This skill supports Bash script development with best practices and safety standards.

## 🎯 Core Rules

### Shebang and Safety
- **Shebang**: Always use `#!/usr/bin/env bash`
- **Set Options**: Always use `set -euo pipefail`
  - `-e`: Exit on error
  - `-u`: Exit on undefined variable
  - `-o pipefail`: Fail pipeline if any command fails

### Variable Handling
- **Quoting**: Always quote variables `"${var}"`
- **Constants**: Use UPPERCASE for global/environment variables
- **Local Variables**: Use lowercase for function-local variables
- **Readonly**: Use `readonly` for constants

### Function Best Practices
- **Local Variables**: Always use `local` keyword
- **Parameter Validation**: Validate required parameters
- **Return Codes**: 0 for success, non-zero for errors
- **Documentation**: Document usage, description, and return codes

## 📚 Script Template

### Standard Script Structure
```bash
#!/usr/bin/env bash
set -euo pipefail

# Script metadata
# Usage: script_name.sh <arg1> [arg2]
# Description: What this script does
# Author: Your Name
# Version: 1.0.0

# Global constants (UPPERCASE)
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly VERSION="1.0.0"

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

#######################################
# Display usage information
# Globals:
#   SCRIPT_NAME
# Arguments:
#   None
# Outputs:
#   Writes usage to stdout
#######################################
usage() {
  cat <<EOF
Usage: ${SCRIPT_NAME} <arg1> [arg2]

Description:
  What this script does in detail

Arguments:
  arg1    Required argument description
  arg2    Optional argument description (default: value)

Options:
  -h, --help    Show this help message
  -v, --version Show version information

Examples:
  ${SCRIPT_NAME} value1
  ${SCRIPT_NAME} value1 value2
EOF
}

#######################################
# Print error message and exit
# Globals:
#   RED, NC
# Arguments:
#   Error message
# Outputs:
#   Writes error to stderr
# Returns:
#   1 (error code)
#######################################
error() {
  echo -e "${RED}Error: $*${NC}" >&2
  exit 1
}

#######################################
# Print info message
# Globals:
#   GREEN, NC
# Arguments:
#   Info message
# Outputs:
#   Writes message to stdout
#######################################
info() {
  echo -e "${GREEN}Info: $*${NC}"
}

#######################################
# Print warning message
# Globals:
#   YELLOW, NC
# Arguments:
#   Warning message
# Outputs:
#   Writes warning to stdout
#######################################
warn() {
  echo -e "${YELLOW}Warning: $*${NC}"
}

#######################################
# Main function
# Globals:
#   None
# Arguments:
#   Command line arguments
# Returns:
#   0 on success, 1 on error
#######################################
main() {
  local arg1="${1:?Error: arg1 required}"
  local arg2="${2:-default_value}"

  info "Processing: ${arg1}"

  # Your logic here

  info "Completed successfully"
  return 0
}

# Error handler
trap 'error "Script failed on line $LINENO"' ERR

# Parse arguments
case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
  -v|--version)
    echo "${SCRIPT_NAME} version ${VERSION}"
    exit 0
    ;;
esac

# Execute main function
main "$@"
```

## 🛠️ Common Patterns

### Error Handling
```bash
# Check if command exists
if ! command -v git &> /dev/null; then
  error "git is not installed"
fi

# Check if file exists
if [[ ! -f "${config_file}" ]]; then
  error "Config file not found: ${config_file}"
fi

# Check if directory exists
if [[ ! -d "${target_dir}" ]]; then
  mkdir -p "${target_dir}" || error "Failed to create directory"
fi
```

### Input Validation
```bash
# Validate required argument
validate_arg() {
  local arg="${1:?Error: argument required}"
  if [[ -z "${arg}" ]]; then
    error "Argument cannot be empty"
  fi
}

# Validate number
validate_number() {
  local num="$1"
  if ! [[ "${num}" =~ ^[0-9]+$ ]]; then
    error "Invalid number: ${num}"
  fi
}
```

### File Operations
```bash
# Safe file read
read_file() {
  local file="$1"
  if [[ ! -r "${file}" ]]; then
    error "Cannot read file: ${file}"
  fi
  cat "${file}"
}

# Safe file write
write_file() {
  local file="$1"
  local content="$2"
  echo "${content}" > "${file}" || error "Failed to write file"
}
```

### Array Handling
```bash
# Declare array
declare -a items=("item1" "item2" "item3")

# Iterate over array
for item in "${items[@]}"; do
  echo "Processing: ${item}"
done

# Array length
echo "Total items: ${#items[@]}"
```

## 🎯 Quality Checklist

Check these before committing:

- [ ] Shebang `#!/usr/bin/env bash` present
- [ ] `set -euo pipefail` at the beginning
- [ ] All variables quoted `"${var}"`
- [ ] Global variables in UPPERCASE
- [ ] Local variables use `local` keyword
- [ ] Functions have documentation comments
- [ ] Error handling implemented
- [ ] Usage function provided
- [ ] Exit codes are meaningful (0=success, non-zero=error)
- [ ] Script tested with `shellcheck`

## 🔍 Common Anti-patterns to Avoid

❌ **Don't**:
```bash
# Unquoted variables
cd $HOME/dir

# Missing error handling
mkdir /some/dir

# Undefined variables
echo $UNDEFINED_VAR

# No set options
#!/bin/bash
```

✅ **Do**:
```bash
# Quoted variables
cd "${HOME}/dir" || error "Failed to change directory"

# With error handling
mkdir -p "${target_dir}" || error "Failed to create directory"

# Check before use
if [[ -n "${VAR:-}" ]]; then
  echo "${VAR}"
fi

# Proper set options
#!/usr/bin/env bash
set -euo pipefail
```

## 💡 Testing

### Using ShellCheck
```bash
# Install shellcheck
brew install shellcheck  # macOS

# Check script
shellcheck script.sh

# Ignore specific warnings
# shellcheck disable=SC2086
command ${unquoted}
```

### Testing Functions
```bash
# Simple test function
test_function() {
  local expected="expected_value"
  local actual
  actual="$(your_function)"

  if [[ "${actual}" != "${expected}" ]]; then
    error "Test failed: expected '${expected}', got '${actual}'"
  fi
  info "Test passed"
}
```
