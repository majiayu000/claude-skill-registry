---
name: obsidian-vault-intelligence
description: Use when working with Obsidian vault via MCP - covers effective search patterns, note operations, intelligent queries, and cross-reference strategies for knowledge extraction
---

# Obsidian Vault Intelligence via MCP

## When to Use This Skill

Invoke this skill when you need to:
- Search user's Obsidian vault for project context, decisions, or strategic information
- Retrieve specific notes about companies, projects, or technical approaches
- Query vault for patterns, themes, or cross-referenced information
- Create or update notes with new insights or action items
- Find backlinks to understand note relationships
- Extract knowledge for research, planning, or decision-making

## Core Principles

1. **Progressive Search**: Start broad with intelligent_search, narrow with specific tools
2. **Context Preservation**: Capture full note content when relevant for decision-making
3. **Cross-Reference Intelligence**: Use backlinks to understand note relationships
4. **Smart Queries**: Use natural language for vault queries, specific patterns for search
5. **Note Hygiene**: When creating/updating, follow existing vault conventions

## Available MCP Tools

### Primary Tools

- **query_vault**: Natural language queries about vault contents (best for: "what do I know about X?")
- **intelligent_search**: Advanced search with link analysis and tag hierarchies (best for: finding related notes)
- **search_notes**: Keyword/phrase search in filenames or content (best for: finding specific terms)
- **get_note**: Retrieve full note content by path (best for: reading specific notes)
- **get_backlinks**: Find all notes linking to a target note (best for: understanding relationships)

### Secondary Tools

- **write_note**: Overwrite note with new content (use sparingly - destructive)
- **create_note**: Create new note with frontmatter (requires title, path)
- **append_to_note**: Add content to end of existing note (best for: adding updates)
- **update_note_section**: Update specific heading section (best for: targeted updates)
- **list_directories**: List vault structure (best for: understanding organization)

### Advanced Tools

- **guided_path**: Generate narrative tour through linked notes from a seed note
- **audit_recent_notes**: Find recently modified notes missing required structure
- **contextual_companions**: Suggest related notes based on topic or seed note
- **fresh_energy**: Find recent notes lacking backlinks (integration opportunities)
- **initiative_bridge**: Identify initiative-tagged notes with outstanding tasks
- **pattern_echo**: Find notes reusing specific phrasing or patterns
- **synthesis_ready**: Flag note clusters that need synthesis/summary note

## Search Strategy Patterns

### Pattern 1: Discovery (What do I know about X?)

```
Use: mcp__obsidian__query_vault
Query: "What do I know about Partner Project's protein interaction prediction technology?"

Result: Natural language summary with relevant context
```

**When to use**: Starting point for unfamiliar topics, broad context gathering

### Pattern 2: Specific Term Search

```
Use: mcp__obsidian__search_notes
SearchTerm: "protein-protein interaction"
SearchType: "both" (filename and content)

Result: List of notes containing the exact term
```

**When to use**: Finding notes mentioning specific technical terms, company names, or concepts

### Pattern 3: Intelligent Context Search

```
Use: mcp__obsidian__intelligent_search
Query: "LightForge Works email marketing campaign with Clay and Attio"

Result: Ranked results with link analysis and structural context
```

**When to use**: Multi-concept searches, finding related notes across different areas

### Pattern 4: Relationship Mapping

```
# Step 1: Find seed note
Use: mcp__obsidian__search_notes
SearchTerm: "Partner Project Master Command Center"

# Step 2: Get backlinks
Use: mcp__obsidian__get_backlinks
NotePath: "Areas/Companies/Partner Project/Partner Project Master Command Center.md"

Result: All notes linking to command center (related projects, meetings, action items)
```

**When to use**: Understanding how a topic connects to other work, finding related contexts

### Pattern 5: Recent Activity Analysis

```
Use: mcp__obsidian__fresh_energy
HoursBack: 48
MinWords: 80
Limit: 10

Result: Recently updated substantive notes that lack integration (backlinks)
```

**When to use**: Weekly reviews, finding recent work that needs cross-referencing

## Common Use Case Workflows

### Use Case: Strategic Context for Meeting

**Goal**: Prepare for Partner Project partnership discussion

```markdown
Step 1: Query for overview
mcp__obsidian__query_vault("Partner Project partnership status, technology details, and strategic next steps")

Step 2: Get command center details
mcp__obsidian__get_note(notePath: "Areas/Companies/Partner Project/Partner Project Master Command Center.md")

Step 3: Find related action items
mcp__obsidian__search_notes(searchTerm: "Partner Project", searchType: "content")
Filter results for notes in "next_up/Action Items/"

Step 4: Check recent meeting notes
mcp__obsidian__intelligent_search("Partner Project meetings 2025")

Step 5: Get market research prompt
mcp__obsidian__get_note(notePath: "Areas/Companies/Partner Project/market_research/Partner Project Market Analysis Research Prompt.md")
```

