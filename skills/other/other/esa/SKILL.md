---
name: esa
description: Search and retrieve information from esa.io team using the esa-cli tool. Use this skill to find posts, get team information, or search by category/tag in esa.
---

# esa Search Skill

This skill enables you to search and retrieve information from esa.io team using the `esa-cli` command-line tool.

## Prerequisites

Before using this skill, ensure:
1. `ESA_TEAM` environment variable is set with your esa team name
2. `ESA_ACCESS_TOKEN` environment variable is set with a valid esa access token
3. The `esa-cli` binary is available in PATH or installed locally

## Available Commands

### 1. Get Team Information

Retrieve information about your esa team:

```bash
esa-cli team
```

**Example Output:**
```
================================================================================
Team Information
================================================================================

Name: your-team
Privacy: closed
Description: Team description here
URL: https://your-team.esa.io

================================================================================
```

### 2. Search Posts

Search for posts containing specific keywords across your team:

```bash
esa-cli search "<query>"
```

**Options:**
- `--page=N`: Page number (default: 1)
- `--per-page=N`: Number of results per page (default: 20, max: 100)
- `--sort=ORDER`: Sort order - `updated` (default), `created`, `stars`, `watches`, `comments`, `best_match`

**Query Filters:**
- `category:<name>`: Filter by category (e.g., `category:dev/api`)
- `tag:<name>`: Filter by tag (e.g., `tag:important`)
- `user:<name>`: Filter by user (e.g., `user:username`)
- `kind:<type>`: Filter by kind - `stock` or `flow`

**Examples:**
```bash
# Basic search
esa-cli search "API documentation"

# Search by category
esa-cli search "category:dev/api"

# Search by tag
esa-cli search "tag:important"

# Combined filters
esa-cli search "category:dev/api tag:important"

# Search with pagination and sort
esa-cli search "database" --page=2 --per-page=50 --sort=stars

# Search by user
esa-cli search "user:john.doe"

# Search by kind
esa-cli search "kind:stock"
```

### 3. Get Specific Post

Retrieve a specific post by its number:

```bash
esa-cli get <post-number>
```

**Example:**
```bash
# Get post #123
esa-cli get 123
```

**Output includes:**
- Post title and full name
- Category and tags
- Created and updated timestamps
- Full Markdown body content
- Post URL

### 4. Get Posts by Category

Retrieve all posts in a specific category:

```bash
esa-cli category "<category-name>"
```

**Options:**
- `--page=N`: Page number
- `--per-page=N`: Results per page
- `--sort=ORDER`: Sort order

**Examples:**
```bash
# Get posts in "dev/api" category
esa-cli category "dev/api"

# With pagination
esa-cli category "docs" --page=2 --per-page=30

# Sort by creation date
esa-cli category "team/meeting" --sort=created
```

### 5. Get Posts by Tag

Retrieve all posts with a specific tag:

```bash
esa-cli tag "<tag-name>"
```

**Options:**
- `--page=N`: Page number
- `--per-page=N`: Results per page
- `--sort=ORDER`: Sort order

**Examples:**
```bash
# Get posts tagged "important"
esa-cli tag "important"

# With pagination and sort
esa-cli tag "release" --page=1 --per-page=50 --sort=stars
```

## Output Format

### Search Results Format

```
Found N posts:
================================================================================

[1] #123 Post Title
Full Name: Category/Subcategory/Post Title
Updated: 2024-01-15T10:30:00
URL: https://your-team.esa.io/posts/123
Category: Category/Subcategory
Tags: tag1, tag2, tag3

[2] #124 Another Post
...

================================================================================
Page 1 (Total: 50 posts, 20 per page)
```

### Post Detail Format

```
================================================================================
Post #123: Post Title
================================================================================

Full Name: Category/Subcategory/Post Title
Category: Category/Subcategory
Tags: tag1, tag2, tag3
Created: 2024-01-01T09:00:00
Updated: 2024-01-15T10:30:00
URL: https://your-team.esa.io/posts/123

--- Body (Markdown) ---

# Post Content

Your markdown content here...

================================================================================
```

## Usage Guidelines

### When to Use This Skill

Use this skill when you need to:
- Find specific information in your esa knowledge base
- Retrieve documentation or technical notes
- Search for posts by category or topic
- Get the latest updates in specific areas
- Access full content of specific posts
- Browse team knowledge base

### Best Practices

