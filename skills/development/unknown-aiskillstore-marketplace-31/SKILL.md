---
name: raindrop-io
description: Manage Raindrop.io bookmarks with AI assistance. Save and organize bookmarks, search your collection, manage reading lists, and organize research materials. Use when working with bookmarks, web research, reading lists, or when user mentions Raindrop.io.
license: MIT
compatibility: Requires Raindrop.io Pro subscription and MCP server configuration. Works with Claude Code, Claude Desktop, Claude.ai, Codex, Cursor, and other MCP-compatible clients.
metadata:
  author: dansegal
  version: "1.0.0"
  mcp_server: "https://api.raindrop.io/rest/v2/ai/mcp"
  mcp_type: "sse"
---

# Raindrop.io Bookmark Management Skill

Manage your Raindrop.io bookmarks with AI assistance. This skill enables you to save, organize, search, and manage your bookmarks through natural language conversations.

## Prerequisites

Before using this skill, ensure you have:

1. **Raindrop.io Pro subscription**: The official MCP server requires a Pro account
2. **MCP server configured**: Follow the setup guide in [references/SETUP.md](references/SETUP.md)
3. **Active connection**: Verify MCP tools are available by listing your tools

To verify the connection is working:
- Check that Raindrop.io MCP tools appear in your available tools list
- Try a simple operation like listing collections

If you encounter issues, see the troubleshooting section at the end of this document.

## Quick Start Workflows

### 1. Save a Bookmark

**When to use**: Adding new bookmarks to your collection with smart organization.

**Steps**:
1. Ask the user for the URL they want to save
2. Use the appropriate MCP tool to create the bookmark
3. Ask the user if they want to:
   - Add to a specific collection
   - Add tags for organization
   - Mark as favorite
   - Add notes or description
4. Apply the requested organization
5. Confirm the bookmark was saved successfully

**Example conversation**:
```
User: Save this article about AI: https://example.com/ai-article
Assistant: I'll save that bookmark for you. Would you like me to:
- Add it to a specific collection?
- Tag it with relevant keywords?
- Mark it as a favorite?
User: Yes, add it to my "AI Research" collection and tag it with "machine-learning" and "research"
Assistant: Done! I've saved the bookmark to your AI Research collection with the tags machine-learning and research.
```

### 2. Search Bookmarks

**When to use**: Finding bookmarks by content, tags, domains, or other criteria.

**Steps**:
1. Identify what the user is searching for
2. Use the MCP search tool with appropriate filters:
   - By tags
   - By collection
   - By domain
   - By date range
   - By search term in title/description
3. Present results in a clear, scannable format
4. Offer to:
   - Open specific bookmarks
   - Show more details
   - Refine the search

**Example conversation**:
```
User: Find all my bookmarks about Python from last month
Assistant: I'll search for Python-related bookmarks from the past month.
[searches using MCP tools]
Found 8 bookmarks:
1. Python Best Practices (pythonguide.org) - tagged: python, programming
2. FastAPI Tutorial (fastapi.tiangolo.com) - tagged: python, api
...

Would you like me to show more details or refine the search?
```

### 3. Manage Reading List

**When to use**: Organizing articles to read, marking progress, and extracting highlights.

**Steps**:
1. **Add to reading list**:
   - Use collection named "Reading List" or create one
   - Save bookmarks with appropriate tags

2. **Review reading list**:
   - Search bookmarks in reading list collection
   - Sort by date or priority
   - Show unread items

3. **Mark as read**:
   - Update bookmark status
   - Optionally move to different collection
   - Add highlights or notes

4. **Extract highlights**:
   - Retrieve saved highlights from bookmarks
   - Organize by topic or theme
   - Export for note-taking

**Example conversation**:
```
User: Show me my reading list
Assistant: Here are your unread articles:
1. [Article Title] - saved 2 days ago
2. [Article Title] - saved 1 week ago
...

User: Mark the first one as read and add a highlight
Assistant: I've marked it as read. What highlight would you like to add?
User: "The key insight was the importance of asynchronous processing"
Assistant: Highlight saved! Would you like to move this to a different collection or keep it in your Archive?
```

### 4. Organize Research

**When to use**: Managing research projects with multiple bookmarks, collections, and tags.

**Steps**:
1. **Create research project structure**:
   - Create a collection for the project
   - Define relevant tags
   - Set up sub-collections if needed

2. **Add bookmarks to project**:
   - Save new sources to the collection
   - Tag systematically
   - Add notes and context

3. **Bulk organize**:
   - Update multiple bookmarks at once
   - Apply tags to groups
   - Move bookmarks between collections

4. **Review and export**:
   - Generate summary of bookmarked sources
   - List by category or tag
   - Export highlights and notes

**Example conversation**:
```
User: Help me organize research for my machine learning project
Assistant: I'll help you set up a research collection. First, let me create a "Machine Learning Project" collection for you.

What main topics should we track? (e.g., neural-networks, training, deployment)

User: neural networks, datasets, model-architectures, papers
Assistant: Perfect! I've created the collection with those tags. Now you can add bookmarks with:
"Save [URL] to my machine learning project, tag: neural-networks"

I'll automatically organize them for you. Would you like me to help you add some bookmarks now?
```

## Common Patterns and Best Practices

