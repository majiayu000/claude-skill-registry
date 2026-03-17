---
name: invoking-github
description: Enables GitHub repository operations (read/write/commit/PR) for Claude.ai chat environments. Use when users request GitHub commits, repository updates, DEVLOG persistence, or cross-session state management via GitHub branches. Not needed in Claude Code (has native git access).
metadata:
  version: 0.0.3
---

# Invoking GitHub

Programmatically interact with GitHub repositories from Claude.ai chat: read files, commit changes, create PRs, and persist state across sessions.

## When to Use This Skill

**Primary use cases:**
- Commit code/documentation from Claude.ai chat (mobile/web)
- Auto-persist DEVLOG.md for iterating skill
- Manage state across sessions via GitHub branches
- Read and update repository files programmatically
- Create pull requests from chat interface

**Trigger patterns:**
- "Commit this to the repository"
- "Update the README on GitHub"
- "Save this to a feature branch"
- "Create a PR with these changes"
- "Persist DEVLOG to GitHub"
- "Read the config file from my repo"

**Not needed for:**
- Claude Code environments (use native git commands)
- Read-only repository access (use GitHub UI or API directly)

## Quick Start

### Prerequisites

Create a GitHub Personal Access Token and add to Project Knowledge:

1. Go to https://github.com/settings/tokens
2. Create new token (classic or fine-grained)
3. Required scopes: `repo` (or `public_repo` for public repos only)
4. In Claude.ai, add to Project Knowledge:
   - Title: `GITHUB_API_KEY`
   - Content: Your token (e.g., `ghp_abc123...`)

### Single File Commit

```python
from invoking_github import commit_file

result = commit_file(
    repo="username/repo-name",
    path="README.md",
    content="# Updated README\n\nNew content here...",
    branch="main",
    message="Update README with new instructions"
)

print(f"Committed: {result['commit_sha']}")
```

### Read File

```python
from invoking_github import read_file

content = read_file(
    repo="username/repo-name",
    path="config.json",
    branch="main"
)

print(content)
```

### Batch Commit (Multiple Files)

```python
from invoking_github import commit_files

files = [
    {"path": "src/main.py", "content": "# Python code..."},
    {"path": "README.md", "content": "# Updated docs..."},
    {"path": "tests/test.py", "content": "# Tests..."}
]

result = commit_files(
    repo="username/repo-name",
    files=files,
    branch="feature-branch",
    message="Add new feature implementation",
    create_branch_from="main"  # Create branch if it doesn't exist
)

print(f"Committed {len(files)} files: {result['commit_sha']}")
```

### Create Pull Request

```python
from invoking_github import create_pull_request

pr = create_pull_request(
    repo="username/repo-name",
    head="feature-branch",
    base="main",
    title="Add new feature",
    body="## Changes\n- Implemented feature X\n- Updated docs\n- Added tests"
)

print(f"PR created: {pr['html_url']}")
```

## Core Functions

### `read_file()`

Read a file from repository:

```python
read_file(
    repo: str,           # "owner/name"
    path: str,           # "path/to/file.py"
    branch: str = "main" # Branch name
) -> str
```

**Returns**: File content as string
**Raises**: `GitHubAPIError` if file not found or access denied

### `commit_file()`

Commit a single file (create or update):

```python
commit_file(
    repo: str,                      # "owner/name"
    path: str,                      # "path/to/file.py"
    content: str,                   # New file content
    branch: str,                    # Target branch
    message: str,                   # Commit message
    create_branch_from: str = None  # Create branch from this if doesn't exist
) -> dict
```

**Returns**: Dict with `commit_sha`, `branch`, `file_path`
**Raises**: `GitHubAPIError` on conflicts or auth failures

### `commit_files()`

Commit multiple files in a single commit:

```python
commit_files(
    repo: str,                      # "owner/name"
    files: list[dict],              # [{"path": "...", "content": "..."}]
    branch: str,                    # Target branch
    message: str,                   # Commit message
    create_branch_from: str = None  # Create branch from this if doesn't exist
) -> dict
```

**Returns**: Dict with `commit_sha`, `branch`, `files_committed`
**Raises**: `GitHubAPIError` on failures

**Note**: Uses Git Trees API for efficiency - atomic commit of all files.

### `create_pull_request()`

Create a pull request:

```python
create_pull_request(
    repo: str,      # "owner/name"
    head: str,      # Source branch (your changes)
    base: str,      # Target branch (where to merge)
    title: str,     # PR title
    body: str = ""  # PR description (supports markdown)
) -> dict
```

**Returns**: Dict with `number`, `html_url`, `state`
**Raises**: `GitHubAPIError` if branches invalid or PR exists

## Credential Configuration

This skill requires a GitHub Personal Access Token. Two configuration methods:

### Method 1: Project Knowledge (Recommended)

Best for Claude.ai chat users (mobile/web):

1. Create token at https://github.com/settings/tokens
2. In Claude.ai Project settings → Add to Project Knowledge
3. Create document titled `GITHUB_API_KEY`
4. Paste your token as content

**Permissions required**:
- Classic token: `repo` scope
- Fine-grained token: Repository permissions → Contents (read/write) and Pull requests (read/write)

