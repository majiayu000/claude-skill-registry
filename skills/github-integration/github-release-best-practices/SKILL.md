---
name: github-release-best-practices
description: Systematic approach to GitHub release preparation following 2025 best practices for Rust workspace projects
audience: maintainers
workflow: github
---
# GitHub Release Best Practices

Systematic approach to GitHub release preparation following 2025 best practices for Rust workspace projects.

## Purpose

Establish comprehensive release management procedures for Rust workspaces with multiple crates, ensuring professional-grade releases with proper versioning, changelog management, and quality gate enforcement.

## 2025 GitHub Release Best Practices

### Immutable Releases (New in 2025)

**What it is**: GitHub's supply chain security feature that locks releases after publication.

**Key Benefits**:
- Assets cannot be added, modified, or deleted after publishing
- Release tags are protected and cannot be moved
- Cryptographic attestations enable verification
- Protects against post-release tampering

**Implementation Strategy**:
```bash
# Draft-first approach for immutable releases
gh release create v0.1.8 --draft
# Review content, attach assets, then publish
gh release edit v0.1.8 --publish
```

### Auto-Generated Release Notes

**Features**:
- Lists merged pull requests automatically
- Identifies and lists contributors
- Provides links to full changelog
- Customizable via `.github/release.yml` configuration

**Configuration Example** (`.github/release.yml`):
```yaml
changelog:
  exclude:
    labels:
      - ignore-for-release
      - dependencies
    authors:
      - dependabot
  categories:
    - title: 🚀 New Features
      labels:
        - feature
        - enhancement
    - title: 🐛 Bug Fixes
      labels:
        - bug
        - fix
    - title: 📚 Documentation
      labels:
        - documentation
        - docs
    - title: 🔧 Other Changes
      labels:
        - "*"
```

**Best Practice**: Use auto-generation as starting point, then always review and refine before publishing. Recent implementations show 90% reduction in effort (2-3 hours → 15 minutes review time).

## Automated Changelog Generation from Git History

### Git Command Strategies

**Analyze Changes Since Last Release**:
```bash
# Get commits since last release
git log v0.1.7..HEAD --oneline --decorate

# Group commits by type using conventional commits
git log --grep="^feat|^fix|^docs|^chore|^refactor" v0.1.7..HEAD

# Generate commit summary with PR references
git log v0.1.7..HEAD --pretty=format:"- %s (%h)" --abbrev-commit
```

**Extract PR Information**:
```bash
# Get PR numbers from commit messages
git log v0.1.7..HEAD --grep="#[0-9]" --pretty=format:"- %s (Closes %h)"

# Extract breaking changes
git log v0.1.7..BREAKING --pretty=format:"- **BREAKING**: %s"
```

### Keep a Changelog Format Implementation

**Required Structure**:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Feature X for use case Y

### Changed
- Improved performance of Z

## [0.1.8] - 2025-12-28

### Fixed
- Resolved clippy warning in premem_integration_test.rs
- Fixed unnecessary_unwrap pattern in test code

### Changed
- Improved error messages in integration tests
- Inlined format arguments in semantic_summary_test.rs

### Added
- GOAP execution plan documentation
```

**Categories (in order)**:
1. **Added** - New features
2. **Changed** - Changes to existing functionality  
3. **Deprecated** - Features planned for removal
4. **Removed** - Removed features
5. **Fixed** - Bug fixes
6. **Security** - Security vulnerability patches

## Version Bump Strategies for Rust Workspaces

### Semantic Versioning Decision Matrix

| Change Type | Version Bump | Example | Rationale |
|-------------|--------------|---------|-----------|
| Breaking Changes | MAJOR | 0.1.7 → 1.0.0 | Public API changes |
| New Features | MINOR | 0.1.7 → 0.2.0 | Backward-compatible additions |
| Bug Fixes | PATCH | 0.1.7 → 0.1.8 | Backward-compatible fixes |
| CI/Quality | PATCH | 0.1.7 → 0.1.8 | Infrastructure improvements |
| Documentation | PATCH | 0.1.7 → 0.1.8 | Non-functional changes |

### Workspace Version Coordination

**Root Cargo.toml Management**:
```toml
[workspace.package]
version = "0.1.8"  # Single source of truth

[workspace.members]
# All members inherit workspace.package version
```

**Version Validation**:
```bash
# Check version consistency across workspace
cargo metadata --format-version 1 --no-deps | \
  jq '.packages[] | select(.name != "rust-self-learning-memory") | {name, version}'

# Validate all crates have consistent versions
cargo workspaces version --all
```

### Special Considerations for 0.x Versions

**During 0.x Development**:
- "Anything MAY change at any time"
- "The public API SHOULD NOT be considered stable"
- Standard semver guarantees are relaxed
- Typically increment MINOR (0.1.x → 0.2.0) for most changes
- PATCH reserved for critical bug fixes only

## Release Validation Workflows

### Pre-Release Quality Gates

**CI/CD Validation**:
```bash
# Run comprehensive quality checks
./scripts/quality-gates.sh

# Specific validations
cargo fmt --check
cargo clippy --all -- -D warnings
cargo test --all
cargo audit
cargo deny check
```

**Coverage Requirements**:
- Maintain >90% test coverage across all modules
- Zero clippy warnings with strict linting
- All GitHub Actions workflows passing
- Security audit clean with no known vulnerabilities

### Release Creation Validation

**Git Tag Management**:
```bash
# Create annotated tag with release message
git tag -a v0.1.8 -m "Release v0.1.8 - CI fixes and code quality improvements"

# Verify tag creation
git show v0.1.8

# Push tag to trigger release workflow
git push origin v0.1.8
```

**GitHub Release Validation**:
```bash
# Create release with auto-generated notes
gh release create v0.1.8 \
  --title "v0.1.8 - CI Fixes and Code Quality" \
  --notes "See CHANGELOG.md for details"

