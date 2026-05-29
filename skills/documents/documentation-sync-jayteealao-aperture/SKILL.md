---
name: documentation-sync
description: Synchronize version numbers across any project type using version file adapters
user-invocable: false
---

# Documentation Sync

## Purpose

Updates version numbers in version files (using appropriate adapters) and documentation files for any project type. Supports Node.js, Python, Rust, Go, Java, generic projects, and Claude Code plugins. Handles multiple version files and documentation references.

## Input Context

Requires:
- **Project Configuration**: Output from `detect-project-type` skill
- **Old Version**: Previous version string (e.g., "1.1.0")
- **New Version**: New version string (e.g., "1.2.0")

## Workflow

### 1. Load Project Configuration

Use configuration from `detect-project-type`:
- `version_files` - List of version files with adapters
- `documentation_files` - Files to search for version references
- `project_type` - Determines file update strategy

### 2. Update Version Files

For each version file, use the appropriate adapter to update the version.

See [Version Adapters Reference](../../docs/version-adapters.md) for implementation details.

**JSON files (package.json, plugin.json, etc.):**
```bash
file="package.json"
old_version="1.1.0"
new_version="1.2.0"

# Update using jq
jq --indent 2 ".version = \"$new_version\"" "$file" > tmp.json && mv tmp.json "$file"

# Verify update
updated_version=$(jq -r '.version' "$file")
if [ "$updated_version" = "$new_version" ]; then
  echo "✓ Updated $file: $old_version → $new_version"
else
  echo "✗ Failed to update $file"
fi
```

**TOML files (Cargo.toml, pyproject.toml):**
```bash
file="Cargo.toml"

# Update version in [package] section
sed -i '/^\[package\]/,/^\[/ s/^version = ".*"/version = "'"$new_version"'"/' "$file"

# For pyproject.toml [project] section
sed -i '/^\[project\]/,/^\[/ s/^version = ".*"/version = "'"$new_version"'"/' pyproject.toml

# For pyproject.toml [tool.poetry] section
sed -i '/^\[tool.poetry\]/,/^\[/ s/^version = ".*"/version = "'"$new_version"'"/' pyproject.toml

# Verify
updated_version=$(grep '^version = ' "$file" | head -1 | sed 's/version = "\(.*\)"/\1/')
```

**Python __version__.py files:**
```bash
file="src/mypackage/__version__.py"

# Update __version__ variable
sed -i 's/^__version__ = ".*"/__version__ = "'"$new_version"'"/' "$file"

# Verify
updated_version=$(grep '^__version__ = ' "$file" | sed 's/__version__ = "\(.*\)"/\1/')
```

**Text files (VERSION, version.txt):**
```bash
file="VERSION"

# Simply write new version
echo "$new_version" > "$file"

# Verify
updated_version=$(cat "$file" | tr -d '[:space:]')
```

**Gradle files:**
```bash
# gradle.properties
sed -i 's/^version=.*/version='"$new_version"'/' gradle.properties

# build.gradle (single quotes)
sed -i "s/^version = '.*'/version = '${new_version}'/" build.gradle

# build.gradle (double quotes)
sed -i 's/^version = ".*"/version = "'"$new_version"'"/' build.gradle
```

**Maven pom.xml:**
```bash
# Replace first <version> tag (project version)
sed -i '0,/<version>.*<\/version>/s//<version>'"$new_version"'<\/version>/' pom.xml
```

**Multiple version files:**
Update all files in sequence, tracking successes and failures:

```bash
updated_files=()
failed_files=()

for version_file_config in "${version_files[@]}"; do
  file_path="${version_file_config[path]}"
  adapter="${version_file_config[adapter]}"

  # Update using appropriate adapter
  case "$adapter" in
    "json")
      jq --indent 2 ".version = \"$new_version\"" "$file_path" > tmp.json && mv tmp.json "$file_path"
      ;;
    "toml")
      # ... toml update logic
      ;;
    "python-file")
      # ... python file update logic
      ;;
    # ... other adapters
  esac

  # Verify update succeeded
  if verify_version_updated "$file_path" "$new_version"; then
    updated_files+=("$file_path")
  else
    failed_files+=("$file_path")
  fi
done
```

### 3. Update Documentation Files

Search documentation files for version references and update them.

Use `documentation_files` from configuration (default: `["README.md"]`, supports globs).

