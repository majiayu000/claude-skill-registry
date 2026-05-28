---
name: version-bump
description: Calculate semantic version bumps for any project type using version file adapters
user-invocable: false
---

# Version Bump

## Purpose

Reads the current version from any project type (Node.js, Python, Rust, Go, Java, generic, Claude Code plugins), analyzes git commits since the last release tag, and calculates the appropriate semantic version bump (major/minor/patch) based on conventional commit patterns. Supports multiple version files kept in sync.

## Input Context

Requires:
- **Project Configuration**: Output from `detect-project-type` skill
- **Version Type** (optional): "major", "minor", "patch", or "auto" (default)

## Workflow

### 1. Load Project Configuration

Use configuration from `detect-project-type`:
- Project type
- Version file paths and adapters
- Tag pattern
- Conventional commits enabled/disabled

### 2. Read Current Version

Use the Read tool to read the primary version file and extract the version. See [Version Adapters Reference](../../docs/version-adapters.md) for detailed adapter implementations.

**For JSON files (package.json, plugin.json):**
1. Use Read tool to read the JSON file
2. Parse JSON content to extract the "version" field value
3. Store the extracted version as current_version

**For TOML files (Cargo.toml, pyproject.toml):**
1. Use Read tool to read the TOML file
2. For Cargo.toml: Search for line starting with "version = " in the [package] section
3. For pyproject.toml: Search in [project] or [tool.poetry] section for "version = "
4. Extract the version value from between the quotes
5. Store as current_version

**For Python __version__.py files:**
1. Use Read tool to read the __version__.py file
2. Search for line starting with "__version__ = "
3. Extract the version string from between the quotes
4. Store as current_version

**For text files (VERSION, version.txt):**
1. Use Read tool to read the file
2. The entire file content (with whitespace trimmed) is the version
3. Store as current_version

**For Gradle files:**
1. Use Read tool to read gradle.properties or build.gradle
2. For gradle.properties: Search for line "version=" and extract value after the =
3. For build.gradle: Search for line "version = " and extract value from between quotes
4. Store as current_version

**For Maven pom.xml:**
1. Use Read tool to read pom.xml
2. Search for the first <version> tag in the project section
3. Extract the version value between <version> and </version> tags
4. Store as current_version

**For Go projects (git tags only):**
1. Use Bash tool: `git describe --tags --abbrev=0 2>/dev/null`
2. If successful, remove the 'v' prefix if present (e.g., "v1.2.3" → "1.2.3")
3. If no tags exist, use "0.0.0" as default
4. Store as current_version

**For multiple version files:**
1. Read version from the primary file (first in list) using appropriate method above
2. Read version from each secondary file using appropriate method
3. Compare all versions - if they don't match, warn the user with version mismatch details
4. Use the primary file's version as current_version

### 3. Find Last Release Tag

Use the tag pattern from project configuration to find the most recent release tag:

1. Get the tag_pattern from project configuration (e.g., "v{version}", "{package}-v{version}")
2. Convert the pattern to a git tag search pattern:
   - `v{version}` → search for `v*`
   - `{package}-v{version}` → search for `{package}-v*`
3. Use Bash tool to list tags: `git tag -l "v*" --sort=-version:refname` (adjust pattern as needed)
4. Take the first (most recent) tag from the sorted list
5. Store as last_tag

**If no tag exists:**
- This is likely the first release
- Use current version from file as baseline
- The bump type will be "initial" (not a bump, but initial release)

### 4. Analyze Commits Since Last Release

Get the list of commits to analyze for version bump determination:

1. If last_tag exists:
   - Use Bash: `git log {last_tag}..HEAD --format="%s" --no-merges` to get commit messages since the tag
2. If no last_tag (first release):
   - Use Bash: `git log --format="%s" --no-merges` to get all commit messages
3. Store the list of commit messages for parsing

### 5. Parse Conventional Commits

If `conventional_commits` is enabled in configuration (default: true), analyze each commit message:

**Major Bump Indicators (breaking changes):**
- Commit message contains `BREAKING CHANGE:` or `BREAKING-CHANGE:` anywhere
- Commit type followed by exclamation mark: `feat!:`, `fix!:`, `refactor!:`, etc.

**Minor Bump Indicators (new features):**
- Commit starts with `feat:` or `feat(scope):`

**Patch Bump Indicators (bug fixes and other):**
- Commit starts with `fix:` or `fix(scope):`
- Other conventional types: `chore:`, `docs:`, `style:`, `refactor:`, `test:`, `perf:`

