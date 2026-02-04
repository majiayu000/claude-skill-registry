---
name: web-content-extraction-navigator
description: When the user needs to extract specific content from websites that require interactive navigation, particularly when dealing with dynamic content, truncated text, or pages that require clicking buttons to reveal full information. This skill handles browser automation to navigate web pages, interact with page elements (like expanding truncated descriptions), extract structured content from complex page layouts, and overcome common web scraping challenges like bot detection or IP blocking. It's triggered when dealing with websites that require clicking 'show more', 'expand', or similar interactive elements to access complete information.
---
# Skill: Web Content Extraction Navigator

## Purpose
Extract structured content from dynamic web pages that require user interaction (clicking buttons, expanding sections, navigating through page elements) to reveal complete information.

## Primary Use Case
When the target content is hidden behind:
- "Show more", "Expand", "...more" buttons
- Truncated descriptions or lists
- Dynamic page loads requiring interaction
- Pages with bot detection mechanisms

## Core Strategy
1. **Browser Automation First**: Use Playwright for reliable interaction with dynamic content.
2. **Fallback Layers**: When direct APIs fail (e.g., transcript APIs blocked), navigate manually.
3. **Progressive Discovery**: Navigate through page spans/sections to locate target content.
4. **Structured Extraction**: Parse and format extracted content according to user requirements.

## Execution Workflow

### Phase 1: Initial Setup & Exploration
1. **Read Format Requirements**: Check for any format specifications in workspace files.
2. **Search for Target**: Use web search to locate the target URL/content.
3. **Attempt Direct Methods**: Try direct API access first (e.g., YouTube transcript API).

### Phase 2: Browser Navigation & Interaction
4. **Navigate to Target URL**: Use Playwright to load the page.
5. **Handle Bot Detection**: Recognize and work around sign-in prompts or bot checks.
6. **Expand Hidden Content**: 
   - Look for truncation indicators ("...more", "Show more", "Expand description")
   - Click interactive elements to reveal full content
   - Use snapshot navigation to explore different page sections

### Phase 3: Content Extraction & Processing
7. **Locate Target Content**: Identify the specific content area (e.g., video description, tracklist).
8. **Extract Structured Data**: Parse the content into clean, structured format.
9. **Format According to Requirements**: Apply any specified formatting templates.
10. **Write Output File**: Save extracted content to the requested location.

## Key Techniques
- **Snapshot Navigation**: Use `browser_snapshot_navigate_to_next_span` to explore large pages
- **Element Targeting**: Click specific elements by reference ID or role/text
- **Content Parsing**: Extract clean text from HTML structures
- **Error Recovery**: Handle API blocks, bot detection, and loading issues

## Common Patterns
- YouTube video descriptions with tracklists
- Articles with "Read more" buttons
- Comment sections requiring expansion
- Paginated content
- Modal popups with additional information

## Output Requirements
- Always verify the extracted content matches the request
- Follow any specified format templates exactly
- Include source attribution when relevant
- Handle edge cases (missing content, format variations)

## Failure Recovery
1. If direct API fails → Use browser automation
2. If page blocks access → Try alternative search results
3. If content not found → Search for similar pages
4. If format unclear → Use sensible defaults and document assumptions
