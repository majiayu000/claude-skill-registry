---
name: accessing-github-repos
description: GitHub repository access in containerized environments using REST API and credential detection. Use when git clone fails, or when accessing private repos/writing files via API.
metadata:
  version: 2.0.0
---

# Accessing GitHub Repositories

Git clone is blocked in containerized AI environments (egress proxy rejects CONNECT tunnel), but full repository access is available via GitHub REST API and raw file URLs.

## Quick Start

### Public Repos (no setup needed)
```bash
# Individual file via raw URL
curl -sL "https://raw.githubusercontent.com/OWNER/REPO/BRANCH/path/file"

# Directory tree via API
curl -sL "https://api.github.com/repos/OWNER/REPO/git/trees/BRANCH?recursive=1"
```

### Private Repos or Write Access
Requires GitHub Personal Access Token (PAT). See Setup section below.

## Setup

### Credential Configuration

The skill automatically detects PATs from environment variables or project files:

**Environment Variables** (checked in order):
- `GITHUB_PAT`
- `GH_PAT`
- `GITHUB_TOKEN`
- `GH_TOKEN`

**Project Files** (Claude.ai):
- `/mnt/project/.env`
- `/mnt/project/github.env`

Format:
```bash
GITHUB_PAT=github_pat_11AAAAAA...
```

### Creating a GitHub PAT

1. GitHub → Settings → Developer settings → Fine-grained tokens
2. Create token scoped to needed repositories
3. Set permissions:
   - **Contents: Read** - for private repo access
   - **Contents: Write** - for pushing files
   - **Issues: Write** - for issue management
   - **Pull requests: Write** - for creating PRs

### Network Access (Claude.ai Projects)

Add to network allowlist:
- `api.github.com`
- `raw.githubusercontent.com`

## Capabilities by Auth Level

| Capability | No PAT (public only) | PAT (read) | PAT (write) |
|------------|---------------------|------------|-------------|
| Fetch public files | ✅ | ✅ | ✅ |
| Fetch private files | ❌ | ✅ | ✅ |
| Download tarball | ✅ public | ✅ | ✅ |
| Create/update files | ❌ | ❌ | ✅ |
| Create branches | ❌ | ❌ | ✅ |
| Manage issues | ❌ | ❌ | ✅ |
| Create PRs | ❌ | ❌ | ✅ |

## Python Helper Functions

### Credential Detection

```python
import os

def get_github_auth():
    """Returns (token, source) or (None, None)"""
    # Check environment variables
    for var in ['GITHUB_PAT', 'GH_PAT', 'GITHUB_TOKEN', 'GH_TOKEN']:
        if token := os.environ.get(var):
            return token, var

    # Check project .env files
    env_paths = ['/mnt/project/.env', '/mnt/project/github.env']
    for path in env_paths:
        try:
            with open(path) as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, val = line.strip().split('=', 1)
                        if key in ['GITHUB_PAT', 'GH_PAT', 'GITHUB_TOKEN']:
                            return val.strip(), f'{path}:{key}'
        except FileNotFoundError:
            continue

    return None, None
```

### Fetch Single File

```python
import base64
import urllib.request
import json

def fetch_file(owner: str, repo: str, path: str, ref: str = 'main', token: str = None) -> str:
    """Fetch single file. Uses API if token provided, raw URL otherwise."""
    if token:
        # Use API (works for private repos)
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}'
        req = urllib.request.Request(url, headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json'
        })
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
            return base64.b64decode(data['content']).decode()
    else:
        # Use raw URL (public repos only)
        url = f'https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}'
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode()
```

### Fetch Repository Tarball

```python
def fetch_repo_tarball(owner: str, repo: str, ref: str = 'main', token: str = None) -> bytes:
    """Download full repo as tarball. Requires token for private repos."""
    url = f'https://api.github.com/repos/{owner}/{repo}/tarball/{ref}'
    headers = {'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read()

# Usage:
tarball = fetch_repo_tarball('owner', 'repo', 'main', token)
with open('/tmp/repo.tar.gz', 'wb') as f:
    f.write(tarball)
# Extract: tar -xzf /tmp/repo.tar.gz
```