### Use Case: Project Discovery

**Goal**: Find all information about a specific project

```markdown
Step 1: Intelligent search for project
mcp__obsidian__intelligent_search("LightForge Works micro-application development business")

Step 2: Get project note
mcp__obsidian__get_note(notePath: "[path from search results]")

Step 3: Find related notes
mcp__obsidian__get_backlinks(notePath: "[project note path]")

Step 4: Check for recent updates
mcp__obsidian__fresh_energy(hoursBack: 168)  # Last week
Filter for project-related notes

Step 5: Find action items
mcp__obsidian__search_notes(searchTerm: "@paia", searchType: "content")
Filter for project-specific paia tags
```

### Use Case: Research Synthesis

**Goal**: Extract knowledge for market research report

```markdown
Step 1: Query for thematic overview
mcp__obsidian__query_vault("What research have I done on pharmaceutical drug discovery market and protein interaction prediction competitors?")

Step 2: Pattern search for specific insights
mcp__obsidian__pattern_echo(snippet: "AlphaFold accuracy")

Step 3: Find synthesis opportunities
mcp__obsidian__synthesis_ready(minClusterSize: 3)
Identify if research notes need a synthesis document

Step 4: Get detailed notes
For each relevant note from steps 1-3:
  mcp__obsidian__get_note(notePath: "[note path]")

Step 5: Create synthesis note
mcp__obsidian__create_note(
  notePath: "Areas/Companies/Partner Project/market_research/Competitive Landscape Synthesis.md",
  title: "Competitive Landscape Synthesis",
  content: "[synthesized content]"
)
```

### Use Case: Task Management Integration

**Goal**: Find outstanding tasks across projects

```markdown
Step 1: Find initiative-tagged tasks
mcp__obsidian__initiative_bridge(
  initiative: "Partner Project",
  frontmatterField: "project"
)

Step 2: Search for @paia tags
mcp__obsidian__search_notes(searchTerm: "@paia-updater", searchType: "content")

Step 3: Check recent notes for unprocessed items
mcp__obsidian__audit_recent_notes(
  hoursBack: 72,
  requiredFields: ["status", "priority"]
)

Step 4: Get specific action plan
mcp__obsidian__get_note(notePath: "next_up/Action Items/[specific action plan].md")
```

### Use Case: Knowledge Connection

**Goal**: Find related notes to create strategic connections

```markdown
Step 1: Find contextual companions for a topic
mcp__obsidian__contextual_companions(
  topic: "multi-agent AI coordination",
  limit: 5
)

Step 2: Generate narrative tour
mcp__obsidian__guided_path(
  notePath: "Areas/Tech/Development/Claude Code Multi-Agent Patterns.md",
  supportingLimit: 3,
  counterpointLimit: 2
)

Step 3: Update note with cross-references
mcp__obsidian__update_note_section(
  notePath: "[target note]",
  sectionHeading: "Related Concepts",
  newContent: "[connections from steps 1-2]"
)
```

## Note Operations Best Practices

### Creating Notes

```
Use: mcp__obsidian__create_note

Requirements:
- notePath: Full path relative to vault root
- title: Clear, descriptive title
- content: Well-structured markdown
- tags: Relevant tags array (optional)

Pattern:
notePath: "Areas/[Category]/[Subcategory]/[Title].md"
title: "Descriptive Title"
tags: ["tag1", "tag2"]
content: |
  # Title

  ## Overview
  Context and purpose

  ## Key Points
  - Point 1
  - Point 2

  ## Related
  - [[Related Note 1]]
  - [[Related Note 2]]
```

### Updating Notes

```
PREFER: mcp__obsidian__update_note_section
Over: write_note (destructive) or append_to_note (less precise)

Pattern:
1. Read current note: get_note
2. Identify target section heading
3. Update only that section: update_note_section

Example:
notePath: "Areas/Companies/Partner Project/Partner Project Master Command Center.md"
sectionHeading: "Next Steps"
newContent: |
  - Execute comprehensive market research
  - Schedule follow-up with partner contact
  - Prepare partnership proposal
```

### Appending Updates

```
Use: mcp__obsidian__append_to_note
When: Adding new information to end of note (meeting updates, action items)

Pattern:
notePath: "[existing note path]"
content: |

  ## Update [Date]
  New information or action items
  - Action 1
  - Action 2
```

## Vault Structure Intelligence

user's vault organization (common paths):

```
Areas/
  ├── Companies/              # Client and partnership companies
  │   ├── Partner Project/
  │   ├── Company B/
  │   └── LightForge/
  ├── Tech/                   # Technical notes and development
  │   ├── Development/
  │   └── Tools/
  └── Projects/               # Active projects

next_up/
  ├── Action Items/           # Actionable tasks
  ├── Opportunities/          # Business opportunities
  │   └── Active/
  └── Research/               # Ongoing research

people/                       # Contact and relationship notes

daily/                        # Daily notes (date-based)
```

