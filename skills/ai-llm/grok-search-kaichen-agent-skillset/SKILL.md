---
name: grok-search
description: Use Grok AI (grok.com) to search and research topics via browser automation. Triggers on "use grok to search", "ask grok", "grok research", "search with grok", or when user wants real-time X/Twitter data analysis, trending topics, or AI-powered web research.
---

# Grok Search

Search and research using Grok AI via browser automation with Claude in Chrome MCP.

## Prerequisites

- Claude in Chrome MCP extension installed and configured
- Logged into grok.com in Chrome

## Quick Start

### Direct URL Query (Recommended)

Use URL parameters to submit queries directly without manual input:

```
https://grok.com/?q={your_query}
```

This automatically submits the query and starts generating results.

### Example Workflow

```javascript
// 1. Create new tab
mcp__claude-in-chrome__tabs_create_mcp()

// 2. Navigate with query parameter
mcp__claude-in-chrome__navigate({
  url: "https://grok.com/?q=your search query here",
  tabId: <tab_id>
})

// 3. Wait for results (typically 5-30 seconds for regular, 1-3 minutes for DeepSearch)
mcp__claude-in-chrome__computer({ action: "wait", duration: 10, tabId: <tab_id> })

// 4. Get page text content
mcp__claude-in-chrome__get_page_text({ tabId: <tab_id> })

// 5. Find and click copy button (aria-label="Copy") or (aria-label="复制") 
mcp__claude-in-chrome__find({ query: "复制 button", tabId: <tab_id> })
mcp__claude-in-chrome__computer({ action: "left_click", ref: "ref_xxx", tabId: <tab_id> })

// 6. Save to file via clipboard
Bash: pbpaste > result.md
```

## Search Modes

### Default Mode (Fast)
- URL: `https://grok.com/?q={query}`
- Response time: 5-15 seconds
- Best for: Quick questions, simple lookups

### DeepSearch Mode (Thorough)
- Requires clicking DeepSearch button before submitting
- Response time: 1-3 minutes
- Best for: Research, comprehensive analysis, multi-source information

To enable DeepSearch:
```javascript
// After navigating to grok.com (without query param)
mcp__claude-in-chrome__find({ query: "DeepSearch button", tabId: <tab_id> })
mcp__claude-in-chrome__computer({ action: "left_click", ref: "ref_xxx", tabId: <tab_id> })
// Then input query and submit
```

## Common Use Cases

### 1. Real-time X/Twitter Analysis
```
Query: "24h内中文热门推特在讨论什么"
Query: "What are trending topics on X about AI in the last 24 hours"
Query: "24h内我关注的中文推特时间线里有哪些热门讨论"
```

### 2. News and Current Events
```
Query: "最近24小时内 Claude 相关的信息有哪些"
Query: "Latest news about [topic] in the past 24 hours"
```

### 3. Research Topics
```
Query: "[Topic] 的最新进展和讨论"
Query: "Comprehensive overview of [topic]"
```

## Handling Results

### Method 1: Copy Button (Preferred)
```javascript
// Find copy button using aria-label
mcp__claude-in-chrome__find({ query: "复制 button", tabId: <tab_id> })
// Click to copy content to clipboard
mcp__claude-in-chrome__computer({ action: "left_click", ref: "ref_xxx", tabId: <tab_id> })
// Save from clipboard
Bash: pbpaste > result.md
```

### Method 2: Direct Text Extraction (Fallback)
```javascript
// If copy button fails, extract text directly
const text = mcp__claude-in-chrome__get_page_text({ tabId: <tab_id> })
// Then save content via Write tool
```

## Tips

1. **Check Generation Status**: Look for timing indicators like "思考了 Xs" or "Searching" in page text
2. **Wait Adequately**: DeepSearch can take 1-3 minutes; check periodically with `get_page_text`
3. **Tab Management**: Create new tabs for parallel searches
4. **Error Recovery**: If extension conflicts occur, try `get_page_text` as fallback for content extraction
5. **URL Encoding**: Complex queries with special characters should be URL-encoded

## Troubleshooting

### Extension Conflicts
If you encounter "Cannot access a chrome-extension:// URL" errors:
1. Try navigating to a fresh URL
2. Use `get_page_text` instead of screenshot
3. Create a new tab and retry

### Results Not Loading
1. Increase wait time
2. Check if Grok is still generating (look for loading indicators)
3. Verify you're logged into grok.com

### Copy Button Not Working
1. Use `get_page_text` to extract content directly
2. Format and save the text content manually