**Analysis Process:**
1. Initialize counters: breaking_count=0, feat_count=0, fix_count=0
2. For each commit message in the list:
   - Check if it contains "BREAKING CHANGE:" or "BREAKING-CHANGE:", increment breaking_count
   - Check if it matches pattern `*!:*` (type with exclamation), increment breaking_count
   - Check if it starts with "feat:" or "feat(*", increment feat_count
   - Check if it starts with "fix:" or "fix(*", increment fix_count
3. Store the counts for use in determining bump type

**If `conventional_commits` is disabled:**
- Default to patch bump for any commits (unless explicit version type was provided by user)

### 6. Determine Bump Type

Apply precedence rules to determine the semantic version bump:

1. **If user provided explicit version type** (major/minor/patch via argument):
   - Use the explicit type, ignoring commit analysis
   - Set bump_type to the user's choice
   - Add reasoning: "Explicit {type} bump requested by user"

2. **Else if breaking_count > 0:**
   - Set bump_type = "major"
   - Add reasoning: "{breaking_count} breaking change(s) detected → major bump"

3. **Else if feat_count > 0:**
   - Set bump_type = "minor"
   - Add reasoning: "{feat_count} feature(s) added → minor bump"

4. **Else if fix_count > 0 or any other commits exist:**
   - Set bump_type = "patch"
   - Add reasoning: "{fix_count} fix(es) applied → patch bump" or "Commits detected → patch bump (default)"

5. **Else (no commits since last tag):**
   - Set bump_type = "none"
   - Add reasoning: "No new commits since last release"

**Special case: Initial release (no last tag):**
- If current version is 0.x.x, treat as pre-1.0 (no bump needed)
- If current version is 1.0.0+, use as-is
- Otherwise, default to 1.0.0

### 7. Calculate New Version

Parse the current version and calculate the new version based on bump type:

1. **Parse the current version** (format: X.Y.Z):
   - Split current_version by '.' to get major, minor, patch numbers
   - If patch has pre-release metadata (e.g., "3-alpha"), extract only the numeric part
   - Store major, minor, patch as integers

2. **Calculate new version based on bump_type:**
   - **If bump_type is "major":**
     - Increment major by 1
     - Reset minor and patch to 0
     - new_version = "{major+1}.0.0"

   - **If bump_type is "minor":**
     - Keep major unchanged
     - Increment minor by 1
     - Reset patch to 0
     - new_version = "{major}.{minor+1}.0"

   - **If bump_type is "patch":**
     - Keep major and minor unchanged
     - Increment patch by 1
     - new_version = "{major}.{minor}.{patch+1}"

   - **If bump_type is "none" or "initial":**
     - Keep version unchanged
     - new_version = current_version

3. Store new_version for output

### 8. Generate Reasoning

Create a human-readable list explaining the version bump decision:

1. Initialize an empty reasoning list
2. Add reasoning based on what was detected:
   - If breaking_count > 0: Add "{breaking_count} breaking change(s) detected → major bump"
   - If feat_count > 0: Add "{feat_count} feature(s) added → minor bump"
   - If fix_count > 0: Add "{fix_count} fix(es) applied → patch bump"
3. If multiple bump indicators exist, add a note about precedence (e.g., "Major bump takes precedence")
4. If no conventional commits were found, add "No conventional commits found → patch bump (default)"
5. If explicit version type was provided, add "Explicit {type} bump requested by user"

## Output Format

Return:

```json
{
  "current_version": "1.2.3",
  "new_version": "1.3.0",
  "bump_type": "minor",
  "reasoning": [
    "2 feature(s) added → minor bump",
    "1 fix(es) applied → patch bump",
    "Minor bump takes precedence"
  ],
  "last_tag": "v1.2.3",
  "commits_analyzed": 5,
  "version_files": [
    {
      "path": "package.json",
      "current": "1.2.3",
      "new": "1.3.0",
      "adapter": "json"
    }
  ],
  "commit_examples": [
    "feat: add new deployment command",
    "fix: correct version detection",
    "docs: update README"
  ]
}
```

## Examples

### Example 1: Node.js Project - Minor Bump

**Input:**
- Project type: `nodejs`
- Version file: `package.json` (current: `1.1.0`)
- Last tag: `v1.1.0`

**Commits since v1.1.0:**
```
feat: add new API endpoint
fix: handle edge case in parser
docs: update installation guide
```