## Search Query Optimization

### Natural Language Queries (query_vault)

**Good**: "What are my next steps for the Partner Project partnership?"
**Better**: "What are my next steps for Partner Project partnership development, including market research tasks and strategic priorities?"

### Keyword Searches (search_notes)

**Good**: "LightForge"
**Better**: "LightForge Works" (more specific)
**Best**: Use searchType: "both" to search filenames and content

### Intelligent Searches (intelligent_search)

**Good**: "protein prediction"
**Better**: "protein-protein interaction prediction market pharmaceutical"
**Best**: Include context words that appear in related notes

## Integration with Other Skills

### With coordinating-sub-agents

```
Coordinator Claude workflow:
1. Query vault for strategic context: mcp__obsidian__query_vault
2. Get specific notes: mcp__obsidian__get_note
3. Delegate task to sub-agent with context
4. After completion: append_to_note with results
```

### With syncing-task-completions

```
Sync workflow:
1. Search for task notes: mcp__obsidian__search_notes(searchTerm: "TODO")
2. For each project, find action items: intelligent_search
3. Update master task list: update_note_section
4. Append completion dates: append_to_note
```

### With processing-paia-tags

```
PAIA processing workflow:
1. Search for @paia tags: search_notes(searchTerm: "@paia")
2. Get full note content: get_note
3. Analyze cross-references: get_backlinks
4. Execute @paia instruction
5. Update note status: update_note_section
```

### With learning-from-outcomes

```
Learning workflow:
1. Query vault for past similar situations: query_vault
2. Find pattern echoes: pattern_echo
3. Create synthesis: create_note
4. Link to related notes: update_note_section with [[links]]
```

## Performance Optimization

### Minimize API Calls

**Bad**: Multiple get_note calls for discovery
```
get_note(path1)
get_note(path2)
get_note(path3)
```

**Good**: Use search/query to identify, then get_note only what you need
```
search_results = search_notes("Partner Project")
# Filter in memory to top 2 most relevant
get_note(top_result_1)
get_note(top_result_2)
```

### Batch Related Operations

**Bad**: Search, read, search, read
**Good**: Search all, read all relevant

### Cache Context

**Bad**: Re-query vault for same information
**Good**: Query once, use results for entire workflow

## Error Handling

```python
# When note path might not exist
try:
    note = mcp__obsidian__get_note(notePath: "Areas/Companies/Unknown/Note.md")
except:
    # Fall back to search
    results = mcp__obsidian__search_notes(searchTerm: "Unknown Company", searchType: "both")

# When search returns no results
results = mcp__obsidian__search_notes(searchTerm: "obscure-term")
if not results or len(results) == 0:
    # Try broader query
    results = mcp__obsidian__query_vault("What do I know related to obscure-term?")
```

## Vault Query Checklist

Before querying Obsidian vault:

- [ ] **Search Strategy**: Have I chosen the right tool (query_vault vs search_notes vs intelligent_search)?
- [ ] **Query Clarity**: Is my query specific enough to get relevant results?
- [ ] **Breadth-First**: Am I starting broad (search/query) before narrow (get_note)?
- [ ] **Relationship Mapping**: Do I need backlinks to understand context?
- [ ] **Result Filtering**: Can I filter results programmatically to reduce API calls?
- [ ] **Update Plan**: If I'm updating notes, am I using update_note_section over write_note?
- [ ] **Cross-References**: Should I link this work to related notes?

## Common Patterns Summary

| Goal | Primary Tool | Secondary Tool | Notes |
|------|-------------|----------------|-------|
| "What do I know about X?" | query_vault | intelligent_search | Start here for discovery |
| Find specific term | search_notes | grep content | Use searchType: "both" |
| Related notes | get_backlinks | contextual_companions | Understand relationships |
| Read specific note | get_note | - | Only after identifying path |
| Recent activity | fresh_energy | audit_recent_notes | Weekly review pattern |
| Create new note | create_note | - | Use full paths |
| Update existing | update_note_section | append_to_note | Prefer section updates |
| Find clusters | synthesis_ready | intelligent_search | Identify synthesis needs |
| Task tracking | initiative_bridge | search_notes @paia | Project management |

## Obsidian Vault as Strategic Intelligence

Think of the Obsidian vault as user's:
- **Strategic Memory**: Past decisions, approaches, learnings
- **Project Context**: Current initiatives, next steps, blockers
- **Relationship Map**: Connections between concepts, projects, people
- **Task System**: @paia tags, action items, initiative tracking
- **Research Archive**: Market analysis, competitive intelligence, technical explorations

Use it proactively to:
- Inform delegation decisions with past context
- Avoid re-solving already-solved problems
- Understand user's preferences and approaches
- Connect new work to existing strategic priorities
- Capture learnings and insights for future sessions
