---
context: fork
---

# /related

Find all notes related to a topic using parallel sub-agents for comprehensive search.

## Usage

```
/related <topic>
/related VendorA
/related Cloud Platform
/related Jane Doe
```

## Instructions

### Phase 1: Planning

1. Analyse the topic to determine:
   - Is it a person? → Focus on Person notes, meetings with them
   - Is it a technology? → Focus on Pages, ADRs, Projects
   - Is it a project? → Focus on Project, Meetings, Tasks
   - Is it an organisation? → Focus on Organisation, People, Meetings

2. Load relevant context file:
   - People topic → `.claude/context/people.md`
   - Tech topic → `.claude/context/technology.md`
   - Project topic → `.claude/context/projects.md`
   - Org topic → `.claude/context/organisations.md`

### Phase 2: Parallel Search (use sub-agents)

Launch 4 sub-agents in parallel using `model: "haiku"` for efficiency:

**Agent 1: Direct Matches** (Haiku)
- Find notes with topic in filename
- Find notes with topic in title frontmatter
- Return: filename, type, title

**Agent 2: Content Search** (Haiku)
- Grep for topic across all .md files in vault root
- Return: filename, matching line, context

**Agent 3: Backlink Analysis** (Haiku)
- If a note exists for topic, find all notes linking TO it
- Return: linking notes with context

**Agent 4: Tag & Metadata Search** (Haiku)
- Search frontmatter for topic in tags, project, organisation fields
- Return: notes with metadata matches

### Phase 3: Compile & Rank Results

```markdown
# Notes Related to: {{topic}}

**Found**: {{count}} related notes

## Direct Matches ({{count}})

Notes specifically about {{topic}}:

| Note | Type | Last Modified |
|------|------|---------------|
{{direct matches}}

## Mentions ({{count}})

Notes that reference {{topic}}:

| Note | Type | Context |
|------|------|---------|
{{content matches with snippet}}

## Linked Notes ({{count}})

Notes connected via wiki-links:

{{backlink results}}

## By Type

### Meetings ({{count}})
{{meeting list}}

### Projects ({{count}})
{{project list}}

### People ({{count}})
{{people list}}

### ADRs ({{count}})
{{adr list}}

### Tasks ({{count}})
{{task list}}

## Suggested Connections

{{identify notes that SHOULD link to each other but don't}}
```
