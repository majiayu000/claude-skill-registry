---
name: dependency-management
description: Manage project dependencies effectively. Use when adding, updating, or auditing dependencies. Covers version management, security scanning, and lockfiles.
allowed-tools: Read, Bash, Glob, Grep
---

# Dependency Management

## Workflows

- [ ] **Audit**: Check for known vulnerabilities
- [ ] **Update**: Keep dependencies reasonably current
- [ ] **Lock**: Ensure reproducible builds
- [ ] **Minimize**: Remove unused dependencies

## Security Scanning

```bash
# Node.js
npm audit
pnpm audit

# Python
pip-audit
safety check

# Go
govulncheck ./...

# Rust
cargo audit
```

## Version Management

### Semantic Versioning
- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backward compatible
- **Patch** (0.0.1): Bug fixes, backward compatible

### Version Constraints

```json
// package.json
{
  "dependencies": {
    "exact": "1.2.3",        // Exactly 1.2.3
    "patch": "~1.2.3",       // 1.2.x (patch updates)
    "minor": "^1.2.3",       // 1.x.x (minor updates)
    "range": ">=1.2.3 <2.0.0" // Range
  }
}
```

## Lockfiles

Always commit lockfiles for reproducible builds:
- `package-lock.json` or `pnpm-lock.yaml` (Node.js)
- `poetry.lock` or `uv.lock` (Python)
- `go.sum` (Go)
- `Cargo.lock` (Rust)

## Best Practices

1. **Pin Versions in Production**: Use exact versions or lockfiles
2. **Update Regularly**: Don't let dependencies get too stale
3. **Review Changelogs**: Check breaking changes before major updates
4. **Test After Updates**: Run full test suite after dependency changes
5. **Minimize Dependencies**: Each dependency is a liability

## Removing Unused Dependencies

```bash
# Node.js
npx depcheck

# Python
pip-autoremove

# Go
go mod tidy
```
