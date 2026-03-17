---
name: github-actions-versions
description: Use when writing or updating GitHub Actions workflow files (.github/workflows/*.yml) - provides latest version tags for official and popular third-party actions to avoid using outdated versions

---

# GitHub Actions Versions

## Overview

Always use the latest major version tags when referencing GitHub Actions in workflow files.

## Quick Reference

Fetch latest versions:

```
https://ramblurr.github.io/actions-latest/versions.txt
```

Returns a list of `owner/repo@version` for:
- Official GitHub Actions (actions/checkout, actions/setup-node, etc.)
- Popular third-party actions (docker/build-push-action, tailscale/github-action, DeterminateSystems/nix-installer-action, etc.)

## Usage

Before writing `uses:` lines in workflow files, fetch the URL above to get current versions. Use WebFetch or curl to retrieve the list.