**Output:**
```json
{
  "current_version": "1.1.0",
  "new_version": "1.2.0",
  "bump_type": "minor",
  "reasoning": [
    "1 feature(s) added → minor bump",
    "1 fix(es) applied → patch bump",
    "Minor bump takes precedence"
  ],
  "last_tag": "v1.1.0",
  "commits_analyzed": 3,
  "version_files": [
    {
      "path": "package.json",
      "current": "1.1.0",
      "new": "1.2.0",
      "adapter": "json"
    }
  ]
}
```

### Example 2: Python Project - Major Bump with Multiple Version Files

**Input:**
- Project type: `python`
- Version files:
  - `pyproject.toml` (current: `2.1.0`)
  - `src/mypackage/__version__.py` (current: `2.1.0`)
- Last tag: `v2.1.0`

**Commits:**
```
feat!: redesign API interface
BREAKING CHANGE: removed legacy methods
```

**Output:**
```json
{
  "current_version": "2.1.0",
  "new_version": "3.0.0",
  "bump_type": "major",
  "reasoning": [
    "1 breaking change(s) detected → major bump"
  ],
  "last_tag": "v2.1.0",
  "commits_analyzed": 1,
  "version_files": [
    {
      "path": "pyproject.toml",
      "current": "2.1.0",
      "new": "3.0.0",
      "adapter": "toml"
    },
    {
      "path": "src/mypackage/__version__.py",
      "current": "2.1.0",
      "new": "3.0.0",
      "adapter": "python-file"
    }
  ]
}
```

### Example 3: Rust Project - Patch Bump

**Input:**
- Project type: `rust`
- Version file: `Cargo.toml` (current: `0.3.1`)
- Last tag: `v0.3.1`

**Commits:**
```
fix: correct memory leak in parser
test: add unit tests for edge cases
```

**Output:**
```json
{
  "current_version": "0.3.1",
  "new_version": "0.3.2",
  "bump_type": "patch",
  "reasoning": [
    "1 fix(es) applied → patch bump"
  ],
  "last_tag": "v0.3.1",
  "commits_analyzed": 2
}
```

### Example 4: Go Project - First Release

**Input:**
- Project type: `go`
- Version via tags: (no tags exist)
- Version from go.mod: N/A

**Output:**
```json
{
  "current_version": "0.0.0",
  "new_version": "1.0.0",
  "bump_type": "initial",
  "reasoning": [
    "No previous tags found → first release",
    "Defaulting to v1.0.0"
  ],
  "last_tag": null,
  "commits_analyzed": 15
}
```

### Example 5: Explicit Version Type Override

**Input:**
- Project type: `nodejs`
- Current version: `1.5.0`
- Version type: `major` (explicit)

**Output:**
```json
{
  "current_version": "1.5.0",
  "new_version": "2.0.0",
  "bump_type": "major",
  "reasoning": [
    "Explicit major bump requested by user"
  ],
  "last_tag": "v1.5.0",
  "commits_analyzed": 8
}
```

### Example 6: Version Mismatch Warning

**Input:**
- Version files:
  - `package.json`: `1.2.0`
  - `src/version.ts`: `1.1.9`

**Output:**
```json
{
  "current_version": "1.2.0",
  "new_version": "1.3.0",
  "bump_type": "minor",
  "warnings": [
    "Version mismatch detected:",
    "  package.json: 1.2.0",
    "  src/version.ts: 1.1.9",
    "Using primary version: 1.2.0",
    "Both files will be updated to: 1.3.0"
  ]
}
```

## Error Handling

**Invalid version format:**
```json
{
  "error": "Invalid version format in package.json: 'v1.2.3'",
  "suggestion": "Version must be X.Y.Z format (e.g., 1.2.3)"
}
```

**No version file found:**
```json
{
  "error": "Could not read version from package.json",
  "suggestion": "Ensure file exists and contains 'version' field"
}
```

**Git errors:**
```json
{
  "error": "Git log failed: not a git repository",
  "suggestion": "Run 'git init' to initialize repository"
}
```

## Integration Notes

This skill is invoked by the `/release` command in Phase 2. The command will:
1. Display calculated version bump with reasoning
2. Prompt user to confirm or provide custom version
3. Use confirmed version for remaining phases
4. Update all version files in Phase 4 (documentation-sync skill)

## Reference Documentation

- [Version Adapters Reference](../../docs/version-adapters.md) - Adapter implementations
- [Configuration Reference](../../docs/configuration.md) - Conventional commits settings
