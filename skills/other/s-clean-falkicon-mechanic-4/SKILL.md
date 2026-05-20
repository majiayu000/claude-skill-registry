---
name: s-clean
description: >
  Find and remove dead code and stale documentation. Covers unused functions,
  orphaned files, dead links, and outdated references. Use for maintenance,
  pre-release cleanup, or codebase hygiene.
  Triggers: clean, dead code, unused, orphan, stale, cruft, maintenance.
---

# Cleaning WoW Addons

Expert guidance for finding and removing cruft in addon codebases.

## Related Commands

- [c-clean](../../commands/c-clean.md) - Cleanup workflow
- [c-review](../../commands/c-review.md) - Full review (includes clean step)

## MCP Tools

| Task | MCP Tool |
|------|----------|
| Find Dead Code | `addon.deadcode(addon="MyAddon")` |
| Find Stale Docs | `docs.stale(addon="MyAddon")` |
| Filter by Confidence | `addon.deadcode(addon="MyAddon", include_suspicious=false)` |

## Capabilities

1. **Dead Code Detection** — Find unused functions, orphaned files, dead exports
2. **Stale Docs Detection** — Find broken links, outdated refs, version drift
3. **Confidence Levels** — Definite (100%), Likely (90%+), Suspicious (70%+)

## Detection Categories

### Dead Code (`addon.deadcode`)

| Category | Description |
|----------|-------------|
| `unused_function` | Functions defined but never called |
| `orphaned_file` | Lua files not in TOC |
| `dead_export` | Exported values never used |
| `unused_library` | Libraries in Libs/ never used |
| `stale_event` | Event handlers for unregistered events |
| `commented_code` | Large blocks of commented-out code |

### Stale Docs (`docs.stale`)

| Category | Description |
|----------|-------------|
| `dead_link` | Internal links to non-existent files |
| `dead_reference` | Mentions of functions/files that don't exist |
| `version_drift` | Old version numbers in documentation |
| `relative_staleness` | Docs not updated in many commits |

## Workflow

### Quick Cleanup

1. Run `addon.deadcode` with `include_suspicious=false` for high-confidence issues only
2. Remove identified dead code
3. Run `docs.stale` to find documentation issues
4. Fix broken links and update outdated references

### Deep Cleanup

1. Run `addon.deadcode` with all confidence levels
2. Manually verify suspicious findings before removal
3. Run `docs.stale` with all techniques
4. Update documentation to match current code

## Confidence Interpretation

| Level | Meaning | Action |
|-------|---------|--------|
| **Definite** | 100% certain (e.g., file not in TOC) | Safe to remove |
| **Likely** | 90%+ certain (e.g., function never called) | Review briefly, usually safe |
| **Suspicious** | 70%+ certain (e.g., dynamic code patterns) | Manual verification required |

## Best Practices

1. **Start with definite issues** — These are safe to fix immediately
2. **Check dynamic patterns** — `_G`, `rawget`, `loadstring` may hide usage
3. **Preserve intentional dead code** — Mark with `-- KEEP:` comment if needed
4. **Update docs after code changes** — Run `docs.stale` after refactoring
