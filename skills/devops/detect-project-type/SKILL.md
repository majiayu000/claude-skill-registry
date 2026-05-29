---
name: detect-project-type
description: Detect project type and configuration for generic application releases
user-invocable: false
---

# Detect Project Type

## Purpose

Analyzes the project directory to determine the project type (Node.js, Python, Rust, Go, Java, generic, Claude Code plugin, or monorepo) and loads or generates appropriate release configuration. This is the foundation for generic release automation that works with any application.

## Input Context

The skill expects to be invoked in a project root directory. It examines:
- Configuration files (`.release-config.json`, `.releaserc.json`)
- Project markers (package.json, Cargo.toml, pyproject.toml, etc.)
- Directory structure (monorepo patterns)
- Version file locations

## Workflow

### 1. Check for Explicit Configuration

First, check if user has provided explicit configuration:

```bash
# Check for config files in order of precedence
if [ -f ".release-config.json" ]; then
  config_file=".release-config.json"
elif [ -f ".releaserc.json" ]; then
  config_file=".releaserc.json"
elif [ -f ".releaserc" ]; then
  config_file=".releaserc"
else
  config_file=""
fi
```

If config file exists:
- Parse JSON to extract configuration
- Validate configuration (required fields, file paths exist)
- Return configuration with `config_source: "explicit"`

See [Configuration Reference](../../docs/configuration.md) for schema details.

### 2. Auto-Detect Project Type

If no configuration file, detect project type from filesystem markers:

```bash
# Detection logic (in priority order)
project_type="unknown"

# Check for monorepo first (multiple package.json or project files in subdirs)
if [ $(find packages -name "package.json" 2>/dev/null | wc -l) -gt 1 ] || \
   [ $(find apps -name "package.json" 2>/dev/null | wc -l) -gt 1 ]; then
  project_type="monorepo"

# Node.js project
elif [ -f "package.json" ]; then
  project_type="nodejs"

# Python project
elif [ -f "pyproject.toml" ]; then
  project_type="python"

# Rust project
elif [ -f "Cargo.toml" ]; then
  project_type="rust"

# Go project
elif [ -f "go.mod" ]; then
  project_type="go"

# Java/Gradle project
elif [ -f "build.gradle" ] || [ -f "gradle.properties" ]; then
  project_type="java"

# Maven project
elif [ -f "pom.xml" ]; then
  project_type="java"

# Claude Code plugin
elif [ -f ".claude-plugin/plugin.json" ]; then
  project_type="claude-plugin"

# Claude Code marketplace
elif [ -f ".claude-plugin/marketplace.json" ]; then
  project_type="claude-marketplace"

# Generic project with VERSION file
elif [ -f "VERSION" ] || [ -f "version.txt" ] || [ -f ".version" ]; then
  project_type="generic"

# Legacy Python (setup.py)
elif [ -f "setup.py" ]; then
  project_type="python"

else
  project_type="unknown"
fi
```

### 3. Determine Version Files

Based on detected project type, determine version file locations:

**Node.js:**
```bash
version_files=("package.json")
adapter="json"
field="version"
```

**Python:**
```bash
# Check for multiple version sources
version_files=()

if [ -f "pyproject.toml" ]; then
  version_files+=("pyproject.toml")
fi

# Look for __version__.py files
if [ -d "src" ]; then
  # Find __version__.py in src directory
  version_file=$(find src -name "__version__.py" | head -1)
  if [ -n "$version_file" ]; then
    version_files+=("$version_file")
  fi
fi

# Legacy setup.py
if [ -f "setup.py" ]; then
  version_files+=("setup.py")
fi
```

**Rust:**
```bash
version_files=("Cargo.toml")
```

**Go:**
```bash
# Go uses git tags for versions, no version file
version_files=()
version_via_tags=true
```

**Java/Gradle:**
```bash
if [ -f "gradle.properties" ]; then
  version_files=("gradle.properties")
elif [ -f "build.gradle" ]; then
  version_files=("build.gradle")
fi
```

**Maven:**
```bash
version_files=("pom.xml")
```

