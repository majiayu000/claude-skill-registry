---
context: fork
---

# /find-decisions

Find all architecture decisions and choices related to a topic using sub-agents.

## Usage

```
/find-decisions <topic>
/find-decisions Kafka
/find-decisions authentication
/find-decisions SAP integration
```

## Instructions

### Phase 1: Planning

1. Identify search terms from the topic
2. Plan search across multiple note types:
   - ADRs (primary source)
   - Meeting notes (decisions made sections)
   - Project files (architectural notes)
   - Pages (technical documentation)

### Phase 2: Parallel Search (use sub-agents)

Launch these sub-agents in parallel using `model: "haiku"` for efficiency:

**Agent 1: ADR Search** (Haiku)
- Search all `ADR - *.md` files
- Look for topic in title, context, decision sections
- Extract: title, status, decision summary, date

**Agent 2: Meeting Decisions** (Haiku)
- Search `+Meetings/Meeting - *.md` files
- Focus on "Decisions Made" and "Action Items" sections
- Look for topic keywords
- Extract: date, meeting name, decision text

**Agent 3: Technical Documentation** (Haiku)
- Search `Page - *.md` files
- Look for architectural/technical content about topic
- Extract relevant sections

**Agent 4: Project References** (Haiku)
- Search `Project - *.md` files
- Find projects that involve this topic
- Note any architectural decisions mentioned

### Phase 3: Compile Results

```markdown
# Decisions Related to: {{topic}}

**Search Date**: {{DATE}}
**Results Found**: {{count}}

## Architecture Decision Records

| ADR | Status | Decision | Date |
|-----|--------|----------|------|
{{ADR results}}

### ADR Details

#### {{ADR Title}}
- **Status**: {{status}}
- **Decision**: {{summary}}
- **Rationale**: {{key points}}
- **Link**: [[ADR - {{title}}]]

## Decisions from Meetings

| Date | Meeting | Decision |
|------|---------|----------|
{{meeting decisions}}

## Related Projects

{{projects involving this topic}}

## Technical Documentation

{{relevant pages with summaries}}

## Timeline

{{chronological view of decisions}}

## Gaps Identified

{{note if there are areas without documented decisions}}
```

4. Highlight any conflicting decisions or areas needing clarification
