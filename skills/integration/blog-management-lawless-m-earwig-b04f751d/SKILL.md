---
name: Blog Management
description: Managing Cyril's Workshop blog posts and devblog via API - creating, editing, publishing, and updating content programmatically
---

# Blog Management

This skill enables programmatic management of blog posts on steponnopets.net, including both the main Cyril blog and the devblog. Use this skill when the user asks to edit, update, or fix published blog posts.

## Instructions

When the user requests blog post edits or updates, follow these guidelines:

1. **Identify the Target Post**: Determine which post to edit from the user's request (by slug, "latest", or content description)

2. **Read API Key**: Always read the API key from `~/.claude/cyril-api-key` before making API calls

3. **Fetch Current Content**: GET the post to see current state before making changes

4. **Make Targeted Updates**: Only PATCH the fields that need to change (title, content, tags, or publish status)

5. **Confirm Success**: Report the update with the post URL so the user can verify

6. **Handle Both Blogs**: DevBlog is at `/devblog/api`, main Cyril blog is at `/cyril/api`

## Examples

### Example 1: Fix a Typo
```
User: Fix the typo in the admin panel post, change 'teh' to 'the'

Claude: I'll fetch the post, fix the typo, and update it:
- Read API key from ~/.claude/cyril-api-key
- Fetch post content from /devblog/api/posts
- Find the post about admin panel
- Replace 'teh' with 'the' in the content
- PATCH the updated content back

[Uses the PATCH Update pattern from reference material below]

Updated post "admin-panel-and-tag-filtering": https://steponnopets.net/devblog/#/post/admin-panel-and-tag-filtering
```

### Example 2: Update a Link
```
User: In the latest devblog post, change the repo link to https://github.com/lawless-m/Robocyril

Claude: I'll update the GitHub link in the most recent post:
- Fetch all posts from /devblog/api/posts
- Identify the latest by published_at timestamp
- Update the GitHub URL in the content
- PATCH just the content field

[Uses the PATCH Update pattern from reference material below]
```

### Example 3: Add Tags
```
User: Add 'automation' and 'admin' tags to the post about the admin panel

Claude: I'll update the tags for that post:
- Find the admin panel post by searching titles/slugs
- Get current tags array
- Add 'automation' and 'admin' to the array
- PATCH just the tags field

[Uses the PATCH Update pattern from reference material below]
```

### Example 4: Change Title
```
User: Change the title of the post 'old-slug' to 'Better New Title'

Claude: I'll update the title while keeping the same slug:
- Fetch post by slug 'old-slug'
- PATCH with new title only
- Note: Slug stays the same (it's the identifier)

[Uses the PATCH Update pattern from reference material below]
```

---

# Reference Implementation Details

The sections below contain working patterns and exact API formats for managing blog posts.

## API Endpoints

### DevBlog
- Base URL: `https://steponnopets.net/devblog`
- Get all posts: `GET /devblog/api/posts`
- Get with drafts: `GET /devblog/api/posts?include_drafts=true` (requires auth)
- Get single post: `GET /devblog/api/post?slug=<slug>`
- Create post: `POST /devblog/api/posts`
- Update post: `PATCH /devblog/api/post?slug=<slug>`
- Delete post: `DELETE /devblog/api/post?slug=<slug>`

### Cyril's Workshop (Main Blog)
- Base URL: `https://steponnopets.net/cyril`
- Same API structure as DevBlog, just replace `/devblog/` with `/cyril/`

## Authentication Pattern

**Location**: `~/.claude/cyril-api-key`
**Purpose**: Authenticate all write operations

All POST, PATCH, and DELETE requests require:

```bash
-H "X-Cyril-Key: $(cat ~/.claude/cyril-api-key)"
```

**Key Points**:
- API key is stored as single line with no newline
- Same key works for both Cyril blog and DevBlog
- GET requests for published posts don't need auth
- GET with `?include_drafts=true` requires auth

## GET Posts Pattern

**Purpose**: Fetch current post content before editing

**Get all published posts:**
```bash
curl https://steponnopets.net/devblog/api/posts
```

**Get single post by slug:**
```bash
curl "https://steponnopets.net/devblog/api/post?slug=my-post-slug"
```

**Response format:**
```json
{
  "slug": "post-title",
  "title": "Post Title",
  "content": "# Markdown content...",
  "tags": ["rust", "web"],
  "repo": "https://github.com/user/repo",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "published_at": "2025-01-15T10:30:00Z"
}
```

**Key Points**:
- Drafts have `published_at = null`
- Tags are JSON array
- Slugs are auto-generated from titles (lowercase, hyphens)
- Slugs cannot be changed after creation

## PATCH Update Pattern

**Purpose**: Update specific fields of an existing post

**ALWAYS use this exact pattern:**

