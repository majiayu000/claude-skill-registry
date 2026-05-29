---
name: specstory-project-stats
description: Fetch project statistics from SpecStory Cloud. Run when user says "get project stats", "show SpecStory stats", "project statistics", "how many sessions", or "SpecStory metrics".
license: Apache-2.0
metadata:
  author: SpecStory, Inc.
  version: "1.0.0"
allowed-tools: Bash(node *)
---

# SpecStory Project Stats

Fetches project statistics from SpecStory's cloud platform, showing contributor counts, session activity, and other project metrics.

## How It Works

1. **Identifies** the project via `.specstory/.project.json`, git remote, or folder name
2. **Calls** the SpecStory Cloud API
3. **Returns** project statistics in JSON format
4. **Presents** the data in a readable summary

## Prerequisites

- Project must be synced to SpecStory Cloud
- Node.js must be available to run the script

## Usage

### Slash Command

| User says | Action |
|-----------|--------|
| `/specstory-project-stats` | Fetch stats for current project |
| `/specstory-project-stats` | Same as above (no arguments needed) |

### Direct Script Usage

```bash
# Fetch stats for current project
node skills/specstory-project-stats/scripts/get-stats.js

# With custom API endpoint (for development)
SPECSTORY_API_URL=http://localhost:5173 node skills/specstory-project-stats/scripts/get-stats.js
```

## Output

The script outputs JSON with project statistics:

```json
{
  "project_id": "specstoryai/agent-skills",
  "sessions": {
    "total": 156,
    "last_30_days": 47,
    "last_7_days": 12
  },
  "contributors": {
    "total": 5,
    "active_last_30_days": 3
  },
  "activity": {
    "first_session": "2025-10-15",
    "last_session": "2026-01-28",
    "avg_sessions_per_week": 8.2
  }
}
```

## Project ID Resolution

The script determines project ID in this order:

1. **`.specstory/.project.json`** - Uses `git_id` or `workspace_id` field
2. **Git remote** - Extracts repo name from `origin` remote URL
3. **Folder name** - Falls back to current directory name

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 404 | Project not found | Project needs to sync to SpecStory Cloud first |
| 401 | Unauthorized | API endpoint may require authentication |
| Network error | Can't reach API | Check internet connection |

## Present Results to User

After fetching stats, present them in a friendly format:

### Example Response (success)

```
Here are the stats for **specstoryai/agent-skills**:

**Sessions**
- Total: 156 sessions captured
- Last 30 days: 47 sessions
- Last 7 days: 12 sessions

**Contributors**
- Total: 5 contributors
- Active recently: 3

**Activity**
- First session: October 15, 2025
- Most recent: January 28, 2026
- Average: ~8 sessions per week

Your project has been actively using AI-assisted coding!
```

### Example Response (404 error)

```
This project doesn't exist on SpecStory Cloud yet.

To get started:
1. Make sure you have SpecStory installed
2. Run `specstory sync` to push your local sessions to the cloud
3. Try this command again

Need help? Check the docs at https://docs.specstory.com
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SPECSTORY_API_URL` | `https://cloud.specstory.com` | API endpoint |

## Notes

- Statistics are fetched from SpecStory Cloud, not local history
- Project must have synced sessions to show meaningful stats
- The API is public and doesn't require authentication for basic stats
