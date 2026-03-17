---
name: twitter-to-obsidian
description: Extract content from Twitter/X articles, summarize key points, and save as structured Obsidian notes. Use when user provides a Twitter/X URL and wants to save it as a note, or mentions "save to Obsidian", "create a note from this tweet/article", or similar requests.
---

# Twitter to Obsidian Note Converter

This skill automates the process of extracting content from Twitter/X articles, analyzing and structuring the information, and saving it as a well-formatted Obsidian note.

## When to Use This Skill

Use this skill when:
- User provides a Twitter/X URL (x.com or twitter.com) and wants to save it
- User mentions "save to Obsidian", "create a note", "save as note"
- User asks to "梳理" (organize/summarize) a Twitter article and save it
- User wants to extract and organize content from social media posts

## Workflow

### Step 1: Access the Twitter/X Content

Use Chrome DevTools MCP to access the Twitter/X page:

1. **List available pages**:
   ```
   mcp__chrome-devtools__list_pages
   ```

2. **Navigate to URL** (if not already open):
   ```
   mcp__chrome-devtools__navigate_page
   type: url
   url: <twitter-url>
   ```

3. **Take snapshot** to extract content:
   ```
   mcp__chrome-devtools__take_snapshot
   ```

### Step 2: Analyze and Structure Content

Extract the following information from the snapshot:

1. **Metadata**:
   - Author name and handle
   - Publication date/time
   - Engagement metrics (replies, retweets, likes, bookmarks, views)
   - Source URL

2. **Main Content**:
   - Article title (if it's an X Article)
   - Full text content
   - Main sections and headings
   - Code examples or diagrams (preserve formatting)
   - Key images (note their descriptions)

3. **Structured Summary**:
   - Core concepts/main points
   - Key takeaways
   - Practical examples
   - Step-by-step instructions (if applicable)
   - Related resources/links

### Step 3: Format as Obsidian Note

Create a well-structured Markdown document with:

#### Required Sections:

1. **Header with metadata**:
   ```markdown
   # [Title]

   > **来源**: [Twitter/X - @username](url)
   > **作者**: Author Name
   > **发布时间**: YYYY年MM月DD日
   > **保存时间**: YYYY年MM月DD日

   ---
   ```

2. **概述 (Overview)**: Brief summary of the content

3. **核心内容 (Core Content)**: Main body organized with:
   - Clear headings (##, ###)
   - Bullet points for lists
   - Code blocks with language tags
   - Tables for structured data
   - Blockquotes for important quotes
   - Emoji for visual hierarchy (optional, use sparingly)

4. **相关资源 (Related Resources)**: Links mentioned in the article

5. **标签 (Tags)**: Relevant tags with # prefix

6. **个人笔记 (Personal Notes)**: Empty section for user's own thoughts

#### Formatting Best Practices:

- Use proper Markdown hierarchy (H1 for title, H2 for major sections, H3 for subsections)
- Preserve code formatting with triple backticks and language identifiers
- Use tables for comparisons or structured data
- Include ASCII diagrams if present in original content
- Add emoji sparingly for visual clarity (e.g., 🎯, 📌, ✅, ❌)
- Ensure all links are clickable Markdown links
- Use blockquotes (>) for important callouts or quotes

### Step 4: Save to Obsidian

1. **Determine the file path**:
   - Default Obsidian vault: `/Users/douba/Library/Mobile Documents/com~apple~CloudDocs/douba-OB`
   - Use a descriptive filename based on the article title
   - Replace special characters in filename with hyphens or spaces

2. **Save the file**:
   ```
   Write tool
   file_path: /Users/douba/Library/Mobile Documents/com~apple~CloudDocs/douba-OB/[filename].md
   content: [formatted markdown content]
   ```

3. **Confirm success** with the user:
   - Report the save location
   - Provide a brief summary of what was saved
   - List the main sections included

## Error Handling

### If Browser Access Fails:
- Check if user has the Twitter/X page already open in Chrome
- Ask user to open the page manually
- Verify Chrome DevTools MCP connection

### If Content Extraction is Incomplete:
- Notify user which sections are missing
- Explain what content was successfully extracted
- Offer to retry or ask user to provide missing information

### If Save Fails:
- Verify the Obsidian vault path exists
- Check file permissions
- Suggest alternative save location if needed

## Example Usage

**User**: "https://x.com/0xYuker/status/2013094122656334136 这篇文章的内容你梳理一下"

**Process**:
1. Access the Twitter URL via Chrome DevTools
2. Extract the article content about Multi-Agent systems
3. Structure it with clear sections: overview, core concepts, implementation steps
4. Save to Obsidian with metadata, tags, and formatted content

**User**: "你能够帮我直接存储到我的Obsidian里面，作为一篇笔记吗？"

**Process**:
1. Use previously extracted content
2. Format as Obsidian note with all required sections
3. Save to specified Obsidian vault path

## Tips for Quality Notes

1. **Preserve Structure**: Maintain the logical flow of the original content
2. **Add Value**: Don't just copy-paste; organize and clarify
3. **Context**: Include metadata so notes are self-contained
4. **Searchability**: Use relevant tags and clear headings
5. **Links**: Preserve all URLs as clickable Markdown links
6. **Examples**: Keep code examples and diagrams intact
7. **Visual Hierarchy**: Use consistent heading levels and formatting

## Output Style

- Be concise in status updates
- Confirm successful save with file path
- Highlight key sections that were included
- Use emoji sparingly for user-facing messages (✅ for success, ⚠️ for warnings)
