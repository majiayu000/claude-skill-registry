---
name: pre-release-validation
description: Validate release readiness for any project type with comprehensive checks
user-invocable: false
---

# Pre-Release Validation

## Purpose

Performs comprehensive validation checks before finalizing a release for any project type. Validates version files, changelog, git state, and runs project-specific and custom validation checks. Returns both blocking errors (must be fixed) and non-blocking warnings (can proceed with caution).

## Input Context

Requires:
- **Project Configuration**: Output from `detect-project-type` skill
- **New Version**: Version to be released (e.g., "1.2.0")
- **Changelog Path**: Path to changelog file
- **Modified Files**: List of files that will be committed

## Workflow

### 1. Load Configuration

Use configuration from `detect-project-type`:
- `project_type` - Determines project-specific checks
- `version_files` - Files to validate
- `tag_pattern` - For checking tag conflicts
- `custom_validations` - Custom validation scripts
- `skip_validations` - Validations to skip

### 2. Version Tag Conflict Check

Check if a git tag already exists for this version:

```bash
# Build tag name from pattern
tag_pattern="v{version}"  # from config
tag_name="${tag_pattern//\{version\}/$new_version}"

# Check if tag exists
if git tag -l "$tag_name" | grep -q "$tag_name"; then
  error="Version $new_version already released (tag $tag_name exists)"
  suggestion="Choose a different version or delete existing tag with: git tag -d $tag_name"
fi
```

**Can skip with:** `skip_validations: ["version-tag-conflict"]`

### 3. Version Format Validation

Validate the version string follows semantic versioning:

```bash
# Semantic version pattern: X.Y.Z
if ! echo "$new_version" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
  error="Invalid version format: $new_version (expected X.Y.Z)"
  suggestion="Use semantic versioning format like 1.2.3"
fi
```

**Can skip with:** `skip_validations: ["version-format"]`

### 4. Version Progression Check

Compare new version to current version:

```bash
# Parse versions
IFS='.' read -r curr_major curr_minor curr_patch <<< "$current_version"
IFS='.' read -r new_major new_minor new_patch <<< "$new_version"

# Check if new > current
is_greater=false

if [ $new_major -gt $curr_major ]; then
  is_greater=true
elif [ $new_major -eq $curr_major ] && [ $new_minor -gt $curr_minor ]; then
  is_greater=true
elif [ $new_major -eq $curr_major ] && [ $new_minor -eq $curr_minor ] && [ $new_patch -gt $curr_patch ]; then
  is_greater=true
fi

if [ "$is_greater" = false ]; then
  error="New version $new_version must be greater than current version $current_version"
  suggestion="Increment version appropriately"
fi
```

**Can skip with:** `skip_validations: ["version-progression"]`

### 5. Required Files Existence

Check that all version files and required project files exist:

```bash
required_files=()

# Add version files
for version_file in "${version_files[@]}"; do
  required_files+=("$version_file")
done

# Add changelog
required_files+=("$changelog_file")

# Project-specific required files
case "$project_type" in
  "nodejs")
    required_files+=("package.json")
    ;;
  "python")
    # pyproject.toml or setup.py required
    if [ ! -f "pyproject.toml" ] && [ ! -f "setup.py" ]; then
      error="Python project requires pyproject.toml or setup.py"
    fi
    ;;
  "rust")
    required_files+=("Cargo.toml")
    ;;
  "go")
    required_files+=("go.mod")
    ;;
  "java")
    # build.gradle or pom.xml required
    if [ ! -f "build.gradle" ] && [ ! -f "gradle.properties" ] && [ ! -f "pom.xml" ]; then
      error="Java project requires build.gradle, gradle.properties, or pom.xml"
    fi
    ;;
esac

# Check each required file
for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    error="Required file not found: $file"
    suggestion="Create the file before releasing"
  fi
done
```

**Can skip with:** `skip_validations: ["required-files"]`