### Tagging Strategy
- Use lowercase, hyphenated tags (e.g., `machine-learning`, not `Machine Learning`)
- Create a consistent taxonomy for your domain
- Use broad tags for discovery (e.g., `programming`) and specific tags for precision (e.g., `python-asyncio`)
- Limit to 3-5 tags per bookmark for clarity

### Collection Organization
- Create collections for projects, topics, or workflows
- Use descriptive names that reflect the content
- Consider creating a "Reading List" for articles to read
- Use "Archive" for completed or reference material
- Nest collections when you have clear hierarchies

### Search Tips
- Combine multiple filters for precision (tags + collection + date range)
- Search by domain to find all bookmarks from a specific site
- Use date ranges to find recent additions or old bookmarks
- Full-text search looks in titles, descriptions, and content

### Workflow Integration
- **Daily review**: Check bookmarks added today
- **Weekly cleanup**: Review untagged bookmarks and organize them
- **Project workflows**: Create collection → Add bookmarks → Tag systematically → Extract highlights
- **Reading workflow**: Save to reading list → Mark as read → Add highlights → Move to archive

## Working with MCP Tools

When using this skill, you'll interact with the Raindrop.io MCP server through natural language. The skill will handle the technical details of calling MCP tools.

### Available Operations
Based on typical Raindrop.io API capabilities, you can expect to:

- **Create bookmarks**: Add new URLs with metadata
- **Search bookmarks**: Find bookmarks by various criteria
- **Update bookmarks**: Modify tags, collections, notes
- **Delete bookmarks**: Remove unwanted bookmarks
- **Manage collections**: Create, update, delete collections
- **Manage tags**: Rename, merge, delete tags
- **Handle highlights**: Create and retrieve highlights
- **Bulk operations**: Update multiple bookmarks at once

For detailed tool documentation, see [references/API-REFERENCE.md](references/API-REFERENCE.md).

## Advanced Usage

For advanced workflows and automation, see [references/WORKFLOWS.md](references/WORKFLOWS.md) for examples including:

- Research project setup with bulk import
- Automated reading list management
- Tag organization strategies
- Cross-collection search patterns
- Highlight extraction and note-taking integration

## Troubleshooting

### MCP Server Not Connected
**Symptoms**: Tools not available, connection errors

**Solutions**:
1. Verify your Raindrop.io Pro subscription is active
2. Check MCP server configuration (see [references/SETUP.md](references/SETUP.md))
3. Try reauthorizing through OAuth flow
4. Restart your AI client (Claude Desktop, etc.)

### Authentication Errors
**Symptoms**: 401 Unauthorized, access denied

**Solutions**:
1. Reauthorize the MCP connection
2. Check that your API token is valid (if using token auth)
3. Verify your account has Pro access
4. Clear and reconnect the MCP server

### Bookmarks Not Saving
**Symptoms**: Operations complete but bookmarks don't appear

**Solutions**:
1. Verify the URL is valid and accessible
2. Check you have permission to write to the collection
3. Try refreshing your Raindrop.io web interface
4. Check for rate limiting (official server should handle this)

### Search Not Finding Bookmarks
**Symptoms**: Expected bookmarks not in search results

**Solutions**:
1. Verify bookmarks exist in Raindrop.io web interface
2. Try broader search terms
3. Check collection filters aren't too restrictive
4. Wait a moment for indexing if just added

### Beta Limitations
**Note**: The official Raindrop.io MCP server is currently in beta. Some features may:
- Have limited functionality
- Require updates as the API evolves
- Behave differently than documented

Report issues to Raindrop.io support at info@raindrop.io or check [help.raindrop.io/mcp](https://help.raindrop.io/mcp) for updates.

## Tips for Success

1. **Start simple**: Begin with basic bookmark saving and searching before advanced workflows
2. **Be specific**: Provide clear instructions about collections, tags, and organization
3. **Verify results**: Check that operations completed as expected
4. **Build gradually**: Develop your organization system over time
5. **Stay consistent**: Use consistent naming and tagging conventions
6. **Review regularly**: Periodic cleanup keeps your bookmarks useful

## Privacy and Security

- MCP connection uses OAuth 2.1 for secure authentication
- Your bookmarks remain in your Raindrop.io account
- The skill only accesses bookmarks you've authorized
- No data is stored outside of Raindrop.io's servers
- Review Raindrop.io's privacy policy for details

## Getting Help

- **Setup issues**: See [references/SETUP.md](references/SETUP.md)
- **Advanced workflows**: See [references/WORKFLOWS.md](references/WORKFLOWS.md)
- **Tool reference**: See [references/API-REFERENCE.md](references/API-REFERENCE.md)
- **Raindrop.io support**: info@raindrop.io
- **MCP documentation**: https://help.raindrop.io/mcp

## About This Skill

This skill provides a natural language interface to Raindrop.io using the official MCP server. It's designed for:

- Researchers managing sources and references
- Developers organizing technical documentation
- Readers managing articles and reading lists
- Anyone who needs better bookmark organization

The skill is open source and welcomes contributions. Find it on GitHub or skillstore.io.

---

**Version**: 1.0.0
**Author**: dansegal
**License**: MIT
**MCP Server**: https://api.raindrop.io/rest/v2/ai/mcp
**Status**: Beta (official Raindrop.io MCP server is in beta)