---
name: bash-script-helper
description: Expert helper for bash scripting, debugging, and best practices
---

# Bash-script-helper

## Instructions

When writing or debugging bash scripts:
- Always use #!/bin/bash shebang
- Set -e (exit on error), -u (error on undefined var)
- Use [[ ]] instead of [ ] for tests
- Quote variables: "$variable" not $variable
- Use $() instead of backticks
- Check command exit codes: $?
- Use trap for cleanup
- Provide meaningful error messages
- Validate input parameters
- Argument parsing with getopts
- Reading files line by line
- Function definitions and calls
- Arrays and associative arrays
- Use set -x for trace mode
- shellcheck for static analysis
- Use echo/printf for debugging output
- Avoid eval
- Sanitize user input
- Use mktemp for temporary files
- Set proper file permissions


## Examples

Add examples of how to use this skill here.

## Notes

- This skill was auto-generated
- Edit this file to customize behavior