### Method 2: API Credentials Skill (Fallback)

Alternatively, use combined credentials file:

1. Create `API_CREDENTIALS.json` in project knowledge
2. Add: `{"github_api_key": "ghp_your-token-here"}`

## Integration with Iterating Skill

Auto-persist DEVLOG.md to GitHub for cross-session continuity:

```python
# In your DEVLOG update function
from invoking_github import commit_file
from pathlib import Path

def update_devlog_with_sync(data, repo="user/project", branch="devlog"):
    """Update DEVLOG.md locally and sync to GitHub"""

    # Update local DEVLOG
    update_devlog(data)  # Your existing function

    # Auto-sync to GitHub
    try:
        devlog_content = Path("DEVLOG.md").read_text()

        result = commit_file(
            repo=repo,
            path="DEVLOG.md",
            content=devlog_content,
            branch=branch,
            message=f"DEVLOG: {data['title']}",
            create_branch_from="main"
        )

        print(f"✓ DEVLOG synced to GitHub ({repo}:{branch})")
        return result

    except Exception as e:
        print(f"⚠ DEVLOG sync failed: {e}")
        # Continue anyway - local DEVLOG.md still updated
        return None
```

**Benefits:**
- Automatic backup of session progress
- Cross-device access to development logs
- Git history of decisions and progress
- No manual copy/paste to Project Knowledge

See [references/iterating-integration.md](references/iterating-integration.md) for complete patterns.

## Error Handling

All functions raise `GitHubAPIError` with descriptive messages:

```python
from invoking_github import commit_file, GitHubAPIError

try:
    result = commit_file(
        repo="user/repo",
        path="file.py",
        content="...",
        branch="main",
        message="Update"
    )
except GitHubAPIError as e:
    if e.status_code == 404:
        print("Repository or branch not found")
    elif e.status_code == 401:
        print("Authentication failed - check your token")
    elif e.status_code == 403:
        print("Access denied - check token permissions")
    elif e.status_code == 409:
        print("Conflict - file was modified since last read")
    else:
        print(f"GitHub API error: {e}")
```

**Common errors:**
- **404**: Repository, branch, or file not found
- **401/403**: Invalid token or insufficient permissions
- **409**: Merge conflict (file changed concurrently)
- **422**: Validation error (invalid branch name, etc.)
- **Rate limit**: Too many requests (wait before retrying)

## Best Practices

1. **Use descriptive commit messages**
   - Bad: "Update files"
   - Good: "Add authentication middleware and update user routes"

2. **Batch commits when possible**
   - Use `commit_files()` for related changes
   - Single atomic commit = cleaner git history

3. **Create feature branches**
   - Don't commit directly to main
   - Use `create_branch_from="main"` parameter
   - Create PR for review

4. **Handle errors gracefully**
   - Always wrap in try-except
   - Provide fallback behavior
   - Don't fail silently

5. **Secure token management**
   - Use fine-grained tokens with minimal scopes
   - Set expiration dates
   - Rotate regularly
   - Never commit tokens to repositories

## Advanced Usage

### Conditional Commits

Only commit if file content changed:

```python
from invoking_github import read_file, commit_file, GitHubAPIError

try:
    current_content = read_file(repo, path, branch)
    if current_content != new_content:
        commit_file(repo, path, new_content, branch, "Update file")
    else:
        print("No changes detected, skipping commit")
except GitHubAPIError as e:
    if e.status_code == 404:
        # File doesn't exist, create it
        commit_file(repo, path, new_content, branch, "Create file")
    else:
        raise
```

### Session-Specific Branches

Avoid conflicts with unique branch names:

```python
import datetime

session_id = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
branch_name = f"devlog-{session_id}"

commit_file(
    repo="user/project",
    path="DEVLOG.md",
    content=devlog_content,
    branch=branch_name,
    message="Session progress",
    create_branch_from="main"
)
```

### Multi-Repository Workflows

Work across multiple repos:

```python
repos = ["user/frontend", "user/backend", "user/docs"]

for repo in repos:
    commit_file(
        repo=repo,
        path="VERSION",
        content="2.0.0\n",
        branch="release-2.0",
        message="Bump version to 2.0.0"
    )
```

## Limitations

- **Target environment**: Claude.ai chat only (not Claude Code)
- **No OAuth**: Must use Personal Access Tokens manually
- **No git operations**: Pure REST API (no clone, pull, rebase, etc.)
- **File size**: GitHub API limits ~100MB per file
- **Rate limits**: 5000 requests/hour for authenticated users
- **Network required**: All operations require internet access

## See Also

- [references/api-reference.md](references/api-reference.md) - Detailed API documentation
- [references/credential-setup.md](references/credential-setup.md) - Step-by-step credential guide
- [references/iterating-integration.md](references/iterating-integration.md) - DEVLOG auto-sync patterns
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and solutions
- [GitHub REST API Docs](https://docs.github.com/rest) - Official GitHub API reference

## Token Efficiency

This skill uses ~800 tokens when loaded but provides essential GitHub operations for claude.ai chat environments where native git access isn't available. Enables persistent state management and cross-session workflows.
