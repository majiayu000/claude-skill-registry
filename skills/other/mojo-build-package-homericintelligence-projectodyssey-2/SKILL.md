---
name: mojo-build-package
description: "Build Mojo packages (.mojopkg files) for distribution. Use when creating distributable libraries or during packaging phase."
mcp_fallback: none
category: mojo
agent: test-engineer
user-invocable: false
---

# Mojo Build Package Skill

Build compiled Mojo packages for distribution and reuse.

## When to Use

- Creating distributable libraries
- Packaging phase of development
- Preparing for package installation
- Building modular components

## Quick Reference

```bash
# Build single package
mojo package src/tensor -o packages/tensor.mojopkg

# Build and test
./scripts/build_package.sh tensor --test

# Build all packages
./scripts/build_all_packages.sh
```

## Workflow

1. **Verify structure** - Check `__init__.mojo` exists
2. **Build package** - Run `mojo package` or script
3. **Test imports** - Verify package can be imported
4. **Verify exports** - Check `__all__` in `__init__.mojo`

## Mojo-Specific Notes

- Every package needs `__init__.mojo` entry point
- Export public API in `__all__` list
- Packages compile to `.mojopkg` binary format
- No circular dependencies allowed

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing __init__.mojo` | No package entry point | Add `__init__.mojo` to package dir |
| `Circular dependency` | Modules depend on each other | Refactor to break cycle |
| `Export not found` | Missing from `__all__` | Add name to `__all__` list |
| `Build failed` | Syntax errors in module | Fix syntax before building |

## References

- `.claude/shared/mojo-guidelines.md` - Function definition patterns
- Package metadata template: `templates/package_toml.toml`
