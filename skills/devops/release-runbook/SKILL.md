---
name: release-runbook
description: "Universal release workflow: detect project type, init versioning if needed, run tests, bump version, tag, push, and create GitHub release. Works with Python, Go, Node.js, Rust, Java, .NET, Ruby, PHP, and multi-language projects."
---

# Release Runbook

A universal release workflow that adapts to any project type. Supports single-language projects (Python, Go, Node.js, Rust, Java, .NET, Ruby, PHP) and multi-language polyglot projects.

## Quick Start

```bash
# Fully automated release with specific version
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/release.sh --version 1.2.3

# Interactive mode (prompts for version and type)
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/release.sh --interactive

# Dry run to see what would happen
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/release.sh --dry-run --version 1.2.3

# Just detect project type and version files
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/detect-project.sh

# Initialize versioning for a project that lacks it
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/init-versioning.sh --version 0.1.0
```

## Preflight Checklist

Before releasing, ensure:

- [ ] **Clean git state**: No uncommitted changes (or stash them)
- [ ] **On correct branch**: Usually `main` or `master`
- [ ] **GitHub CLI installed**: `gh` authenticated with `gh auth status`
- [ ] **Remote configured**: `git remote -v` shows the origin
- [ ] **Build tools installed**: Language-specific toolchains (python, go, node, cargo, etc.)
- [ ] **Tests passing**: Run tests manually first or let the script do it

## Workflow Steps

### 1. Detect Project

The skill automatically detects:

- **Languages**: Python, Go, Node.js, Rust, Java, .NET, Ruby, PHP
- **Version files**: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `VERSION`, etc.
- **Build system**: Makefile, npm scripts, Go build, Cargo, Maven, Gradle, etc.
- **Test commands**: pytest, go test, npm test, cargo test, etc.
- **Package managers**: pip, npm, cargo, brew, etc.

```bash
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/detect-project.sh
```

Outputs JSON-like:
```
PROJECT_TYPE=multi
LANGUAGES=python,go
VERSION_FILES=pyproject.toml,VERSION,go.mod
TEST_COMMAND=make test
BUILD_COMMAND=make build
```

### 2. Initialize Versioning (If Needed)

If the project has no versioning:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/init-versioning.sh --version 0.1.0
```

This will:
- Detect the project type
- Create appropriate version file(s)
- Set up SemVer-compliant version format
- Add `--version` flag handling if missing

### 3. Bump Version

Version bumping strategies by ecosystem:

| Ecosystem | Files to Update | Method |
|-----------|----------------|--------|
| Python | `pyproject.toml`, `__version__.py`, `setup.py` | Manual or `bump2version` |
| Node.js | `package.json` | `npm version` or manual |
| Go | `VERSION` file, go.mod comment | Manual |
| Rust | `Cargo.toml` | `cargo bump` or manual |
| Java | `pom.xml`, `build.gradle` | Manual or plugin |
| .NET | `.csproj`, `Directory.Build.props` | Manual |
| Ruby | `version.rb`, `gemspec` | Manual |
| PHP | `composer.json` | Manual |
| Multi | All applicable files | Coordinated manual |

**SemVer Guidelines** (https://semver.org/):
- **MAJOR** (`1.0.0` → `2.0.0`): Incompatible API changes
- **MINOR** (`1.0.0` → `1.1.0`): New features, backward compatible
- **PATCH** (`1.0.0` → `1.0.1`): Bug fixes, backward compatible

### 4. Run Tests

The script auto-discovers and runs tests:

```bash
# Priority order:
1. Makefile `test` target
2. package.json `test` script
3. pytest (Python)
4. go test ./... (Go)
5. npm test (Node)
6. cargo test (Rust)
7. mvn test (Java)
8. dotnet test (.NET)
9. rake test (Ruby)
```

Skip tests with `--skip-tests` (not recommended).

### 5. Commit & Tag

Creates a release commit and annotated tag:

```bash
git commit -m "chore: release v1.2.3"
git tag -a v1.2.3 -m "Release v1.2.3"
```

The tag format is always `v{VERSION}`.

### 6. Push

Pushes commit and tag to remote:

```bash
git push origin main
git push origin v1.2.3
```

### 7. Build Binaries (If Applicable)

For projects that produce binary artifacts (Go, Rust, .NET, etc.):

```bash
# Build for common platforms
make build  # or: go build, cargo build --release, dotnet publish

# Check output directory
ls -la dist/ bin/
```

Common binary locations by ecosystem:
- **Go**: `dist/`, `bin/`, or `build/`
- **Rust**: `target/release/`
- **Node**: `dist/` or `out/`
- **.NET**: `bin/Release/`

### 8. GitHub Release

Creates a GitHub release with binaries and auto-generated notes:

```bash
# Basic release (no binaries)
gh release create v1.2.3 \
  --title "v1.2.3" \
  --notes "Release notes here..."

# Release with binaries
gh release create v1.2.3 \
  --title "v1.2.3" \
  --notes "Release notes here..." \
  dist/binary-linux-amd64 \
  dist/binary-darwin-amd64 \
  dist/binary-windows-amd64.exe