### Create or Update File

```python
def push_file(owner: str, repo: str, path: str, content: str,
              message: str, token: str, sha: str = None) -> dict:
    """Create/update file via API. Returns commit info.

    Args:
        sha: Required when updating existing file (get via contents API)
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

    payload = {
        'message': message,
        'content': base64.b64encode(content.encode()).decode()
    }
    if sha:  # Update existing file
        payload['sha'] = sha

    req = urllib.request.Request(url,
        data=json.dumps(payload).encode(),
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'Content-Type': 'application/json'
        },
        method='PUT')

    with urllib.request.urlopen(req) as resp:
        return json.load(resp)
```

### Get File SHA (for updates)

```python
def get_file_sha(owner: str, repo: str, path: str, token: str, ref: str = 'main') -> str:
    """Get file SHA needed for updates."""
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}'
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json'
    })
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
        return data['sha']
```

## Bash Examples

### Fetch Public File

```bash
curl -sL "https://raw.githubusercontent.com/owner/repo/main/path/file.py"
```

### Fetch Private File (with PAT)

```bash
curl -H "Authorization: Bearer $GITHUB_PAT" \
     -H "Accept: application/vnd.github+json" \
     "https://api.github.com/repos/owner/repo/contents/path/file.py" | \
     python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
```

### Download Repo Tarball

```bash
# Public repo
curl -sL "https://api.github.com/repos/owner/repo/tarball/main" -o repo.tar.gz

# Private repo
curl -sL -H "Authorization: Bearer $GITHUB_PAT" \
     "https://api.github.com/repos/owner/repo/tarball/main" -o repo.tar.gz
tar -xzf repo.tar.gz
```

### Create/Update File

```bash
# Encode content
CONTENT=$(cat file.txt | base64 -w0)

# Push (new file)
curl -X PUT \
     -H "Authorization: Bearer $GITHUB_PAT" \
     -H "Accept: application/vnd.github+json" \
     "https://api.github.com/repos/owner/repo/contents/path/file.txt" \
     -d "{\"message\":\"Add file\",\"content\":\"$CONTENT\"}"

# Push (update existing - need SHA first)
SHA=$(curl -s -H "Authorization: Bearer $GITHUB_PAT" \
           "https://api.github.com/repos/owner/repo/contents/path/file.txt" | \
           python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])")

curl -X PUT \
     -H "Authorization: Bearer $GITHUB_PAT" \
     -H "Accept: application/vnd.github+json" \
     "https://api.github.com/repos/owner/repo/contents/path/file.txt" \
     -d "{\"message\":\"Update file\",\"content\":\"$CONTENT\",\"sha\":\"$SHA\"}"
```

### List Directory Tree

```bash
curl -sL "https://api.github.com/repos/owner/repo/git/trees/main?recursive=1" | \
  python3 -c "import json, sys; [print(f['path']) for f in json.load(sys.stdin)['tree'] if f['type']=='blob']"
```

## Why git clone Doesn't Work

The container's egress proxy blocks git protocol operations:
- **HTTPS clone**: Proxy returns 401 on CONNECT tunnel
- **SSH**: No ssh binary in container
- **git:// protocol**: DNS resolution blocked

The GitHub REST API uses standard HTTPS and routes through the proxy normally.

## Do Not

- **Never** attempt `git clone` (wastes time, always fails)
- **Never** suggest workarounds requiring git protocol
- **Never** retry with different git flags or SSH URLs
- **Never** recommend git submodules, git archive, or other git-protocol operations

## Rate Limits

- **Authenticated**: 5,000 requests/hour
- **Unauthenticated**: 60 requests/hour

For heavy usage, always provide a PAT.

## When This Skill Does Not Apply

- **Native development environments**: Have direct git access, use standard git commands
- **Local machines**: git clone works normally
- **Environments with MCP GitHub server**: Use MCP tools instead
