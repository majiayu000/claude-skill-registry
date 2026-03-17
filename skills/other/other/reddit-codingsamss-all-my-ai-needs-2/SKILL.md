---
name: reddit
description: "Read Reddit content via Composio MCP. Actions: search posts, view hot/top/new posts, read post content, read comments. Keywords: reddit, subreddit, post, comment, search reddit, hot posts, top posts."
---

# Reddit Skill (Read-Only)

Read Reddit content using the Composio Reddit MCP integration. This skill only exposes read-only operations.

## When to Use This Skill

Triggered by:
- "search reddit [query]", "find on reddit [query]"
- "reddit hot posts [subreddit]", "what's hot on r/[subreddit]"
- "reddit top posts [subreddit]", "top posts on r/[subreddit]"
- "reddit new posts [subreddit]", "latest on r/[subreddit]"
- "read reddit post [url/id]", "show reddit post"
- "reddit comments [url/id]", "show comments on reddit"

## Prerequisites

1. Composio Reddit MCP must be registered in Claude Code
2. Reddit OAuth authorization must be completed via Composio
3. Verify with: `claude mcp list` (should show `composio-reddit: Connected`)

## MCP Tools

All tools are accessed via the `composio-reddit` MCP server.

### 1. Search Reddit
**Triggers:** "search reddit [query]", "find on reddit [query]", "reddit search [query]"

Use MCP tool: `REDDIT_SEARCH_ACROSS_SUBREDDITS`
- Searches across all subreddits by keyword
- Returns matching posts and comments

### 2. Get Hot Posts from Subreddit
**Triggers:** "hot posts on r/[subreddit]", "what's trending on reddit [subreddit]"

Use MCP tool: `REDDIT_RETRIEVE_REDDIT_POST`
- Retrieves hot/popular posts from a specific subreddit
- Specify subreddit name without the "r/" prefix

### 3. Read Post Content
**Triggers:** "read reddit post [url/id]", "show reddit post [url/id]"

Use MCP tool: `REDDIT_RETRIEVE_SPECIFIC_COMMENT`
- Fetches full content of a specific post
- Accepts post URL or ID

### 4. Read Post Comments
**Triggers:** "reddit comments [url/id]", "show comments for reddit post"

Use MCP tool: `REDDIT_RETRIEVE_POST_COMMENTS`
- Fetches comment tree for a specific post
- Returns threaded comments with author and score

## Common Subreddits for Reference

- `r/MachineLearning` - ML research and news
- `r/LocalLLaMA` - Local LLM discussions
- `r/ClaudeAI` - Claude-specific discussions
- `r/ChatGPT` - ChatGPT discussions
- `r/programming` - General programming
- `r/webdev` - Web development
- `r/devops` - DevOps and infrastructure
- `r/artificial` - AI general discussions
- `r/singularity` - AI progress and AGI discussions

## Important Notes

- This skill is READ-ONLY - no posting, commenting, or voting
- Powered by Composio MCP with Reddit OAuth
- Free tier: 20,000 calls/month, 1,000 calls/hour (personal use sufficient)
- If authentication expires, re-authorize via Composio Dashboard

## Excluded Actions (Write Operations)

The following actions are intentionally NOT exposed:
- `REDDIT_CREATE_REDDIT_POST` - Create posts
- `REDDIT_POST_REDDIT_COMMENT` - Post comments
- `REDDIT_EDIT_REDDIT_COMMENT_OR_POST` - Edit content
- `REDDIT_DELETE_REDDIT_POST` - Delete posts
- `REDDIT_DELETE_REDDIT_COMMENT` - Delete comments
