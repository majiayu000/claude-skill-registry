---
name: githubbing
description: GitHub CLI (gh) installation and authenticated operations in Claude.ai containers. Use when user needs to create issues, PRs, view repos, or perform GitHub operations beyond raw API calls.
metadata:
  version: 1.1.1
  requires: configuring
---

# Githubbing

Install and use GitHub CLI (`gh`) for authenticated GitHub operations.

## 1. Install

```bash
bash /path/to/githubbing/scripts/install-gh.sh
```

## 2. Configure Authentication

`gh` reads tokens from `GH_TOKEN` or `GITHUB_TOKEN` environment variables.

```python
from configuring import get_env
import os

token = get_env("GH_TOKEN") or get_env("GITHUB_TOKEN")
if token:
    os.environ["GH_TOKEN"] = token
```

## 3. Verify

```bash
gh auth status
```
