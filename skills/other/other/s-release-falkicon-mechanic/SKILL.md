---
name: s-release
description: >
  Prepare and execute an addon release, including version bumping, changelog
  updates, git tagging, and validation. Use when ready to publish a new version.
  Triggers: release, version bump, changelog, git tag, publish.
---

# Releasing WoW Addons

Expert guidance for the full addon release workflow using Mechanic automation.

## Related Commands

- [c-release](../../commands/c-release.md) - Automated release workflow

## CLI Commands (Use These First)

> **MANDATORY**: Always use CLI commands before manual exploration.

| Task | Command |
|------|---------|
| Full Release | `mech release MyAddon 1.2.0 "Release message"` |
| Bump Version | `mech call version.bump -i '{"addon": "MyAddon", "version": "1.2.0"}'` |
| Add Changelog | `mech call changelog.add -i '{"addon": "MyAddon", "version": "1.2.0", "message": "..."}'` |
| Commit Changes | `mech call git.commit -i '{"addon": "MyAddon", "message": "Release 1.2.0"}'` |
| Create Tag | `mech call git.tag -i '{"addon": "MyAddon", "version": "1.2.0"}'` |

## Capabilities

1. **Full Automation** — Single-command release workflow (bump → changelog → commit → tag)
2. **Version Management** — Consistent version bumping across `.toc` files
3. **Changelog Maintenance** — Structured `CHANGELOG.md` updates with categories
4. **Git Integration** — Automated commits and annotated tags

## Routing Logic

| Request type | Load reference |
|--------------|----------------|
| Release workflow, changelog format | [../../docs/integration/release.md](../../docs/integration/release.md) |
| CLI Reference | [../../docs/cli-reference.md](../../docs/cli-reference.md) |

## Quick Reference

### The One-Command Release
```bash
# Recommended: Validates → Bumps → Changelogs → Commits → Tags
mech release MyAddon 1.2.0 "Added cooldown tracking and fixed memory leaks"
```

### Pre-Release Checklist
1. **Validate**: `mech call addon.validate -i '{"addon": "MyAddon"}'`
2. **Lint**: `mech call addon.lint -i '{"addon": "MyAddon"}'`
3. **Test**: `mech call addon.test -i '{"addon": "MyAddon"}'`
4. **Audit**: `mech call addon.deprecations -i '{"addon": "MyAddon"}'`

### Changelog Categories
- `### Added`: New features
- `### Changed`: Changes to existing features
- `### Fixed`: Bug fixes
- `### Removed`: Removed features
- `### Deprecated`: Features to be removed
- `### Security`: Security-related changes