1. **Use Specific Search Terms**: Use precise keywords to get relevant results
2. **Leverage Categories**: When you know the category, use category search for better results
3. **Use Tags for Topics**: Tags are great for cross-category topic searches
4. **Adjust Page Size**: Increase `--per-page` if you need more results at once
5. **Sort Appropriately**: Use `--sort=best_match` for keyword relevance, `--sort=updated` for recency
6. **Check Post Numbers**: Note post numbers from search results to fetch full content later

### Common Use Cases

**Finding API Documentation:**
```bash
esa-cli search "API" --sort=best_match
esa-cli category "dev/api"
```

**Checking Recent Updates:**
```bash
esa-cli search "category:team/meeting" --sort=updated --per-page=10
```

**Getting Team Guidelines:**
```bash
esa-cli category "team/guidelines"
```

**Finding Important Announcements:**
```bash
esa-cli tag "important"
esa-cli tag "announcement"
```

**Reading Specific Post:**
```bash
# First, search to find the post number
esa-cli search "onboarding guide"

# Then, get the full content
esa-cli get 456
```

**Investigating Topics:**
```bash
# Search broadly
esa-cli search "database migration"

# Check specific category
esa-cli category "dev/database"

# Check related tags
esa-cli tag "migration"
```

**Browsing Popular Posts:**
```bash
esa-cli search "*" --sort=stars --per-page=20
```

## Error Handling

### Common Errors and Solutions

1. **"ESA_TEAM environment variable is not set"**
   - Set the environment variable: `export ESA_TEAM=your-team-name`

2. **"ESA_ACCESS_TOKEN environment variable is not set"**
   - Set the environment variable: `export ESA_ACCESS_TOKEN=your-token`
   - Get your token from: `https://[your-team].esa.io/user/applications`

3. **"esa API HTTP Error"**
   - Verify your access token is valid and not expired
   - Check that your team name is correct
   - Ensure the token has appropriate read permissions

4. **"No posts found"**
   - Try broader search terms
   - Check if the category or tag name is correct (case-sensitive)
   - Verify you have access to the content

5. **Post not found (when using `get`)**
   - Verify the post number is correct
   - Check if the post was deleted or archived
   - Ensure you have permission to view the post

## Access Token Setup

### Creating an Access Token

1. Visit `https://[your-team].esa.io/user/applications`
2. Click "Generate new token"
3. Select at minimum the following scopes:
   - `read` - Read posts and team information
4. Generate the token and copy it
5. Set it as an environment variable:
   ```bash
   export ESA_ACCESS_TOKEN=your-token-here
   ```

### Storing Credentials Securely

Add to your shell configuration file (`.bashrc`, `.zshrc`, etc.):
```bash
export ESA_TEAM=your-team-name
export ESA_ACCESS_TOKEN=your-access-token
```

Or use `direnv` with `.envrc`:
```bash
export ESA_TEAM=your-team-name
export ESA_ACCESS_TOKEN=your-access-token
```

## Limitations

- **Read-Only**: This CLI only supports read operations (no post creation/editing/deletion)
- **Permissions**: Only accesses content you have permission to read
- **Rate Limits**: esa API has rate limits; avoid rapid consecutive requests
- **Page Size**: Maximum 100 posts per page
- **Search Scope**: Searches are limited to your team's content

## Tips for Effective Searching

1. **Start with Categories**: If you know the category structure, use category search
2. **Use Tags for Themes**: Tags often represent cross-cutting themes or projects
3. **Combine Filters**: Use multiple filters together for precise results
4. **Sort by Relevance**: Use `--sort=best_match` when keyword matching is crucial
5. **Sort by Time**: Use `--sort=updated` or `--sort=created` for chronological browsing
6. **Iterate Searches**: Start broad, note interesting post numbers, then fetch full content
7. **Check Pagination**: If you don't see what you're looking for, check the next page

## Integration with Workflows

This skill works well in combination with other tasks:
- Search esa → Find relevant documentation → Summarize for current task
- Get post → Extract code examples → Apply to implementation
- Search by tag → Compile related information → Create comprehensive guide
- Browse categories → Identify knowledge gaps → Suggest new documentation
- Find team guidelines → Ensure compliance → Propose improvements

## Example Workflow: Researching a Topic

```bash
# Step 1: Broad search to understand scope
esa-cli search "authentication"

# Step 2: Check specific category
esa-cli category "dev/security"

# Step 3: Look for related tags
esa-cli tag "auth"

# Step 4: Get full content of relevant posts
esa-cli get 123
esa-cli get 456

# Step 5: Check for recent updates
esa-cli search "category:dev/security" --sort=updated --per-page=5
```
