---
name: bash-lint
description: 'This skill should be used when the user asks to "lint bash script", "run shellcheck", "format shell script", "use shfmt", "fix shellcheck errors", or mentions shell script linting, formatting, code quality, or pre-commit hooks for bash.'
---

# Bash Linting

Shellcheck and shfmt integration for bash script quality assurance.

## Shellcheck

### Installation

```bash
# Debian/Ubuntu
apt install shellcheck

# macOS
brew install shellcheck

# From source
cabal update && cabal install ShellCheck
```

### Basic Usage

```bash
# Check single file
shellcheck script.sh

# Check multiple files
shellcheck *.sh

# With specific shell dialect
shellcheck --shell=bash script.sh
shellcheck --shell=sh script.sh

# Exclude specific rules
shellcheck --exclude=SC2086 script.sh
shellcheck --exclude=SC2086,SC2046 script.sh

# Output formats
shellcheck --format=gcc script.sh    # GCC-style
shellcheck --format=json script.sh   # JSON for tooling
shellcheck --format=diff script.sh   # Unified diff
```

### Common Shellcheck Codes

| Code   | Issue                                      | Fix                            |
| ------ | ------------------------------------------ | ------------------------------ |
| SC2086 | Double quote to prevent globbing/splitting | `"$var"`                       |
| SC2046 | Quote command substitution                 | `"$(cmd)"`                     |
| SC2006 | Use `$()` instead of backticks             | `$(cmd)`                       |
| SC2034 | Variable appears unused                    | Remove or export               |
| SC2155 | Declare and assign separately              | Split `local var; var=$(...)`  |
| SC2164 | Use `cd ... \|\| exit`                     | Handle cd failure              |
| SC2181 | Check exit status directly                 | `if cmd; then`                 |
| SC2129 | Consider grouping writes                   | Use `{ } > file`               |
| SC1090 | Can't follow sourced file                  | Use `# shellcheck source=path` |
| SC2154 | Variable referenced but not assigned       | Initialize or declare          |

### Shellcheck Directives

```bash
# Disable for next line
# shellcheck disable=SC2086
echo $unquoted_var

# Disable for entire file (at top)
# shellcheck disable=SC2086,SC2046

# Specify source file for sourcing
# shellcheck source=./lib/functions.sh
source "$SCRIPT_DIR/lib/functions.sh"

# Specify shell dialect
# shellcheck shell=bash

# Disable for block (not supported - use per-line)
```

### Inline Directive Patterns

```bash
# Disable specific warning with explanation
# shellcheck disable=SC2034 # Variable used by sourcing script
readonly CONFIG_VERSION="1.0"

# Disable multiple codes
# shellcheck disable=SC2086,SC2046
result=$(echo $var)

# Source directive for dynamic paths
# shellcheck source=/dev/null
source "${DYNAMIC_PATH}/config.sh"
```

## shfmt

### Installation

```bash
# macOS
brew install shfmt

# Go install
go install mvdan.cc/sh/v3/cmd/shfmt@latest

# Snap
snap install shfmt

# Binary download
# From https://github.com/mvdan/sh/releases
```

### Basic Usage

```bash
# Format and print to stdout
shfmt script.sh

# Format in place
shfmt -w script.sh

# Check formatting (exit 1 if unformatted)
shfmt -d script.sh

# Recursive directory
shfmt -w .
shfmt -w scripts/
```

### Formatting Options

```bash
# Indentation
shfmt -i 2 script.sh  # 2-space indent
shfmt -i 4 script.sh  # 4-space indent
shfmt -i 0 script.sh  # tabs (default)

# Binary operators at start of line
shfmt -bn script.sh

# Switch cases indented
shfmt -ci script.sh

# Redirect operators followed by space
shfmt -sr script.sh

# Keep column alignment paddings
shfmt -kp script.sh

# Function opening brace on separate line
shfmt -fn script.sh

# Combined
shfmt -i 4 -ci -bn script.sh
```

### Configuration (.editorconfig)

