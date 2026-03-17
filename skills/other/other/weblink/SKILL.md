---
context: fork
---

# /weblink

Save a URL as a weblink note with analysis and summary.

## Usage

```
/weblink <url>
/weblink <url> <optional title>
```

## Examples

```
/weblink https://github.com/anthropics/claude-code
/weblink https://aws.amazon.com/bedrock/ AWS Bedrock Service
```

## Instructions

1. **Fetch and analyse the URL**:
   - Use WebFetch to retrieve the page content
   - Extract: title, author, source/domain, main content
   - **ALWAYS provide analysis** - this is mandatory, not optional

2. **Generate analysis** (REQUIRED):
   - Write a 2-3 sentence summary of what the resource is
   - Extract 4-8 key points as bullet points
   - Identify relevance to your organization/Solutions Architecture work where applicable
   - Note any technical details (technologies, integrations, versions)

3. **Generate filename**: `Weblink - {{title}}.md`

4. **Create weblink in vault root**:

```markdown
---
type: Weblink
title: {{title}}
created: {{DATE}}
modified: {{DATE}}
tags: [{{relevant tags}}]
url: {{url}}
domain: {{domain}}
author: {{author or null}}
source: {{source name}}
---

# {{title}}

## Source

- **URL:** {{url}}
- **Author:** {{author}}
- **Source:** {{source}}

## Summary

{{2-3 sentence summary of the resource}}

## Key Points

- {{key point 1}}
- {{key point 2}}
- {{key point 3}}
- {{...more as relevant}}

## Relevance to your organization

{{How this relates to YourOrg work, if applicable. Remove section if not relevant.}}

## Related

- {{wiki-links to related notes in vault}}
```

5. **Tag extraction**:
   - Identify 2-5 relevant tags from content
   - Use existing vault tags where possible (check other notes)
   - Common tags: AWS, SAP, MCP, AI, architecture, integration, security

6. **Find related notes**:
   - Search vault for related topics
   - Add wiki-links to relevant existing notes
   - Consider: projects, technologies, people, other weblinks

7. **After creating**:
   - Confirm creation with file path
   - Show brief summary of what was saved
   - Mention key relevance if applicable

## Quality Standards

- **Never** create a weblink without fetching and analysing the content first
- **Always** include a meaningful summary (not just the page title)
- **Always** extract key points - minimum 3, maximum 8
- **Check** for existing related notes to link to
- Use UK English throughout
