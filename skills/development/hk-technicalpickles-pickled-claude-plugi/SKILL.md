---
name: hk
description: Use when hk.pkl exists in project, hook output shows hk running, or working with git hooks in hk-managed projects. Also use when setting up, configuring, or troubleshooting hk git hooks.
---

# hk - Git Hook Manager

## Overview

hk is a fast git hook manager by jdx (author of mise). Uses pkl configuration language. Provides 90+ built-in linters.

**Docs:** https://hk.jdx.dev/
**GitHub:** https://github.com/jdx/hk

## Detection

Identify which hook manager a project uses:

| File | Hook Manager |
|------|--------------|
| `hk.pkl` | hk |
| `lefthook.yml` | lefthook |
| `.husky/` directory | husky |
| `.pre-commit-config.yaml` | pre-commit (python) |

## Key Commands

```bash
hk init              # Create initial hk.pkl
hk install           # Set up git hooks
hk check             # Run checks manually (read-only)
hk fix               # Auto-fix issues
hk builtins          # List available builtins
hk validate          # Validate config
hk config dump       # Show effective configuration
```

## Core Concepts

- **Hooks:** Git hook types (pre-commit, commit-msg, pre-push)
- **Steps:** Named units of work within hooks
- **Builtins:** Pre-configured linters (90+) via `Builtins.pkl`
- **Profiles:** Enable/disable groups of steps (`--profile slow`)

## Configuration

When editing hk.pkl, read `hk-pkl-reference.md` in this skill directory for structure and examples.

## Built-in Linters

When looking up builtins, read `builtins-reference.md` in this skill directory. Or run `hk builtins` for the live list.

## Finding Help

**Stable reference:** Read the reference files in this skill directory when needed.

**Latest docs:**
```bash
npx @mdream/crawl https://hk.jdx.dev/ --output /tmp/hk-docs
```

**GitHub issues:**
```bash
gh issue list -R jdx/hk                    # List open issues
gh search issues --repo jdx/hk "error"     # Search issues
gh issue view 123 -R jdx/hk                # View specific issue
```

## Troubleshooting

**Hook not running:**
```bash
hk install        # Reinstall hooks
cat .git/hooks/pre-commit  # Verify hook calls hk
```

**Step skipped:**
```bash
hk check -v       # Verbose output shows skip reasons
hk config dump    # Check effective configuration
```

**Validate config:**
```bash
hk validate       # Check hk.pkl syntax
```