# Verify release creation
gh release view v0.1.8 --json tagName,createdAt,url
```

## Release Note Templates and Examples

### Patch Release Template (v0.X.Y)

```markdown
## Summary
This patch release resolves critical bugs, improves code quality, and enhances CI/CD reliability. All changes are backward-compatible.

## Fixed
- **Clippy Warnings**: Resolved `unnecessary_unwrap` lint in premem_integration_test.rs by refactoring to use proper match patterns
- **Performance Tests**: Fixed type conversion compilation error in performance.rs
- **Release Workflow**: Corrected asset upload failure by updating action version

## Changed
- Improved error messages in integration tests (replaced `.unwrap()` with `.expect()`)
- Inlined format arguments in semantic_summary tests for improved readability
- Enforced warnings-as-errors consistently across all CI workflows

## Added
- GOAP execution plan documentation for complex workflows
- Response validation test suite for memory-mcp server

## Technical Details
- All GitHub Actions workflows passing (Quick Check, Performance Benchmarks, Security, CodeQL)
- Zero clippy warnings with -D warnings enforcement
- Test coverage maintained at 92.5%
- Performance targets exceeded across all metrics

## Full Changelog
https://github.com/d-o-hub/rust-self-learning-memory/compare/v0.1.7...v0.1.8
```

### Minor Release Template (v0.X.0)

```markdown
## Summary
This minor release introduces new features and enhancements while maintaining backward compatibility. Key highlights include multi-provider embeddings, improved security, and performance optimizations.

## Added
- **Multi-Provider Embeddings**: Support for OpenAI, Cohere, Ollama, and local CPU embeddings
- **Configuration Caching**: Reduced API calls through intelligent caching
- **Wasmtime Sandbox**: 6-layer defense-in-depth security architecture
- **Vector Search Optimization**: Improved similarity search performance

## Changed
- **[BREAKING]** Migrated from bincode to postcard for serialization
- Performance improvements: 10-100x faster than baselines
- Enhanced security with zero clippy warnings across all crates
- Improved cache hit rates with new configuration caching

## Breaking Changes
- **Serialization Format**: Existing redb databases must be recreated
  - Postcard format is incompatible with previous bincode format
  - See migration guide for step-by-step instructions
  - Postcard provides better security guarantees

## Performance
- Episode Creation: 19,531x faster (~2.5 µs vs 50ms target)
- Step Logging: 17,699x faster (~1.1 µs vs 20ms target)
- Memory Retrieval: 138x faster (~721 µs vs 100ms target)

## Security
- **Postcard Serialization**: Safer than bincode, preventing deserialization attacks
- **Wasmtime Sandbox**: 6-layer defense-in-depth security
- **Zero Clippy Warnings**: Enforced strict linting across all code

## Migration Guide
1. **Backup existing data**: Export redb databases before upgrading
2. **Update dependencies**: Update to latest versions of dependencies
3. **Recreate databases**: Postcard format requires fresh database creation
4. **Verify functionality**: Run test suite to ensure compatibility

## Statistics
- Test Pass Rate: 99.3% (424/427 tests passing)
- Test Coverage: 92.5% across all modules
- Rust Source Files: 367 files with ~44,250 LOC
- Workspace Members: 8 crates

## Full Changelog
https://github.com/d-o-hub/rust-self-learning-memory/compare/v0.1.7...v0.2.0
```

## Release Workflow Automation

### Complete Release Script

```bash
#!/bin/bash
# release-workflow.sh - Complete release automation

set -e

RELEASE_VERSION=$1
if [ -z "$RELEASE_VERSION" ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 0.1.8"
    exit 1
fi

echo "🚀 Starting release workflow for v$RELEASE_VERSION"

# 1. Quality Gates
echo "📋 Running quality gates..."
./scripts/quality-gates.sh

# 2. Update changelog
echo "📝 Updating CHANGELOG.md..."
# Implementation depends on changelog tool selection

# 3. Commit changelog
echo "💾 Committing changelog..."
git add CHANGELOG.md
git commit -m "docs(changelog): update for v$RELEASE_VERSION"

# 4. Create and push tag
echo "🏷️ Creating git tag v$RELEASE_VERSION..."
git tag -a "v$RELEASE_VERSION" -m "Release v$RELEASE_VERSION"
git push origin "v$RELEASE_VERSION"

# 5. Create GitHub release
echo "🎉 Creating GitHub release..."
gh release create "v$RELEASE_VERSION" \
  --title "v$RELEASE_VERSION - [Auto-generated]" \
  --notes "See CHANGELOG.md for detailed changes" \
  --draft

echo "✅ Release workflow completed!"
echo "Next: Review release draft at https://github.com/d-o-hub/rust-self-learning-memory/releases"
```

### CI/CD Integration

**Release Workflow Configuration** (`.github/workflows/release.yml`):
```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          components: cargo, clippy, rustfmt
       
      - name: Run quality gates
        run: ./scripts/quality-gates.sh
       
      - name: Create release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          VERSION=${GITHUB_REF#refs/tags/}
          gh release create "$VERSION" \
            --title "Release $VERSION" \
            --notes-file CHANGELOG.md \
            --draft
```

## Integration with Opencode Agents

This skill provides foundational knowledge for:
- **github-release-best-practices** agent: Orchestrates complete release workflows
- **goap-agent**: Handles complex multi-phase release coordination
- **testing-qa**: Validates release quality gates and compliance
- **code-reviewer**: Assesses pre-release code quality and standards
- **security**: Performs security audits and vulnerability assessments

The skill complements agent capabilities by providing reusable procedures, templates, and best practices that agents can leverage and enhance based on specific project requirements.