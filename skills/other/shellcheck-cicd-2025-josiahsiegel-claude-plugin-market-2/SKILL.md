---
name: shellcheck-cicd-2025
description: ShellCheck validation as non-negotiable 2025 workflow practice
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# ShellCheck CI/CD Integration (2025)

## ShellCheck: Non-Negotiable in 2025

ShellCheck is now considered **mandatory** in modern bash workflows (2025 best practices):

### Latest Version: v0.11.0 (August 2025)

**What's New:**
- Full Bash 5.3 support (`${| cmd; }` and `source -p`)
- **New warnings**: SC2327/SC2328 (capture group issues)
- **POSIX.1-2024 compliance**: SC3013 removed (-ot/-nt/-ef now POSIX standard)
- Enhanced static analysis capabilities
- Improved performance and accuracy

### Why Mandatory?

- Catches subtle bugs before production
- Prevents common security vulnerabilities
- Enforces consistent code quality
- Required by most DevOps teams
- Standard in enterprise environments
- Supports latest POSIX.1-2024 standard

## Installation

```bash
# Ubuntu/Debian
apt-get install shellcheck

# macOS
brew install shellcheck

# Alpine (Docker)
apk add shellcheck

# Windows (WSL/Git Bash)
choco install shellcheck

# Or download binary
wget https://github.com/koalaman/shellcheck/releases/latest/download/shellcheck-stable.linux.x86_64.tar.xz
tar -xf shellcheck-stable.linux.x86_64.tar.xz
sudo cp shellcheck-stable/shellcheck /usr/local/bin/
```

## GitHub Actions Integration

### Mandatory Pre-Merge Check

```yaml
# .github/workflows/shellcheck.yml
name: ShellCheck

on:
  pull_request:
    paths:
      - '**.sh'
      - '**Dockerfile'
  push:
    branches: [main]

jobs:
  shellcheck:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Run ShellCheck
      uses: ludeeus/action-shellcheck@master
      with:
        severity: warning
        format: gcc  # or: tty, json, checkstyle
        scandir: './scripts'
        # Fail on any issues
        ignore_paths: 'node_modules'

    # Block merge on failures
    - name: Annotate PR
      if: failure()
      uses: actions/github-script@v6
      with:
        script: |
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '⛔ ShellCheck validation failed. Fix issues before merging.'
          })
```

## Azure DevOps Integration

```yaml
# azure-pipelines.yml
trigger:
- main

pr:
- main

stages:
- stage: Validate
  jobs:
  - job: ShellCheck
    pool:
      vmImage: 'ubuntu-24.04'

    steps:
    - script: |
        sudo apt-get install -y shellcheck
      displayName: 'Install ShellCheck'

    - script: |
        find . -name "*.sh" -type f | xargs shellcheck --format=gcc --severity=warning
      displayName: 'Run ShellCheck'
      failOnStderr: true

    - task: PublishTestResults@2
      condition: always()
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: '**/shellcheck-results.xml'
        failTaskOnFailedTests: true
```

## Git Hooks (Pre-Commit)

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

# Find all staged .sh files
mapfile -t STAGED_SH < <(git diff --cached --name-only --diff-filter=ACMR | grep '\.sh$' || true)

