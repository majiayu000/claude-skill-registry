---
name: canvas-api
description: Canvas API Connection Skill
---

# Canvas API Connection Skill

Complete guide to connecting and using Canvas LMS API for Whitecliffe courses.

## Quick Reference

| Item | Value |
|------|-------|
| **User ID** | 2396 |
| **User Name** | Mohamed Abdul Latiff (Ariff) |
| **Canvas URL** | https://learn.mywhitecliffe.com |
| **MCP Server** | canvas-mcp-sse.ariff.dev |

## Current Courses (2025)

| Course | ID | Code |
|--------|-----|------|
| Applied Project | 2366 | IT8107 |
| Cybersecurity Architecture | 2368 | IT8109 |

## Connection Methods

### Method 1: Canvas MCP (Recommended)

The Canvas MCP server is already configured and provides 12 tools:

**Course Tools:**
- `get_courses` - List all enrolled courses
- `get_modules` - Get course modules

**Assignment Tools:**
- `get_assignments` - List assignments for a course
- `get_upcoming_assignments` - Next 7 days deadlines

**Grade Tools:**
- `get_grades` - Current grades for a course
- `get_submissions` - Submission details

**Discussion Tools:**
- `get_discussion_topics` - List discussions
- `get_announcements` - Course announcements

**Quiz Tools:**
- `get_quizzes` - List quizzes

#### Example Usage

```python
# Get all courses
mcp__canvas-mcp__get_courses()

# Get assignments for IT8107
mcp__canvas-mcp__get_assignments(course_id=2366)

# Check grades
mcp__canvas-mcp__get_grades(course_id=2366)

# Get upcoming deadlines
mcp__canvas-mcp__get_upcoming_assignments()
```

### Method 2: Direct API

For custom integrations or when MCP is unavailable:

**Base URL:** `https://learn.mywhitecliffe.com/api/v1`

**Authentication:**
```bash
# Store token securely (never commit!)
export CANVAS_TOKEN="your-token-here"

# API request
curl -H "Authorization: Bearer $CANVAS_TOKEN" \
     "https://learn.mywhitecliffe.com/api/v1/courses"
```

**Common Endpoints:**

| Endpoint | Description |
|----------|-------------|
| `/courses` | List courses |
| `/courses/:id/assignments` | Course assignments |
| `/courses/:id/grades` | Course grades |
| `/courses/:id/modules` | Course modules |
| `/users/self/upcoming_events` | Upcoming events |

### Method 3: Python SDK

```python
from canvasapi import Canvas

API_URL = "https://learn.mywhitecliffe.com"
API_KEY = os.environ.get("CANVAS_TOKEN")

canvas = Canvas(API_URL, API_KEY)
user = canvas.get_current_user()
courses = user.get_courses(enrollment_state='active')
```

## Setup Instructions

### Adding Canvas MCP to Claude

Already configured in `mcp-config.json`:

```json
{
  "mcpServers": {
    "canvas-mcp": {
      "type": "sse",
      "url": "https://canvas-mcp-sse.ariff.dev/sse"
    }
  }
}
```

### Getting API Token

1. Log in to https://learn.mywhitecliffe.com
2. Go to Account → Settings
3. Scroll to "Approved Integrations"
4. Click "+ New Access Token"
5. Set expiry (recommended: end of semester)
6. Copy token immediately (shown only once)

### Storing Token Securely

**macOS Keychain:**
```bash
security add-generic-password -a "$USER" -s "canvas-api" -w "YOUR_TOKEN"
```

**Environment variable:**
```bash
# Add to ~/.zshrc
export CANVAS_TOKEN="$(security find-generic-password -a "$USER" -s "canvas-api" -w)"
```

## Important Notes

⚠️ **Always verify with MCP tools** - Don't assume course/assignment details

⚠️ **Token security** - Never commit tokens to git

⚠️ **Rate limits** - Canvas has API rate limits, batch requests when possible

⚠️ **Course IDs change** - Each semester has new course IDs

## Troubleshooting

**"Unauthorized" errors:**
- Token expired - generate new one
- Token revoked - check Canvas settings

**MCP not responding:**
- Check https://canvas-mcp-sse.ariff.dev/health
- Verify mcp-config.json syntax

**Missing courses:**
- Check enrollment status
- Some courses may be unpublished
