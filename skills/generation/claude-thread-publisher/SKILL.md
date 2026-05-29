---
name: claude-thread-publisher
description: >
  Publish Claude Code conversation threads as static HTML pages hosted on GitHub Gists,
  with shareable gistpreview links. Use when the user asks to share, publish, or delete
  a Claude Code thread.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(python:*)
---

# Claude Thread Publisher

Publish Claude Code conversation threads as beautiful static HTML pages hosted on GitHub Gists, with shareable permalinks via gistpreview.github.io.

## Instructions

### When to Use This Skill

Use this skill when the user asks to:
- Publish, share, or export a Claude Code conversation
- Create a shareable link for the current thread
- Delete a previously published thread
- Update an existing published thread

### High-Level Workflow

#### Publishing a Thread

When the user wants to publish the current thread:

1. **Check for GitHub Token**:
   - Look for existing token in `~/.claude/thread-publisher/config.json`
   - If missing, guide the user to create a GitHub PAT with `gist` scope
   - Store the token locally for future use

2. **Locate Current Session**:
   - Use `session_locator.py` to find the current Claude Code session JSONL file
   - Handle cases where no session is found gracefully

3. **Generate Content**:
   - Use `render_thread.py` to convert JSONL to:
     - Beautiful static HTML (`index.html`)
     - Normalized thread JSON (`thread.json`)
     - Metadata (`metadata.json`)

4. **Publish to Gist**:
   - Use `publish_to_gist.py` to create/update GitHub Gist with the three files
   - Use secret gists by default for privacy
   - Store mapping of thread hash → gist ID in local index

5. **Provide Result**:
   - Return the gistpreview permalink (e.g., `https://gistpreview.github.io/?abcdef1234...`)
   - Also provide the raw Gist URL for reference
   - Include brief confirmation and reminder that the link is live

#### Deleting a Published Thread

When the user wants to delete a published thread:

1. **Locate Current Thread**:
   - Use `session_locator.py` + `render_thread.py` to compute the current thread's hash
   - Look up the thread hash in the local index (`~/.claude/thread-publisher/index.json`)

2. **Verify and Delete**:
   - If mapping exists, use `delete_gist.py` to delete the corresponding GitHub Gist
   - Remove the entry from the local index
   - Confirm successful deletion to the user

3. **Handle Missing Threads**:
   - If no mapping exists, inform the user that no published link was found
   - Offer to list all published threads if they want to check

#### Updating a Published Thread

When the user wants to update an existing published thread:

1. **Detect Changes**:
   - Compute current thread hash and compare with stored version
   - If hash differs, the thread has been updated since last publication

2. **Update Strategy**:
   - By default, update the existing Gist (replace contents)
   - This preserves the same permalink URL
   - Update the local index with new timestamp

3. **Provide Updated Link**:
   - Return the same permalink (URL unchanged)
   - Confirm that the content has been updated

### Script Usage Patterns

#### Session Location
```bash
python scripts/session_locator.py --mode current
```
Returns JSON with session file path and project information.

#### Thread Rendering
```bash
python scripts/render_thread.py \
  --input /path/to/session.jsonl \
  --output-html /tmp/thread.html \
  --output-json /tmp/thread.json \
  --metadata /tmp/metadata.json \
  --project-path /current/project \
  --session-file /path/to/session.jsonl
```

#### Gist Publishing
```bash
python scripts/publish_to_gist.py \
  --html /tmp/thread.html \
  --thread-json /tmp/thread.json \
  --metadata /tmp/metadata.json \
  --project-path /current/project \
  --session-file /path/to/session.jsonl
```

#### Gist Deletion
```bash
python scripts/delete_gist.py \
  --thread-hash <hash>  # or --session-file /path/to/session.jsonl
```

## Key Features

### HTML Rendering
- Beautiful dark theme optimized for code display
- Responsive design that works on mobile and desktop
- Syntax highlighting for code blocks
- Clear separation between user, assistant, and system messages
- One-click "copy link" functionality
- Metadata display (thread hash, generation time, message count)

### GitHub Integration
- Uses GitHub Personal Access Tokens with `gist` scope only
- Creates secret (private) gists by default for privacy
- Supports both creation and updates of gists
- Maintains local index for tracking published threads
- Graceful handling of authentication and API errors

### Thread Management
- Content-based hashing to detect thread changes
- Supports re-publishing updated threads
- Comprehensive deletion capabilities
- Orphaned gist cleanup functionality

## File Structure

```
claude-thread-publisher/
├── SKILL.md                    # This file
├── examples.md                 # Example prompts
├── scripts/
│   ├── session_locator.py      # Find current Claude Code session
│   ├── render_thread.py        # Convert JSONL to HTML/JSON
│   ├── publish_to_gist.py      # Create/update GitHub Gists
│   └── delete_gist.py          # Delete Gists and manage cleanup
└── templates/                  # (reserved for future HTML templates)
```

## Configuration

The skill stores configuration in `~/.claude/thread-publisher/`:

- `config.json`: GitHub token and preferences
- `index.json`: Mapping of thread hashes to Gist IDs

### Example Configuration
```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx",
  "gists_private_by_default": true
}
```

### Example Index Entry
```json
{
  "threads": {
    "a1b2c3d4e5f6...": {
      "gist_id": "abcdef1234567890...",
      "gist_url": "https://gist.github.com/abcdef1234567890...",
      "last_published_at": "2024-01-01T12:00:00Z",
      "project_path": "/home/user/my-project",
      "session_file": "/home/user/.claude/projects/abc/sessions/def.jsonl",
      "title": "Implement user authentication feature"
    }
  }
}
```

## Security and Privacy

- **Local Token Storage**: GitHub PAT is stored locally on user's machine only
- **Gist Privacy**: Creates secret (private) gists by default
- **Content Control**: Only publishes the specific thread content user requests
- **No External Services**: Relies only on GitHub's official Gist API
- **Token Scope**: Requires only `gist` scope (minimal permission)

## Error Handling

- **Missing Session**: Gracefully handles cases where no current session can be found
- **Authentication Issues**: Guides users through PAT setup when missing
- **API Failures**: Provides clear error messages for GitHub API issues
- **File I/O Errors**: Handles file permission and path issues gracefully
- **Network Issues**: Implements timeouts and retry logic where appropriate

## Troubleshooting

### Common Issues

1. **"No session file found"**
   - User may be in a directory without a Claude Code project
   - Check if `~/.claude/projects/` exists and contains relevant project
   - Try explicitly specifying session file path

2. **"GitHub token required"**
   - User needs to create a PAT at github.com/settings/tokens
   - Token must have `gist` scope
   - Token will be stored locally after first use

3. **"Gist creation failed"**
   - Check GitHub API status
   - Verify token has correct permissions
   - Check network connectivity

4. **"Thread hash mismatch"**
   - Thread content has changed since last publication
   - This is normal when updating threads
   - Skill will handle updating the gist

## Examples

### Basic Publishing
> "Publish this Claude Code conversation as a shareable link."

### Updating
> "Update the published link for this thread with the new messages."

### Deleting
> "Delete the public link you created for this conversation."

### Listing
> "Show me all the threads I've published."

## Dependencies

- Python 3.7+
- `requests` library for HTTP requests
- Standard library modules: `json`, `pathlib`, `datetime`, `argparse`, `hashlib`

## Best Practices

- Always confirm with user before deleting published content
- Use descriptive thread titles based on first user message
- Keep gists private by default to respect user privacy
- Provide both gistpreview permalink and direct gist URL
- Maintain local index for thread management
- Handle API errors gracefully with user-friendly messages
