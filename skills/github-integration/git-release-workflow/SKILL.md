---
name: git-release-workflow
description: Execute git commit, tag, and push operations with configurable patterns for any project type
user-invocable: false
---

# Git Release Workflow

## Purpose

Executes the git operations for a release: running pre-release hooks, staging modified files, creating a commit with proper formatting and attribution, creating an annotated git tag with configurable patterns, and running post-release hooks. Works with any project type.

## Input Context

Requires:
- **Project Configuration**: Output from `detect-project-type` skill
- **Version**: New version string (e.g., "1.2.0")
- **Commit Message**: Pre-formatted commit message (from changelog-update skill)
- **Files to Stage**: List of modified files to include in commit

## Workflow

### 1. Load Configuration

Use configuration from `detect-project-type`:
- `tag_pattern` - Pattern for git tag (e.g., "v{version}", "{package}-v{version}")
- `tag_message` - Message template for annotated tag
- `commit_message_template` - Template for commit message
- `pre_release_hook` - Script to run before git operations (optional)
- `post_release_hook` - Script to run after successful push (optional)

### 2. Run Pre-Release Hook

If `preReleaseHook` is configured, execute it before any git operations:

```bash
if [ -n "$pre_release_hook" ]; then
  echo "Running pre-release hook: $pre_release_hook"

  if [ -x "$pre_release_hook" ]; then
    # Run hook and capture output
    if ! hook_output=$($pre_release_hook 2>&1); then
      # Hook failed - abort release
      echo "✗ Pre-release hook failed:"
      echo "$hook_output"
      exit 1
    else
      echo "✓ Pre-release hook succeeded"
      echo "$hook_output"
    fi
  else
    echo "⚠️  Pre-release hook not executable: $pre_release_hook"
    exit 1
  fi
fi
```

**Common pre-release hook use cases:**
- Run tests: `npm test`, `cargo test`, `go test ./...`
- Build project: `npm run build`, `cargo build --release`
- Run linters: `npm run lint`, `cargo clippy`
- Generate documentation: `npm run docs`
- Validate package: `npm pack --dry-run`, `twine check dist/*`

### 3. Stage Modified Files

Stage all files that were modified during the release process:

```bash
git add {file1} {file2} {file3} ...
```

**Files typically include:**
- Version configuration files (plugin.json, marketplace.json, variants.json)
- Changelog files (CHANGELOG.md)
- Documentation files (README.md)

Verify staging succeeded:
```bash
git status --short
```

### 2. Create Commit

Create commit with the provided message, ensuring proper formatting and attribution:

```bash
git commit -m "$(cat <<'EOF'
{commit-message}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

**Commit message format:**
```
Release {scope} v{version}

{changelog-body}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Important:** Use heredoc (`<<'EOF'`) to preserve formatting and handle multi-line messages correctly.

Capture commit hash:
```bash
git rev-parse HEAD
```

### 5. Create Annotated Git Tag

Create an annotated tag (not lightweight) using configurable pattern from configuration:

**Build tag name from pattern:**
```bash
# Get pattern from config (e.g., "v{version}", "{package}-v{version}")
tag_pattern="v{version}"  # from config

# Replace placeholders
tag_name="${tag_pattern//\{version\}/$new_version}"

# For monorepo/plugins, also replace {package}
if [[ "$tag_pattern" == *"{package}"* ]]; then
  tag_name="${tag_name//\{package\}/$package_name}"
fi

# Examples:
# Pattern: "v{version}" → Tag: "v1.2.0"
# Pattern: "release-{version}" → Tag: "release-1.2.0"
# Pattern: "{package}-v{version}" → Tag: "my-lib-v1.2.0"
```

**Build tag message from template:**
```bash
# Get template from config (default: "Release v{version}")
tag_message_template="Release v{version}"  # from config

# Replace placeholders
tag_message="${tag_message_template//\{version\}/$new_version}"
tag_message="${tag_message//\{package\}/$package_name}"

# Example: "Release v1.2.0"
```

**Create tag:**
```bash
git tag -a "$tag_name" -m "$tag_message"
```

**Verify tag created:**
```bash
if git tag -l "$tag_name" | grep -q "$tag_name"; then
  echo "✓ Created tag: $tag_name"
else
  echo "✗ Failed to create tag: $tag_name"
  exit 1
fi
```

### 4. Prepare Push Information

Do NOT automatically push. Instead, prepare information for the command to display:

```bash
# Get remote URL
git remote get-url origin

# Get current branch
git branch --show-current

# Show what will be pushed
git log origin/{branch}..HEAD --oneline
```

Return push command for user to execute:
```bash
git push origin {branch} --follow-tags
```

Or if using `--force-with-lease` after rebase:
```bash
git push origin {branch} --follow-tags --force-with-lease
```

### 6. Run Post-Release Hook (After Push)

**Note:** This section is executed by the `/release` command AFTER successful push, not within this skill.

If `postReleaseHook` is configured, execute it after git push succeeds:

```bash
if [ -n "$post_release_hook" ]; then
  echo "Running post-release hook: $post_release_hook"

  if [ -x "$post_release_hook" ]; then
    # Run hook and capture output
    if ! hook_output=$($post_release_hook 2>&1); then
      # Hook failed - warn but don't abort (release already pushed)
      echo "⚠️  Post-release hook failed:"
      echo "$hook_output"
      # Continue anyway - release is already public
    else
      echo "✓ Post-release hook succeeded"
      echo "$hook_output"
    fi
  else
    echo "⚠️  Post-release hook not executable: $post_release_hook"
  fi
fi
```