**Find all documentation files:**
```bash
doc_files=()

for pattern in "${documentation_files[@]}"; do
  # Expand glob patterns
  if [[ "$pattern" == *"*"* ]]; then
    # Use find for glob patterns like "docs/**/*.md"
    while IFS= read -r file; do
      doc_files+=("$file")
    done < <(find . -path "./$pattern" -type f)
  else
    # Direct file path
    if [ -f "$pattern" ]; then
      doc_files+=("$pattern")
    fi
  done
done
```

**For each documentation file, perform context-aware version replacement:**

```bash
for doc_file in "${doc_files[@]}"; do
  echo "Processing $doc_file..."

  # Create backup
  cp "$doc_file" "${doc_file}.bak"

  # Perform replacements (context-aware)

  # 1. Version badges (shields.io, etc.)
  sed -i "s/version-${old_version//./-}/version-${new_version//./-}/g" "$doc_file"
  sed -i "s/v${old_version}-/v${new_version}-/g" "$doc_file"

  # 2. Installation commands
  # npm install package@1.1.0 → package@1.2.0
  sed -i "s/@${old_version}/@${new_version}/g" "$doc_file"

  # pip install package==1.1.0 → package==1.2.0
  sed -i "s/==${old_version}/==${new_version}/g" "$doc_file"

  # cargo add package@1.1.0 → package@1.2.0
  # (already covered by @version pattern)

  # 3. Git tag references
  # v1.1.0 → v1.2.0 (when followed by space, ), or end of line)
  sed -i "s/v${old_version}\([^0-9]\)/v${new_version}\1/g" "$doc_file"
  sed -i "s/v${old_version}$/v${new_version}/g" "$doc_file"

  # 4. Standalone version numbers in specific contexts
  # "Version 1.1.0" → "Version 1.2.0"
  sed -i "s/Version ${old_version}/Version ${new_version}/g" "$doc_file"
  sed -i "s/version ${old_version}/version ${new_version}/g" "$doc_file"

  # 5. In code blocks (more conservative - only in known safe contexts)
  # Only replace if part of package reference
  sed -i "s/\"${old_version}\"/\"${new_version}\"/g" "$doc_file"
  sed -i "s/'${old_version}'/'${new_version}'/g" "$doc_file"

  # Count changes
  changes=$(diff -u "${doc_file}.bak" "$doc_file" | grep '^[-+]' | wc -l)

  if [ $changes -gt 0 ]; then
    echo "✓ Updated $doc_file ($changes lines changed)"
    rm "${doc_file}.bak"
  else
    echo "  No version references found in $doc_file"
    mv "${doc_file}.bak" "$doc_file"  # Restore original
  fi
done
```

**Conservative replacement strategy:**
- Only replace version strings in known safe contexts
- Avoid replacing arbitrary numbers (could be dates, IDs, etc.)
- Use word boundaries and context markers
- Verify replacements made sense (count changes, show diff)

### 4. Project-Specific Updates

Some project types have additional files to update:

**Node.js (package-lock.json):**
```bash
if [ -f "package-lock.json" ]; then
  # Update version in lockfile (both root and package entry)
  jq ".version = \"$new_version\"" package-lock.json > tmp.json && mv tmp.json package-lock.json
  jq ".packages[\"\"].version = \"$new_version\"" package-lock.json > tmp.json && mv tmp.json package-lock.json
fi
```

**Python (setuptools-scm):**
If using setuptools-scm, version is managed by git tags - no file updates needed.

**Rust (Cargo.lock):**
If exists, update with:
```bash
cargo update --workspace
```

**Go:**
No files to update - versions managed by git tags only.

### 5. Generate Git Diff

Create a summary of all changes:

```bash
# Stage all modified files
git add -u

# Generate diff
git diff --cached > /tmp/release-diff.patch

# Display summary
echo "Files modified:"
git diff --cached --name-only

echo ""
echo "Diff summary:"
git diff --cached --stat
```

### 6. Validation

Verify all updates were successful:

```bash
validation_errors=()

# Check each version file
for file in "${updated_files[@]}"; do
  actual_version=$(read_version_from_file "$file")

  if [ "$actual_version" != "$new_version" ]; then
    validation_errors+=("$file: expected $new_version, got $actual_version")
  fi
done

# If any errors, return them
if [ ${#validation_errors[@]} -gt 0 ]; then
  echo "✗ Validation failed:"
  printf '%s\n' "${validation_errors[@]}"
  exit 1
fi
```

