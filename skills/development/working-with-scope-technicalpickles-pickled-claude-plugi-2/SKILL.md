---
name: scope
description: Guide for working with Scope, a developer environment management tool that automates environment checks, detects known errors, and provides automated fixes. Use when creating Scope configurations (ScopeKnownError, ScopeDoctorGroup, ScopeReportLocation), debugging environment issues, or writing rules for error detection and remediation.
---

# Scope - Developer Environment Management

Scope is a DevEx tool that helps maintain consistent development environments through automated checks, error detection, and fixes.

## Core Commands

### scope doctor

Run automated environment checks and fixes.

```bash
scope doctor run                   # Run all checks
scope doctor run --only group-name # Run specific group
scope doctor run --fix=false       # Check only, no fixes
scope doctor run --no-cache        # Disable caching
scope doctor list                  # List available checks
```

### scope analyze

Detect known errors in logs or command output.

```bash
scope analyze logs file.log                # Analyze log file
scope analyze command -- cmd args          # Analyze command output
scope analyze --extra-config path file.log # Use additional configs
```

### scope report

Generate bug reports with automatic secret redaction.

```bash
scope report ./script.sh     # Run and report on script
scope report -- command args # Run and report on command
```

### scope-intercept

Monitor script execution in real-time (used as shebang).

```bash
#!/usr/bin/env scope-intercept bash
# Script content here
```

## Configuration Resources

All Scope configurations use Kubernetes-inspired YAML format:

```yaml
apiVersion: scope.github.com/v1alpha
kind: <ResourceType>
metadata:
  name: unique-identifier
  description: Human-readable description
spec:
  # Resource-specific configuration
```

## ScopeKnownError

Define error patterns and provide automated help/fixes for common issues.

### Structure

```yaml
apiVersion: scope.github.com/v1alpha
kind: ScopeKnownError
metadata:
  name: descriptive-error-name
  description: Brief description of what this error means
spec:
  pattern: 'regex pattern to match the error'
  help: |
    Clear explanation of the issue.

    Steps to resolve:
    1. First step
    2. Second step
    3. Where to get help if needed
  fix:
    prompt:
      text: User-friendly prompt asking permission
    commands:
      - first-fix-command
      - second-fix-command
```

### Key Fields

- **pattern**: Regex pattern using ripgrep syntax to match error text
- **help**: Multi-line markdown explanation with resolution steps
- **fix** (optional): Automated remediation configuration
  - **commands**: List of commands to run to fix the error (required)
  - **helpText**: Descriptive text shown if the fix fails (optional)
  - **helpUrl**: Documentation link for manual resolution (optional)
  - **prompt**: User approval before running fix (optional)
    - **text**: Question asking for user permission
    - **extraContext**: Additional context about what the fix does and why approval is needed

**Note:** When a fix is defined, it only runs when the error pattern is detected. The fix is optional - if not provided, only the help text is shown.

### File Organization

Place files in categorized directories:

- Location: `{config-root}/known-errors/{category}/{error-name}.yaml`
- Common categories: `docker/`, `ruby/`, `git/`, `github/`, `mysql/`, `postgres/`, `dns/`, `aws/`
- Include matching `.txt` file with example error for testing

### Example

```yaml
apiVersion: scope.github.com/v1alpha
kind: ScopeKnownError
metadata:
  name: gem-missing-file
  description: A gem source file is missing and fails to be loaded
spec:
  pattern: "/lib/ruby/.* `require': cannot load such file --.*/lib/ruby/gems/.*(LoadError)"
  help: |
    A gem source file is missing. The solution is to reinstall the gems:
    1. Run `bundle pristine`
  fix:
    commands:
      - bundle pristine
    helpText: |
      Bundle pristine failed. Try these steps:
      1. Check your bundle config: bundle config list
      2. Reinstall bundler: gem install bundler
      3. Contact #help-ruby if issues persist
    helpUrl: https://bundler.io/man/bundle-pristine.1.html
    prompt:
      text: |-
        This will reinstall all gems from your Gemfile.
        Do you wish to continue?
      extraContext: >-
        bundle pristine reinstalls gems without changing versions,
        which resolves missing file errors but preserves your lock file