```ini
# .editorconfig
[*.sh]
indent_style = space
indent_size = 4
shell_variant = bash
binary_next_line = true
switch_case_indent = true
space_redirects = true
```

### Example Transformations

**Before shfmt:**

```bash
if [ -f "$file" ];then
echo "exists"
fi

for i in 1 2 3;do
    process $i
done
```

**After shfmt -i 4 -ci:**

```bash
if [ -f "$file" ]; then
    echo "exists"
fi

for i in 1 2 3; do
    process $i
done
```

## Pre-commit Integration

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/koalaman/shellcheck-precommit
    rev: v0.9.0
    hooks:
      - id: shellcheck
        args: ["--severity=warning"]

  - repo: https://github.com/scop/pre-commit-shfmt
    rev: v3.7.0-1
    hooks:
      - id: shfmt
        args: ["-i", "4", "-ci", "-w"]

  # Alternative: local hooks
  - repo: local
    hooks:
      - id: shellcheck
        name: shellcheck
        entry: shellcheck
        language: system
        types: [shell]
        args: ["--severity=warning", "-x"]

      - id: shfmt
        name: shfmt
        entry: shfmt
        language: system
        types: [shell]
        args: ["-i", "4", "-ci", "-w"]
```

### Running Pre-commit

```bash
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run shellcheck --all-files
pre-commit run shfmt --all-files

# Run on specific files
pre-commit run --files script.sh
```

## Integration with CI/CD

### GitHub Actions

```yaml
name: Shell Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run ShellCheck
        uses: ludeeus/action-shellcheck@master
        with:
          severity: warning

      - name: Check formatting with shfmt
        uses: mvdan/github-action-shfmt@master
        with:
          flags: -d -i 4 -ci
```

### GitLab CI

```yaml
shellcheck:
  image: koalaman/shellcheck-alpine:stable
  script:
    - find . -name "*.sh" -exec shellcheck {} +

shfmt:
  image: mvdan/shfmt:latest
  script:
    - shfmt -d -i 4 -ci .
```

## Fixing Common Issues

### SC2086: Quote to prevent splitting

```bash
# Bad
echo $var

# Good
echo "$var"
printf '%s\n' "$var"
```

### SC2155: Declare and assign separately

```bash
# Bad - masks exit status
local var=$(some_command)

# Good
local var
var=$(some_command)
```

### SC2164: Use cd || exit

```bash
# Bad
cd "$dir"
rm -rf *

# Good
cd "$dir" || exit 1
rm -rf *

# Or with subshell
(cd "$dir" && rm -rf *)
```

### SC2181: Check exit directly

```bash
# Bad
command
if [ $? -eq 0 ]; then

# Good
if command; then
```

### SC1090/SC1091: Source issues

```bash
# Add directive for dynamic source
# shellcheck source=/dev/null
source "$DYNAMIC_PATH/lib.sh"

# Or specify actual path
# shellcheck source=./lib/functions.sh
source "$SCRIPT_DIR/lib/functions.sh"
```

## Editor Integration

### VS Code

Install "ShellCheck" extension by Timon Wong.

```json
// settings.json
{
    "shellcheck.enable": true,
    "shellcheck.run": "onSave",
    "shellcheck.executablePath": "shellcheck",
    "editor.formatOnSave": true,
    "[shellscript]": {
        "editor.defaultFormatter": "foxundermoon.shell-format"
    }
}
```

### Vim/Neovim

```vim
" With ALE
let g:ale_linters = {'sh': ['shellcheck']}
let g:ale_fixers = {'sh': ['shfmt']}
let g:ale_sh_shfmt_options = '-i 4 -ci'

" With coc.nvim
" Install coc-sh extension
```

## Best Practices

1. **Run shellcheck early** - integrate into editor and CI
2. **Fix issues, don't suppress** - only disable with good reason
3. **Document suppressions** - explain why rule is disabled
4. **Use severity levels** - `--severity=warning` for CI
5. **Consistent formatting** - use shfmt in pre-commit
6. **Version lock tools** - pin versions in CI/pre-commit
