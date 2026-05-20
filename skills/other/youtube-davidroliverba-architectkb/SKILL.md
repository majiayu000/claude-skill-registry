---
context: fork
---

# /youtube

Save a YouTube video as both a Weblink (quick reference) and a detailed Page (full analysis).

## Usage

```
/youtube <url>
/youtube <url> <optional title override>
```

## Examples

```
/youtube https://www.youtube.com/watch?v=0TpON5T-Sw4
/youtube https://youtu.be/abc123 AWS re:Invent Keynote
```

## Prerequisites

This skill uses the MCP Docker YouTube tools:
- `mcp__MCP_DOCKER__get_video_info` - Video metadata
- `mcp__MCP_DOCKER__get_transcript` - Full transcript

## Instructions

### 1. Fetch Video Data

Use both tools in parallel:
```
mcp__MCP_DOCKER__get_video_info(url)
mcp__MCP_DOCKER__get_transcript(url)
```

Extract:
- Title, channel name, duration, upload date
- Description (contains links, chapters)
- Full transcript text

If transcript unavailable, note this and proceed with description-only analysis.

### 2. Parse Chapter Markers

If the description contains chapter timestamps (e.g., `00:00 - Introduction`), extract these as structured sections for the Page note.

### 3. Analyse Content

From the transcript, identify:
- **Core thesis** - Main argument or purpose
- **Key concepts** - Major ideas, frameworks, principles
- **Actionable insights** - What viewers should do
- **Technologies/tools** - Any mentioned tech stack
- **Notable quotes** - 2-4 memorable statements
- **Relevance to your organization** - Architecture, governance, engineering work

### 4. Create Weblink Note

**Filename:** `Weblink - {{sanitised title}}.md`
**Location:** Vault root

```markdown
---
type: Weblink
title: "{{title}}"
url: {{youtube_url}}
domain: youtube.com
createdAt: {{ISO timestamp}}
created: {{DATE}}
modified: {{DATE}}
tags: [video, {{3-5 relevant tags}}]
---

# {{title}}

**Channel:** {{channel name}}
**Duration:** {{duration}}
**Published:** {{upload date}}

## Summary

{{3-5 sentence summary of video content and main thesis}}

## Key Topics

- {{topic 1}}
- {{topic 2}}
- {{topic 3}}

## Links

- **Video:** {{url}}
- **Channel:** {{channel URL if extractable}}
- **Resources:** {{any links from description}}

## Related

- [[Page - {{title}} - Full Analysis]]
```

### 5. Create Page Note (Full Analysis)

**Filename:** `Page - {{sanitised title}} - Full Analysis.md`
**Location:** Vault root

```markdown
---
type: Page
title: "{{title}} - Full Analysis"
created: {{DATE}}
modified: {{DATE}}
tags: [video, activity/research, {{topic tags}}]
confidence: high
freshness: current
source: secondary
verified: true
reviewed: {{DATE}}
summary: {{one-line summary}}
---

# {{title}} - Full Analysis

**Source:** [[Weblink - {{title}}]]
**Author:** {{channel name}}
**Duration:** {{duration}}

## Core Thesis

{{1-2 paragraphs explaining the main argument or purpose}}

## Key Concepts

### {{Concept 1 Name}}

{{Explanation with context}}

### {{Concept 2 Name}}

{{Explanation with context}}

{{Continue for major concepts}}

## Actionable Insights

1. {{Insight 1}}
2. {{Insight 2}}
3. {{Insight 3}}

## Technologies/Tools Mentioned

| Tool | Purpose |
|------|---------|
| {{tool 1}} | {{what it does}} |
| {{tool 2}} | {{what it does}} |

## Notable Quotes

> "{{quote 1}}"

> "{{quote 2}}"

## Relevance to Your Organization Work

{{How this relates to Solutions Architecture, YourOrg projects, or current work. Remove if not applicable.}}

## Chapter Summary

{{If chapters available, list each with 1-2 sentence summary}}

## Transcript

<details>
<summary>Full Transcript (click to expand)</summary>

{{full transcript, cleaned for readability with paragraph breaks}}

</details>

## Related Notes

- {{wiki-links to related vault notes}}

## Resources

- {{Links from video description}}
```

### 6. Transcript Formatting

- Add paragraph breaks at natural pauses
- Clean up filler words where excessive
- Preserve speaker changes if multiple speakers
- Keep chapter markers if present

### 7. Tag Selection

**Always include:** `video`

**Topic tags (choose 3-5):**
- `ai`, `automation`, `productivity` for AI/productivity content
- `technology/{{tech}}` for specific technologies
- `activity/research` for learning content
- `domain/{{area}}` for business domains

### 8. Find Related Notes

Search vault for:
- Similar topics or technologies
- Related projects
- People mentioned
- Previous videos from same channel

Add wiki-links in Related section.

### 9. Completion

Report:
- Both file paths created
- Brief summary of video content
- Key relevance if applicable
- Channel name for reference

## Quality Standards

- **Always** fetch transcript - never create without attempting
- **Always** create BOTH Weblink and Page notes
- **Always** link them together bidirectionally
- **Provide** meaningful analysis, not just metadata
- **Extract** minimum 3 key concepts for substantive videos
- **Include** full transcript in collapsible section
- **Use** UK English throughout
- **Sanitise** titles for filenames (remove special characters)

## Example Output

For a 30-minute productivity video:
- `Weblink - Building a Second Brain with AI.md` (quick reference)
- `Page - Building a Second Brain with AI - Full Analysis.md` (detailed breakdown)

Both linked together for easy navigation.