```bash
curl -X PATCH "https://steponnopets.net/devblog/api/post?slug=<slug>" \
  -H "Content-Type: application/json" \
  -H "X-Cyril-Key: $(cat ~/.claude/cyril-api-key)" \
  -d '{
    "content": "# Updated content..."
  }'
```

**All fields are optional** - only include what you want to update:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Update post title (slug stays same) |
| `content` | string | Update full markdown content |
| `tags` | array | Replace all tags (["tag1", "tag2"]) |
| `publish` | boolean | `true` to publish, `false` to unpublish |

**Example updating multiple fields:**
```bash
curl -X PATCH "https://steponnopets.net/devblog/api/post?slug=my-post" \
  -H "Content-Type: application/json" \
  -H "X-Cyril-Key: $(cat ~/.claude/cyril-api-key)" \
  -d '{
    "title": "New Title",
    "tags": ["rust", "svelte", "automation"],
    "publish": true
  }'
```

**Key Points**:
- Only send fields you want to change
- Slug in URL identifies the post
- Slug cannot be modified
- Returns updated post on success

## POST Create Pattern

**Purpose**: Create a new blog post (usually done via `/blog` command)

**Format:**
```bash
curl -X POST https://steponnopets.net/cyril/api/posts \
  -H "Content-Type: application/json" \
  -H "X-Cyril-Key: $(cat ~/.claude/cyril-api-key)" \
  -d '{
    "title": "Post Title",
    "content": "# Markdown content here...",
    "repo": "https://github.com/user/repo",
    "tags": ["® RepoName", "rust", "web"],
    "publish": true
  }'
```

**Response:**
```json
{
  "slug": "post-title",
  "url": "https://steponnopets.net/cyril/#/post/post-title"
}
```

**Key Points**:
- For GitHub repos, first tag MUST be project tag: `® RepoName`
- Project tag auto-creates/updates project on Projects page
- Set `"publish": false` to save as draft
- Slug is auto-generated from title

## DELETE Pattern

**Purpose**: Delete a blog post

```bash
curl -X DELETE "https://steponnopets.net/devblog/api/post?slug=my-post-slug" \
  -H "X-Cyril-Key: $(cat ~/.claude/cyril-api-key)"
```

**Key Points**:
- Requires authentication
- Permanent deletion
- No undo available

## Database Schema

Posts are stored in SQLite at `/var/www/data/devblog.db` and `/var/www/data/cyril.db`:

```sql
CREATE TABLE posts (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  tags TEXT,  -- JSON array: ["tag1", "tag2"]
  repo TEXT,
  created_at TEXT,
  updated_at TEXT,
  published_at TEXT  -- NULL for drafts
)
```

## Project Tags System

**Purpose**: Auto-create project entries from blog posts

When a post has a project tag (`® ProjectName`) as the **first tag**:
- A project entry is auto-created/updated in the database
- The project description is extracted from the first paragraph of the post
- The project links to the GitHub repo specified in `repo` field
- Clicking the project tag shows all posts for that project

**Example:**
```json
{
  "title": "Building Robocyril Admin Panel",
  "tags": ["® Robocyril", "rust", "svelte"],
  "repo": "https://github.com/lawless-m/Robocyril",
  "content": "This post describes building an admin panel.\n\nMore details..."
}
```

Creates/updates project:
- **Name**: Robocyril
- **Description**: "This post describes building an admin panel."
- **URL**: https://github.com/lawless-m/Robocyril

## Common Request Patterns

When the user makes these requests, use these patterns:

| User Request | Action | Fields to PATCH |
|-------------|--------|-----------------|
| "Fix typo X to Y" | Search & replace in content | `content` |
| "Add tag Z" | Append to tags array | `tags` |
| "Change title to X" | Replace title | `title` |
| "Update GitHub link" | Replace URL in content | `content` |
| "Unpublish post X" | Set publish to false | `publish` |
| "Publish draft X" | Set publish to true | `publish` |

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 404 | Post not found | Verify slug, check if post exists |
| 401 | Invalid API key | Check ~/.claude/cyril-api-key contents |
| 400 | Invalid JSON | Verify JSON syntax in request |
| 500 | Server error | Check vsprod logs |

## Admin Panel Reference

Web-based admin available at `https://steponnopets.net/devblog/#/admin`:
- View all posts (including drafts)
- Edit post content, title, tags in modal editor
- Publish/unpublish posts
- Delete posts
- Manage projects
- Requires API key authentication

## Best Practices

1. **Always fetch before updating** - GET the current content first to avoid overwriting unintended fields
2. **PATCH only what changed** - Don't send all fields, just the ones being updated
3. **Preserve existing data** - When updating tags, include existing tags plus new ones
4. **Confirm with URL** - Always return the post URL after updating so user can verify
5. **Handle drafts carefully** - Check `published_at` to distinguish drafts from published posts