```

### Validation

Validate schema structure:

```bash
brew install sourcemeta/apps/jsonschema
jsonschema validate schema.json known-error.yaml
```

Test pattern matching:

```bash
scope analyze logs --extra-config config-dir/ test-error.txt
```

### Additional Resources

- [Complete example with fix and prompt](https://github.com/oscope-dev/scope/blob/main/examples/.scope/known-error-with-fix.yaml)
- [ScopeKnownError model documentation](https://oscope-dev.github.io/scope/docs/models/ScopeKnownError)

### Pattern Writing Tips

- Use ripgrep regex syntax (similar to PCRE)
- Escape special characters: `\\.`, `\\[`, `\\(`
- Use character classes: `[[:digit:]]`, `[[:alpha:]]`
- Test patterns: `echo "error text" | rg "pattern"`
- Balance specificity vs flexibility to avoid false positives/negatives

## ScopeDoctorGroup

Define environment setup and maintenance checks with automated fixes.

### Structure

```yaml
apiVersion: scope.github.com/v1alpha
kind: ScopeDoctorGroup
metadata:
  name: tool-name
  description: Brief description of what this group does
spec:
  include: when-required # or "by-default"
  needs:
    - dependency-1
    - dependency-2
  actions:
    - name: action-name
      description: What this action checks/fixes
      required: true # default true; false for optional checks
      check:
        paths:
          - 'file-to-watch.txt'
          - '**/*.config'
        commands:
          - ./bin/check-script.sh
      fix:
        commands:
          - ./bin/fix-script.sh
        helpText: |
          What to do if the fix fails.
          Where to get help.
        helpUrl: https://docs.example.com/help
```

### Key Components

#### Include Modes

- **by-default**: Always runs with `scope doctor run`
- **when-required**: Only runs when explicitly specified or as dependency

#### Dependencies

List other groups that must run first in `needs` array. Creates execution graph.

#### Actions

Each action is an atomic check/fix operation that runs in order.

#### Check Logic

Determines if fix should run. Fix runs when:

- **No check defined**: Fix always runs
- **paths specified**: Any file changed or no files match globs
- **commands specified**: Any command exits non-zero
- Both can be combined (OR logic)

#### Fix Section

- **commands**: List of commands to run in order
- **helpText**: Shown if fix fails (markdown supported)
- **helpUrl**: Optional link to documentation

### File Organization

- Application setup: `{config-root}/application/`
- Environment setup: `{config-root}/environment/`
- Project-specific: `.scope/` in project root

### Example

```yaml
apiVersion: scope.github.com/v1alpha
kind: ScopeDoctorGroup
metadata:
  name: ruby-version
  description: Set up Ruby with correct version
spec:
  include: when-required
  needs:
    - ruby-manager
    - homebrew
  actions:
    - name: install
      description: Ensures correct version of ruby is installed
      check:
        paths:
          - '{{ working_dir }}/.ruby-version'
        commands:
          - ./bin/ruby-version.sh verify
      fix:
        commands:
          - ./bin/ruby-version.sh install
        helpText: |
          Ruby installation failed.
          Contact: #help-channel
```

### Script Conventions

Create helper scripts following check/fix pattern:

```bash
#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-check}"

check() {
  # Return 0 if check passes, non-zero if fix needed
  if [[ condition ]]; then
    echo "Check passed"
    return 0
  else
    echo "Check failed" >&2
    return 1
  fi
}

fix() {
  # Perform fix, return 0 on success
  echo "Running fix..."
  # Fix commands here
  return 0
}

case "$ACTION" in
  check) check ;;
  fix) fix ;;
  *)
    echo "Usage: $0 [check|fix]" >&2
    exit 1
    ;;
esac
```

Script best practices:

- Use relative paths with `./` prefix (relative to YAML file)
- Make scripts idempotent (safe to run multiple times)
- Exit 0 for success, non-zero for failure
- Write errors to stderr
- Include helpful error messages

### Caching

File-based checks use content hashing:

- Cache stores file path and content hash
- Only re-runs if file contents change
- Persists between runs
- Disable with `--no-cache`

## ScopeReportLocation

Configure where and how bug reports are uploaded.

### GitHub Issues

```yaml
apiVersion: scope.github.com/v1alpha
kind: ScopeReportLocation
metadata:
  name: github
spec:
  destination:
    githubIssue:
      owner: org-name
      repo: repo-name
  additionalData:
    nodeVersion: node -v
    rubyPath: which ruby
```

Authentication via environment variables:

- GitHub App: `SCOPE_GH_APP_ID` + `SCOPE_GH_APP_KEY`
- Personal Access Token: `SCOPE_GH_TOKEN`

### Local File System

```yaml
apiVersion: scope.github.com/v1alpha
kind: ScopeReportLocation
metadata:
  name: local
spec:
  destination:
    local:
      directory: /tmp/scope-reports
  additionalData:
    pwd: pwd
    username: id -un
    scopeVersion: scope version
```

### RustyPaste

```yaml
apiVersion: scope.github.com/v1alpha
kind: ScopeReportLocation
metadata:
  name: rustypaste
spec:
  destination:
    rustyPaste:
      url: http://localhost:8000
```

### Additional Data

Capture environment context with arbitrary commands:

```yaml
additionalData:
  diskSpace: df -h
  gitBranch: git branch --show-current
  envVars: env | sort
```

Commands execute at report generation time. Scope automatically redacts secrets.

## Common Patterns

### Version Check Pattern

```yaml
actions:
  - name: minimum-version
    description: Ensure minimum version installed
    check:
      commands:
        - ./bin/check-version.sh check tool 1.2.3
    fix:
      helpText: |
        You don't have the minimum version installed.
        Check Managed Software Center for updates.
