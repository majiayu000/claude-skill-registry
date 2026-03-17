---
name: plugin-release-checker
description: Validate plugin content quality before release. Run skill-validator across plugins, verify marketplace.json completeness, check plugin.json version consistency, and detect broken documentation cross-references. Use when preparing a release, before running release.sh, or when user mentions "release check", "pre-release", "plugin-release-checker", or "release validation".
argument-hint: [--plugin <name>] [--all]
---

# Plugin Release Checker

Pre-release content quality gate that complements `scripts/release.sh`. Run before generating the changelog or triggering the release workflow.

## Quick Start

Run the validation script to check all plugins:

```bash
scripts/check_release_readiness.py --all
```

Check a specific plugin:

```bash
scripts/check_release_readiness.py --plugin core
```

## Release Workflow Integration

```
/plugin-release-checker   ← THIS: validates plugin content quality
    ↓ (all checks pass)
/changelog                ← generates CHANGELOG entry
    ↓
./scripts/release.sh X.Y.Z  ← handles git tag + GitHub Release
```

## Checks Performed

| Check | Description |
|-------|-------------|
| **Skill Validation** | Run skill-validator across all skills in each plugin |
| **Marketplace Sync** | Verify all plugins in `plugins/` have entries in marketplace.json |
| **Version Consistency** | Check plugin.json versions match CHANGELOG entries |
| **Cross-References** | Detect broken links in SKILL.md → WORKFLOW.md, EXAMPLES.md, etc. |
| **Required Files** | Ensure each plugin has plugin.json and README.md |
| **Frontmatter** | Validate YAML frontmatter in agents, commands, and skills |

## Output

```
=== Plugin Release Readiness Report ===

Plugin: core (v2.0.0)
  ✓ All skills pass validation
  ✓ Marketplace entry found
  ✓ Version consistent with CHANGELOG
  ✓ No broken cross-references

Plugin: git (v1.0.0)
  ✗ Skill 'creating-commit': 1 error (SS002: SKILL.md exceeds 500 lines)
  ✓ Marketplace entry found
  ✓ Version consistent with CHANGELOG
  ✓ No broken cross-references

Summary: 9/10 plugins ready, 1 plugin has issues
```

## Command Options

```bash
--all                    # Check all plugins (default)
--plugin NAME            # Check specific plugin
--skip-skill-validator   # Skip skill-validator (faster, less thorough)
--format {text,json}     # Output format
```
