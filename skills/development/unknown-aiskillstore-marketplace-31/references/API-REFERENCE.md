# Raindrop.io MCP API Reference

This document provides a reference for the Model Context Protocol (MCP) tools available through the official Raindrop.io MCP server.

## Overview

The official Raindrop.io MCP server provides tools for managing your bookmarks, collections, tags, and highlights through a standardized interface. These tools are accessed through natural language when using the Raindrop.io skill.

**Note**: The official MCP server is in beta. Tool names, parameters, and capabilities may evolve. This reference documents expected functionality based on Raindrop.io's API capabilities.

## Connection Details

- **Server URL**: https://api.raindrop.io/rest/v2/ai/mcp
- **Transport**: SSE (Server-Sent Events)
- **Authentication**: OAuth 2.1 or Personal API Token
- **Rate Limit**: 120 requests/minute
- **Requirements**: Raindrop.io Pro subscription

## Tool Categories

Tools are organized into the following categories:

1. [Bookmarks](#bookmarks) - Create, read, update, delete bookmarks
2. [Collections](#collections) - Manage bookmark collections
3. [Tags](#tags) - Organize and manage tags
4. [Search](#search) - Find bookmarks with filters
5. [Highlights](#highlights) - Manage text highlights
6. [Bulk Operations](#bulk-operations) - Update multiple items at once

---

## Bookmarks

### Create Bookmark

**Purpose**: Add a new bookmark to your Raindrop.io account

**Typical Parameters**:
- `url` (required): The URL to bookmark
- `title` (optional): Custom title for the bookmark
- `description` (optional): Notes or description
- `collection_id` (optional): Collection to save to (defaults to "Unsorted")
- `tags` (optional): Array of tag strings
- `favorite` (optional): Boolean to mark as favorite
- `important` (optional): Boolean to mark as important

**Example Usage**:
```
"Save https://example.com/article to my Reading List collection with tags: python, tutorial"
```

**Returns**: Bookmark object with ID, URL, title, and other metadata

**Notes**:
- URLs are validated before saving
- Raindrop.io will attempt to fetch title and description if not provided
- Covers/thumbnails are generated automatically when possible

### Get Bookmark

**Purpose**: Retrieve a specific bookmark by ID

**Typical Parameters**:
- `bookmark_id` (required): The ID of the bookmark to retrieve

**Returns**: Full bookmark object with all metadata

**Notes**:
- Includes tags, collection, highlights, and other details
- May return cache information and parsing status

### Update Bookmark

**Purpose**: Modify an existing bookmark

**Typical Parameters**:
- `bookmark_id` (required): The ID of the bookmark to update
- `title` (optional): New title
- `description` (optional): New description
- `tags` (optional): New array of tags (replaces existing)
- `collection_id` (optional): Move to different collection
- `favorite` (optional): Update favorite status
- `important` (optional): Update important status

**Example Usage**:
```
"Update bookmark [ID] to add tags: machine-learning, research"
```

**Returns**: Updated bookmark object

### Delete Bookmark

**Purpose**: Remove a bookmark permanently

**Typical Parameters**:
- `bookmark_id` (required): The ID of the bookmark to delete

**Returns**: Success confirmation

**Notes**:
- Deletion is permanent and cannot be undone
- Associated highlights are also deleted

---

## Collections

### List Collections

**Purpose**: Get all collections in your account

**Parameters**: None typically required

**Returns**: Array of collection objects with IDs, titles, and counts

**Example Usage**:
```
"List all my collections"
```

**Notes**:
- Includes system collections (Unsorted, Trash)
- Shows bookmark count per collection
- Returns hierarchical structure if you have nested collections

### Create Collection

**Purpose**: Create a new collection

**Typical Parameters**:
- `title` (required): Name of the collection
- `description` (optional): Description
- `parent_id` (optional): Parent collection for nesting
- `public` (optional): Whether collection is publicly accessible
- `view` (optional): Display view type (list, grid, etc.)

**Example Usage**:
```
"Create a collection called 'Machine Learning Research'"
```

**Returns**: New collection object with ID

### Update Collection

**Purpose**: Modify collection properties

**Typical Parameters**:
- `collection_id` (required): ID of collection to update
- `title` (optional): New title
- `description` (optional): New description
- `public` (optional): Change public status
- `parent_id` (optional): Move to different parent

**Returns**: Updated collection object

### Delete Collection

**Purpose**: Remove a collection

**Typical Parameters**:
- `collection_id` (required): ID of collection to delete

**Returns**: Success confirmation

**Notes**:
- Bookmarks are moved to "Unsorted" by default, not deleted
- Nested collections are also affected

---

## Tags

### List Tags

**Purpose**: Get all tags in your account

**Parameters**: None typically required

**Returns**: Array of tag names with usage counts

**Example Usage**:
```
"Show all my tags"
```

**Notes**:
- Sorted by usage frequency or alphabetically
- Shows number of bookmarks per tag

### Rename Tag

**Purpose**: Change a tag name across all bookmarks

**Typical Parameters**:
- `old_name` (required): Current tag name
- `new_name` (required): New tag name

**Example Usage**:
```
"Rename tag 'javascript' to 'js'"
```

**Returns**: Success confirmation with count of affected bookmarks

**Notes**:
- Updates all bookmarks with the old tag
- Case-sensitive operation

### Merge Tags

**Purpose**: Combine multiple tags into one

**Typical Parameters**:
- `tags` (required): Array of tag names to merge
- `target_name` (required): The tag name to keep

**Example Usage**:
```
"Merge tags 'ML', 'machine-learning', 'machinelearning' into 'machine-learning'"
```

**Returns**: Success confirmation with affected bookmark count

### Delete Tag

**Purpose**: Remove a tag from all bookmarks

**Typical Parameters**:
- `tag_name` (required): Tag to remove

**Returns**: Success confirmation

**Notes**:
- Removes tag from all bookmarks but doesn't delete bookmarks

---

## Search

### Search Bookmarks

**Purpose**: Find bookmarks using various filters

**Typical Parameters**:
- `query` (optional): Text search in title/description/content
- `tags` (optional): Filter by tags (AND or OR logic)
- `collection_id` (optional): Limit to specific collection
- `domain` (optional): Filter by website domain
- `favorite` (optional): Only favorites
- `important` (optional): Only important bookmarks
- `created_from` (optional): Date filter (from)
- `created_to` (optional): Date filter (to)
- `sort` (optional): Sort order (created, title, domain, etc.)
- `page` (optional): Pagination page number
- `per_page` (optional): Results per page (max 50)

**Example Usage**:
```
"Search for bookmarks tagged 'python' and 'tutorial' from last month"
```

**Returns**: Array of bookmark objects matching criteria

**Advanced Filters**:
- Full-text search looks in titles, descriptions, and cached content
- Multiple tags can use AND or OR logic
- Date ranges use ISO 8601 format
- Supports fuzzy matching for typos

**Notes**:
- Results are paginated for large sets
- Search indexing may have slight delay for new bookmarks
- Case-insensitive search

---

## Highlights

### List Highlights

**Purpose**: Get highlights from a bookmark

**Typical Parameters**:
- `bookmark_id` (required): The bookmark to get highlights from

**Returns**: Array of highlight objects with text and metadata

**Example Usage**:
```
"Show me the highlights from bookmark [ID]"
```

### Create Highlight

**Purpose**: Add a text highlight to a bookmark

**Typical Parameters**:
- `bookmark_id` (required): Bookmark to highlight
- `text` (required): The highlighted text
- `note` (optional): Personal note about the highlight
- `color` (optional): Highlight color code

**Example Usage**:
```
"Add highlight to bookmark [ID]: 'The key insight is asynchronous processing'"
```

**Returns**: New highlight object with ID

### Update Highlight

**Purpose**: Modify an existing highlight

**Typical Parameters**:
- `highlight_id` (required): ID of highlight to update
- `text` (optional): New highlighted text
- `note` (optional): Update note
- `color` (optional): Change color

**Returns**: Updated highlight object

### Delete Highlight

**Purpose**: Remove a highlight

**Typical Parameters**:
- `highlight_id` (required): ID of highlight to delete

**Returns**: Success confirmation

---

## Bulk Operations

### Bulk Update Bookmarks

**Purpose**: Update multiple bookmarks at once

**Typical Parameters**:
- `bookmark_ids` (required): Array of bookmark IDs
- `operation` (required): Type of operation
  - `add_tags`: Add tags to bookmarks
  - `remove_tags`: Remove tags from bookmarks
  - `set_tags`: Replace all tags
  - `move_collection`: Move to different collection
  - `set_favorite`: Mark as favorite/unfavorite
  - `set_important`: Mark as important/unimportant
- `value` (varies): Operation-specific value (tags array, collection_id, boolean)

**Example Usage**:
```
"Add tag 'archive' to all bookmarks in my Old Projects collection"
```

**Returns**: Success confirmation with count of updated bookmarks

**Notes**:
- Limited to reasonable batch sizes (typically 100-500 bookmarks)
- Operations are atomic - all succeed or all fail
- Can be slow for large batches

### Bulk Delete Bookmarks

**Purpose**: Delete multiple bookmarks at once

**Typical Parameters**:
- `bookmark_ids` (required): Array of bookmark IDs to delete

**Returns**: Success confirmation with count

**Notes**:
- Permanent operation, cannot be undone
- Consider moving to Trash collection instead for safety

---

## Error Handling

All tools may return errors in these situations:

### Common Error Codes

- `400` - Bad Request: Invalid parameters
- `401` - Unauthorized: Authentication failed or expired
- `403` - Forbidden: Pro subscription required or access denied
- `404` - Not Found: Bookmark, collection, or resource doesn't exist
- `429` - Rate Limited: Too many requests
- `500` - Server Error: Raindrop.io server issue

### Error Response Format

Errors typically include:
- `error`: Boolean (true)
- `errorMessage`: Human-readable error description
- `code`: HTTP status code
- `details`: Additional context when available

### Handling Errors in Natural Language

When an error occurs:
1. The AI will explain what went wrong
2. Suggest corrective actions
3. Retry if appropriate (e.g., after rate limit delay)

---

## Best Practices

### Efficient Tool Usage

1. **Batch operations**: Use bulk updates when modifying many bookmarks
2. **Specific queries**: Provide as many search filters as possible
3. **Pagination**: For large result sets, fetch pages as needed
4. **Cache locally**: Store collection/tag lists to avoid repeated fetches
5. **Error handling**: Always check for errors and handle gracefully

### Rate Limiting

- Keep requests under 120/minute per user
- MCP server should handle rate limiting automatically
- If you hit limits, wait 60 seconds before retrying
- Use bulk operations to reduce total request count

### Data Consistency

- Bookmark IDs are stable and can be cached
- Collection structure may change between sessions
- Tags are case-sensitive - establish conventions early
- Search indexes may have a few seconds delay

---

## Tool Discovery

To see the actual tools available in your MCP connection:

1. Ask: "What Raindrop.io tools are available?"
2. Request: "List all MCP tools"
3. Check your client's tools/commands menu

Actual tool names and parameters may vary from this reference as the official server is in beta.

---

## Examples

### Complete Workflow Examples

**Save and Organize**:
```
1. Create bookmark with URL
2. Add tags: ["python", "web-scraping"]
3. Move to "Development" collection
4. Mark as favorite
```

**Research Project**:
```
1. Create collection "My Research"
2. Search for bookmarks with domain "arxiv.org"
3. Bulk update to add tag "research"
4. Move to new collection
```

**Cleanup**:
```
1. List untagged bookmarks
2. Filter by old date (> 1 year)
3. Review and tag or delete
```

---

## Additional Resources

- **Official Raindrop.io API Docs**: https://developer.raindrop.io
- **MCP Protocol Spec**: https://modelcontextprotocol.io
- **Raindrop.io MCP Help**: https://help.raindrop.io/mcp
- **Get Support**: info@raindrop.io

## Beta Status Note

This reference is based on expected functionality. As the official Raindrop.io MCP server is in beta:

- Tool names may differ
- Parameters may vary
- New tools may be added
- Some operations may not be available yet

Always check actual tool documentation from your MCP client and report discrepancies to Raindrop.io.

---

**Last Updated**: 2025-02-18
**Server Version**: Beta
**API Version**: v2