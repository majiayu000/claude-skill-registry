---
name: gitea-wiki
description: Manage Gitea wiki pages. Use when working with wiki content, creating documentation, or updating wiki pages.
version: 1.0.0
---

# Gitea Wiki Manager

## Overview

Manage Gitea wiki pages using MCP tools. Wiki content is base64 encoded - use shell commands to decode/encode, avoiding large base64 strings in LLM context.

## MCP Tools Reference

### mcp__gitea__list_wiki_pages
List all wiki pages in a repository.

**Parameters:**
- `owner` (required): repository owner
- `repo` (required): repository name

**Response:** Array of page objects with `title`, `sub_url`

---

### mcp__gitea__get_wiki_page
Get wiki page content and metadata.

**Parameters:**
- `owner` (required): repository owner
- `repo` (required): repository name
- `pageName` (required): wiki page name

**Response:**
```json
{
  "title": "Home",
  "sub_url": "Home",
  "content_base64": "IyBIb21lCg==",  // <-- base64 encoded content
  "commit_count": 5,
  "last_commit": {...}
}
```

---

### mcp__gitea__create_wiki_page
Create a new wiki page.

**Parameters:**
- `owner` (required): repository owner
- `repo` (required): repository name
- `title` (required): page title
- `content_base64` (required): page content as base64
- `message` (optional): commit message

---

### mcp__gitea__update_wiki_page
Update an existing wiki page.

**Parameters:**
- `owner` (required): repository owner
- `repo` (required): repository name
- `pageName` (required): current page name
- `content_base64` (required): new content as base64
- `title` (optional): new page title
- `message` (optional): commit message

---

### mcp__gitea__delete_wiki_page
Delete a wiki page.

**Parameters:**
- `owner` (required): repository owner
- `repo` (required): repository name
- `pageName` (required): page name to delete

---

### mcp__gitea__get_wiki_revisions
Get revision history of a wiki page.

**Parameters:**
- `owner` (required): repository owner
- `repo` (required): repository name
- `pageName` (required): wiki page name

## Workflows

### Reading a Wiki Page

```
Step 1: Call MCP tool
        mcp__gitea__get_wiki_page(owner="user", repo="myrepo", pageName="Home")

Step 2: Response contains content_base64 field
        Extract the base64 string from response

Step 3: Decode using Bash (NOT in LLM context)
        echo "<content_base64_value>" | base64 -d > /tmp/wiki-page.md

Step 4: Read decoded file
        Use Read tool on /tmp/wiki-page.md
```

### Creating a Wiki Page

```
Step 1: Write content to temp file
        Use Write tool to create /tmp/new-page.md with content

Step 2: Encode to base64 using Bash
        base64 < /tmp/new-page.md | tr -d '\n'

Step 3: Call MCP tool with base64 output
        mcp__gitea__create_wiki_page(
          owner="user",
          repo="myrepo",
          title="API Docs",
          content_base64="<output_from_step_2>"
        )
```

### Updating a Wiki Page

```
Step 1: Get current content
        mcp__gitea__get_wiki_page(owner="user", repo="myrepo", pageName="Home")

Step 2: Decode to temp file
        echo "<content_base64>" | base64 -d > /tmp/edit-page.md

Step 3: Edit the temp file
        Use Edit tool on /tmp/edit-page.md

Step 4: Re-encode
        base64 < /tmp/edit-page.md | tr -d '\n'

Step 5: Call MCP update
        mcp__gitea__update_wiki_page(
          owner="user",
          repo="myrepo",
          pageName="Home",
          content_base64="<output_from_step_4>"
        )
```

## Guidelines

### Do
- Use temp files (`/tmp/wiki-*.md`) for content manipulation
- Use `tr -d '\n'` when encoding - API requires no line breaks
- Clean up temp files after operations
- Decode content via Bash before reading

### Don't
- Include raw base64 content in LLM responses
- Skip the decode step when reading wiki pages
- Forget to encode content before creating/updating pages
- Leave temp files after operations complete

## Examples

### Example: Read Home page
```
1. mcp__gitea__get_wiki_page(owner="acme", repo="docs", pageName="Home")
   → Response: {"content_base64": "IyBXZWxjb21l..."}

2. Bash: echo "IyBXZWxjb21l..." | base64 -d > /tmp/wiki-home.md

3. Read: /tmp/wiki-home.md
   → Shows: "# Welcome..."
```

### Example: Create new page
```
1. Write /tmp/new-wiki.md:
   # Installation
   Run `npm install`

2. Bash: base64 < /tmp/new-wiki.md | tr -d '\n'
   → Output: IyBJbnN0YWxsYXRpb24KUnVuIGBucG0gaW5zdGFsbGA=

3. mcp__gitea__create_wiki_page(
     owner="acme",
     repo="docs",
     title="Installation",
     content_base64="IyBJbnN0YWxsYXRpb24KUnVuIGBucG0gaW5zdGFsbGA="
   )
```