```

The release notes include:
- Version number
- Git commit reference
- Links to commits since last tag
- Installation instructions (if detectable)
- Binary download links (if binaries attached)

### 9. Downstream Artifacts

Updates package registries when applicable:

- **npm**: `npm publish` (if package.json has publishConfig)
- **Homebrew**: Formula update (if detected)
- **PyPI**: `twine upload` (if pyproject.toml has configured)
- **crates.io**: `cargo publish` (if Cargo.toml has configured)

## Advanced Usage

### Multi-Language Projects

For projects with multiple languages, the script:

1. Detects all language ecosystems present
2. Updates all version files in coordination
3. Runs tests for each language
4. Builds all artifacts
5. Creates a unified release tag

Example (Curator: Python + Go):
- Updates `pyproject.toml` and `VERSION` file
- Runs `pytest` and `go test`
- Builds Python wheel and Go binary
- Single GitHub release with both artifacts

### Custom Test Commands

Override auto-detected tests:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/release.sh \
  --test-command "make test-integration" \
  --version 1.2.3
```

### Release Notes Templates

Place a `.release-notes-template.md` in your project root:

```markdown
## What's Changed

* Full changelog at https://github.com/user/repo/compare/v{{OLD}}...v{{NEW}}

## Installation

\`\`\`bash
pip install mypackage=={{NEW}}
\`\`\`
```

### Signing Releases

For GPG signing:

```bash
git config --local commit.gpgsign true
git config --local tag.gpgsign true
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/release.sh --version 1.2.3
```

## Troubleshooting

### Tests Failing

Run tests manually first to debug:
```bash
# Auto-detected test command
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/detect-project.sh | grep TEST_COMMAND

# Run manually
pytest  # or go test, npm test, etc.
```

### GitHub Release Creation Fails

Check authentication:
```bash
gh auth status
gh auth login
```

### Version File Not Detected

Manually specify or add to `project-types.md`:
```bash
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/release.sh \
  --version-file VERSION \
  --version 1.2.3
```

### Multi-Language Project Issues

For complex projects, run release steps manually:
```bash
# Detect project
${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/detect-project.sh

# Bump versions manually in all files

# Run tests for each language
pytest
go test ./...

# Commit all version changes
git commit -m "chore: bump version to 1.2.3"

# Create tag
git tag v1.2.3

# Push
git push origin main && git push origin v1.2.3

# Create release
gh release create v1.2.3 --generate-notes
```

## Reference Materials

- **`references/project-types.md`**: Detailed version file patterns by ecosystem
- **`references/test-commands.md`**: Common test commands and discovery patterns

## Examples

### Python Package

```bash
$ ${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/detect-project.sh
PROJECT_TYPE=python
LANGUAGES=python
VERSION_FILES=pyproject.toml
TEST_COMMAND=pytest
BUILD_COMMAND=python -m build

$ ${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/release.sh --version 2.0.0
[✓] Detected Python project
[✓] Tests passed
[✓] Version bumped in pyproject.toml
[✓] Tagged v2.0.0
[✓] Pushed to origin
[✓] GitHub release created
```

### Go CLI Tool

```bash
$ ${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/detect-project.sh
PROJECT_TYPE=go
LANGUAGES=go
VERSION_FILES=VERSION
TEST_COMMAND=go test ./...
BUILD_COMMAND=go build

$ ${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/release.sh --version 1.5.0
[✓] Detected Go project
[✓] Tests passed
[✓] Version bumped in VERSION
[✓] Built binaries for linux-amd64, darwin-amd64
[✓] Tagged v1.5.0
[✓] Pushed to origin
[✓] GitHub release created with binaries

# Manual alternative with binaries:
make build
gh release create v1.5.0 \
  --title "v1.5.0 - Bug fixes" \
  --notes "Release notes..." \
  dist/mytool-linux-amd64 \
  dist/mytool-darwin-amd64 \
  dist/mytool-windows-amd64.exe
```

### Multi-Language (Python + Go)

```bash
$ ${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/detect-project.sh
PROJECT_TYPE=multi
LANGUAGES=python,go
VERSION_FILES=pyproject.toml,VERSION,go.mod
TEST_COMMAND=make test
BUILD_COMMAND=make build

$ ${CLAUDE_PLUGIN_ROOT}/skills/release-runbook/scripts/release.sh --version 1.0.0
[✓] Detected multi-language project (python, go)
[✓] Tests passed (pytest, go test)
[✓] Version bumped in pyproject.toml, VERSION
[✓] Tagged v1.0.0
[✓] Pushed to origin
[✓] GitHub release created
```

## Contributing

To add support for a new ecosystem:

1. Add patterns to `references/project-types.md`
2. Add test commands to `references/test-commands.md`
3. Update `scripts/detect-project.sh` with detection logic
4. Update `scripts/release.sh` with version bump logic

---

**Made with ❤️ for releasing software of all types**