```

### File-Based Check Pattern

```yaml
actions:
  - name: config-file
    description: Verify config file exists and is valid
    check:
      paths:
        - .config-file
      commands:
        - test -s .config-file
    fix:
      commands:
        - ./bin/setup-config.sh
```

### Service Health Pattern

```yaml
actions:
  - name: service-running
    description: Ensure service is running
    check:
      commands:
        - ./bin/check-service.sh
    fix:
      commands:
        - ./bin/start-service.sh
      helpText: |
        Service failed to start.
        Check logs: tail "$(brew --prefix)/var/log/service.log"
```

### Dependency Install Pattern

```yaml
actions:
  - name: install-packages
    description: Install project dependencies
    check:
      paths:
        - package.json
        - yarn.lock
    fix:
      commands:
        - yarn install
```

### Orchestration Pattern

```yaml
# Main group that just coordinates dependencies
spec:
  needs:
    - environment-setup
    - database-setup
    - language-runtime
  actions: [] # No actions, just orchestration
```

## Workflow: Creating Known Error

1. **Identify error pattern**

   - Capture actual error output
   - Find unique identifying text
   - Create regex pattern

2. **Create files**

   ```bash
   mkdir -p {config-root}/known-errors/category
   touch {config-root}/known-errors/category/error-name.yaml
   touch {config-root}/known-errors/category/error-name.txt
   ```

3. **Write YAML definition**

   - Use template structure
   - Write clear help text with numbered steps
   - Add fix commands if automation is possible

4. **Create test file**

   - Put actual error output in `.txt` file
   - Include enough context for pattern matching

5. **Test pattern**

   ```bash
   scope analyze logs \
     --extra-config {config-root} \
     {config-root}/known-errors/category/error-name.txt
   ```

6. **Validate schema**
   ```bash
   jsonschema validate schema.json error-name.yaml
   ```

## Workflow: Creating Doctor Group

1. **Define problem domain**

   - What needs checking/fixing?
   - What are the dependencies?
   - Application or environment level?

2. **Create group file**

   ```bash
   # Application-level
   touch {config-root}/application/tool.yaml
   
   # Environment-level
   touch {config-root}/environment/tool.yaml
   
   # Project-specific
   touch .scope/tool.yaml
   ```

3. **Create helper scripts**

   ```bash
   mkdir -p .scope/bin
   touch .scope/bin/tool.sh
   chmod +x .scope/bin/tool.sh
   ```

4. **Write group definition**

   - Define metadata (name, description)
   - List dependencies in `needs`
   - Create actions for each discrete check
   - Reference scripts with relative paths

5. **Test the group**

   ```bash
   scope doctor list                       # Verify detected
   scope doctor run --only tool            # Test execution
   scope doctor run --only tool --no-cache # Test without cache
   ```

6. **Add to parent group**
   Update parent group's `needs` list if this is a new dependency

## Debugging

### Known Error Not Matching

- Test regex: `rg "pattern" test-file.txt`
- Check special character escaping
- Verify pattern exists in test file
- Use `scope analyze logs --extra-config` with test file

### Doctor Check Always Running

- Verify `paths` globs match files
- Check commands exit 0 on success
- Try `--no-cache` to rule out caching
- Verify script permissions (executable)

### Dependency Issues

- Run `scope doctor list` to see execution order
- Verify all `needs` items exist
- Check for circular dependencies
- Use `--only` to test individual groups

### Script Path Issues

- Use `./` prefix for relative paths (relative to YAML)
- Ensure scripts have execute permissions
- Use absolute paths or PATH for system commands
- Verify working directory

## Security Features

### Automatic Redaction

Scope automatically redacts sensitive information:

- GitHub API tokens
- AWS credentials
- SSH keys
- Environment variable values containing secrets
- Uses patterns from [ripsecrets](https://github.com/sirwart/ripsecrets)

This makes it safe to capture full environment in reports and share debug output publicly.

## Reference

### Configuration Structure

```
config-repository/
├── {config-root}/
│   ├── application/          # App-level (ruby, node, postgres)
│   ├── environment/          # System-level (homebrew, docker, github)
│   ├── known-errors/         # Error definitions by category
│   │   ├── docker/
│   │   ├── ruby/
│   │   ├── git/
│   │   └── ...
│   └── reports/              # Report locations
```

### At Scale

Real-world implementations include:

- 70+ known error definitions
- 30+ doctor groups
- Categories: Docker, Ruby, Git, GitHub, MySQL, Postgres, DNS, AWS
- Reduces time-to-resolution for common issues
- Self-service troubleshooting
- Consistent environments across teams

## Additional Resources

See references directory for:

- `quick-reference.md` - Command cheat sheet and pattern examples
- `real-world-examples.md` - Production-tested configurations
- `testing-guide.md` - Comprehensive validation workflows