## Output Format

Return:

```json
{
  "files_updated": [
    "package.json",
    "README.md",
    "docs/installation.md"
  ],
  "version_files": [
    {
      "path": "package.json",
      "old_version": "1.1.0",
      "new_version": "1.2.0",
      "adapter": "json",
      "success": true
    }
  ],
  "documentation_files": [
    {
      "path": "README.md",
      "changes": 5,
      "patterns_matched": ["version badge", "installation command", "git tag reference"]
    },
    {
      "path": "docs/installation.md",
      "changes": 2,
      "patterns_matched": ["installation command"]
    }
  ],
  "warnings": [],
  "git_diff_summary": {
    "files_changed": 3,
    "insertions": 8,
    "deletions": 8
  }
}
```

## Examples

### Example 1: Node.js Project

**Input:**
- Project type: `nodejs`
- Old version: `1.1.0`
- New version: `1.2.0`
- Version files: `["package.json"]`
- Documentation files: `["README.md"]`

**Operations:**
1. Update `package.json`: `"version": "1.1.0"` → `"version": "1.2.0"`
2. Update `package-lock.json` (if exists)
3. Update `README.md`: version badge, install command

**Output:**
```json
{
  "files_updated": ["package.json", "package-lock.json", "README.md"],
  "version_files": [
    {
      "path": "package.json",
      "old_version": "1.1.0",
      "new_version": "1.2.0",
      "success": true
    }
  ],
  "documentation_files": [
    {
      "path": "README.md",
      "changes": 3,
      "patterns_matched": ["version badge", "npm install"]
    }
  ]
}
```

### Example 2: Python Project with Multiple Version Files

**Input:**
- Project type: `python`
- Old version: `2.1.0`
- New version: `3.0.0`
- Version files:
  - `pyproject.toml`
  - `src/mypackage/__version__.py`

**Operations:**
1. Update `pyproject.toml` [project] section
2. Update `src/mypackage/__version__.py`
3. Update `README.md` references

**Output:**
```json
{
  "version_files": [
    {
      "path": "pyproject.toml",
      "old_version": "2.1.0",
      "new_version": "3.0.0",
      "adapter": "toml",
      "success": true
    },
    {
      "path": "src/mypackage/__version__.py",
      "old_version": "2.1.0",
      "new_version": "3.0.0",
      "adapter": "python-file",
      "success": true
    }
  ]
}
```

### Example 3: Rust Crate

**Input:**
- Project type: `rust`
- Old version: `0.3.1`
- New version: `0.3.2`
- Version files: `["Cargo.toml"]`

**Operations:**
1. Update `Cargo.toml` [package].version
2. Run `cargo update` to update `Cargo.lock`
3. Update documentation

### Example 4: Go Module

**Input:**
- Project type: `go`
- Old version: `1.5.0`
- New version: `1.6.0`
- Version files: `[]` (versions via tags only)

**Operations:**
1. No version files to update (Go uses git tags)
2. Update README.md and docs with new version references

**Output:**
```json
{
  "version_files": [],
  "documentation_files": [
    {
      "path": "README.md",
      "changes": 2,
      "patterns_matched": ["version reference", "go get command"]
    }
  ],
  "notes": ["Go project: version managed via git tags only"]
}
```

## Error Handling

**File update failure:**
```json
{
  "version_files": [
    {
      "path": "package.json",
      "success": false,
      "error": "Permission denied"
    }
  ]
}
```

**Version mismatch after update:**
```json
{
  "warnings": [
    "package.json: expected 1.2.0 after update, but still reads 1.1.0",
    "File may need manual review"
  ]
}
```

**Documentation file not found:**
```json
{
  "warnings": [
    "Documentation file not found: docs/installation.md",
    "Specified in configuration but does not exist"
  ]
}
```

## Integration Notes

This skill is invoked by the `/release` command in Phase 4. The command will:
1. Display git diff of all changes
2. Allow user to review before proceeding
3. Stage all modified files for commit in Phase 6

## Reference Documentation

- [Version Adapters Reference](../../docs/version-adapters.md) - Adapter implementation details
- [Configuration Reference](../../docs/configuration.md) - Configuring version and documentation files