**Claude Code Plugin:**
```bash
version_files=(".claude-plugin/plugin.json")
```

**Generic:**
```bash
# Find version file by name
if [ -f "VERSION" ]; then
  version_files=("VERSION")
elif [ -f "version.txt" ]; then
  version_files=("version.txt")
elif [ -f ".version" ]; then
  version_files=(".version")
fi
```

### 4. Determine Changelog File

```bash
# Check for existing changelog in common formats
if [ -f "CHANGELOG.md" ]; then
  changelog_file="CHANGELOG.md"
elif [ -f "HISTORY.md" ]; then
  changelog_file="HISTORY.md"
elif [ -f "CHANGES.md" ]; then
  changelog_file="CHANGES.md"
elif [ -f "NEWS.md" ]; then
  changelog_file="NEWS.md"
elif [ -f "CHANGES.rst" ]; then
  changelog_file="CHANGES.rst"
else
  # Will be created
  changelog_file="CHANGELOG.md"
fi
```

### 5. Determine Tag Pattern

```bash
# Project-specific tag patterns
case "$project_type" in
  "nodejs"|"python"|"rust"|"generic")
    tag_pattern="v{version}"
    ;;
  "go")
    tag_pattern="v{version}"  # Go convention
    ;;
  "java")
    tag_pattern="v{version}"
    ;;
  "claude-plugin")
    # Use plugin name from plugin.json
    plugin_name=$(jq -r '.name' .claude-plugin/plugin.json)
    tag_pattern="${plugin_name}-v{version}"
    ;;
  "claude-marketplace")
    tag_pattern="marketplace-v{version}"
    ;;
  "monorepo")
    tag_pattern="{package}-v{version}"
    ;;
esac
```

### 6. Detect Monorepo Packages

For monorepo projects, scan for packages:

```bash
monorepo_packages=()

# Check common monorepo patterns
for pattern in "packages/*" "apps/*" "libs/*"; do
  for dir in $pattern; do
    if [ -d "$dir" ]; then
      # Check if directory contains a project marker
      if [ -f "$dir/package.json" ] || \
         [ -f "$dir/Cargo.toml" ] || \
         [ -f "$dir/pyproject.toml" ]; then
        monorepo_packages+=("$dir")
      fi
    fi
  done
done
```

### 7. Determine Documentation Files

```bash
documentation_files=("README.md")

# Add common doc patterns
if [ -d "docs" ]; then
  documentation_files+=("docs/**/*.md")
fi

if [ -d "website/docs" ]; then
  documentation_files+=("website/docs/**/*.md")
fi
```

### 8. Validation

Validate the detected configuration:

**Required validations:**
- At least one version file exists (unless Go project)
- Version files are readable
- Project type is not "unknown"

**Warnings:**
- No changelog file exists (will be created)
- No README.md exists

## Output Format

Return structured configuration:

```json
{
  "project_type": "nodejs",
  "config_source": "auto-detected",
  "version_files": [
    {
      "path": "package.json",
      "adapter": "json",
      "field": "version",
      "exists": true
    }
  ],
  "changelog_file": "CHANGELOG.md",
  "changelog_format": "keep-a-changelog",
  "tag_pattern": "v{version}",
  "tag_message": "Release v{version}",
  "conventional_commits": true,
  "documentation_files": [
    "README.md",
    "docs/**/*.md"
  ],
  "monorepo": {
    "enabled": false,
    "packages": []
  },
  "validations": {
    "errors": [],
    "warnings": [
      "No CHANGELOG.md found, will be created"
    ]
  }
}
```

## Examples

### Example 1: Node.js Project

**Project structure:**
```
/
├── package.json
├── README.md
└── src/
```

**Detection result:**
```json
{
  "project_type": "nodejs",
  "config_source": "auto-detected",
  "version_files": [
    {
      "path": "package.json",
      "adapter": "json",
      "field": "version"
    }
  ],
  "changelog_file": "CHANGELOG.md",
  "tag_pattern": "v{version}",
  "conventional_commits": true
}
```

### Example 2: Python Package