if [ ${#STAGED_SH[@]} -eq 0 ]; then
  exit 0
fi

echo "Running ShellCheck on staged files..."

# Run ShellCheck
shellcheck --format=gcc --severity=warning "${STAGED_SH[@]}"

if [ $? -ne 0 ]; then
  echo "⛔ ShellCheck failed. Fix issues before committing."
  exit 1
fi

echo "✅ ShellCheck passed"
exit 0
```

**Install Pre-Commit Hook:**
```bash
chmod +x .git/hooks/pre-commit

# Or use pre-commit framework
# .pre-commit-config.yaml
repos:
- repo: https://github.com/shellcheck-py/shellcheck-py
  rev: v0.11.0.0
  hooks:
  - id: shellcheck
    args: ['--severity=warning']

# Install
pip install pre-commit
pre-commit install
```

## VS Code Integration

```json
// .vscode/settings.json
{
  "shellcheck.enable": true,
  "shellcheck.run": "onType",
  "shellcheck.executablePath": "/usr/local/bin/shellcheck",
  "shellcheck.exclude": ["SC1090", "SC1091"],  // Optional excludes
  "shellcheck.customArgs": [
    "-x",  // Follow source files
    "--severity=warning"
  ]
}
```

## Docker Build Integration

```dockerfile
# Dockerfile with ShellCheck validation
FROM alpine:3.19 AS builder

# Install ShellCheck
RUN apk add --no-cache shellcheck bash

# Copy scripts
COPY scripts/ /scripts/

# Validate all scripts before continuing
RUN find /scripts -name "*.sh" -type f -exec shellcheck --severity=warning {} +

# Final stage
FROM alpine:3.19
COPY --from=builder /scripts/ /scripts/
RUN chmod +x /scripts/*.sh

ENTRYPOINT ["/scripts/entrypoint.sh"]
```

## Common ShellCheck Rules (2025)

### New in v0.11.0: SC2327/SC2328 - Capture Groups

```bash
# ❌ Bad - Capture groups may not work as expected
if [[ "$string" =~ ([0-9]+)\.([0-9]+) ]]; then
  echo "$1"  # Wrong: $1 is script arg, not capture group
fi

# ✅ Good - Use BASH_REMATCH array
if [[ "$string" =~ ([0-9]+)\.([0-9]+) ]]; then
  echo "${BASH_REMATCH[1]}.${BASH_REMATCH[2]}"
fi
```

### SC2294: eval Negates Array Benefits (New)

```bash
# ❌ Bad - eval defeats array safety
eval "command ${array[@]}"

# ✅ Good - Direct array usage
command "${array[@]}"
```

### SC2295: Quote Expansions Inside ${}

```bash
# ❌ Bad
echo "${var-$default}"  # $default not quoted

# ✅ Good
echo "${var-"$default"}"
```

### SC2086: Quote Variables

```bash
# ❌ Bad
file=$1
cat $file  # Fails if filename has spaces

# ✅ Good
file=$1
cat "$file"
```

### SC2046: Quote Command Substitution

```bash
# ❌ Bad
for file in $(find . -name "*.txt"); do
  echo $file
done

# ✅ Good
find . -name "*.txt" -print0 | while IFS= read -r -d '' file; do
  echo "$file"
done
```

### SC2155: Separate Declaration and Assignment

```bash
# ❌ Bad
local result=$(command)  # Hides command exit code

# ✅ Good
local result
result=$(command)
```

### SC2164: Use cd || exit

```bash
# ❌ Bad
cd /some/directory
./script.sh  # Runs in wrong dir if cd fails

# ✅ Good
cd /some/directory || exit 1
./script.sh
```

## Google Shell Style Guide (50-Line Limit)

2025 recommendation: Keep scripts under 50 lines:

```bash
# ❌ Bad: 500-line monolithic script
#!/usr/bin/env bash
# ... 500 lines of code ...

# ✅ Good: Modular scripts < 50 lines each

# lib/logging.sh (20 lines)
log_info() { echo "[INFO] $*"; }
log_error() { echo "[ERROR] $*" >&2; }

# lib/validation.sh (30 lines)
validate_input() { ... }
check_dependencies() { ... }

# main.sh (40 lines)
source "$(dirname "$0")/lib/logging.sh"
source "$(dirname "$0")/lib/validation.sh"

main() {
  validate_input "$@"
  check_dependencies
  # ... core logic ...
}

main "$@"
```

## Enforce in CI/CD

### Fail Build on Issues

```yaml
# Strict enforcement
- name: ShellCheck (Strict)
  run: |
    shellcheck --severity=warning scripts/*.sh
  # Exit code 1 fails the build

# Advisory only (warnings but don't fail)
- name: ShellCheck (Advisory)
  run: |
    shellcheck --severity=warning scripts/*.sh || true
  # Logs warnings but doesn't fail
```

### Generate Reports

```bash
# JSON format for parsing
shellcheck --format=json scripts/*.sh > shellcheck-report.json

# GitHub annotations format
shellcheck --format=gcc scripts/*.sh

# Human-readable
shellcheck --format=tty scripts/*.sh
```

## Modern Error Handling Trio (2025)

Always use with ShellCheck validation:

```bash
#!/usr/bin/env bash

# Modern error handling (non-negotiable in 2025)
set -o errexit   # Exit on command failure
set -o nounset   # Exit on undefined variable
set -o pipefail  # Exit on pipe failure

# ShellCheck approved
main() {
  local config_file="${1:?Config file required}"

  if [[ ! -f "$config_file" ]]; then
    echo "Error: Config file not found: $config_file" >&2
    return 1
  fi

  # Safe command execution
  local result
  result=$(process_config "$config_file")

  echo "$result"
}

main "$@"
```

## Best Practices (2025)

1. **Run ShellCheck in CI/CD (mandatory)**
2. **Use pre-commit hooks** to catch issues early
3. **Keep scripts under 50 lines** (Google Style Guide)
4. **Use modern error handling trio** (errexit, nounset, pipefail)
5. **Fix all warnings** before merging
6. **Document any disabled rules** with reasoning
7. **Integrate with IDE** for real-time feedback

## Resources

- [ShellCheck](https://www.shellcheck.net)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck GitHub Action](https://github.com/ludeeus/action-shellcheck)