**Common post-release hook use cases:**
- Publish package: `npm publish`, `cargo publish`, `twine upload dist/*`
- Deploy to CDN/hosting: `netlify deploy`, `vercel --prod`
- Send notifications: `./scripts/notify-slack.sh`, `./scripts/post-to-discord.sh`
- Update documentation site: `./scripts/deploy-docs.sh`
- Trigger CI/CD: `curl -X POST $CI_WEBHOOK_URL`
- Create GitHub release: `gh release create $TAG_NAME`

### 7. Generate Summary

Collect information for post-release summary:
- Commit hash (short: first 7 characters)
- Tag name
- Files committed (count)
- Current branch
- Remote URL (if configured)

## Output Format

Return:

```
{
  "commit_hash": "a1b2c3d",
  "commit_hash_full": "a1b2c3d4e5f6g7h8i9j0",
  "tag_name": "daily-carry-v1.2.0",
  "files_committed": [
    "plugins/daily-carry/.claude-plugin/plugin.json",
    "plugins/daily-carry/CHANGELOG.md",
    ".claude-plugin/marketplace.json"
  ],
  "files_count": 3,
  "branch": "master",
  "remote_url": "https://github.com/jayteealao/agent-skills.git",
  "push_command": "git push origin master --follow-tags",
  "success": true
}
```

## Examples

### Example 1: Plugin Release

**Input:**
- Scope: `plugin:daily-carry`
- Version: `1.2.0`
- Commit message:
  ```
  Release plugin:daily-carry v1.2.0

  Added:
  - New deployment command

  Fixed:
  - Git push error handling

  Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
  ```
- Files: `["plugins/daily-carry/.claude-plugin/plugin.json", "plugins/daily-carry/CHANGELOG.md", ".claude-plugin/marketplace.json"]`

**Operations:**
```bash
# Stage files
git add plugins/daily-carry/.claude-plugin/plugin.json
git add plugins/daily-carry/CHANGELOG.md
git add .claude-plugin/marketplace.json

# Create commit
git commit -m "$(cat <<'EOF'
Release plugin:daily-carry v1.2.0

Added:
- New deployment command

Fixed:
- Git push error handling

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Create tag
git tag -a "daily-carry-v1.2.0" -m "Release plugin:daily-carry v1.2.0"
```

**Output:**
```
{
  "commit_hash": "f7e8d9c",
  "commit_hash_full": "f7e8d9c6b5a4e3d2c1b0a9f8e7d6c5b4",
  "tag_name": "daily-carry-v1.2.0",
  "files_committed": [
    "plugins/daily-carry/.claude-plugin/plugin.json",
    "plugins/daily-carry/CHANGELOG.md",
    ".claude-plugin/marketplace.json"
  ],
  "files_count": 3,
  "branch": "master",
  "remote_url": "https://github.com/jayteealao/agent-skills.git",
  "push_command": "git push origin master --follow-tags",
  "success": true
}
```

### Example 2: Marketplace Release

**Input:**
- Scope: `marketplace`
- Version: `1.1.0`
- Files: `[".claude-plugin/marketplace.json", "CHANGELOG.md", "README.md"]`

**Tag created:** `marketplace-v1.1.0`

**Output:**
```
{
  "commit_hash": "b4c5d6e",
  "tag_name": "marketplace-v1.1.0",
  "files_count": 3,
  "branch": "master",
  "push_command": "git push origin master --follow-tags",
  "success": true
}
```

### Example 3: Variants Release

**Input:**
- Scope: `variants`
- Version: `2.0.0`
- Files: `["variants/variants.json", "variants/CHANGELOG.md"]`

**Tag created:** `variants-v2.0.0`

## Error Handling

### Git Add Failure

**Error:** File doesn't exist or permission denied

**Response:**
```
{
  "success": false,
  "error": "Failed to stage files",
  "details": "git add failed: {error-message}",
  "suggestion": "Verify files exist and are writable"
}
```

### Git Commit Failure

**Error:** Nothing to commit, commit hook failed, etc.

**Response:**
```
{
  "success": false,
  "error": "Failed to create commit",
  "details": "{git-error-message}",
  "suggestion": "Check git status and pre-commit hooks"
}
```

**Rollback:** If commit fails, unstage files:
```bash
git reset HEAD
```

### Git Tag Failure

**Error:** Tag already exists, invalid tag name, etc.

**Response:**
```
{
  "success": false,
  "error": "Failed to create tag",
  "details": "{git-error-message}",
  "commit_hash": "f7e8d9c",
  "suggestion": "Tag may already exist. Use 'git tag -d {tag}' to delete or choose different version"
}
```

**Rollback:** Offer to undo commit:
```bash
git reset --soft HEAD~1
```

### No Remote Configured

**Warning:** (non-blocking)

**Response:**
```
{
  "success": true,
  "commit_hash": "f7e8d9c",
  "tag_name": "daily-carry-v1.2.0",
  "remote_url": null,
  "push_command": null,
  "warning": "No git remote configured - cannot push"
}
```

## Integration Notes

This skill is invoked by the `/release` command in Phase 6. The command will:
1. Execute git operations via this skill
2. Display commit hash and tag name
3. Prompt user to push with provided command
4. If user confirms, execute push:
   ```bash
   git push origin {branch} --follow-tags
   ```
5. Proceed to Phase 7 for verification

## Git Best Practices

- **Always use annotated tags** (`-a` flag) for releases (contains metadata)
- **Use heredoc for multi-line commit messages** to preserve formatting
- **Include Co-Authored-By** for attribution when Claude assists
- **Use `--follow-tags`** when pushing to include annotated tags
- **Never force push** unless explicitly requested and using `--force-with-lease`
- **Verify operations** after each git command (check status, verify tag exists)

## Linear History Maintenance

To maintain linear git history:
- Commit directly to master/main (no merge commits)
- If on feature branch, rebase onto master first
- Use fast-forward merges only
- Avoid `git merge --no-ff`