### 6. Version File Validity

Validate each version file can be parsed and read:

```bash
for version_file_config in "${version_files[@]}"; do
  file_path="${version_file_config[path]}"
  adapter="${version_file_config[adapter]}"

  case "$adapter" in
    "json")
      # Validate JSON
      if ! jq empty "$file_path" 2>/dev/null; then
        error="Invalid JSON in $file_path"
        suggestion="Fix JSON syntax errors"
      fi

      # Check version field exists
      if ! jq -e '.version' "$file_path" >/dev/null 2>&1; then
        error="Missing 'version' field in $file_path"
      fi
      ;;

    "toml")
      # Validate TOML syntax (basic check)
      if ! grep -q '^version = ' "$file_path"; then
        error="No version field found in $file_path"
      fi
      ;;

    "python-file")
      # Validate Python syntax
      if ! python -c "import ast; ast.parse(open('$file_path').read())" 2>/dev/null; then
        error="Invalid Python syntax in $file_path"
      fi

      # Check __version__ is defined
      if ! grep -q '^__version__ = ' "$file_path"; then
        error="Missing __version__ in $file_path"
      fi
      ;;

    "text")
      # Check file is not empty
      if [ ! -s "$file_path" ]; then
        error="Version file $file_path is empty"
      fi
      ;;
  esac
done
```

**Can skip with:** `skip_validations: ["json-validity"]` or `skip_validations: ["version-file-validity"]`

### 7. Changelog Entry Verification

Read changelog file and verify entry exists for new version:

```bash
if [ ! -f "$changelog_file" ]; then
  warning="Changelog file $changelog_file does not exist (will be created)"
else
  # Look for version entry in changelog
  version_pattern="## Version $new_version"

  if ! grep -q "$version_pattern" "$changelog_file"; then
    error="Changelog entry for version $new_version not found in $changelog_file"
    suggestion="Run changelog-update skill to generate entry"
  else
    # Check if entry has content (not just header)
    # Get lines after version header until next version or EOF
    entry_lines=$(sed -n "/^## Version $new_version/,/^## Version/p" "$changelog_file" | wc -l)

    if [ $entry_lines -lt 3 ]; then
      warning="Changelog entry for $new_version appears to be empty"
    fi
  fi
fi
```

**Can skip with:** `skip_validations: ["changelog-entry"]`

### 8. Git Remote Configuration

Check if git remote is configured:

```bash
if ! git remote -v | grep -q 'origin'; then
  warning="No git remote 'origin' configured - push will fail"
  suggestion="Add remote with: git remote add origin <url>"
fi
```

**Can skip with:** `skip_validations: ["git-remote"]`

### 9. Uncommitted Changes Check

Check for unexpected uncommitted changes:

```bash
# Get all uncommitted files
uncommitted=$(git status --porcelain | grep -v '^??' | cut -c 4-)

# Filter out expected release files
expected_files=(
  "$changelog_file"
  "${version_files[@]}"
  "${modified_files[@]}"
)

unexpected_changes=()

while IFS= read -r file; do
  is_expected=false

  for expected in "${expected_files[@]}"; do
    if [ "$file" = "$expected" ]; then
      is_expected=true
      break
    fi
  done

  if [ "$is_expected" = false ]; then
    unexpected_changes+=("$file")
  fi
done <<< "$uncommitted"

if [ ${#unexpected_changes[@]} -gt 0 ]; then
  warning="Unexpected uncommitted changes found:"
  for file in "${unexpected_changes[@]}"; do
    warning+=" - $file"
  done
  suggestion="Commit or stash unrelated changes before release"
fi
```

### 10. Branch Validation

Check current branch matches expected:

```bash
current_branch=$(git branch --show-current)
expected_branches=("master" "main")

is_valid_branch=false
for branch in "${expected_branches[@]}"; do
  if [ "$current_branch" = "$branch" ]; then
    is_valid_branch=true
    break
  fi
done

if [ "$is_valid_branch" = false ]; then
  warning="Not on master/main branch (currently on $current_branch)"
  suggestion="Releases are typically done from master/main branch"
fi
```

