---
name: extract-wisdom
description: Extract wisdom, insights, and actionable takeaways from text sources. Use when asked to analyse, summarise, or extract key learnings from blog posts, articles, markdown files, or other text content.
---

# Text Wisdom Extraction

## Overview

Extract meaningful insights, key learnings, and actionable wisdom from written content. This skill handles both web-based sources (blog posts, articles) and local text files (markdown, plain text), performing analysis and presenting findings conversationally or saving to markdown files. The user will likely want you to use this skill when they need to gain understanding from large amounts of text, identify important points, or distil complex information into practical takeaways.

## When to Use This Skill

Activate this skill when users request:
- Analysis or summary of blog posts, articles, or web content
- Extraction of key insights or learnings from text sources
- Identification of notable quotes or important statements
- Structured breakdown of written content
- Actionable takeaways from informational or educational text
- Analysis of local text or markdown files

If the user provides a Youtube URL, stop and use the youtube-wisdom skill instead if it is available.

## Workflow

### Step 1: Identify Source Type

Determine whether the source is a URL or local file:

**URL patterns**:
- Use WebFetch tool to extract content
- WebFetch automatically converts HTML to markdown

**File paths**:
- Use Read tool to load content directly
- Handles .txt, .md, and other text formats

### Step 2: Extract Content

**For URLs (blog posts, articles)**:
```
Use WebFetch with prompt: "Extract the main article content"
```
WebFetch returns cleaned markdown-formatted content ready for analysis.

**For local files**:
```
Use Read tool with the file path
```
Read returns the raw file content for analysis.

### Step 3: Analyse and Extract Wisdom

Perform analysis on the content, extracting:

#### 1. Key Insights & Takeaways
- Identify main ideas, core concepts, and central arguments
- Extract fundamental learnings and important revelations
- Highlight expert advice, best practices, or recommendations
- Note any surprising or counterintuitive information

#### 2. Notable Quotes (if applicable)
- Extract memorable, impactful, or particularly well-articulated statements
- Include context when relevant
- Focus on quotes that encapsulate key ideas or provide unique perspectives
- Preserve original wording exactly

#### 3. Structured Summary
- Create hierarchical organisation of content
- Break down into logical sections or themes
- Provide clear headings reflecting content structure
- Include high-level overview followed by detailed breakdowns
- Note important examples, case studies, or data points

#### 4. Actionable Takeaways
- List specific, concrete actions readers can implement
- Frame as clear, executable steps
- Prioritise practical advice over theoretical concepts
- Include any tools, resources, or techniques mentioned
- Distinguish between immediate actions and longer-term strategies

### Step 4: Present Findings

**Default behaviour**: Present analysis in conversation

**Optional file save**: When user requests markdown output, create a file with this structure:

**File location**: User-specified or `~/Downloads/text-wisdom/<sanitised-title>.md`

**Format**:
```markdown
# Analysis: [Title or URL]

**Source**: [URL or file path]
**Analysis Date**: [YYYY-MM-DD]

## Summary
[2-3 sentence overview of the main topic and key points]

## Key Insights
- [Insight 1 with supporting detail]
- [Insight 2 with supporting detail]
- [Insight 3 with supporting detail]

## Notable Quotes (Only include if there are notable quotes)
> "[Quote 1]"

Context: [Brief context if needed]

> "[Quote 2]"

Context: [Brief context if needed]

## Structured Breakdown
### [Section 1 Title]
[Content summary]

### [Section 2 Title]
[Content summary]

## Actionable Takeaways
1. [Specific action item 1]
2. [Specific action item 2]
3. [Specific action item 3]

## Additional Resources
[Any tools, links, or references mentioned in the content]
```

After writing the analysis file (if requested), inform the user of the location.

## Additional Capabilities

### Multiple Source Analysis
When analysing multiple sources:
- Process each source sequentially using the workflow above
- Create comparative analysis highlighting common themes or contrasting viewpoints
- Synthesise insights across sources in a unified summary

### Topic-Specific Focus
When user requests focused analysis on specific topics:
- Search content for relevant keywords and themes
- Extract only content related to specified topics
- Provide concentrated analysis on areas of interest

### Different Content Types
Handles various text formats:
- Blog posts and articles (via URL)
- Markdown documentation
- Plain text files
- Technical papers (as text)
- Meeting transcripts
- Long-form essays
- Any web page with readable text content

## Tips

- Don't add new lines between items in a list
- Avoid marketing speak, fluff or other unnecessary verbiage such as "comprehensive", "cutting-edge", "state-of-the-art", "enterprise-grade" etc.
- Always use Australian English spelling
- Do not use em-dashes or smart quotes
- Only use **bold** where emphasis is truly needed
- Ensure clarity and conciseness in summaries and takeaways
- Always ask yourself if the sentence adds value - if not, remove it
- You can consider creating mermaid diagrams to explain complex concepts, relationships, or workflows found in the text
