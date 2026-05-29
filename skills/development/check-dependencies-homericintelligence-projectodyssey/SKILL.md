---
name: check-dependencies
description: "Validate and verify dependencies are available and compatible. Use when setting up environments."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Check Dependencies

Verify that required dependencies are installed and compatible with the project requirements.

## When to Use

- Setting up development environment
- Validating CI/CD environment configuration
- Troubleshooting import errors
- Checking version compatibility

## Quick Reference

```bash
# Check Python dependencies
pip check

# Verify specific package versions
pip show package_name

# Validate pixi environment
pixi info
pixi task list
```

## Workflow

1. **List requirements**: Identify all declared dependencies (pixi.toml, requirements.txt)
2. **Verify installation**: Check that all packages are installed and importable
3. **Check versions**: Confirm version constraints are met
4. **Test imports**: Actually import modules to detect hidden issues
5. **Report status**: Document any missing or incompatible dependencies

## Output Format

Dependency validation report:

- All declared dependencies listed
- Installation status (installed/missing)
- Installed version vs required version
- Compatibility status (compatible/incompatible)
- Issues found (if any)

## References

- See CLAUDE.md > Environment Setup for Pixi configuration
- See `extract-dependencies` skill for dependency extraction
- See pixi.toml in repository root for project dependencies