### 11. Project-Specific Validations

Run validations specific to project type:

**Node.js:**
```bash
if [ "$project_type" = "nodejs" ]; then
  # Check if node_modules exists (dependencies installed)
  if [ ! -d "node_modules" ]; then
    warning="node_modules not found - dependencies may not be installed"
    suggestion="Run: npm install"
  fi

  # Check for package-lock.json or yarn.lock consistency
  if [ -f "package-lock.json" ]; then
    # Verify lockfile is in sync (would need npm ci to fully validate)
    if ! npm ls >/dev/null 2>&1; then
      warning="Dependency tree has issues - check with npm ls"
    fi
  fi
fi
```

**Python:**
```bash
if [ "$project_type" = "python" ]; then
  # Check if pyproject.toml is valid
  if [ -f "pyproject.toml" ]; then
    # Try to build (dry-run)
    if command -v python >/dev/null 2>&1; then
      if ! python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))" 2>/dev/null; then
        warning="pyproject.toml may have syntax errors"
      fi
    fi
  fi

  # Check if dist/ directory exists from previous builds
  if [ -d "dist" ]; then
    warning="dist/ directory exists from previous build"
    suggestion="Consider cleaning with: rm -rf dist/"
  fi
fi
```

**Rust:**
```bash
if [ "$project_type" = "rust" ]; then
  # Check if Cargo.lock is in sync
  if [ -f "Cargo.lock" ]; then
    if ! cargo check --quiet 2>/dev/null; then
      warning="Cargo check failed - dependencies may have issues"
    fi
  fi
fi
```

**Go:**
```bash
if [ "$project_type" = "go" ]; then
  # Verify go.mod is valid
  if ! go mod verify 2>/dev/null; then
    warning="go.mod verification failed"
  fi

  # Check for go.sum
  if [ ! -f "go.sum" ]; then
    warning="go.sum not found"
    suggestion="Run: go mod tidy"
  fi
fi
```

### 12. Custom Validation Scripts

Run custom validation scripts from configuration:

```bash
if [ ${#custom_validations[@]} -gt 0 ]; then
  for script in "${custom_validations[@]}"; do
    echo "Running custom validation: $script"

    if [ -x "$script" ]; then
      # Run script and capture output
      if ! output=$($script 2>&1); then
        error="Custom validation failed: $script"
        error+="Output: $output"
      fi
    else
      warning="Custom validation script not executable: $script"
    fi
  done
fi
```

### 13. Pre-Release Hook Validation

If `preReleaseHook` is configured, validate it exists and is executable:

```bash
if [ -n "$pre_release_hook" ]; then
  if [ ! -f "$pre_release_hook" ]; then
    warning="Pre-release hook not found: $pre_release_hook"
  elif [ ! -x "$pre_release_hook" ]; then
    warning="Pre-release hook not executable: $pre_release_hook"
    suggestion="Run: chmod +x $pre_release_hook"
  fi
fi
```

## Output Format

Return validation results:

```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    {
      "level": "WARNING",
      "check": "branch_validation",
      "message": "Not on master branch (currently on develop)",
      "suggestion": "Switch to master with: git checkout master"
    }
  ],
  "checks_passed": 12,
  "checks_total": 13,
  "checks_skipped": ["git-remote"],
  "project_specific_checks": {
    "nodejs": ["dependencies_installed", "lockfile_valid"]
  }
}
```

## Examples

### Example 1: All Checks Pass (Node.js)

**Input:**
- Project type: `nodejs`
- New version: `1.2.0`
- Current version: `1.1.0`

