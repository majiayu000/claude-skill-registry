---
name: cross-linking
description: Guidance for finding and adding bidirectional wikilinks when creating or updating content in the knowledge base. Use when user creates new content or wants to improve discoverability by adding links to related pages. Helps maintain the interconnected graph structure.
---

# Cross-Linking

Maintain bidirectional links for discoverability and graph navigation.

## What to Link

### Always Link
| Content Type | Link To | Example |
|--------------|---------|---------|
| People | Person profile | `[[Alice Smith]]` not "Alice" |
| Projects | Project README | `[[AGI-Assistant]]` |
| Tasks | Task file | `[[Integrate-Zep-Memory]]` |
| Meetings | Meeting note | `[[2026-01-12 Weekly Sync]]` |
| Tools/Tech | Research entry | `[[Zep]]`, `[[LangChain]]` |

### On First Mention
Link concepts, tools, and references on their first appearance in a document.

## Link Syntax

### Basic Wikilink
```markdown
[[Page Name]]
```

### With Display Text
```markdown
[[Page-Name|Display Text]]
[[Team/Alice-Smith|Alice]]
```

### With Relative Path
```markdown
[[../Team/Alice-Smith|Alice Smith]]
[[../../04-Knowledge/AI-Ecosystem/Zep|Zep]]
```

## Finding Related Content

### By Topic
Search for related pages in the same category:
- AI tools → `04-Knowledge/AI-Ecosystem/`
- Projects → `03-Projects/`
- Team → `01-Team/`

### By Tag
Find pages with similar tags:
```
#project/agi-assistant
#topic/ai
#team/member
```

### By Existing Links
Check what the page already links to, then find related pages that should also be linked.

## Linking Checklist

When creating/editing content:

1. **People mentioned?** → Link to profiles in `01-Team/`
2. **Projects referenced?** → Link to project READMEs
3. **Tasks discussed?** → Link to task files
4. **Tools/tech mentioned?** → Link to AI-Ecosystem entries
5. **Related knowledge?** → Link to relevant research pages
6. **Meetings referenced?** → Link to meeting notes

## Bidirectional Linking

Obsidian automatically creates backlinks, but for better navigation:

1. **Link from new page** to existing related content
2. **Consider updating** related pages to link back (for important connections)

## Common Link Targets

### Team
- Link to team member profiles in `Database/People/`

### Projects
- Link to project documentation in `Projects/` or `Database/Projects/`

### AI Ecosystem Categories
- `[[Agent-Frameworks]]`
- `[[LLM-Providers]]`
- `[[Developer-Tools]]`
- `[[MCP-Ecosystem]]`
- `[[Vector-Databases]]`

## Example

Before:
```markdown
Alice is working on the authentication integration for our web app project.
```

After:
```markdown
[[Alice Smith]] is working on the [[OAuth]] integration for our [[Web App]] project.
```
