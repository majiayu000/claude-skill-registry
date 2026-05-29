---
name: oxmono-diff
description: Use when comparing modified OxCaml packages against pristine upstream, finding package sources, or understanding what changes were made to a vendored package
---

# Oxmono Diff

## Overview

`oxmono diff <package>` shows differences between pristine upstream packages and their OxCaml-adapted versions. Use this to understand what modifications were made to any package in the monorepo.

## When to Use

- Reviewing what changes were made to a package for OxCaml compatibility
- Understanding why a package differs from upstream
- Preparing to update a package to a newer upstream version
- Checking if local modifications need rebasing

## Quick Reference

```bash
# Show diff for a package
oxmono diff <package-name>

# Example
oxmono diff bytesrw
```

## Finding Package Sources

Sources are tracked in `sources.yaml` and can be found by grepping through the package directories:

```bash
# Find a package in the modified (OxCaml) directory
ls opam/<package-name>

# Find a package in the pristine upstream directory
ls sources/<package-name>

# Find packages in bleeding-edge development
ls bleeding/<package-name>

# Search for a package by partial name
ls opam/ | grep <pattern>
ls bleeding/ | grep <pattern>
```

**Directory purposes:**
- `opam/` - OxCaml-adapted packages (what gets built)
- `sources/` - Pristine upstream copies (read-only reference)
- `bleeding/` - New libraries being developed for OxCaml

## How Diff Works

1. Locates pristine source at `sources/<package>`
2. Locates modified version at `opam/<package>`
3. Runs `diff -ruN` to show unified recursive diff
4. Output shows all files that differ between upstream and local

## Common Patterns

| Task | Command |
|------|---------|
| View package diff | `oxmono diff <pkg>` |
| List all opam packages | `ls opam/` |
| List bleeding packages | `ls bleeding/` |
| Find package source URL | `grep -A5 "<pkg>:" sources.yaml` |
| Check if package exists | `ls opam/<pkg> sources/<pkg>` |