**Output:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "checks_passed": 13,
  "checks_total": 13,
  "project_specific_checks": {
    "nodejs": ["dependencies_installed", "lockfile_valid"]
  }
}
```

### Example 2: Version Conflict

**Input:**
- New version: `1.0.0`
- Tag `v1.0.0` exists

**Output:**
```json
{
  "valid": false,
  "errors": [
    {
      "level": "BLOCKING",
      "check": "version_tag_conflict",
      "message": "Version 1.0.0 already released (tag v1.0.0 exists)",
      "suggestion": "Choose version 1.0.1 or 1.1.0 instead"
    }
  ],
  "warnings": [],
  "checks_passed": 12,
  "checks_total": 13
}
```

### Example 3: Missing Changelog Entry (Python)

**Input:**
- Project type: `python`
- New version: `2.0.0`
- Changelog exists but no entry for 2.0.0

**Output:**
```json
{
  "valid": false,
  "errors": [
    {
      "level": "BLOCKING",
      "check": "changelog_entry",
      "message": "Changelog entry for version 2.0.0 not found in CHANGELOG.md",
      "suggestion": "Add changelog entry before releasing"
    }
  ],
  "warnings": [],
  "checks_passed": 12,
  "checks_total": 13
}
```

### Example 4: Multiple Warnings (Rust)

**Input:**
- Project type: `rust`
- On `feature-branch`
- No git remote
- Cargo check warnings

**Output:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    {
      "level": "WARNING",
      "check": "branch_validation",
      "message": "Not on master/main branch (currently on feature-branch)",
      "suggestion": "Switch to master before releasing"
    },
    {
      "level": "WARNING",
      "check": "git_remote",
      "message": "No git remote configured - push will fail",
      "suggestion": "Add remote with: git remote add origin <url>"
    },
    {
      "level": "WARNING",
      "check": "rust_cargo_check",
      "message": "Cargo check reported warnings",
      "suggestion": "Fix warnings before releasing"
    }
  ],
  "checks_passed": 10,
  "checks_total": 13
}
```

### Example 5: Custom Validation Failure

**Input:**
- Custom validation: `./scripts/validate-docs.sh`
- Script exits with code 1

**Output:**
```json
{
  "valid": false,
  "errors": [
    {
      "level": "BLOCKING",
      "check": "custom_validation",
      "message": "Custom validation failed: ./scripts/validate-docs.sh",
      "output": "Error: Missing API documentation for new endpoints"
    }
  ],
  "checks_passed": 12,
  "checks_total": 13
}
```

### Example 6: Skipped Validations

**Input:**
- Configuration: `skip_validations: ["git-remote", "branch-validation"]`

**Output:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "checks_passed": 11,
  "checks_total": 13,
  "checks_skipped": ["git-remote", "branch-validation"]
}
```

## Error Handling

**Git command failures:**
```json
{
  "valid": false,
  "errors": [
    {
      "check": "git_state",
      "message": "Git command failed: not a git repository",
      "suggestion": "Ensure you're in a git repository"
    }
  ]
}
```

**File read errors:**
```json
{
  "valid": false,
  "errors": [
    {
      "check": "file_access",
      "message": "Cannot read version file: package.json",
      "suggestion": "Check file permissions"
    }
  ]
}
```

## Auto-Fix Suggestions

For certain errors, provide auto-fix options:

**Version conflict:**
- Suggest next patch: `1.2.1`
- Suggest next minor: `1.3.0`

**Missing changelog:**
- Offer to run `changelog-update` skill

**Invalid JSON:**
- Show exact parse error location
- Offer to format with `jq`

## Integration Notes

This skill is invoked by the `/release` command in Phase 5. The command will:
1. Display all errors and warnings
2. Block release if `valid: false`
3. Prompt user to proceed if only warnings
4. Offer auto-fix for fixable errors
5. Allow retry after manual fixes

## Reference Documentation

- [Configuration Reference](../../docs/configuration.md) - Custom validations and skip settings
- [Version Adapters Reference](../../docs/version-adapters.md) - Version file validation
