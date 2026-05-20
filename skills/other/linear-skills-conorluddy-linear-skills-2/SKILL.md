---
name: linear-skills
version: 1.0.0
description: Lightweight Linear skill for fetching issue details. Returns only essential data (title, description, state, assignee) to optimize context usage compared to full Linear MCP.
---

# Linear Get Issue Skill

Fetch Linear issue details by ID with minimal context overhead.

## Quick Start

```bash
# Set up your Linear API key
export LINEAR_API_KEY="your_api_key_here"

# Search for issues by keyword
python scripts/search_issues.py "filtering"

# Get full details of a specific issue
python scripts/get_issue.py LUDDY-320

# Get JSON output for parsing
python scripts/get_issue.py LUDDY-320 --json
```

## Available Scripts

### Two-Part Workflow: Search + Get

**Search** to find issues, then **Get** full details of the one you want.

### search_issues.py - Find issues

Search Linear issues by keywords in title, description, or ID.

**Usage:**
```bash
python scripts/search_issues.py <query> [--limit N] [--json]
```

**Arguments:**
- `<query>` - Search term (e.g., "filtering", "exercise", "bug")

**Options:**
- `--limit N` - Max results (default: 10)
- `--json` - Output as JSON
- `--help` - Show help

**Output (default - compact list):**
```
Found 3 issue(s):

1. LUDDY-320 - Filtering System - Progressive Disclosure UX
   Status: In Progress | Assignee: Unassigned | Team: LUDDY

2. LUDDY-321 - FilterChip and FilterChipGroup Atoms
   Status: Backlog | Assignee: Unassigned | Team: LUDDY

3. LUDDY-323 - Filter Logic & State Management
   Status: Backlog | Assignee: Unassigned | Team: LUDDY
```

**Then use the identifier from search results with get_issue.py**

---

### get_issue.py - Fetch issue details

Retrieve full Linear issue details including title, description, state, assignee, team, and labels.

**Usage:**
```bash
python scripts/get_issue.py <issue-id> [--json]
```

**Arguments:**
- `<issue-id>` - Linear issue identifier (e.g., `ENG-123`, `DES-45`)

**Options:**
- `--json` - Output as JSON (for parsing in scripts)
- `--help` - Show help message

**Output (default - human readable):**
```
ENG-123: Fix login bug
Status: In Progress
Priority: High
Assignee: John Doe (john@example.com)
Team: Engineering
Labels: bug, p1

Description:
Users unable to login with SSO on mobile Safari. Started after
the recent auth middleware update.

URL: https://linear.app/workspace/issue/ENG-123/...
Created: 2024-12-15
Updated: 2024-12-16
```

**Output (--json):**
```json
{
  "id": "issue_uuid",
  "identifier": "ENG-123",
  "title": "Fix login bug",
  "description": "Users unable to login...",
  "state": {
    "name": "In Progress",
    "type": "started"
  },
  "priority": "High",
  "assignee": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "team": {
    "name": "Engineering",
    "key": "ENG"
  },
  "labels": [
    {"name": "bug", "color": "#ff0000"}
  ],
  "url": "https://linear.app/...",
  "created_at": "2024-12-15T10:30:00",
  "updated_at": "2024-12-16T14:22:00"
}
```

## Environment Setup

1. Get your Linear API key from Settings > API in your Linear workspace
2. Copy `.env.example` to `.env` in the skill directory:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   LINEAR_API_KEY=your_api_key_here
   ```

**Alternative:** Export directly without `.env`:
```bash
export LINEAR_API_KEY="your_api_key_here"
```

**Note:** The script checks for `.env` in:
1. Skill directory (`.claude/skills/linear-skills/.env`)
2. Project root (fallback)
3. Current working directory (fallback)

## Requirements

- Python 3.9+
- Linear API key (get from workspace Settings > API)
- **Zero external dependencies** - uses only Python stdlib (urllib, json, argparse)

## Installation

No dependencies to install! Just set up your `.env` file and run.

## Why This Skill?

The full Linear MCP can be context-heavy when you only **read** issues. This lightweight skill:

**Benefits:**
- **Zero Dependencies**: Pure Python stdlib
- **Lightweight**: Direct GraphQL queries, minimal overhead
- **Read-Only**: Perfect for lookups and searching
- **Optimized Output**: 3-7 lines by default, JSON on demand
- **Context Efficient**: Saves significant tokens vs full Linear MCP
- **Fast**: No SDK initialization, direct API calls

**When to use this skill:**
- Searching for issues by keyword
- Getting issue details and status
- Quick lookups without modifying anything
- Reducing context overhead

**When to use the full Linear MCP instead:**
- Creating new issues
- Updating status, assignees, labels, or milestones
- Adding comments or attachments
- Complex workflows that require write access

## Examples

**Get issue and see description:**
```bash
python scripts/get_issue.py ENG-123
```

**Parse issue data in a script:**
```bash
python scripts/get_issue.py ENG-123 --json | jq '.description'
```

**Use with Claude Code:**
Simply ask: "Get issue ENG-123" and this skill will be invoked automatically.

---

Use these scripts directly or let Claude Code invoke them automatically when your request matches the skill description.
