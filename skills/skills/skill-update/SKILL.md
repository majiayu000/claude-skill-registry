---
name: skill-update
description: Self-improvement protocol for Neo4j agents. Instructs agents to report skill updates needed.
---

# Skill Update Protocol

**MANDATORY: Before returning results, check if skill files need updates.** This is not optional.

## Report Format

You cannot edit files directly. Instead, include this block in your response:

```
SKILL_UPDATE_NEEDED
action: ADD | CORRECT | REMOVE
file: /full/path/to/SKILL.md
content: |
  the exact content to add, correct, or remove
reason: why this update is needed
```

The main agent will execute the edit.

## When to Report

### ADD - New Discovery
You found a working query pattern or data gap not in the skill file.

**Data gaps include:**
- Schema tool returned incomplete/incorrect data
- Query returned unexpected empty/null results
- Data didn't match documented expectations
- Property name different than expected (camelCase vs snake_case)

### CORRECT - Wrong Entry
You see an entry in Known Data Gaps that is incorrect based on your queries.

### REMOVE - Outdated Entry
You see an entry that's no longer true (issue was fixed, data now exists).

## Skill File Paths

| Domain | Path | Scope |
|--------|------|-------|
| Schema | `/home/faisal/EventMarketDB/.claude/skills/neo4j-schema/SKILL.md` | Schema issues, MCP tool gaps |
| Entity | `/home/faisal/EventMarketDB/.claude/skills/neo4j-entity/SKILL.md` | Company, Sector, Industry |
| Report | `/home/faisal/EventMarketDB/.claude/skills/neo4j-report/SKILL.md` | SEC filings, exhibits |
| News | `/home/faisal/EventMarketDB/.claude/skills/neo4j-news/SKILL.md` | News, fulltext/vector |
| Transcript | `/home/faisal/EventMarketDB/.claude/skills/neo4j-transcript/SKILL.md` | Transcripts, Q&A |
| XBRL | `/home/faisal/EventMarketDB/.claude/skills/neo4j-xbrl/SKILL.md` | XBRL facts, concepts |

## Rules

- Use generic patterns (`$param`, not hardcoded values)
- Don't duplicate existing patterns
- Don't report failed/empty queries as patterns
- Include exact content so main agent can copy-paste

---
*Version 1.4 | 2026-01-11 | Changed to report-based updates*
