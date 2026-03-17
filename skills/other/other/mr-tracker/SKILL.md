---
name: mr-tracker
description: Tracks and monitors GitLab merge request activity including comments, status, and real-time updates
---

## Features

- **Comment monitoring**: Fetches and displays MR comments with file/line context
- **Real-time watching**: Watch MRs for new comments with customizable intervals
- **Status overview**: Shows MR status, approvals, and changes summary
- **Current branch detection**: Automatically finds MRs for your current branch
- **Diff context**: Shows file paths and line numbers for diff comments
- **Interactive monitoring**: Live updates with timestamp notifications

## Installation

1. Ensure you have the required dependencies:
   ```bash
   # GitLab CLI
   pip install glab
   
   # Or follow installation instructions at https://gitlab.com/gitlab-org/cli
   
   # jq for JSON processing (usually pre-installed on most systems)
   # On macOS: brew install jq
   # On Ubuntu: sudo apt-get install jq
   ```

2. Make sure the script is executable:
   ```bash
   chmod +x scripts/mr_tracker.sh
   ```

## Usage

### Show comments for a specific MR:
```bash
./scripts/mr_tracker.sh comments 123
```

### Show limited comments:
```bash
./scripts/mr_tracker.sh comments 123 5  # Show only 5 most recent comments
```

### Show MRs for current branch:
```bash
./scripts/mr_tracker.sh current
```

### Watch MR for new comments:
```bash
./scripts/mr_tracker.sh watch 123 30  # Check every 30 seconds
```

### Show MR status and summary:
```bash
./scripts/mr_tracker.sh status 123
```

### Show help:
```bash
./scripts/mr_tracker.sh help
```

## Command Reference

### `comments <mr_iid> [limit]`
Displays comments for a specific merge request with rich context including:
- Author information with username
- Creation date
- File path and line numbers for diff comments
- Comment body with truncation for long comments

### `current`
Lists all merge requests for your current git branch, showing:
- MR number and title
- Current state (opened, closed, merged)

### `watch <mr_iid> [interval]`
Monitors an MR for new comments in real-time:
- Shows initial comment count
- Checks for new comments at specified intervals (default: 60 seconds)
- Displays only new comments when detected
- Continues until interrupted with Ctrl+C

### `status <mr_iid>`
Shows comprehensive MR information:
- Title and state
- Author and branch information
- Creation and update timestamps
- Approval count and merge status
- File changes summary
- Recent comments

## Configuration

### GitLab Project
The MR tracker assumes the project path `cnty-ai/continuity`. To change this, modify the project path in `scripts/mr_tracker.sh`:

```bash
# Change this line in multiple places:
projects/cnty-ai%2Fcontinuity/merge_requests/
# To your project:
projects/your-group%2Fyour-project/merge_requests/
```

### Customizing Output
The script uses `jq` for JSON processing and formatting. You can modify the `jq` queries in the script to customize the output format.

## Examples

### Example 1: Monitor MR activity
```bash
# Watch MR #123 for new comments every 30 seconds
./scripts/mr_tracker.sh watch 123 30
```

Output:
```
👀 Watching MR #123 for new comments (checking every 30s)...
Press Ctrl+C to stop

📊 Initial comment count: 3

🆕 New comments detected! (Mon Oct 19 10:30:15 EDT 2025)
================================
🔍 DIFF COMMENT
👤 John Doe (@johndoe) - 2025-10-19
📁 File: src/components/Button.tsx
📍 Line: 45→47

Consider adding error handling for the edge case here...

─────────────────────────────────────────────────
```

### Example 2: Check current branch MRs
```bash
./scripts/mr_tracker.sh current
```

Output:
```
🔍 Looking for MRs on branch: feature/new-button
==========================================
MR #456: Add new button component (State: opened)
```

### Example 3: Get MR status
```bash
./scripts/mr_tracker.sh status 456
```

Output:
```
📊 MR #456 Status
==================
Title: Add new button component
State: opened
Author: Jane Smith
Source Branch: feature/new-button
Target Branch: main
Created: 2025-10-19T09:15:30.000Z
Updated: 2025-10-19T10:30:15.000Z
👍 Approvals: 2
🔁 Merge Status: can_be_merged
📝 Changes: 3 files, +45 -12

📝 Recent Comments:
📝 Comments for MR #456 (with file/line context):
==================================================
💬 GENERAL COMMENT
👤 John Doe (@johndoe) - 2025-10-19

Looks good! Just one suggestion...

──────────────────────────────────────────────────
```

## Troubleshooting

### Common Issues

1. **"glab command not found"**
   - Install GitLab CLI: https://gitlab.com/gitlab-org/cli
   - Authenticate: `glab auth login`

2. **"jq command not found"**
   - Install jq: `brew install jq` (macOS) or `sudo apt-get install jq` (Ubuntu)

3. **"Not in a git repository"**
   - Make sure you're in a git repository when using `current` command

4. **"No MRs found for branch"**
   - Check that you're on the correct branch
   - Verify the MR exists and targets the correct project

5. **"MR #X not found"**
   - Verify the MR number is correct
   - Check that the MR exists in the configured project

### Debug Mode

For debugging API calls, you can run glab commands directly:
```bash
glab api "projects/cnty-ai%2Fcontinuity/merge_requests/123"
```

## Contributing

To extend this tool:

1. **Add new commands**: Extend the case statement in the main script logic
2. **Customize output format**: Modify the `jq` queries for different formatting
3. **Add new project support**: Update the project path configuration
4. **Enhance monitoring**: Add additional real-time features like status changes

## License

This skill is part of the OpenCode project and follows the same license terms.