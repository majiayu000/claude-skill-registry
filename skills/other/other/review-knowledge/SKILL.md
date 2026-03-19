---
name: review-knowledge
description: >-
  Review and maintain the knowledge base — find stale entries, orphan entries without connections,
  missing links between related entries, and generate topic summaries. Supports the "internalization"
  phase of knowledge management by surfacing knowledge for periodic review and reflection.
license: MIT
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Review Knowledge

## Goal
Maintain knowledge base health and surface entries for review, helping the user internalize accumulated knowledge through periodic reflection.

## When to Use
- User explicitly requests a knowledge review (e.g., "review knowledge", "check knowledge base")
- At the end of a significant work phase or project milestone
- When the user wants to understand the current state of knowledge on a topic
- Periodically (e.g., weekly/monthly) to keep the knowledge base healthy

## Prerequisites
- `.claude/knowledge/entries/` directory exists with entries created by `record-knowledge`
- `.claude/knowledge/CLAUDE.md` tag registry exists

## Review Modes

Invoke with an optional argument to select a mode. If no argument is given, run **health check**.

### 1. Health Check (default)
Scan the entire knowledge base and report:

#### a. Stale Entries
- Entries older than 90 days with `status: active` — may need review for accuracy
- Detect by comparing `created:` date in frontmatter to the current date
- Report: list of entries with age, title, and tags

#### b. Orphan Entries
- Active entries with NO `- see:` links (disconnected from the knowledge graph)
- These represent isolated knowledge that may be hard to discover in future sessions
- Report: list of orphan entries with title and tags

#### c. Missing Connections
- Find pairs of active entries that share 2+ tags but have no `- see:` link between them
- These are likely related but not explicitly connected
- Report: list of suggested connections with shared tags

#### d. Tag Health
- Tags in entries that are not registered in `.claude/knowledge/CLAUDE.md`
- Tags in the registry that are not used by any entry
- Near-duplicate tags (same rules as record-knowledge similarity check)

#### e. Summary Statistics
- Total entries (active / deprecated)
- Average see links per entry
- Most connected entries (highest see link count)
- Most used tags

#### f. Unidirectional Links
- Entry A has a `- see:` link to entry B, but entry B does NOT have a `- see:` link back to entry A
- These represent broken bidirectional links that reduce discoverability from the target entry's side
- Report: list of unidirectional pairs with source entry, target entry, and direction of missing link

### 2. Topic Review (`topic:<keyword or tag>`)
Deep dive into a specific topic:

1. Search entries by tag or keyword
2. Present a structured summary of all related knowledge:
   - Key facts and decisions
   - Known pitfalls
   - Related entries and their connections
3. Ask the user reflective questions:
   - "Is this still accurate based on your current experience?"
   - "Have you encountered new pitfalls not yet recorded?"
   - "Are there entries that should be deprecated?"

### 3. Fix Mode (`fix`)
Interactively fix issues found in the health check:

1. Run health check first
2. For each issue found, take action:
   - **Orphan entries**: Search for related entries and add see links (using the same search procedure as record-knowledge step 4)
   - **Missing connections**: Add see links between suggested pairs (with user-facing notification)
   - **Unidirectional links**: Add the missing reverse `- see:` link to the target entry so both entries link to each other
   - **Unregistered tags**: Auto-add missing tags to the registry in `.claude/knowledge/CLAUDE.md` under the appropriate section
   - **Unused tags**: Report for manual review (do not auto-delete)
3. Report actions taken

## Output Format

```markdown
# Knowledge Base Review — YYYY-MM-DD

## Health Summary
- Total entries: N (active: N, deprecated: N)
- Orphan entries: N
- Stale entries (>90 days): N
- Missing connections: N suggested
- Unidirectional links: N
- Tag issues: N

## Stale Entries
| Entry | Age | Tags |
|-------|-----|------|
| [title](slug.md) | N days | #tag1 #tag2 |

## Orphan Entries
| Entry | Tags |
|-------|------|
| [title](slug.md) | #tag1 #tag2 |

## Suggested Connections
| Entry A | Entry B | Shared Tags |
|---------|---------|-------------|
| [title](slug.md) | [title](slug.md) | #tag1 #tag2 |

## Unidirectional Links
| Source | Target | Missing Direction |
|--------|--------|-------------------|
| [title](slug.md) | [title](slug.md) | target → source |

## Tag Issues
- Unregistered: #tag1, #tag2
- Unused: #tag3
- Near-duplicates: #foo / #foos
```

## Procedure

1. Glob `.claude/knowledge/entries/*.md` to list all entries
2. Read each entry's YAML frontmatter (title, status, created, tags) and scan for `- see:` lines
3. Read `.claude/knowledge/CLAUDE.md` for the tag registry
4. Analyze and generate the report based on the selected mode
5. If `fix` mode: execute fixes autonomously and report what was changed
6. Output the report to the user (do NOT write it to a file unless requested)