**Project structure:**
```
/
├── pyproject.toml
├── src/
│   └── mypackage/
│       └── __version__.py
└── README.md
```

**Detection result:**
```json
{
  "project_type": "python",
  "config_source": "auto-detected",
  "version_files": [
    {
      "path": "pyproject.toml",
      "adapter": "toml",
      "section": "project"
    },
    {
      "path": "src/mypackage/__version__.py",
      "adapter": "python-file"
    }
  ],
  "changelog_file": "CHANGELOG.md",
  "tag_pattern": "v{version}"
}
```

### Example 3: Rust Crate

**Project structure:**
```
/
├── Cargo.toml
├── src/
└── README.md
```

**Detection result:**
```json
{
  "project_type": "rust",
  "config_source": "auto-detected",
  "version_files": [
    {
      "path": "Cargo.toml",
      "adapter": "toml",
      "section": "package"
    }
  ],
  "changelog_file": "CHANGELOG.md",
  "tag_pattern": "v{version}"
}
```

### Example 4: Go Module

**Project structure:**
```
/
├── go.mod
├── main.go
└── README.md
```

**Detection result:**
```json
{
  "project_type": "go",
  "config_source": "auto-detected",
  "version_files": [],
  "version_via_tags": true,
  "changelog_file": "CHANGELOG.md",
  "tag_pattern": "v{version}"
}
```

### Example 5: Monorepo

**Project structure:**
```
/
├── packages/
│   ├── lib-a/
│   │   └── package.json
│   └── lib-b/
│       └── package.json
└── README.md
```

**Detection result:**
```json
{
  "project_type": "monorepo",
  "config_source": "auto-detected",
  "monorepo": {
    "enabled": true,
    "packages": [
      "packages/lib-a",
      "packages/lib-b"
    ]
  },
  "tag_pattern": "{package}-v{version}",
  "changelog_file": "{package}/CHANGELOG.md"
}
```

### Example 6: Claude Code Plugin

**Project structure:**
```
/
├── .claude-plugin/
│   └── plugin.json
├── skills/
└── README.md
```

**Detection result:**
```json
{
  "project_type": "claude-plugin",
  "config_source": "auto-detected",
  "version_files": [
    {
      "path": ".claude-plugin/plugin.json",
      "adapter": "json",
      "field": "version"
    }
  ],
  "tag_pattern": "my-plugin-v{version}",
  "changelog_file": "CHANGELOG.md"
}
```

### Example 7: Explicit Configuration

**Project structure:**
```
/
├── .release-config.json
├── VERSION
└── README.md
```

**.release-config.json:**
```json
{
  "projectType": "generic",
  "versionFiles": ["VERSION"],
  "tagPattern": "release-{version}"
}
```

**Detection result:**
```json
{
  "project_type": "generic",
  "config_source": "explicit",
  "version_files": [
    {
      "path": "VERSION",
      "adapter": "text"
    }
  ],
  "tag_pattern": "release-{version}",
  "changelog_file": "CHANGELOG.md"
}
```

## Error Handling

**Unknown project type:**
```json
{
  "project_type": "unknown",
  "validations": {
    "errors": [
      "Could not detect project type. Please create .release-config.json with explicit configuration."
    ]
  }
}
```

**Invalid configuration:**
```json
{
  "config_source": "explicit",
  "validations": {
    "errors": [
      "Configuration file .release-config.json contains invalid JSON",
      "versionFiles[0]: 'missing.json' does not exist"
    ]
  }
}
```

**No version files found:**
```json
{
  "project_type": "generic",
  "validations": {
    "errors": [
      "No version files found. Expected one of: VERSION, version.txt, package.json"
    ]
  }
}
```

## Integration Notes

This skill is invoked by the `/release` command in Phase 1. The command will:
1. Use the detected configuration for all subsequent phases
2. Display project type and configuration to user
3. Allow user to override with `--config` argument if needed
4. Proceed with release workflow using detected/configured settings

## Reference Documentation

- [Version Adapters Reference](../../docs/version-adapters.md) - Details on reading/writing versions
- [Configuration Reference](../../docs/configuration.md) - Configuration schema and examples
